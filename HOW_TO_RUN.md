# How to Run the Project - Terminal Guide

Complete step-by-step guide to run the OCEAN AI project in terminal.

## 🚀 Quick Start (5 Minutes)

### Prerequisites Check

```bash
# Check Python version (need 3.9+)
python3 --version

# Check Node.js version (need 14+)
node --version

# Check npm
npm --version
```

---

## 📋 Step-by-Step Instructions

### Step 1: Setup Backend

**1.1 Navigate to backend directory:**
```bash
cd /Users/rajni/Desktop/OCEANAI/backend
```

**1.2 Create virtual environment (if not exists):**
```bash
python3 -m venv venv
```

**1.3 Activate virtual environment:**
```bash
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

**1.4 Install dependencies:**
```bash
pip install -r requirements.txt
```

**1.5 Setup environment variables:**
```bash
# Copy example file
cp .env.example .env

# Generate SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
```

**1.6 Edit .env file:**
```bash
# Use your preferred editor
nano .env
# or
vim .env
# or
code .env  # if using VS Code
```

**Add to .env:**
```env
# For local development - use PostgreSQL or SQLite for testing
DATABASE_URL=postgresql://user:password@localhost:5432/oceanai
# Or for quick testing: DATABASE_URL=sqlite:///./oceanai.db

SECRET_KEY=<paste-generated-key-here>
GEMINI_API_KEY=<your-gemini-api-key>  # Required for AI features - get from https://aistudio.google.com/apikey
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
ENVIRONMENT=development
DEBUG=True
```

**1.7 Create database tables:**
```bash
# Run Alembic migrations (recommended)
alembic upgrade head

# Or create tables directly (alternative)
python3 -c "from app.database import Base, engine; from app.models import user, project, document, refinement; Base.metadata.create_all(bind=engine); print('✅ Database tables created')"
```

**1.8 Start backend server:**
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**✅ Backend should now be running at:** http://localhost:8000

**Keep this terminal window open!**

---

### Step 2: Setup Frontend (New Terminal)

**2.1 Open a NEW terminal window/tab:**
- Keep backend terminal running
- Open new terminal for frontend

**2.2 Navigate to frontend directory:**
```bash
cd /Users/rajni/Desktop/OCEANAI/frontend
```

**2.3 Install dependencies (first time only):**
```bash
npm install
```

**2.4 (Optional) Create .env file:**
```bash
# Only needed if backend is not on localhost:8000
cp .env.example .env
# Edit if needed (defaults work for development)
```

**2.5 Start frontend server:**
```bash
npm start
```

**✅ Frontend should now be running at:** http://localhost:3000

**Keep this terminal window open too!**

---

## 🎯 Running Both Servers

### Option 1: Two Terminal Windows (Recommended)

**Terminal 1 - Backend:**
```bash
cd /Users/rajni/Desktop/OCEANAI/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd /Users/rajni/Desktop/OCEANAI/frontend
npm start
```

---

### Option 2: Background Processes

**Start backend in background:**
```bash
cd /Users/rajni/Desktop/OCEANAI/backend
source venv/bin/activate
nohup uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 > backend.log 2>&1 &
echo "Backend started. PID: $!"
```

**Start frontend in background:**
```bash
cd /Users/rajni/Desktop/OCEANAI/frontend
BROWSER=none npm start > frontend.log 2>&1 &
echo "Frontend started. PID: $!"
```

**View logs:**
```bash
# Backend logs
tail -f /Users/rajni/Desktop/OCEANAI/backend/backend.log

# Frontend logs
tail -f /Users/rajni/Desktop/OCEANAI/frontend/frontend.log
```

**Stop servers:**
```bash
# Find processes
ps aux | grep uvicorn
ps aux | grep react-scripts

# Kill processes
pkill -f "uvicorn app.main:app"
pkill -f "react-scripts start"
```

---

### Option 3: Using Screen/Tmux (Advanced)

**Using Screen:**
```bash
# Install screen (if not installed)
# macOS: brew install screen
# Linux: sudo apt-get install screen

# Start screen session
screen -S oceanai

# Start backend
cd /Users/rajni/Desktop/OCEANAI/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Press Ctrl+A then D to detach

