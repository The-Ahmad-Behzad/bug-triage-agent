"""
Vercel serverless function handler for Bug Triage AI Agent
This file wraps the FastAPI application for Vercel deployment
"""

import sys
import os

# Add parent directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from src.main.app import app

# Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
# Mangum converts ASGI to AWS Lambda/API Gateway format
handler = Mangum(app, lifespan="off")

