# AI-Assisted Document Authoring Platform - Project Plan

## Recommended Tech Stack (Best Combination)

Based on the assignment requirements, here's the optimal technology selection:

### Backend

- **FastAPI** ✅ (Modern, async, excellent documentation, built-in API docs)
  - Better than Flask for async operations and API documentation
  - Native support for async/await (important for LLM API calls)
  - Automatic OpenAPI/Swagger documentation

### Frontend

- **React** ✅ (Most popular, extensive ecosystem, component-based)
  - Better than Vue for larger projects and community support
  - Rich ecosystem for UI components
  - Better state management options

### Database

- **PostgreSQL** ✅ (Production-ready, robust, scalable)
  - Better than SQLite for concurrent users and production use
  - Better than Firestore for structured relational data
  - Can use SQLAlchemy ORM for easy database management
  - Note: Can easily switch to SQLite for development if needed

### Authentication

- **JWT-based system** ✅ (Simpler, no external dependencies)
  - Better than Firebase Auth for this assignment (no external service setup)
  - Self-contained, easier to deploy
  - Standard JWT tokens with FastAPI

### LLM Integration

- **Google Gemini API** ✅ (As specified in assignment)

### Document Libraries

- **python-docx** ✅ (For Word documents)
- **python-pptx** ✅ (For PowerPoint documents)

---

## Project Structure

```
OCEANAI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration and environment variables
│   │   ├── database.py             # Database connection and session management
│   │   │
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # User model
│   │   │   ├── project.py          # Project model
│   │   │   ├── document.py         # Document configuration model
│   │   │   └── refinement.py       # Refinement history model
│   │   │
│   │   ├── schemas/                # Pydantic schemas for request/response
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── document.py
│   │   │   └── refinement.py
│   │   │
│   │   ├── api/                    # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── deps.py             # Dependencies (auth, db session)
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py         # Authentication routes
│   │   │   │   ├── projects.py     # Project management routes
│   │   │   │   ├── documents.py    # Document configuration routes
│   │   │   │   ├── generation.py   # AI content generation routes
│   │   │   │   ├── refinement.py   # Refinement routes
│   │   │   │   └── export.py       # Document export routes
│   │   │
│   │   ├── services/               # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py     # Authentication logic
│   │   │   ├── ai_service.py       # Gemini API integration
│   │   │   ├── document_service.py # Document generation logic
│   │   │   └── export_service.py   # Document export logic
│   │   │
│   │   ├── utils/                  # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── security.py        # Password hashing, JWT tokens
│   │   │   └── validators.py       # Input validation helpers
│   │   │
│   │   └── core/                   # Core configuration
│   │       ├── __init__.py
│   │       ├── security.py         # Security settings
│   │       └── config.py           # App settings
│   │
│   ├── alembic/                    # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment variables template
│   └── README.md                   # Backend setup instructions
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── components/             # Reusable React components
│   │   │   ├── common/
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   ├── LoadingSpinner.jsx
│   │   │   │   └── ErrorMessage.jsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.jsx
│   │   │   │   └── RegisterForm.jsx
│   │   │   ├── dashboard/
│   │   │   │   ├── ProjectCard.jsx
│   │   │   │   └── ProjectList.jsx
│   │   │   ├── document/
│   │   │   │   ├── DocumentTypeSelector.jsx
│   │   │   │   ├── WordOutlineEditor.jsx
│   │   │   │   ├── PowerPointSlideEditor.jsx
│   │   │   │   ├── AITemplateGenerator.jsx (Bonus)
│   │   │   │   └── ContentEditor.jsx
│   │   │   └── refinement/
│   │   │       ├── RefinementPanel.jsx
│   │   │       ├── SectionEditor.jsx
│   │   │       └── FeedbackButtons.jsx
│   │   │
│   │   ├── pages/                  # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ProjectCreate.jsx
│   │   │   ├── ProjectEdit.jsx
│   │   │   └── DocumentView.jsx
│   │   │
│   │   ├── services/               # API service layer
│   │   │   ├── api.js              # Axios instance and base config
│   │   │   ├── authService.js
│   │   │   ├── projectService.js
│   │   │   ├── documentService.js
│   │   │   └── exportService.js
│   │   │
│   │   ├── context/                # React Context for state management
│   │   │   ├── AuthContext.jsx
│   │   │   └── ProjectContext.jsx
│   │   │
│   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── useAuth.js
│   │   │   └── useProjects.js
│   │   │
│   │   ├── utils/                  # Utility functions
│   │   │   ├── constants.js
│   │   │   └── helpers.js
│   │   │
│   │   ├── App.jsx                 # Main App component
│   │   ├── App.css
│   │   ├── index.js                # React entry point
│   │   └── index.css
│   │
│   ├── package.json
│   ├── .env.example
│   └── README.md                   # Frontend setup instructions
│
├── .gitignore
├── README.md                       # Main project README
└── PROJECT_PLAN.md                 # This file
```

---

## Implementation Plan

### Phase 1: Project Setup & Infrastructure (Day 1)

1. **Initialize Backend**

   - Set up FastAPI project structure
   - Configure PostgreSQL database connection
   - Set up SQLAlchemy ORM
   - Create Alembic for migrations
   - Set up environment variables (.env)

