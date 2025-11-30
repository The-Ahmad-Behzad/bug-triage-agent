"""Integration tests for bug triage agent"""

import pytest
import json
from src.handlers.triage_handler import process_triage_request


def test_full_triage_workflow_complete_input():
    """Test full triage workflow with complete input"""
    request = {
        "message_id": "test-001",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-001",
                    "title": "NullPointerException in AuthService",
                    "description": "The app throws a NullPointerException after entering credentials.",
                    "steps_to_reproduce": [
                        "Open app",
                        "Enter username and password",
                        "Click Login"
                    ],
                    "stack_trace": "java.lang.NullPointerException at AuthService.java:42",
                    "logs": "2025-01-01 10:02:15 ERROR AuthService failed to load user",
                    "code_context": {
                        "file_path": "src/auth/AuthService.java",
                        "line_start": 30,
                        "line_end": 60,
                        "snippet": "User user = db.findUser(email);\nreturn user.getName();"
                    },
                    "language": "java",
                    "file_type": ".java",
                    "metadata": {
                        "reported_by": "ahmad",
                        "environment": "production",
                        "tags": ["crash", "auth", "nullpointer"]
                    }
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Hassan Raza",
                    "skills": {
                        "languages": ["java", "python"],
                        "frameworks": ["spring", "django"],
                        "domains": ["backend", "authentication"]
                    },
                    "modules_owned": ["auth", "session-management"],
                    "current_load": 2
                },
                {
                    "member_id": "dev-02",
                    "name": "Sara Ahmed",
                    "skills": {
                        "languages": ["javascript", "typescript"],
                        "frameworks": ["react", "vue"],
                        "domains": ["frontend", "ui"]
                    },
                    "modules_owned": ["ui", "dashboard"],
                    "current_load": 1
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    assert response["status"] == "completed"
    assert "results" in response
    assert "triage" in response["results"]
    assert len(response["results"]["triage"]) == 1
    
    triage_result = response["results"]["triage"][0]
    assert triage_result["bug_id"] == "BUG-001"
    assert "classification" in triage_result
    assert "priority" in triage_result
    assert "assignment" in triage_result
    assert "suggested_fix" in triage_result
    assert "confidence_scores" in triage_result


def test_triage_with_minimal_input():
    """Test triage with minimal required fields only"""
    request = {
        "message_id": "test-002",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-002",
                    "title": "App crashes",
                    "description": "The application crashes when clicking the login button"
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Hassan Raza",
                    "skills": ["java", "backend"]
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    # Should still work but with warnings
    assert response["status"] == "completed"
    assert "results" in response
    assert "triage" in response["results"]
    assert len(response["results"]["triage"]) == 1
    
    # Should have warnings about missing fields
    if "warnings" in response:
        assert len(response["warnings"]) > 0


def test_triage_with_auto_detected_language():
    """Test triage with auto-detected language from file path"""
    request = {
        "message_id": "test-003",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-003",
                    "title": "TypeError in Python code",
                    "description": "TypeError when processing data",
                    "code_context": {
                        "file_path": "src/processor.py",
                        "snippet": "def process(data): return data.upper()"
                    }
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Python Developer",
                    "skills": {
                        "languages": ["python"]
                    }
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    assert response["status"] == "completed"
    triage_result = response["results"]["triage"][0]
    assert triage_result["bug_id"] == "BUG-003"


def test_triage_batch_processing():
    """Test batch processing of multiple bugs"""
    request = {
        "message_id": "test-004",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-004A",
                    "title": "Security vulnerability",
                    "description": "SQL injection possible"
                },
                {
                    "bug_id": "BUG-004B",
                    "title": "Performance issue",
                    "description": "Slow response time"
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Developer",
                    "skills": ["java", "python"]
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    assert response["status"] == "completed"
    assert len(response["results"]["triage"]) == 2
    assert response["results"]["triage"][0]["bug_id"] == "BUG-004A"
    assert response["results"]["triage"][1]["bug_id"] == "BUG-004B"


def test_triage_error_handling_missing_required():
    """Test error handling for missing required fields"""
    request = {
        "message_id": "test-005",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-005",
                    # Missing title and description - should fail
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Developer"
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    # Should return error response
    assert response["status"] == "failed"
    assert "error" in response


def test_triage_error_handling_empty_team_profiles():
    """Test error handling for empty team profiles"""
    request = {
        "message_id": "test-006",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-006",
                    "title": "Test bug",
                    "description": "Test description"
                }
            ],
            "team_profiles": []  # Empty - should fail
        }
    }
    
    response = process_triage_request(request)
    
    # Should return error response
    assert response["status"] == "failed"
    assert "error" in response



