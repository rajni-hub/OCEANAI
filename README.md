# AI-Assisted Document Authoring and Generation Platform

A full-stack web application for generating, refining, and exporting structured business documents (.docx and .pptx) using AI.

## 🚀 Features

- ✅ **User Authentication** - Secure JWT-based authentication
- ✅ **Project Management** - Create, view, update, and delete projects
- ✅ **Document Configuration** - Define Word outlines and PowerPoint slide structures
- ✅ **AI Content Generation** - Generate content using Google Gemini API
- ✅ **Content Refinement** - Refine content with AI prompts, feedback, and comments
- ✅ **Document Export** - Export finalized documents as .docx or .pptx
- ✅ **Responsive UI** - Modern, intuitive React frontend
- ✅ **Secure API** - FastAPI backend with JWT authentication

## 📋 Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **SQLite/PostgreSQL** - Database (SQLite for development, PostgreSQL for production)
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing
- **python-docx** - Word document generation
- **python-pptx** - PowerPoint document generation
- **Google Gemini API** - AI content generation

### Frontend

- **React 18** - UI library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Context API** - State management

## 🏗️ Project Structure

```
OCEANAI/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── core/              # Core configuration
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utility functions
│   ├── alembic/               # Database migrations
│   ├── migrations/            # Custom migration scripts
│   ├── requirements.txt        # Python dependencies
│   ├── run.sh                 # Backend startup script
│   ├── .env.example           # Environment variables template
│   └── test_*.py              # Backend test files
├── frontend/
│   ├── public/                # Static files
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── context/           # React Context
│   │   ├── pages/             # Page components
│   │   └── services/          # API services
│   ├── package.json           # Node dependencies
│   └── .env.example           # Environment variables template
├── docs/                      # Additional documentation
├── start.sh                   # Start both servers
├── stop.sh                    # Stop both servers
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 14+
- SQLite (included with Python) or PostgreSQL 12+ (for production)
- Google Gemini API Key (optional, for AI features)

### Using Helper Scripts (Easiest)

**Start both servers:**

```bash
./start.sh
```

**Stop both servers:**

```bash
./stop.sh
```

**Or start backend only:**

```bash
cd backend
./run.sh
```

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `backend` directory:

   ```env
   # For development (SQLite - no setup required)
   DATABASE_URL=sqlite:///./oceanai.db

   # For production (PostgreSQL - create database first)
   # DATABASE_URL=postgresql://user:password@localhost:5432/oceanai

   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   GEMINI_API_KEY=your-gemini-api-key  # Optional, for AI features
   CORS_ORIGINS=["http://localhost:3000"]
   ```

   **Quick setup:** Copy `.env.example` and generate a SECRET_KEY:

   ```bash
   cp .env.example .env
   python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
   ```

5. **Run database migrations (optional for SQLite):**

   ```bash
   # For SQLite: Database is created automatically on first run
   # For PostgreSQL: Run migrations
   alembic upgrade head
   ```

6. **Start the server:**

   ```bash
   uvicorn app.main:app --reload
   # Or use the helper script:
   # ./run.sh
   ```

   The API will be available at:

   - **API**: `http://localhost:8000`
   - **Swagger UI**: `http://localhost:8000/api/docs`
   - **ReDoc**: `http://localhost:8000/api/redoc`

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Create environment file (optional):**
   Create a `.env` file in the `frontend` directory:

   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Start the development server:**

   ```bash
   npm start
   ```

   The app will be available at `http://localhost:3000`

## 📖 Usage Guide

### 1. Register/Login

- Navigate to the application
- Register a new account or login with existing credentials
- JWT token is automatically stored and used for API requests

### 2. Create a Project

- Click "New Project" from the dashboard
- Enter project title
- Select document type (Word or PowerPoint)
- Enter main topic
- Click "Create Project"

### 3. Configure Document Structure

- Open your project
- Go to "Configure" tab
- Add sections (Word) or slides (PowerPoint) manually
- Or use "AI Suggest Template" for AI-generated structure
- Reorder items using up/down arrows
- Click "Save Configuration"

### 4. Generate Content

- Go to "Generate" tab
- Click "Generate Content"
- Wait for AI to generate content for all sections/slides
- Review generated content

### 5. Refine Content

- Go to "Refine" tab
- Select a section/slide from sidebar
- Enter refinement prompt (e.g., "Make this more formal")
- Click "Refine with AI"
- Provide feedback (like/dislike)
- Add comments for reference

### 6. Export Document

- After content is generated, click "Export" button
- Document downloads automatically as .docx or .pptx
- File includes all latest refined content

## 🔐 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Projects

- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects` - Create new project
- `PATCH /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Documents

- `POST /api/projects/{id}/configure` - Configure document structure
- `GET /api/projects/{id}/configuration` - Get document configuration
- `PATCH /api/projects/{id}/structure` - Update document structure
- `POST /api/projects/{id}/ai-suggest-template` - AI suggest template

