"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base
from app.api.routes import auth, projects, documents, generation, refinement, export

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-Assisted Document Authoring and Generation Platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
# Include Vercel frontend URL in allowed origins
cors_origins = settings.CORS_ORIGINS.copy() if isinstance(settings.CORS_ORIGINS, list) else list(settings.CORS_ORIGINS)
if "https://ocean-ai-seven.vercel.app" not in cors_origins:
    cors_origins.append("https://ocean-ai-seven.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(documents.router, prefix="/api/projects", tags=["Documents"])
app.include_router(generation.router, prefix="/api/projects", tags=["Generation"])
app.include_router(refinement.router, prefix="/api/projects", tags=["Refinement"])
app.include_router(export.router, prefix="/api/projects", tags=["Export"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Document Authoring Platform API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

