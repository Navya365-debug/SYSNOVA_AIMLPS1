# 🔑 API Key Setup for NeuroQuest

## Where to Add Your NVIDIA NIM API Key

### Step 1: Open the .env file
```bash
# In the NeuroQuest directory
open .env
# or edit with your preferred editor
nano .env
# or
vim .env
```

### Step 2: Find this line
```bash
NIM_API_KEY=your_nvidia_nim_api_key_here
```

### Step 3: Replace with your actual API key
```bash
NIM_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Save the file

## 📝 Complete .env Configuration

Your `.env` file should look like this (with your actual key):

```bash
# Database
DATABASE_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest
DATABASE_TEST_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest_test

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_URL=redis://localhost:6379/1

# API Keys - ADD YOUR NVIDIA NIM API KEY HERE
NIM_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NIM_BASE_URL=https://integrate.api.nvidia.com/v1

# Optional: Other API Keys (if you have them)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# arXiv
ARXIV_API_BASE=http://export.arxiv.org/api/query

# PubMed
PUBMED_API_BASE=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
PUBMED_API_KEY=your_pubmed_api_key_here

# JWT Secret
JWT_SECRET_KEY=neuroquest_jwt_secret_change_in_production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Encryption
ENCRYPTION_KEY=neuroquest_encryption_key_change_in_production

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

# AI Model Configuration
AI_PROVIDER=nim  # Options: nim, anthropic, openai
NIM_MODEL=meta/llama-3.1-405b-instruct  # Default NIM model

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
```

## 🚀 Quick Start After Adding API Key

### 1. Start Services
```bash
./start.sh
```

### 2. Access the Application
- **Local**: http://localhost:3000
- **Network**: http://YOUR_IP:3000 (run `./get_ip.sh` to get your IP)

### 3. Test the AI Features
- Search for papers
- The system will use your NVIDIA NIM API key for AI inference
- Results will be synthesized using NIM models

## 🔧 Available NIM Models

The system supports these NVIDIA NIM models:

- `meta/llama-3.1-405b-instruct` (default, most powerful)
- `meta/llama-3.1-70b-instruct` (balanced performance)
- `meta/llama-3.1-8b-instruct` (faster, lighter)
- `mistralai/mistral-large` (alternative model)
- `mistralai/mixtral-8x7b-instruct-v0.1` (Mixture of Experts)

To change the model, edit this line in `.env`:
```bash
NIM_MODEL=meta/llama-3.1-70b-instruct
```

## 🧪 Test Your API Key

You can test if your API key works by running:

```bash
python -c "
from ai.nim_retriever import NIMClient
client = NIMClient()
response = client.text_completion(
    model='meta/llama-3.1-8b-instruct',
    prompt='Hello, this is a test.',
    max_tokens=50
)
print('✅ API key works!' if 'choices' in response else '❌ API key failed')
"
```

## ⚠️ Important Notes

1. **Keep your API key secret**: Never commit `.env` files to git
2. **Check your quota**: Ensure you have sufficient credits on NVIDIA NIM
3. **Model availability**: Some models may have availability restrictions
4. **Rate limits**: Be aware of API rate limits for your account

## 🐛 Troubleshooting

### API Key Not Working
- Verify the key format: `nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- Check your NVIDIA NIM dashboard for key status
- Ensure you have credits/quota available

### Connection Issues
- Check your internet connection
- Verify the NIM_BASE_URL is correct
- Check firewall settings

### Model Not Available
- Try a different model from the available list
- Check NVIDIA NIM status page
- Verify your account has access to the model

## 📚 More Information

- **NVIDIA NIM Documentation**: https://docs.nvidia.com/
- **Available Models**: Check your NVIDIA NIM dashboard
- **API Reference**: https://integrate.api.nvidia.com/v1

---

**Need help?** Check the logs for detailed error messages:
```bash
tail -f backend.log
```
