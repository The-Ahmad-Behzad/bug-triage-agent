"""Validation utilities for input and output"""

from typing import Tuple, Dict, Any, List
from src.models.input_models import HandshakeMessage, BugInput, TeamProfile
from src.models.output_models import HandshakeResponse
from src.utils.language_detector import detect_and_validate_language_file_type, validate_language_file_type_consistency


def validate_input(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate input data structure
    
    Args:
        data: Input data dictionary
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Validate handshake message structure
        message = HandshakeMessage(**data)
        
        # Validate task if present
        if message.task:
            # Validate bugs
            for bug in message.task.bugs:
                # Auto-detect language/file_type if not provided
                if bug.code_context and bug.code_context.file_path:
                    detected_lang, detected_type = detect_and_validate_language_file_type(
                        file_path=bug.code_context.file_path,
                        language=bug.language,
                        file_type=bug.file_type
                    )
                    # Update bug with detected values if not provided
                    if not bug.language and detected_lang:
                        bug.language = detected_lang
                    if not bug.file_type and detected_type:
                        bug.file_type = detected_type
                
                # Validate language/file_type consistency if both provided
                if bug.language and bug.file_type:
                    if not validate_language_file_type_consistency(bug.language, bug.file_type):
                        return False, f"Language '{bug.language}' and file_type '{bug.file_type}' are inconsistent for bug {bug.bug_id}"
        
        return True, ""
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_output(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate output data structure
    
    Args:
        data: Output data dictionary
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Validate handshake response structure
        response = HandshakeResponse(**data)
        
        # Additional validations
        if response.status == "completed" and not response.results.triage:
            return False, "Status is 'completed' but no triage results provided"
        
        return True, ""
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_bug_object(bug: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate individual bug object
    
    Args:
        bug: Bug object dictionary
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        bug_obj = BugInput(**bug)
        
        # Check required fields
        if not bug_obj.bug_id:
            return False, "bug_id is required"
        if not bug_obj.title:
            return False, "title is required"
        if not bug_obj.description:
            return False, "description is required"
        
        # Validate code_context if provided
        if bug_obj.code_context and not bug_obj.code_context.file_path:
            return False, "code_context.file_path is required if code_context is provided"
        
        return True, ""
    
    except Exception as e:
        return False, f"Bug validation error: {str(e)}"


def validate_team_profiles(profiles: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Validate team profiles array
    
    Args:
        profiles: List of team profile dictionaries
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not profiles:
        return False, "team_profiles array cannot be empty"
    
    try:
        for profile in profiles:
            team_profile = TeamProfile(**profile)
            
            # Check required fields
            if not team_profile.member_id:
                return False, "member_id is required for all team profiles"
            if not team_profile.name:
                return False, "name is required for all team profiles"
        
        return True, ""
    
    except Exception as e:
        return False, f"Team profile validation error: {str(e)}"



