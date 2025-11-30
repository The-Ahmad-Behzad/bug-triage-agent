"""Comprehensive tests for all completed phases"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.input_models import HandshakeMessage, BugInput, TeamProfile
from src.models.output_models import HandshakeResponse, TriageResult
from src.utils.validators import validate_input, validate_output
from src.utils.language_detector import detect_language_from_path, detect_file_type_from_path
from src.engines.classification import classify_bug
from src.engines.priority import assess_priority
from src.engines.assignment import assign_bug
from src.engines.fix_suggestion import suggest_fix
from src.handlers.triage_handler import process_triage_request


class TestPhase2Schemas:
    """Test Phase 2: Input/Output Schema and Validation"""
    
    def test_input_schema_validation(self):
        """Test input schema validation"""
        valid_input = {
            "message_id": "test-001",
            "sender": "supervisor",
            "recipient": "bug_triage_agent",
            "type": "task_assignment",
            "timestamp": "2025-01-01T12:00:00Z",
            "task": {
                "bugs": [{
                    "bug_id": "BUG-001",
                    "title": "Test",
                    "description": "Test description"
                }],
                "team_profiles": [{
                    "member_id": "dev-01",
                    "name": "Developer"
                }]
            }
        }
        
        is_valid, error = validate_input(valid_input)
        assert is_valid is True
        assert error == ""
    
    def test_language_detection(self):
        """Test language detection"""
        assert detect_language_from_path("test.py") == "python"
        assert detect_language_from_path("Main.java") == "java"
        assert detect_language_from_path("app.js") == "javascript"
        assert detect_file_type_from_path("test.py") == ".py"
        assert detect_file_type_from_path("Main.java") == ".java"


class TestPhase4Classification:
    """Test Phase 4: Bug Classification Engine"""
    
    def test_classify_runtime_error(self):
        """Test classification of runtime error"""
        bug = {
            "bug_id": "BUG-001",
            "title": "NullPointerException",
            "description": "App crashes with NullPointerException",
            "stack_trace": "java.lang.NullPointerException at line 42"
        }
        
        result = classify_bug(bug)
        assert result["category"] == "Runtime Error"
        assert result["confidence"] > 0.0
    
    def test_classify_security(self):
        """Test classification of security issue"""
        bug = {
            "bug_id": "BUG-002",
            "title": "SQL Injection",
            "description": "SQL injection vulnerability detected"
        }
        
        result = classify_bug(bug)
        assert result["category"] == "Security"


class TestPhase5Priority:
    """Test Phase 5: Priority Assessment Engine"""
    
    def test_priority_assessment(self):
        """Test priority assessment"""
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
        assert result["level"] in ["critical", "high", "medium", "low"]
        assert "justification" in result
        assert result["confidence"] > 0.0


class TestPhase6Assignment:
    """Test Phase 6: Team Member Assignment Engine"""
    
    def test_assignment_by_language(self):
        """Test assignment by language"""
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
        
        result = assign_bug(bug, team_profiles)
        assert result["assigned_to_member_id"] == "dev-01"
        assert result["confidence"] > 0.0


class TestPhase7FixSuggestion:
    """Test Phase 7: Fix Suggestion Engine"""
    
    def test_fix_suggestion(self):
        """Test fix suggestion"""
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
        assert "approach" in result
        assert "estimated_effort" in result
        assert len(result["approach"]) > 0


class TestPhase8Orchestration:
    """Test Phase 8: Main Agent Endpoint and Orchestration"""
    
    def test_full_workflow(self):
        """Test full workflow"""
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
        assert response["status"] == "completed"
        assert "results" in response
    
    def test_robust_handling_missing_optional_fields(self):
        """Test robust handling of missing optional fields"""
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
        # Should still work
        assert response["status"] == "completed"
        # Should have warnings
        if "warnings" in response:
            assert len(response["warnings"]) > 0



