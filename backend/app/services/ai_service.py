"""
AI service for Gemini API integration - Template and content generation
"""
import google.generativeai as genai
from app.core.config import settings
from app.models.project import DocumentType
from app.schemas.document import AITemplateRequest, AITemplateResponse
from typing import Dict, Any, Optional
import json
import uuid
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def initialize_gemini():
    """Initialize Gemini API client"""
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "":
        raise ValueError("GEMINI_API_KEY is not set in environment variables. Please set it to use AI features.")
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use gemini-2.0-flash as it's the latest stable model
        # Fallback to gemini-pro-latest if needed
        try:
            return genai.GenerativeModel('gemini-2.0-flash')
        except Exception:
            # Fallback to latest pro model
            return genai.GenerativeModel('gemini-pro-latest')
    except Exception as e:
        raise ValueError(f"Failed to initialize Gemini API: {str(e)}")


def generate_word_outline(main_topic: str) -> Dict[str, Any]:
    """
    Generate Word document outline using Gemini API
    
    Args:
        main_topic: Main topic for the document
        
    Returns:
        Dictionary with sections structure
    """
    try:
        model = initialize_gemini()
        
        prompt = f"""Generate a comprehensive outline for a Word document about: {main_topic}

Please provide a structured outline with 5-8 sections. Each section should have a clear, descriptive title.

Return the response as a JSON array of sections, where each section has:
- id: a unique identifier (e.g., "section-1", "section-2")
- title: the section title/header
- order: the order number (starting from 0)

Example format:
[
  {{"id": "section-1", "title": "Introduction", "order": 0}},
  {{"id": "section-2", "title": "Background", "order": 1}},
  ...
]

Return ONLY the JSON array, no additional text or explanation."""

        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        sections = json.loads(response_text)
        
        # Validate and format
        if not isinstance(sections, list):
            raise ValueError("Response is not a list")
        
        formatted_sections = []
        for i, section in enumerate(sections):
            if not isinstance(section, dict):
                continue
            
            formatted_sections.append({
                "id": section.get("id", f"section-{i+1}"),
                "title": section.get("title", f"Section {i+1}"),
                "order": section.get("order", i)
            })
        
        return {
            "sections": formatted_sections
        }
        
    except json.JSONDecodeError as e:
        # Fallback: Generate a basic outline
        return generate_fallback_word_outline(main_topic)
    except Exception as e:
        # Fallback: Generate a basic outline
        return generate_fallback_word_outline(main_topic)


def generate_powerpoint_slides(main_topic: str) -> Dict[str, Any]:
    """
    Generate PowerPoint slide structure using Gemini API
    
    Args:
        main_topic: Main topic for the presentation
        
    Returns:
        Dictionary with slides structure
    """
    try:
        model = initialize_gemini()
        
        prompt = f"""Generate a slide structure for a PowerPoint presentation about: {main_topic}

Please provide 6-10 slides with clear, concise titles. The first slide should be a title slide.

Return the response as a JSON array of slides, where each slide has:
- id: a unique identifier (e.g., "slide-1", "slide-2")
- title: the slide title
- order: the order number (starting from 0)

Example format:
[
  {{"id": "slide-1", "title": "Title Slide", "order": 0}},
  {{"id": "slide-2", "title": "Overview", "order": 1}},
  ...
]

Return ONLY the JSON array, no additional text or explanation."""

        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        slides = json.loads(response_text)
        
        # Validate and format
        if not isinstance(slides, list):
            raise ValueError("Response is not a list")
        
        formatted_slides = []
        for i, slide in enumerate(slides):
            if not isinstance(slide, dict):
                continue
            
            formatted_slides.append({
                "id": slide.get("id", f"slide-{i+1}"),
                "title": slide.get("title", f"Slide {i+1}"),
                "order": slide.get("order", i)
            })
        
        return {
            "slides": formatted_slides
        }
        
    except json.JSONDecodeError as e:
        # Fallback: Generate a basic structure
        return generate_fallback_powerpoint_slides(main_topic)
    except Exception as e:
        # Fallback: Generate a basic structure
        return generate_fallback_powerpoint_slides(main_topic)


def generate_fallback_word_outline(main_topic: str) -> Dict[str, Any]:
    """Generate a fallback Word outline if AI fails"""
    return {
        "sections": [
            {"id": "section-1", "title": "Introduction", "order": 0},
            {"id": "section-2", "title": "Background", "order": 1},
            {"id": "section-3", "title": "Analysis", "order": 2},
            {"id": "section-4", "title": "Findings", "order": 3},
            {"id": "section-5", "title": "Conclusion", "order": 4}
        ]
    }


def generate_fallback_powerpoint_slides(main_topic: str) -> Dict[str, Any]:
    """Generate a fallback PowerPoint structure if AI fails"""
    return {
        "slides": [
            {"id": "slide-1", "title": "Title Slide", "order": 0},
            {"id": "slide-2", "title": "Overview", "order": 1},
            {"id": "slide-3", "title": "Key Points", "order": 2},
            {"id": "slide-4", "title": "Details", "order": 3},
            {"id": "slide-5", "title": "Conclusion", "order": 4}
        ]
    }


def generate_template(
    main_topic: str,
    document_type: DocumentType
) -> Dict[str, Any]:
    """
    Generate document template structure using AI
    
    Args:
        main_topic: Main topic for the document
        document_type: Type of document (word or powerpoint)
        
    Returns:
        Dictionary with generated structure
    """
    if document_type == DocumentType.WORD:
        return generate_word_outline(main_topic)
    elif document_type == DocumentType.POWERPOINT:
        return generate_powerpoint_slides(main_topic)
    else:
        raise ValueError(f"Invalid document type: {document_type}")


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator for retrying function calls on failure
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
                    else:
                        raise last_exception
            return None
        return wrapper
    return decorator


