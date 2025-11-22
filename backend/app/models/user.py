"""
User model
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base, get_uuid_column


class User(Base):
    """User model for authentication and project ownership"""
    
    __tablename__ = "users"
    
    id = Column(
        get_uuid_column(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

