"""
Document model
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base, get_uuid_column


class Document(Base):
    """Document model storing structure and content"""
    
    __tablename__ = "documents"
    
    id = Column(
        get_uuid_column(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    project_id = Column(
        get_uuid_column(),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    structure = Column(JSON, nullable=False)  # Outline for Word, Slides for PPT
    content = Column(JSON, nullable=True)  # Section/slide content
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    project = relationship("Project", back_populates="document")
    refinements = relationship(
        "Refinement",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    feedback_records = relationship(
        "Feedback",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Document(id={self.id}, project_id={self.project_id}, version={self.version})>"

