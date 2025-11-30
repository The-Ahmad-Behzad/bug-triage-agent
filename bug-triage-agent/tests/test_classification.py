"""Tests for classification engine"""

import pytest
from src.engines.classification import (
    classify_bug,
    classify_category,
    classify_type,
    analyze_root_cause,
    calculate_classification_confidence
)


def test_classify_bug_runtime_error():
    """Test classification of runtime error"""
    bug = {
        "bug_id": "BUG-001",
        "title": "NullPointerException in AuthService",
        "description": "App crashes with NullPointerException",
        "stack_trace": "java.lang.NullPointerException at AuthService.java:42"
    }
    
    result = classify_bug(bug)
    assert result["category"] == "Runtime Error"
    assert "NullPointerException" in result["type"] or "null" in result["type"].lower()
    assert result["confidence"] > 0.0


def test_classify_bug_security():
    """Test classification of security issue"""
    bug = {
        "bug_id": "BUG-002",
        "title": "SQL Injection vulnerability",
        "description": "User input not sanitized in database query"
    }
    
    result = classify_bug(bug)
    assert result["category"] == "Security"
    assert result["confidence"] > 0.0


def test_classify_category_runtime():
    """Test category classification for runtime error"""
    text = "NullPointerException at line 42"
    category = classify_category(text)
    assert category == "Runtime Error"


def test_classify_type_nullpointer():
    """Test type classification for NullPointerException"""
    text = "java.lang.NullPointerException"
    category = "Runtime Error"
    bug_type = classify_type(text, category)
    assert "NullPointer" in bug_type or "null" in bug_type.lower()


def test_analyze_root_cause():
    """Test root cause analysis"""
    bug = {
        "title": "NullPointerException",
        "description": "App crashes"
    }
    category = "Runtime Error"
    bug_type = "NullPointerException"
    
    root_cause = analyze_root_cause(bug, category, bug_type)
    assert root_cause is not None
    assert len(root_cause) > 0


def test_calculate_confidence_with_stack_trace():
    """Test confidence calculation with stack trace"""
    bug = {
        "title": "Error",
        "description": "Something broke",
        "stack_trace": "Exception at line 1"
    }
    
    confidence = calculate_classification_confidence(bug, None, "Runtime Error", "Exception")
    assert confidence >= 0.7  # Should be higher with stack trace


def test_calculate_confidence_with_code_context():
    """Test confidence calculation with code context"""
    bug = {
        "title": "Error",
        "description": "Something broke"
    }
    code_context = {
        "snippet": "def function(): pass"
    }
    
    confidence = calculate_classification_confidence(bug, code_context, "Logic Error", "Issue")
    assert confidence >= 0.65  # Should be higher with code context



