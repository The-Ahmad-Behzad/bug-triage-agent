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
    # In serverless environments (like Vercel), filesystem is read-only
    # So we gracefully skip file logging setup
    logs_dir = Path("logs")
    try:
        logs_dir.mkdir(exist_ok=True)
    except (OSError, PermissionError) as e:
        # Serverless environment - filesystem is read-only
        # Logs will go to console/stdout which Vercel captures
        pass
    
    # Check if we're in a serverless environment (Vercel, AWS Lambda, etc.)
    is_serverless = (
        os.getenv("VERCEL") is not None or 
        os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None or
        os.getenv("LAMBDA_TASK_ROOT") is not None
    )
    
    if os.path.exists(path) and not is_serverless:
        # Only use YAML config in non-serverless environments
        # Serverless environments should use console logging only
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(f"Error loading logging config: {e}")
                logging.basicConfig(level=level)
    else:
        # Use basic console logging for serverless or if config file doesn't exist
        if is_serverless:
            # In serverless, use console-only logging (Vercel captures stdout/stderr)
            logging.basicConfig(
                level=level,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[logging.StreamHandler()]
            )
        else:
            logging.basicConfig(level=level)
    
    logger = logging.getLogger("bug_triage_agent")
    logger.info("Logging configured successfully")
    return logger



