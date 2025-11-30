"""Bug triage request handler"""

from typing import Dict, Any, List
import logging
from datetime import datetime, UTC
import time
import uuid

from src.models.input_models import HandshakeMessage
from src.models.output_models import HandshakeResponse, TriageResult, Classification, Priority, Assignment, SuggestedFix, ConfidenceScores
from src.utils.validators import validate_input
from src.utils.team_profile_loader import load_and_merge_profiles
from src.utils.language_detector import detect_and_validate_language_file_type
from src.utils.metrics import metrics_collector
from src.engines.classification import classify_bug
from src.engines.priority import assess_priority
from src.engines.assignment import assign_bug
from src.engines.fix_suggestion import suggest_fix
from src.database.severity_priority_rules import get_all_priority_rules
from src.database.routing_rules import get_applicable_routing_rules
from src.database.triage_history import save_triage_history

logger = logging.getLogger("bug_triage_agent")


def process_triage_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process bug triage request
    
    Args:
        request_data: Request data dictionary
    
    Returns:
        Response dictionary
    """
    start_time = time.perf_counter()
    bug_count = len(request_data.get("task", {}).get("bugs", [])) if isinstance(request_data, dict) else 0
    try:
        # Validate input
        is_valid, error = validate_input(request_data)
        if not is_valid:
            response = create_error_response(request_data.get("message_id", ""), error)
            metrics_collector.record_request(time.perf_counter() - start_time, bug_count, "failed_validation")
            return response
        
        # Parse handshake message
        message = HandshakeMessage(**request_data)
        
        if not message.task:
            response = create_error_response(message.message_id, "Task data is required")
            metrics_collector.record_request(time.perf_counter() - start_time, bug_count, "failed_validation")
            return response
        
        bug_count = len(message.task.bugs)
        
        # Convert team profiles to dicts for processing
        team_profiles_dicts = []
        for profile in message.task.team_profiles:
            if hasattr(profile, 'model_dump'):
                team_profiles_dicts.append(profile.model_dump())
            elif hasattr(profile, 'dict'):
                team_profiles_dicts.append(profile.dict())
            else:
                team_profiles_dicts.append(profile)
        
        # Load and merge team profiles (try database, fallback to input only)
        try:
            team_profiles = load_and_merge_profiles(team_profiles_dicts, use_database=True)
        except Exception as e:
            logger.warning(f"Database unavailable: {e}. Using input team profiles only.")
            team_profiles = load_and_merge_profiles(team_profiles_dicts, use_database=False)
        
        # Get severity rules from database
        try:
            severity_rules = get_all_priority_rules()
        except Exception as e:
            logger.warning(f"Could not load severity rules: {e}. Continuing without rules.")
            severity_rules = []
        
        # Process each bug
        triage_results = []
        warnings = []  # Collect warnings for missing optional fields
        
        for bug_input in message.task.bugs:
            # Check for missing optional fields and log warnings
            missing_fields = []
            if not bug_input.steps_to_reproduce:
                missing_fields.append("steps_to_reproduce")
            if not bug_input.stack_trace:
                missing_fields.append("stack_trace")
            if not bug_input.logs:
                missing_fields.append("logs")
            if not bug_input.code_context:
                missing_fields.append("code_context")
            elif bug_input.code_context and not bug_input.code_context.snippet:
                missing_fields.append("code_context.snippet")
            
            if missing_fields:
                warning_msg = f"Bug {bug_input.bug_id}: Missing optional fields: {', '.join(missing_fields)}. Output may be less accurate."
                warnings.append(warning_msg)
                logger.info(warning_msg)
            
            # Auto-detect language/file_type if not provided
            if bug_input.code_context and bug_input.code_context.file_path:
                detected_lang, detected_type = detect_and_validate_language_file_type(
                    file_path=bug_input.code_context.file_path,
                    language=bug_input.language,
                    file_type=bug_input.file_type
                )
                if not bug_input.language and detected_lang:
                    bug_input.language = detected_lang
                    logger.info(f"Auto-detected language '{detected_lang}' for bug {bug_input.bug_id}")
                if not bug_input.file_type and detected_type:
                    bug_input.file_type = detected_type
                    logger.info(f"Auto-detected file_type '{detected_type}' for bug {bug_input.bug_id}")
            
            # Convert to dict for processing
            if hasattr(bug_input, 'model_dump'):
                bug_dict = bug_input.model_dump()
            else:
                bug_dict = bug_input.dict() if hasattr(bug_input, 'dict') else bug_input
            code_context_dict = bug_dict.get("code_context")
            
            # Classify bug
            classification_result = classify_bug(bug_dict, code_context_dict)
            
            # Assess priority
            priority_result = assess_priority(bug_dict, classification_result, severity_rules)
            
            # Assign bug
            assignment_result = assign_bug(bug_dict, team_profiles)
            
            # Suggest fix
            fix_result = suggest_fix(bug_dict, classification_result, code_context_dict)
            
            # Calculate overall confidence
            overall_confidence = (
                classification_result.get("confidence", 0.5) +
                priority_result.get("confidence", 0.5) +
                assignment_result.get("confidence", 0.5)
            ) / 3.0
            
            # Create triage result
            triage_result = TriageResult(
                bug_id=bug_input.bug_id,
                classification=Classification(
                    category=classification_result["category"],
                    type=classification_result["type"],
                    root_cause=classification_result.get("root_cause")
                ),
                priority=Priority(
                    level=priority_result["level"],
                    justification=priority_result["justification"]
                ),
                assignment=Assignment(
                    assigned_to_member_id=assignment_result["assigned_to_member_id"],
                    assigned_to_name=assignment_result["assigned_to_name"],
                    confidence=assignment_result["confidence"]
                ),
                suggested_fix=SuggestedFix(
                    approach=fix_result["approach"],
                    estimated_effort=fix_result["estimated_effort"]
                ),
                confidence_scores=ConfidenceScores(
                    classification_confidence=classification_result.get("confidence", 0.5),
                    priority_confidence=priority_result.get("confidence", 0.5),
                    assignee_confidence=assignment_result.get("confidence", 0.5),
                    overall_confidence=overall_confidence
                )
            )
            
            triage_results.append(triage_result)
            
            # Save to triage history
            try:
                save_triage_history(bug_dict, classification_result, priority_result, assignment_result, fix_result)
            except Exception as e:
                logger.warning(f"Could not save triage history: {e}")
        
        # Create response
        response_dict = {
            "message_id": str(uuid.uuid4()),
            "sender": "bug_triage_agent",
            "recipient": "supervisor",
            "type": "task_response",
            "related_message_id": message.message_id,
            "status": "completed",
            "timestamp": datetime.now(UTC).isoformat(),
            "results": {"triage": [result.model_dump() if hasattr(result, 'model_dump') else result.dict() for result in triage_results]}
        }
        
        # Add warnings if any
        if warnings:
            response_dict["warnings"] = warnings
        
        response = HandshakeResponse(**response_dict)
        metrics_collector.record_request(time.perf_counter() - start_time, bug_count, "completed", warnings_count=len(warnings))
        return response.model_dump() if hasattr(response, 'model_dump') else response.dict()
    
    except Exception as e:
        logger.error(f"Error processing triage request: {e}", exc_info=True)
        metrics_collector.record_request(time.perf_counter() - start_time, bug_count, "error")
        return create_error_response(
            request_data.get("message_id", ""),
            f"Internal error: {str(e)}"
        )


def create_error_response(message_id: str, error: str) -> Dict[str, Any]:
    """
    Create error response
    
    Args:
        message_id: Original message ID
        error: Error message
    
    Returns:
        Error response dictionary
    """
    return {
        "message_id": str(uuid.uuid4()),
        "sender": "bug_triage_agent",
        "recipient": "supervisor",
        "type": "task_response",
        "related_message_id": message_id,
        "status": "failed",
        "timestamp": datetime.now(UTC).isoformat(),
        "error": error
    }

