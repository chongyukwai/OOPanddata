"""
Magazine model - inherits from LibraryItem
"""
from datetime import datetime

from models.items.base_item import LibraryItem


class Magazine(LibraryItem):
    """Magazine class extending LibraryItem"""
    
    def __init__(self, title: str, item_id: str, issue_number: int, 
                 publisher: str, **kwargs):
        """
        Initialize a magazine
        
        Args:
            title: Magazine title
            item_id: Unique identifier
            issue_number: Issue number
            publisher: Publisher name
            **kwargs: Additional arguments
        """
        super().__init__(title, item_id, **kwargs)
        self.issue_number = issue_number
        self.publisher = publisher
        self.publication_date = kwargs.get('publication_date', datetime.now())
    
    def get_details(self) -> str:
        """Get detailed magazine information"""
        pub_date = self.publication_date.strftime("%B %Y") if hasattr(self.publication_date, 'strftime') else str(self.publication_date)
        return (f"📰 Magazine: {self.title}\n"
                f"🔢 Issue: #{self.issue_number}\n"
                f"🏢 Publisher: {self.publisher}\n"
                f"📅 Published: {pub_date}\n"
                f"📊 Status: {'✅ Available' if self.is_available else '❌ Checked out'}")
    
    def get_item_type(self) -> str:
        return "Magazine"
    
    def checkout(self, user_id: str, max_days: int = 7) -> bool:
        """
        Check out with shorter borrowing period for magazines
        
        Args:
            user_id: User ID
            max_days: Maximum checkout days (default: 7)
        """
        success = super().checkout(user_id)
        if success:
            # Magazines have shorter checkout period
            self._due_date = datetime.now() + timedelta(days=max_days)
        return success
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'issue_number': self.issue_number,
            'publisher': self.publisher,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'item_type': 'magazine'
        })
        return data