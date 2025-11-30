"""Team member database operations"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pymongo.database import Database
from pymongo.collection import Collection
import logging

from src.database.connection import get_database
from src.database.models import TeamMember

logger = logging.getLogger("bug_triage_agent")


def get_team_members_collection() -> Collection:
    """Get team_members collection"""
    db = get_database()
    return db.team_members


def create_team_member(member_data: Dict[str, Any]) -> str:
    """
    Create a new team member
    
    Args:
        member_data: Team member data dictionary
    
    Returns:
        Created member_id
    """
    collection = get_team_members_collection()
    
    # Ensure member_id is unique
    if collection.find_one({"member_id": member_data["member_id"]}):
        raise ValueError(f"Team member with member_id '{member_data['member_id']}' already exists")
    
    # Add timestamps
    member_data["created_at"] = datetime.utcnow()
    member_data["updated_at"] = datetime.utcnow()
    
    # Insert document
    result = collection.insert_one(member_data)
    logger.info(f"Created team member: {member_data['member_id']}")
    return member_data["member_id"]


def get_team_member(member_id: str) -> Optional[Dict[str, Any]]:
    """
    Get team member by member_id
    
    Args:
        member_id: Team member ID
    
    Returns:
        Team member document or None if not found
    """
    collection = get_team_members_collection()
    member = collection.find_one({"member_id": member_id})
    
    if member:
        member["_id"] = str(member["_id"])  # Convert ObjectId to string
    
    return member


def update_team_member(member_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update team member
    
    Args:
        member_id: Team member ID
        updates: Dictionary of fields to update
    
    Returns:
        True if updated, False if not found
    """
    collection = get_team_members_collection()
    
    # Add updated_at timestamp
    updates["updated_at"] = datetime.utcnow()
    
    result = collection.update_one(
        {"member_id": member_id},
        {"$set": updates}
    )
    
    if result.modified_count > 0:
        logger.info(f"Updated team member: {member_id}")
        return True
    
    return False


def query_by_language(language: str) -> List[Dict[str, Any]]:
    """
    Query team members by programming language
    
    Args:
        language: Programming language name
    
    Returns:
        List of team member documents
    """
    collection = get_team_members_collection()
    
    # Query by skills.languages array
    members = collection.find({
        "skills.languages": {"$in": [language.lower()]}
    })
    
    result = []
    for member in members:
        member["_id"] = str(member["_id"])
        result.append(member)
    
    return result


def query_by_skills(skills: List[str]) -> List[Dict[str, Any]]:
    """
    Query team members by skills
    
    Args:
        skills: List of skill strings
    
    Returns:
        List of team member documents
    """
    collection = get_team_members_collection()
    
    # Query across languages, frameworks, and domains
    query = {
        "$or": [
            {"skills.languages": {"$in": skills}},
            {"skills.frameworks": {"$in": skills}},
            {"skills.domains": {"$in": skills}}
        ]
    }
    
    members = collection.find(query)
    
    result = []
    for member in members:
        member["_id"] = str(member["_id"])
        result.append(member)
    
    return result


def query_by_module(module: str) -> List[Dict[str, Any]]:
    """
    Query team members by module ownership
    
    Args:
        module: Module name
    
    Returns:
        List of team member documents
    """
    collection = get_team_members_collection()
    
    members = collection.find({
        "modules_owned": {"$in": [module]}
    })
    
    result = []
    for member in members:
        member["_id"] = str(member["_id"])
        result.append(member)
    
    return result


def get_all_team_members() -> List[Dict[str, Any]]:
    """
    Get all team members
    
    Returns:
        List of all team member documents
    """
    collection = get_team_members_collection()
    
    members = collection.find({})
    
    result = []
    for member in members:
        member["_id"] = str(member["_id"])
        result.append(member)
    
    return result