# Start frontend in new screen
screen -S frontend
cd /Users/rajni/Desktop/OCEANAI/frontend
npm start

# Detach: Ctrl+A then D

# Reattach later:
screen -r oceanai  # backend
screen -r frontend  # frontend
```

---

## ✅ Verify Servers Are Running

### Check Backend:
```bash
curl http://localhost:8000/api/health
```

**Expected response:**
```json
{"status":"healthy","environment":"development"}
```

### Check Frontend:
```bash
curl http://localhost:3000
```

**Expected:** HTML content (status 200)

### Check Processes:
```bash
# Check if servers are running
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Or
ps aux | grep uvicorn
ps aux | grep react-scripts
```

---

## 🌐 Access the Application

Once both servers are running:

1. **Open browser:** http://localhost:3000
2. **Register** a new account or **login**
3. **Create a project** and start using the application

**Backend API Docs:** http://localhost:8000/api/docs

---

## 🛑 Stopping Servers

### If running in foreground (Ctrl+C):
- Press `Ctrl+C` in each terminal window

### If running in background:
```bash
# Find and kill processes
pkill -f "uvicorn app.main:app"
pkill -f "react-scripts start"

# Or find PID and kill
ps aux | grep uvicorn
kill <PID>
```

---

## 🔧 Troubleshooting

### Backend won't start

**Check if port 8000 is in use:**
```bash
lsof -i :8000
# If something is using it, kill it or use different port
```

**Check virtual environment:**
```bash
cd backend
source venv/bin/activate
which python  # Should show venv path
```

**Check dependencies:**
```bash
pip list | grep fastapi
pip list | grep uvicorn
```

**Check .env file:**
```bash
cd backend
cat .env  # Verify SECRET_KEY is set
```

### Frontend won't start

**Check if port 3000 is in use:**
```bash
lsof -i :3000
```

**Clear npm cache:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Check Node version:**
```bash
node --version  # Should be 14+
```

### Database errors

**For PostgreSQL:**
```bash
cd backend
source venv/bin/activate
# Reset migrations
alembic downgrade base
alembic upgrade head
```

**For SQLite (local testing only):**
```bash
cd backend
source venv/bin/activate
rm -f oceanai.db  # Remove old database
python3 -c "from app.database import Base, engine; from app.models import user, project, document, refinement; Base.metadata.create_all(bind=engine); print('✅ Database recreated')"
```

**Note:** Production uses PostgreSQL on Railway, which is automatically configured.

---

## 📝 Using Helper Scripts

The repository includes helper scripts for easy server management:

### Option 1: Start Both Servers

**Use the provided `start.sh` script:**
```bash
./start.sh
```

This will:
- Start backend on http://localhost:8000
- Start frontend on http://localhost:3000
- Create log files (backend.log, frontend.log)
- Allow stopping both servers with Ctrl+C

**Stop both servers:**
```bash
./stop.sh
```

### Option 2: Start Backend Only

**Use the provided `backend/run.sh` script:**
```bash
cd backend
./run.sh
```

### Option 3: Manual Script (Alternative)

If you prefer to create your own script, here's an example:

**Create `start.sh` in project root:**
```bash
#!/bin/bash

# Start Backend
echo "🚀 Starting Backend Server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait a bit
sleep 3

# Start Frontend
echo "🚀 Starting Frontend Server..."
cd ../frontend
npm start &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ Both servers started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
wait
```

**Make executable:**
```bash
chmod +x start.sh
```

**Run:**
```bash
./start.sh
```

---

## 🎯 Quick Commands Reference

### Backend
```bash
# Navigate
cd backend

# Activate venv
source venv/bin/activate

# Start server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Check health
curl http://localhost:8000/api/health
```

### Frontend
```bash
# Navigate
cd frontend

# Start server
npm start

# Build for production
npm run build
```

---

## 📚 Additional Resources

- **Backend API Docs:** http://localhost:8000/api/docs
- **Backend ReDoc:** http://localhost:8000/api/redoc
- **Environment Setup:** See `ENVIRONMENT_VARIABLES_GUIDE.md`

---

**Happy Coding! 🚀**