### Generation

- `POST /api/projects/{id}/generate` - Generate content

### Refinement

- `POST /api/projects/{id}/refine` - Refine content with AI
- `POST /api/projects/{id}/feedback` - Submit feedback
- `POST /api/projects/{id}/comments` - Add comments
- `GET /api/projects/{id}/refinement-history` - Get refinement history

### Export

- `GET /api/projects/{id}/export` - Export document
- `GET /api/projects/{id}/export/docx` - Export Word document
- `GET /api/projects/{id}/export/pptx` - Export PowerPoint document

## 🧪 Testing

### Backend Tests

Test scripts are available in the `backend` directory:

```bash
cd backend
source venv/bin/activate
python test_auth.py
python test_projects.py
python test_documents.py
python test_generation.py
python test_refinement.py
python test_export.py
```

Or run all tests:

```bash
cd backend
source venv/bin/activate
pytest  # If pytest is installed
```

### Frontend Testing

The frontend can be tested manually by:

1. Starting both backend and frontend servers
2. Navigating through all features
3. Testing on different screen sizes (desktop, tablet, mobile)
4. Testing responsive design breakpoints

### Development Tools

**Backend Code Formatting:**

```bash
cd backend
# Using black (install: pip install black)
black app/

# Using autopep8 (install: pip install autopep8)
autopep8 --in-place --recursive app/
```

**Database Migrations:**

```bash
cd backend
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 📚 Documentation

- **Backend API Docs**: Available at `http://localhost:8000/api/docs` (Swagger UI)
- **Setup Guide**: `HOW_TO_RUN.md` - Detailed setup and run instructions
- **Additional Docs**: See `docs/` folder for:
  - Database architecture and optimization
  - Environment variables guide
  - Project planning and status
  - Quick setup guides
- **Backend Feature Docs**: See `backend/*.md` files for detailed API documentation:
  - `AUTHENTICATION.md` - Authentication system
  - `PROJECT_MANAGEMENT.md` - Project management
  - `DOCUMENT_CONFIGURATION.md` - Document configuration
  - `CONTENT_GENERATION.md` - AI content generation
  - `REFINEMENT_INTERFACE.md` - Content refinement
  - `DOCUMENT_EXPORT.md` - Document export

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- User isolation (users can only access their own projects)
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy

## 🎨 UI Features

- Responsive design (desktop, tablet, mobile)
- Clean, modern interface
- Loading states and error handling
- Success notifications
- Empty states with helpful messages
- Tab-based navigation
- Visual project cards

## 🐛 Troubleshooting

### Backend Issues

1. **Database connection error:**

   - For SQLite: Check that the backend directory is writable
   - For PostgreSQL: Check PostgreSQL is running (`pg_isready`)
   - Verify DATABASE_URL in .env file
   - Run migrations: `alembic upgrade head` (optional for SQLite)
   - For SQLite: Database file is created automatically on first run

2. **Import errors:**

   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **CORS errors:**
   - Check CORS_ORIGINS in .env includes frontend URL
   - Restart backend server

### Frontend Issues

1. **API connection errors:**

   - Verify backend is running on port 8000
   - Check REACT_APP_API_URL in .env
   - Check browser console for errors

2. **Authentication issues:**

   - Clear localStorage and login again
   - Check token expiration

3. **Build issues:**
   - Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
   - Check Node.js version: `node --version` (requires 14+)

## 📝 Environment Variables

### Backend (.env)

```env
# Development (SQLite - easiest setup)
DATABASE_URL=sqlite:///./oceanai.db

# Production (PostgreSQL - requires database setup)
# DATABASE_URL=postgresql://user:password@localhost:5432/oceanai

SECRET_KEY=your-secret-key-here  # Generate with: python3 -c "import secrets; print(secrets.token_urlsafe(32))"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=your-gemini-api-key  # Optional, required for AI features
CORS_ORIGINS=["http://localhost:3000"]
APP_NAME=OCEAN AI Platform
ENVIRONMENT=development
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Backend Deployment

1. Set production environment variables
2. Run database migrations
3. Use production WSGI server (e.g., Gunicorn with Uvicorn workers)
4. Set up reverse proxy (Nginx)
5. Configure SSL/TLS

### Frontend Deployment

1. Build production bundle:

   ```bash
   cd frontend
   npm run build
   ```

   This creates an optimized production build in the `build` folder.

2. Serve `build` folder with static file server (Nginx, Apache, etc.)
3. Configure API URL for production in environment variables
4. Set up reverse proxy if needed

## 📄 License

This project is part of an assignment submission.

## 👥 Author

Developed as part of Assignment 3: AI-Assisted Document Authoring and Generation Platform.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React for the UI library
- Google Gemini for AI capabilities
- python-docx and python-pptx for document generation

---

**Status:** ✅ Production Ready  
**All features implemented and tested** 🚀
