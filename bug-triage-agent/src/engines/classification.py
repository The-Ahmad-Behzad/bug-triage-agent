"""Bug classification engine"""

import re
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger("bug_triage_agent")


# Category patterns
CATEGORY_PATTERNS = {
    "Runtime Error": [
        r"NullPointerException",
        r"IndexOutOfBoundsException",
        r"ArrayIndexOutOfBounds",
        r"TypeError",
        r"AttributeError",
        r"KeyError",
        r"ValueError",
        r"RuntimeException",
        r"undefined is not",
        r"Cannot read property",
        r"is not defined"
    ],
    "Security": [
        r"SQL.*injection",
        r"XSS",
        r"cross.?site.*scripting",
        r"authentication.*failed",
        r"unauthorized",
        r"forbidden",
        r"CSRF",
        r"security.*vulnerability",
        r"insecure",
        r"vulnerability"
    ],
    "Performance": [
        r"timeout",
        r"slow",
        r"performance",
        r"memory.*leak",
        r"out of memory",
        r"OOM",
        r"CPU.*high",
        r"response.*time",
        r"latency"
    ],
    "Logic Error": [
        r"logic.*error",
        r"incorrect.*calculation",
        r"wrong.*result",
        r"unexpected.*behavior",
        r"does not work",
        r"not.*working",
        r"broken"
    ],
    "Configuration Error": [
        r"configuration.*error",
        r"config.*missing",
        r"environment.*variable",
        r"setting.*not.*found",
        r"invalid.*config"
    ],
    "UX/UI Issue": [
        r"UI.*issue",
        r"user.*interface",
        r"display.*wrong",
        r"layout.*broken",
        r"styling",
        r"CSS",
        r"rendering"
    ]
}

# Type patterns (more specific)
TYPE_PATTERNS = {
    "NullPointerException": [r"NullPointerException", r"null.*pointer", r"NoneType"],
    "SQL Injection": [r"SQL.*injection", r"SQLi"],
    "Index Out of Bounds": [r"IndexOutOfBounds", r"array.*index", r"list.*index"],
    "Type Error": [r"TypeError", r"type.*error", r"cannot.*convert"],
    "Authentication Error": [r"authentication.*failed", r"unauthorized", r"login.*failed"],
    "Timeout": [r"timeout", r"request.*timed.*out"],
    "Memory Leak": [r"memory.*leak", r"out.*of.*memory", r"OOM"]
}


