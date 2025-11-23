# 🚀 Deploy Backend to Render (Free Tier)

Render is simpler and more reliable than Railway for FastAPI apps. Follow these steps:

## ✅ Step 1: Prepare Your Code

Your `render.yaml` is already configured! Just commit and push:

```bash
git add render.yaml backend/Procfile backend/nixpacks.toml
git commit -m "Prepare for Render deployment"
git push origin main
```

## ✅ Step 2: Create Render Account

1. Go to 👉 **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended)

## ✅ Step 3: Deploy from GitHub

1. In Render Dashboard, click **"New +"** → **"Blueprint"**
2. Connect your GitHub account if not already connected
3. Select your repository: **ocean-ai** (or your repo name)
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

## ✅ Step 4: Configure Environment Variables

After deployment starts, go to your service → **Environment** tab:

Add these variables:

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

## ✅ Step 5: Get Your Backend URL

Render will give you a URL like:
- `https://oceanai-backend.onrender.com`

**Note:** Free tier services spin down after 15 minutes of inactivity. First request may take 30-60 seconds to wake up.

## ✅ Step 6: Test Your Backend

Visit: `https://your-backend-url/api/docs`

You should see Swagger UI! ✅

## ✅ Step 7: Connect Frontend (Vercel)

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Add:
   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com
   ```
3. Click **Save**
4. Go to **Deployments** → Click **"Redeploy"**

## 🎉 Done!

Your backend is now live on Render!

---

## 🔄 Alternative: Manual Setup (Without Blueprint)

If you prefer manual setup:

1. **New +** → **Web Service**
2. Connect GitHub repo
3. Settings:
   - **Name:** `oceanai-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** Leave empty (uses repo root)
4. Add environment variables (same as Step 4)
5. Click **Create Web Service**

---

## 💡 Why Render?

- ✅ **Simpler setup** - Just works with Python
- ✅ **Free tier** - 750 hours/month (enough for most projects)
- ✅ **Auto-deploy** - Deploys on every git push
- ✅ **Better Python support** - No Nixpacks issues
- ✅ **PostgreSQL option** - Free PostgreSQL database available

## ⚠️ Free Tier Limitations

- Services spin down after 15 min inactivity (first request is slow)
- 750 hours/month total across all services
- 512MB RAM limit

For production, consider upgrading to paid plan ($7/month) for always-on service.

