"""
Test Auto-Fixer: Automatically fixes test failures by sending errors back to LLM.

This module implements a self-healing test generation system that:
1. Runs generated tests
2. Captures errors and failures
3. Sends errors back to LLM with context
4. Gets improved test code
5. Retries up to 3 times
"""

import logging
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json

logger = logging.getLogger(__name__)


class TestAutoFixer:
    """Automatically fixes test failures using LLM feedback loop."""

    def __init__(self, llm_client=None, max_retries: int = 3):
        """
        Initialize the auto-fixer.

        Args:
            llm_client: LLM client for generating fixes
            max_retries: Maximum number of fix attempts (default: 3)
        """
        self.llm_client = llm_client
        self.max_retries = max_retries
        self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LLM client if not provided."""
        if not self.llm_client:
            try:
                # Check if API key is set
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    logger.error("OPENAI_API_KEY not set - auto-fix will not work!")
                    logger.error("Please set OPENAI_API_KEY in GitHub Secrets")
                    self.llm_client = None
                    return

                from rag_pipeline import LLMModelFactory

                model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
                self.llm_client = LLMModelFactory.get_llm(model_name)
                logger.info(f"✅ Initialized LLM for auto-fixing: {model_name}")
            except Exception as e:
                logger.error(f"❌ Could not initialize LLM for auto-fixing: {e}")
                logger.error("Auto-fix will be skipped")
                self.llm_client = None

    def run_tests_and_capture_errors(
        self, test_file_path: str, language: str = "python"
    ) -> Tuple[bool, str, str]:
        """
        Run tests and capture output/errors.

        Args:
            test_file_path: Path to the test file
            language: Programming language (python, javascript, go, java)

        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            if language == "python":
                # Try to find pytest - check multiple possible locations
                pytest_cmd = None
                for cmd_try in ["python3", "-m", "pytest"], ["python", "-m", "pytest"], ["pytest"]:
                    try:
                        # Test if command works
                        test_result = subprocess.run(
                            cmd_try + ["--version"],
                            capture_output=True,
                            timeout=5
                        )
                        if test_result.returncode == 0:
                            pytest_cmd = cmd_try
                            break
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        continue

                if not pytest_cmd:
                    logger.error("pytest not found! Tried: python3 -m pytest, python -m pytest, pytest")
                    return False, "", "Error running tests: pytest not found. Install pytest or ensure it's in PATH."

                cmd = pytest_cmd + [test_file_path, "-v", "--tb=short", "--no-header"]
            elif language == "javascript":
                cmd = ["npm", "test", "--", test_file_path]
            elif language == "go":
                cmd = ["go", "test", "-v", test_file_path]
            elif language == "java":
                cmd = ["mvn", "test", f"-Dtest={Path(test_file_path).stem}"]
            else:
                raise ValueError(f"Unsupported language: {language}")

            # Find project root for test execution
            test_path = Path(test_file_path).resolve()

            # Try to find project root by looking for common markers
            current = test_path.parent
            project_root = None

            # Look for project root indicators
            root_markers = [
                ".git",
                "setup.py",
                "pyproject.toml",
                "package.json",
                "go.mod",
                "pom.xml",
                "requirements.txt",
            ]

            while current != current.parent:
                if any((current / marker).exists() for marker in root_markers):
                    project_root = current
                    break
                current = current.parent

            # Fallback to current working directory
            if not project_root:
                project_root = Path.cwd()

            logger.info(f"Running tests from project root: {project_root}")
            logger.info(f"Test file: {test_file_path}")

            # Set PYTHONPATH to include project root for Python tests
            env = os.environ.copy()
            if language == "python":
                pythonpath = str(project_root)
                if "PYTHONPATH" in env:
                    pythonpath = f"{pythonpath}{os.pathsep}{env['PYTHONPATH']}"
                env["PYTHONPATH"] = pythonpath
                logger.info(f"Set PYTHONPATH: {pythonpath}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(project_root),
                env=env,
            )

            success = result.returncode == 0
            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return False, "", "Test execution timed out after 60 seconds"
        except FileNotFoundError as e:
            error_msg = f"Command not found: {e}. Make sure the test framework is installed."
            logger.error(error_msg)
            return False, "", error_msg
        except Exception as e:
            return False, "", f"Error running tests: {str(e)}"

    def extract_error_details(
        self, stdout: str, stderr: str, language: str = "python"
    ) -> Dict[str, Any]:
        """
        Extract structured error information from test output.

        Args:
            stdout: Standard output from test run
            stderr: Standard error from test run
            language: Programming language

        Returns:
            Dictionary with error details
        """
        error_info = {
            "language": language,
            "errors": [],
            "failures": [],
            "raw_output": stdout + "\n" + stderr,
        }

        combined_output = stdout + "\n" + stderr
        lines = combined_output.split("\n")

        # Check for pytest/test framework not found errors
        if "Error running tests" in combined_output or "No such file or directory" in combined_output:
            error_info["errors"].append({
                "type": "EnvironmentError",
                "message": stderr.strip() or stdout.strip() or "Test framework not available",
                "context": combined_output[:1000]
            })
            return error_info

        if language == "python":
            # Extract collection errors (pytest import errors)
            if "ERROR collecting" in combined_output:
                for i, line in enumerate(lines):
                    if "ERROR collecting" in line:
                        # Get the full error traceback
                        error_start = i
                        error_end = i
                        # Find the end of the error (next === line or end of output)
                        for j in range(i + 1, len(lines)):
                            if lines[j].startswith("===") or lines[j].startswith("___"):
                                error_end = j
                                break
                        else:
                            error_end = len(lines)

                        error_context = "\n".join(lines[error_start:error_end])

                        # Extract the actual error type and message
                        error_type = "CollectionError"
                        error_msg = line.strip()
                        for err_line in lines[error_start:error_end]:
                            if (
                                "ModuleNotFoundError" in err_line
                                or "ImportError" in err_line
                            ):
                                error_type = (
                                    "ModuleNotFoundError"
                                    if "ModuleNotFoundError" in err_line
                                    else "ImportError"
                                )
                                error_msg = err_line.strip()
                                break

                        error_info["errors"].append(
                            {
                                "type": error_type,
                                "message": error_msg,
                                "context": error_context,
                            }
                        )

            # Extract Python syntax errors
            if (
                "SyntaxError" in combined_output
                or "IndentationError" in combined_output
            ):
                for i, line in enumerate(lines):
                    if "SyntaxError" in line or "IndentationError" in line:
                        error_info["errors"].append(
                            {
                                "type": "SyntaxError"
                                if "SyntaxError" in line
                                else "IndentationError",
                                "message": line.strip(),
                                "context": "\n".join(
                                    lines[max(0, i - 3) : min(len(lines), i + 3)]
                                ),
                            }
                        )

            # Extract test failures
            if "FAILED" in combined_output:
                for i, line in enumerate(lines):
                    if "FAILED" in line or "ERROR" in line:
                        error_info["failures"].append(
                            {
                                "test_name": line.strip(),
                                "context": "\n".join(
                                    lines[max(0, i - 5) : min(len(lines), i + 5)]
                                ),
                            }
                        )

            # Extract standalone import errors (not collection errors)
            if (
                "ImportError" in combined_output
                or "ModuleNotFoundError" in combined_output
            ) and "ERROR collecting" not in combined_output:
                for i, line in enumerate(lines):
                    if "ImportError" in line or "ModuleNotFoundError" in line:
                        error_info["errors"].append(
                            {
                                "type": "ImportError"
                                if "ImportError" in line
                                else "ModuleNotFoundError",
                                "message": line.strip(),
                                "context": "\n".join(
                                    lines[max(0, i - 2) : min(len(lines), i + 2)]
                                ),
                            }
                        )

        return error_info

    def build_fix_prompt(
        self,
        original_test_code: str,
        error_info: Dict[str, Any],
        attempt_number: int,
        source_code: Optional[str] = None,
    ) -> str:
        """
        Build LLM prompt for fixing test errors.

        Args:
            original_test_code: The test code that failed
            error_info: Structured error information
            attempt_number: Which fix attempt this is (1-3)
            source_code: Optional source code being tested

        Returns:
            Prompt string for LLM
        """
        prompt = f"""You are a test fixing expert. A generated test has errors and needs to be fixed.

**Attempt**: {attempt_number} of {self.max_retries}

**Test Code with Errors**:
```{error_info["language"]}
{original_test_code}
```

**Errors Found**:
"""

        if error_info.get("errors"):
            prompt += "\n**Syntax/Import Errors**:\n"
            for error in error_info["errors"]:
                prompt += f"- {error['type']}: {error['message']}\n"
                prompt += f"  Context: {error['context']}\n\n"

        if error_info.get("failures"):
            prompt += "\n**Test Failures**:\n"
            for failure in error_info["failures"]:
                prompt += f"- {failure['test_name']}\n"
                prompt += f"  Context: {failure['context']}\n\n"

        if source_code:
            prompt += f"\n**Source Code Being Tested**:\n```{error_info['language']}\n{source_code}\n```\n\n"

        prompt += """
**Instructions**:
1. Analyze the errors carefully - especially collection/import errors
2. Fix ALL issues in the test code
3. For ModuleNotFoundError/ImportError:
   - The project root is automatically added to PYTHONPATH, so absolute imports should work
   - Use the correct absolute import path from project root (e.g., `from routes.reactions import ...`)
   - DO NOT use sys.path.insert() or sys.path manipulation - it's not needed
   - Check if the module name in the import matches the actual file/package structure
4. Ensure proper indentation (NO leading spaces for module-level code)
5. Remove any placeholder imports or TODO comments  
6. Make sure fixtures are properly defined
7. Return ONLY the fixed test code, no explanations

**Common Issues to Fix**:
- ModuleNotFoundError: Check the import path matches the actual file structure. Example: if testing `routes/reactions.py`, use `from routes.reactions import ...`
- IndentationError: Check that @pytest.fixture, imports, and def statements have NO leading spaces at module level
- ImportError: Ensure all imports are from actual modules, not placeholders like 'your_module' or 'module_name'
- Missing fixtures: Define all fixtures that tests depend on
- Syntax errors: Fix any Python syntax issues

**Import Path Rules**:
- If testing file `routes/reactions.py`, import as: `from routes.reactions import function_name`
- If testing file `app/services/auth.py`, import as: `from app.services.auth import function_name`
- Never use placeholder names like 'your_module', 'module', or 'package_name'
- The project root is in PYTHONPATH automatically, so use absolute imports from root

**Fixed Test Code** (return only valid code, no markdown):
"""

        return prompt

    def get_fixed_test_from_llm(
        self, prompt: str, language: str = "python"
    ) -> Optional[str]:
        """
        Get fixed test code from LLM.

        Args:
            prompt: The prompt to send to LLM
            language: Programming language

        Returns:
            Fixed test code or None if LLM unavailable
        """
        if not self.llm_client:
            logger.warning("No LLM client available for auto-fixing")
            return None

        try:
            # Call LLM with the fix prompt
            response = self.llm_client.invoke(prompt)

            # Extract code from response
            if hasattr(response, "content"):
                fixed_code = response.content
            else:
                fixed_code = str(response)

            # Clean up response (remove markdown if present)
            if f"```{language}" in fixed_code:
                start = fixed_code.find(f"```{language}") + len(f"```{language}")
                end = fixed_code.find("```", start)
                if end != -1:
                    fixed_code = fixed_code[start:end].strip()
            elif "```" in fixed_code:
                start = fixed_code.find("```") + 3
                end = fixed_code.find("```", start)
                if end != -1:
                    fixed_code = fixed_code[start:end].strip()

            return fixed_code.strip()

        except Exception as e:
            logger.error(f"Error getting fixed code from LLM: {e}")
            return None

    def remove_problematic_tests(
        self, test_code: str, error_info: Dict[str, Any], language: str = "python"
    ) -> Optional[str]:
        """
        Ask LLM to remove problematic test functions that can't be fixed.

        Args:
            test_code: The test code with errors
            error_info: Error information
            language: Programming language

        Returns:
            Modified test code with problematic tests removed, or None
        """
        if not self.llm_client:
            return None

        prompt = f"""You are a test cleanup expert. The following test file has persistent errors that couldn't be fixed after 3 attempts.

**Test Code**:
```{language}
{test_code}
```

**Errors**:
{json.dumps(error_info.get('errors', []), indent=2)}

**Instructions**:
1. Identify which specific test functions are causing the errors
2. Remove ONLY those problematic test functions
3. Keep all working test functions and fixtures
4. If an import is only used by removed tests, remove that import too
5. Return the cleaned test code with only working tests

**IMPORTANT**:
- Remove entire test functions that have errors (including decorators and docstrings)
- Keep all fixtures that working tests might need
- Maintain proper code structure and formatting
- If ALL tests have errors, return a minimal valid test file with just imports and fixtures

Return ONLY the cleaned test code, no explanations:
"""

        try:
            response = self.llm_client.invoke(prompt)
            if hasattr(response, "content"):
                cleaned_code = response.content
            else:
                cleaned_code = str(response)

            # Extract code from markdown if present
            if f"```{language}" in cleaned_code:
                start = cleaned_code.find(f"```{language}") + len(f"```{language}")
                end = cleaned_code.find("```", start)
                if end != -1:
                    cleaned_code = cleaned_code[start:end].strip()
            elif "```" in cleaned_code:
                start = cleaned_code.find("```") + 3
                end = cleaned_code.find("```", start)
                if end != -1:
                    cleaned_code = cleaned_code[start:end].strip()

            return cleaned_code.strip()

        except Exception as e:
            logger.error(f"Error removing problematic tests: {e}")
            return None

    def auto_fix_test(
        self,
        test_code: str,
        test_file_path: str,
        language: str = "python",
        source_code: Optional[str] = None,
    ) -> Tuple[bool, str, List[str]]:
        """
        Automatically fix test errors with LLM feedback loop.

        Args:
            test_code: Original test code
            test_file_path: Path where test file will be written
            language: Programming language
            source_code: Optional source code being tested

        Returns:
            Tuple of (success, final_test_code, fix_history)
        """
        # Check if LLM is available
        if not self.llm_client:
            logger.warning("⚠️ LLM client not initialized - skipping auto-fix")
            logger.warning("Make sure OPENAI_API_KEY is set in environment")
            return False, test_code, ["LLM not initialized - skipping auto-fix"]

        fix_history = []
        current_code = test_code

        logger.info(
            f"Starting auto-fix for {test_file_path} (max {self.max_retries} attempts)"
        )

        for attempt in range(1, self.max_retries + 1):
            # Write current code to file
            Path(test_file_path).write_text(current_code, encoding="utf-8")

            # Run tests
            success, stdout, stderr = self.run_tests_and_capture_errors(
                test_file_path, language
            )

            if success:
                logger.info(f"✅ Tests passed on attempt {attempt}!")
                fix_history.append(f"Attempt {attempt}: SUCCESS")
                return True, current_code, fix_history

            # Extract error details
            error_info = self.extract_error_details(stdout, stderr, language)

            fix_history.append(
                f"Attempt {attempt}: FAILED - "
                f"{len(error_info['errors'])} errors, {len(error_info['failures'])} failures"
            )

            logger.warning(
                f"❌ Attempt {attempt} failed with {len(error_info['errors'])} errors, "
                f"{len(error_info['failures'])} failures"
            )

            # Log extracted errors for debugging
            if error_info["errors"]:
                logger.info(f"📋 Extracted errors:")
                for err in error_info["errors"]:
                    logger.info(f"  - {err['type']}: {err['message'][:100]}")
            else:
                logger.warning(f"⚠️ No errors extracted from output!")
                logger.warning(f"📄 Raw output (first 500 chars):")
                logger.warning(f"{error_info['raw_output'][:500]}")

            # If this is the last attempt, don't try to fix
            if attempt >= self.max_retries:
                logger.error(f"Max retries ({self.max_retries}) reached. Giving up.")
                break

            # Build fix prompt
            prompt = self.build_fix_prompt(
                current_code, error_info, attempt, source_code
            )

            # Get fixed code from LLM
            fixed_code = self.get_fixed_test_from_llm(prompt, language)

            if not fixed_code:
                logger.error("Could not get fixed code from LLM")
                break

            logger.info(f"🔧 Got fixed code from LLM, trying again...")
            current_code = fixed_code

        # If we get here, all attempts failed - try last resort: remove problematic functions
        logger.warning("⚠️ All fix attempts failed. Trying last resort: removing problematic test functions")

        try:
            fallback_code = self.remove_problematic_tests(current_code, error_info, language)
            if fallback_code and fallback_code != current_code:
                # Write and test the fallback code
                Path(test_file_path).write_text(fallback_code, encoding="utf-8")
                success, stdout, stderr = self.run_tests_and_capture_errors(
                    test_file_path, language
                )

                if success:
                    logger.info("✅ Fallback successful - removed problematic tests")
                    fix_history.append("Fallback: Removed problematic tests - SUCCESS")
                    return True, fallback_code, fix_history
                else:
                    logger.warning("⚠️ Fallback did not fix all issues")
                    fix_history.append("Fallback: Removed problematic tests - still have errors")
        except Exception as e:
            logger.error(f"Error in fallback: {e}")
            fix_history.append(f"Fallback failed: {e}")

        return False, current_code, fix_history


