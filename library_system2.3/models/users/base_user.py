"""
Base user classes - Person base class and Borrower mixin
Demonstrates: Composition, Mixins, Multiple inheritance preparation
"""
from typing import List
from datetime import datetime

from models.base import BaseModel
from models.items.base_item import LibraryItem


class Person(BaseModel):
    """Base class for all people in the system"""
    
    def __init__(self, name: str, email: str, **kwargs):
        """
        Initialize a person
        
        Args:
            name: Person's full name
            email: Email address
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self.phone = kwargs.get('phone', '')
        self.address = kwargs.get('address', '')
    
    def get_contact_info(self) -> str:
        """Get formatted contact information"""
        info = f"{self.name} <{self.email}>"
        if self.phone:
            info += f" | 📞 {self.phone}"
        return info
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address
        })
        return data
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"


# models/users/borrower.py
from datetime import datetime, timedelta

class Borrower:
    """Borrower mixin class for borrowing functionality"""
    
    def __init__(self):
        self.borrowed_items = []
        self._max_borrow_limit = 5  # Default limit
    
    @property
    def max_borrow_limit(self) -> int:
        """Get maximum borrow limit"""
        return self._max_borrow_limit
    
    @max_borrow_limit.setter
    def max_borrow_limit(self, limit: int):
        """Set maximum borrow limit"""
        if limit < 0:
            raise ValueError("Borrow limit cannot be negative")
        self._max_borrow_limit = limit
    
    def borrow_item(self, item) -> bool:
        """Borrow an item"""
        if len(self.borrowed_items) >= self.max_borrow_limit:
            return False
        
        if item not in self.borrowed_items:
            self.borrowed_items.append(item)
            # Set due date (14 days from now)
            item.due_date = datetime.now() + timedelta(days=14)
            return True
        return False
    
    def return_item(self, item) -> bool:
        """Return an item"""
        if item in self.borrowed_items:
            self.borrowed_items.remove(item)
            item.due_date = None
            item.is_available = True
            return True
        return False