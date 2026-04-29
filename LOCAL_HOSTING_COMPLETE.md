# SYSNOVA_AIMLPS1 - Local Hosting Guide

Host the complete SYSNOVA_AIMLPS1 application locally on your machine. This guide covers setup, running, and troubleshooting.

## Quick Start

### 1. Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Docker & Docker Compose** (recommended for databases)
- **macOS/Linux or WSL** (Windows users use WSL2)
- **4GB+ RAM**
- **2GB+ free disk space**

### 2. One-Command Startup

```bash
cd /path/to/SYSNOVA_AIMLPS1
chmod +x run-local.sh stop-local.sh status-local.sh
./run-local.sh
```

That's it! The script will:
- Check prerequisites
- Set up Python virtual environment
- Install dependencies
- Start Docker containers (if available)
- Start backend and frontend

### 3. Access Application

Open in browser:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health/

## Detailed Setup

### Manual Installation (Without run-local.sh)

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r ai/requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev -- --host 0.0.0.0 --port 3000
```

Frontend will be available at: http://localhost:3000

#### Database Services (Docker)

```bash
cd docker

# Start databases
docker-compose up -d postgres redis

# View logs
docker-compose logs -f
```

Or manually with Docker:

```bash
# PostgreSQL
docker run -d -p 5432:5432 --name sysnova-postgres \
  -e POSTGRES_DB=neuroquest \
  -e POSTGRES_USER=neuroquest \
  -e POSTGRES_PASSWORD=neuroquest_password \
  postgres:15-alpine

# Redis
docker run -d -p 6379:6379 --name sysnova-redis \
  redis:7-alpine
```

## Configuration

### Environment Setup

1. Copy .env.example to .env:
```bash
cp .env.example .env
```

2. Edit .env with your settings:
```bash
# Database
DATABASE_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest

# API Keys
NIM_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Ports
FRONTEND_PORT=3000
BACKEND_PORT=8000
```

### Port Configuration

If default ports are in use, change them:

```bash
# Frontend - Edit frontend/vite.config.ts or use:
npm run dev -- --port 3001

# Backend - Change in .env or command:
uvicorn main:app --port 8001
```

## Service Management

### View Status

```bash
./status-local.sh
```

Shows:
- Running services and PIDs
- Ports in use
- Database status
- Recent logs

### Stop Services

```bash
./stop-local.sh
```

Or manually:
```bash
# Kill specific PIDs
kill $(cat pids/backend.pid)
kill $(cat pids/frontend.pid)

# Stop Docker
docker-compose -f docker/docker-compose.yml down
```

### View Logs

```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs
tail -f logs/frontend.log

# Docker logs
docker-compose logs -f
```

## API Testing

### Using curl

```bash
# Health check
curl http://localhost:8000/api/health/

# Search endpoint
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning"}'

# View API documentation
open http://localhost:8000/docs
```

### Using Postman

1. Import this endpoint collection:
   - Base URL: `http://localhost:8000/api`
   - Collections available in `docs/API.md`

## Development Workflow

### Making Changes

**Backend**:
```bash
cd backend
# Edit code - changes auto-reload with --reload flag
# Test changes at http://localhost:8000
```

**Frontend**:
```bash
cd frontend
# Edit code - hot reload enabled automatically
# Changes visible at http://localhost:3000
```

### Database Access

Connect directly to PostgreSQL:
```bash
psql -h localhost -U neuroquest -d neuroquest

# Password: neuroquest_password
```

View Redis data:
```bash
redis-cli
> KEYS *
> GET key_name
```

## Troubleshooting

### Backend Won't Start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Check Python version
python3 --version  # Should be 3.10+

# Check if dependencies installed
source backend/venv/bin/activate
pip list | grep fastapi

# View error logs
cat logs/backend.log
```

### Frontend Won't Start

```bash
# Check if port 3000 is in use
lsof -i :3000

# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf frontend/node_modules frontend/package-lock.json
npm install

# View error logs
cat logs/frontend.log
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Test connection
psql -h localhost -U neuroquest -d neuroquest

