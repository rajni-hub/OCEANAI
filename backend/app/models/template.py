"""
Template model for document styling and formatting
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base, get_uuid_column


class Template(Base):
    """
    Template model storing visual design specifications for document exports
    
    Templates define:
    - Color palettes (primary, secondary, accent, text, background)
    - Typography (fonts, sizes, weights, line heights)
    - Spacing (margins, padding, section gaps)
    - Layout settings (slide dimensions, document styles)
    """
    
    __tablename__ = "templates"
    
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
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    document_type = Column(String(20), nullable=False)  # "word" or "powerpoint"
    
    # Template configuration stored as JSON
    # Structure:
    # {
    #   "color_palette": {
    #     "primary": "#1E40AF",
    #     "secondary": "#3B82F6",
    #     "accent": "#60A5FA",
    #     "text": "#000000",
    #     "background": "#FFFFFF",
    #     "heading": "#1E40AF",
    #     "body": "#000000"
    #   },
    #   "typography": {
    #     "heading_font": "Arial",
    #     "body_font": "Calibri",
    #     "heading_size": 44,
    #     "body_size": 18,
    #     "heading_weight": "bold",
    #     "body_weight": "normal",
    #     "line_height": 1.5
    #   },
    #   "spacing": {
    #     "section_margin": 24,
    #     "paragraph_spacing": 12,
    #     "title_margin_bottom": 18,
    #     "content_padding": 16
    #   },
    #   "layout": {
    #     "slide_width": 10,
    #     "slide_height": 7.5,
    #     "slide_layout": "title_content",
    #     "document_margins": {
    #       "top": 1,
    #       "bottom": 1,
    #       "left": 1,
    #       "right": 1
    #     }
    #   },
    #   "styles": {
    #     "heading_alignment": "left",
    #     "body_alignment": "left",
    #     "title_alignment": "center",
    #     "bullet_style": "default"
    #   }
    # }
    config = Column(JSON, nullable=False)
    
    is_default = Column(Boolean, default=False, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)  # For future: shared templates
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    owner = relationship("User", back_populates="templates")
    
    def __repr__(self):
        return f"<Template(id={self.id}, name={self.name}, type={self.document_type})>"

