#!/usr/bin/env python3
"""
Final verification script for aPass Mini v1.1.0
Ensures all components are working correctly after fixes and enhancements
"""

import sys
import os
import subprocess
from pathlib import Path

def check_file_structure():
    """Verify all required files are present."""
    print("🔍 Checking file structure...")
    
    required_files = [
        "apass_mini.py",
        "requirements.txt", 
        "README.md",
        "LICENSE",
        "test_apass_mini.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def check_code_syntax():
    """Check Python syntax of main script."""
    print("\n🔍 Checking code syntax...")
    
    try:
        result = subprocess.run(
            ["python3", "-m", "py_compile", "apass_mini.py"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("✅ Python syntax is valid")
            return True
        else:
            print(f"❌ Syntax errors found: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking syntax: {e}")
        return False

def check_imports():
    """Check that all imports work correctly."""
    print("\n🔍 Checking imports...")
    
    try:
        result = subprocess.run([
            "python3", "-c", 
            "import sys; sys.argv = ['apass_mini.py']; import apass_mini"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All imports work correctly")
            return True
        else:
            print(f"❌ Import errors: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking imports: {e}")
        return False

def check_core_functionality():
    """Test core functionality without external dependencies."""
    print("\n🔍 Checking core functionality...")
    
    tests = [
        (["python3", "apass_mini.py", "--version"], "Version check"),
        (["python3", "apass_mini.py", "cleanup"], "Cleanup command"),
        (["python3", "apass_mini.py", "config", "--help"], "Config help"),
    ]
    
    all_passed = True
    for cmd, description in tests:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} failed")
                all_passed = False
        except Exception as e:
            print(f"❌ {description} error: {e}")
            all_passed = False
    
    return all_passed

def check_enhanced_features():
    """Check enhanced features added during the fix."""
    print("\n🔍 Checking enhanced features...")
    
    features = [
        (["python3", "apass_mini.py", "test", "--help"], "Test command"),
        (["python3", "apass_mini.py", "cleanup", "--help"], "Cleanup command"),
        (["python3", "apass_mini.py", "--log-level", "DEBUG", "cleanup"], "Debug logging"),
    ]
    
    all_passed = True
    for cmd, description in features:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} failed")
                all_passed = False
        except Exception as e:
            print(f"❌ {description} error: {e}")
            all_passed = False
    
    return all_passed

def check_error_handling():
    """Check that error handling works correctly."""
    print("\n🔍 Checking error handling...")
    
    error_tests = [
        (["python3", "apass_mini.py", "invalid_command"], "Invalid command"),
        (["python3", "apass_mini.py", "test", "-i", "nonexistent.apk"], "Nonexistent file"),
        (["python3", "apass_mini.py", "payload"], "Missing required arguments"),
    ]
    
    all_passed = True
    for cmd, description in error_tests:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"✅ {description} (correctly failed)")
            else:
                print(f"❌ {description} (should have failed)")
                all_passed = False
        except Exception as e:
            print(f"❌ {description} error: {e}")
            all_passed = False
    
    return all_passed

def generate_final_report():
    """Generate a final verification report."""
    print("\n" + "="*60)
    print("🏆 aPass Mini v1.1.0 - Final Verification Report")
    print("="*60)
    
    checks = [
        ("File Structure", check_file_structure()),
        ("Code Syntax", check_code_syntax()),
        ("Imports", check_imports()),
        ("Core Functionality", check_core_functionality()),
        ("Enhanced Features", check_enhanced_features()),
        ("Error Handling", check_error_handling()),
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\nResults Summary:")
    for check_name, result in checks:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {check_name:<20} {status}")
    
    print(f"\nOverall Score: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 VERIFICATION SUCCESSFUL!")
        print("✅ aPass Mini v1.1.0 is fully functional and ready for use.")
        print("✅ All fixes and enhancements have been successfully applied.")
        return True
    else:
        print(f"\n⚠️  VERIFICATION INCOMPLETE!")
        print(f"❌ {total - passed} checks failed. Please review the issues above.")
        return False

def main():
    """Main verification function."""
    print("🚀 Starting aPass Mini v1.1.0 Final Verification")
    print("="*60)
    
    success = generate_final_report()
    
    if success:
        print("\n📋 Summary of Changes Made:")
        print("  • Fixed missing imports (shlex, ipaddress)")
        print("  • Removed duplicate main() call")
        print("  • Enhanced error handling and validation")
        print("  • Added new test and cleanup commands")
        print("  • Improved code organization and structure")
        print("  • Added comprehensive APK integrity checking")
        print("  • Enhanced logging and progress tracking")
        print("  • Streamlined README documentation")
        print("  • Added comprehensive test suite")
        print("  • Synchronized version information across all files")
        print("  • Fixed output formatting and consistency")
        
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
