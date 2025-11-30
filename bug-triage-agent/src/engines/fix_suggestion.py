"""Fix suggestion engine"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger("bug_triage_agent")


def suggest_fix(
    bug: Dict[str, Any],
    classification: Dict[str, Any],
    code_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Suggest fix approach for a bug
    
    Args:
        bug: Bug input dictionary
        classification: Classification result
        code_context: Optional code context
    
    Returns:
        Dictionary with approach and estimated_effort
    """
    category = classification.get("category", "")
    bug_type = classification.get("type", "")
    root_cause = classification.get("root_cause", "")
    
    # Generate fix approach
    approach = generate_fix_approach(category, bug_type, root_cause, code_context)
    
    # Estimate effort
    estimated_effort = estimate_effort(category, bug_type, code_context)
    
    return {
        "approach": approach,
        "estimated_effort": estimated_effort
    }


def generate_fix_approach(
    category: str,
    bug_type: str,
    root_cause: str,
    code_context: Optional[Dict[str, Any]]
) -> str:
    """
    Generate fix approach description
    
    Args:
        category: Bug category
        bug_type: Bug type
        root_cause: Root cause description
        code_context: Optional code context
    
    Returns:
        Fix approach string
    """
    approaches = []
    
    # Category-specific approaches
    if category == "Runtime Error":
        if "NullPointerException" in bug_type or "null" in bug_type.lower():
            approaches.append("Add null check before accessing object properties or methods")
            if code_context:
                approaches.append("Ensure object is properly initialized before use")
        elif "IndexOutOfBounds" in bug_type or "index" in bug_type.lower():
            approaches.append("Add bounds checking before accessing array or list indices")
            approaches.append("Validate array/list size before iteration")
    
    elif category == "Security":
        if "SQL Injection" in bug_type:
            approaches.append("Use parameterized queries or prepared statements")
            approaches.append("Sanitize and validate all user inputs")
        elif "XSS" in bug_type:
            approaches.append("Escape user input before rendering in HTML")
            approaches.append("Use Content Security Policy (CSP) headers")
        elif "Authentication" in bug_type:
            approaches.append("Verify authentication credentials properly")
            approaches.append("Implement proper session management")
    
    elif category == "Performance":
        if "Timeout" in bug_type:
            approaches.append("Optimize slow database queries")
            approaches.append("Add caching for frequently accessed data")
            approaches.append("Consider increasing timeout values if appropriate")
        elif "Memory Leak" in bug_type:
            approaches.append("Ensure proper resource cleanup (close files, connections)")
            approaches.append("Review object lifecycle and memory management")
    
    elif category == "Logic Error":
        approaches.append("Review business logic and algorithm implementation")
        approaches.append("Add unit tests to verify correct behavior")
        if code_context:
            approaches.append("Trace through code execution path to identify incorrect logic")
    
    elif category == "Configuration Error":
        approaches.append("Verify all required configuration values are set")
        approaches.append("Check environment variables and configuration files")
        approaches.append("Validate configuration values on application startup")
    
    # Root cause specific
    if root_cause:
        if "null check" in root_cause.lower():
            approaches.append("Implement defensive programming with null checks")
        if "exception handling" in root_cause.lower():
            approaches.append("Add try-catch blocks for error handling")
    
    # Generic approach if no specific approach found
    if not approaches:
        approaches.append(f"Review and fix the {category.lower()} issue")
        approaches.append("Test the fix thoroughly before deployment")
    
    return ". ".join(approaches) + "."


def estimate_effort(
    category: str,
    bug_type: str,
    code_context: Optional[Dict[str, Any]]
) -> str:
    """
    Estimate effort required to fix the bug
    
    Args:
        category: Bug category
        bug_type: Bug type
        code_context: Optional code context
    
    Returns:
        Effort estimate string
    """
    # Base effort by category
    if category == "Runtime Error":
        if "NullPointerException" in bug_type:
            return "1-2 hours"
        elif "IndexOutOfBounds" in bug_type:
            return "1-2 hours"
        else:
            return "2-4 hours"
    
    elif category == "Security":
        if "SQL Injection" in bug_type:
            return "4-8 hours"  # Requires careful review
        elif "XSS" in bug_type:
            return "2-4 hours"
        else:
            return "3-6 hours"
    
    elif category == "Performance":
        if "Memory Leak" in bug_type:
            return "4-8 hours"  # Requires profiling and analysis
        elif "Timeout" in bug_type:
            return "2-6 hours"  # Depends on root cause
        else:
            return "3-6 hours"
    
    elif category == "Logic Error":
        return "2-6 hours"  # Varies significantly
    
    elif category == "Configuration Error":
        return "30 minutes - 2 hours"  # Usually quick fix
    
    elif category == "UX/UI Issue":
        return "1-4 hours"  # Depends on complexity
    
    # Default estimate
    if code_context:
        return "2-4 hours"
    else:
        return "1-3 hours"



