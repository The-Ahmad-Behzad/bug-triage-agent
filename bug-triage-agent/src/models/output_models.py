"""Output schema models for Bug Triage Agent"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Classification(BaseModel):
    """Classification object"""
    category: str = Field(..., description="High-level category (e.g., Runtime Error, Security, Performance)")
    type: str = Field(..., description="Specific type (e.g., NullPointerException, SQL Injection)")
    root_cause: Optional[str] = Field(None, description="AI-detected root cause")


class Priority(BaseModel):
    """Priority object"""
    level: str = Field(..., description="Priority level")
    justification: str = Field(..., description="Explanation for priority level")

    @field_validator('level')
    @classmethod
    def validate_level(cls, v):
        """Validate priority level"""
        valid_levels = ["critical", "high", "medium", "low"]
        if v not in valid_levels:
            raise ValueError(f"level must be one of: {', '.join(valid_levels)}")
        return v


class Assignment(BaseModel):
    """Assignment object"""
    assigned_to_member_id: str = Field(..., description="ID from team_profiles")
    assigned_to_name: str = Field(..., description="Name from team_profiles")
    confidence: float = Field(..., description="Confidence score (0.0 to 1.0)")

    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v):
        """Validate confidence is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        return v


class SuggestedFix(BaseModel):
    """Suggested fix object"""
    approach: str = Field(..., description="Description of suggested fix")
    estimated_effort: str = Field(..., description="Time estimate (e.g., '2-4 hours', '1 day')")


class ConfidenceScores(BaseModel):
    """Confidence scores object"""
    classification_confidence: float = Field(..., description="Classification confidence (0.0 to 1.0)")
    priority_confidence: float = Field(..., description="Priority confidence (0.0 to 1.0)")
    assignee_confidence: float = Field(..., description="Assignee confidence (0.0 to 1.0)")
    overall_confidence: float = Field(..., description="Overall confidence (0.0 to 1.0)")

    @field_validator('*', mode='before')
    @classmethod
    def validate_all_confidence(cls, v):
        """Validate all confidence scores are between 0.0 and 1.0"""
        if isinstance(v, (int, float)):
            if not 0.0 <= float(v) <= 1.0:
                raise ValueError("All confidence scores must be between 0.0 and 1.0")
        return v


class TriageResult(BaseModel):
    """Triage result object"""
    bug_id: str = Field(..., description="Matches input bug_id")
    classification: Classification = Field(..., description="Bug classification")
    priority: Priority = Field(..., description="Priority assessment")
    assignment: Assignment = Field(..., description="Team member assignment")
    suggested_fix: Optional[SuggestedFix] = Field(None, description="Fix recommendation")
    confidence_scores: ConfidenceScores = Field(..., description="Detailed confidence metrics")


class TriageResponse(BaseModel):
    """Triage response structure"""
    triage: list[TriageResult] = Field(..., description="Array of triage results, one per input bug")


class HandshakeResponse(BaseModel):
    """Handshake response structure"""
    message_id: str = Field(..., description="Unique identifier for the response")
    sender: str = Field(default="bug_triage_agent", description="Always 'bug_triage_agent'")
    recipient: str = Field(default="supervisor", description="Always 'supervisor'")
    type: str = Field(default="task_response", description="Message type")
    related_message_id: Optional[str] = Field(None, description="Reference to original task message")
    status: str = Field(..., description="Status: completed, failed, or in_progress")
    timestamp: str = Field(..., description="ISO8601 timestamp")
    results: TriageResponse = Field(..., description="Triage results")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """Validate status"""
        valid_statuses = ["completed", "failed", "in_progress"]
        if v not in valid_statuses:
            raise ValueError(f"status must be one of: {', '.join(valid_statuses)}")
        return v

