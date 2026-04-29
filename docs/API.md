# NeuroQuest API Documentation

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.neuroquest.com`

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Health Check

#### GET /api/health
Check the health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "anthropic_api": "healthy",
    "openai_api": "healthy"
  }
}
```

#### GET /api/health/detailed
Get detailed health information with service-specific status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890.0,
  "uptime": "uptime_placeholder",
  "services": {
    "database": {
      "status": "healthy",
      "connection_pool": "active"
    },
    "redis": {
      "status": "healthy",
      "memory_usage": "low"
    }
  }
}
```

### Search

#### POST /api/search/
Search for papers across multiple sources.

**Request Body:**
```json
{
  "query": "machine learning",
  "sources": ["arxiv", "pubmed", "scholar"],
  "max_results": 10,
  "use_personalization": true
}
```

**Parameters:**
- `query` (string, required): Search query
- `sources` (array, optional): Data sources to search. Default: ["arxiv", "pubmed", "scholar"]
- `max_results` (integer, optional): Maximum number of results. Default: 10, Range: 1-50
- `use_personalization` (boolean, optional): Use personalization. Default: true

**Response:**
```json
{
  "query": "machine learning",
  "results": [
    {
      "id": "arxiv_12345",
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "abstract": "Paper abstract...",
      "source": "arxiv",
      "url": "https://arxiv.org/abs/12345",
      "published_date": "2024-01-01",
      "relevance_score": 0.95,
      "citation_count": 100,
      "metadata": {
        "category": "cs.AI"
      }
    }
  ],
  "total_results": 10,
  "sources_used": ["arxiv", "pubmed", "scholar"],
  "personalized": true,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### GET /api/search/suggestions
Get search suggestions based on partial query.

**Query Parameters:**
- `query` (string, required): Partial search query
- `limit` (integer, optional): Number of suggestions. Default: 5

**Response:**
```json
[
  "machine learning in deep learning",
  "machine learning neural networks",
  "machine learning natural language processing"
]
```

#### GET /api/search/trending
Get trending research topics.

**Query Parameters:**
- `limit` (integer, optional): Number of topics. Default: 10

**Response:**
```json
[
  {
    "topic": "Large Language Models",
    "count": 1250,
    "growth": "+15%"
  }
]
```

### User

#### GET /api/user/profile
Get user profile.

**Query Parameters:**
- `user_id` (string, required): User identifier

**Response:**
```json
{
  "user_id": "user123",
  "name": "John Doe",
  "email": "john@example.com",
  "research_interests": ["Machine Learning", "NLP"],
  "preferences": {
    "language": "en",
    "results_per_page": 10
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### PUT /api/user/profile
Update user profile.

**Request Body:**
```json
{
  "user_id": "user123",
  "name": "John Doe",
  "email": "john@example.com",
  "research_interests": ["Machine Learning", "NLP"],
  "preferences": {
    "language": "en",
    "results_per_page": 10
  }
}
```

#### POST /api/user/behavior
Track user behavior for personalization.

**Request Body:**
```json
{
  "user_id": "user123",
  "action": "click",
  "paper_id": "arxiv_12345",
  "timestamp": "2024-01-01T00:00:00Z",
  "metadata": {
    "source": "arxiv"
  }
}
```

#### GET /api/user/personalization/settings
Get personalization settings.

**Query Parameters:**
- `user_id` (string, required): User identifier

**Response:**
```json
{
  "enabled": true,
  "min_interactions": 5,
  "weight_clicks": 0.3,
  "weight_time": 0.2,
  "weight_saves": 0.5
}
```

#### GET /api/user/recommendations
Get personalized recommendations.

**Query Parameters:**
- `user_id` (string, required): User identifier
- `limit` (integer, optional): Number of recommendations. Default: 10

**Response:**
```json
[
  {
    "id": "rec_1",
    "title": "Recommended Paper",
    "reason": "Based on your interest in Machine Learning",
    "relevance_score": 0.95
  }
]
```

### Knowledge Graph

#### POST /api/graph/explore
Explore the knowledge graph.

**Request Body:**
```json
{
  "query": "machine learning",
  "node_types": ["concept", "paper"],
  "max_nodes": 50,
  "max_depth": 3
}
```

**Response:**
```json
{
  "nodes": [
    {
      "id": "node_1",
      "label": "Machine Learning",
      "type": "concept",
      "properties": {},
      "weight": 1.0
    }
  ],
  "edges": [
    {
      "source": "node_1",
      "target": "node_2",
      "relationship": "includes",
      "weight": 0.9,
      "properties": {}
    }
  ],
  "metadata": {
    "query": "machine learning",
    "total_nodes": 5,
    "total_edges": 4
  }
}
```

#### GET /api/graph/node/{node_id}
Get details for a specific graph node.

**Response:**
```json
{
  "id": "node_1",
  "label": "Machine Learning",
  "type": "concept",
  "properties": {},
  "weight": 1.0
}
```

#### GET /api/graph/statistics
Get knowledge graph statistics.

**Response:**
```json
{
  "total_nodes": 10000,
  "total_edges": 25000,
  "node_types": {
    "paper": 7000,
    "author": 2000,
    "concept": 800,
    "topic": 200
  },
  "edge_types": {
    "cites": 15000,
    "authored_by": 5000,
    "related_to": 3000
  }
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required or invalid
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Rate Limiting

- Default: 60 requests per minute per user
- Rate limit headers are included in responses:
  - `X-RateLimit-Limit`: Maximum requests per minute
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

## Data Models

### SearchResult
```typescript
interface SearchResult {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  source: string;
  url: string;
  published_date?: string;
  relevance_score: number;
  citation_count?: number;
  metadata?: Record<string, any>;
}
```

### UserProfile
```typescript
interface UserProfile {
  user_id: string;
  name?: string;
  email?: string;
  research_interests: string[];
  preferences: Record<string, any>;
  created_at: string;
  updated_at: string;
}
```

### GraphNode
```typescript
interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties?: Record<string, any>;
  weight: number;
}
```

### GraphEdge
```typescript
interface GraphEdge {
  source: string;
  target: string;
  relationship: string;
  weight: number;
  properties?: Record<string, any>;
}
```
