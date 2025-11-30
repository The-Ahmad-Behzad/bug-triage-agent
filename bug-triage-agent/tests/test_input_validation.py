"""Tests for input validation"""

import pytest
from src.utils.validators import validate_input, validate_bug_object, validate_team_profiles
from src.models.input_models import HandshakeMessage


def test_validate_input_valid():
    """Test validation of valid input"""
    valid_input = {
        "message_id": "test-001",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-001",
                    "title": "Test bug",
                    "description": "Test description",
                    "code_context": {
                        "file_path": "src/test.py"
                    }
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Test Developer"
                }
            ]
        }
    }
    
    is_valid, error = validate_input(valid_input)
    assert is_valid is True
    assert error == ""


def test_validate_input_invalid_sender():
    """Test validation fails with invalid sender"""
    invalid_input = {
        "message_id": "test-001",
        "sender": "invalid_sender",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [],
            "team_profiles": []
        }
    }
    
    is_valid, error = validate_input(invalid_input)
    assert is_valid is False
    assert "sender" in error.lower()


def test_validate_bug_object_valid():
    """Test validation of valid bug object"""
    valid_bug = {
        "bug_id": "BUG-001",
        "title": "Test bug",
        "description": "Test description"
    }
    
    is_valid, error = validate_bug_object(valid_bug)
    assert is_valid is True
    assert error == ""


def test_validate_bug_object_missing_required():
    """Test validation fails with missing required fields"""
    invalid_bug = {
        "bug_id": "BUG-001"
        # Missing title and description
    }
    
    is_valid, error = validate_bug_object(invalid_bug)
    assert is_valid is False
    assert "required" in error.lower() or "title" in error.lower() or "description" in error.lower()


def test_validate_team_profiles_valid():
    """Test validation of valid team profiles"""
    valid_profiles = [
        {
            "member_id": "dev-01",
            "name": "Test Developer"
        }
    ]
    
    is_valid, error = validate_team_profiles(valid_profiles)
    assert is_valid is True
    assert error == ""


def test_validate_team_profiles_empty():
    """Test validation fails with empty team profiles"""
    is_valid, error = validate_team_profiles([])
    assert is_valid is False
    assert "empty" in error.lower()