def classify_bug(bug: Dict[str, Any], code_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Classify a bug into category, type, and root cause
    
    Args:
        bug: Bug input dictionary
        code_context: Optional code context dictionary
    
    Returns:
        Dictionary with classification, type, and root_cause
    """
    # Combine text sources for analysis
    text_sources = []
    
    if bug.get("title"):
        text_sources.append(bug["title"].lower())
    if bug.get("description"):
        text_sources.append(bug["description"].lower())
    if bug.get("stack_trace"):
        text_sources.append(bug["stack_trace"].lower())
    if bug.get("logs"):
        text_sources.append(bug["logs"].lower())
    
    combined_text = " ".join(text_sources)
    
    # Classify category
    category = classify_category(combined_text, code_context)
    
    # Classify type
    bug_type = classify_type(combined_text, category, code_context)
    
    # Analyze root cause
    root_cause = analyze_root_cause(bug, category, bug_type, code_context)
    
    # Calculate confidence
    confidence = calculate_classification_confidence(bug, code_context, category, bug_type)
    
    return {
        "category": category,
        "type": bug_type,
        "root_cause": root_cause,
        "confidence": confidence
    }


def classify_category(text: str, code_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Classify bug category
    
    Args:
        text: Combined text from bug description, stack trace, etc.
        code_context: Optional code context
    
    Returns:
        Category string
    """
    category_scores = {}
    
    # Score each category based on pattern matches
    for category, patterns in CATEGORY_PATTERNS.items():
        score = 0
        for pattern in patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches
        category_scores[category] = score
    
    # Check code context for additional hints
    if code_context:
        snippet = code_context.get("snippet", "").lower()
        file_path = code_context.get("file_path", "").lower()
        
        # Security-related file paths
        if any(term in file_path for term in ["auth", "security", "login", "password"]):
            category_scores["Security"] = category_scores.get("Security", 0) + 1
        
        # Performance-related patterns in code
        if any(term in snippet for term in ["loop", "recursion", "while", "for"]):
            category_scores["Performance"] = category_scores.get("Performance", 0) + 0.5
    
    # Return category with highest score, default to "Logic Error"
    if category_scores:
        max_category = max(category_scores.items(), key=lambda x: x[1])
        if max_category[1] > 0:
            return max_category[0]
    
    return "Logic Error"  # Default category


def classify_type(text: str, category: str, code_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Classify specific bug type
    
    Args:
        text: Combined text
        category: Detected category
        code_context: Optional code context
    
    Returns:
        Type string
    """
    type_scores = {}
    
    # Score each type based on pattern matches
    for bug_type, patterns in TYPE_PATTERNS.items():
        score = 0
        for pattern in patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches
        type_scores[bug_type] = score
    
    # Category-specific type inference
    if category == "Runtime Error":
        # Look for specific exception types in stack trace
        if "stack_trace" in text:
            if "NullPointerException" in text or "null pointer" in text:
                return "NullPointerException"
            elif "IndexOutOfBounds" in text:
                return "Index Out of Bounds"
            elif "TypeError" in text:
                return "Type Error"
    
    elif category == "Security":
        if "sql" in text and "injection" in text:
            return "SQL Injection"
        elif "xss" in text or "cross-site" in text:
            return "XSS"
        elif "authentication" in text or "unauthorized" in text:
            return "Authentication Error"
    
    elif category == "Performance":
        if "timeout" in text:
            return "Timeout"
        elif "memory" in text and "leak" in text:
            return "Memory Leak"
    
    # Return type with highest score, or generic type
    if type_scores:
        max_type = max(type_scores.items(), key=lambda x: x[1])
        if max_type[1] > 0:
            return max_type[0]
    
    # Default type based on category
    return f"{category} Issue"


def analyze_root_cause(
    bug: Dict[str, Any],
    category: str,
    bug_type: str,
    code_context: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """
    Analyze root cause of the bug
    
    Args:
        bug: Bug input dictionary
        category: Detected category
        bug_type: Detected type
        code_context: Optional code context
    
    Returns:
        Root cause description or None
    """
    root_causes = []
    
    # Analyze based on category and type
    if category == "Runtime Error":
        if bug_type == "NullPointerException":
            if code_context and code_context.get("snippet"):
                root_causes.append("Missing null check before accessing object property or method")
            else:
                root_causes.append("Object is null when accessed")
        
        elif bug_type == "Index Out of Bounds":
            root_causes.append("Array or list index exceeds bounds")
    
    elif category == "Security":
        if bug_type == "SQL Injection":
            root_causes.append("User input not properly sanitized before database query")
        elif bug_type == "Authentication Error":
            root_causes.append("Authentication credentials invalid or session expired")
    
    elif category == "Performance":
        if bug_type == "Timeout":
            root_causes.append("Operation taking longer than expected timeout period")
        elif bug_type == "Memory Leak":
            root_causes.append("Memory not properly released, causing gradual memory consumption")
    
    # Analyze code context if available
    if code_context:
        snippet = code_context.get("snippet", "")
        file_path = code_context.get("file_path", "")
        
        # Look for common patterns
        if snippet and "null" in snippet.lower() and "check" not in snippet.lower():
            root_causes.append("Missing null check in code")
        
        stack_trace = bug.get("stack_trace") or ""
        if snippet and "try" not in snippet.lower() and stack_trace and "exception" in stack_trace.lower():
            root_causes.append("Missing exception handling")
    
    # Return first root cause or generic description
    if root_causes:
        return root_causes[0]
    
    return f"Issue in {category.lower()} category, type: {bug_type}"


def calculate_classification_confidence(
    bug: Dict[str, Any],
    code_context: Optional[Dict[str, Any]],
    category: str,
    bug_type: str
) -> float:
    """
    Calculate confidence in classification
    
    Args:
        bug: Bug input dictionary
        code_context: Optional code context
        category: Detected category
        bug_type: Detected type
    
    Returns:
        Confidence score (0.0 to 1.0)
    """
    confidence = 0.5  # Base confidence
    
    # Increase confidence if stack trace is available
    if bug.get("stack_trace"):
        confidence += 0.2
    
    # Increase confidence if code context is available
    if code_context and code_context.get("snippet"):
        confidence += 0.15
    
    # Increase confidence if description is detailed
    description = bug.get("description", "")
    if len(description) > 100:
        confidence += 0.1
    
    # Increase confidence if logs are available
    if bug.get("logs"):
        confidence += 0.05
    
    # Cap at 1.0
    return min(confidence, 1.0)