@retry_on_failure(max_retries=3, delay=1.0)
def generate_section_content(
    main_topic: str,
    section_title: str,
    section_id: str,
    previous_sections: Optional[list] = None
) -> str:
    """
    Generate content for a Word document section using Gemini API
    
    Args:
        main_topic: Main topic of the document
        section_title: Title of the section
        section_id: Unique identifier of the section
        previous_sections: List of previous section titles for context
        
    Returns:
        Generated content text for the section
        
    Raises:
        ValueError: If API key is not set or generation fails
    """
    try:
        model = initialize_gemini()
        
        # Build context from previous sections
        context = ""
        if previous_sections:
            context = f"\n\nPrevious sections in this document:\n"
            for prev_section in previous_sections:
                context += f"- {prev_section}\n"
        
        prompt = f"""Write comprehensive content for a section in a document about: {main_topic}

Section Title: {section_title}
{context}

Requirements:
- Write detailed, informative content for this section
- The content should be well-structured and professional
- Include relevant information, analysis, or discussion
- Write 3-5 paragraphs (approximately 300-500 words)
- Make it contextually relevant to the main topic: {main_topic}
- Ensure the content flows naturally and is engaging

Write only the content for this section, without the section title or any headers."""

        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Clean up the content
        if not content:
            raise ValueError("Generated content is empty")
        
        return content
        
    except Exception as e:
        # Log the actual error for debugging
        logger.error(f"Error generating content for section '{section_title}': {str(e)}", exc_info=True)
        # If all retries fail, return a placeholder
        return f"[Content generation failed for section '{section_title}'. Please try again or refine manually.]"


@retry_on_failure(max_retries=3, delay=1.0)
def generate_slide_content(
    main_topic: str,
    slide_title: str,
    slide_id: str,
    previous_slides: Optional[list] = None
) -> str:
    """
    Generate content for a PowerPoint slide using Gemini API
    
    Args:
        main_topic: Main topic of the presentation
        slide_title: Title of the slide
        slide_id: Unique identifier of the slide
        previous_slides: List of previous slide titles for context
        
    Returns:
        Generated content text for the slide
        
    Raises:
        ValueError: If API key is not set or generation fails
    """
    try:
        model = initialize_gemini()
        
        # Build context from previous slides
        context = ""
        if previous_slides:
            context = f"\n\nPrevious slides in this presentation:\n"
            for prev_slide in previous_slides:
                context += f"- {prev_slide}\n"
        
        prompt = f"""Write content for a slide in a presentation about: {main_topic}

Slide Title: {slide_title}
{context}

Requirements:
- Write concise, bullet-point style content suitable for a presentation slide
- Include 3-6 key points or bullet points
- Keep it brief and impactful (suitable for a slide)
- Make it contextually relevant to the main topic: {main_topic}
- Use clear, professional language
- Format as bullet points (use • or - for each point)

Write only the content for this slide, without the slide title."""

        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Clean up the content
        if not content:
            raise ValueError("Generated content is empty")
        
        return content
        
    except Exception as e:
        # If all retries fail, return a placeholder
        return f"[Content generation failed for slide '{slide_title}'. Please try again or refine manually.]"


def generate_all_content(
    main_topic: str,
    structure: Dict[str, Any],
    document_type: DocumentType
) -> Dict[str, str]:
    """
    Generate content for all sections/slides in a document
    
    Args:
        main_topic: Main topic of the document
        structure: Document structure (sections or slides)
        document_type: Type of document (word or powerpoint)
        
    Returns:
        Dictionary mapping section/slide IDs to generated content
    """
    content_dict = {}
    
    if document_type == DocumentType.WORD:
        sections = structure.get("sections", [])
        previous_titles = []
        
        # Sort sections by order
        sorted_sections = sorted(sections, key=lambda x: x.get("order", 0))
        
        for section in sorted_sections:
            section_id = section.get("id")
            section_title = section.get("title", "")
            
            if not section_id or not section_title:
                continue
            
            # Generate content for this section
            try:
                content = generate_section_content(
                    main_topic=main_topic,
                    section_title=section_title,
                    section_id=section_id,
                    previous_sections=previous_titles if previous_titles else None
                )
                content_dict[section_id] = content
                previous_titles.append(section_title)
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error generating content for section '{section_title}': {str(e)}", exc_info=True)
                content_dict[section_id] = f"[Content generation failed for section '{section_title}'. Please try again or refine manually.]"
    
    elif document_type == DocumentType.POWERPOINT:
        slides = structure.get("slides", [])
        previous_titles = []
        
        # Sort slides by order
        sorted_slides = sorted(slides, key=lambda x: x.get("order", 0))
        
        for slide in sorted_slides:
            slide_id = slide.get("id")
            slide_title = slide.get("title", "")
            
            if not slide_id or not slide_title:
                continue
            
            # Generate content for this slide
            try:
                content = generate_slide_content(
                    main_topic=main_topic,
                    slide_title=slide_title,
                    slide_id=slide_id,
                    previous_slides=previous_titles if previous_titles else None
                )
                content_dict[slide_id] = content
                previous_titles.append(slide_title)
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error generating content for slide '{slide_title}': {str(e)}", exc_info=True)
                content_dict[slide_id] = f"[Content generation failed for slide '{slide_title}'. Please try again or refine manually.]"
    
    return content_dict
