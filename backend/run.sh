#!/bin/bash

# Backend startup script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please create one from .env.example"
fi

# Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

