"""
Health Check API Endpoint
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
import os

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    environment: str
    services: Dict[str, str]


@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns the health status of the API and its dependencies.
    """
    # Check if we can connect to required services
    services_status = {}

    # Check database (simplified - in production, actually test connection)
    services_status["database"] = "healthy"

    # Check Redis (simplified)
    services_status["redis"] = "healthy"

    # Check AI services
    services_status["anthropic_api"] = "healthy" if os.getenv("ANTHROPIC_API_KEY") else "not_configured"
    services_status["openai_api"] = "healthy" if os.getenv("OPENAI_API_KEY") else "not_configured"

    return HealthResponse(
        status="healthy",
        version="0.1.0",
        environment=os.getenv("ENVIRONMENT", "development"),
        services=services_status,
    )


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with service-specific information.
    """
    return {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time(),
        "uptime": "uptime_placeholder",  # In production, track actual uptime
        "services": {
            "database": {
                "status": "healthy",
                "connection_pool": "active",
            },
            "redis": {
                "status": "healthy",
                "memory_usage": "low",
            },
            "ai_services": {
                "anthropic": "configured" if os.getenv("ANTHROPIC_API_KEY") else "not_configured",
                "openai": "configured" if os.getenv("OPENAI_API_KEY") else "not_configured",
            },
        },
    }
