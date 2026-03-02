"""
Library User model - multiple inheritance from Person and Borrower
"""
from datetime import datetime, timedelta
from typing import List

from models.users.base_user import Person, Borrower


class LibraryUser(Person, Borrower):
    """
    Library User - multiple inheritance from Person and Borrower
    Demonstrates: Multiple inheritance, MRO (Method Resolution Order)
    """
    
    def __init__(self, name: str, email: str, user_id: str, **kwargs):
        """
        Initialize a library user
        
        Args:
            name: User's full name
            email: Email address
            user_id: Unique user ID
            **kwargs: Additional arguments
        """
        # Initialize parent classes
        Person.__init__(self, name, email, **kwargs)
        Borrower.__init__(self)
        
        self.user_id = user_id
        self._membership_level = kwargs.get('membership_level', "Basic")
        self.join_date = kwargs.get('join_date', datetime.now())
        self.borrowing_history = kwargs.get('borrowing_history', [])
        self.fines_owed = kwargs.get('fines_owed', 0.0)
        
        # Ensure borrowed_items exists (should come from Borrower)
        if not hasattr(self, 'borrowed_items'):
            self.borrowed_items = []
    
    def __len__(self) -> int:
        """Operator overloading - len() returns borrowed items count"""
        return len(self.borrowed_items)
    
    def __add__(self, days: int) -> datetime:
        """Operator overloading - + adds days to join date"""
        if isinstance(days, (int, float)):
            return self.join_date + timedelta(days=days)
        raise TypeError(f"Can't add {type(days)} to LibraryUser")
    
    def __iadd__(self, fine: float):
        """Operator overloading - += adds fines"""
        if isinstance(fine, (int, float)):
            self.fines_owed += fine
            return self
        raise TypeError(f"Can't add {type(fine)} to fines")
    
    @property
    def membership_level(self) -> str:
        return self._membership_level
    
    @membership_level.setter
    def membership_level(self, level: str):
        """Set membership level with validation"""
        valid_levels = ["Basic", "Premium", "VIP"]
        if level not in valid_levels:
            raise ValueError(f"Membership level must be one of: {valid_levels}")
        self._membership_level = level
        self.update_timestamp()
    
    @property
    def max_borrow_limit(self) -> int:
        """Property to maintain compatibility with Borrower class"""
        return self.get_max_borrow_limit()
    
    def get_max_borrow_limit(self) -> int:
        """Get maximum borrow limit based on membership"""
        limits = {
            "Basic": 3,
            "Premium": 5,
            "VIP": 10
        }
        return limits.get(self._membership_level, 3)
    
    def can_borrow_more(self) -> bool:
        """Check if user can borrow more items"""
        return len(self.borrowed_items) < self.max_borrow_limit
    
    def borrow_item(self, item) -> bool:
        """Override borrow_item with membership check"""
        if not self.can_borrow_more():
            raise ValueError(f"Cannot borrow more than {self.max_borrow_limit} items")
        
        # Call parent's borrow_item
        success = super().borrow_item(item)
        
        if success:
            self.borrowing_history.append({
                'item_id': item.item_id,
                'title': item.title,
                'borrowed_date': datetime.now()
            })
        return success
    
    def return_item(self, item) -> bool:
        """Return an item"""
        if item in self.borrowed_items:
            success = super().return_item(item)
            if success:
                # Update borrowing history if needed
                pass
            return success
        return False
    
    def get_user_info(self) -> str:
        """Get formatted user information"""
        contact = Person.get_contact_info(self)
        return (f"{contact}\n"
                f"🆔 ID: {self.user_id}\n"
                f"⭐ Membership: {self.membership_level}\n"
                f"📅 Joined: {self.join_date.strftime('%Y-%m-%d')}\n"
                f"📚 Borrowed: {len(self.borrowed_items)}/{self.max_borrow_limit}\n"
                f"💰 Fines: ${self.fines_owed:.2f}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = Person.to_dict(self)
        data.update({
            'user_id': self.user_id,
            'membership_level': self._membership_level,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'fines_owed': self.fines_owed,
            'borrowed_items': [item.item_id for item in self.borrowed_items],
            'user_type': 'library_user'
        })
        return data