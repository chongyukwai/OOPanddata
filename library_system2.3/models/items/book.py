"""
Book model - inherits from LibraryItem
"""
from typing import Optional

from models.items.base_item import LibraryItem


class Book(LibraryItem):
    """Book class extending LibraryItem"""
    
    def __init__(self, title: str, item_id: str, author: str, 
                 isbn: str, pages: int, **kwargs):
        """
        Initialize a book
        
        Args:
            title: Book title
            item_id: Unique identifier
            author: Book author
            isbn: ISBN number
            pages: Number of pages
            **kwargs: Additional arguments
        """
        super().__init__(title, item_id, **kwargs)
        self.author = author
        self.isbn = isbn
        self.pages = pages
        self._genre = kwargs.get('genre', "General")
    
    def get_details(self) -> str:
        """Get detailed book information"""
        return (f"📚 Book: {self.title}\n"
                f"✍️ Author: {self.author}\n"
                f"🏷️ ISBN: {self.isbn}\n"
                f"📄 Pages: {self.pages}\n"
                f"🎭 Genre: {self._genre}\n"
                f"📊 Status: {'✅ Available' if self.is_available else '❌ Checked out'}")
    
    def get_item_type(self) -> str:
        return "Book"
    
    @property
    def genre(self) -> str:
        return self._genre
    
    @genre.setter
    def genre(self, value: str):
        """Set genre with validation"""
        valid_genres = ["Fiction", "Non-Fiction", "Science", "History", 
                        "Biography", "Fantasy", "Mystery", "Romance", 
                        "Thriller", "Self-Help", "Technical", "General"]
        if value and value not in valid_genres:
            raise ValueError(f"Genre must be one of: {valid_genres}")
        self._genre = value or "General"
        self.update_timestamp()
    
    def calculate_reading_time(self, pages_per_hour: int = 30) -> float:
        """Calculate estimated reading time in hours"""
        return self.pages / pages_per_hour
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'author': self.author,
            'isbn': self.isbn,
            'pages': self.pages,
            'genre': self._genre,
            'item_type': 'book'
        })
        return data