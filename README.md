# NeuroQuest

A self-evolving AI research assistant that aggregates papers from arXiv, PubMed, Google Scholar, and the open web — and gets smarter about each user with every session.

## Team: SysNova | Hackathon: Triverse | Domain: AIML

## What It Is

NeuroQuest is an intelligent research platform that combines multi-source paper retrieval, behavior-driven personalization, and dynamic knowledge graphs to help researchers discover relevant papers faster.

## Problem Being Solved

- Researchers face millions of papers; manual filtering wastes days
- Generic tools return identical results for every user
- No session memory — every search starts from scratch

## Core Features (MVP)

1. **Multi-Source Retrieval + Synthesis** - Aggregate and synthesize results from arXiv, PubMed, and Google Scholar
2. **Behavior-Driven Personalization** - Learn from user behavior (clicks, time, saves) to improve results
3. **Knowledge Graph Builder** - Visualize how concepts and papers relate
4. **Private & Encrypted User Profiles** - Keep user data private and encrypted on device

## Tech Stack

### Frontend
- React.js + TypeScript
- Tailwind CSS
- WebSocket for realtime updates

### Backend
- Python (FastAPI)
- PostgreSQL + Redis Cache
- Celery Task Queue
- OAuth2 Authentication

### AI / ML Layer
- LangChain (RAG pipeline)
- FAISS Vector Store
- Claude API (primary inference model)
- spaCy NLP
- OpenAI GPT-4o API (fallback)

### Infrastructure
- Docker + Docker Compose
- GitHub CI/CD

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL
- Redis

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd NeuroQuest
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. **Start with Docker Compose (Recommended)**
```bash
docker-compose up --build
```

4. **Or run locally**

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**AI Services:**
```bash
cd ai
pip install -r requirements.txt
python -m retrievers.arxiv_retriever
python -m retrievers.pubmed_retriever
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Architecture

```
User Query → Multi-Source Retrieval → Context & Profile Fetch
→ Reranking → Personalized Response
```

## Project Structure

```
NeuroQuest/
├── frontend/          # React + TypeScript + Tailwind
├── backend/           # Python + FastAPI
├── ai/                # LangChain + FAISS + ML models
├── docker/            # Docker configurations
├── docs/              # Documentation
└── README.md
```

## API Documentation

See [docs/API.md](docs/API.md) for detailed API documentation.

## Architecture Documentation

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system architecture details.

## Development

### Running Tests

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

### Code Style

**Backend:**
```bash
cd backend
black .
flake8 .
```

**Frontend:**
```bash
cd frontend
npm run lint
npm run format
```

## Deployment

### Docker Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

See deployment documentation in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Team

| Name | Role |
|------|------|
| Mohd Ariz | Lead |
| Navya Khare | Backend Dev |
| Gopal Kumar | Frontend |
| Lakshya Shukla | Data Science |

## Innovation Claim

NeuroQuest is the only system combining adaptive learning, conversational AI, and dynamic knowledge graphs in one unified research platform.

## Acknowledgments

- Built for Triverse Hackathon
- Powered by Claude API and LangChain
- Inspired by the need for smarter research tools
