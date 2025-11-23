# 🔧 Railway Deployment Fix

## Current Issue
Railway is trying to execute `cd` which doesn't work in Docker mode.

## ✅ Solution

### Step 1: Verify Railway Settings

In Railway Dashboard → Your Service → **Settings**:

1. **Root Directory:** Must be `/backend` (not `/`)
2. **Start Command:** Should be **EMPTY** or **AUTO** (let Railway use Procfile/nixpacks.toml)
   - ❌ Don't set: `cd backend && python -m uvicorn...`
   - ✅ Leave empty or delete any custom start command

### Step 2: Clear Build Cache

1. Railway Dashboard → Your Service → **Settings**
2. Scroll to **"Danger Zone"**
3. Click **"Clear Build Cache"** or **"Redeploy"**

### Step 3: Verify Files Are Correct

Your files should be:

**`backend/Procfile`:**
```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**`backend/nixpacks.toml`:**
```toml
[providers]
python = "3.9"

[phases.setup]
nixPkgs = ["python39"]

[phases.install]
cmds = [
  "python -m pip install --upgrade pip",
  "python -m pip install -r requirements.txt"
]

[start]
cmd = "python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

**`backend/runtime.txt`:**
```
python-3.9
```

### Step 4: Commit and Push

```bash
git add backend/Procfile backend/nixpacks.toml backend/runtime.txt
git commit -m "Fix Railway: remove cd command, use nixpacks start"
git push origin main
```

### Step 5: Check Railway Logs

After redeploy, check the logs:
- Railway Dashboard → Your Service → **Deployments** → Latest → **View Logs**

Look for:
- ✅ "Installing dependencies..."
- ✅ "Starting application..."
- ❌ Any errors about `cd` command

## 🎯 Why This Works

1. **Root Directory = `/backend`** - Railway starts in backend directory
2. **No `cd` commands** - All commands run directly (no need to change directory)
3. **nixpacks.toml start command** - Takes precedence over Procfile
4. **Python 3.9** - Consistent across all config files

## ⚠️ Common Mistakes

1. **Setting Start Command in Dashboard** - Don't add custom start command with `cd`
2. **Wrong Root Directory** - Must be `/backend`, not `/`
3. **Cached Build** - Always clear cache after config changes
4. **Python Version Mismatch** - runtime.txt and nixpacks.toml must match

## 🚀 Expected Result

After fixing:
- ✅ Build completes successfully
- ✅ Dependencies install
- ✅ App starts with: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- ✅ Backend accessible at Railway URL

