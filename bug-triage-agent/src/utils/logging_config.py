"""Logging configuration setup"""

import logging
import logging.config
import os
from pathlib import Path

import yaml


def setup_logging(
    default_path: str = "config/logging.yaml",
    default_level: int = logging.INFO,
    env_key: str = "LOG_LEVEL"
) -> logging.Logger:
    """
    Setup logging configuration from YAML file or environment variable
    
    Args:
        default_path: Path to logging configuration YAML file
        default_level: Default logging level
        env_key: Environment variable key for log level
    
    Returns:
        Configured logger instance
    """
    path = default_path
    value = os.getenv(env_key, None)
    level = logging.getLevelName(value) if value else default_level
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(f"Error loading logging config: {e}")
                logging.basicConfig(level=level)
    else:
        logging.basicConfig(level=level)
    
    logger = logging.getLogger("bug_triage_agent")
    logger.info("Logging configured successfully")
    return logger



