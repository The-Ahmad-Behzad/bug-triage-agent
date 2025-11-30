"""Routing rules database operations"""

from typing import List, Dict, Any
from pymongo.collection import Collection
import logging

from src.database.connection import get_database

logger = logging.getLogger("bug_triage_agent")


def get_routing_rules_collection() -> Collection:
    """Get routing_rules collection"""
    db = get_database()
    return db.routing_rules


def get_applicable_routing_rules(bug: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get routing rules applicable to a bug
    
    Args:
        bug: Bug input dictionary
    
    Returns:
        List of applicable routing rule documents
    """
    collection = get_routing_rules_collection()
    
    language = bug.get("language", "")
    code_context = bug.get("code_context", {})
    file_path = code_context.get("file_path", "")
    metadata = bug.get("metadata", {})
    tags = metadata.get("tags", [])
    
    # Build query
    query = {"$or": []}
    
    # Check language conditions
    if language:
        query["$or"].append({"conditions.languages": {"$in": [language]}})
    
    # Check tag conditions
    if tags:
        query["$or"].append({"conditions.tags": {"$in": tags}})
    
    # Check module conditions (from file path)
    if file_path:
        if '/auth' in file_path.lower():
            query["$or"].append({"conditions.modules": {"$in": ["auth"]}})
        elif '/api' in file_path.lower():
            query["$or"].append({"conditions.modules": {"$in": ["api"]}})
    
    # If no conditions, return empty
    if not query["$or"]:
        return []
    
    # Get rules sorted by priority (higher first)
    rules = collection.find(query).sort("priority", -1)
    
    result = []
    for rule in rules:
        rule["_id"] = str(rule["_id"])
        result.append(rule)
    
    return result



