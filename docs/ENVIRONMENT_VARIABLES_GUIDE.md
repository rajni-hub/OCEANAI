# Environment Variables & Secrets Guide

Complete guide for all required environment variables and secrets in the OCEAN AI project.

## 📋 Summary

### Backend Environment Variables (9 total)

| Variable                      | Required      | Generate Yourself | Auto-Generated | Purpose                                                    |
| ----------------------------- | ------------- | ----------------- | -------------- | ---------------------------------------------------------- |
| `DATABASE_URL`                | ✅ Yes        | ✅ Yes            | ❌ No          | Database connection string                                 |
| `SECRET_KEY`                  | ✅ Yes        | ✅ Yes            | ❌ No          | JWT token signing key                                      |
| `GEMINI_API_KEY`              | ⚠️ Optional\* | ✅ Yes            | ❌ No          | Google Gemini API key                                      |
| `CORS_ORIGINS`                | ⚠️ Optional   | ❌ No             | ✅ Yes         | Allowed frontend origins                                   |
| `ALGORITHM`                   | ⚠️ Optional   | ❌ No             | ✅ Yes         | JWT algorithm (default: HS256)                             |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ⚠️ Optional   | ❌ No             | ✅ Yes         | Token expiration (default: 30)                             |
| `ENVIRONMENT`                 | ⚠️ Optional   | ❌ No             | ✅ Yes         | Environment name (default: development)                    |
| `DEBUG`                       | ⚠️ Optional   | ❌ No             | ✅ Yes         | Debug mode (default: True)                                 |
| `APP_NAME`                    | ⚠️ Optional   | ❌ No             | ✅ Yes         | Application name (default: AI Document Authoring Platform) |

\*GEMINI_API_KEY is required for AI features (content generation, refinement, AI suggest template)

### Frontend Environment Variables (1 total)

