"""Severity priority rules database operations"""

from typing import List, Dict, Any
from pymongo.collection import Collection
import logging

from src.database.connection import get_database

logger = logging.getLogger("bug_triage_agent")


def get_severity_priority_rules_collection() -> Collection:
    """Get severity_priority_rules collection"""
    db = get_database()
    return db.severity_priority_rules


def get_priority_rule(severity: str) -> Dict[str, Any]:
    """
    Get priority rule for a severity
    
    Args:
        severity: Severity string
    
    Returns:
        Priority rule document or None
    """
    collection = get_severity_priority_rules_collection()
    rule = collection.find_one({"severity": severity})
    
    if rule:
        rule["_id"] = str(rule["_id"])
        return rule
    
    return None


def get_all_priority_rules() -> List[Dict[str, Any]]:
    """
    Get all priority rules
    
    Returns:
        List of priority rule documents
    """
    collection = get_severity_priority_rules_collection()
    rules = collection.find({})
    
    result = []
    for rule in rules:
        rule["_id"] = str(rule["_id"])
        result.append(rule)
    
    return result



