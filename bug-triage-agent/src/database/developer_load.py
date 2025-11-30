"""Developer load database operations"""

from typing import Dict, Any, Optional
from datetime import datetime
from pymongo.collection import Collection
import logging

from src.database.connection import get_database

logger = logging.getLogger("bug_triage_agent")


def get_developer_load_collection() -> Collection:
    """Get developer_load collection"""
    db = get_database()
    return db.developer_load


def get_developer_load(member_id: str) -> Optional[Dict[str, Any]]:
    """
    Get developer load information
    
    Args:
        member_id: Team member ID
    
    Returns:
        Developer load document or None if not found
    """
    collection = get_developer_load_collection()
    
    load_doc = collection.find_one({"member_id": member_id})
    
    if load_doc:
        load_doc["_id"] = str(load_doc["_id"])
        return load_doc
    
    return None


def update_developer_load(member_id: str, load_data: Dict[str, Any]) -> bool:
    """
    Update developer load information
    
    Args:
        member_id: Team member ID
        load_data: Load data dictionary
    
    Returns:
        True if updated, False if not found
    """
    collection = get_developer_load_collection()
    
    load_data["updated_at"] = datetime.utcnow()
    
    result = collection.update_one(
        {"member_id": member_id},
        {"$set": load_data},
        upsert=True  # Create if doesn't exist
    )
    
    if result.modified_count > 0 or result.upserted_id:
        logger.info(f"Updated developer load: {member_id}")
        return True
    
    return False


def get_all_developer_loads() -> Dict[str, Dict[str, Any]]:
    """
    Get all developer load information
    
    Returns:
        Dictionary mapping member_id to load data
    """
    collection = get_developer_load_collection()
    
    loads = collection.find({})
    
    result = {}
    for load in loads:
        member_id = load["member_id"]
        load["_id"] = str(load["_id"])
        result[member_id] = load
    
    return result



