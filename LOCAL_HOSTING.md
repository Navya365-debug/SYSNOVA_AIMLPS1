# NeuroQuest Local Hosting Guide

Complete guide for hosting NeuroQuest on your local machine or local network.

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (for PostgreSQL and Redis)
- Your API keys:
  - Anthropic API Key (for Claude)
  - OpenAI API Key (optional, for fallback)
  - PubMed API Key (optional)

## Quick Start

### 1. Initial Setup

Run the setup script to configure your environment:

```bash
python setup_keys.py
```

This will:
- Generate secure encryption keys
- Prompt you for your API keys
- Create `.env` files with proper configuration
- Set up network access settings

### 2. Start All Services

Simply run:

```bash
./start.sh
```

This will automatically:
- Start PostgreSQL (in Docker)
- Start Redis (in Docker)
- Install backend dependencies
- Start the FastAPI backend
- Start the React frontend
- Display access URLs

### 3. Access the Application

Once started, you can access NeuroQuest at:

- **Local access**: http://localhost:3000
- **Network access**: http://YOUR_LOCAL_IP:3000
- **API docs**: http://localhost:8000/docs

## Network Access

### Finding Your Local IP Address

The startup script will automatically display your local IP. To find it manually:

**On macOS/Linux:**
```bash
hostname -I
```

**On Windows:**
```bash
ipconfig
```

Look for the "IPv4 Address" under your active network adapter.

### Accessing from Other Devices

1. **Make sure devices are on the same network**
   - All devices should be connected to the same WiFi or local network

2. **Use your local IP address**
   - Instead of `localhost`, use your machine's IP address
   - Example: `http://192.168.1.100:3000`

3. **Configure firewall (if needed)**
   - Allow incoming connections on ports 3000 and 8000
   - On macOS: System Preferences → Security & Privacy → Firewall
   - On Windows: Windows Defender Firewall → Allow an app

## Service Management

### Check Status

```bash
./status.sh
```

This shows:
- Running services and their PIDs
- Port status
- Health checks
- Recent log entries

### Stop Services

```bash
./stop.sh
```

This will:
- Stop backend and frontend processes
- Optionally stop Docker containers
- Clean up PID files

### Restart Services

```bash
./stop.sh && ./start.sh
```

## Manual Control

If you prefer to control services manually:

### Backend Only

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Only

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

### Docker Services

```bash
# Start PostgreSQL
docker run -d \
  --name neuroquest-postgres \
  -e POSTGRES_DB=neuroquest \
  -e POSTGRES_USER=neuroquest \
  -e POSTGRES_PASSWORD=neuroquest_password \
  -p 5432:5432 \
  postgres:15-alpine

# Start Redis
docker run -d \
  --name neuroquest-redis \
  -p 6379:6379 \
  redis:7-alpine

# Stop containers
docker stop neuroquest-postgres neuroquest-redis

# Remove containers
docker rm neuroquest-postgres neuroquest-redis
```

## Troubleshooting

### Port Already in Use

If you get "port already in use" errors:

```bash
# Find process using the port
lsof -i :3000  # or :8000

# Kill the process
kill -9 <PID>

# Or use the stop script
./stop.sh
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check PostgreSQL logs
docker logs neuroquest-postgres

# Restart PostgreSQL
docker restart neuroquest-postgres
```

### Redis Connection Issues

```bash
# Check if Redis is running
docker ps | grep redis

# Check Redis logs
docker logs neuroquest-redis

# Test Redis connection
redis-cli ping
```

### API Key Issues

If AI services aren't working:

1. Check your `.env` file contains valid API keys
2. Verify API keys have sufficient credits/quota
3. Check backend logs for error messages:
   ```bash
   tail -f backend.log
   ```

### Network Access Issues

If other devices can't connect:

1. **Check firewall settings**
   - Ensure ports 3000 and 8000 are allowed
   - Try temporarily disabling firewall for testing

2. **Verify network connectivity**
   - Ping your machine from the other device
   - Check you're on the same network

3. **Check service is listening on all interfaces**
   - The startup script uses `0.0.0.0` which allows all interfaces
   - Verify with: `netstat -tuln | grep -E '3000|8000'`

### Frontend Not Loading

If the frontend shows errors:

```bash
# Check frontend logs
tail -f frontend.log

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clear browser cache and reload
```

## Configuration

### Environment Variables

Key environment variables in `.env`:

```bash
# API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Network Access
BACKEND_URL=http://0.0.0.0:8000
CORS_ORIGINS=http://localhost:3000,http://0.0.0.0:3000

# Database
DATABASE_URL=postgresql://neuroquest:neuroquest_password@localhost:5432/neuroquest

# Redis
REDIS_URL=redis://localhost:6379/0
```

### Changing Ports

To use different ports, modify the startup script or environment variables:

```bash
# In .env
BACKEND_URL=http://0.0.0.0:8080

# When starting backend
uvicorn main:app --host 0.0.0.0 --port 8080

# When starting frontend
npm run dev -- --host 0.0.0.0 --port 8080
```

## Performance Optimization

### Backend Performance

```bash
# Use multiple workers (production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Enable log rotation
uvicorn main:app --host 0.0.0.0 --port 8000 --log-config log_config.yaml
```

### Frontend Performance

```bash
# Build for production
cd frontend
npm run build

# Serve with nginx (or your preferred web server)
# Point nginx to the dist/ directory
```

## Security Considerations

### Local Network Security

- **Only use on trusted networks**: Local hosting exposes services to your network
- **Use strong passwords**: For database and any authentication
- **Keep software updated**: Regularly update dependencies
- **Monitor logs**: Check for suspicious activity

### API Key Security

- **Never commit `.env` files**: They're in `.gitignore`
- **Rotate keys regularly**: If you suspect compromise
- **Use environment variables**: Don't hardcode keys in source code
- **Limit key permissions**: Only grant necessary scopes

### Firewall Configuration

Consider restricting access to specific IPs:

```bash
# On Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 3000 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 3000 -j DROP

# On macOS (pfctl)
# Edit /etc/pf.conf to add rules
```

## Advanced Setup

### SSL/HTTPS for Local Network

For HTTPS on local network, you can:

1. **Use self-signed certificates**
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```

2. **Use a reverse proxy with SSL**
   ```bash
   # Example with nginx
   server {
       listen 443 ssl;
       server_name your-local-ip;

       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;

       location / {
           proxy_pass http://localhost:3000;
       }
   }
   ```

### Domain Name for Local Access

Use local DNS or `/etc/hosts`:

```bash
# On all devices, add to /etc/hosts (Linux/macOS) or C:\Windows\System32\drivers\etc\hosts (Windows)
192.168.1.100 neuroquest.local
```

Then access at: `http://neuroquest.local:3000`

## Monitoring and Logs

### View Logs in Real-time

```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log

# Docker logs
docker logs -f neuroquest-postgres
docker logs -f neuroquest-redis
```

### Log Locations

- Backend: `backend.log`
- Frontend: `frontend.log`
- PostgreSQL: Docker logs (`docker logs neuroquest-postgres`)
- Redis: Docker logs (`docker logs neuroquest-redis`)

## Support

For issues or questions:

1. Check the logs for error messages
2. Review this troubleshooting section
3. Ensure all prerequisites are met
4. Verify your API keys are valid
5. Check network connectivity

## Next Steps

- **Explore the features**: Try searching for papers, exploring the knowledge graph
- **Customize the configuration**: Modify `.env` to suit your needs
- **Set up monitoring**: Configure logging and alerts
- **Scale up**: Consider moving to cloud hosting for production use

Enjoy using NeuroQuest! 🚀
