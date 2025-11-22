"""
Input validation utilities
"""
from typing import Any, Dict


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> bool:
    """Validate password strength (minimum 8 characters)"""
    return len(password) >= 8


def validate_document_structure(structure: Dict[str, Any], doc_type: str) -> bool:
    """Validate document structure based on type"""
    if doc_type == "word":
        # Word documents should have sections with headers
        return "sections" in structure and isinstance(structure["sections"], list)
    elif doc_type == "powerpoint":
        # PowerPoint should have slides with titles
        return "slides" in structure and isinstance(structure["slides"], list)
    return False

