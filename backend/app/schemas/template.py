"""
Template schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID


class ColorPalette(BaseModel):
    """Color palette configuration"""
    primary: str = Field(..., description="Primary brand color (hex)")
    secondary: str = Field(..., description="Secondary brand color (hex)")
    accent: str = Field(..., description="Accent color (hex)")
    text: str = Field(..., description="Body text color (hex)")
    background: str = Field(..., description="Background color (hex)")
    heading: str = Field(..., description="Heading color (hex)")
    body: str = Field(..., description="Body text color (hex)")


class Typography(BaseModel):
    """Typography configuration"""
    heading_font: str = Field(..., description="Font for headings")
    body_font: str = Field(..., description="Font for body text")
    heading_size: int = Field(..., ge=8, le=144, description="Heading font size in points")
    body_size: int = Field(..., ge=8, le=72, description="Body font size in points")
    heading_weight: str = Field(default="bold", description="Heading font weight")
    body_weight: str = Field(default="normal", description="Body font weight")
    line_height: float = Field(default=1.5, ge=1.0, le=3.0, description="Line height multiplier")


class Spacing(BaseModel):
    """Spacing configuration"""
    section_margin: int = Field(default=24, ge=0, description="Margin between sections in points")
    paragraph_spacing: int = Field(default=12, ge=0, description="Spacing between paragraphs in points")
    title_margin_bottom: int = Field(default=18, ge=0, description="Bottom margin for title in points")
    content_padding: int = Field(default=16, ge=0, description="Content padding in points")


class Layout(BaseModel):
    """Layout configuration"""
    slide_width: float = Field(default=10, ge=5, le=20, description="Slide width in inches (PowerPoint)")
    slide_height: float = Field(default=7.5, ge=5, le=20, description="Slide height in inches (PowerPoint)")
    slide_layout: str = Field(default="title_content", description="Slide layout type")
    document_margins: Optional[Dict[str, float]] = Field(
        default=None,
        description="Document margins in inches (top, bottom, left, right)"
    )


class Styles(BaseModel):
    """Additional style configuration"""
    heading_alignment: str = Field(default="left", description="Heading alignment")
    body_alignment: str = Field(default="left", description="Body text alignment")
    title_alignment: str = Field(default="center", description="Title alignment")
    bullet_style: str = Field(default="default", description="Bullet point style")


class TemplateConfig(BaseModel):
    """Complete template configuration"""
    color_palette: ColorPalette
    typography: Typography
    spacing: Spacing
    layout: Layout
    styles: Styles


class TemplateBase(BaseModel):
    """Base template schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    document_type: str = Field(..., pattern="^(word|powerpoint)$", description="Document type")
    config: TemplateConfig
    is_default: bool = Field(default=False, description="Set as default template")
    is_public: bool = Field(default=False, description="Make template public (future feature)")


class TemplateCreate(TemplateBase):
    """Schema for creating a template"""
    pass


class TemplateUpdate(BaseModel):
    """Schema for updating a template"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    config: Optional[TemplateConfig] = None
    is_default: Optional[bool] = None
    is_public: Optional[bool] = None


class TemplateResponse(TemplateBase):
    """Schema for template response"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TemplateListResponse(BaseModel):
    """Schema for template list response"""
    templates: list[TemplateResponse]
    total: int

