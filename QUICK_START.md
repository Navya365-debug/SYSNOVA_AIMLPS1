# NeuroQuest - Quick Start Guide

## 🚀 Fastest Way to Start

### 1. Setup (One-time)
```bash
python setup_keys.py
```
Enter your API keys when prompted.

### 2. Start
```bash
./start.sh
```

### 3. Access
- **Local**: http://localhost:3000
- **Network**: http://YOUR_IP:3000
- **API Docs**: http://localhost:8000/docs

## 📊 Status Check
```bash
./status.sh
```

## 🛑 Stop Services
```bash
./stop.sh
```

## 🔧 Common Commands

### Backend Only
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Only
```bash
cd frontend
npm run dev -- --host 0.0.0.0 --port 3000
```

### Docker Services
```bash
# Start PostgreSQL & Redis
docker run -d -p 5432:5432 --name neuroquest-postgres \
  -e POSTGRES_DB=neuroquest -e POSTGRES_PASSWORD=neuroquest_password \
  postgres:15-alpine

docker run -d -p 6379:6379 --name neuroquest-redis redis:7-alpine
```

## 🌐 Network Access

### Find Your IP
```bash
# macOS/Linux
hostname -I

# Windows
ipconfig
```

### Access from Other Devices
Use your IP instead of localhost:
```
http://192.168.1.XXX:3000
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
lsof -i :3000  # or :8000
kill -9 <PID>
```

### Check Logs
```bash
tail -f backend.log
tail -f frontend.log
```

### Restart Everything
```bash
./stop.sh && ./start.sh
```

## 📝 Configuration

Edit `.env` file to change:
- API keys
- Ports
- Database settings
- Network access

## 🔑 Required API Keys

- **Anthropic API Key**: `sk-ant-...` (Required)
- **OpenAI API Key**: `sk-...` (Optional, fallback)
- **PubMed API Key**: (Optional)

Get them at:
- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/api-keys

## 📚 More Info

- **Full Guide**: See `LOCAL_HOSTING.md`
- **API Docs**: http://localhost:8000/docs
- **Architecture**: See `docs/ARCHITECTURE.md`

## 💡 Tips

- Make sure Docker is running for PostgreSQL and Redis
- Check firewall settings if network access fails
- Use `./status.sh` to verify all services are running
- Monitor logs for any errors

---

**Need help?** Check `LOCAL_HOSTING.md` for detailed troubleshooting.
