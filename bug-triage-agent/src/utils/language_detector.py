"""Language and file type detection utilities"""

import os
from typing import Optional, Tuple


# Mapping of file extensions to programming languages
EXTENSION_TO_LANGUAGE = {
    # Python
    '.py': 'python',
    '.pyw': 'python',
    '.pyx': 'python',
    
    # Java
    '.java': 'java',
    '.class': 'java',
    '.jar': 'java',
    
    # JavaScript/TypeScript
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.mjs': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    
    # C/C++
    '.c': 'c',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.h': 'c',
    '.hpp': 'cpp',
    
    # C#
    '.cs': 'csharp',
    
    # Go
    '.go': 'go',
    
    # Rust
    '.rs': 'rust',
    
    # Ruby
    '.rb': 'ruby',
    
    # PHP
    '.php': 'php',
    
    # Swift
    '.swift': 'swift',
    
    # Kotlin
    '.kt': 'kotlin',
    '.kts': 'kotlin',
    
    # Scala
    '.scala': 'scala',
    
    # R
    '.r': 'r',
    '.R': 'r',
    
    # Shell
    '.sh': 'shell',
    '.bash': 'shell',
    '.zsh': 'shell',
    
    # PowerShell
    '.ps1': 'powershell',
    '.psm1': 'powershell',
    
    # HTML/CSS
    '.html': 'html',
    '.htm': 'html',
    '.css': 'css',
    '.scss': 'css',
    '.sass': 'css',
    
    # SQL
    '.sql': 'sql',
    
    # YAML/JSON
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.json': 'json',
    
    # XML
    '.xml': 'xml',
}


def detect_language_from_path(file_path: str) -> Optional[str]:
    """
    Detect programming language from file path
    
    Args:
        file_path: Path to the source file
    
    Returns:
        Programming language name or None if not detected
    """
    if not file_path:
        return None
    
    # Get file extension
    _, ext = os.path.splitext(file_path.lower())
    
    # Look up in mapping
    return EXTENSION_TO_LANGUAGE.get(ext)


def detect_file_type_from_path(file_path: str) -> Optional[str]:
    """
    Detect file type (extension) from file path
    
    Args:
        file_path: Path to the source file
    
    Returns:
        File extension (with dot) or None if not detected
    """
    if not file_path:
        return None
    
    # Get file extension
    _, ext = os.path.splitext(file_path.lower())
    
    return ext if ext else None


def validate_language_file_type_consistency(language: Optional[str], file_type: Optional[str]) -> bool:
    """
    Validate that language and file_type are consistent
    
    Args:
        language: Programming language name
        file_type: File extension (with or without dot)
    
    Returns:
        True if consistent or if either is None, False otherwise
    """
    if not language or not file_type:
        return True  # If either is missing, consider it consistent
    
    # Normalize file_type (ensure it starts with dot)
    if not file_type.startswith('.'):
        file_type = '.' + file_type
    
    # Get expected language for this file type
    expected_language = EXTENSION_TO_LANGUAGE.get(file_type.lower())
    
    # If we can't determine expected language, consider it consistent
    if not expected_language:
        return True
    
    # Check if languages match (case-insensitive)
    return language.lower() == expected_language.lower()


def detect_and_validate_language_file_type(
    file_path: Optional[str] = None,
    language: Optional[str] = None,
    file_type: Optional[str] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Detect and validate language and file_type, auto-detecting if not provided
    
    Args:
        file_path: Path to source file (for auto-detection)
        language: Explicitly provided language
        file_type: Explicitly provided file type
    
    Returns:
        Tuple of (language, file_type) - both may be None if detection fails
    """
    # Auto-detect from file_path if not provided
    if not language and file_path:
        language = detect_language_from_path(file_path)
    
    if not file_type and file_path:
        file_type = detect_file_type_from_path(file_path)
    
    # Validate consistency if both are provided
    if language and file_type:
        if not validate_language_file_type_consistency(language, file_type):
            # If inconsistent, prefer file_type detection
            if file_path:
                detected_language = detect_language_from_path(file_path)
                if detected_language:
                    language = detected_language
    
    return language, file_type



