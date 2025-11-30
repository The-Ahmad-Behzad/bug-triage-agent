"""Team profile loading and merging utilities"""

from typing import List, Dict, Any
import logging

from src.database.team_members import get_team_member, get_all_team_members

logger = logging.getLogger("bug_triage_agent")


def load_and_merge_profiles(
    input_profiles: List[Dict[str, Any]],
    use_database: bool = True
) -> List[Dict[str, Any]]:
    """
    Load team profiles from input and merge with database data
    
    Args:
        input_profiles: List of team profiles from input
        use_database: Whether to merge with database data
    
    Returns:
        List of merged team profile dictionaries
    """
    merged_profiles = []
    
    # Get all database profiles if using database
    db_profiles_map = {}
    if use_database:
        try:
            db_profiles = get_all_team_members()
            db_profiles_map = {profile["member_id"]: profile for profile in db_profiles}
        except Exception as e:
            logger.warning(f"Could not load database profiles: {e}. Continuing without database.")
            # Continue without database - use input profiles only
    
    for input_profile in input_profiles:
        # Convert Pydantic model to dict if needed
        if hasattr(input_profile, 'model_dump'):
            input_profile = input_profile.model_dump()
        elif hasattr(input_profile, 'dict'):
            input_profile = input_profile.dict()
        
        member_id = input_profile.get("member_id")
        
        if not member_id:
            logger.warning("Skipping profile without member_id")
            continue
        
        # Start with input profile
        merged_profile = input_profile.copy()
        
        # Merge with database profile if available
        if use_database and member_id in db_profiles_map:
            db_profile = db_profiles_map[member_id]
            
            # Merge skills (prefer database if structured, otherwise combine)
            if "skills" in db_profile:
                db_skills = db_profile["skills"]
                input_skills = input_profile.get("skills", {})
                
                if isinstance(db_skills, dict) and isinstance(input_skills, dict):
                    # Merge structured skills
                    merged_skills = {
                        "languages": list(set(
                            (db_skills.get("languages", []) or []) +
                            (input_skills.get("languages", []) or [])
                        )),
                        "frameworks": list(set(
                            (db_skills.get("frameworks", []) or []) +
                            (input_skills.get("frameworks", []) or [])
                        )),
                        "domains": list(set(
                            (db_skills.get("domains", []) or []) +
                            (input_skills.get("domains", []) or [])
                        ))
                    }
                    merged_profile["skills"] = merged_skills
                elif isinstance(input_skills, list):
                    # Input is legacy array format
                    merged_profile["skills"] = db_skills if isinstance(db_skills, dict) else input_skills
            
            # Merge modules_owned
            db_modules = set(db_profile.get("modules_owned", []) or [])
            input_modules = set(input_profile.get("modules_owned", []) or [])
            merged_profile["modules_owned"] = list(db_modules.union(input_modules))
            
            # Use database values for fields not in input
            if "email" not in merged_profile and "email" in db_profile:
                merged_profile["email"] = db_profile["email"]
            if "primary_stack" not in merged_profile and "primary_stack" in db_profile:
                merged_profile["primary_stack"] = db_profile["primary_stack"]
            if "experience_years" not in merged_profile and "experience_years" in db_profile:
                merged_profile["experience_years"] = db_profile["experience_years"]
            
            # Merge workload (prefer database for current_load if available)
            if "current_load" not in merged_profile:
                db_workload = db_profile.get("workload", {})
                if db_workload:
                    merged_profile["current_load"] = db_workload.get("open_assigned_bugs", 0)
        
        merged_profiles.append(merged_profile)
    
    return merged_profiles

