#!/bin/bash

# NeuroQuest Local Hosting Startup Script

echo "🚀 Starting NeuroQuest for Local Hosting..."
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Running setup..."
    python setup_keys.py
fi

# Function to check if a service is running
check_service() {
    if pgrep -x "$1" > /dev/null; then
        echo "✅ $1 is running"
        return 0
    else
        echo "❌ $1 is not running"
        return 1
    fi
}

# Function to start PostgreSQL
start_postgres() {
    echo "🐘 Starting PostgreSQL..."
    if ! check_service "postgres"; then
        # Check if PostgreSQL is running in Docker
        if docker ps | grep -q postgres; then
            echo "✅ PostgreSQL is running in Docker"
        else
            echo "📦 Starting PostgreSQL in Docker..."
            docker run -d \
                --name neuroquest-postgres \
                -e POSTGRES_DB=neuroquest \
                -e POSTGRES_USER=neuroquest \
                -e POSTGRES_PASSWORD=neuroquest_password \
                -p 5432:5432 \
                postgres:15-alpine

            echo "⏳ Waiting for PostgreSQL to be ready..."
            sleep 5
        fi
    fi
}

# Function to start Redis
start_redis() {
    echo "🔴 Starting Redis..."
    if ! check_service "redis-server"; then
        # Check if Redis is running in Docker
        if docker ps | grep -q redis; then
            echo "✅ Redis is running in Docker"
        else
            echo "📦 Starting Redis in Docker..."
            docker run -d \
                --name neuroquest-redis \
                -p 6379:6379 \
                redis:7-alpine

            echo "⏳ Waiting for Redis to be ready..."
            sleep 3
        fi
    fi
}

# Function to start backend
start_backend() {
    echo "🔧 Starting Backend..."
    cd backend

    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating Python virtual environment..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Install dependencies
    echo "📦 Installing backend dependencies..."
    pip install -q -r requirements.txt

    # Start backend in background
    echo "🚀 Starting FastAPI server..."
    nohup uvicorn main:app --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../backend.pid

    cd ..
    echo "✅ Backend started (PID: $BACKEND_PID)"
    echo "📋 Backend logs: backend.log"
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting Frontend..."
    cd frontend

    # Install dependencies
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi

    # Start frontend in background
    echo "🚀 Starting React development server..."
    nohup npm run dev -- --host 0.0.0.0 --port 3000 > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../frontend.pid

    cd ..
    echo "✅ Frontend started (PID: $FRONTEND_PID)"
    echo "📋 Frontend logs: frontend.log"
}

# Function to get local IP address
get_local_ip() {
    if command -v hostname >/dev/null 2>&1; then
        hostname -I 2>/dev/null | awk '{print $1}'
    elif command -v ipconfig >/dev/null 2>&1; then
        ipconfig getifaddr en0 2>/dev/null
    else
        echo "localhost"
    fi
}

# Main startup sequence
main() {
    # Start services
    start_postgres
    start_redis

    # Wait for services to be ready
    echo "⏳ Waiting for services to be ready..."
    sleep 5

    # Start applications
    start_backend
    start_frontend

    # Get access information
    LOCAL_IP=$(get_local_ip)

    echo ""
    echo "=========================================="
    echo "🎉 NeuroQuest is now running!"
    echo "=========================================="
    echo ""
    echo "📍 Access URLs:"
    echo "   Local:    http://localhost:3000"
    echo "   Network:  http://$LOCAL_IP:3000"
    echo ""
    echo "🔧 API Documentation:"
    echo "   Local:    http://localhost:8000/docs"
    echo "   Network:  http://$LOCAL_IP:8000/docs"
    echo ""
    echo "📋 Logs:"
    echo "   Backend:  backend.log"
    echo "   Frontend: frontend.log"
    echo ""
    echo "🛑 To stop all services, run: ./stop.sh"
    echo ""
    echo "💡 Tips:"
    echo "   - Make sure your firewall allows connections on ports 3000 and 8000"
    echo "   - For network access, use your machine's IP address instead of localhost"
    echo "   - Check logs if you encounter any issues"
    echo ""
}

# Run main function
main
