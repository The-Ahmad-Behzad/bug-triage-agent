"""Module ownership database operations"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pymongo.collection import Collection
import logging

from src.database.connection import get_database
from src.database.models import ModuleOwnership

logger = logging.getLogger("bug_triage_agent")


def get_module_ownership_collection() -> Collection:
    """Get module_ownership collection"""
    db = get_database()
    return db.module_ownership


def get_module_owners(module: str) -> List[str]:
    """
    Get list of owner member_ids for a module
    
    Args:
        module: Module name
    
    Returns:
        List of member_ids
    """
    collection = get_module_ownership_collection()
    
    module_doc = collection.find_one({"module_name": module})
    
    if module_doc:
        return module_doc.get("owners", [])
    
    return []


def get_modules_by_language(language: str) -> List[str]:
    """
    Get list of modules that use a specific language
    
    Args:
        language: Programming language
    
    Returns:
        List of module names
    """
    collection = get_module_ownership_collection()
    
    modules = collection.find({
        "$or": [
            {"primary_language": language.lower()},
            {"tech_stack": {"$in": [language.lower()]}}
        ]
    })
    
    return [module["module_name"] for module in modules]


def get_module_info(module: str) -> Optional[Dict[str, Any]]:
    """
    Get full module information
    
    Args:
        module: Module name
    
    Returns:
        Module document or None if not found
    """
    collection = get_module_ownership_collection()
    
    module_doc = collection.find_one({"module_name": module})
    
    if module_doc:
        module_doc["_id"] = str(module_doc["_id"])
        return module_doc
    
    return None


def create_or_update_module(module_data: Dict[str, Any]) -> str:
    """
    Create or update module ownership
    
    Args:
        module_data: Module data dictionary
    
    Returns:
        Module name
    """
    collection = get_module_ownership_collection()
    
    module_name = module_data["module_name"]
    
    # Check if exists
    existing = collection.find_one({"module_name": module_name})
    
    if existing:
        # Update
        module_data["updated_at"] = datetime.utcnow()
        collection.update_one(
            {"module_name": module_name},
            {"$set": module_data}
        )
        logger.info(f"Updated module: {module_name}")
    else:
        # Create
        module_data["created_at"] = datetime.utcnow()
        module_data["updated_at"] = datetime.utcnow()
        collection.insert_one(module_data)
        logger.info(f"Created module: {module_name}")
    
    return module_name



