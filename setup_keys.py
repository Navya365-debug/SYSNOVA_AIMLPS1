"""
Setup script for generating encryption keys and validating API keys
"""
import os
import secrets
from cryptography.fernet import Fernet
import base64


def generate_encryption_key():
    """Generate a secure encryption key."""
    key = Fernet.generate_key()
    return base64.urlsafe_b64encode(key).decode()


def generate_jwt_secret():
    """Generate a secure JWT secret."""
    return secrets.token_urlsafe(32)


def validate_api_key_format(api_key: str, service: str) -> bool:
    """Basic validation of API key format."""
    if not api_key or api_key.startswith("your_"):
        return False

    if service == "anthropic":
        return api_key.startswith("sk-ant-")
    elif service == "openai":
        return api_key.startswith("sk-")
    elif service == "pubmed":
        return len(api_key) >= 10  # PubMed keys are typically longer

    return True


def setup_environment():
    """Set up environment variables with user input."""
    print("🔐 NeuroQuest Setup - Local Hosting Configuration")
    print("=" * 60)

    # Generate secure keys
    encryption_key = generate_encryption_key()
    jwt_secret = generate_jwt_secret()

    print("\n📝 Please enter your API keys:")
    print("(Press Enter to skip if you don't have a key yet)")

    # Get API keys
    anthropic_key = input("Anthropic API Key (sk-ant-...): ").strip()
    openai_key = input("OpenAI API Key (sk-...): ").strip()
    pubmed_key = input("PubMed API Key (optional): ").strip()

    # Validate keys
    print("\n🔍 Validating API keys...")
    if anthropic_key and not validate_api_key_format(anthropic_key, "anthropic"):
        print("⚠️  Warning: Anthropic API key format looks incorrect")
    if openai_key and not validate_api_key_format(openai_key, "openai"):
        print("⚠️  Warning: OpenAI API key format looks incorrect")

    # Get network configuration
    print("\n🌐 Network Configuration:")
    print("Default: localhost (only accessible from this machine)")
    use_network = input("Make accessible from local network? (y/n): ").strip().lower()

    host = "0.0.0.0" if use_network == 'y' else "localhost"

    # Get local IP address if network access is enabled
    if host == "0.0.0.0":
        import socket
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"📡 Your local IP address: {local_ip}")
            print(f"   Access the app from other devices at: http://{local_ip}:3000")
        except:
            print("⚠️  Could not determine local IP address")

    # Create .env file
    env_content = f"""# Database
DATABASE_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest
DATABASE_TEST_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest_test

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_URL=redis://localhost:6379/1

# API Keys
ANTHROPIC_API_KEY={anthropic_key}
OPENAI_API_KEY={openai_key}

# arXiv
ARXIV_API_BASE=http://export.arxiv.org/api/query

# PubMed
PUBMED_API_BASE=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
PUBMED_API_KEY={pubmed_key}

# JWT Secret
JWT_SECRET_KEY={jwt_secret}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Encryption
ENCRYPTION_KEY={encryption_key}

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
BACKEND_URL=http://{host}:8000

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
"""

    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)

    print("\n✅ Configuration saved to .env file")
    print(f"🔐 Generated encryption key: {encryption_key[:20]}...")
    print(f"🔐 Generated JWT secret: {jwt_secret[:20]}...")

    # Create backend .env file
    backend_env = env_content.replace("VECTOR_STORE_PATH=./ai/vector_store", "VECTOR_STORE_PATH=./vector_store")
    with open('backend/.env', 'w') as f:
        f.write(backend_env)

    # Create frontend .env file
    frontend_env = f"""VITE_API_URL=http://{host}:8000
VITE_APP_NAME=NeuroQuest
VITE_APP_VERSION=0.1.0
"""
    with open('frontend/.env', 'w') as f:
        f.write(frontend_env)

    print("\n🚀 Next steps:")
    print("1. Make sure PostgreSQL and Redis are running:")
    print("   - PostgreSQL: docker run -d -p 5432:5432 -e POSTGRES_DB=neuroquest -e POSTGRES_PASSWORD=neuroquest_password postgres:15")
    print("   - Redis: docker run -d -p 6379:6379 redis:7")
    print("2. Start the backend: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --host {host} --port 8000")
    print("3. Start the frontend: cd frontend && npm install && npm run dev -- --host {host} --port 3000")
    print(f"4. Access the app at: http://{host}:3000")

    if host == "0.0.0.0":
        print("\n📡 For network access from other devices:")
        print("   - Use your machine's IP address instead of localhost")
        print("   - Make sure your firewall allows connections on ports 3000 and 8000")


if __name__ == "__main__":
    try:
        setup_environment()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