2. **Initialize Frontend**

   - Create React app (using Vite or Create React App)
   - Set up routing (React Router)
   - Configure Axios for API calls
   - Set up basic folder structure

3. **Database Schema Design**
   - Design User model (id, email, hashed_password, created_at)
   - Design Project model (id, user_id, title, document_type, created_at, updated_at)
   - Design Document model (id, project_id, structure, content, version)
   - Design Refinement model (id, document_id, section_id, prompt, content, feedback, comments, created_at)

### Phase 2: Authentication System (Day 2)

1. **Backend Auth**

   - Implement password hashing (bcrypt)
   - Create JWT token generation/verification
   - Build registration endpoint
   - Build login endpoint
   - Create authentication dependency for protected routes

2. **Frontend Auth**
   - Create login/register pages
   - Implement AuthContext for global auth state
   - Set up token storage (localStorage)
   - Add protected route wrapper
   - Create auth service for API calls

### Phase 3: Project Management (Day 3)

1. **Backend**

   - Create project CRUD endpoints
   - Implement project listing with user filtering
   - Add project deletion/update endpoints

2. **Frontend**
   - Build Dashboard page with project list
   - Create ProjectCard component
   - Implement project creation modal/page
   - Add project navigation

### Phase 4: Document Configuration (Day 4)

1. **Backend**

   - Create document configuration endpoints
   - Implement Word outline structure (sections with headers)
   - Implement PowerPoint slide structure (slides with titles)
   - Add validation for document structure

2. **Frontend**
   - Build DocumentTypeSelector component
   - Create WordOutlineEditor (add/remove/reorder sections)
   - Create PowerPointSlideEditor (add/remove slides, set titles)
   - Implement AI template generator (Bonus feature)

### Phase 5: AI Content Generation (Day 5)

1. **Backend**

   - Set up Gemini API integration
   - Create AI service for content generation
   - Implement section-by-section generation
   - Implement slide-by-slide generation
   - Store generated content in database
   - Add error handling and retry logic

2. **Frontend**
   - Create generation status UI
   - Show progress for each section/slide
   - Display generated content in editor

### Phase 6: Refinement Interface (Day 6)

1. **Backend**

   - Create refinement endpoints
   - Implement section-specific refinement
   - Store refinement history
   - Add feedback (like/dislike) endpoints
   - Add comment storage

2. **Frontend**
   - Build RefinementPanel component
   - Create SectionEditor for each section/slide
   - Add AI refinement prompt input
   - Implement like/dislike buttons
   - Add comment box
   - Show refinement history

### Phase 7: Document Export (Day 7)

1. **Backend**

   - Implement python-docx export
   - Implement python-pptx export
   - Create export endpoints
   - Handle file generation and download

2. **Frontend**
   - Add export button
   - Handle file download
   - Show export status

### Phase 8: Polish & Documentation (Day 8)

1. **Code Quality**

   - Add error handling throughout
   - Implement input validation
   - Add loading states
   - Improve UI/UX
   - Add responsive design

2. **Documentation**

   - Write comprehensive README.md
   - Document API endpoints
   - Add setup instructions
   - Create environment variable documentation
   - Add usage examples

3. **Testing**
   - Test end-to-end flow
   - Verify document export quality
   - Test all user interactions

---

## Database Schema Details

### Users Table

```sql
- id: UUID (Primary Key)
- email: String (Unique, Indexed)
- hashed_password: String
- created_at: DateTime
- updated_at: DateTime
```

### Projects Table

```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key -> Users)
- title: String
- document_type: Enum ('word', 'powerpoint')
- main_topic: String
- created_at: DateTime
- updated_at: DateTime
```

### Documents Table

```sql
- id: UUID (Primary Key)
- project_id: UUID (Foreign Key -> Projects)
- structure: JSON (Outline for Word, Slides for PPT)
- content: JSON (Section/slide content)
- version: Integer
- created_at: DateTime
- updated_at: DateTime
```

### Refinements Table

```sql
- id: UUID (Primary Key)
- document_id: UUID (Foreign Key -> Documents)
- section_id: String (Section/slide identifier)
- refinement_prompt: String
- previous_content: Text
- new_content: Text
- feedback: Enum ('like', 'dislike', null)
- comments: Text
- created_at: DateTime
```

---

## API Endpoints Structure

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token

### Projects

- `GET /api/projects` - List user's projects
- `POST /api/projects` - Create new project
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Documents

- `POST /api/projects/{id}/configure` - Configure document structure
- `GET /api/projects/{id}/document` - Get document content
- `POST /api/projects/{id}/generate-template` - AI template generation (Bonus)

### Generation

- `POST /api/projects/{id}/generate` - Generate content
- `GET /api/projects/{id}/generation-status` - Check generation status

### Refinement

- `POST /api/projects/{id}/refine` - Refine specific section
- `POST /api/projects/{id}/feedback` - Submit like/dislike
- `POST /api/projects/{id}/comments` - Add comment
- `GET /api/projects/{id}/refinement-history` - Get refinement history

### Export

- `GET /api/projects/{id}/export` - Export document (.docx or .pptx)

---

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5432/oceanai
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=your-gemini-api-key
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)

```
REACT_APP_API_URL=http://localhost:8000
```

---

## Next Steps

1. Review and approve this plan
2. Set up project structure
3. Begin Phase 1 implementation

Would you like me to proceed with setting up the project structure?
