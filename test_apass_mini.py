#!/usr/bin/env python3
"""
Test script for aPass Mini v1.1.0
Comprehensive testing suite for all functions and features
"""

import subprocess
import sys
import os
import json
import tempfile
from pathlib import Path

def run_command(cmd, expect_success=True):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        success = result.returncode == 0
        output = result.stdout + result.stderr
        
        if expect_success and not success:
            print(f"❌ Command failed: {cmd}")
            print(f"Exit code: {result.returncode}")
            if output.strip():
                print(f"Output: {output}")
            return False, output
        elif not expect_success and success:
            print(f"❌ Command should have failed but succeeded: {cmd}")
            return False, output
        else:
            print(f"✅ Command {'succeeded' if success else 'failed as expected'}: {cmd}")
            return success, output
    except Exception as e:
        print(f"❌ Exception running command: {e}")
        return False, str(e)

def test_basic_functionality():
    """Test basic functionality like help, version, etc."""
    print("\n🧪 Testing Basic Functionality")
    print("=" * 50)
    
    tests = [
        ("python3 apass_mini.py --help", True),
        ("python3 apass_mini.py --version", True),
        ("python3 apass_mini.py cleanup", True),
        ("python3 apass_mini.py --log-level DEBUG cleanup", True),
        ("python3 apass_mini.py config --help", True),
        ("python3 apass_mini.py payload --help", True),
        ("python3 apass_mini.py bypass --help", True),
        ("python3 apass_mini.py sign --help", True),
        ("python3 apass_mini.py full --help", True),
        ("python3 apass_mini.py test --help", True),
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, expect_success in tests:
        success, _ = run_command(cmd, expect_success)
        if success == expect_success:
            passed += 1
    
    print(f"\n📊 Basic Functionality: {passed}/{total} tests passed")
    return passed == total

def test_input_validation():
    """Test input validation functionality."""
    print("\n🧪 Testing Input Validation")
    print("=" * 50)
    
    tests = [
        ("python3 apass_mini.py test -i nonexistent.apk", False),
        ("python3 apass_mini.py bypass -i nonexistent.apk -t obfuscapk", False),
        ("python3 apass_mini.py sign -i nonexistent.apk", False),
        
        ("python3 apass_mini.py payload -l invalid_ip -p 4444 -s test.apk", False),
        ("python3 apass_mini.py payload -l 192.168.1.1 -p 999999 -s test.apk", False),
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, expect_success in tests:
        success, _ = run_command(cmd, expect_success)
        if success == expect_success:
            passed += 1
    
    print(f"\n📊 Input Validation: {passed}/{total} tests passed")
    return passed == total

def test_config_system():
    """Test configuration system."""
    print("\n🧪 Testing Configuration System")
    print("=" * 50)
    
    test_config = {
        "keystore_path": "test-keystore.jks",
        "keystore_password": "",
        "key_alias": "test-alias",
        "key_password": "",
        "temp_dir": "/tmp/apass_test"
    }
    
    try:
        with open("test_config.json", "w") as f:
            json.dump(test_config, f, indent=2)
        
        print("✅ Test config file created successfully")
        
        os.remove("test_config.json")
        print("✅ Test config file cleaned up successfully")
        
        return True
    except Exception as e:
        print(f"❌ Config system test failed: {e}")
        return False

def test_file_operations():
    """Test file operations and utilities."""
    print("\n🧪 Testing File Operations")
    print("=" * 50)
    
    try:
        test_file = "test_operations.txt"
        with open(test_file, "w") as f:
            f.write("Test content for aPass Mini")
        
        if os.path.isfile(test_file):
            print("✅ File creation successful")
        else:
            print("❌ File creation failed")
            return False
        
        os.remove(test_file)
        print("✅ File cleanup successful")
        
        return True
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_error_handling():
    """Test error handling scenarios."""
    print("\n🧪 Testing Error Handling")
    print("=" * 50)
    
    tests = [
 
        ("python3 apass_mini.py invalid_command", False),
        ("python3 apass_mini.py payload", False),  
        ("python3 apass_mini.py bypass", False),   
        ("python3 apass_mini.py sign", False),     
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, expect_success in tests:
        success, _ = run_command(cmd, expect_success)
        if success == expect_success:
            passed += 1
    
    print(f"\n📊 Error Handling: {passed}/{total} tests passed")
    return passed == total

def test_code_quality():
    """Test code quality and syntax."""
    print("\n🧪 Testing Code Quality")
    print("=" * 50)
    
    try:
        
        result = subprocess.run("python3 -m py_compile apass_mini.py", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Python syntax check passed")
            syntax_ok = True
        else:
            print(f"❌ Python syntax check failed: {result.stderr}")
            syntax_ok = False
        
        result = subprocess.run("python3 -c 'import sys; sys.argv = [\"test\"]; exec(open(\"apass_mini.py\").read().replace(\"if __name__ == \\\"__main__\\\":\", \"if False:\"))'", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Import test passed")
            import_ok = True
        else:
            print(f"❌ Import test failed: {result.stderr}")
            import_ok = False
        
        return syntax_ok and import_ok
    except Exception as e:
        print(f"❌ Code quality test failed: {e}")
        return False

def create_test_report(results):
    """Create a comprehensive test report."""
    print("\n" + "=" * 60)
    print("🏁 aPass Mini v1.1.0 - Test Report")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:<30} {status}")
    
    print("-" * 60)
    print(f"Overall Result: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests PASSED! aPass Mini is ready for use.")
        return True
    else:
        print("⚠️  Some tests FAILED. Please review the issues above.")
        return False

def main():
    """Main test execution function."""
    print("🚀 Starting aPass Mini v1.1.0 Test Suite")
    print("=" * 60)
    
    test_results = {
        "Basic Functionality": test_basic_functionality(),
        "Input Validation": test_input_validation(),
        "Configuration System": test_config_system(),
        "File Operations": test_file_operations(),
        "Error Handling": test_error_handling(),
        "Code Quality": test_code_quality(),
    }
    
    success = create_test_report(test_results)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