# Check Docker network
docker network ls
docker network inspect sysnova_aimlps1_network
```

### Port Already in Use

**macOS/Linux**:
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
# Backend
uvicorn main:app --port 8001

# Frontend
npm run dev -- --port 3001
```

**Windows**:
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### Can't Connect to Database

```bash
# Check if Docker is running
docker ps

# Verify PostgreSQL is accessible
nc -zv localhost 5432

# Check .env DATABASE_URL
cat .env | grep DATABASE_URL
```

### Module Not Found (Backend)

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
pip install -r ai/requirements.txt

# If still failing
python -m pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

### Missing Dependencies (Frontend)

```bash
cd frontend
npm ci  # Clean install
npm install
npm run type-check
```

## Performance Optimization

### Local Development

```bash
# Backend - Use --reload for development
uvicorn main:app --reload

# Frontend - Keep HMR (Hot Module Replacement) enabled
npm run dev
```

### Production Mode (Local)

```bash
# Backend - Production build
uvicorn main:app --workers 4

# Frontend - Build optimized bundle
npm run build
npm run preview
```

## Network Access (Same Network)

Access from another machine on same network:

1. Get your local IP:
```bash
hostname -I  # Linux
ifconfig | grep inet  # macOS
ipconfig  # Windows
```

2. Access using that IP:
```
http://192.168.1.XXX:3000  # Frontend
http://192.168.1.XXX:8000  # Backend
```

**Note**: Update CORS_ORIGINS in .env to allow cross-origin requests.

## Docker Volumes & Persistence

Data is persisted in Docker volumes:

```bash
# View volumes
docker volume ls | grep sysnova

# Inspect volume
docker volume inspect sysnova_aimlps1_postgres_data

# Backup data
docker run --rm -v sysnova_aimlps1_postgres_data:/backup \
  -v $(pwd)/backup:/host alpine tar czf /host/postgres-backup.tar.gz -C /backup .
```

## Backup & Restore

### Backup Database

```bash
# PostgreSQL backup
docker exec sysnova-postgres pg_dump -U neuroquest neuroquest > backup.sql

# Restore
cat backup.sql | docker exec -i sysnova-postgres psql -U neuroquest neuroquest
```

## Advanced Topics

### Using Custom Domains

Edit `/etc/hosts` (macOS/Linux) or `C:\Windows\System32\drivers\etc\hosts` (Windows):

```
127.0.0.1 sysnova.local
127.0.0.1 api.sysnova.local
```

Update .env:
```
FRONTEND_URL=http://sysnova.local:3000
BACKEND_URL=http://api.sysnova.local:8000
CORS_ORIGINS=http://sysnova.local:3000,http://api.sysnova.local:8000
```

### SSL/TLS for Local Development

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Backend - Use with uvicorn
uvicorn main:app --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### Performance Profiling

**Backend**:
```bash
# Add to backend code
pip install py-spy

py-spy record -o profile.svg -- python -m uvicorn main:app
```

**Frontend**:
```bash
# Use React DevTools and Vite profiler
npm run build -- --profile
```

## Useful Commands Reference

| Command | Purpose |
|---------|---------|
| `./run-local.sh` | Start all services |
| `./stop-local.sh` | Stop all services |
| `./status-local.sh` | Check service status |
| `docker-compose -f docker/docker-compose.yml ps` | View containers |
| `docker-compose -f docker/docker-compose.yml logs -f` | View all logs |
| `tail -f logs/backend.log` | View backend logs |
| `tail -f logs/frontend.log` | View frontend logs |

## Next Steps

1. ✅ Application is running locally
2. 📝 Explore the API at http://localhost:8000/docs
3. 🧪 Run tests: `pytest backend/tests/`
4. 📚 Read [DEVELOPMENT.md](DEVELOPMENT.md) for deeper setup
5. 🚀 Deploy to production using Docker or cloud platform

## Support

For issues:
1. Check [DEVELOPMENT.md](DEVELOPMENT.md)
2. Review logs in `logs/` directory
3. Check GitHub issues: https://github.com/Navya365-debug/NeuroQuest/issues
4. Read [SECURITY.md](SECURITY.md) for security concerns

---

**Happy local hosting!** 🚀

Last updated: April 29, 2026
