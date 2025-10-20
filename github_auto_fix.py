#!/usr/bin/env python3
"""
GitHub Auto-Fix Script for Test Files
Downloads and runs the auto-fixer from codity.ai repository
"""

import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

def download_file(url, local_path):
    """Download a file from URL to local path."""
    try:
        result = subprocess.run(['curl', '-s', '-o', local_path, url], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 github_auto_fix.py <test_file1> [test_file2] ...")
        sys.exit(1)
    
    test_files = sys.argv[1:]
    print(f"🔧 Auto-fixing {len(test_files)} test file(s)...")
    
    # Create temporary directory for auto-fixer files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Download auto-fixer files
        print("📥 Downloading auto-fixer files...")
        
        # Create directory structure
        (temp_path / "test_generation" / "execution").mkdir(parents=True)
        
        # Download files
        files_to_download = [
            ("https://raw.githubusercontent.com/codity-ai/codity.ai/feat/auto-testing/test_generation/execution/github_auto_fix.py", "github_auto_fix.py"),
            ("https://raw.githubusercontent.com/codity-ai/codity.ai/feat/auto-testing/test_generation/execution/test_auto_fixer.py", "test_generation/execution/test_auto_fixer.py"),
            ("https://raw.githubusercontent.com/codity-ai/codity.ai/feat/auto-testing/test_generation/__init__.py", "test_generation/__init__.py"),
            ("https://raw.githubusercontent.com/codity-ai/codity.ai/feat/auto-testing/test_generation/execution/__init__.py", "test_generation/execution/__init__.py"),
        ]
        
        for url, local_file in files_to_download:
            local_path = temp_path / local_file
            if not download_file(url, str(local_path)):
                print(f"❌ Failed to download {local_file}")
                # Create minimal fallback files
                if local_file.endswith("__init__.py"):
                    local_path.write_text("")
                elif local_file == "github_auto_fix.py":
                    # Create a minimal auto-fix script
                    local_path.write_text("""
import sys
from test_generation.execution.test_auto_fixer import TestAutoFixer
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 github_auto_fix.py <test_file1> [test_file2] ...")
        sys.exit(1)
    
    test_files = sys.argv[1:]
    auto_fixer = TestAutoFixer(max_retries=1)
    
    for test_file in test_files:
        print(f"🔧 Processing {test_file}...")
        test_code = Path(test_file).read_text()
        success, fixed_code, history = auto_fixer.auto_fix_test(
            test_code=test_code,
            test_file_path=test_file,
            language='python'
        )
        Path(test_file).write_text(fixed_code)
        print(f"✅ Updated {test_file}")

if __name__ == "__main__":
    main()
""")
                else:
                    print(f"⚠️ Using fallback for {local_file}")
        
        # Change to temp directory and run auto-fix
        os.chdir(temp_path)
        
        # Run the auto-fix script
        cmd = ["python3", "github_auto_fix.py"] + test_files
        print(f"🚀 Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True)
            print("✅ Auto-fix completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Auto-fix failed with exit code {e.returncode}")
            sys.exit(e.returncode)

if __name__ == "__main__":
    main()