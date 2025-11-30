"""Test runner script for all phases"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_phase_2_schemas():
    """Test Phase 2: Input/Output Schema and Validation"""
    print("\n=== Testing Phase 2: Input/Output Schema and Validation ===")
    
    try:
        from src.utils.language_detector import detect_language_from_path, detect_file_type_from_path
        
        # Test language detection
        assert detect_language_from_path("test.py") == "python", "Python detection failed"
        assert detect_language_from_path("Main.java") == "java", "Java detection failed"
        assert detect_language_from_path("app.js") == "javascript", "JavaScript detection failed"
        assert detect_file_type_from_path("test.py") == ".py", "File type detection failed"
        
        print("✅ Language detection: PASSED")
        return True
    except Exception as e:
        print(f"❌ Language detection: FAILED - {e}")
        return False


def test_phase_4_classification():
    """Test Phase 4: Bug Classification Engine"""
    print("\n=== Testing Phase 4: Bug Classification Engine ===")
    
    try:
        from src.engines.classification import classify_bug
        
        # Test runtime error classification
        bug = {
            "bug_id": "BUG-001",
            "title": "NullPointerException",
            "description": "App crashes with NullPointerException",
            "stack_trace": "java.lang.NullPointerException at line 42"
        }
        
        result = classify_bug(bug)
        assert result["category"] == "Runtime Error", "Category classification failed"
        assert result["confidence"] > 0.0, "Confidence should be > 0"
        
        print("✅ Classification: PASSED")
        return True
    except Exception as e:
        print(f"❌ Classification: FAILED - {e}")
        return False


def test_phase_5_priority():
    """Test Phase 5: Priority Assessment Engine"""
    print("\n=== Testing Phase 5: Priority Assessment Engine ===")
    
    try:
        from src.engines.priority import assess_priority
        
        bug = {
            "metadata": {
                "environment": "production",
                "tags": ["crash"]
            }
        }
        classification = {
            "category": "Runtime Error",
            "type": "NullPointerException"
        }
        
        result = assess_priority(bug, classification)
        assert result["level"] in ["critical", "high", "medium", "low"], "Invalid priority level"
        assert "justification" in result, "Missing justification"
        
        print("✅ Priority assessment: PASSED")
        return True
    except Exception as e:
        print(f"❌ Priority assessment: FAILED - {e}")
        return False


def test_phase_6_assignment():
    """Test Phase 6: Team Member Assignment Engine"""
    print("\n=== Testing Phase 6: Team Member Assignment Engine ===")
    
    try:
        from src.engines.assignment import assign_bug
        
        bug = {
            "bug_id": "BUG-001",
            "title": "Python bug",
            "description": "Python code issue",
            "language": "python"
        }
        team_profiles = [
            {
                "member_id": "dev-01",
                "name": "Python Dev",
                "skills": {
                    "languages": ["python"]
                },
                "current_load": 1
            },
            {
                "member_id": "dev-02",
                "name": "Java Dev",
                "skills": {
                    "languages": ["java"]
                },
                "current_load": 1
            }
        ]
        
        result = assign_bug(bug, team_profiles, db_available=False)
        assert "assigned_to_member_id" in result, "Missing assignment"
        assert result["confidence"] > 0.0, "Confidence should be > 0"
        
        print("✅ Assignment: PASSED")
        return True
    except Exception as e:
        print(f"❌ Assignment: FAILED - {e}")
        return False


def test_phase_7_fix_suggestion():
    """Test Phase 7: Fix Suggestion Engine"""
    print("\n=== Testing Phase 7: Fix Suggestion Engine ===")
    
    try:
        from src.engines.fix_suggestion import suggest_fix
        
        bug = {
            "bug_id": "BUG-001",
            "title": "NullPointerException",
            "description": "Null pointer error"
        }
        classification = {
            "category": "Runtime Error",
            "type": "NullPointerException",
            "root_cause": "Missing null check"
        }
        
        result = suggest_fix(bug, classification)
        assert "approach" in result, "Missing fix approach"
        assert "estimated_effort" in result, "Missing effort estimate"
        
        print("✅ Fix suggestion: PASSED")
        return True
    except Exception as e:
        print(f"❌ Fix suggestion: FAILED - {e}")
        return False


def test_phase_8_orchestration():
    """Test Phase 8: Main Agent Endpoint and Orchestration"""
    print("\n=== Testing Phase 8: Main Agent Endpoint and Orchestration ===")
    
    try:
        from src.handlers.triage_handler import process_triage_request
        
        # Test with complete input
        request = {
            "message_id": "test-001",
            "sender": "supervisor",
            "recipient": "bug_triage_agent",
            "type": "task_assignment",
            "timestamp": "2025-01-01T12:00:00Z",
            "task": {
                "bugs": [{
                    "bug_id": "BUG-001",
                    "title": "Test bug",
                    "description": "Test description"
                }],
                "team_profiles": [{
                    "member_id": "dev-01",
                    "name": "Developer",
                    "skills": ["python"]
                }]
            }
        }
        
        response = process_triage_request(request)
        assert response["status"] == "completed", "Status should be completed"
        assert "results" in response, "Missing results"
        
        print("✅ Orchestration: PASSED")
        return True
    except Exception as e:
        print(f"❌ Orchestration: FAILED - {e}")
        return False


def test_robust_handling():
    """Test robust handling of missing optional fields"""
    print("\n=== Testing Robust Handling of Missing Optional Fields ===")
    
    try:
        from src.handlers.triage_handler import process_triage_request
        
        # Test with minimal input (missing optional fields)
        request = {
            "message_id": "test-002",
            "sender": "supervisor",
            "recipient": "bug_triage_agent",
            "type": "task_assignment",
            "timestamp": "2025-01-01T12:00:00Z",
            "task": {
                "bugs": [{
                    "bug_id": "BUG-002",
                    "title": "Minimal bug",
                    "description": "Minimal description"
                    # Missing: steps_to_reproduce, stack_trace, logs, code_context
                }],
                "team_profiles": [{
                    "member_id": "dev-01",
                    "name": "Developer",
                    "skills": ["python"]
                }]
            }
        }
        
        response = process_triage_request(request)
        assert response["status"] == "completed", "Should still work with missing optional fields"
        
        # Should have warnings
        if "warnings" in response:
            print(f"✅ Warnings generated: {len(response['warnings'])} warnings")
        
        print("✅ Robust handling: PASSED")
        return True
    except Exception as e:
        print(f"❌ Robust handling: FAILED - {e}")
        return False


def test_error_handling():
    """Test error handling for missing required fields"""
    print("\n=== Testing Error Handling for Missing Required Fields ===")
    
    try:
        from src.handlers.triage_handler import process_triage_request
        
        # Test with missing required fields
        request = {
            "message_id": "test-003",
            "sender": "supervisor",
            "recipient": "bug_triage_agent",
            "type": "task_assignment",
            "timestamp": "2025-01-01T12:00:00Z",
            "task": {
                "bugs": [{
                    "bug_id": "BUG-003"
                    # Missing: title and description (required)
                }],
                "team_profiles": [{
                    "member_id": "dev-01",
                    "name": "Developer"
                }]
            }
        }
        
        response = process_triage_request(request)
        assert response["status"] == "failed", "Should fail with missing required fields"
        assert "error" in response, "Should have error message"
        
        print("✅ Error handling: PASSED")
        return True
    except Exception as e:
        print(f"❌ Error handling: FAILED - {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Bug Triage AI Agent - Comprehensive Test Suite")
    print("=" * 60)
    
    results = {
        "test_date": datetime.now().isoformat(),
        "phases_tested": [],
        "total_tests": 0,
        "passed": 0,
        "failed": 0
    }
    
    tests = [
        ("Phase 2: Schemas", test_phase_2_schemas),
        ("Phase 4: Classification", test_phase_4_classification),
        ("Phase 5: Priority", test_phase_5_priority),
        ("Phase 6: Assignment", test_phase_6_assignment),
        ("Phase 7: Fix Suggestion", test_phase_7_fix_suggestion),
        ("Phase 8: Orchestration", test_phase_8_orchestration),
        ("Robust Handling", test_robust_handling),
        ("Error Handling", test_error_handling),
    ]
    
    for test_name, test_func in tests:
        results["total_tests"] += 1
        try:
            if test_func():
                results["passed"] += 1
                results["phases_tested"].append({"phase": test_name, "status": "PASSED"})
            else:
                results["failed"] += 1
                results["phases_tested"].append({"phase": test_name, "status": "FAILED"})
        except Exception as e:
            results["failed"] += 1
            results["phases_tested"].append({"phase": test_name, "status": "FAILED", "error": str(e)})
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total_tests']*100):.1f}%")
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to test_results.json")
    
    return results


if __name__ == "__main__":
    main()



