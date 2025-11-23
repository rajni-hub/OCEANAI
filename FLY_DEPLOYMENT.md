# 🚀 Deploy Backend to Fly.io (Free Tier)

Fly.io offers a generous free tier with always-on services and global edge network!

## ✅ Step 1: Install Fly CLI

**macOS:**

```bash
curl -L https://fly.io/install.sh | sh
```

**Or download from:** https://fly.io/docs/getting-started/installing-flyctl/

**Verify installation:**

```bash
flyctl version
```

## ✅ Step 2: Sign Up / Login

```bash
flyctl auth signup
# Or if you already have an account:
flyctl auth login
```

This will open your browser to create/login to Fly.io account.

## ✅ Step 3: Navigate to Backend Directory

```bash
cd backend
```

## ✅ Step 4: Launch Your App

```bash
flyctl launch
```

This will:

- Detect your Dockerfile
- Ask for app name (or use default: `oceanai-backend`)
- Ask for region (choose closest to you, e.g., `iad` for US East)
- Ask if you want a Postgres database (say **No** for now, we're using SQLite)
- Ask if you want a Redis database (say **No**)

## ✅ Step 5: Set Environment Variables

```bash
# Generate a secret key first
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then set environment variables:

```bash
flyctl secrets set \
  DATABASE_URL=sqlite:///./oceanai.db \
  SECRET_KEY=<paste-your-generated-key> \
  ALGORITHM=HS256 \
  ACCESS_TOKEN_EXPIRE_MINUTES=60 \
  CORS_ORIGINS='["https://ocean-ai-seven.vercel.app"]' \
  ENVIRONMENT=production \
  DEBUG=false
```

**Optional - If you have Gemini API key:**

```bash
flyctl secrets set GEMINI_API_KEY=your-gemini-key-here
```

## ✅ Step 6: Deploy!

```bash
flyctl deploy
```

This will:

- Build your Docker image
- Push it to Fly.io
- Deploy your app

## ✅ Step 7: Get Your URL

After deployment, Fly.io will show you your app URL:

- Example: `https://oceanai-backend.fly.dev`

**Or check it:**

```bash
flyctl status
flyctl open
```

## ✅ Step 8: Test Your Backend

Visit: `https://your-app-name.fly.dev/api/docs`

You should see Swagger UI! ✅

## ✅ Step 9: Connect Frontend (Vercel)

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Add:
   ```
   REACT_APP_API_URL=https://your-app-name.fly.dev
   ```
3. Click **Save**
4. Go to **Deployments** → Click **"Redeploy"**

## 🎉 Done!

Your backend is now live on Fly.io!

---

## 🔧 Useful Fly.io Commands

```bash
# View logs
flyctl logs

# Check app status
flyctl status

# Open app in browser
flyctl open

# SSH into your app
flyctl ssh console

# Scale your app (free tier: 1 shared-cpu-1x, 256MB RAM)
flyctl scale count 1

# View environment variables
flyctl secrets list

# Update environment variable
flyctl secrets set KEY=value

# Remove environment variable
flyctl secrets unset KEY

# Restart app
flyctl apps restart oceanai-backend
```

## 💡 Why Fly.io?

- ✅ **Always-on free tier** - No spin-down delays!
- ✅ **Global edge network** - Fast worldwide
- ✅ **Simple Docker deployment** - Just works
- ✅ **3 shared-cpu-1x VMs free** - Enough for most apps
- ✅ **256MB RAM per VM** - Sufficient for FastAPI
- ✅ **Automatic HTTPS** - SSL certificates included

## ⚠️ Free Tier Limits

- 3 shared-cpu-1x VMs
- 3GB persistent volume storage
- 160GB outbound data transfer/month
- Perfect for small to medium apps!

## 🐛 Troubleshooting

**Build fails:**

```bash
# Check build logs
flyctl logs

# Rebuild from scratch
flyctl deploy --no-cache
```

**App won't start:**

```bash
# Check logs
flyctl logs

# Check status
flyctl status

# SSH into container
flyctl ssh console
```

**Database issues:**

- SQLite files are ephemeral on Fly.io
- For production, consider Fly Postgres (free tier available)
- Or use external database service

---

## 🚀 Quick Deploy Script

Save this as `deploy.sh` in the backend directory:

```bash
#!/bin/bash
cd backend
flyctl deploy
```

Make it executable:

```bash
chmod +x deploy.sh
```

Then just run:

```bash
./deploy.sh
```
