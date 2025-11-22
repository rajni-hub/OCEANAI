# OCEANAI - Deployment Guide

Complete guide to deploy OCEANAI on Netlify/Vercel (Frontend) and Python hosting (Backend).

---

## 🏗️ Architecture Overview

- **Frontend**: React app → Deploy to **Netlify** or **Vercel**
- **Backend**: FastAPI app → Deploy to **Railway**, **Render**, or **Fly.io**

---

## 📦 Part 1: Frontend Deployment

### Option A: Deploy to Netlify

#### Step 1: Prepare Repository
```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for Netlify deployment"
git push origin main
```

#### Step 2: Connect to Netlify

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com
   - Sign in with GitHub

2. **Add New Site**
   - Click "Add new site" → "Import an existing project"
   - Select your GitHub repository: `rajni-hub/OCEANAI`
   - Netlify will auto-detect `netlify.toml`

3. **Configure Build Settings** (if not auto-detected)
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Publish directory**: `frontend/build`
   - **Base directory**: Leave empty (or set to root)

4. **Set Environment Variables**
   - Go to: Site Settings → Environment Variables
   - Add:
     ```
     REACT_APP_API_URL = https://your-backend-url.railway.app
     ```
     (Replace with your actual backend URL after deploying backend)

5. **Deploy**
   - Click "Deploy site"
   - Wait for build to complete
   - Your site will be live at: `https://your-site-name.netlify.app`

#### Step 3: Update Backend CORS (After Frontend is Deployed)

Once you have your Netlify URL, update backend CORS:
- Add your Netlify URL to `CORS_ORIGINS` in backend environment variables

---

### Option B: Deploy to Vercel

#### Step 1: Install Vercel CLI (Optional)
```bash
npm install -g vercel
```

#### Step 2: Create `vercel.json` Configuration

Create `vercel.json` in the root:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "headers": {
        "cache-control": "public, max-age=31536000, immutable"
      }
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/build/$1"
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/frontend/build/index.html"
    }
  ]
}
```

#### Step 3: Update `frontend/package.json`

Add build script for Vercel:
```json
{
  "scripts": {
    "build": "react-scripts build",
    "vercel-build": "npm run build"
  }
}
```

#### Step 4: Deploy via Vercel Dashboard

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - **Root Directory**: Set to `frontend`
   - **Framework Preset**: Create React App
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

3. **Set Environment Variables**
   - Add:
     ```
     REACT_APP_API_URL = https://your-backend-url.railway.app
     ```

4. **Deploy**
   - Click "Deploy"
   - Your site will be live at: `https://your-project.vercel.app`

---

## 🐍 Part 2: Backend Deployment

### Option A: Deploy to Railway (Recommended - Easiest)

#### Step 1: Prepare Backend

1. **Create `Procfile`** (for Railway)
   ```bash
   cd backend
   echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile
   ```

2. **Create `runtime.txt`** (optional, for Python version)
   ```bash
   echo "python-3.9" > runtime.txt
   ```

#### Step 2: Deploy to Railway

1. **Go to Railway**
   - Visit: https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Service**
   - Railway will auto-detect Python
   - **Root Directory**: Set to `backend`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   - Go to Variables tab
   - Add:
     ```
     DATABASE_URL = postgresql://... (Railway provides PostgreSQL)
     SECRET_KEY = your-secret-key-here
     GEMINI_API_KEY = your-gemini-api-key
     CORS_ORIGINS = ["https://your-frontend.netlify.app","https://your-frontend.vercel.app"]
     ENVIRONMENT = production
     DEBUG = False
     ```

5. **Add PostgreSQL Database**
   - Click "+ New" → "Database" → "PostgreSQL"
   - Railway will auto-create and set `DATABASE_URL`

6. **Run Migrations**
   - In Railway, open a shell/terminal
   - Run: `alembic upgrade head`

7. **Deploy**
   - Railway will auto-deploy
   - Your API will be at: `https://your-project.railway.app`

---

### Option B: Deploy to Render

#### Step 1: Create `render.yaml`

