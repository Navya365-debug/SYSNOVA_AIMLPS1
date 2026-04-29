#!/bin/bash

#  SYSNOVA_AIMLPS1 - Local Hosting Setup
# This script sets up and starts the entire application locally

set -e  # Exit on any error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"
LOG_DIR="$PROJECT_ROOT/logs"
PIDs_DIR="$PROJECT_ROOT/pids"

# Create necessary directories
mkdir -p "$LOG_DIR" "$PIDs_DIR"

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        return 1
    fi
    print_success "Docker is installed"
    return 0
}

# Check if .env exists
check_env() {
    if [ ! -f "$ENV_FILE" ]; then
        print_error ".env file not found"
        print_info "Creating .env from .env.example..."
        if [ -f "$ENV_FILE.example" ]; then
            cp "$ENV_FILE.example" "$ENV_FILE"
            print_success ".env created. Please update with your API keys."
        else
            print_error ".env.example not found"
            return 1
        fi
    fi
    print_success ".env file exists"
    return 0
}

# Start Docker containers
start_docker() {
    print_header "Starting Docker Services"
    
    cd "$PROJECT_ROOT/docker"
    
    # Check if containers are already running
    if docker ps | grep -q neuroquest-postgres; then
        print_info "PostgreSQL container already running"
    else
        print_info "Starting PostgreSQL and Redis..."
        docker-compose -f docker-compose.yml up -d postgres redis
        sleep 3
        print_success "Database services started"
    fi
    
    cd "$PROJECT_ROOT"
}

# Start Backend
start_backend() {
    print_header "Starting Backend (FastAPI)"
    
    cd "$PROJECT_ROOT/backend"
    
    # Create Python venv if it doesn't exist
    if [ ! -d "venv" ]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate venv and install dependencies
    source venv/bin/activate
    
    if [ -f requirements.txt ]; then
        print_info "Installing backend dependencies..."
        pip install -q -r requirements.txt
    fi
    
    if [ -f ai/requirements.txt ]; then
        print_info "Installing AI dependencies..."
        pip install -q -r ai/requirements.txt
    fi
    
    # Start backend in background
    print_info "Starting FastAPI server on port 8000..."
    nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > "$LOG_DIR/backend.log" 2>&1 &
    
    BACKEND_PID=$!
    echo $BACKEND_PID > "$PIDs_DIR/backend.pid"
    
    sleep 2
    
    if ps -p $BACKEND_PID > /dev/null; then
        print_success "Backend running (PID: $BACKEND_PID)"
    else
        print_error "Failed to start backend"
        return 1
    fi
    
    cd "$PROJECT_ROOT"
}

# Start Frontend
start_frontend() {
    print_header "Starting Frontend (React + Vite)"
    
    cd "$PROJECT_ROOT/frontend"
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_info "Installing frontend dependencies..."
        npm install
    fi
    
    # Start frontend in background
    print_info "Starting Vite dev server on port 3000..."
    nohup npm run dev -- --host 0.0.0.0 --port 3000 > "$LOG_DIR/frontend.log" 2>&1 &
    
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$PIDs_DIR/frontend.pid"
    
    sleep 2
    
    if ps -p $FRONTEND_PID > /dev/null; then
        print_success "Frontend running (PID: $FRONTEND_PID)"
    else
        print_error "Failed to start frontend"
        return 1
    fi
    
    cd "$PROJECT_ROOT"
}

# Show access information
show_access_info() {
    print_header "Application Running!"
    
    echo ""
    echo -e "${GREEN}Local Access:${NC}"
    echo "  Frontend:  http://localhost:3000"
    echo "  Backend:   http://localhost:8000"
    echo "  API Docs:  http://localhost:8000/docs"
    echo ""
    
    # Try to get local IP
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "0.0.0.0")
    if [ "$LOCAL_IP" != "0.0.0.0" ]; then
        echo -e "${GREEN}Network Access (on same network):${NC}"
        echo "  Frontend:  http://$LOCAL_IP:3000"
        echo "  Backend:   http://$LOCAL_IP:8000"
        echo ""
    fi
    
    echo -e "${GREEN}Services:${NC}"
    echo "  PostgreSQL: localhost:5432"
    echo "  Redis:      localhost:6379"
    echo ""
    
    echo -e "${YELLOW}Logs:${NC}"
    echo "  Backend:  $LOG_DIR/backend.log"
    echo "  Frontend: $LOG_DIR/frontend.log"
    echo ""
    
    echo -e "${YELLOW}To stop services:${NC}"
    echo "  ./stop.sh"
    echo ""
}

# Main execution
main() {
    print_header "SYSNOVA_AIMLPS1 - Local Hosting Setup"
    
    # Checks
    check_env || exit 1
    
    # Optional Docker for databases
    if check_docker; then
        start_docker
    else
        print_info "Docker not found. Make sure PostgreSQL and Redis are running locally."
    fi
    
    # Start services
    start_backend || exit 1
    start_frontend || exit 1
    
    # Show info
    show_access_info
    
    # Keep script running
    print_info "Press Ctrl+C to stop all services"
    wait
}

# Run main function
main "$@"
