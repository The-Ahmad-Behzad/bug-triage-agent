"""Input schema models for Bug Triage Agent"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CodeContext(BaseModel):
    """Code context object"""
    file_path: str = Field(..., description="Path to source file")
    line_start: Optional[int] = Field(None, description="Starting line number")
    line_end: Optional[int] = Field(None, description="Ending line number")
    snippet: Optional[str] = Field(None, description="Code snippet")


class Metadata(BaseModel):
    """Metadata object"""
    reported_by: Optional[str] = Field(None, description="Username of reporter")
    environment: Optional[str] = Field(None, description="Environment (dev/staging/production)")
    tags: Optional[List[str]] = Field(None, description="Array of tag strings")


class BugInput(BaseModel):
    """Bug input object"""
    bug_id: str = Field(..., description="Unique identifier for the bug")
    title: str = Field(..., description="Short description of the bug")
    description: str = Field(..., description="Detailed description")
    steps_to_reproduce: Optional[List[str]] = Field(None, description="List of reproduction steps")
    stack_trace: Optional[str] = Field(None, description="Error stack trace")
    logs: Optional[str] = Field(None, description="Relevant log entries")
    code_context: Optional[CodeContext] = Field(None, description="Code snippet and location")
    language: Optional[str] = Field(None, description="Programming language (e.g., java, python, javascript)")
    file_type: Optional[str] = Field(None, description="File extension (e.g., .java, .py, .js)")
    metadata: Optional[Metadata] = Field(None, description="Additional metadata")

    @field_validator('language', 'file_type', mode='before')
    @classmethod
    def validate_language_file_type(cls, v):
        """Validate language and file_type consistency"""
        return v


class Skills(BaseModel):
    """Structured skills object"""
    languages: Optional[List[str]] = Field(None, description="Array of programming languages")
    frameworks: Optional[List[str]] = Field(None, description="Array of frameworks")
    domains: Optional[List[str]] = Field(None, description="Array of domain expertise")


class TeamProfile(BaseModel):
    """Team profile object"""
    member_id: str = Field(..., description="Unique identifier for team member")
    name: str = Field(..., description="Full name")
    skills: Optional[Any] = Field(None, description="Skills - can be structured object or array")
    modules_owned: Optional[List[str]] = Field(None, description="Array of module names owned")
    current_load: Optional[int] = Field(None, description="Current number of assigned tasks")

    @field_validator('skills', mode='before')
    @classmethod
    def validate_skills(cls, v):
        """Handle both structured skills object and legacy array format"""
        if isinstance(v, dict):
            return Skills(**v)
        elif isinstance(v, list):
            # Legacy format - convert to structured format
            return Skills(languages=v, frameworks=[], domains=[])
        return v


class TaskAssignment(BaseModel):
    """Task assignment object"""
    bugs: List[BugInput] = Field(..., description="Array of bug objects to triage")
    team_profiles: List[TeamProfile] = Field(..., description="Array of team member profiles")

    @field_validator('bugs')
    @classmethod
    def validate_bugs_not_empty(cls, v):
        """Ensure bugs array is not empty"""
        if not v:
            raise ValueError("bugs array cannot be empty")
        return v

    @field_validator('team_profiles')
    @classmethod
    def validate_team_profiles_not_empty(cls, v):
        """Ensure team_profiles array is not empty"""
        if not v:
            raise ValueError("team_profiles array cannot be empty")
        return v


class HandshakeMessage(BaseModel):
    """Handshake message structure"""
    message_id: str = Field(..., description="Unique identifier for the message")
    sender: str = Field(..., description="Sender identifier")
    recipient: str = Field(..., description="Recipient identifier")
    type: str = Field(..., description="Message type (task_assignment or task_response)")
    related_message_id: Optional[str] = Field(None, description="Reference to related message")
    timestamp: str = Field(..., description="ISO8601 timestamp")
    task: Optional[TaskAssignment] = Field(None, description="Task assignment data")

    @field_validator('sender')
    @classmethod
    def validate_sender(cls, v):
        """Validate sender is supervisor for task assignments"""
        if v != "supervisor":
            raise ValueError("sender must be 'supervisor' for task assignments")
        return v

    @field_validator('recipient')
    @classmethod
    def validate_recipient(cls, v):
        """Validate recipient is bug_triage_agent"""
        if v != "bug_triage_agent":
            raise ValueError("recipient must be 'bug_triage_agent'")
        return v

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        """Validate message type"""
        if v not in ["task_assignment", "task_response"]:
            raise ValueError("type must be 'task_assignment' or 'task_response'")
        return v

