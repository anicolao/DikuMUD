#!/usr/bin/env python3
"""Process integration test results and move failed tests to failures directory."""

import sys
import os
import glob
import shutil

def main():
    outputs = sorted(glob.glob("integration_test_outputs/**/*.out", recursive=True))
    total = len(outputs)
    
    if total == 0:
        print("No test outputs found")
        sys.exit(0)
    
    passed = sum(1 for f in outputs if open(f).readlines()[-1].strip() == "PASSED")
    failed = total - passed
    
    print(f"Total:  {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("")
    
    failed_files = [f for f in outputs if open(f).readlines()[-1].strip() == "FAILED"]
    
    if failed == 0:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"❌ {failed} test(s) failed")
        print("")
        print("Failed tests:")
        for f in failed_files:
            print(f"  - {f}")
        print("")
        print("Moving failed test outputs to integration_test_failures/...")
        
        # Create failures directory structure
        os.makedirs("integration_test_failures", exist_ok=True)
        for subdir in ["shops", "items", "quests", "zones"]:
            os.makedirs(f"integration_test_failures/{subdir}", exist_ok=True)
        
        # Move failed test outputs
        for failed_file in failed_files:
            dest = failed_file.replace("integration_test_outputs/", "integration_test_failures/")
            shutil.move(failed_file, dest)
            print(f"  Moved: {failed_file} -> {dest}")
        
        print("")
        print("Run 'make all' again to retry only the failed tests.")
        sys.exit(1)

if __name__ == "__main__":
    main()
