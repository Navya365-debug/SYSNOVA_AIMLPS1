#!/bin/bash

# NeuroQuest Status Check Script

echo "📊 NeuroQuest Status Check"
echo "=========================================="

# Function to check service status
check_service() {
    local name=$1
    local port=$2
    local pid_file=$3

    # Check if process is running
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "✅ $name: Running (PID: $pid)"
        else
            echo "❌ $name: Not running (stale PID file)"
        fi
    else
        echo "❌ $name: Not running"
    fi

    # Check if port is listening
    if command -v lsof >/dev/null 2>&1; then
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo "   📡 Port $port: Listening"
        else
            echo "   📡 Port $port: Not listening"
        fi
    elif command -v netstat >/dev/null 2>&1; then
        if netstat -tuln 2>/dev/null | grep -q ":$port "; then
            echo "   📡 Port $port: Listening"
        else
            echo "   📡 Port $port: Not listening"
        fi
    fi
}

# Function to check Docker containers
check_docker() {
    local name=$1
    if docker ps | grep -q "$name"; then
        echo "✅ $name: Running in Docker"
    else
        echo "❌ $name: Not running in Docker"
    fi
}

# Function to check API health
check_api_health() {
    local url=$1
    local name=$2

    if command -v curl >/dev/null 2>&1; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
        if [ "$response" = "200" ]; then
            echo "✅ $name: Healthy (HTTP $response)"
        else
            echo "❌ $name: Unhealthy (HTTP $response)"
        fi
    else
        echo "⚠️  curl not available, skipping health check"
    fi
}

# Check services
echo "🔧 Application Services:"
check_service "Backend" 8000 "backend.pid"
check_service "Frontend" 3000 "frontend.pid"

echo ""
echo "📦 Docker Services:"
check_docker "neuroquest-postgres"
check_docker "neuroquest-redis"

echo ""
echo "🏥 Health Checks:"
check_api_health "http://localhost:8000/api/health" "Backend API"
check_api_health "http://localhost:3000" "Frontend"

echo ""
echo "📋 Recent Logs:"
if [ -f "backend.log" ]; then
    echo "📝 Backend (last 5 lines):"
    tail -5 backend.log | sed 's/^/   /'
fi

if [ -f "frontend.log" ]; then
    echo ""
    echo "📝 Frontend (last 5 lines):"
    tail -5 frontend.log | sed 's/^/   /'
fi

echo ""
echo "=========================================="
echo "💡 Quick Actions:"
echo "   Start:  ./start.sh"
echo "   Stop:   ./stop.sh"
echo "   Restart: ./stop.sh && ./start.sh"
echo "=========================================="
