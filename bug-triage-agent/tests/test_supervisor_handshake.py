"""Tests for Supervisor handshake format compatibility and envelope metadata."""

import pytest
from datetime import datetime, UTC
from src.handlers.triage_handler import process_triage_request


def test_handshake_envelope_structure():
    """Test that response follows Supervisor handshake format."""
    request = {
        "message_id": "test-msg-001",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": datetime.now(UTC).isoformat(),
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-001",
                    "title": "Test bug",
                    "description": "A test bug for handshake validation",
                    "code_context": {
                        "file_path": "test.py",
                        "line_start": 1,
                        "line_end": 10,
                        "snippet": "print('test')"
                    },
                    "language": "python",
                    "file_type": ".py"
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Test Developer",
                    "skills": {
                        "languages": ["python"],
                        "frameworks": [],
                        "domains": []
                    },
                    "current_load": 0
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    # Verify envelope structure
    assert "message_id" in response
    assert "sender" in response
    assert "recipient" in response
    assert "type" in response
    assert "related_message_id" in response
    assert "status" in response
    assert "timestamp" in response
    
    # Verify envelope values
    assert response["sender"] == "bug_triage_agent"
    assert response["recipient"] == "supervisor"
    assert response["type"] == "task_response"
    assert response["related_message_id"] == "test-msg-001"
    assert response["status"] in ["completed", "failed"]
    
    # Verify results structure if completed
    if response["status"] == "completed":
        assert "results" in response
        assert "triage" in response["results"]
        assert isinstance(response["results"]["triage"], list)
        assert len(response["results"]["triage"]) == 1


def test_handshake_with_warnings():
    """Test that warnings are properly included in response envelope."""
    request = {
        "message_id": "test-msg-002",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": datetime.now(UTC).isoformat(),
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-002",
                    "title": "Minimal bug",
                    "description": "Bug with missing optional fields"
                    # Intentionally missing: steps_to_reproduce, stack_trace, logs, code_context
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Test Developer",
                    "skills": {
                        "languages": ["python"],
                        "frameworks": [],
                        "domains": []
                    },
                    "current_load": 0
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    # Should still complete successfully
    assert response["status"] == "completed"
    
    # Should include warnings array if warnings were generated
    # (Warnings are only added if optional fields are missing)
    if "warnings" in response:
        assert isinstance(response["warnings"], list)
        if len(response["warnings"]) > 0:
            # Verify warning messages mention missing fields
            warning_text = " ".join(response["warnings"])
            assert "missing" in warning_text.lower() or "optional" in warning_text.lower()


def test_handshake_error_response():
    """Test error response format for invalid input."""
    invalid_request = {
        "message_id": "test-msg-003",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": datetime.now(UTC).isoformat(),
        # Missing required "task" field
    }
    
    response = process_triage_request(invalid_request)
    
    # Should return error response
    assert response["status"] == "failed"
    assert "error" in response
    
    # Should still have proper envelope
    assert response["sender"] == "bug_triage_agent"
    assert response["recipient"] == "supervisor"
    assert response["type"] == "task_response"
    assert response["related_message_id"] == "test-msg-003"


def test_handshake_batch_processing():
    """Test handshake format with multiple bugs."""
    request = {
        "message_id": "test-msg-004",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": datetime.now(UTC).isoformat(),
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-003",
                    "title": "Bug 1",
                    "description": "First bug",
                    "code_context": {
                        "file_path": "test1.py",
                        "line_start": 1,
                        "line_end": 5,
                        "snippet": "code1"
                    },
                    "language": "python",
                    "file_type": ".py"
                },
                {
                    "bug_id": "BUG-004",
                    "title": "Bug 2",
                    "description": "Second bug",
                    "code_context": {
                        "file_path": "test2.js",
                        "line_start": 1,
                        "line_end": 5,
                        "snippet": "code2"
                    },
                    "language": "javascript",
                    "file_type": ".js"
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Python Dev",
                    "skills": {
                        "languages": ["python"],
                        "frameworks": [],
                        "domains": []
                    },
                    "current_load": 0
                },
                {
                    "member_id": "dev-02",
                    "name": "JS Dev",
                    "skills": {
                        "languages": ["javascript"],
                        "frameworks": [],
                        "domains": []
                    },
                    "current_load": 0
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    assert response["status"] == "completed"
    assert len(response["results"]["triage"]) == 2
    
    # Verify each result has proper structure
    for result in response["results"]["triage"]:
        assert "bug_id" in result
        assert "classification" in result
        assert "priority" in result
        assert "assignment" in result
        assert "suggested_fix" in result
        assert "confidence_scores" in result


def test_handshake_related_message_id_preservation():
    """Test that related_message_id correctly references original message."""
    original_message_id = "supervisor-msg-abc123"
    
    request = {
        "message_id": original_message_id,
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": datetime.now(UTC).isoformat(),
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-005",
                    "title": "Test bug",
                    "description": "Testing message ID preservation",
                    "code_context": {
                        "file_path": "test.py",
                        "line_start": 1,
                        "line_end": 10,
                        "snippet": "test code"
                    },
                    "language": "python",
                    "file_type": ".py"
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Test Dev",
                    "skills": {
                        "languages": ["python"],
                        "frameworks": [],
                        "domains": []
                    },
                    "current_load": 0
                }
            ]
        }
    }
    
    response = process_triage_request(request)
    
    # Verify related_message_id matches original
    assert response["related_message_id"] == original_message_id
    
    # Verify response has its own unique message_id
    assert response["message_id"] != original_message_id
    assert response["message_id"] is not None

