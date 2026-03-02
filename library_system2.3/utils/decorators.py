"""
Decorators for the library system
"""
import time
import functools
from typing import Any, Callable
from datetime import datetime


def log_action(func: Callable) -> Callable:
    """
    Decorator to log function calls
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📝 Calling: {func.__name__}")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"   ✅ Completed in {elapsed:.3f}s")
        return result
    return wrapper


def timer(func: Callable) -> Callable:
    """
    Decorator to time function execution
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱️ {func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper


def require_librarian(func: Callable) -> Callable:
    """
    Decorator to require librarian privileges
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check if current user is a librarian
        current_user = getattr(self, 'current_user', None)
        if current_user and current_user.__class__.__name__ == 'Librarian':
            return func(self, *args, **kwargs)
        else:
            print("⛔ This action requires librarian privileges")
            return None
    return wrapper


def singleton(cls):
    """
    Class decorator for singleton pattern
    
    Args:
        cls: Class to make singleton
        
    Returns:
        Singleton class
    """
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


def validate_input(validators: dict):
    """
    Decorator to validate function arguments
    
    Args:
        validators: Dictionary mapping parameter names to validator functions
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Combine args and kwargs
            all_args = {}
            
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate each argument
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        raise ValueError(f"Invalid value for '{param_name}': {value}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on failure
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def deprecated(message: str = ""):
    """
    Decorator to mark functions as deprecated
    
    Args:
        message: Deprecation message
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"⚠️ DEPRECATED: {func.__name__} is deprecated. {message}")
            return func(*args, **kwargs)
        return wrapper
    return decorator