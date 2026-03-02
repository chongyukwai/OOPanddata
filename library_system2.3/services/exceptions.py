"""
Custom exceptions for the library system
"""


class LibraryException(Exception):
    """Base exception for all library-related errors"""
    pass


class ItemNotFoundException(LibraryException):
    """Raised when an item is not found in the catalog"""
    
    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(f"Item with ID '{item_id}' not found")


class ItemNotAvailableException(LibraryException):
    """Raised when an item is not available for checkout"""
    
    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(f"Item with ID '{item_id}' is not available")


class UserNotFoundException(LibraryException):
    """Raised when a user is not found in the system"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User with ID '{user_id}' not found")


class BorrowLimitExceededException(LibraryException):
    """Raised when a user tries to borrow more than their limit"""
    
    def __init__(self, user_id: str, limit: int):
        self.user_id = user_id
        self.limit = limit
        super().__init__(f"User {user_id} has reached borrow limit of {limit} items")


class InvalidItemTypeException(LibraryException):
    """Raised when an invalid item type is provided"""
    
    def __init__(self, item_type: str):
        self.item_type = item_type
        super().__init__(f"Invalid item type: '{item_type}'")


class DuplicateItemException(LibraryException):
    """Raised when trying to add an item with an existing ID"""
    
    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(f"Item with ID '{item_id}' already exists")


class DuplicateUserException(LibraryException):
    """Raised when trying to add a user with an existing ID"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User with ID '{user_id}' already exists")