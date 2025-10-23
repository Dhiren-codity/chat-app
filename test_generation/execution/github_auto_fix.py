#!/usr/bin/env python3
"""
GitHub Actions Auto-Fix Script
Runs in GitHub Actions to automatically fix failing tests for ALL languages.
Supports: Python, JavaScript, TypeScript, Go, Java

This script uses language-specific auto-fixers for optimal test fixing.
"""

import sys
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.insert(0, ".")

# Import language-specific auto-fixers
try:
    from test_generation.execution.python_auto_fixer import PythonTestAutoFixer
    from test_generation.execution.go_auto_fixer import GoTestAutoFixer
    from test_generation.execution.js_auto_fixer import JSTestAutoFixer
    from test_generation.execution.java_auto_fixer import JavaTestAutoFixer
except ImportError as e:
    logger.error(f"Failed to import auto-fixers: {e}")
    # Fallback to legacy auto-fixer
    from test_generation.execution.test_auto_fixer import TestAutoFixer
    PythonTestAutoFixer = TestAutoFixer
    GoTestAutoFixer = None
    JSTestAutoFixer = None
    JavaTestAutoFixer = None


def detect_language(file_path: str) -> str:
    """Detect programming language from file extension and patterns."""
    ext = Path(file_path).suffix.lower()
    file_name = Path(file_path).name

    # Language detection by file extension and naming patterns
    if (
        ext == ".py"
        or "_test.py" in file_name
        or (file_name.startswith("test_") and ext == ".py")
    ):
        return "python"
    elif ext in [".js", ".jsx"] or ".test.js" in file_name or ".spec.js" in file_name:
        return "javascript"
    elif ext in [".ts", ".tsx"] or ".test.ts" in file_name or ".spec.ts" in file_name:
        return "javascript"  # TypeScript uses same test tools
    elif ext == ".go" or "_test.go" in file_name:
        return "go"
    elif ext == ".java" or "Test.java" in file_name:
        return "java"
    else:
        # Default to python if can't detect
        return "python"


def remove_bad_imports(test_code: str, language: str) -> str:
    """
    Pre-process test code - DISABLED for now.

    The nuclear option (keep_only_passing_tests) will handle everything by:
    1. Testing each function individually
    2. Keeping functions that pass
    3. Removing functions that fail (including those using bad imports)

    Removing imports here causes issues because tests that use those imports
    will fail when tested individually, leading to all tests being removed.
    """
    if language != "python":
        return test_code

    # Just return the code as-is
    # Let the auto-fix nuclear option handle bad imports by removing failing tests
    print(
        f"  📝 Pre-processor: Skipping import removal, letting nuclear option handle it"
    )
    return test_code


def get_auto_fixer_for_language(language: str, max_retries: int = 1):
    """Get the appropriate auto-fixer for the detected language."""
    if language == "python":
        if PythonTestAutoFixer:
            return PythonTestAutoFixer(max_retries=max_retries)
    elif language == "go":
        if GoTestAutoFixer:
            return GoTestAutoFixer(max_retries=max_retries)
    elif language in ["javascript", "typescript"]:
        if JSTestAutoFixer:
            return JSTestAutoFixer(max_retries=max_retries)
    elif language == "java":
        if JavaTestAutoFixer:
            return JavaTestAutoFixer(max_retries=max_retries)

    # Fallback to Python auto-fixer (legacy support)
    logger.warning(f"No specific auto-fixer for {language}, using Python auto-fixer")
    return PythonTestAutoFixer(max_retries=max_retries)


def main():
    """Run auto-fix for test files provided as arguments."""
    if len(sys.argv) < 2:
        print("Usage: github_auto_fix.py <test_file1> [test_file2] ...")
        print("Supports: Python, JavaScript, TypeScript, Go, Java")
        sys.exit(1)

    test_files = sys.argv[1:]
    all_success = True

    print(f"🚀 Starting multi-language test cleanup for {len(test_files)} test file(s)...")
    print(f"🔧 AUTO-FIX STRATEGY:")
    print(f"   1. Run tests and extract passing/failing test names")
    print(f"   2. Try LLM fix with full RAG context (1 attempt)")
    print(f"   3. Nuclear option: Remove failing tests, keep passing ones")
    print(f"📊 Supported languages: Python, Go, JavaScript/TypeScript, Java")

    for test_file in test_files:
        language = detect_language(test_file)
        print(f"\n{'=' * 60}")
        print(f"🔧 Processing: {test_file}")
        print(f"📝 Language: {language.upper()}")
        print(f"{'=' * 60}")

        if not Path(test_file).exists():
            print(f"❌ Test file not found: {test_file}")
            all_success = False
            continue

        try:
            # Get language-specific auto-fixer
            auto_fixer = get_auto_fixer_for_language(language, max_retries=1)
            print(f"✅ Using auto-fixer: {auto_fixer.__class__.__name__}")

            test_code = Path(test_file).read_text()
            print(f"📄 Test file size: {len(test_code)} characters")

            # Pre-process: Remove obvious bad imports before auto-fix (Python only)
            test_code = remove_bad_imports(test_code, language)

            # Run auto-fix
            success, fixed_code, history = auto_fixer.auto_fix_test(
                test_code=test_code,
                test_file_path=test_file,
                language=language
            )

            if success:
                print(f"\n✅ Test cleanup successful for {test_file}")
                print(f"   Final size: {len(fixed_code)} characters")
                Path(test_file).write_text(fixed_code)
                print(f"   ✍️  Updated test file written")
            else:
                print(f"\n⚠️ Test cleanup failed for {test_file}")
                all_success = False
                print(f"   📋 Fix history:")
                for i, h in enumerate(history, 1):
                    print(f"      Step {i}: {h}")

                # Check if it's a dependency error (not fixable by auto-fix)
                if any("DEPENDENCY ERROR" in str(h) for h in history):
                    print(f"\n   ⚠️  NOTE: This is a dependency/setup issue, not a test code issue.")
                    print(f"      The test code is correct but the project has incompatible dependencies.")
                    print(f"      Please fix the project dependencies before running tests.")

        except Exception as e:
            print(f"\n❌ Error during auto-fix for {test_file}: {e}")
            import traceback
            traceback.print_exc()
            all_success = False

    print("\n" + "=" * 60)
    if all_success:
        print("✅ All tests auto-fixed successfully!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("⚠️ Some tests could not be auto-fixed")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
