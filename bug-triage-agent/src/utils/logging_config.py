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
    # Check if we're in a serverless environment FIRST (before any file operations)
    # Vercel sets: VERCEL=1, VERCEL_ENV, VERCEL_URL
    # AWS Lambda sets: AWS_LAMBDA_FUNCTION_NAME, LAMBDA_TASK_ROOT
    is_serverless = (
        os.getenv("VERCEL") is not None or 
        os.getenv("VERCEL_ENV") is not None or
        os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None or
        os.getenv("LAMBDA_TASK_ROOT") is not None
    )
    
    path = default_path
    value = os.getenv(env_key, None)
    level = logging.getLevelName(value) if value else default_level
    
    if is_serverless:
        # In serverless environments (Vercel, Lambda), filesystem is read-only
        # Use console-only logging - Vercel/Lambda capture stdout/stderr automatically
        logging.basicConfig(
            level=level,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[logging.StreamHandler()],
            force=True  # Override any existing configuration
        )
    else:
        # Local/container environment - can use file logging
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        try:
            logs_dir.mkdir(exist_ok=True)
        except (OSError, PermissionError) as e:
            # If directory creation fails, fall back to console-only logging
            logging.basicConfig(
                level=level,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[logging.StreamHandler()]
            )
            logger = logging.getLogger("bug_triage_agent")
            logger.warning(f"Could not create logs directory, using console logging only: {e}")
            return logger
        
        # Try to load YAML config if it exists
        if os.path.exists(path):
            try:
                with open(path, "rt") as f:
                    config = yaml.safe_load(f.read())
                    # Remove file handlers if logs directory doesn't exist or isn't writable
                    # This prevents errors if the directory was created but isn't writable
                    if config and "handlers" in config:
                        # Check if we can actually write to the logs directory
                        test_file = logs_dir / ".test_write"
                        try:
                            test_file.write_text("test")
                            test_file.unlink()
                        except (OSError, PermissionError):
                            # Can't write to logs directory, remove file handlers from config
                            file_handlers = [k for k, v in config["handlers"].items() 
                                           if v.get("class", "").endswith("FileHandler")]
                            for handler_name in file_handlers:
                                # Remove file handler from all logger configs
                                if "loggers" in config:
                                    for logger_name, logger_config in config["loggers"].items():
                                        if "handlers" in logger_config:
                                            logger_config["handlers"] = [
                                                h for h in logger_config["handlers"] 
                                                if h != handler_name
                                            ]
                                if "root" in config and "handlers" in config["root"]:
                                    config["root"]["handlers"] = [
                                        h for h in config["root"]["handlers"] 
                                        if h != handler_name
                                    ]
                    
                    logging.config.dictConfig(config)
            except Exception as e:
                # If YAML config fails, fall back to basic console logging
                logging.basicConfig(
                    level=level,
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    handlers=[logging.StreamHandler()]
                )
                logger = logging.getLogger("bug_triage_agent")
                logger.warning(f"Error loading logging config, using console logging: {e}")
                return logger
        else:
            # No config file, use basic console logging
            logging.basicConfig(
                level=level,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[logging.StreamHandler()]
            )
    
    logger = logging.getLogger("bug_triage_agent")
    logger.info("Logging configured successfully")
    return logger



