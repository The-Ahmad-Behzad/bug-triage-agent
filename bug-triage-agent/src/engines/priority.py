"""Priority assessment engine"""

from typing import Dict, Any, Optional
import logging

from src.database.severity_priority_rules import get_priority_rule

logger = logging.getLogger("bug_triage_agent")


PRIORITY_LEVELS = ["critical", "high", "medium", "low"]


def assess_priority(
    bug: Dict[str, Any],
    classification: Dict[str, Any],
    severity_rules: Optional[list] = None
) -> Dict[str, Any]:
    """
    Assess bug priority level
    
    Args:
        bug: Bug input dictionary
        classification: Classification result
        severity_rules: Optional list of severity priority rules from database
    
    Returns:
        Dictionary with level and justification
    """
    category = classification.get("category", "")
    bug_type = classification.get("type", "")
    metadata = bug.get("metadata") or {}
    environment = metadata.get("environment", "").lower() if metadata else ""
    tags = metadata.get("tags", []) if metadata else []
    
    # Check severity rules first
    if severity_rules:
        rule_priority = check_severity_rules(bug, classification, severity_rules)
        if rule_priority:
            return rule_priority
    
    # Assess based on category and type
    priority_level = determine_priority_level(category, bug_type, environment, tags)
    
    # Generate justification
    justification = generate_justification(category, bug_type, environment, tags, priority_level)
    
    # Calculate confidence
    confidence = calculate_priority_confidence(bug, classification, priority_level)
    
    return {
        "level": priority_level,
        "justification": justification,
        "confidence": confidence
    }


def determine_priority_level(
    category: str,
    bug_type: str,
    environment: str,
    tags: list
) -> str:
    """
    Determine priority level based on factors
    
    Args:
        category: Bug category
        bug_type: Bug type
        environment: Environment (production, staging, dev)
        tags: List of tags
    
    Returns:
        Priority level string
    """
    # Critical conditions
    if environment == "production":
        if category == "Security":
            return "critical"
        if category == "Runtime Error" and "crash" in " ".join(tags).lower():
            return "critical"
        if "data_loss" in " ".join(tags).lower():
            return "critical"
    
    # High priority conditions
    if category == "Security":
        return "high"
    if category == "Runtime Error":
        if "crash" in bug_type.lower() or "exception" in bug_type.lower():
            return "high"
    if environment == "production" and category in ["Performance", "Logic Error"]:
        return "high"
    
    # Medium priority conditions
    if category in ["Performance", "Logic Error"]:
        return "medium"
    if category == "Configuration Error":
        return "medium"
    
    # Default to low
    return "low"


def generate_justification(
    category: str,
    bug_type: str,
    environment: str,
    tags: list,
    priority_level: str
) -> str:
    """
    Generate justification for priority level
    
    Args:
        category: Bug category
        bug_type: Bug type
        environment: Environment
        tags: List of tags
        priority_level: Priority level
    
    Returns:
        Justification string
    """
    reasons = []
    
    if environment == "production":
        reasons.append("affecting production environment")
    
    if category == "Security":
        reasons.append("security vulnerability")
    
    if category == "Runtime Error":
        reasons.append("runtime error causing application instability")
    
    if "crash" in " ".join(tags).lower():
        reasons.append("causing application crashes")
    
    if priority_level == "critical":
        return f"Critical priority: {'; '.join(reasons) if reasons else 'severe impact on system'}"
    elif priority_level == "high":
        return f"High priority: {'; '.join(reasons) if reasons else 'significant impact'}"
    elif priority_level == "medium":
        return f"Medium priority: {'; '.join(reasons) if reasons else 'moderate impact'}"
    else:
        return f"Low priority: {'; '.join(reasons) if reasons else 'minimal impact'}"


def check_severity_rules(
    bug: Dict[str, Any],
    classification: Dict[str, Any],
    severity_rules: list
) -> Optional[Dict[str, Any]]:
    """
    Check severity priority rules from database
    
    Args:
        bug: Bug input dictionary
        classification: Classification result
        severity_rules: List of severity priority rules
    
    Returns:
        Priority dict if rule matches, None otherwise
    """
    category = classification.get("category", "")
    metadata = bug.get("metadata") or {}
    environment = metadata.get("environment", "") if metadata else ""
    tags = metadata.get("tags", []) if metadata else []
    
    for rule in severity_rules:
        severity = rule.get("severity", "")
        conditions = rule.get("conditions", [])
        
        # Check if conditions match
        matches = True
        for condition in conditions:
            if condition == "production" and environment.lower() != "production":
                matches = False
                break
            if condition not in " ".join(tags).lower() and condition not in category.lower():
                # Check if condition is a general tag
                if condition not in [tag.lower() for tag in tags]:
                    matches = False
                    break
        
        if matches:
            priority_level = rule.get("priority", "medium")
            justification = f"Matches severity rule: {severity} -> {priority_level}"
            return {
                "level": priority_level,
                "justification": justification,
                "confidence": 0.9  # High confidence for rule-based priority
            }
    
    return None


def calculate_priority_confidence(
    bug: Dict[str, Any],
    classification: Dict[str, Any],
    priority_level: str
) -> float:
    """
    Calculate confidence in priority assessment
    
    Args:
        bug: Bug input dictionary
        classification: Classification result
        priority_level: Priority level
    
    Returns:
        Confidence score (0.0 to 1.0)
    """
    confidence = 0.7  # Base confidence
    
    # Increase confidence if environment is specified
    metadata = bug.get("metadata") or {}
    if metadata and metadata.get("environment"):
        confidence += 0.1
    
    # Increase confidence if tags are provided
    if metadata and metadata.get("tags"):
        confidence += 0.1
    
    # Increase confidence if classification is confident
    classification_confidence = classification.get("confidence", 0.5)
    if classification_confidence > 0.8:
        confidence += 0.1
    
    # Cap at 1.0
    return min(confidence, 1.0)

