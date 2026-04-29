# NeuroQuest Development Guide

## 🚀 Initial Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- macOS/Linux/WSL

### 1. Clone & Navigate
```bash
git clone https://github.com/Navya365-debug/NeuroQuest.git
cd NeuroQuest
```

### 2. Get API Keys
- **NVIDIA NIM**: https://build.nvidia.com/nvidia/llama-3-1-405b-instruct
- **OpenAI** (optional): https://platform.openai.com/api-keys
- **Anthropic** (optional): https://console.anthropic.com/

### 3. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys
nano .env
# or
vim .env
```

### 4. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# For AI module dependencies
cd ai
pip install -r requirements.txt
cd ..

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 5. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Optional: Build tailwind CSS
npm run build
```

## 🔧 Running the Project

### Option 1: Using Start Scripts (Recommended)
```bash
# From root directory
./start.sh          # Starts both frontend and backend
./status.sh         # Check service status
./stop.sh           # Stop all services
```

### Option 2: Manual - Backend
```bash
cd backend
source venv/bin/activate

# Development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Option 3: Manual - Frontend
```bash
cd frontend

# Development server
npm run dev -- --host 0.0.0.0 --port 3000

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🐳 Docker Setup

### Start Services
```bash
# Start PostgreSQL
docker run -d -p 5432:5432 --name neuroquest-postgres \
  -e POSTGRES_DB=neuroquest \
  -e POSTGRES_PASSWORD=neuroquest_password \
  -e POSTGRES_USER=neuroquest \
  postgres:15-alpine

# Start Redis
docker run -d -p 6379:6379 --name neuroquest-redis \
  redis:7-alpine

# Optional: View logs
docker logs -f neuroquest-postgres
docker logs -f neuroquest-redis
```

### Using Docker Compose (Recommended)
```bash
cd docker

# Development environment
docker-compose -f docker-compose.dev.yml up -d

# Production environment
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📝 Code Quality

### Linting & Formatting

**Frontend:**
```bash
cd frontend
npm run lint          # Check for issues
npm run format        # Auto-format code
npm run type-check    # TypeScript type checking
```

**Backend:**
```bash
cd backend
pip install pylint black
black .               # Format Python code
pylint app/          # Lint Python code
```

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm test
npm run test:watch   # Watch mode
npm run test:coverage
```

### Backend Tests
```bash
cd backend
pytest tests/
pytest --cov=app tests/  # With coverage
```

## 🌐 Accessing the Application

### Local Development
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- API Redoc: http://localhost:8000/redoc

### Network Access
```bash
# Find your IP
hostname -I  # Linux/macOS
ipconfig     # Windows

# Access from other machine
http://YOUR_IP:3000
```

## 📊 Database Migrations

```bash
cd backend

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔐 Security Notes

- Never commit `.env` files
- Regenerate JWT_SECRET_KEY for production
- Use strong ENCRYPTION_KEY in production
- Store all API keys in a secure vault
- Rotate credentials regularly
- Keep dependencies updated: `pip-audit`, `npm audit`

## 🐛 Debugging

### Backend Debugging
```bash
# Enable debug mode in .env
DEBUG=True

# Check logs
tail -f backend.log
```

### Frontend Debugging
```bash
# React DevTools
# Install browser extension: https://github.com/facebook/react-devtools

# VS Code Debugger
# Install: Debugger for Chrome
# Press F5 to start debugging
```

## 📦 Dependencies Update

```bash
# Backend
cd backend
pip list --outdated
pip install --upgrade <package>

# Frontend
cd frontend
npm outdated
npm update <package>
npm audit fix
```

## 🚀 Deployment Checklist

- [ ] Update API keys in production `.env`
- [ ] Enable DEBUG=False
- [ ] Set ENVIRONMENT=production
- [ ] Configure CORS_ORIGINS appropriately
- [ ] Set strong JWT_SECRET_KEY
- [ ] Set strong ENCRYPTION_KEY
- [ ] Configure database backups
- [ ] Setup monitoring/logging
- [ ] Run security audit
- [ ] Test all API endpoints
- [ ] Performance test with load
- [ ] Document deployment process

## 🆘 Common Issues

### Port Already in Use
```bash
# macOS/Linux
lsof -i :3000
kill -9 <PID>

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Module Not Found
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
pip install -r ai/requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database Connection Error
```bash
# Check PostgreSQL is running
psql postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest

# Reset database
dropdb neuroquest
createdb neuroquest
alembic upgrade head
```

### API Key Errors
- Verify API key in `.env` is correct
- Check API key hasn't expired
- Verify rate limits aren't exceeded
- Check API key has correct permissions

## 📚 Useful Links

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Redis Docs](https://redis.io/documentation)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)

## 💬 Support

For issues or questions:
1. Check existing issues on GitHub
2. Review error logs in `backend.log` and `frontend.log`
3. Run with DEBUG=True for detailed error messages
4. Check API documentation at http://localhost:8000/docs
