# Quick Setup Guide - Environment Variables

## 🚀 Fastest Setup (Development)

### Backend Setup (2 minutes)

1. **Generate SECRET_KEY:**

   ```bash
   cd backend
   python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
   ```

2. **Create .env file:**

   ```bash
   cat > .env << 'EOF'
   # For local development - use PostgreSQL or SQLite for testing
   DATABASE_URL=postgresql://user:password@localhost:5432/oceanai
   # Or for quick testing: DATABASE_URL=sqlite:///./oceanai.db
   
   SECRET_KEY=<paste-generated-key-here>
   GEMINI_API_KEY=<your-gemini-api-key>  # Required for AI features
   CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
   ENVIRONMENT=development
   DEBUG=True
   EOF
   ```

3. **Edit .env and add:**
   - Paste the generated SECRET_KEY
   - (Optional) Add GEMINI_API_KEY from https://aistudio.google.com/app/apikey

### Frontend Setup (30 seconds)

```bash
cd frontend
# .env is optional - defaults to http://localhost:8000
# Only create if backend is on different URL
```

---

## 📋 Required vs Optional

### ✅ REQUIRED (Must Set)

1. **SECRET_KEY** - Generate yourself (see instructions above)
2. **DATABASE_URL** - For local dev: PostgreSQL or SQLite (`sqlite:///./oceanai.db` for quick testing)
   - **Production**: Automatically set by Railway PostgreSQL service

### ⚠️ OPTIONAL (But Recommended)

3. **GEMINI_API_KEY** - **Required** for AI features
   - Get from: https://aistudio.google.com/apikey
   - Required for: Content generation, refinement, AI template suggestions
   - Must be set in Railway environment variables for production

### ✅ AUTO-GENERATED (Defaults Work)

- `ALGORITHM` (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30)
- `CORS_ORIGINS` (default: localhost:3000)
- `ENVIRONMENT` (default: development)
- `DEBUG` (default: True)
- `REACT_APP_API_URL` (default: http://localhost:8000)

---

## 🎯 Minimal Working Configuration

### Backend `.env` (Minimum Required)

```env
# Local development - PostgreSQL or SQLite
DATABASE_URL=postgresql://user:password@localhost:5432/oceanai
# Or: DATABASE_URL=sqlite:///./oceanai.db

SECRET_KEY=<generate-using-command-above>
GEMINI_API_KEY=<your-api-key>  # Required for AI features
```

### Frontend `.env` (Optional)

```env
# Not required - defaults work for development
```

---

## 🔑 Key Generation Commands

### SECRET_KEY (Choose one method)

**Method 1: Python secrets (Recommended)**

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Method 2: OpenSSL**

```bash
openssl rand -hex 32
```

**Method 3: Python UUID**

```bash
python3 -c "import uuid; print(uuid.uuid4().hex + uuid.uuid4().hex)"
```

### GEMINI_API_KEY

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key
5. Add to `.env`: `GEMINI_API_KEY=your-key-here`

---

## ✅ Verification

After setting up, verify configuration:

```bash
# Backend
cd backend
source venv/bin/activate
python3 -c "from app.core.config import settings; print('✅ Config OK' if settings.SECRET_KEY != 'change-this-secret-key-in-production' else '❌ SECRET_KEY not set')"
```

---

## 📝 Complete Example Files

See `.env.example` files in:

- `backend/.env.example`
- `frontend/.env.example`

Copy and customize:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```