| Variable            | Required    | Generate Yourself | Auto-Generated | Purpose                                          |
| ------------------- | ----------- | ----------------- | -------------- | ------------------------------------------------ |
| `REACT_APP_API_URL` | ⚠️ Optional | ❌ No             | ✅ Yes         | Backend API URL (default: http://localhost:8000) |

---

## 🔑 Keys You Must Generate Yourself

### 1. SECRET_KEY (Backend) - **REQUIRED**

**Purpose:** Used to sign and verify JWT authentication tokens. Critical for security.

**How to Generate:**

**Option A: Using Python (Recommended)**

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Option B: Using OpenSSL**

```bash
openssl rand -hex 32
```

**Option C: Using Python UUID**

```bash
python3 -c "import uuid; print(uuid.uuid4().hex + uuid.uuid4().hex)"
```

**Option D: Online Generator**

- Visit: https://randomkeygen.com/
- Use "CodeIgniter Encryption Keys" or "Fort Knox Passwords"
- Copy a 32+ character random string

**Requirements:**

- Minimum 32 characters
- Random and unpredictable
- Never commit to version control
- Use different keys for development and production

**Example:**

```
SECRET_KEY=your-super-secret-key-minimum-32-characters-long-random-string-here
```

---

### 2. GEMINI_API_KEY (Backend) - **REQUIRED FOR AI FEATURES**

**Purpose:** Google Gemini API key for AI content generation, refinement, and template suggestions.

**How to Obtain:**

1. **Go to Google AI Studio:**

   - Visit: https://aistudio.google.com/app/apikey
   - Or: https://makersuite.google.com/app/apikey

2. **Sign in with Google Account:**

   - Use your Google account to sign in

3. **Create API Key:**

   - Click "Create API Key" or "Get API Key"
   - Select "Create API key in new project" or use existing project
   - Copy the generated API key

4. **Store Securely:**
   - Never commit to version control
   - Add to `.env` file
   - Keep it private

**Note:**

- Free tier available with usage limits
- API key is required for:
  - Content generation (`/api/projects/{id}/generate`)
  - Content refinement (`/api/projects/{id}/refine`)
  - AI template suggestions (`/api/projects/{id}/ai-suggest-template`)
- Without this key, these features will not work, but other features (auth, projects, export) will work fine

**Example:**

```
GEMINI_API_KEY=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
```

---

### 3. DATABASE_URL (Backend) - **REQUIRED**

**Purpose:** Database connection string for PostgreSQL or SQLite.

**For SQLite (Development - Easiest):**

```
DATABASE_URL=sqlite:///./oceanai.db
```

- No setup required
- Database file created automatically
- Good for development and testing

**For PostgreSQL (Production - Recommended):**

**Step 1: Install PostgreSQL**

```bash
# macOS (using Homebrew)
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# Windows
# Download from: https://www.postgresql.org/download/windows/
```

**Step 2: Create Database**

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE oceanai;

# Create user (optional)
CREATE USER oceanai_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE oceanai TO oceanai_user;

# Exit
\q
```

**Step 3: Format Connection String**

```
DATABASE_URL=postgresql://username:password@localhost:5432/oceanai
```

**Examples:**

```
# With user and password
DATABASE_URL=postgresql://oceanai_user:your_password@localhost:5432/oceanai

# Default postgres user
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/oceanai

# With custom port
DATABASE_URL=postgresql://user:password@localhost:5433/oceanai

# Remote database
DATABASE_URL=postgresql://user:password@db.example.com:5432/oceanai
```

---

## ✅ Keys That Can Be Auto-Generated (Optional)

These have sensible defaults and don't need to be set unless you want to customize:

### Backend Optional Variables

1. **ALGORITHM** (Default: `HS256`)

   - JWT signing algorithm
   - Options: `HS256`, `HS384`, `HS512`
   - Usually no need to change

2. **ACCESS_TOKEN_EXPIRE_MINUTES** (Default: `30`)

   - JWT token expiration time in minutes
   - Set to `60` for 1 hour, `1440` for 24 hours, etc.

3. **CORS_ORIGINS** (Default: `http://localhost:3000,http://localhost:5173`)

   - Comma-separated list of allowed frontend origins
   - For production, add your domain: `https://yourdomain.com`
   - Format: `origin1,origin2,origin3` (no spaces)

4. **ENVIRONMENT** (Default: `development`)

   - Environment name: `development`, `staging`, `production`
   - Used for logging and configuration

5. **DEBUG** (Default: `True`)

   - Enable debug mode: `True` or `False`
   - Set to `False` in production

6. **APP_NAME** (Default: `AI Document Authoring Platform`)
   - Application name (used in API docs)

### Frontend Optional Variables

1. **REACT_APP_API_URL** (Default: `http://localhost:8000`)
   - Backend API URL
   - For production: `https://api.yourdomain.com`
   - Must start with `REACT_APP_` prefix for React to read it

---

## 📝 Step-by-Step Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Copy the example file:**

   ```bash
   cp .env.example .env
   ```

3. **Generate SECRET_KEY:**

   ```bash
   python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
   ```

   Copy the output and add it to `.env`

4. **Get GEMINI_API_KEY:**

   - Visit: https://aistudio.google.com/app/apikey
   - Sign in and create API key
   - Copy and add to `.env`

5. **Set DATABASE_URL:**

   - For development: `sqlite:///./oceanai.db` (easiest)
   - For production: PostgreSQL connection string

6. **Edit `.env` file:**
   ```bash
   nano .env  # or use your preferred editor
   ```
   Fill in the required values

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Copy the example file:**

   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file (optional):**
   - Only needed if backend is not on `http://localhost:8000`
   - For production, set to your backend URL

---

## 🔒 Security Best Practices

1. **Never commit `.env` files:**

   - Already in `.gitignore`
   - Double-check before committing

2. **Use different keys for different environments:**

   - Development: One set of keys
   - Production: Different set of keys

3. **Rotate keys regularly:**

   - Especially `SECRET_KEY` and `GEMINI_API_KEY`
   - If compromised, regenerate immediately

4. **Limit API key permissions:**

   - Gemini API: Use API key restrictions if available
   - Database: Use least privilege principle

5. **Store production keys securely:**
   - Use secret management services (AWS Secrets Manager, HashiCorp Vault)
   - Never hardcode in code
   - Use environment variables or secure vaults

---

## 🧪 Testing Your Configuration

### Test Backend Configuration

```bash
cd backend
source venv/bin/activate
python3 << 'EOF'
from app.core.config import settings
print("✅ Configuration loaded successfully!")
print(f"DATABASE_URL: {settings.DATABASE_URL[:30]}...")
print(f"SECRET_KEY: {'✅ Set' if settings.SECRET_KEY != 'change-this-secret-key-in-production' else '❌ Not set'}")
print(f"GEMINI_API_KEY: {'✅ Set' if settings.GEMINI_API_KEY else '❌ Not set (AI features disabled)'}")
print(f"CORS_ORIGINS: {settings.CORS_ORIGINS}")
EOF
```

### Test Frontend Configuration

```bash
cd frontend
npm start
# Check browser console for any API connection errors
```

---

## 📦 Production Checklist

Before deploying to production:

- [ ] Generate new `SECRET_KEY` (different from development)
- [ ] Set `DATABASE_URL` to production PostgreSQL database
- [ ] Set `GEMINI_API_KEY` (if using AI features)
- [ ] Set `CORS_ORIGINS` to production frontend URL
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Set `REACT_APP_API_URL` to production backend URL
- [ ] Verify all keys are set and working
- [ ] Test authentication flow
- [ ] Test AI features (if enabled)
- [ ] Ensure `.env` files are not committed to git

---

## 🆘 Troubleshooting

### "SECRET_KEY not set" error

- Generate a new SECRET_KEY using the commands above
- Add it to `.env` file
- Restart backend server

### "GEMINI_API_KEY not set" error

- Get API key from Google AI Studio
- Add to `.env` file
- Restart backend server
- Note: This only affects AI features, other features work without it

### "Database connection failed"

- Check DATABASE_URL format
- Verify PostgreSQL is running (if using PostgreSQL)
- Check database credentials
- For SQLite, ensure write permissions in backend directory

### "CORS error" in browser

- Add frontend URL to `CORS_ORIGINS` in backend `.env`
- Format: `http://localhost:3000` (no trailing slash)
- Restart backend server

### Frontend can't connect to backend

- Check `REACT_APP_API_URL` in frontend `.env`
- Verify backend is running on the specified port
- Check browser console for errors

---

## 📚 Additional Resources

- **Google Gemini API:** https://ai.google.dev/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **JWT.io (JWT Debugger):** https://jwt.io/
- **FastAPI Security:** https://fastapi.tiangolo.com/tutorial/security/

---

**Last Updated:** 2024-11-20
