#!/bin/bash

# OCEAN AI - Stop Script
# This script stops both backend and frontend servers

echo "🛑 Stopping OCEAN AI servers..."

# Stop backend
pkill -f "uvicorn app.main:app" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend server stopped"
else
    echo "ℹ️  Backend server was not running"
fi

# Stop frontend
pkill -f "react-scripts start" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Frontend server stopped"
else
    echo "ℹ️  Frontend server was not running"
fi

echo ""
echo "✅ All servers stopped"
