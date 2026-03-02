"""
Librarian model - demonstrates composition (has-a LibraryCard)
"""
from datetime import datetime

from models.users.base_user import Person


class Librarian(Person):
    """
    Librarian class - demonstrates composition
    A Librarian HAS-A LibraryCard (inner class)
    """
    
    class LibraryCard:
        """Inner class - composition relationship"""
        
        def __init__(self, card_number: str, issue_date: datetime, access_level: str = "Full"):
            self.card_number = card_number
            self.issue_date = issue_date
            self.access_level = access_level
            self.expiry_date = datetime.now().replace(year=datetime.now().year + 2)
        
        def renew(self, years: int = 2) -> None:
            """Renew the library card"""
            self.expiry_date = self.expiry_date.replace(
                year=self.expiry_date.year + years
            )
        
        def is_valid(self) -> bool:
            """Check if card is still valid"""
            return datetime.now() < self.expiry_date
        
        def __str__(self):
            return (f"🪪 Card: {self.card_number} | Level: {self.access_level} | "
                    f"Expires: {self.expiry_date.strftime('%Y-%m-%d')}")
    
    def __init__(self, name: str, email: str, employee_id: str, **kwargs):
        """
        Initialize a librarian
        
        Args:
            name: Librarian's full name
            email: Email address
            employee_id: Employee ID
            **kwargs: Additional arguments
        """
        super().__init__(name, email, **kwargs)
        self.employee_id = employee_id
        self.department = kwargs.get('department', 'General')
        self.hire_date = kwargs.get('hire_date', datetime.now())
        
        # Composition: Librarian HAS-A LibraryCard
        card_number = kwargs.get('card_number', f"LIB-{employee_id}")
        self._library_card = self.LibraryCard(
            card_number=card_number,
            issue_date=self.hire_date,
            access_level=kwargs.get('access_level', 'Full')
        )
    
    @property
    def library_card(self):
        """Get the librarian's library card"""
        return self._library_card
    
    def manage_item(self, item, action: str) -> str:
        """
        Perform management actions on library items
        
        Args:
            item: Library item to manage
            action: Action to perform (add, remove, update)
            
        Returns:
            Status message
        """
        actions = {
            "add": "➕ added to catalog",
            "remove": "❌ removed from catalog",
            "update": "✏️ updated in catalog",
            "process": "📋 processed"
        }
        
        item_title = getattr(item, 'title', str(item))
        return f"{self.name} {actions.get(action, 'processed')}: '{item_title}'"
    
    def issue_card(self, user) -> str:
        """Issue a library card to a user"""
        card_id = f"CARD-{user.get_id()}-{datetime.now().strftime('%Y%m')}"
        return f"✅ Card '{card_id}' issued to {user.name}"
    
    def get_librarian_info(self) -> str:
        """Get formatted librarian information"""
        contact = Person.get_contact_info(self)
        card_valid = "✅ Valid" if self.library_card.is_valid() else "❌ Expired"
        return (f"{contact}\n"
                f"🆔 Employee: {self.employee_id}\n"
                f"🏢 Department: {self.department}\n"
                f"📅 Hired: {self.hire_date.strftime('%Y-%m-%d')}\n"
                f"🪪 {self.library_card}\n"
                f"📊 Card Status: {card_valid}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = Person.to_dict(self)
        data.update({
            'employee_id': self.employee_id,
            'department': self.department,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'card_number': self.library_card.card_number,
            'access_level': self.library_card.access_level,
            'user_type': 'librarian'
        })
        return data