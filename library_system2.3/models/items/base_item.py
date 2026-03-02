"""
Abstract base class for all library items
Demonstrates: Abstract classes, inheritance, encapsulation
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from models.base import BaseModel


class LibraryItem(BaseModel, ABC):
    """Abstract Base Class for all library items"""
    
    # Class variable - shared across all instances
    total_items = 0
    
    def __init__(self, title: str, item_id: str, **kwargs):
        """
        Initialize a library item
        
        Args:
            title: Item title
            item_id: Unique identifier
            **kwargs: Additional arguments for base class
        """
        super().__init__(**kwargs)
        
        # Private attributes - encapsulation
        self._title = title
        self._item_id = item_id
        self._is_available = True
        self._checkout_date: Optional[datetime] = None
        self._checkout_user_id: Optional[str] = None
        
        LibraryItem.total_items += 1
    
    @abstractmethod
    def get_details(self) -> str:
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_item_type(self) -> str:
        """Abstract method - returns item type"""
        pass
    
    @property
    def title(self) -> str:
        """Getter property - encapsulation"""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """Setter property with validation"""
        if not value or len(value.strip()) < 1:
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
        self.update_timestamp()
    
    @property
    def item_id(self) -> str:
        return self._item_id
    
    @property
    def is_available(self) -> bool:
        return self._is_available
    
    @property
    def checkout_date(self) -> Optional[datetime]:
        return self._checkout_date
    
    @property
    def checkout_user_id(self) -> Optional[str]:
        return self._checkout_user_id
    
    def checkout(self, user_id: str) -> bool:
        """
        Check out the item to a user
        
        Args:
            user_id: ID of user checking out the item
            
        Returns:
            True if successful, False otherwise
        """
        if self._is_available:
            self._is_available = False
            self._checkout_date = datetime.now()
            self._checkout_user_id = user_id
            self.update_timestamp()
            return True
        return False
    
    def return_item(self) -> bool:
        """Return the item to the library"""
        if not self._is_available:
            self._is_available = True
            self._checkout_date = None
            self._checkout_user_id = None
            self.update_timestamp()
            return True
        return False
    
    @classmethod
    def get_total_items(cls) -> int:
        """Class method - returns total items created"""
        return cls.total_items
    
    @staticmethod
    def validate_id(item_id: str) -> bool:
        """Static method - validates item ID format"""
        return len(item_id) >= 3 and item_id.replace('-', '').isalnum()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'title': self._title,
            'item_id': self._item_id,
            'is_available': self._is_available,
            'checkout_date': self._checkout_date.isoformat() if self._checkout_date else None,
            'checkout_user_id': self._checkout_user_id
        })
        return data
    
    def __str__(self):
        """String representation"""
        status = "✅ Available" if self._is_available else "❌ Checked out"
        return f"{self.__class__.__name__}: {self._title} (ID: {self._item_id}) - {status}"