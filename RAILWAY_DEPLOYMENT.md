# 🚀 Deploy Backend to Railway (Fixed Setup)

This guide uses Railway's auto-detection - no complex Nixpacks configuration needed!

## ✅ Step 1: Prepare Your Code

Your code is ready! Just commit and push:

```bash
git add Procfile backend/Procfile backend/runtime.txt backend/requirements.txt
git commit -m "Prepare for Railway deployment"
git push origin main
```

## ✅ Step 2: Deploy on Railway

1. Go to 👉 **https://railway.app**
2. Login with **GitHub**
3. Click **"New Project"** → **"Deploy from GitHub Repo"**
4. Select your repository: **ocean-ai** (or your repo name)

## ✅ Step 3: Configure Root Directory

**IMPORTANT:** In Railway Dashboard:

1. Go to your project → **Settings** → **Service**
2. Set **Root Directory** to: `/` (just a forward slash - repository root)
3. Click **Save**

Railway will use the root `Procfile` which handles the `cd backend` automatically.

## ✅ Step 4: Set Environment Variables

In Railway Dashboard → Your project → **Variables** tab:

Add these environment variables:

```
DATABASE_URL=sqlite:///./oceanai.db
SECRET_KEY=<generate-a-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=["https://ocean-ai-seven.vercel.app"]
ENVIRONMENT=production
DEBUG=false
```

**Generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Optional - If you have Gemini API key:**
```
GEMINI_API_KEY=your-gemini-api-key-here
```

## ✅ Step 5: Railway Auto-Detection

Railway will automatically:
- ✅ Detect Python from `backend/runtime.txt` or `backend/requirements.txt`
- ✅ Install Python 3.9
- ✅ Run `pip install -r backend/requirements.txt` (auto-detected)
- ✅ Use the root `Procfile` to start your app

## ✅ Step 6: Get Your Backend URL

Railway will give you a URL like:
- `https://ocean-ai-production.up.railway.app`

**Test it:**
Visit: `https://your-backend-url/api/docs`

You should see Swagger UI! ✅

## ✅ Step 7: Connect Frontend (Vercel)

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Add:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   ```
3. Click **Save**
4. Go to **Deployments** → Click **"Redeploy"**

## 🎉 Done!

Your backend is now live on Railway!

---

## 🔧 Troubleshooting

### Issue: "uvicorn: command not found"

**Solution:** Make sure:
1. Root Directory is set to `/` (repository root)
2. Railway is using the root `Procfile` (which uses `python -m uvicorn`)
3. Dependencies are installing (check build logs)

### Issue: "cd: backend: No such file or directory"

**Solution:** 
- Set Root Directory to `/` (not `/backend`)
- Railway will use root `Procfile` which handles `cd backend`

### Issue: Dependencies not installing

**Check build logs:**
- Railway Dashboard → Your Service → **Deployments** → Click latest deployment → **View Logs**
- Look for `pip install` commands
- Make sure `backend/requirements.txt` exists

### Issue: Python version wrong

**Solution:**
- Railway reads `backend/runtime.txt` which specifies `python-3.9`
- Or Railway auto-detects from `requirements.txt`

### Force Redeploy

If something's not working:
1. Railway Dashboard → Your Service → **Settings**
2. Scroll down → **Danger Zone**
3. Click **"Redeploy"** or **"Clear Build Cache"**

---

## 📋 Railway Configuration Summary

- **Root Directory:** `/` (repository root)
- **Build Command:** Auto-detected (installs from `backend/requirements.txt`)
- **Start Command:** From root `Procfile`: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Python Version:** 3.9 (from `backend/runtime.txt`)

---

## 💡 Why This Setup Works

1. **Root Directory = `/`** - Railway starts at repo root
2. **Root Procfile** - Handles `cd backend` to navigate to backend folder
3. **Auto-detection** - Railway automatically finds and installs Python dependencies
4. **Simple & Reliable** - No complex Nixpacks configuration needed

This is the simplest and most reliable Railway setup! 🚀

