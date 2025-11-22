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

### 2. GEMINI_API_KEY (Backend) - **OPTIONAL** (Required for AI features)

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

**Note:** Without this, AI features (content generation, refinement) won't work, but everything else will.

---

### 3. DATABASE_URL (Backend) - **REQUIRED**

**For Development (Easiest):**
```
DATABASE_URL=sqlite:///./oceanai.db
```

**For Production (PostgreSQL):**
1. Install PostgreSQL
2. Create database: `CREATE DATABASE oceanai;`
3. Set: `DATABASE_URL=postgresql://user:password@localhost:5432/oceanai`

---

## ✅ Keys That Are Auto-Generated (Optional)

These have defaults and work without setting:

| Variable | Default Value | Can Skip? |
|----------|--------------|------------|
| `ALGORITHM` | `HS256` | ✅ Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | ✅ Yes |
| `CORS_ORIGINS` | `["http://localhost:3000","http://localhost:5173"]` | ✅ Yes |
| `ENVIRONMENT` | `development` | ✅ Yes |
| `DEBUG` | `True` | ✅ Yes |
| `APP_NAME` | `AI Document Authoring Platform` | ✅ Yes |
| `REACT_APP_API_URL` | `http://localhost:8000` | ✅ Yes |

---

## 📝 Minimal Setup (2 Variables)

**Backend `.env` (Minimum):**
```env
DATABASE_URL=sqlite:///./oceanai.db
SECRET_KEY=<generate-using-command-above>
```

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
