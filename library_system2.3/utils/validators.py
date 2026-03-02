"""
Validation utilities
"""
import re
from typing import Any, Union


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_isbn(isbn: str) -> bool:
    """
    Validate ISBN format (ISBN-10 or ISBN-13)
    
    Args:
        isbn: ISBN to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove hyphens and spaces
    isbn_clean = re.sub(r'[-\s]', '', isbn)
    
    # Check ISBN-10
    if len(isbn_clean) == 10 and isbn_clean[:-1].isdigit() and (isbn_clean[-1].isdigit() or isbn_clean[-1] == 'X'):
        return True
    
    # Check ISBN-13
    if len(isbn_clean) == 13 and isbn_clean.isdigit():
        return True
    
    return False


def validate_item_id(item_id: str) -> bool:
    """
    Validate item ID format
    
    Args:
        item_id: Item ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not item_id or len(item_id) < 3:
        return False
    
    # Allow letters, numbers, and hyphens
    return bool(re.match(r'^[A-Za-z0-9-]+$', item_id))


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format
    
    Args:
        user_id: User ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not user_id or len(user_id) < 3:
        return False
    
    # Allow letters, numbers, hyphens, and underscores
    return bool(re.match(r'^[A-Za-z0-9_-]+$', user_id))


def validate_positive_number(value: Any, allow_zero: bool = False) -> bool:
    """
    Validate that a value is a positive number
    
    Args:
        value: Value to validate
        allow_zero: Whether zero is allowed
        
    Returns:
        True if valid, False otherwise
    """
    try:
        num = float(value)
        if allow_zero:
            return num >= 0
        return num > 0
    except (ValueError, TypeError):
        return False


def validate_string_length(value: str, min_len: int = 1, max_len: int = 100) -> bool:
    """
    Validate string length
    
    Args:
        value: String to validate
        min_len: Minimum length
        max_len: Maximum length
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    return min_len <= len(value.strip()) <= max_len