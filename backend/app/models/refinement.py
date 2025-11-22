"""
Refinement model - Optimized to store only metadata, not content
Content is stored in documents.content as the single source of truth
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum
from app.database import Base, get_uuid_column


class FeedbackType(str, enum.Enum):
    """Feedback type enumeration"""
    LIKE = "like"
    DISLIKE = "dislike"


class Refinement(Base):
    """
    Refinement model storing only metadata about refinements.
    Content is stored in documents.content as the single source of truth.
    This prevents data duplication and reduces storage usage.
    """
    
    __tablename__ = "refinements"
    
    id = Column(
        get_uuid_column(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    document_id = Column(
        get_uuid_column(),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    section_id = Column(String(100), nullable=False, index=True)  # Section/slide identifier
    refinement_prompt = Column(Text, nullable=True)  # User's refinement request
    # TEMPORARY: Keep these for backward compatibility until migration is run
    # After migration, these will be removed - content is in documents.content
    previous_content = Column(Text, nullable=True)  # DEPRECATED - will be removed after migration
    new_content = Column(Text, nullable=True)  # DEPRECATED - will be removed after migration
    feedback = Column(
        SQLEnum(FeedbackType),
        nullable=True
    )  # User's like/dislike (deprecated - use Feedback model instead)
    comments = Column(Text, nullable=True)  # User's comments
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="refinements")
    
    # Composite indexes for performance
    __table_args__ = (
        Index('idx_refinement_document_section', 'document_id', 'section_id'),
        Index('idx_refinement_section_created', 'section_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Refinement(id={self.id}, document_id={self.document_id}, section_id={self.section_id})>"


class Feedback(Base):
    """
    Separate Feedback model for storing likes/dislikes.
    This allows better separation of concerns and easier querying.
    """
    
    __tablename__ = "feedback"
    
    id = Column(
        get_uuid_column(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    document_id = Column(
        get_uuid_column(),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    section_id = Column(String(100), nullable=False, index=True)  # Section/slide identifier
    feedback_type = Column(
        SQLEnum(FeedbackType),
        nullable=False
    )  # Like or dislike
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="feedback_records")
    
    # Composite indexes for performance
    __table_args__ = (
        Index('idx_feedback_document_section', 'document_id', 'section_id'),
        Index('idx_feedback_section_created', 'section_id', 'created_at'),
        # Unique constraint: one feedback per section (latest wins)
        Index('idx_feedback_unique_section', 'document_id', 'section_id', unique=True),
    )
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, document_id={self.document_id}, section_id={self.section_id}, type={self.feedback_type})>"

