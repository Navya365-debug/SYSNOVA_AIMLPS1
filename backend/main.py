"""
NeuroQuest Backend - Main FastAPI Application
"""
import sys
from pathlib import Path

# Add parent directory to path to import ai modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routers
from app.api import search, user, graph, health, learning


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    print("🚀 NeuroQuest Backend starting up...")
    yield
    # Shutdown
    print("👋 NeuroQuest Backend shutting down...")


# Create FastAPI app
app = FastAPI(
    title="NeuroQuest API",
    description="AI Research Assistant API",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(graph.router, prefix="/api/graph", tags=["graph"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to NeuroQuest API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "name": "NeuroQuest API",
        "version": "0.1.0",
        "endpoints": {
            "search": "/api/search",
            "user": "/api/user",
            "graph": "/api/graph",
            "health": "/api/health",
            "learning": "/api/learning",
        },
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
