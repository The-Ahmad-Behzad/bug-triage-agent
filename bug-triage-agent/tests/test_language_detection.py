"""Tests for language and file type detection"""

import pytest
from src.utils.language_detector import (
    detect_language_from_path,
    detect_file_type_from_path,
    validate_language_file_type_consistency,
    detect_and_validate_language_file_type
)


def test_detect_language_from_path_python():
    """Test language detection for Python files"""
    assert detect_language_from_path("src/main.py") == "python"
    assert detect_language_from_path("test/test_file.pyw") == "python"


def test_detect_language_from_path_java():
    """Test language detection for Java files"""
    assert detect_language_from_path("src/Main.java") == "java"


def test_detect_language_from_path_javascript():
    """Test language detection for JavaScript files"""
    assert detect_language_from_path("src/app.js") == "javascript"
    assert detect_language_from_path("src/component.jsx") == "javascript"


def test_detect_language_from_path_typescript():
    """Test language detection for TypeScript files"""
    assert detect_language_from_path("src/app.ts") == "typescript"
    assert detect_language_from_path("src/component.tsx") == "typescript"


def test_detect_language_from_path_unknown():
    """Test language detection for unknown file types"""
    assert detect_language_from_path("src/unknown.xyz") is None
    assert detect_language_from_path("") is None


def test_detect_file_type_from_path():
    """Test file type detection"""
    assert detect_file_type_from_path("src/main.py") == ".py"
    assert detect_file_type_from_path("src/Main.java") == ".java"
    assert detect_file_type_from_path("src/app.js") == ".js"
    assert detect_file_type_from_path("src/component.tsx") == ".tsx"
    assert detect_file_type_from_path("src/unknown") is None


def test_validate_language_file_type_consistency():
    """Test language and file type consistency validation"""
    # Valid combinations
    assert validate_language_file_type_consistency("python", ".py") is True
    assert validate_language_file_type_consistency("java", ".java") is True
    assert validate_language_file_type_consistency("javascript", ".js") is True
    
    # Invalid combinations
    assert validate_language_file_type_consistency("python", ".java") is False
    assert validate_language_file_type_consistency("java", ".py") is False
    
    # None values should be considered consistent
    assert validate_language_file_type_consistency(None, ".py") is True
    assert validate_language_file_type_consistency("python", None) is True


def test_detect_and_validate_language_file_type():
    """Test combined detection and validation"""
    # Auto-detect from file path
    lang, ftype = detect_and_validate_language_file_type(file_path="src/main.py")
    assert lang == "python"
    assert ftype == ".py"
    
    # Use provided values
    lang, ftype = detect_and_validate_language_file_type(
        file_path="src/main.py",
        language="java",
        file_type=".java"
    )
    assert lang == "java"
    assert ftype == ".java"
    
    # Auto-detect when not provided
    lang, ftype = detect_and_validate_language_file_type(file_path="src/app.js")
    assert lang == "javascript"
    assert ftype == ".js"



