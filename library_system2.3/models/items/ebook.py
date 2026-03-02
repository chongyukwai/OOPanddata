"""
EBook model - inherits from Book (multi-level inheritance)
"""
from models.items.book import Book


class EBook(Book):
    """EBook class extending Book (multi-level inheritance)"""
    
    def __init__(self, title: str, item_id: str, author: str, 
                 isbn: str, pages: int, file_size: float, 
                 format: str = "PDF", **kwargs):
        """
        Initialize an eBook
        
        Args:
            title: eBook title
            item_id: Unique identifier
            author: eBook author
            isbn: ISBN number
            pages: Number of pages
            file_size: File size in MB
            format: File format (PDF, EPUB, MOBI)
            **kwargs: Additional arguments
        """
        super().__init__(title, item_id, author, isbn, pages, **kwargs)
        self.file_size = file_size
        self.format = format.upper()
        self._download_count = kwargs.get('download_count', 0)
    
    def get_details(self) -> str:
        """Get detailed eBook information"""
        details = super().get_details()
        return (f"{details}\n"
                f"💾 File Size: {self.file_size} MB\n"
                f"📁 Format: {self.format}\n"
                f"⬇️ Downloads: {self._download_count}")
    
    def get_item_type(self) -> str:
        return "EBook"
    
    def download(self) -> str:
        """Simulate downloading the eBook"""
        self._download_count += 1
        self.update_timestamp()
        return f"⬇️ Downloading '{self.title}' in {self.format} format... (Download #{self._download_count})"
    
    @property
    def download_count(self) -> int:
        return self._download_count
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'file_size': self.file_size,
            'format': self.format,
            'download_count': self._download_count,
            'item_type': 'ebook'
        })
        return data