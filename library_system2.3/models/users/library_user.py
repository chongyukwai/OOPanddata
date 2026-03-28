"""
Library User model - multiple inheritance from Person and Borrower
"""
from datetime import datetime, timedelta
from typing import List

from models.users.base_user import Person, Borrower


class LibraryUser(Person, Borrower):
    """
    Library User - multiple inheritance from Person and Borrower
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
        Borrower.__init__(self)  # This creates the borrowed_items list
        
        self.user_id = user_id
        self._membership_level = kwargs.get('membership_level', "Basic")
        self.join_date = kwargs.get('join_date', datetime.now())
        self.borrowing_history = kwargs.get('borrowing_history', [])
        self.fines_owed = kwargs.get('fines_owed', 0.0)
        
        # IMPORTANT: Clear and add items from kwargs to the SAME list
        if 'borrowed_items' in kwargs and kwargs['borrowed_items']:
            # Clear the existing list (from Borrower.__init__)
            self.borrowed_items.clear()
            # Add items from kwargs
            for item in kwargs['borrowed_items']:
                self.borrowed_items.append(item)
    
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
        valid_levels = ["Basic", "Premium"]
        if level not in valid_levels:
            raise ValueError(f"Membership level must be one of: {valid_levels}")
        self._membership_level = level
        self.update_timestamp()
    
    @property
    def max_borrow_limit(self) -> int:
        """Get maximum borrow limit based on membership"""
        limits = {
            "Basic": 0,     # Basic members cannot borrow
            "Premium": 5    # Premium members can borrow up to 5 items
        }
        return limits.get(self._membership_level, 0)
    
    def can_borrow_more(self) -> bool:
        """Check if user can borrow more items"""
        if self.membership_level == "Basic":
            return False
        return len(self.borrowed_items) < self.max_borrow_limit
    
    def borrow_item(self, item) -> bool:
        """Override borrow_item with membership check"""
        if not self.can_borrow_more():
            if self.membership_level == "Basic":
                raise ValueError("Basic members cannot borrow items")
            else:
                raise ValueError(f"Cannot borrow more than {self.max_borrow_limit} items")
        
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
            return super().return_item(item)
        return False
    
    def get_overdue_items(self) -> List:
        """Get list of overdue items"""
        overdue = []
        now = datetime.now()
        for item in self.borrowed_items:
            if hasattr(item, 'due_date') and item.due_date and now > item.due_date:
                overdue.append(item)
        return overdue
    
    def get_user_info(self) -> str:
        """Get formatted user information"""
        contact = Person.get_contact_info(self)
        can_borrow = "Yes" if self.membership_level == "Premium" else "No"
        return (f"{contact}\n"
                f"🆔 ID: {self.user_id}\n"
                f"⭐ Membership: {self.membership_level}\n"
                f"📅 Joined: {self.join_date.strftime('%Y-%m-%d')}\n"
                f"📚 Borrowed: {len(self.borrowed_items)}/{self.max_borrow_limit}\n"
                f"✅ Can Borrow: {can_borrow}\n"
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