#!/bin/bash

# OCEAN AI - Start Script
# This script starts both backend and frontend servers

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Starting OCEAN AI Application                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend virtual environment not found!"
    echo "   Run: cd backend && python3 -m venv venv"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Frontend dependencies not installed!"
    echo "   Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    pkill -f "uvicorn app.main:app" 2>/dev/null
    pkill -f "react-scripts start" 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo "🚀 Starting Backend Server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo "   ✅ Backend started (PID: $BACKEND_PID)"
echo "   📍 URL: http://localhost:8000"
echo ""

# Wait for backend to start
sleep 3

# Start Frontend
echo "🚀 Starting Frontend Server..."
cd frontend
BROWSER=none npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "   ✅ Frontend started (PID: $FRONTEND_PID)"
echo "   📍 URL: http://localhost:3000"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Both servers are running!"
echo ""
echo "📋 Access URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 Press Ctrl+C to stop both servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Wait for processes
wait
