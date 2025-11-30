"""Team member assignment engine"""

from typing import Dict, Any, List, Optional
import logging

from src.database.team_members import query_by_language, query_by_skills, query_by_module, get_team_member
from src.database.module_ownership import get_module_owners
from src.database.developer_load import get_developer_load, get_all_developer_loads
from src.database.routing_rules import get_applicable_routing_rules

logger = logging.getLogger("bug_triage_agent")


def assign_bug(
    bug: Dict[str, Any],
    team_profiles: List[Dict[str, Any]],
    db_available: bool = True
) -> Dict[str, Any]:
    """
    Assign bug to most suitable team member
    
    Args:
        bug: Bug input dictionary
        team_profiles: List of team member profiles
        db_available: Whether database is available
    
    Returns:
        Assignment dictionary with member_id, name, and confidence
    """
    # Check routing rules first
    if db_available:
        routing_rule = check_routing_rules(bug)
        if routing_rule:
            return routing_rule
    
    # Get bug requirements
    language = bug.get("language")
    code_context = bug.get("code_context") or {}
    file_path = code_context.get("file_path", "") if code_context else ""
    
    # Extract module from file path
    module = extract_module_from_path(file_path)
    
    # Score each team member
    candidates = []
    for profile in team_profiles:
        score = calculate_assignment_score(bug, profile, language, module, db_available)
        if score > 0:
            candidates.append({
                "profile": profile,
                "score": score
            })
    
    # Sort by score (highest first)
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    if not candidates:
        # Fallback: assign to first available member
        if team_profiles:
            return {
                "assigned_to_member_id": team_profiles[0]["member_id"],
                "assigned_to_name": team_profiles[0]["name"],
                "confidence": 0.3
            }
        return {
            "assigned_to_member_id": "unknown",
            "assigned_to_name": "Unknown",
            "confidence": 0.0
        }
    
    # Get best candidate
    best_candidate = candidates[0]
    profile = best_candidate["profile"]
    score = best_candidate["score"]
    
    # Normalize score to confidence (0.0-1.0)
    confidence = min(score / 10.0, 1.0)  # Assuming max score is around 10
    
    return {
        "assigned_to_member_id": profile["member_id"],
        "assigned_to_name": profile["name"],
        "confidence": confidence
    }


def calculate_assignment_score(
    bug: Dict[str, Any],
    profile: Dict[str, Any],
    language: Optional[str],
    module: Optional[str],
    db_available: bool
) -> float:
    """
    Calculate assignment score for a team member
    
    Args:
        bug: Bug input dictionary
        profile: Team member profile
        language: Bug language
        module: Bug module
        db_available: Whether database is available
    
    Returns:
        Assignment score (higher is better)
    """
    score = 0.0
    
    # Language matching (highest weight)
    if language:
        skills = profile.get("skills", {})
        if isinstance(skills, dict):
            languages = skills.get("languages", [])
        elif isinstance(skills, list):
            languages = skills
        else:
            languages = []
        
        if language.lower() in [lang.lower() for lang in languages]:
            score += 5.0  # Strong match
        elif db_available:
            # Check database for additional language skills
            try:
                db_member = get_team_member(profile["member_id"])
                if db_member:
                    db_skills = db_member.get("skills", {})
                    if isinstance(db_skills, dict):
                        db_languages = db_skills.get("languages", [])
                        if language.lower() in [lang.lower() for lang in db_languages]:
                            score += 4.0
            except Exception:
                # Database unavailable, skip database lookup
                pass
    
    # Module ownership (high weight)
    if module:
        modules_owned = profile.get("modules_owned", [])
        if module in modules_owned:
            score += 4.0
        elif db_available:
            # Check database for module ownership
            try:
                db_member = get_team_member(profile["member_id"])
                if db_member:
                    db_modules = db_member.get("modules_owned", [])
                    if module in db_modules:
                        score += 3.5
            except Exception:
                # Database unavailable, skip database lookup
                pass
    
    # Skills matching (medium weight)
    skills = profile.get("skills", {})
    if isinstance(skills, dict):
        frameworks = skills.get("frameworks") or []
        domains = skills.get("domains") or []
    elif isinstance(skills, list):
        frameworks = []
        domains = skills or []
    else:
        frameworks = []
        domains = []
    
    # Check bug description for skill keywords
    description = bug.get("description", "").lower()
    for framework in (frameworks or []):
        if framework.lower() in description:
            score += 1.0
    
    for domain in (domains or []):
        if domain.lower() in description:
            score += 1.0
    
    # Workload consideration (negative weight)
    current_load = profile.get("current_load")
    if current_load is not None:
        if current_load > 5:
            score -= 1.0  # Penalize high workload
        elif current_load == 0:
            score += 0.5  # Bonus for low workload
    
    # Database workload check
    if db_available:
        try:
            load_data = get_developer_load(profile["member_id"])
            if load_data:
                load_score = load_data.get("current_load_score", 0.5)
                if load_score > 0.8:
                    score -= 1.5  # High load penalty
                elif load_score < 0.3:
                    score += 0.5  # Low load bonus
        except Exception:
            # Database unavailable, skip workload check
            pass
    
    return max(score, 0.0)  # Ensure non-negative


def extract_module_from_path(file_path: str) -> Optional[str]:
    """
    Extract module name from file path
    
    Args:
        file_path: File path string
    
    Returns:
        Module name or None
    """
    if not file_path:
        return None
    
    path_lower = file_path.lower()
    
    # Common module patterns
    if '/auth' in path_lower or '\\auth' in path_lower:
        return "auth"
    elif '/api' in path_lower or '\\api' in path_lower:
        return "api"
    elif '/db' in path_lower or '/database' in path_lower:
        return "database"
    elif '/ui' in path_lower or '/frontend' in path_lower:
        return "ui"
    elif '/user' in path_lower:
        return "user"
    elif '/payment' in path_lower:
        return "payment"
    
    return None


def check_routing_rules(bug: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Check if any routing rules apply
    
    Args:
        bug: Bug input dictionary
    
    Returns:
        Assignment dict if rule applies, None otherwise
    """
    try:
        rules = get_applicable_routing_rules(bug)
        if rules:
            # Use first applicable rule
            rule = rules[0]
            assign_to = rule.get("assign_to", [])
            if assign_to:
                # Return assignment for first member in list
                return {
                    "assigned_to_member_id": assign_to[0],
                    "assigned_to_name": assign_to[0],  # Would need to lookup name
                    "confidence": 0.95  # High confidence for rule-based assignment
                }
    except Exception as e:
        # Database unavailable or error - continue without routing rules
        logger.debug(f"Could not check routing rules: {e}")
    
    return None

