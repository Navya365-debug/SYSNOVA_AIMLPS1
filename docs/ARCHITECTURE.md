# NeuroQuest System Architecture

## Overview

NeuroQuest is a full-stack AI research assistant platform that aggregates papers from multiple sources, provides personalized results, and maintains privacy through encrypted user profiles.

## System Components

### Frontend Layer
- **Technology**: React + TypeScript + Tailwind CSS
- **Responsibilities**: User interface, API communication, state management
- **Key Features**:
  - Search interface with real-time results
  - Knowledge graph visualization
  - User profile management
  - Privacy settings

### Backend Layer
- **Technology**: Python + FastAPI
- **Responsibilities**: API endpoints, business logic, data processing
- **Key Features**:
  - RESTful API design
  - Authentication and authorization
  - Request validation
  - Error handling

### AI/ML Layer
- **Technology**: LangChain + FAISS + Claude API
- **Responsibilities**: Paper retrieval, synthesis, personalization
- **Key Features**:
  - Multi-source paper retrieval
  - RAG pipeline for result synthesis
  - Behavior-driven personalization
  - Knowledge graph construction

### Data Layer
- **Technologies**: PostgreSQL + Redis
- **Responsibilities**: Data persistence, caching, session management
- **Key Features**:
  - Encrypted user data storage
  - Search history tracking
  - User behavior analytics
  - Knowledge graph storage

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Search Page │  │  Graph Page  │  │ Profile Page │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       API Gateway                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Auth        │  │  Rate Limit  │  │  Validation  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Backend Services                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Search API  │  │  User API    │  │  Graph API   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      AI/ML Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Retrieval   │  │  RAG Pipeline│  │Personalization│     │
│  │  Service     │  │              │  │  Engine      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  Knowledge   │  │  Vector      │                         │
│  │  Graph       │  │  Store       │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Data Sources                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  arXiv API   │  │  PubMed API  │  │  Scholar API │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Storage                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │  Redis       │  │  Vector Store│      │
│  │  (Encrypted) │  │  (Cache)     │  │  (FAISS)      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Search Flow

1. **User Query**: User enters search query in frontend
2. **API Request**: Frontend sends POST request to `/api/search/`
3. **Authentication**: API gateway validates JWT token
4. **Rate Limiting**: Check rate limits for user
5. **Multi-Source Retrieval**:
   - Query arXiv API
   - Query PubMed API
   - Query Google Scholar
6. **Result Aggregation**: Combine results from all sources
7. **Personalization**: Apply user behavior-based personalization
8. **Reranking**: Rerank results based on relevance and personalization
9. **Response**: Return personalized results to frontend
10. **Behavior Tracking**: Log user interaction for future personalization

### Knowledge Graph Flow

1. **Graph Query**: User requests knowledge graph exploration
2. **Graph Construction**: Build graph from papers and relationships
3. **Subgraph Extraction**: Extract relevant subgraph based on query
4. **Visualization**: Return graph data for frontend visualization
5. **Interaction**: Track user interactions with graph nodes

### Personalization Flow

1. **User Action**: User interacts with papers (click, save, share)
2. **Behavior Logging**: Log action with metadata
3. **Profile Update**: Update user profile with new behavior data
4. **Interest Extraction**: Extract research interests from behavior
5. **Score Calculation**: Calculate personalization scores
6. **Result Ranking**: Apply personalization to future searches

## Security Architecture

### Authentication
- JWT-based authentication
- Token expiration and refresh
- Multi-factor authentication support

### Data Encryption
- AES-256 encryption for sensitive user data
- Encrypted fields: email, preferences, research interests
- Encryption at rest and in transit

### Privacy Protection
- User consent management
- Data anonymization for analytics
- GDPR compliance features
- Data retention policies

### Rate Limiting
- Per-user rate limiting
- IP-based fallback
- Configurable limits

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Redis for session management
- Load balancer support

### Caching Strategy
- Redis for frequently accessed data
- API response caching
- Vector store caching

### Background Processing
- Celery for async tasks
- Task queues for heavy operations
- Scheduled tasks for maintenance

## Technology Stack Details

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router
- **Graph Visualization**: D3.js

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery
- **Authentication**: JWT + OAuth2

### AI/ML
- **Framework**: LangChain
- **Vector Store**: FAISS
- **Embeddings**: Sentence Transformers
- **LLM**: Claude API (primary), OpenAI (fallback)
- **Graph Processing**: NetworkX

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Web Server**: Nginx
- **Monitoring**: Prometheus (optional)

## Deployment Architecture

### Development Environment
- Local development with Docker Compose
- Hot reload for frontend and backend
- Local PostgreSQL and Redis

### Production Environment
- Containerized deployment
- Load balancer for API gateway
- Managed database services
- CDN for static assets
- Monitoring and logging

## Performance Optimization

### Database Optimization
- Indexed queries
- Connection pooling
- Query optimization
- Read replicas

### Caching Strategy
- Redis for session data
- API response caching
- Vector store caching
- CDN for static assets

### API Optimization
- Response compression
- Pagination
- Lazy loading
- Async operations

## Monitoring and Observability

### Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Error tracking

### Metrics
- API response times
- Error rates
- User engagement metrics
- System resource usage

### Health Checks
- Database connectivity
- Redis connectivity
- External API availability
- Service health status

## Future Enhancements

### Phase 2 Features
- Advanced personalization models
- Real-time collaboration
- Mobile applications
- Advanced analytics dashboard

### Phase 3 Features
- Multi-tenant support
- Advanced security features
- Integration with academic institutions
- Custom model training
