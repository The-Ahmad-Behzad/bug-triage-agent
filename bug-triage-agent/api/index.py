"""
Vercel serverless function handler for Bug Triage AI Agent
This file wraps the FastAPI application for Vercel deployment
"""

import sys
import os

# Add parent directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from mangum import Mangum
    from src.main.app import app
    
    # Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
    # Mangum converts ASGI to AWS Lambda/API Gateway format
    # lifespan="off" prevents startup/shutdown events from blocking
    handler = Mangum(app, lifespan="off")
except Exception as e:
    # Better error handling for import failures
    import logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to import app: {e}", exc_info=True)
    raise

