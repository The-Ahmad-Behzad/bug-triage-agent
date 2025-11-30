"""Application startup tasks"""

import logging
from src.database.init import initialize_database

logger = logging.getLogger("bug_triage_agent")


def startup_tasks():
    """Run startup tasks"""
    logger.info("Running startup tasks...")
    
    # Initialize database
    try:
        if initialize_database():
            logger.info("Database initialized successfully")
        else:
            logger.warning("Database initialization completed with warnings")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # Continue anyway - database might be available later
    
    logger.info("Startup tasks completed")



