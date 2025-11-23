# Environment Variables - Quick Reference

## 🔑 Keys You MUST Generate Yourself

### 1. SECRET_KEY (Backend) - **REQUIRED**

**Generate:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Add to:** `backend/.env`
```
SECRET_KEY=<generated-key-here>
```

---

### 2. GEMINI_API_KEY (Backend) - **REQUIRED** (for AI features)

**Get from:** https://aistudio.google.com/app/apikey

**Steps:**
1. Visit the URL above
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

**Add to:** `backend/.env`
```
GEMINI_API_KEY=your-api-key-here
```

**Note:** Required for AI features (content generation, refinement, AI template suggestions).

---

### 3. DATABASE_URL (Backend) - **REQUIRED**

**For Local Development:**
```
# PostgreSQL (recommended)
DATABASE_URL=postgresql://user:password@localhost:5432/oceanai

# Or SQLite for quick testing
DATABASE_URL=sqlite:///./oceanai.db
```

**For Production (Railway):**
- Railway automatically sets `DATABASE_URL` when you add a PostgreSQL service
- No manual configuration needed
- Go to Railway Dashboard → Add PostgreSQL → DATABASE_URL is auto-configured

---

## ✅ Keys That Are Auto-Generated (Optional)

These have defaults and work without setting:

| Variable | Default Value | Can Skip? |
|----------|--------------|------------|
| `ALGORITHM` | `HS256` | ✅ Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | ✅ Yes |
| `CORS_ORIGINS` | `["http://localhost:3000","http://localhost:5173"]` (dev) / `["https://ocean-ai-seven.vercel.app"]` (prod) | ✅ Yes |
| `ENVIRONMENT` | `development` | ✅ Yes |
| `DEBUG` | `True` | ✅ Yes |
| `APP_NAME` | `AI Document Authoring Platform` | ✅ Yes |
| `REACT_APP_API_URL` | `http://localhost:8000` | ✅ Yes |

---

## 📝 Minimal Setup (2 Variables)

**Backend `.env` (Minimum for Local Development):**
```env
# PostgreSQL or SQLite for local testing
DATABASE_URL=postgresql://user:password@localhost:5432/oceanai
# Or: DATABASE_URL=sqlite:///./oceanai.db

SECRET_KEY=<generate-using-command-above>
GEMINI_API_KEY=<your-api-key>  # Required for AI features
```

**Production (Railway):**
- All environment variables set in Railway Dashboard
- DATABASE_URL automatically provided by Railway PostgreSQL service

**Frontend `.env` (Optional):**
```env
# Not needed for development - defaults work
```

---

## 🚀 Quick Start

```bash
# 1. Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 2. Create backend/.env
cd backend
cp .env.example .env
# Edit .env and add SECRET_KEY

# 3. (Optional) Get GEMINI_API_KEY
# Visit: https://aistudio.google.com/app/apikey

# 4. Done! Start servers
```

---

## 📚 Full Documentation

- **Complete Guide:** `ENVIRONMENT_VARIABLES_GUIDE.md`
- **Quick Setup:** `QUICK_SETUP_GUIDE.md`
- **Checklist:** `SECRETS_CHECKLIST.md`
- **Examples:** `backend/.env.example` and `frontend/.env.example`
