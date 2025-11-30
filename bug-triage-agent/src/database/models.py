"""MongoDB collection models and schemas"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId


# Collection: team_members
class TeamMember(BaseModel):
    """Team member document model"""
    id: Optional[str] = Field(default=None, alias="_id")
    member_id: str
    name: str
    email: Optional[str] = None
    skills: Dict[str, List[str]] = Field(default_factory=dict)  # {languages: [], frameworks: [], domains: []}
    modules_owned: List[str] = Field(default_factory=list)
    primary_stack: Optional[str] = None
    experience_years: Optional[int] = None
    past_bugs_fixed: Optional[int] = 0
    workload: Dict[str, Any] = Field(default_factory=dict)  # {open_assigned_bugs: 0, current_sprint_tasks: 0, availability_score: 1.0}
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)
    preferences: Dict[str, bool] = Field(default_factory=dict)
    last_active: Optional[datetime] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


# Collection: module_ownership
class ModuleOwnership(BaseModel):
    """Module ownership document model"""
    id: Optional[str] = Field(default=None, alias="_id")
    module_name: str
    owners: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)
    primary_language: Optional[str] = None
    risk_level: Optional[str] = None
    recent_bugs: Optional[int] = 0
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


# Collection: historical_bugs
class HistoricalBug(BaseModel):
    """Historical bug document model"""
    id: Optional[str] = Field(default=None, alias="_id")
    bug_id: str
    title: str
    description: str
    category: Optional[str] = None
    type: Optional[str] = None
    root_cause: Optional[str] = None
    module: Optional[str] = None
    language: Optional[str] = None
    file_type: Optional[str] = None
    resolved_by: Optional[str] = None
    resolution_time_hours: Optional[float] = None
    date_resolved: Optional[datetime] = None
    input_signature: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


# Collection: severity_priority_rules
class SeverityPriorityRule(BaseModel):
    """Severity priority rule document model"""
    id: Optional[str] = Field(default=None, alias="_id")
    severity: str
    priority: str
    conditions: List[str] = Field(default_factory=list)
    auto_assign: Optional[bool] = False
    language_specific: Optional[bool] = False
    languages: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


# Collection: developer_load
class DeveloperLoad(BaseModel):
    """Developer load document model"""
    id: Optional[str] = Field(default=None, alias="_id")
    member_id: str
    current_load_score: float = Field(default=0.0, ge=0.0, le=1.0)
    recent_activity: Optional[str] = "active"
    focus_area: List[str] = Field(default_factory=list)
    active_languages: List[str] = Field(default_factory=list)
    burnout_risk_estimate: float = Field(default=0.0, ge=0.0, le=1.0)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


# Collection: embeddings (simplified for now)
class Embedding(BaseModel):
    """Embedding document model"""
    id: Optional[str] = Field(default=None, alias="_id")
    bug_id: str
    vector: List[float] = Field(default_factory=list)
    model: Optional[str] = None
    text_content: Optional[str] = None
    last_trained: Optional[datetime] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


# Collection: routing_rules
class RoutingRule(BaseModel):
    """Routing rule document model"""
    id: Optional[str] = Field(default=None, alias="_id")
    rule_type: str
    assign_to: List[str] = Field(default_factory=list)
    auto_escalate: Optional[bool] = False
    conditions: Dict[str, Any] = Field(default_factory=dict)
    priority: Optional[int] = 0
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


# Collection: triage_history
class TriageHistory(BaseModel):
    """Triage history document model"""
    id: Optional[str] = Field(default=None, alias="_id")
    bug_id: str
    language: Optional[str] = None
    file_type: Optional[str] = None
    classification: Dict[str, Any] = Field(default_factory=dict)
    priority: Dict[str, Any] = Field(default_factory=dict)
    assignment: Dict[str, Any] = Field(default_factory=dict)
    suggested_fix: Optional[Dict[str, Any]] = None
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    raw_input: Optional[Dict[str, Any]] = None
    raw_output: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    feedback: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

