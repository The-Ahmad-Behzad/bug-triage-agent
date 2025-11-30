"""Main FastAPI application for Bug Triage AI Agent"""

import logging
import os
from datetime import datetime, UTC
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.utils.logging_config import setup_logging
from src.main.startup import startup_tasks
from src.utils.metrics import metrics_collector

# Setup logging
logger = setup_logging()

# Run startup tasks
startup_tasks()

# Create FastAPI app
app = FastAPI(
    title="Bug Triage AI Agent",
    description="AI-driven module that automatically classifies, prioritizes, and assigns software bugs",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    agent_name: str
    version: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    
    Returns the current status of the agent
    """
    try:
        # Check database connectivity
        db_status = "connected"
        try:
            from src.database.connection import get_database
            db = get_database()
            db.command('ping')
        except Exception as e:
            db_status = f"disconnected: {str(e)}"
            logger.warning(f"Database health check failed: {e}")
        
        status = "healthy" if db_status == "connected" else "degraded"
        metrics_collector.record_health_check(status)
        
        return HealthResponse(
            status=status,
            agent_name="bug_triage_agent",
            version="1.0.0",
            timestamp=datetime.now(UTC).isoformat(),
            details={
                "database": db_status,
                "uptime_seconds": metrics_collector.uptime_seconds(),
                "totals": metrics_collector.snapshot()["totals"],
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Bug Triage AI Agent",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/execute")
async def execute(request: dict):
    """
    Execute bug triage
    
    Accepts handshake format input and returns triage results
    """
    from src.handlers.triage_handler import process_triage_request
    return process_triage_request(request)


@app.get("/metrics")
async def metrics():
    """
    Return runtime metrics for observability dashboards.
    """
    return metrics_collector.snapshot()


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

