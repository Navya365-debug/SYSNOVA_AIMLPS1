#!/bin/bash

# SYSNOVA_AIMLPS1 - Stop All Services

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDs_DIR="$PROJECT_ROOT/pids"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

echo "🛑 Stopping SYSNOVA_AIMLPS1 Services..."

# Stop Backend
if [ -f "$PIDs_DIR/backend.pid" ]; then
    BACKEND_PID=$(cat "$PIDs_DIR/backend.pid")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        print_success "Backend stopped"
        rm "$PIDs_DIR/backend.pid"
    fi
fi

# Stop Frontend
if [ -f "$PIDs_DIR/frontend.pid" ]; then
    FRONTEND_PID=$(cat "$PIDs_DIR/frontend.pid")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID
        print_success "Frontend stopped"
        rm "$PIDs_DIR/frontend.pid"
    fi
fi

# Stop Docker containers
if command -v docker &> /dev/null; then
    print_info "Stopping Docker containers..."
    cd "$PROJECT_ROOT/docker"
    docker-compose down 2>/dev/null || true
    print_success "Docker containers stopped"
    cd "$PROJECT_ROOT"
fi

print_success "All services stopped"
