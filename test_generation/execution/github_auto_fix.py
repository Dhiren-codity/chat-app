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
    Pre-process test code to remove bad imports AND any code that uses them.
    This prevents collection errors from blocking auto-fix.
    """
    if language != 'python':
        return test_code

    import re

    # Find bad imports and track what names they import
    bad_imports = {}
    lines = test_code.split('\n')

    for line in lines:
        # Check for imports that commonly fail
        match = re.search(r'from\s+(\S+)\s+import\s+(.+)', line)
        if match:
            module = match.group(1)
            imports = match.group(2)

            # Common problematic imports
            if any(name in imports for name in ['decorated_function', 'nonexistent', 'placeholder', 'your_', 'module_name']):
                print(f"  🔧 Detected bad import: {line.strip()}")
                # Extract all imported names
                import_names = [n.strip().split(' as ')[0] for n in imports.split(',')]
                for name in import_names:
                    if any(bad in name for bad in ['decorated_function', 'nonexistent', 'placeholder', 'your_', 'module_name']):
                        bad_imports[name.strip()] = True

    if not bad_imports:
        return test_code

    print(f"  🗑️ Removing {len(bad_imports)} bad imports and their usages: {list(bad_imports.keys())}")

    # Now remove imports and any functions/tests that use them
    cleaned_lines = []
    skip_function = False
    skip_import = False
    current_function_indent = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this line imports something bad
        if any(f'import {name}' in line or f'import.*{name}' in stripped for name in bad_imports):
            print(f"  ❌ Removing import line: {stripped[:80]}")
            skip_import = True
            continue

        # Skip continuation of multi-line imports
        if skip_import:
            if stripped == '' or not stripped.startswith(('import', 'from', ',')):
                skip_import = False
            else:
                continue

        # Check if this is a function/class definition
        if stripped.startswith('def ') or stripped.startswith('class '):
            # Check if this function uses any bad imports
            function_code = '\n'.join(lines[i:min(i+100, len(lines))])
            uses_bad_import = any(re.search(rf'\b{name}\b', function_code) for name in bad_imports)

            if uses_bad_import:
                skip_function = True
                current_function_indent = len(line) - len(line.lstrip())
                print(f"  ❌ Removing function using bad import: {stripped[:80]}")
                continue

        # Skip lines that are part of a bad function
        if skip_function:
            line_indent = len(line) - len(line.lstrip())
            # Continue skipping until we're back to same or lower indentation
            if stripped and line_indent > current_function_indent:
                continue
            else:
                skip_function = False

        # Check if line uses bad imports directly
        if any(re.search(rf'\b{name}\b', line) for name in bad_imports):
            print(f"  ❌ Removing line using bad import: {stripped[:80]}")
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


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
