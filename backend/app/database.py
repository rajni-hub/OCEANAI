"""
Database connection and session management
"""
from sqlalchemy import create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from app.core.config import settings
import uuid

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Helper function to get UUID type based on database
def get_uuid_column():
    """Returns appropriate UUID column type based on database"""
    if 'sqlite' in settings.DATABASE_URL.lower():
        return String(36)  # Use String for SQLite
    else:
        return PostgresUUID(as_uuid=True)  # Use UUID for PostgreSQL


def get_db():
    """
    Dependency function to get database session
    Yields a database session and closes it after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

