#!/bin/bash

# NeuroQuest Stop Script

echo "🛑 Stopping NeuroQuest..."
echo "=========================================="

# Function to stop a process by PID file
stop_process() {
    local pid_file=$1
    local name=$2

    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "🛑 Stopping $name (PID: $pid)..."
            kill $pid
            rm "$pid_file"
            echo "✅ $name stopped"
        else
            echo "⚠️  $name process not found (PID: $pid)"
            rm "$pid_file"
        fi
    else
        echo "⚠️  $name PID file not found"
    fi
}

# Stop backend
stop_process "backend.pid" "Backend"

# Stop frontend
stop_process "frontend.pid" "Frontend"

# Optional: Stop Docker containers
read -p "📦 Stop Docker containers (PostgreSQL, Redis)? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🛑 Stopping Docker containers..."
    docker stop neuroquest-postgres 2>/dev/null && echo "✅ PostgreSQL stopped"
    docker stop neuroquest-redis 2>/dev/null && echo "✅ Redis stopped"
    docker rm neuroquest-postgres 2>/dev/null && echo "✅ PostgreSQL container removed"
    docker rm neuroquest-redis 2>/dev/null && echo "✅ Redis container removed"
fi

echo ""
echo "=========================================="
echo "✅ NeuroQuest stopped successfully"
echo "=========================================="
