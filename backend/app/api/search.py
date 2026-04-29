"""
Search API Endpoint
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.services.retrieval_service import RetrievalService

router = APIRouter()


class SearchRequest(BaseModel):
    """Search request model."""
    query: str = Field(..., description="Search query", min_length=1)
    sources: Optional[List[str]] = Field(
        default=["arxiv", "pubmed", "scholar"],
        description="Data sources to search",
    )
    max_results: Optional[int] = Field(default=10, ge=1, le=50, description="Maximum number of results")
    use_personalization: Optional[bool] = Field(default=True, description="Use personalization")


class SearchResult(BaseModel):
    """Search result model."""
    id: str
    title: str
    authors: List[str]
    abstract: str
    source: str
    url: str
    published_date: Optional[str] = None
    relevance_score: float
    citation_count: Optional[int] = None
    metadata: Dict[str, Any] = {}


class SearchResponse(BaseModel):
    """Search response model."""
    query: str
    results: List[SearchResult]
    total_results: int
    sources_used: List[str]
    personalized: bool
    timestamp: str


@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """
    Search for papers across multiple sources.

    This endpoint aggregates results from arXiv, PubMed, and Google Scholar,
    applies personalization if enabled, and returns synthesized results.
    """
    try:
        # Initialize retrieval service
        retrieval_service = RetrievalService()

        # Perform search
        results = await retrieval_service.search(
            query=request.query,
            sources=request.sources,
            max_results=request.max_results,
            use_personalization=request.use_personalization,
        )

        return SearchResponse(
            query=request.query,
            results=results["results"],
            total_results=results["total_results"],
            sources_used=results["sources_used"],
            personalized=results["personalized"],
            timestamp=datetime.utcnow().isoformat(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/suggestions")
async def get_search_suggestions(query: str, limit: int = 5) -> List[str]:
    """
    Get search suggestions based on partial query.

    Provides autocomplete suggestions for search queries.
    """
    # In production, this would use actual search history and ML models
    suggestions = [
        f"{query} in machine learning",
        f"{query} deep learning",
        f"{query} neural networks",
        f"{query} natural language processing",
        f"{query} computer vision",
    ]

    return suggestions[:limit]


@router.get("/trending")
async def get_trending_topics(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get trending research topics.

    Returns currently trending research topics based on recent activity.
    """
    # In production, this would be computed from actual usage data
    trending = [
        {"topic": "Large Language Models", "count": 1250, "growth": "+15%"},
        {"topic": "Transformer Architectures", "count": 980, "growth": "+12%"},
        {"topic": "Diffusion Models", "count": 850, "growth": "+20%"},
        {"topic": "Multimodal Learning", "count": 720, "growth": "+18%"},
        {"topic": "Reinforcement Learning", "count": 650, "growth": "+8%"},
        {"topic": "Graph Neural Networks", "count": 580, "growth": "+10%"},
        {"topic": "Federated Learning", "count": 520, "growth": "+14%"},
        {"topic": "Explainable AI", "count": 480, "growth": "+11%"},
        {"topic": "AI Ethics", "count": 450, "growth": "+16%"},
        {"topic": "Quantum Machine Learning", "count": 420, "growth": "+22%"},
    ]

    return trending[:limit]
