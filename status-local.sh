#!/bin/bash

# SYSNOVA_AIMLPS1 - Check Status of Running Services

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDs_DIR="$PROJECT_ROOT/pids"
LOG_DIR="$PROJECT_ROOT/logs"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

check_service() {
    local service_name=$1
    local port=$2
    local pid_file="$PIDs_DIR/${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name${NC} (PID: $pid) - Running on port $port"
            return 0
        else
            echo -e "${RED}❌ $service_name${NC} - Process stopped (stale PID: $pid)"
            rm "$pid_file"
            return 1
        fi
    else
        # Try to detect if service is running on port
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  $service_name${NC} - Running on port $port (PID unknown)"
            return 0
        else
            echo -e "${RED}❌ $service_name${NC} - Not running"
            return 1
        fi
    fi
}

check_docker_service() {
    local service_name=$1
    local container_name=$2
    
    if docker ps | grep -q "$container_name"; then
        local container_id=$(docker ps --filter "name=$container_name" --format "{{.ID}}" | head -1)
        echo -e "${GREEN}✅ $service_name${NC} (Container: ${container_id:0:12})"
        return 0
    else
        echo -e "${RED}❌ $service_name${NC} - Not running"
        return 1
    fi
}

print_header "SYSNOVA_AIMLPS1 - Service Status"

echo ""
echo -e "${BLUE}Application Services:${NC}"
check_service "backend" 8000
check_service "frontend" 3000

echo ""
echo -e "${BLUE}Database Services:${NC}"
if command -v docker &> /dev/null; then
    check_docker_service "PostgreSQL" "neuroquest-postgres"
    check_docker_service "Redis" "neuroquest-redis"
else
    echo -e "${YELLOW}ℹ️  Docker not available${NC}"
fi

echo ""
echo -e "${BLUE}Access URLs:${NC}"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"

echo ""
echo -e "${BLUE}Recent Logs:${NC}"
if [ -f "$LOG_DIR/backend.log" ]; then
    echo "Backend (last 5 lines):"
    tail -5 "$LOG_DIR/backend.log" | sed 's/^/  /'
fi

echo ""
echo -e "${YELLOW}Quick Commands:${NC}"
echo "  Start:  ./run-local.sh"
echo "  Stop:   ./stop-local.sh"
echo "  Status: ./status-local.sh"

echo ""
