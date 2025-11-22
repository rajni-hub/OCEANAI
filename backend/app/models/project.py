"""
Project model
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum
from app.database import Base, get_uuid_column


class DocumentType(str, enum.Enum):
    """Document type enumeration"""
    WORD = "word"
    POWERPOINT = "powerpoint"


class Project(Base):
    """Project model representing a user's document project"""
    
    __tablename__ = "projects"
    
    id = Column(
        get_uuid_column(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    user_id = Column(
        get_uuid_column(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title = Column(String(255), nullable=False)
    document_type = Column(
        SQLEnum(DocumentType),
        nullable=False
    )
    main_topic = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    document = relationship(
        "Document",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Project(id={self.id}, title={self.title}, type={self.document_type})>"

