#!/bin/bash

# Simple setup script for NeuroQuest

echo "🔐 NeuroQuest Setup - Simple Configuration"
echo "=========================================="

# Generate secure keys
echo "🔑 Generating secure keys..."

# Generate encryption key
ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; import base64; print(base64.urlsafe_b64encode(Fernet.generate_key()).decode())")

# Generate JWT secret
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

echo "✅ Keys generated successfully"

# Create .env file with placeholder keys
cat > .env << ENVFILE
# Database
DATABASE_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest
DATABASE_TEST_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest_test

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_URL=redis://localhost:6379/1

# API Keys - ADD YOUR KEYS BELOW
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# arXiv
ARXIV_API_BASE=http://export.arxiv.org/api/query

# PubMed
PUBMED_API_BASE=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
PUBMED_API_KEY=your_pubmed_api_key_here

# JWT Secret
JWT_SECRET_KEY=$JWT_SECRET
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Encryption
ENCRYPTION_KEY=$ENCRYPTION_KEY

# CORS - Allow local network access
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://0.0.0.0:3000,http://0.0.0.0:8000

# Application
APP_NAME=NeuroQuest
APP_VERSION=0.1.0
DEBUG=True
ENVIRONMENT=development

# Frontend
FRONTEND_URL=http://localhost:3000

# Backend
BACKEND_URL=http://0.0.0.0:8000

# Celery
CELERY_BROKER_URL=redis://localhost:6379/2
CELERY_RESULT_BACKEND=redis://localhost:6379/3

# Vector Store
VECTOR_STORE_PATH=./ai/vector_store
VECTOR_STORE_DIMENSION=1536

# RAG Pipeline
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_TOP_K_RESULTS=5

# Personalization
PERSONALIZATION_ENABLED=True
PERSONALIZATION_MIN_INTERACTIONS=5

# Knowledge Graph
KNOWLEDGE_GRAPH_ENABLED=True
KNOWLEDGE_GRAPH_MAX_NODES=100

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Monitoring
SENTRY_DSN=
PROMETHEUS_ENABLED=False
ENVFILE

# Create backend .env
cat > backend/.env << BACKENDENV
# Database
DATABASE_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest
DATABASE_TEST_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest_test

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_URL=redis://localhost:6379/1

# API Keys - ADD YOUR KEYS BELOW
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# arXiv
ARXIV_API_BASE=http://export.arxiv.org/api/query

# PubMed
PUBMED_API_BASE=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
PUBMED_API_KEY=your_pubmed_api_key_here

# JWT Secret
JWT_SECRET_KEY=$JWT_SECRET
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Encryption
ENCRYPTION_KEY=$ENCRYPTION_KEY

# CORS - Allow local network access
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://0.0.0.0:3000,http://0.0.0.0:8000

# Application
APP_NAME=NeuroQuest
APP_VERSION=0.1.0
DEBUG=True
ENVIRONMENT=development

# Frontend
FRONTEND_URL=http://localhost:3000

# Backend
BACKEND_URL=http://0.0.0.0:8000

# Celery
CELERY_BROKER_URL=redis://localhost:6379/2
CELERY_RESULT_BACKEND=redis://localhost:6379/3

# Vector Store
VECTOR_STORE_PATH=./vector_store
VECTOR_STORE_DIMENSION=1536

# RAG Pipeline
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_TOP_K_RESULTS=5

# Personalization
PERSONALIZATION_ENABLED=True
PERSONALIZATION_MIN_INTERACTIONS=5

# Knowledge Graph
KNOWLEDGE_GRAPH_ENABLED=True
KNOWLEDGE_GRAPH_MAX_NODES=100

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Monitoring
SENTRY_DSN=
PROMETHEUS_ENABLED=False
BACKENDENV

# Create frontend .env
cat > frontend/.env << FRONTENDENV
VITE_API_URL=http://0.0.0.0:8000
VITE_APP_NAME=NeuroQuest
VITE_APP_VERSION=0.1.0
FRONTENDENV

echo ""
echo "✅ Configuration files created!"
echo ""
echo "📝 NEXT STEPS:"
echo "1. Edit .env file and add your API keys:"
echo "   - ANTHROPIC_API_KEY=your_actual_key_here"
echo "   - OPENAI_API_KEY=your_actual_key_here"
echo ""
echo "2. Start the services:"
echo "   ./start.sh"
echo ""
echo "3. Access the application:"
echo "   http://localhost:3000"
echo ""
echo "🔑 Generated keys (for your reference):"
echo "   Encryption Key: ${ENCRYPTION_KEY:0:20}..."
echo "   JWT Secret: ${JWT_SECRET:0:20}..."
echo ""
echo "📚 For detailed setup, see: LOCAL_HOSTING.md"
