"""Database initialization"""

import logging
from datetime import datetime
from pymongo.database import Database
from pymongo.collection import Collection

from src.database.connection import get_database

logger = logging.getLogger("bug_triage_agent")


def create_indexes():
    """Create indexes for all collections"""
    db = get_database()
    
    # team_members indexes
    db.team_members.create_index("member_id", unique=True)
    db.team_members.create_index("skills.languages")
    db.team_members.create_index("modules_owned")
    
    # module_ownership indexes
    db.module_ownership.create_index("module_name", unique=True)
    db.module_ownership.create_index("primary_language")
    db.module_ownership.create_index("owners")
    
    # historical_bugs indexes
    db.historical_bugs.create_index("bug_id", unique=True)
    db.historical_bugs.create_index("category")
    db.historical_bugs.create_index("type")
    db.historical_bugs.create_index("language")
    db.historical_bugs.create_index("module")
    db.historical_bugs.create_index("resolved_by")
    
    # severity_priority_rules indexes
    db.severity_priority_rules.create_index("severity")
    db.severity_priority_rules.create_index("language_specific")
    
    # developer_load indexes
    db.developer_load.create_index("member_id", unique=True)
    db.developer_load.create_index("current_load_score")
    db.developer_load.create_index("active_languages")
    
    # embeddings indexes
    db.embeddings.create_index("bug_id", unique=True)
    
    # routing_rules indexes
    db.routing_rules.create_index("rule_type")
    db.routing_rules.create_index("conditions.languages")
    db.routing_rules.create_index("priority")
    
    # triage_history indexes
    db.triage_history.create_index("bug_id")
    db.triage_history.create_index("timestamp")
    db.triage_history.create_index("assignment.member_id")
    db.triage_history.create_index("language")
    db.triage_history.create_index("classification.category")
    
    logger.info("Created all database indexes")


def seed_initial_data():
    """Seed initial data (routing rules, severity rules)"""
    db = get_database()
    
    # Seed severity_priority_rules
    severity_rules = [
        {
            "severity": "crash",
            "priority": "critical",
            "conditions": ["production"],
            "auto_assign": True,
            "language_specific": False,
            "languages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "severity": "security_vulnerability",
            "priority": "critical",
            "conditions": ["public_exploit", "production"],
            "auto_assign": True,
            "language_specific": False,
            "languages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "severity": "data_loss",
            "priority": "critical",
            "conditions": ["production"],
            "auto_assign": True,
            "language_specific": False,
            "languages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    for rule in severity_rules:
        existing = db.severity_priority_rules.find_one({
            "severity": rule["severity"],
            "priority": rule["priority"]
        })
        if not existing:
            db.severity_priority_rules.insert_one(rule)
            logger.info(f"Seeded severity rule: {rule['severity']} -> {rule['priority']}")
    
    logger.info("Seeded initial data")


def initialize_database() -> bool:
    """
    Initialize database: create collections, indexes, and seed data
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("Initializing database...")
        
        # Create indexes
        create_indexes()
        
        # Seed initial data
        seed_initial_data()
        
        logger.info("Database initialization completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False



