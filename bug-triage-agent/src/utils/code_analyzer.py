"""Code context analysis utilities"""

import re
from typing import Dict, Any, List, Optional


def parse_code_snippet(snippet: str) -> Dict[str, Any]:
    """
    Parse code snippet to extract information
    
    Args:
        snippet: Code snippet string
    
    Returns:
        Dictionary with parsed information
    """
    if not snippet:
        return {}
    
    lines = snippet.split('\n')
    
    return {
        "line_count": len(lines),
        "has_loops": has_loops(snippet),
        "has_conditionals": has_conditionals(snippet),
        "has_null_checks": has_null_checks(snippet),
        "has_exception_handling": has_exception_handling(snippet),
        "function_calls": extract_function_calls(snippet),
        "variable_assignments": extract_variable_assignments(snippet)
    }


def extract_error_patterns(stack_trace: str) -> List[str]:
    """
    Extract error patterns from stack trace
    
    Args:
        stack_trace: Stack trace string
    
    Returns:
        List of error patterns
    """
    if not stack_trace:
        return []
    
    patterns = []
    
    # Extract exception type
    exception_match = re.search(r'(\w+Exception|\w+Error)', stack_trace)
    if exception_match:
        patterns.append(exception_match.group(1))
    
    # Extract file and line number
    file_line_match = re.search(r'(\w+\.\w+):(\d+)', stack_trace)
    if file_line_match:
        patterns.append(f"{file_line_match.group(1)}:{file_line_match.group(2)}")
    
    # Extract method names
    method_matches = re.findall(r'at\s+(\w+\.\w+\.\w+)', stack_trace)
    patterns.extend(method_matches)
    
    return patterns


def match_patterns_in_code(patterns: List[str], code: str) -> bool:
    """
    Check if error patterns match code
    
    Args:
        patterns: List of error patterns
        code: Code string
    
    Returns:
        True if any pattern matches
    """
    if not patterns or not code:
        return False
    
    code_lower = code.lower()
    
    for pattern in patterns:
        if pattern.lower() in code_lower:
            return True
    
    return False


def has_loops(code: str) -> bool:
    """Check if code contains loops"""
    loop_keywords = ['for', 'while', 'do-while', 'foreach', 'for each']
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in loop_keywords)


def has_conditionals(code: str) -> bool:
    """Check if code contains conditionals"""
    conditional_keywords = ['if', 'else', 'switch', 'case', 'ternary']
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in conditional_keywords)


def has_null_checks(code: str) -> bool:
    """Check if code contains null checks"""
    null_check_patterns = [
        r'if\s*\([^)]*==\s*null',
        r'if\s*\([^)]*!=\s*null',
        r'if\s*\([^)]*is\s+None',
        r'if\s*\([^)]*is\s+not\s+None',
        r'if\s*\([^)]*===?\s*null',
        r'if\s*\([^)]*!==?\s*null'
    ]
    
    for pattern in null_check_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return True
    
    return False


def has_exception_handling(code: str) -> bool:
    """Check if code contains exception handling"""
    exception_keywords = ['try', 'catch', 'except', 'finally', 'throw', 'raise']
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in exception_keywords)


def extract_function_calls(code: str) -> List[str]:
    """Extract function calls from code"""
    # Simple pattern matching for function calls
    pattern = r'(\w+)\s*\([^)]*\)'
    matches = re.findall(pattern, code)
    return list(set(matches))  # Return unique function names


def extract_variable_assignments(code: str) -> List[str]:
    """Extract variable assignments from code"""
    # Pattern for variable assignments (var = value, let var = value, etc.)
    pattern = r'(?:let|var|const|)\s*(\w+)\s*='
    matches = re.findall(pattern, code)
    return list(set(matches))  # Return unique variable names


def analyze_file_path(file_path: str) -> Dict[str, Any]:
    """
    Analyze file path for module and context information
    
    Args:
        file_path: File path string
    
    Returns:
        Dictionary with analysis results
    """
    if not file_path:
        return {}
    
    path_lower = file_path.lower()
    
    # Detect module from path
    module = None
    if '/auth' in path_lower or '\\auth' in path_lower:
        module = "auth"
    elif '/api' in path_lower or '\\api' in path_lower:
        module = "api"
    elif '/db' in path_lower or '/database' in path_lower or '\\db' in path_lower:
        module = "database"
    elif '/ui' in path_lower or '/frontend' in path_lower:
        module = "ui"
    
    # Detect if test file
    is_test = 'test' in path_lower or 'spec' in path_lower
    
    # Detect if config file
    is_config = 'config' in path_lower or 'settings' in path_lower
    
    return {
        "module": module,
        "is_test": is_test,
        "is_config": is_config,
        "file_path": file_path
    }