def auto_fix_test_file(
    test_file_path: str,
    language: str = "python",
    source_file_path: Optional[str] = None,
    llm_client=None,
    max_retries: int = 3,
) -> bool:
    """
    Convenience function to auto-fix a test file.

    Args:
        test_file_path: Path to the test file
        language: Programming language
        source_file_path: Optional path to source code being tested
        llm_client: Optional LLM client
        max_retries: Maximum fix attempts

    Returns:
        True if tests pass after fixing, False otherwise
    """
    # Read current test code
    test_code = Path(test_file_path).read_text()

    # Read source code if provided
    source_code = None
    if source_file_path and Path(source_file_path).exists():
        source_code = Path(source_file_path).read_text()

    # Create auto-fixer
    fixer = TestAutoFixer(llm_client=llm_client, max_retries=max_retries)

    # Run auto-fix
    success, final_code, history = fixer.auto_fix_test(
        test_code=test_code,
        test_file_path=test_file_path,
        language=language,
        source_code=source_code,
    )

    # Log history
    logger.info(f"Auto-fix history for {test_file_path}:")
    for entry in history:
        logger.info(f"  {entry}")

    if success:
        logger.info(f"✅ Successfully fixed {test_file_path}")
        # Write final code back
        Path(test_file_path).write_text(final_code)
    else:
        logger.error(f"❌ Could not fix {test_file_path} after {max_retries} attempts")

    return success
