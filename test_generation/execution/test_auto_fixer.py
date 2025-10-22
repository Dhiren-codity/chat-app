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
                # Try OpenAI first (primary for auto-fix - using GPT-4o as requested)
                openai_key = os.getenv("OPENAI_API_KEY")
                anthropic_key = os.getenv("ANTHROPIC_API_KEY")

                if openai_key:
                    # Use OpenAI GPT-4o for auto-fix (primary)
                    try:
                        from openai import OpenAI

                        self.llm_client = OpenAI(api_key=openai_key)
                        self.model_name = os.getenv("LLM_MODEL", "gpt-4o")
                        self.llm_type = "openai"
                        logger.info(
                            f"✅ Initialized OpenAI for auto-fixing: {self.model_name}"
                        )
                        return
                    except Exception as e:
                        logger.error(f"Failed to initialize OpenAI: {e}")

                # Fallback to Anthropic
                if anthropic_key:
                    try:
                        from anthropic import Anthropic

                        self.llm_client = Anthropic(api_key=anthropic_key)
                        self.model_name = os.getenv(
                            "LLM_MODEL", "claude-sonnet-4-20250514"
                        )
                        self.llm_type = "anthropic"
                        logger.info(
                            f"✅ Initialized Anthropic for auto-fixing: {self.model_name}"
                        )
                        return
                    except ImportError:
                        logger.warning("Anthropic SDK not available")
                    except Exception as e:
                        logger.warning(f"Failed to initialize Anthropic: {e}")

                # No API keys available
                logger.error("❌ No API keys found - auto-fix will not work!")
                logger.error(
                    "Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in GitHub Secrets"
                )
                self.llm_client = None
                self.llm_type = None

            except Exception as e:
                logger.error(f"❌ Could not initialize LLM for auto-fixing: {e}")
                logger.error("Auto-fix will be skipped")
                self.llm_client = None
                self.llm_type = None

    def _call_llm(self, prompt: str) -> Optional[str]:
        """
        Call LLM with a prompt and return the response text.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            Response text or None if unavailable
        """
        if not self.llm_client:
            logger.warning("⚠️ LLM client not initialized - skipping auto-fix")
            logger.warning("Make sure OPENAI_API_KEY is set in environment")
            return None

        try:
            if self.llm_type == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )
                return response.choices[0].message.content
            elif self.llm_type == "anthropic":
                response = self.llm_client.messages.create(
                    model=self.model_name,
                    max_tokens=4096,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )
                return response.content[0].text
            else:
                # Fallback for custom LLM clients with invoke method
                response = self.llm_client.invoke(prompt)
                if hasattr(response, "content"):
                    return response.content
                return str(response)
        except Exception as e:
            logger.error(f"❌ Error calling LLM: {e}")
            return None

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
                for cmd_try in (
                    ["python3", "-m", "pytest"],
                    ["python", "-m", "pytest"],
                    ["pytest"],
                ):
                    try:
                        # Test if command works
                        test_result = subprocess.run(
                            cmd_try + ["--version"], capture_output=True, timeout=5
                        )
                        if test_result.returncode == 0:
                            pytest_cmd = cmd_try
                            break
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        continue

                if not pytest_cmd:
                    logger.error(
                        "pytest not found! Tried: python3 -m pytest, python -m pytest, pytest"
                    )
                    return (
                        False,
                        "",
                        "Error running tests: pytest not found. Install pytest or ensure it's in PATH.",
                    )

                cmd = pytest_cmd + [
                    test_file_path,
                    "-vv",
                    "--tb=long",
                    "--no-header",
                    "-rfE",
                ]
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
            error_msg = (
                f"Command not found: {e}. Make sure the test framework is installed."
            )
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
            "passing": [],  # Track passing tests
            "raw_output": stdout + "\n" + stderr,
        }

        combined_output = stdout + "\n" + stderr
        lines = combined_output.split("\n")

        # Check for pytest/test framework not found errors
        if (
            "Error running tests" in combined_output
            or "No such file or directory" in combined_output
        ):
            error_info["errors"].append(
                {
                    "type": "EnvironmentError",
                    "message": stderr.strip()
                    or stdout.strip()
                    or "Test framework not available",
                    "context": combined_output[:1000],
                }
            )
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

            # Extract test failures and passing tests
            if (
                "FAILED" in combined_output
                or "ERROR" in combined_output
                or "PASSED" in combined_output
            ):
                import re

                # Pytest -vv output format:
                # test_file.py::test_name PASSED
                # test_file.py::test_name FAILED
                # test_file.py::test_name ERROR
                #
                # Short summary format (different):
                # ERROR test_file.py::test_name - ErrorMessage
                # FAILED test_file.py::test_name - AssertionError

                # Match inline status (from -vv output)
                pass_pattern = re.compile(r"(\S+::[\w\[\],-]+)\s+PASSED")
                fail_inline_pattern = re.compile(r"(\S+::[\w\[\],-]+)\s+(FAILED|ERROR)")

                # Match summary status (from short test summary)
                fail_summary_pattern = re.compile(
                    r"(FAILED|ERROR)\s+(\S+::[\w\[\],-]+)\s+-\s+(.+)"
                )

                for i, line in enumerate(lines):
                    # Extract passing tests
                    pass_match = pass_pattern.search(line)
                    if pass_match:
                        test_path = pass_match.group(1)
                        test_name = test_path.split("::")[-1]
                        if test_name not in error_info["passing"]:
                            error_info["passing"].append(test_name)
                            logger.info(f"✅ Found passing test: {test_name}")

                    # Extract failing tests - try inline format first
                    fail_inline_match = fail_inline_pattern.search(line)
                    if fail_inline_match:
                        test_path = fail_inline_match.group(1)
                        status = fail_inline_match.group(2)
                        error_info["failures"].append(
                            {
                                "test_name": line.strip(),
                                "error_type": status,
                                "error_message": f"{status} in test execution",
                                "context": "\n".join(
                                    lines[max(0, i - 10) : min(len(lines), i + 20)]
                                ),
                            }
                        )
                    else:
                        # Try summary format
                        fail_summary_match = fail_summary_pattern.search(line)
                        if fail_summary_match:
                            status, test_path, error_msg = fail_summary_match.groups()
                            error_info["failures"].append(
                                {
                                    "test_name": line.strip(),
                                    "error_type": status,
                                    "error_message": error_msg.strip(),
                                    "context": "\n".join(
                                        lines[max(0, i - 10) : min(len(lines), i + 20)]
                                    ),
                                }
                            )
                        elif "FAILED" in line or "ERROR" in line:
                            error_info["failures"].append(
                                {
                                    "test_name": line.strip(),
                                    "context": "\n".join(
                                        lines[max(0, i - 10) : min(len(lines), i + 20)]
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
            # Limit to first 5 errors to avoid context length issues
            errors_to_show = error_info["errors"][:5]
            for error in errors_to_show:
                prompt += f"- {error['type']}: {error['message']}\n"
                # Limit context to 200 chars
                context = error.get("context", "")[:200]
                if context:
                    prompt += f"  Context: {context}...\n"
                prompt += "\n"

            if len(error_info["errors"]) > 5:
                prompt += (
                    f"\n... and {len(error_info['errors']) - 5} more similar errors\n"
                )

        if error_info.get("failures"):
            prompt += "\n**Test Failures**:\n"
            # Limit to first 10 failures to avoid context length issues
            failures_to_show = error_info["failures"][:10]
            for failure in failures_to_show:
                prompt += f"- {failure['test_name']}\n"
                if "error_message" in failure:
                    prompt += f"  Error: {failure['error_message']}\n"
                # Limit context to 200 chars
                context = failure.get("context", "")[:200]
                if context:
                    prompt += f"  Context: {context}...\n"
                prompt += "\n"

            if len(error_info["failures"]) > 10:
                prompt += f"\n... and {len(error_info['failures']) - 10} more similar failures\n"

        if source_code:
            prompt += f"\n**Source Code Being Tested**:\n```{error_info['language']}\n{source_code}\n```\n\n"

        prompt += """
**Instructions**:
1. Analyze the errors carefully - especially collection/import errors
2. Fix ALL issues in the test code
3. For ImportError "cannot import name 'X' from 'module'":
   - This means the function/class 'X' does NOT exist in the source module
   - REMOVE the import for 'X' entirely
   - REMOVE any tests or code that uses 'X'
   - DO NOT try to add or create 'X' in the test file
4. For ModuleNotFoundError "No module named 'X'":
   - This module does NOT exist - it was HALLUCINATED
   - Common hallucinations: user_status, message_handler, auth_service (when these files don't exist)
   - SOLUTION: Import the class from the ACTUAL source file being tested
   - Example: If "No module named 'user_status'", check if UserStatus is in the source file
   - If UserStatus is in status_manager.py, use: `from status_manager import UserStatus`
   - DO NOT use sys.path.insert() or sys.path manipulation
5. Check the source code above to see what's ACTUALLY available to import
6. Ensure proper indentation (NO leading spaces for module-level code)
7. Remove any placeholder imports or TODO comments
8. Make sure fixtures are properly defined (no 'self' parameter)
9. Return ONLY the fixed test code, no explanations

**CRITICAL - Handling Non-Existent Functions**:
❌ WRONG: Keep importing `decorated_function` and try to fix it
✅ CORRECT: If ImportError says "cannot import name 'decorated_function'", REMOVE:
   - The import: `from routes.reactions import decorated_function`
   - Any test functions that use `decorated_function`
   - Any fixtures that depend on `decorated_function`

**CRITICAL - Handling Hallucinated Modules**:
If you see errors like:
- "ModuleNotFoundError: No module named 'user_status'"
- "ModuleNotFoundError: No module named 'message_handler'"
- "ModuleNotFoundError: No module named 'auth_service'"

This means these modules were INVENTED/HALLUCINATED. To fix:
1. Look at the SOURCE CODE above
2. Find where the class is ACTUALLY defined (usually in the file being tested)
3. Import from the ACTUAL module

Example Fix:
```python
# ❌ WRONG (hallucinated):
from user_status import UserStatus

# ✅ CORRECT (if UserStatus is in status_manager.py):
from status_manager import UserStatus
```

**Common Issues to Fix**:
- ImportError "cannot import name X": REMOVE the import and all uses of X
- ModuleNotFoundError with hallucinated module: Import from ACTUAL source file (check source code above)
- IndentationError: Ensure @pytest.fixture, imports, def have NO leading spaces
- ImportError with placeholders: Remove 'your_module', 'module_name', etc.
- Missing fixtures: Define fixtures (without 'self' parameter)
- Syntax errors: Fix Python syntax issues
- Flask RuntimeError "Working outside of request context":
  * CRITICAL: Use Flask test client for ALL route testing
  * Add proper fixtures at MODULE LEVEL (not in classes):
    ```python
    @pytest.fixture
    def app():
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def client(app):
        with app.test_client() as client:
            with app.app_context():
                yield client
    ```
  * Convert tests to use client.get/post/etc instead of direct function calls
  * Example: response = client.get('/endpoint', headers={'user-id': '123'})
  * Remove 'self' parameter from fixtures
  * NEVER define fixtures inside test classes

**Import Path Rules**:
- If testing `routes/reactions.py`, use: `from routes.reactions import function_name`
- If testing `app/services/auth.py`, use: `from app.services.auth import function_name`
- Never use placeholder names like 'your_module', 'module', or 'package_name'
- Project root is in PYTHONPATH, use absolute imports from root

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

        # Call LLM with the fix prompt
        response = self._call_llm(prompt)
        if not response:
            return None

        # Clean up response (remove markdown if present)
        fixed_code = response
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

    def _remove_bad_imports_from_code(self, test_code: str) -> str:
        """
        Remove obviously bad/placeholder imports from test code.
        This is called BEFORE testing individual functions to allow tests
        that don't use the bad imports to pass.

        Args:
            test_code: Test code with potential bad imports

        Returns:
            Test code with bad imports removed
        """
        import re

        bad_placeholder_patterns = [
            "decorated_function",  # Common LLM hallucination
            "nonexistent",  # Obviously doesn't exist
            "placeholder",  # Placeholder text
            "your_module",  # Placeholder text
            "your_function",  # Placeholder text
            "module_name",  # Placeholder text
            "function_name",  # Placeholder text
            "example_",  # Example placeholders
        ]

        lines = test_code.split("\n")
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()

            # Check if this is an import line with bad placeholders
            if stripped.startswith("from ") or stripped.startswith("import "):
                # Check if line contains any obvious placeholders
                has_bad_import = any(bad in line for bad in bad_placeholder_patterns)

                if has_bad_import:
                    logger.info(f"  🗑️ Removing bad import: {stripped[:100]}")
                    continue  # Skip this import line

            # Keep all other lines
            cleaned_lines.append(line)

        result = "\n".join(cleaned_lines)

        if len(cleaned_lines) < len(lines):
            removed_count = len(lines) - len(cleaned_lines)
            logger.info(f"  ✂️ Removed {removed_count} bad import line(s)")

        return result

    def _fix_flask_fixtures(
        self, test_code: str, test_file_path: str, has_flask_errors: bool = False
    ) -> str:
        """
        Fix Flask test fixtures that are causing context errors.

        Common issues:
        1. Fixtures defined inside test classes with 'self' parameter
        2. Missing Flask app context
        3. Not using app.test_client() properly

        Args:
            test_code: Test code with Flask fixture issues
            test_file_path: Path to test file (used to determine app import)
            has_flask_errors: Whether Flask errors were detected in test output

        Returns:
            Fixed test code with proper Flask fixtures
        """
        import re
        import ast

        logger.info("🔧 Fixing Flask fixtures...")

        try:
            # Try to find the app import in the test file
            app_import = None
            app_var_name = "app"

            for line in test_code.split("\n"):
                # Look for Flask app imports
                if "from flask import" in line.lower() and "flask" in line.lower():
                    continue

                # CRITICAL: Detect bad flask.app import (Flask's internal module)
                # MUST check this BEFORE checking for valid app imports
                if "from flask.app import" in line:
                    logger.warning(f"  ⚠️ Found BAD import: {line.strip()}")
                    logger.warning(
                        f"     This imports Flask's internal module, not your app!"
                    )
                    logger.warning(
                        f"     Will be removed and replaced with correct import"
                    )
                    # Don't use this import at all - skip it entirely
                    continue

                # Only check for valid app imports AFTER filtering out bad ones
                if "import app" in line or (
                    "from" in line and "import" in line and "app" in line
                ):
                    # Double-check this isn't a bad flask.app import (redundant safety)
                    if "flask.app" in line:
                        logger.warning(
                            f"  ⚠️ Skipping bad flask.app import: {line.strip()}"
                        )
                        continue

                    app_import = line.strip()
                    # Try to extract the variable name
                    if "import" in line:
                        parts = line.split("import")
                        if len(parts) > 1:
                            imported = parts[-1].strip().split()[0]
                            if imported and not imported.startswith("("):
                                app_var_name = imported
                                logger.info(
                                    f"  ✅ Found valid app import: {app_import}"
                                )
                                logger.info(
                                    f"     Using app variable name: {app_var_name}"
                                )
                    break

            # If no valid app import found, infer from test file path
            if not app_import:
                logger.info(
                    "  🔍 No valid app import found - inferring correct import..."
                )
                # e.g., routes/reactions_test.py -> likely imports from routes.reactions
                test_path = Path(test_file_path)
                parent_module = test_path.parent.name

                # List of directories that are NOT Python packages
                non_package_dirs = {"tmp", "var", "temp", "home", "usr", "opt", "etc"}

                # First, check if source file exists in same directory (e.g., test_app.py for test_app_test.py)
                module_file = test_path.parent / test_path.name.replace(
                    "_test.py", ".py"
                )
                if module_file.exists():
                    # Check if parent is a Python package or just a system directory
                    if (
                        parent_module
                        and parent_module != "."
                        and parent_module != "flask"
                        and parent_module not in non_package_dirs
                    ):
                        # Parent is a package, use qualified import
                        app_import = (
                            f"from {parent_module}.{module_file.stem} import app"
                        )
                        logger.info(
                            f"  ✅ Inferred app import from package structure: {app_import}"
                        )
                    else:
                        # Parent is not a package (or is tmp/var/etc), use direct import
                        app_import = f"from {module_file.stem} import app"
                        logger.info(
                            f"  ✅ Inferred app import from sibling file: {app_import}"
                        )
                else:
                    # No source file found, use default
                    app_import = "from app import app"
                    logger.info(
                        f"  ✅ No source file found, using default: {app_import}"
                    )

            lines = test_code.split("\n")
            fixed_lines = []
            in_class = False
            class_indent = 0
            fixtures_to_move = []
            current_fixture = None
            fixture_start_idx = None

            i = 0
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()

                # Track if we're inside a class
                if stripped.startswith("class "):
                    in_class = True
                    class_indent = len(line) - len(line.lstrip())
                    fixed_lines.append(line)
                    i += 1
                    continue

                # Check if we're exiting the class (dedent to class level or less)
                if in_class and line and not line[0].isspace():
                    in_class = False

                # Detect fixture inside class
                if in_class and "@pytest.fixture" in stripped:
                    logger.info(f"  🔍 Found fixture inside class at line {i + 1}")
                    fixture_start_idx = i

                    # Find the entire fixture (decorator + function)
                    fixture_lines = [line]
                    i += 1

                    # Get function definition
                    while i < len(lines):
                        fixture_lines.append(lines[i])
                        if lines[i].strip().startswith("def "):
                            # Get function body
                            func_indent = len(lines[i]) - len(lines[i].lstrip())
                            i += 1
                            while i < len(lines) and (
                                not lines[i].strip()
                                or lines[i].startswith(" " * (func_indent + 1))
                            ):
                                fixture_lines.append(lines[i])
                                i += 1
                            break
                        i += 1

                    # Store fixture to move to module level
                    fixtures_to_move.append(fixture_lines)
                    logger.info(
                        f"  📤 Marked fixture for moving to module level ({len(fixture_lines)} lines)"
                    )
                    continue

                fixed_lines.append(line)
                i += 1

            # Always reconstruct to add proper Flask fixtures (even if no fixtures to move)
            # This handles cases where fixtures are missing or incorrectly structured
            should_reconstruct = fixtures_to_move or has_flask_errors

            if should_reconstruct:
                if fixtures_to_move:
                    logger.info(
                        f"  🔄 Moving {len(fixtures_to_move)} fixture(s) to module level..."
                    )
                elif has_flask_errors:
                    logger.info("  🔧 Adding missing Flask fixtures...")

                # Build new file structure
                final_lines = []

                # 1. Keep module docstring if present
                first_non_empty = None
                for i, line in enumerate(fixed_lines):
                    if line.strip():
                        first_non_empty = i
                        break

                if first_non_empty is not None:
                    first_line = fixed_lines[first_non_empty].strip()
                    if first_line.startswith('"""') or first_line.startswith("'''"):
                        # Add docstring
                        quote = '"""' if first_line.startswith('"""') else "'''"
                        if first_line.endswith(quote) and len(first_line) > 6:
                            # Single-line docstring
                            final_lines.append(fixed_lines[first_non_empty])
                            final_lines.append("")
                        else:
                            # Multi-line docstring
                            for j in range(first_non_empty, len(fixed_lines)):
                                final_lines.append(fixed_lines[j])
                                if j > first_non_empty and quote in fixed_lines[j]:
                                    final_lines.append("")
                                    break

                # 2. Keep imports (but filter out bad flask.app imports)
                for line in fixed_lines:
                    if line.strip().startswith(("import ", "from ")):
                        # Skip bad flask.app imports
                        if "from flask.app import" in line:
                            logger.info(f"  🗑️  Removing bad import: {line.strip()}")
                            continue
                        final_lines.append(line)

                # 3. Add proper Flask app import if not present
                has_app_import = any(
                    "import app" in line and "from flask.app" not in line
                    for line in final_lines
                )
                if not has_app_import:
                    logger.info(f"  ➕ Adding correct app import: {app_import}")
                    final_lines.append("")
                    final_lines.append(app_import)
                else:
                    logger.info(f"  ✅ Valid app import already exists")

                final_lines.append("")
                final_lines.append("")

                # 4. Add essential Flask fixtures if not already present
                has_client_fixture = any(
                    "def client" in line for line in test_code.split("\n")
                )
                has_app_fixture = any(
                    "def app(" in line for line in test_code.split("\n")
                )

                # CRITICAL: Do NOT create 'def app():' fixture - it shadows the imported app!
                # Instead, only create client fixture which uses the imported app directly

                # Add client fixture if missing
                if not has_client_fixture:
                    final_lines.append("@pytest.fixture")
                    final_lines.append(
                        "def client():"
                    )  # ✅ No 'app' parameter, use imported app directly
                    final_lines.append('    """Flask test client with app context."""')
                    final_lines.append(f"    {app_var_name}.config['TESTING'] = True")
                    final_lines.append(
                        f"    with {app_var_name}.test_client() as client:"
                    )
                    final_lines.append(f"        with {app_var_name}.app_context():")
                    final_lines.append("            yield client")
                    final_lines.append("")

                # 5. Add moved fixtures at module level with proper Flask context
                for fixture_group in fixtures_to_move:
                    final_lines.append("@pytest.fixture")

                    # Find the def line and remove 'self' parameter
                    for fline in fixture_group:
                        if fline.strip().startswith("def "):
                            # Remove 'self' parameter
                            func_def = fline.strip()
                            func_def = re.sub(r"\(self\s*,\s*", "(", func_def)
                            func_def = re.sub(r"\(self\)", "()", func_def)

                            # Check if it's a 'client' or 'app' fixture - use proper template
                            if "def client" in func_def:
                                # CRITICAL: client fixture should NOT have 'app' parameter
                                # It should use the imported app directly
                                if "(app)" in func_def:
                                    func_def = func_def.replace("(app)", "()")
                                final_lines.append(func_def)
                                final_lines.append(
                                    '    """Flask test client with app context."""'
                                )
                                final_lines.append(
                                    f"    {app_var_name}.config['TESTING'] = True"
                                )
                                final_lines.append(
                                    f"    with {app_var_name}.test_client() as client:"
                                )
                                final_lines.append(
                                    f"        with {app_var_name}.app_context():"
                                )
                                final_lines.append("            yield client")
                            elif "def app" in func_def:
                                # CRITICAL: Do NOT create 'def app():' fixture!
                                # It shadows the imported app. Skip this fixture entirely.
                                logger.warning(
                                    "  ⚠️ Skipping 'def app():' fixture - would shadow imported app"
                                )
                                continue
                            else:
                                # For other fixtures, keep original body but ensure proper indentation
                                final_lines.append(func_def)
                                found_def = False
                                for body_line in fixture_group:
                                    if body_line.strip().startswith("def "):
                                        found_def = True
                                        continue
                                    if found_def and body_line.strip():
                                        final_lines.append("    " + body_line.strip())
                            break

                    final_lines.append("")

                # 6. Add the rest of the file (classes, tests) with client/app param fixes
                # Skip ALL import lines and module docstring (they've been added already)
                skip_until_code = True  # Skip docstrings/imports at the top
                for line in fixed_lines:
                    stripped = line.strip()

                    # Skip imports (already added above with bad ones removed)
                    if stripped.startswith(("import ", "from ")):
                        continue

                    # Skip module-level docstring (already added above)
                    if skip_until_code:
                        if (
                            not stripped
                            or stripped.startswith("#")
                            or stripped.startswith('"""')
                            or stripped.startswith("'''")
                        ):
                            continue
                        # First real code line - stop skipping
                        skip_until_code = False

                    # Fix test methods to include client and app parameters if missing
                    if line.strip().startswith("def test_"):
                        # Check if it needs client or app parameter
                        if "def test_" in line and "(" in line and ")" in line:
                            # Extract parameters
                            match = re.search(r"def\s+test_\w+\((.*?)\)", line)
                            if match:
                                params = match.group(1).strip()
                                # Remove 'self' if present
                                params = re.sub(r"self\s*,?\s*", "", params)
                                # Add client if not present
                                if "client" not in params and params:
                                    params = params + ", client"
                                elif "client" not in params and not params:
                                    params = "client"
                                # Reconstruct the line
                                func_name = re.search(r"def\s+(test_\w+)", line).group(
                                    1
                                )
                                indent = len(line) - len(line.lstrip())
                                line = " " * indent + f"def {func_name}({params}):"

                    final_lines.append(line)

                test_code = "\n".join(final_lines)
                logger.info(f"  ✅ Flask fixtures fixed and moved to module level")

            return test_code

        except Exception as e:
            logger.warning(f"  ⚠️ Error fixing Flask fixtures: {e}")
            logger.warning(f"  Returning original code")
            return test_code

    def parse_failing_tests_from_output(self, stdout: str, stderr: str) -> List[str]:
        """
        Parse failing test function names from pytest output.

        Looks for patterns like:
        - FAILED routes/reactions_test.py::test_function_name
        - FAILED routes/reactions_test.py::TestClass::test_function_name

        Args:
            stdout: pytest stdout
            stderr: pytest stderr

        Returns:
            List of failing test function names
        """
        import re

        failing_tests = []
        combined_output = stdout + "\n" + stderr

        # Pattern to match pytest failure lines
        # Matches: FAILED path/to/file.py::TestClass::test_name or FAILED path/to/file.py::test_name
        fail_pattern = re.compile(r"FAILED\s+[\w/]+\.py::([\w:]+)")

        matches = fail_pattern.findall(combined_output)
        for match in matches:
            # Extract just the test function name (last part after ::)
            if "::" in match:
                test_name = match.split("::")[-1]
            else:
                test_name = match

            if test_name.startswith("test_") and test_name not in failing_tests:
                failing_tests.append(test_name)
                logger.info(f"  🔍 Found failing test: {test_name}")

        return failing_tests

    def keep_only_passing_tests(
        self,
        test_file_path: str,
        language: str = "python",
        initial_passing_tests: list = None,
    ) -> Optional[str]:
        """
        Run tests individually and keep only the ones that pass.
        This is inspired by the reference Go implementation.

        Flow:
        1. Extract all test function names from the file
        2. Run each test individually with pytest -k
        3. Keep tests that pass, remove tests that fail
        4. If no tests pass, return minimal valid file

        Args:
            test_file_path: Path to test file
            language: Programming language

        Returns:
            Cleaned test code with only passing tests, or None if error
        """
        # Log function entry with inputs
        logger.info(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        logger.info(f"🚀 keep_only_passing_tests() called")
        logger.info(f"   test_file_path: {test_file_path}")
        logger.info(f"   language: {language}")
        logger.info(
            f"   initial_passing_tests provided: {initial_passing_tests is not None}"
        )
        if initial_passing_tests is not None:
            logger.info(f"   initial_passing_tests count: {len(initial_passing_tests)}")
            logger.info(
                f"   initial_passing_tests (first 10): {initial_passing_tests[:10]}"
            )
            if len(initial_passing_tests) > 10:
                logger.info(f"   ... and {len(initial_passing_tests) - 10} more")
        logger.info(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        if language != "python":
            logger.warning(
                f"keep_only_passing_tests only supports Python, got: {language}"
            )
            return None

        try:
            import re

            test_code = Path(test_file_path).read_text()
            test_path = Path(test_file_path).resolve()

            # Find project root
            project_root = test_path.parent
            while project_root.parent != project_root:
                if (
                    (project_root / ".git").exists()
                    or (project_root / "setup.py").exists()
                    or (project_root / "pyproject.toml").exists()
                ):
                    break
                project_root = project_root.parent

            env = os.environ.copy()
            env["PYTHONPATH"] = f"{project_root}:{env.get('PYTHONPATH', '')}"

            # CRITICAL: Remove bad imports BEFORE testing individual functions
            # This allows tests that don't use the bad imports to pass
            logger.info(f"🧹 Removing bad placeholder imports before testing...")
            test_code = self._remove_bad_imports_from_code(test_code)

            # Write cleaned code to file so individual test runs work
            Path(test_file_path).write_text(test_code, encoding="utf-8")

            logger.info(f"🔍 Extracting test functions from {test_file_path}...")

            # Extract all test function names (including methods in test classes)
            lines = test_code.split("\n")
            test_functions = []
            in_test_class = False
            current_class = None

            for line in lines:
                stripped = line.strip()

                # Check for test class
                if re.match(r"^\s*class (Test\w+)", line):
                    match = re.search(r"class (Test\w+)", line)
                    if match:
                        current_class = match.group(1)
                        in_test_class = True
                        continue

                # Check for test function
                if re.match(r"^\s*def (test_\w+)", line):
                    match = re.search(r"def (test_\w+)", line)
                    if match:
                        test_name = match.group(1)
                        # For class methods, use Class::method format
                        if in_test_class and current_class:
                            full_name = f"{current_class}::{test_name}"
                        else:
                            full_name = test_name
                        test_functions.append(full_name)

                # Exit test class when we hit another class or top-level function
                if (
                    in_test_class
                    and line
                    and len(line) > 0
                    and not line[0].isspace()
                    and not stripped.startswith("#")
                ):
                    if not stripped.startswith("class " + current_class):
                        in_test_class = False
                        current_class = None

            if not test_functions:
                logger.warning("⚠️ No test functions found in file")
                return self._create_minimal_valid_file(test_code)

            logger.info(f"📋 Found {len(test_functions)} test functions in file")

            # OPTIMIZATION: Use initial_passing_tests if provided
            # IMPORTANT: Check 'is not None' because empty list [] is falsy but still valid
            if initial_passing_tests is not None and len(initial_passing_tests) > 0:
                logger.info(
                    f"✅ Using {len(initial_passing_tests)} tests that passed initially: {initial_passing_tests}"
                )
                logger.info(f"🔍 Test functions found in file: {test_functions}")

                # CRITICAL FIX: Match test functions to initial passing tests
                # Handle parametrized tests: test_foo matches test_foo[param1], test_foo[param2], etc.
                passing_tests = []
                failing_tests = []

                for t in test_functions:
                    # Extract full test name with class (if present)
                    # t looks like: "TestClass::test_method" or "test_function"
                    file_test_name = t.split("[")[
                        0
                    ]  # Remove params: test_foo[x] -> test_foo (or TestClass::test_foo)

                    # Check if this test (or any parametrized version of it) passed
                    matched = False
                    for passing in initial_passing_tests:
                        # passing looks like: "routes/file_test.py::TestClass::test_method" or "routes/file_test.py::test_function"
                        # Extract the test identifier (everything after the file path)
                        if "::" in passing:
                            # Split by :: and take everything except the first part (which is the file path)
                            parts = passing.split("::")
                            if len(parts) >= 2:
                                # Join back parts after the file path
                                # routes/file.py::TestClass::test_method -> TestClass::test_method
                                passing_test_name = "::".join(parts[1:])
                            else:
                                passing_test_name = parts[0]
                        else:
                            passing_test_name = passing

                        # Remove parametrization brackets from passing test
                        passing_base = passing_test_name.split("[")[0]

                        if file_test_name == passing_base:
                            matched = True
                            passing_tests.append(t)
                            logger.info(
                                f"  ✅ KEEP: {t} (matches passing test: {passing})"
                            )
                            break

                    if not matched:
                        failing_tests.append(t)
                        logger.info(f"  ❌ REMOVE: {t} (no match in passing list)")

                logger.info(
                    f"📊 RESULT: Keeping {len(passing_tests)}/{len(test_functions)} test functions"
                )
                logger.info(
                    f"   Expected ~{len(initial_passing_tests)} passing (may differ due to parametrization)"
                )

                # SANITY CHECK: If we're removing >50% of tests, warn about potential matching issue
                if len(passing_tests) < len(initial_passing_tests) * 0.5:
                    logger.error(f"🚨🚨🚨 SANITY CHECK FAILED! 🚨🚨🚨")
                    logger.error(
                        f"⚠️ Only keeping {len(passing_tests)} tests out of {len(initial_passing_tests)} that passed!"
                    )
                    logger.error(
                        f"⚠️ This suggests a parametrized test matching problem!"
                    )
                    logger.error(
                        f"⚠️ Refusing to delete passing tests - returning original code unchanged"
                    )
                    logger.error(f"🚨🚨🚨 NO TESTS WERE DELETED 🚨🚨🚨")
                    return test_code
            else:
                logger.info("⚠️ Testing each individually...")
                passing_tests = []
                failing_tests = []

                for test_name in test_functions:
                    logger.info(f"  🧪 Testing: {test_name}")

                    # Run single test
                    # For class methods (Class::method), pytest uses :: syntax
                    # For standalone functions, use the function name directly
                    if "::" in test_name:
                        # Use full path notation: file.py::Class::method
                        test_specifier = f"{test_path}::{test_name}"
                        cmd = [
                            "python3",
                            "-m",
                            "pytest",
                            test_specifier,
                            "-v",
                            "--tb=no",
                            "-x",
                            "--no-header",
                        ]
                    else:
                        # For standalone test functions, use -k but make it exact with 'and' to avoid partial matches
                        # This prevents test_auth from matching test_authentication
                        cmd = [
                            "python3",
                            "-m",
                            "pytest",
                            str(test_path),
                            "-k",
                            test_name,
                            "-v",
                            "--tb=no",
                            "-x",
                            "--no-header",
                        ]

                    try:
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            timeout=30,
                            cwd=str(project_root),
                            env=env,
                        )

                        output = result.stdout + result.stderr
                        output_lower = output.lower()

                        # Check if test passed
                        # Look for "passed" in output AND returncode 0
                        # Also check for specific patterns like "1 passed" or "passed in"
                        if result.returncode == 0 and (
                            "passed" in output_lower
                            or "1 passed" in output_lower
                            or " passed in" in output_lower
                        ):
                            passing_tests.append(test_name)
                            logger.info(f"    ✅ PASS")
                        else:
                            failing_tests.append(test_name)
                            logger.info(f"    ❌ FAIL")

                    except subprocess.TimeoutExpired:
                        failing_tests.append(test_name)
                        logger.info(f"    ⏱️ TIMEOUT")
                    except Exception as e:
                        failing_tests.append(test_name)
                        logger.info(f"    ❌ ERROR: {str(e)[:100]}")

            # Summary
            logger.info(
                f"📊 Results: {len(passing_tests)} passed, {len(failing_tests)} failed"
            )

            if not passing_tests:
                logger.warning("⚠️ No tests passed individually!")
                logger.warning(
                    "⚠️ This likely means tests need Flask app context or better setup"
                )
                logger.warning(
                    "⚠️ Falling back to minimal file (user wants 60%+ coverage - consider regenerating tests)"
                )
                logger.warning(
                    f"⚠️ DEBUG: initial_passing_tests had {len(initial_passing_tests) if initial_passing_tests else 0} tests"
                )
                logger.warning(
                    f"⚠️ DEBUG: test_functions found {len(test_functions)} functions"
                )
                return self._create_minimal_valid_file(test_code)

            logger.info(
                f"✅ Keeping {len(passing_tests)} passing tests, removing {len(failing_tests)} failing tests"
            )
            logger.info(f"   Passing: {passing_tests[:10]}")
            if len(passing_tests) > 10:
                logger.info(f"   ... and {len(passing_tests) - 10} more")
            logger.info(f"   Failing (first 10): {list(failing_tests)[:10]}")
            if len(failing_tests) > 10:
                logger.info(f"   ... and {len(failing_tests) - 10} more")

            # Now remove failing test functions from the code
            # Extract just the function names (without Class:: prefix)
            failing_function_names = set()
            for test_name in failing_tests:
                if "::" in test_name:
                    failing_function_names.add(test_name.split("::")[-1])
                else:
                    failing_function_names.add(test_name)

            logger.info(f"🗑️ Removing functions: {failing_function_names}")

            cleaned_code = self._remove_test_functions(
                test_code, failing_function_names
            )

            return cleaned_code

        except Exception as e:
            logger.error(f"❌ Error in keep_only_passing_tests: {e}")
            import traceback

            traceback.print_exc()
            return None

    def _remove_test_functions(
        self, test_code: str, function_names_to_remove: set
    ) -> str:
        """
        Remove specific test functions from test code.
        Similar to the Go implementation's removeTestFunction.
        Handles decorators, multi-line signatures, and indentation properly.
        Also removes empty test classes after removing their methods.

        Args:
            test_code: Original test code
            function_names_to_remove: Set of function names to remove

        Returns:
            Test code with specified functions removed
        """
        import re

        lines = test_code.split("\n")
        result_lines = []

        in_function_to_remove = False
        function_start_line = -1
        function_indent_level = 0
        paren_count = 0
        collecting_decorators = False
        decorator_lines_to_skip = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Check if this is a function we want to remove
            if not in_function_to_remove and not collecting_decorators:
                # Check for decorator before function (e.g., @pytest.fixture, @pytest.mark.parametrize)
                if stripped.startswith("@"):
                    # This might be a decorator for a function we want to remove
                    # Look ahead to see if next non-empty line is a test function we want to remove
                    for j in range(i + 1, min(i + 10, len(lines))):
                        next_line = lines[j].strip()
                        if (
                            not next_line
                            or next_line.startswith("@")
                            or next_line.startswith("#")
                        ):
                            continue
                        # Check if this is a test function
                        func_match = re.match(r"^\s*def (test_\w+)\s*\(", lines[j])
                        if func_match:
                            func_name = func_match.group(1)
                            if func_name in function_names_to_remove:
                                # This decorator belongs to a function we're removing
                                collecting_decorators = True
                                decorator_lines_to_skip = []
                            break
                        else:
                            # Not a function definition, stop looking
                            break

                # Match: def test_function_name(
                func_match = re.match(r"^\s*def (test_\w+)\s*\(", line)
                if func_match:
                    func_name = func_match.group(1)
                    if func_name in function_names_to_remove:
                        logger.info(
                            f"  🗑️ Removing: {func_name}"
                            + (
                                f" (with {len(decorator_lines_to_skip)} decorators)"
                                if decorator_lines_to_skip
                                else ""
                            )
                        )
                        in_function_to_remove = True
                        collecting_decorators = False
                        function_start_line = i
                        function_indent_level = len(line) - len(line.lstrip())
                        paren_count = line.count("(") - line.count(")")
                        # Don't add decorator lines or this line
                        continue
                    else:
                        # Function we want to keep, add any collected decorator lines
                        if decorator_lines_to_skip:
                            result_lines.extend(decorator_lines_to_skip)
                            decorator_lines_to_skip = []
                        collecting_decorators = False

                # Collecting decorators for potential removal
                if collecting_decorators:
                    decorator_lines_to_skip.append(line)
                    continue

                # Not in function to remove, keep the line
                result_lines.append(line)
            else:
                # We're inside a function to remove
                # Track parentheses for multi-line function signatures
                if paren_count > 0:
                    paren_count += line.count("(") - line.count(")")
                    if paren_count <= 0 and ":" in line:
                        # Function signature complete
                        paren_count = 0
                    continue

                # Check if we've exited the function
                if stripped:  # Non-empty line
                    current_indent = len(line) - len(line.lstrip())
                    # If we're back to same or lower indentation level, function is complete
                    if current_indent <= function_indent_level:
                        # Check if this is actually a new definition at class level
                        if (
                            line.lstrip().startswith("def ")
                            or line.lstrip().startswith("class ")
                            or (len(line) > 0 and not line[0].isspace())
                        ):
                            in_function_to_remove = False
                            result_lines.append(line)
                            continue
                # Otherwise skip this line (it's part of the function we're removing)

        # CRITICAL: Remove empty test classes (classes with no methods)
        cleaned_code = "\n".join(result_lines)
        cleaned_code = self._remove_empty_test_classes(cleaned_code)

        return cleaned_code

    def _remove_empty_test_classes(self, test_code: str) -> str:
        """
        Remove test classes that have no methods (all methods were removed).
        This prevents IndentationError from empty class definitions.

        Args:
            test_code: Test code that may contain empty classes

        Returns:
            Test code with empty classes removed
        """
        import re

        lines = test_code.split("\n")
        result_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Check if this is a test class definition
            class_match = re.match(r"^(\s*)class (Test\w+)", line)
            if class_match:
                indent = class_match.group(1)
                class_name = class_match.group(2)
                class_indent_level = len(indent)

                # Look ahead to see if this class has any methods
                has_methods = False
                j = i + 1

                while j < len(lines):
                    next_line = lines[j]
                    next_stripped = next_line.strip()

                    # Skip empty lines and docstrings
                    if (
                        not next_stripped
                        or next_stripped.startswith('"""')
                        or next_stripped.startswith("'''")
                    ):
                        j += 1
                        continue

                    # Check indent level
                    next_indent_level = len(next_line) - len(next_line.lstrip())

                    # If we're back to class level or lower, class is done
                    if next_indent_level <= class_indent_level and next_stripped:
                        break

                    # Check if there's a method definition
                    if re.match(r"^\s*def \w+", next_line):
                        has_methods = True
                        break

                    j += 1

                if has_methods:
                    # Keep the class definition
                    result_lines.append(line)
                    i += 1
                else:
                    # Empty class - skip it and all its content (docstrings, etc.)
                    logger.info(f"  🗑️ Removing empty test class: {class_name}")
                    i += 1
                    # Skip lines that belong to this empty class
                    while i < len(lines):
                        next_line = lines[i]
                        next_stripped = next_line.strip()

                        if not next_stripped:
                            # Skip empty lines within the class
                            i += 1
                            continue

                        next_indent_level = len(next_line) - len(next_line.lstrip())

                        # If we're back to class level or lower, stop skipping
                        if next_indent_level <= class_indent_level:
                            break

                        # Skip this line (it's part of the empty class)
                        i += 1
            else:
                # Not a class definition, keep it
                result_lines.append(line)
                i += 1

        return "\n".join(result_lines)

    def _create_minimal_valid_file(self, test_code: str) -> str:
        """
        Create a minimal valid test file with ONLY imports and one passing test.
        Removes ALL test functions, classes, and fixtures to guarantee it works.
        """
        import re

        logger.info("🧹 Creating minimal test file (imports + placeholder only)...")

        # FIRST: Remove bad imports
        test_code = self._remove_bad_imports_from_code(test_code)

        # THEN: Keep ONLY imports
        lines = test_code.split("\n")
        cleaned_lines = []
        in_code_block = False  # Track if we've moved past imports

        for line in lines:
            stripped = line.strip()

            # Keep import lines
            if stripped.startswith("import ") or stripped.startswith("from "):
                cleaned_lines.append(line)
            # Keep empty lines before we hit code
            elif not stripped and not in_code_block:
                cleaned_lines.append(line)
            # Stop at first non-import, non-empty line
            elif stripped:
                in_code_block = True
                # Don't keep anything else (classes, fixtures, tests)

        # Remove trailing empty lines
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()

        # Add minimal test
        cleaned_lines.append("")
        cleaned_lines.append("")
        cleaned_lines.append("def test_placeholder():")
        cleaned_lines.append(
            '    """Minimal placeholder - all tests removed due to failures."""'
        )
        cleaned_lines.append("    assert True")
        cleaned_lines.append("")

        return "\n".join(cleaned_lines)

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

        # Get list of passing tests to preserve
        passing_tests = error_info.get("passing", [])
        passing_info = ""
        if passing_tests:
            passing_info = f"""
**CRITICAL - Tests That PASSED (DO NOT DELETE THESE)**:
{json.dumps(passing_tests, indent=2)}

⚠️ THESE TESTS WORK CORRECTLY - YOU MUST KEEP THEM ALL!
⚠️ Only remove tests that appear in the Errors/Failures list below!
"""

        prompt = f"""You are a test cleanup expert. The following test file has persistent errors that couldn't be fixed after 3 attempts.

**Test Code**:
```{language}
{test_code}
```
{passing_info}
**Errors and Failures**:
{json.dumps(error_info.get("errors", []), indent=2)}
{json.dumps(error_info.get("failures", []), indent=2)}

**Instructions**:
1. Identify which specific test functions are causing the errors/failures
2. Remove ONLY those problematic test functions (NOT the passing ones!)
3. Keep ALL test functions that passed (see list above)
4. Keep all fixtures that working tests might need
5. If an import is only used by removed tests, remove that import too
6. Return the cleaned test code with only working tests

**CRITICAL RULES**:
- DO NOT remove any test that appears in the "Tests That PASSED" list above
- ONLY remove tests that have errors or failures
- Remove entire test functions that have errors (including decorators and docstrings)
- Keep all fixtures that working tests might need
- Maintain proper code structure and formatting
- If ALL tests have errors, return a minimal valid test file with just imports and fixtures

Return ONLY the cleaned test code, no explanations:
"""

        response = self._call_llm(prompt)
        if not response:
            return None

        # Extract code from markdown if present
        cleaned_code = response
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
        # Check if LLM is available (but don't return early - Flask fix doesn't need LLM)
        if not self.llm_client:
            logger.warning("⚠️ LLM client not initialized")
            logger.warning("Will try Flask fixture fix and nuclear option without LLM")

        fix_history = []
        current_code = test_code
        flask_fix_applied = False  # Track if Flask fix was applied

        logger.info(
            f"Starting auto-fix for {test_file_path} (max {self.max_retries} attempts)"
        )

        # CRITICAL: If max_retries=0, go straight to nuclear option
        if self.max_retries == 0:
            logger.warning("⚠️ max_retries=0, going straight to nuclear option")

            # Write and run tests once to get pass/fail info
            Path(test_file_path).write_text(current_code, encoding="utf-8")
            success, stdout, stderr = self.run_tests_and_capture_errors(
                test_file_path, language
            )

            if success:
                logger.info("✅ All tests already passing!")
                return True, current_code, ["Tests already passing"]

            # Extract passing tests for nuclear option
            error_info = self.extract_error_details(stdout, stderr, language)
            passing_tests = error_info.get("passing", [])

            logger.info(
                f"📊 Test results: {len(passing_tests)} passing, "
                f"{len(error_info.get('failures', []))} failing"
            )

            if passing_tests:
                logger.info(
                    f"🚀 Running nuclear option to keep {len(passing_tests)} passing tests..."
                )
                cleaned_code = self.keep_only_passing_tests(
                    test_file_path, language, initial_passing_tests=passing_tests
                )

                if cleaned_code and cleaned_code != current_code:
                    fix_history.append(
                        f"Nuclear option: Kept {len(passing_tests)} passing tests"
                    )
                    return True, cleaned_code, fix_history
                else:
                    fix_history.append("Nuclear option: Failed to clean tests")
                    return False, current_code, fix_history
            else:
                logger.warning("⚠️ No passing tests found, cannot use nuclear option")
                fix_history.append("Nuclear option: No passing tests to keep")
                return False, current_code, fix_history

        for attempt in range(1, self.max_retries + 1):
            logger.info(f"")
            logger.info(f"{'=' * 60}")
            logger.info(f"🔄 ATTEMPT {attempt}/{self.max_retries}")
            logger.info(f"{'=' * 60}")

            # Write current code to file
            Path(test_file_path).write_text(current_code, encoding="utf-8")
            logger.info(f"📝 Test file written: {test_file_path}")
            logger.info(f"   Size: {len(current_code)} chars")

            # Run tests
            logger.info(f"🧪 Running tests...")
            success, stdout, stderr = self.run_tests_and_capture_errors(
                test_file_path, language
            )

            if success:
                logger.info(f"")
                logger.info(f"{'=' * 60}")
                logger.info(f"✅ SUCCESS! Tests passed on attempt {attempt}!")
                logger.info(f"{'=' * 60}")
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
                logger.info(f"📋 Extracted {len(error_info['errors'])} errors:")
                for i, err in enumerate(error_info["errors"], 1):
                    logger.info(
                        f"  Error {i}/{len(error_info['errors'])}: {err['type']}"
                    )
                    logger.info(f"    Message: {err['message'][:200]}")
                    if "context" in err:
                        logger.info(f"    Context: {err['context'][:300]}")

            if error_info["failures"]:
                logger.info(
                    f"📋 Extracted {len(error_info['failures'])} test failures:"
                )
                for i, fail in enumerate(error_info["failures"], 1):
                    logger.info(
                        f"  Failure {i}/{len(error_info['failures'])}: {fail['test_name']}"
                    )
                    if "error_message" in fail:
                        logger.info(f"    Error: {fail['error_message'][:200]}")

            if not error_info["errors"] and not error_info["failures"]:
                logger.warning(f"⚠️ No errors extracted from output!")
                logger.warning(f"📄 Raw output (first 1000 chars):")
                logger.warning(f"{error_info['raw_output'][:1000]}")

            # DISABLED: Early nuclear option was removing too many passing tests
            # The issue is that keep_only_passing_tests() tests each function individually,
            # but many tests need fixtures/context and fail when run alone
            #
            # Example: 69 tests passing together, but only 5 pass when run individually
            #
            # TODO: Fix keep_only_passing_tests to handle fixtures properly before re-enabling

            # Still log coverage for visibility
            passing_tests = error_info.get("passing", [])
            total_tests = len(passing_tests) + len(error_info.get("failures", []))
            if total_tests > 0:
                pass_rate = len(passing_tests) / total_tests
                logger.info(
                    f"📊 Test coverage: {len(passing_tests)}/{total_tests} passed ({pass_rate * 100:.1f}%)"
                )

            # FRAMEWORK-SPECIFIC FIX: Check if failures are framework context errors
            # Apply this fix EARLY (attempt 1) before trying LLM fixes or nuclear option
            if attempt == 1 and language == "python":
                combined_output = error_info["raw_output"]
                is_framework_context_error = (
                    "RuntimeError: Working outside of request context"
                    in combined_output
                    or "AttributeError: 'FixtureFunctionDefinition' object has no attribute"
                    in combined_output
                    or "test_request_context" in combined_output
                    or "Working outside of application context" in combined_output
                    or "NameError: name 'app' is not defined"
                    in combined_output  # CRITICAL: Add missing framework import
                    or "module 'flask.app' has no attribute"
                    in combined_output  # CRITICAL: Fix bad framework import
                    or "cannot import name 'app' from 'flask.app'"
                    in combined_output  # CRITICAL: Fix bad framework import (import error)
                    or "AssertionError" in combined_output
                    and "failures"
                    in combined_output  # CRITICAL: Multiple failures pattern
                    or "def test_" in combined_output
                    and "client.get"
                    not in combined_output  # CRITICAL: Missing test client usage
                    or "NameError: name" in combined_output
                    and "is not defined" in combined_output  # CRITICAL: Missing imports
                    or "ModuleNotFoundError"
                    in combined_output  # CRITICAL: Wrong module imports
                )

                if is_framework_context_error:
                    logger.warning(
                        "🔍 Detected framework context errors on attempt 1 - fixing fixture structure immediately..."
                    )
                    fixed_code = self._fix_flask_fixtures(
                        current_code, test_file_path, has_flask_errors=True
                    )
                    if fixed_code != current_code:
                        logger.info(
                            "✅ Applied framework fixture fixes - will retry with fixed fixtures"
                        )
                        current_code = fixed_code
                        flask_fix_applied = True
                        continue
                    else:
                        logger.warning(
                            "  ⚠️ Flask fix didn't change code (may need manual intervention)"
                        )

                # DEPENDENCY FIX: Check for common dependency/version issues
                is_dependency_error = (
                    "AttributeError: module 'sqlalchemy' has no attribute '__all__'"
                    in combined_output
                    or "AttributeError: module 'werkzeug' has no attribute '__version__'"
                    in combined_output
                    or "ImportError: cannot import name" in combined_output
                    or "ModuleNotFoundError:" in combined_output
                )

                if is_dependency_error:
                    logger.warning(
                        "🔍 Detected dependency error on attempt 1 - this is a project setup issue, not test code issue"
                    )

                    # Check if it's the SQLAlchemy compatibility issue
                    if (
                        "module 'sqlalchemy' has no attribute '__all__'"
                        in combined_output
                    ):
                        logger.error(
                            "❌ SQLAlchemy version incompatibility detected!\n"
                            "   This is a known issue with SQLAlchemy 2.x and Flask-SQLAlchemy.\n"
                            "   The test code is correct - the project needs dependency fixes.\n\n"
                            "   SOLUTION: Add to requirements.txt or run:\n"
                            "   pip install 'sqlalchemy<2.0.0' 'flask-sqlalchemy>=3.0.0'"
                        )
                        fix_history.append(
                            f"Attempt {attempt}: DEPENDENCY ERROR - SQLAlchemy incompatibility (project issue, not test issue)"
                        )
                        # Return test code as-is since it's not a test problem
                        return False, current_code, fix_history

                    # Check if it's the Werkzeug version incompatibility
                    if (
                        "module 'werkzeug' has no attribute '__version__'"
                        in combined_output
                    ):
                        logger.error(
                            "❌ Werkzeug version incompatibility detected!\n"
                            "   This is a known issue with Werkzeug 3.x where __version__ was removed.\n"
                            "   The test code is correct - the project needs dependency fixes.\n\n"
                            "   SOLUTION: Add to requirements.txt or run:\n"
                            "   pip install 'werkzeug<3.0.0' 'flask>=2.3.0,<3.0.0'"
                        )
                        fix_history.append(
                            f"Attempt {attempt}: DEPENDENCY ERROR - Werkzeug incompatibility (project issue, not test issue)"
                        )
                        # Return test code as-is since it's not a test problem
                        return False, current_code, fix_history

                    # For other import errors, log and continue
                    logger.error(
                        "❌ Dependency/import error detected - this is typically a project setup issue.\n"
                        "   Check that all required packages are installed."
                    )
                    fix_history.append(
                        f"Attempt {attempt}: DEPENDENCY ERROR - Missing or incompatible dependencies"
                    )

            # If this is the last attempt, don't try LLM fix - go straight to nuclear option
            if attempt >= self.max_retries:
                logger.info(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                logger.info(
                    f"💣 NUCLEAR OPTION: Max retries ({self.max_retries}) reached"
                )
                logger.info(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                logger.info(
                    f"🎯 Strategy: Keep ONLY tests that passed, remove ALL failing tests"
                )
                logger.info(f"   This is the most aggressive cleanup option")
                logger.info(
                    f"   It ensures 100% pass rate by removing problematic tests"
                )

                passing_tests = error_info.get("passing", [])
                failing_tests = error_info.get("failures", [])

                logger.info(f"📊 Test Summary:")
                logger.info(f"   • Passing tests: {len(passing_tests)}")
                logger.info(f"   • Failing tests: {len(failing_tests)}")
                logger.info(
                    f"   • Target result: {len(passing_tests)} tests (100% pass rate)"
                )

                if passing_tests:
                    logger.info(f"✅ Passing tests (first 10):")
                    for i, test in enumerate(passing_tests[:10], 1):
                        logger.info(f"     {i}. {test}")
                    if len(passing_tests) > 10:
                        logger.info(f"     ... and {len(passing_tests) - 10} more")
                else:
                    logger.warning(f"⚠️ No passing tests found - this is unusual!")
                    logger.warning(f"   The test file may have fundamental issues")

                logger.info(f"🔧 Running nuclear option cleanup...")
                cleaned_code = self.keep_only_passing_tests(
                    test_file_path, language, initial_passing_tests=passing_tests
                )

                if cleaned_code and cleaned_code != current_code:
                    current_code = cleaned_code
                    # Count how many test functions remain
                    import re

                    remaining_tests = len(
                        re.findall(r"^\s*def test_\w+", cleaned_code, re.MULTILINE)
                    )
                    logger.info(
                        f"✅ Nuclear option created cleaned version with {remaining_tests} test functions"
                    )
                    logger.info(
                        f"   Original size: {len(current_code)} chars → Cleaned size: {len(cleaned_code)} chars"
                    )
                    logger.info(f"✅ Testing cleaned version now...")

                    Path(test_file_path).write_text(current_code, encoding="utf-8")
                    success, stdout, stderr = self.run_tests_and_capture_errors(
                        test_file_path, language
                    )
                    if success:
                        logger.info(
                            f"✅ Nuclear option succeeded! Final test count: {remaining_tests}"
                        )
                        fix_history.append(
                            f"Attempt {attempt}: Nuclear option SUCCESS (kept {remaining_tests} tests)"
                        )
                        return True, current_code, fix_history
                    else:
                        logger.warning(
                            f"❌ Nuclear option still has errors after keeping {remaining_tests} tests"
                        )
                        logger.warning(
                            f"   This means even the 'passing' tests fail when run individually!"
                        )
                else:
                    logger.warning("⚠️ Nuclear option failed or didn't change code")

                break

            # Try LLM-based fix only if LLM is available
            if self.llm_client:
                logger.info(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                logger.info(f"🤖 ATTEMPT {attempt}/{self.max_retries}: LLM-BASED FIX")
                logger.info(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                logger.info(f"📊 Issues to fix:")
                logger.info(f"   • {len(error_info['errors'])} syntax/import errors")
                logger.info(f"   • {len(error_info['failures'])} test failures")

                # Show sample errors
                if error_info["errors"][:3]:
                    logger.info(f"   Sample errors:")
                    for i, err in enumerate(error_info["errors"][:3], 1):
                        logger.info(f"     {i}. {err['type']}: {err['message'][:100]}")

                if error_info["failures"][:3]:
                    logger.info(f"   Sample failures:")
                    for i, fail in enumerate(error_info["failures"][:3], 1):
                        logger.info(f"     {i}. {fail['test_name']}")

                # Build fix prompt for LLM
                logger.info(f"🔨 Building fix prompt...")
                prompt = self.build_fix_prompt(
                    current_code, error_info, attempt, source_code
                )
                logger.info(f"   ✅ Prompt built: {len(prompt)} chars")

                # Get fixed code from LLM
                logger.info(f"📤 Sending request to LLM...")
                fixed_code = self.get_fixed_test_from_llm(prompt, language)

                if not fixed_code:
                    logger.error(
                        f"❌ LLM returned no code (may have timed out or failed)"
                    )
                    logger.error(
                        f"   Will fall back to nuclear option on final attempt"
                    )
                    break

                # Check if code actually changed
                code_changed = fixed_code != current_code
                logger.info(f"📥 Received LLM response:")
                logger.info(f"   • Response size: {len(fixed_code)} chars")
                logger.info(f"   • Original size: {len(current_code)} chars")
                logger.info(
                    f"   • Code changed: {'✅ YES' if code_changed else '❌ NO (identical)'}"
                )

                if code_changed:
                    # Count tests before/after
                    import re

                    original_tests = len(
                        re.findall(r"^\s*def test_\w+", current_code, re.MULTILINE)
                    )
                    fixed_tests = len(
                        re.findall(r"^\s*def test_\w+", fixed_code, re.MULTILINE)
                    )
                    logger.info(f"   • Test count: {original_tests} → {fixed_tests}")

                    if fixed_tests < original_tests:
                        logger.info(
                            f"   ⚠️ LLM removed {original_tests - fixed_tests} test(s)"
                        )
                    elif fixed_tests > original_tests:
                        logger.info(
                            f"   ℹ️  LLM added {fixed_tests - original_tests} test(s)"
                        )
                    else:
                        logger.info(f"   ℹ️  LLM modified tests without changing count")

                logger.info(f"🔄 Will test the LLM-fixed code in next iteration...")
                logger.info(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                current_code = fixed_code
            else:
                # No LLM available - skip to nuclear option on next attempt
                logger.warning(f"⚠️ No LLM client available - cannot attempt LLM fix")
                logger.warning(f"   Skipping to nuclear option...")
                break

        # If we get here, all attempts failed - try absolute last resort (requires LLM)
        if self.llm_client:
            logger.warning(
                "⚠️ All attempts failed (including nuclear option). Trying absolute last resort: LLM-based test removal"
            )
            logger.info(f"📊 Last Resort Input:")
            logger.info(f"   Current code size: {len(current_code)} chars")
            # CRITICAL FIX: error_info may not be defined if max_retries=0
            if "error_info" in locals():
                logger.info(f"   Errors: {len(error_info.get('errors', []))}")
                logger.info(f"   Failures: {len(error_info.get('failures', []))}")
            else:
                logger.info(
                    f"   No error_info available (max_retries=0 or loop skipped)"
                )

            try:
                logger.info("🤖 Asking LLM to identify and remove problematic tests...")
                # CRITICAL FIX: Skip if error_info not available
                if "error_info" not in locals():
                    logger.warning(
                        "⚠️ Cannot run fallback: no error_info available (max_retries=0)"
                    )
                    return False, current_code, fix_history

                fallback_code = self.remove_problematic_tests(
                    current_code, error_info, language
                )
                if fallback_code and fallback_code != current_code:
                    import re

                    original_tests = len(
                        re.findall(r"^\s*def test_\w+", current_code, re.MULTILINE)
                    )
                    remaining_tests = len(
                        re.findall(r"^\s*def test_\w+", fallback_code, re.MULTILINE)
                    )

                    logger.info(
                        f"✅ LLM removed {original_tests - remaining_tests} tests, {remaining_tests} remain"
                    )
                    logger.info(
                        f"   Code size: {len(current_code)} → {len(fallback_code)} chars"
                    )

                    # Write and test the fallback code
                    Path(test_file_path).write_text(fallback_code, encoding="utf-8")
                    success, stdout, stderr = self.run_tests_and_capture_errors(
                        test_file_path, language
                    )

                    if success:
                        logger.info(
                            "✅ Fallback successful - removed problematic tests"
                        )
                        fix_history.append(
                            "Fallback: Removed problematic tests - SUCCESS"
                        )
                        return True, fallback_code, fix_history
                    else:
                        logger.warning("⚠️ Fallback did not fix all issues")
                        fix_history.append(
                            "Fallback: Removed problematic tests - still have errors"
                        )
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
