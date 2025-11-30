"""Triage history database operations"""

from typing import Dict, Any
from datetime import datetime, UTC
from pymongo.collection import Collection
import logging

from src.database.connection import get_database

logger = logging.getLogger("bug_triage_agent")


def get_triage_history_collection() -> Collection:
    """Get triage_history collection"""
    db = get_database()
    return db.triage_history


def save_triage_history(
    bug: Dict[str, Any],
    classification: Dict[str, Any],
    priority: Dict[str, Any],
    assignment: Dict[str, Any],
    fix_suggestion: Dict[str, Any]
) -> bool:
    """
    Save triage decision to history
    
    Args:
        bug: Bug input dictionary
        classification: Classification result
        priority: Priority result
        assignment: Assignment result
        fix_suggestion: Fix suggestion result
    
    Returns:
        True if saved successfully
    """
    try:
        collection = get_triage_history_collection()
        
        history_doc = {
            "bug_id": bug.get("bug_id", "unknown"),
            "language": bug.get("language"),
            "file_type": bug.get("file_type"),
            "classification": {
                "category": classification.get("category"),
                "type": classification.get("type"),
                "root_cause": classification.get("root_cause")
            },
            "priority": {
                "level": priority.get("level"),
                "justification": priority.get("justification")
            },
            "assignment": {
                "member_id": assignment.get("assigned_to_member_id"),
                "name": assignment.get("assigned_to_name"),
                "confidence": assignment.get("confidence")
            },
            "suggested_fix": {
                "approach": fix_suggestion.get("approach"),
                "estimated_effort": fix_suggestion.get("estimated_effort")
            },
            "confidence_scores": {
                "classification_confidence": classification.get("confidence", 0.5),
                "priority_confidence": priority.get("confidence", 0.5),
                "assignee_confidence": assignment.get("confidence", 0.5)
            },
            "raw_input": bug,
            "timestamp": datetime.now(UTC)
        }
        
        collection.insert_one(history_doc)
        logger.debug(f"Saved triage history for bug: {bug.get('bug_id')}")
        return True
    
    except Exception as e:
        logger.error(f"Error saving triage history: {e}")
        return False