Create `render.yaml` in root:
```yaml
services:
  - type: web
    name: oceanai-backend
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: GEMINI_API_KEY
        sync: false
      - key: CORS_ORIGINS
        value: '["https://your-frontend.netlify.app"]'
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false

databases:
  - name: oceanai-db
    databaseName: oceanai
    user: oceanai
    plan: free
```

#### Step 2: Deploy to Render

1. **Go to Render**
   - Visit: https://render.com
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Render will detect `render.yaml`

3. **Configure**
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables** (as shown above)

5. **Deploy**
   - Render will auto-deploy
   - Your API will be at: `https://your-service.onrender.com`

---

### Option C: Deploy to Fly.io

#### Step 1: Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
```

#### Step 2: Create `fly.toml`

Run in backend directory:
```bash
cd backend
fly launch
```

Or create manually `backend/fly.toml`:
```toml
app = "oceanai-backend"
primary_region = "iad"

[build]

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  script_checks = []
```

#### Step 3: Deploy
```bash
cd backend
fly deploy
```

---

## 🔗 Part 3: Connect Frontend to Backend

### After Both Are Deployed:

1. **Update Frontend Environment Variable**
   - In Netlify/Vercel dashboard
   - Update `REACT_APP_API_URL` to your backend URL

2. **Update Backend CORS**
   - In Railway/Render/Fly.io dashboard
   - Update `CORS_ORIGINS` to include your frontend URL

3. **Redeploy Both**
   - Frontend: Trigger new deploy
   - Backend: Should auto-redeploy or trigger manually

---

## ✅ Deployment Checklist

### Frontend (Netlify/Vercel)
- [ ] Repository connected
- [ ] Build command configured
- [ ] Environment variables set (`REACT_APP_API_URL`)
- [ ] Deployed successfully
- [ ] All routes working (React Router)

### Backend (Railway/Render/Fly.io)
- [ ] Service created
- [ ] Database provisioned (PostgreSQL)
- [ ] Environment variables set
- [ ] Migrations run (`alembic upgrade head`)
- [ ] CORS configured with frontend URL
- [ ] Deployed successfully
- [ ] API health check passing

### Integration
- [ ] Frontend can reach backend API
- [ ] Authentication working
- [ ] CORS errors resolved
- [ ] All features tested

---

## 🐛 Troubleshooting

### Frontend Issues

**Build Fails:**
- Check Node version (should be 14+)
- Verify `package.json` scripts
- Check build logs in Netlify/Vercel dashboard

**Routes Not Working:**
- Verify `_redirects` file exists in `frontend/public/`
- Check `netlify.toml` or `vercel.json` redirects

**API Calls Failing:**
- Verify `REACT_APP_API_URL` is set correctly
- Check browser console for CORS errors
- Verify backend is running and accessible

### Backend Issues

**Deployment Fails:**
- Check Python version compatibility
- Verify all dependencies in `requirements.txt`
- Check build logs

**Database Connection Errors:**
- Verify `DATABASE_URL` is set correctly
- Check database is provisioned and running
- Run migrations: `alembic upgrade head`

**CORS Errors:**
- Verify `CORS_ORIGINS` includes frontend URL
- Check backend logs for CORS errors
- Ensure frontend URL matches exactly (with https://)

---

## 📚 Quick Reference

### Environment Variables

**Frontend:**
```
REACT_APP_API_URL=https://your-backend.railway.app
```

**Backend:**
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-key
CORS_ORIGINS=["https://your-frontend.netlify.app"]
ENVIRONMENT=production
DEBUG=False
```

### Useful Commands

**Local Testing:**
```bash
# Test frontend build
cd frontend && npm run build

# Test backend
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Database Migrations:**
```bash
# On deployment platform, run:
alembic upgrade head
```

---

## 🎯 Recommended Setup

**For Quickest Deployment:**
- Frontend: **Netlify** (easiest setup)
- Backend: **Railway** (auto-detects Python, provides PostgreSQL)

**For Best Performance:**
- Frontend: **Vercel** (optimized for React)
- Backend: **Fly.io** (global edge network)

---

**Need Help?** Check the deployment platform's documentation or logs for specific errors.

