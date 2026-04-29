"""
Self-Learning API Endpoint
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from ai.self_learning_engine import SelfLearningEngine
from ai.session_memory import SessionMemory

router = APIRouter()

# Initialize engines
self_learning_engine = SelfLearningEngine()
session_memory = SessionMemory()


class InteractionRequest(BaseModel):
    """Interaction tracking request."""
    user_id: str
    paper_id: str
    interaction_type: str  # click, save, share, time_spent, scroll_depth, return_visit
    metadata: Optional[Dict[str, Any]] = None


class SessionRequest(BaseModel):
    """Session creation request."""
    user_id: str


class QueryRequest(BaseModel):
    """Query tracking request."""
    session_id: str
    query: str
    results_count: int


class PaperViewRequest(BaseModel):
    """Paper view tracking request."""
    session_id: str
    paper_id: str
    duration: int  # View duration in seconds


@router.post("/interaction")
async def track_interaction(request: InteractionRequest) -> Dict[str, str]:
    """
    Track user interaction for self-learning.

    This endpoint records user interactions and uses them to improve
    personalization and recommendations over time.
    """
    try:
        # Track interaction in self-learning engine
        self_learning_engine.track_interaction(
            request.user_id,
            request.paper_id,
            request.interaction_type,
            request.metadata
        )

        return {
            "status": "success",
            "message": "Interaction tracked successfully",
            "learning_updated": "true",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track interaction: {str(e)}")


@router.post("/session")
async def create_session(request: SessionRequest) -> Dict[str, str]:
    """
    Create a new learning session.

    Creates a new session for tracking user learning progress
    and maintaining context across interactions.
    """
    try:
        session_id = session_memory.create_session(request.user_id)

        return {
            "status": "success",
            "session_id": session_id,
            "message": "Session created successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.post("/session/query")
async def track_query(request: QueryRequest) -> Dict[str, str]:
    """
    Track search query in session.

    Records search queries to understand user research interests
    and improve future recommendations.
    """
    try:
        session_memory.add_query(
            request.session_id,
            request.query,
            request.results_count
        )

        return {
            "status": "success",
            "message": "Query tracked successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track query: {str(e)}")


@router.post("/session/paper-view")
async def track_paper_view(request: PaperViewRequest) -> Dict[str, str]:
    """
    Track paper view in session.

    Records how long users spend viewing papers to understand
    their engagement and preferences.
    """
    try:
        session_memory.add_paper_view(
            request.session_id,
            request.paper_id,
            request.duration
        )

        return {
            "status": "success",
            "message": "Paper view tracked successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track paper view: {str(e)}")


@router.get("/learning/{user_id}")
async def get_learning_insights(user_id: str) -> Dict[str, Any]:
    """
    Get learning insights for a user.

    Returns detailed information about what the system has learned
    about the user's preferences and behavior patterns.
    """
    try:
        insights = self_learning_engine.get_learning_insights(user_id)
        return insights

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get learning insights: {str(e)}")


@router.get("/learning/{user_id}/recommendations")
async def get_adaptive_recommendations(
    user_id: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Get adaptive recommendations based on learning.

    Returns personalized recommendations that improve as the system
    learns more about the user.
    """
    try:
        recommendations = self_learning_engine.get_adaptive_recommendations(user_id, limit)
        return recommendations

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")


@router.get("/session/{session_id}")
async def get_session_summary(session_id: str) -> Dict[str, Any]:
    """
    Get session summary.

    Returns summary of current session including learning progress
    and goals achieved.
    """
    try:
        summary = session_memory.get_session_summary(session_id)
        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session summary: {str(e)}")


@router.get("/session/{session_id}/save")
async def save_session(session_id: str) -> Dict[str, str]:
    """
    Save session to persistent storage.

    Saves the current session state to disk for future learning
    across sessions.
    """
    try:
        session_memory.save_session(session_id)

        return {
            "status": "success",
            "message": "Session saved successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save session: {str(e)}")


@router.get("/user/{user_id}/sessions")
async def get_user_sessions(user_id: str) -> List[Dict[str, Any]]:
    """
    Get all sessions for a user.

    Returns historical session data showing learning progress
    over time.
    """
    try:
        sessions = session_memory.load_user_sessions(user_id)
        return sessions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load sessions: {str(e)}")


@router.get("/user/{user_id}/learning-history")
async def get_learning_history(user_id: str) -> Dict[str, Any]:
    """
    Get comprehensive learning history.

    Returns aggregated learning data across all sessions,
    showing how the system has improved over time.
    """
    try:
        history = session_memory.get_user_learning_history(user_id)
        return history

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get learning history: {str(e)}")


@router.get("/learning/progress")
async def get_global_learning_progress() -> Dict[str, Any]:
    """
    Get global learning progress statistics.

    Returns overall statistics about the self-learning system's
    performance and improvement.
    """
    try:
        # Calculate global statistics
        total_users = len(self_learning_engine.user_profiles)
        total_interactions = sum(
            profile['total_interactions']
            for profile in self_learning_engine.user_profiles.values()
        )

        # Calculate average learning progress
        if total_users > 0:
            avg_learning_progress = sum(
                profile['learning_progress']
                for profile in self_learning_engine.user_profiles.values()
            ) / total_users
        else:
            avg_learning_progress = 0.0

        return {
            "total_users": total_users,
            "total_interactions": total_interactions,
            "average_learning_progress": avg_learning_progress,
            "active_topics": len(self_learning_engine.topic_models),
            "system_status": "learning",
            "last_updated": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get global progress: {str(e)}")


@router.post("/learning/save")
async def save_learning_state() -> Dict[str, str]:
    """
    Save all learning state to disk.

    Persists the entire learning state for recovery and analysis.
    """
    try:
        self_learning_engine.save_learning_state("./learning_state.json")

        return {
            "status": "success",
            "message": "Learning state saved successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save learning state: {str(e)}")


@router.post("/learning/load")
async def load_learning_state() -> Dict[str, str]:
    """
    Load learning state from disk.

    Restores the learning state from persistent storage.
    """
    try:
        self_learning_engine.load_learning_state("./learning_state.json")

        return {
            "status": "success",
            "message": "Learning state loaded successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load learning state: {str(e)}")
