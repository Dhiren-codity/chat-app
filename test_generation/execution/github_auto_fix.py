#!/usr/bin/env python3
"""
GitHub Actions Auto-Fix Script
Runs in GitHub Actions to automatically fix failing tests for ALL languages.
Supports: Python, JavaScript, TypeScript, Go, Java
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, '.')

from test_generation.execution.test_auto_fixer import TestAutoFixer


def detect_language(file_path: str) -> str:
    """Detect programming language from file extension and patterns."""
    ext = Path(file_path).suffix.lower()
    file_name = Path(file_path).name

    # Language detection by file extension and naming patterns
    if ext == '.py' or '_test.py' in file_name or 'test_' in file_name:
        return 'python'
    elif ext in ['.js', '.jsx'] or '.test.js' in file_name or '.spec.js' in file_name:
        return 'javascript'
    elif ext in ['.ts', '.tsx'] or '.test.ts' in file_name or '.spec.ts' in file_name:
        return 'javascript'  # TypeScript uses same test tools
    elif ext == '.go' or '_test.go' in file_name:
        return 'go'
    elif ext == '.java' or 'Test.java' in file_name:
        return 'java'
    else:
        # Default to python if can't detect
        return 'python'


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
    if language != 'python':
        return test_code

    # Just return the code as-is
    # Let the auto-fix nuclear option handle bad imports by removing failing tests
    print(f"  📝 Pre-processor: Skipping import removal, letting nuclear option handle it")
    return test_code


def main():
    """Run auto-fix for test files provided as arguments."""
    if len(sys.argv) < 2:
        print("Usage: github_auto_fix.py <test_file1> [test_file2] ...")
        print("Supports: Python, JavaScript, TypeScript, Go, Java")
        sys.exit(1)

    test_files = sys.argv[1:]
    auto_fixer = TestAutoFixer(max_retries=3)

    all_success = True

    print(f"🚀 Starting auto-fix for {len(test_files)} test file(s)...")

    for test_file in test_files:
        language = detect_language(test_file)
        print(f'\n🔧 Auto-fixing {test_file} (Language: {language.upper()})...')

        if not Path(test_file).exists():
            print(f'❌ Test file not found: {test_file}')
            all_success = False
            continue

        try:
            test_code = Path(test_file).read_text()

            # Pre-process: Remove obvious bad imports before auto-fix
            test_code = remove_bad_imports(test_code, language)

            success, fixed_code, history = auto_fixer.auto_fix_test(
                test_code=test_code,
                test_file_path=test_file,
                language=language
            )

            if success:
                print(f'✅ Auto-fix successful for {test_file}')
                Path(test_file).write_text(fixed_code)
            else:
                print(f'⚠️ Auto-fix failed for {test_file} after 3 attempts')
                all_success = False
                print(f'   Fix history:')
                for i, h in enumerate(history, 1):
                    print(f'   Attempt {i}: {h}')
        except Exception as e:
            print(f'❌ Error during auto-fix for {test_file}: {e}')
            import traceback
            traceback.print_exc()
            all_success = False

    print('\n' + '='*60)
    if all_success:
        print('✅ All tests auto-fixed successfully!')
        print('='*60)
        sys.exit(0)
    else:
        print('⚠️ Some tests could not be auto-fixed')
        print('='*60)
        sys.exit(1)


if __name__ == '__main__':
    main()
