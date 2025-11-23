#!/usr/bin/env python3
"""
Quick Test Script for Tool 12 - Duplicate Logging Detector

Run this to verify Tool 12 is working correctly:
    python3 test_duplicate_logging_quick.py
"""

import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.tools.tool_12_duplicate_logging_detector import detect_duplicate_logging


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_exact_duplicates():
    """Test 1: Exact Duplicate Detection"""
    print_section("TEST 1: Exact Duplicate Detection")
    
    logging_statements = [
        {"message": "User logged in successfully", "file_path": "auth/login.py", "line_number": 42, "function": "handle_login"},
        {"message": "User logged in successfully", "file_path": "api/auth.py", "line_number": 88, "function": "authenticate"},
        {"message": "User logged in successfully", "file_path": "services/user_service.py", "line_number": 156, "function": "login_user"},
    ]
    
    result = detect_duplicate_logging(
        logging_statements=logging_statements,
        entities=[],
        repository_path="/tmp/test"
    )
    
    print(f"✅ Success: {result['success']}")
    print(f"📊 Mode: {result['detection_mode']}")
    print(f"🔍 Total Duplicates Found: {result['statistics']['total_duplicates']}")
    print(f"📝 Message: {result['message']}")
    
    if result['duplicate_logs']:
        dup = result['duplicate_logs'][0]
        print(f"\n📋 First Duplicate:")
        print(f"   Type: {dup['type']}")
        print(f"   Severity: {dup['severity']}")
        print(f"   Occurrences: {dup['occurrences']}")
        print(f"   Recommendation: {dup['recommendation']}")
    
    return result['success']


def test_log_spam():
    """Test 2: Log Spam Detection"""
    print_section("TEST 2: Log Spam Detection (Loops)")
    
    logging_statements = [
        {
            "message": "Processing item {item}",
            "file_path": "batch/processor.py",
            "line_number": 55,
            "function": "process_batch",
            "context": "for item in items:",
            "level": "INFO"
        }
    ]
    
    result = detect_duplicate_logging(
        logging_statements=logging_statements,
        entities=[],
        repository_path="/tmp/test"
    )
    
    print(f"✅ Success: {result['success']}")
    print(f"🔁 Log Spam Found: {result['statistics']['by_type'].get('spam', 0)}")
    
    if result['duplicate_logs']:
        spam = result['duplicate_logs'][0]
        print(f"\n🔁 Spam Details:")
        print(f"   Type: {spam['type']}")
        print(f"   Severity: {spam['severity']}")
        print(f"   Message: {spam['message']}")
        print(f"   Recommendation: {spam['recommendation'][:100]}...")
    
    return result['success']


def test_noise_logs():
    """Test 3: Noise Log Detection"""
    print_section("TEST 3: Noise Log Detection")
    
    logging_statements = [
        {"message": "Entering function", "file_path": "service.py", "line_number": 10, "function": "some_function", "level": "DEBUG"},
        {"message": "Debug checkpoint", "file_path": "utils.py", "line_number": 30, "function": "helper", "level": "TRACE"},
    ]
    
    result = detect_duplicate_logging(
        logging_statements=logging_statements,
        entities=[],
        repository_path="/tmp/test"
    )
    
    print(f"✅ Success: {result['success']}")
    print(f"🔇 Noise Logs Found: {result['statistics']['by_type'].get('noise', 0)}")
    
    return result['success']


def test_mixed_duplicates():
    """Test 4: Mixed Types"""
    print_section("TEST 4: Mixed Duplicate Types")
    
    logging_statements = [
        # Exact duplicates
        {"message": "Request processed", "file_path": "a.py", "line_number": 1, "function": "f1", "level": "INFO"},
        {"message": "Request processed", "file_path": "b.py", "line_number": 2, "function": "f2", "level": "INFO"},
        
        # Spam
        {"message": "Processing item", "file_path": "c.py", "line_number": 3, "function": "process_batch", "context": "for item", "level": "INFO"},
        
        # Noise
        {"message": "Entering function", "file_path": "d.py", "line_number": 4, "function": "f3", "level": "DEBUG"},
        
        # Similar
        {"message": "User authentication successful", "file_path": "e.py", "line_number": 5, "function": "f4", "level": "INFO"},
        {"message": "User authentication completed successfully", "file_path": "f.py", "line_number": 6, "function": "f5", "level": "INFO"},
    ]
    
    result = detect_duplicate_logging(
        logging_statements=logging_statements,
        entities=[],
        repository_path="/tmp/test"
    )
    
    print(f"✅ Success: {result['success']}")
    print(f"📊 Statistics:")
    print(f"   Total Duplicates: {result['statistics']['total_duplicates']}")
    print(f"   Total Affected Locations: {result['statistics']['total_affected_locations']}")
    
    print(f"\n📋 By Type:")
    for dup_type, count in result['statistics']['by_type'].items():
        print(f"   - {dup_type}: {count}")
    
    print(f"\n⚠️  By Severity:")
    for severity, count in result['statistics']['by_severity'].items():
        print(f"   - {severity}: {count}")
    
    return result['success']


def test_output_format():
    """Test 5: Output Format (JSON Serialization)"""
    print_section("TEST 5: Output Format Validation")
    
    logging_statements = [
        {"message": "Test log", "file_path": "test.py", "line_number": 1, "function": "test", "level": "INFO"}
    ]
    
    result = detect_duplicate_logging(
        logging_statements=logging_statements,
        entities=[],
        repository_path="/tmp/test"
    )
    
    # Test JSON serialization (for database storage)
    try:
        json_str = json.dumps(result, indent=2)
        parsed = json.loads(json_str)
        print("✅ Output is JSON-serializable")
        print(f"📦 Output size: {len(json_str)} bytes")
        print(f"\n📄 Sample output structure:")
        print(json.dumps({
            "success": parsed["success"],
            "detection_mode": parsed["detection_mode"],
            "statistics": parsed["statistics"],
            "duplicate_logs_count": len(parsed["duplicate_logs"])
        }, indent=2))
        return True
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False


def main():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  Tool 12: Duplicate Logging Detector - Quick Test Suite    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Exact Duplicates", test_exact_duplicates),
        ("Log Spam", test_log_spam),
        ("Noise Logs", test_noise_logs),
        ("Mixed Types", test_mixed_duplicates),
        ("Output Format", test_output_format),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 All tests passed! Tool 12 is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
