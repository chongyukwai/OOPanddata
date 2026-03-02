"""
Library Service - Core service for library operations
"""
import sys
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from services/
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models.items.book import Book
from models.items.ebook import EBook
from models.items.magazine import Magazine
from models.users.library_user import LibraryUser
from models.users.librarian import Librarian
from services.exceptions import ItemNotFoundException


class LibraryService:
    """Singleton service for library management"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if getattr(self, '_initialized', False):
            return
            
        self._initialized = True
        self._items: Dict[str, Any] = {}  # Store items by ID
        self._users: Dict[str, LibraryUser] = {}  # Store regular users by user_id
        self._librarians: Dict[str, Librarian] = {}  # Store librarians by employee_id
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data for testing"""
        # Add sample users - pass membership_level as keyword argument
        user1 = LibraryUser("Alice Johnson", "alice@email.com", "USR001", membership_level="Premium")
        user2 = LibraryUser("Bob Wilson", "bob@email.com", "USR002", membership_level="Basic")
        user3 = LibraryUser("sad", "sd@link.edu.hk", "USR003", membership_level="Basic")
        
        self._users[user1.user_id] = user1
        self._users[user2.user_id] = user2
        self._users[user3.user_id] = user3
        
        # Add sample librarian
        librarian = Librarian("John Smith", "john@library.com", "EMP001")
        self._librarians[librarian.employee_id] = librarian
        
        # Add sample items
        book1 = Book("Python Programming", "BK001", "John Doe", "1234567890", 350)
        book2 = Book("Data Structures", "BK002", "Jane Smith", "0987654321", 400)
        ebook1 = EBook("Advanced Python", "EB001", "Jim Brown", "978-1234567", 350, 5.2, "PDF")
        magazine1 = Magazine("Tech Monthly", "MG001", 42, "Tech Media", publication_date="2024-01")
        
        self._items[book1.item_id] = book1
        self._items[book2.item_id] = book2
        self._items[ebook1.item_id] = ebook1
        self._items[magazine1.item_id] = magazine1
        
        # Instead of trying to set is_available directly, we need to understand
        # how the LibraryItem base class handles availability. Since is_available is a property
        # without a setter, availability might be determined by other attributes.
        
        # For now, we'll just add items to the user's borrowed_items list
        # This should be enough for the UI to show them as borrowed
        user1.borrowed_items.append(book1)
        user1.borrowed_items.append(ebook1)
        
        # Set due dates for testing
        book1.due_date = datetime.now() + timedelta(days=14)
        ebook1.due_date = datetime.now() + timedelta(days=7)
        
        # We're not trying to set is_available directly
        # The is_available property might be computed based on whether the item has a due_date or is in someone's borrowed_items
    
    def get_all_users(self) -> List[LibraryUser]:
        """Get all regular users"""
        return list(self._users.values())
    
    def get_all_librarians(self) -> List[Librarian]:
        """Get all librarians"""
        return list(self._librarians.values())
    
    def get_all_items(self) -> List[Any]:
        """Get all items"""
        return list(self._items.values())
    
    def get_available_items(self) -> List[Any]:
        """Get all available items"""
        # Since is_available is a property without a setter, we need to determine
        # availability by checking if the item is in any user's borrowed_items list
        available_items = []
        for item in self._items.values():
            is_borrowed = False
            for user in self._users.values():
                if item in user.borrowed_items:
                    is_borrowed = True
                    break
            if not is_borrowed:
                available_items.append(item)
        return available_items
    
    def get_user(self, user_id: str) -> Optional[LibraryUser]:
        """Get a user by ID"""
        if user_id in self._users:
            return self._users[user_id]
        return None
    
    def get_librarian(self, employee_id: str) -> Optional[Librarian]:
        """Get a librarian by employee ID"""
        return self._librarians.get(employee_id)
    
    def get_item(self, item_id: str) -> Optional[Any]:
        """Get an item by ID"""
        return self._items.get(item_id)
    
    def add_user(self, user: LibraryUser) -> str:
        """Add a new user"""
        if user.user_id in self._users:
            return f"❌ User ID {user.user_id} already exists"
        
        self._users[user.user_id] = user
        return f"✅ User {user.name} added successfully"
    
    def add_librarian(self, librarian: Librarian) -> str:
        """Add a new librarian"""
        if librarian.employee_id in self._librarians:
            return f"❌ Employee ID {librarian.employee_id} already exists"
        
        self._librarians[librarian.employee_id] = librarian
        return f"✅ Librarian {librarian.name} added successfully"
    
    def add_item(self, item: Any) -> str:
        """Add a new item"""
        if item.item_id in self._items:
            return f"❌ Item ID {item.item_id} already exists"
        
        self._items[item.item_id] = item
        return f"✅ Item {item.title} added successfully"
    
    def find_item_by_id(self, item_id):
        """Find an item by its ID"""
        if item_id in self._items:
            return self._items[item_id]
        return None
    
    def is_item_available(self, item):
        """Check if an item is available by seeing if it's in any user's borrowed_items"""
        for user in self._users.values():
            if item in user.borrowed_items:
                return False
        return True
    
    def borrow_item(self, item_id, user):
        """Borrow an item"""
        try:
            # Find the item using the dictionary
            item = self._items.get(item_id)
            
            if not item:
                return False, f"Item {item_id} not found"
            
            # Check if item is available (not in any user's borrowed_items)
            if not self.is_item_available(item):
                return False, f"Item {item_id} is not available"
            
            # Check if user can borrow more items
            if len(user.borrowed_items) >= user.max_borrow_limit:
                return False, f"User {user.name} has reached maximum borrow limit"
            
            # Add item to user's borrowed items
            user.borrowed_items.append(item)
            
            # Set due date (14 days from now)
            item.due_date = datetime.now() + timedelta(days=14)
            
            return True, f"Item '{item.title}' borrowed successfully. Due date: {item.due_date.strftime('%Y-%m-%d')}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def return_item(self, item_id, user):
        """Return a borrowed item"""
        try:
            # Find the item
            item = self._items.get(item_id)
            
            if not item:
                return False, f"Item {item_id} not found"
            
            # Check if the user actually has this item borrowed
            if item not in user.borrowed_items:
                return False, f"Item {item_id} is not borrowed by {user.name}"
            
            # Remove from user's borrowed items
            user.borrowed_items.remove(item)
            
            # Calculate any fines if overdue
            fine_message = ""
            if hasattr(item, 'due_date') and item.due_date:
                if datetime.now() > item.due_date:
                    # Calculate fine (e.g., $0.50 per day overdue)
                    days_overdue = (datetime.now() - item.due_date).days
                    fine_amount = days_overdue * 0.50
                    user.fines_owed += fine_amount
                    fine_message = f" Late fee: ${fine_amount:.2f}"
            
            # Clear the due date
            item.due_date = None
            
            return True, f"Item '{item.title}' returned successfully.{fine_message}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def pay_fines(self, user_id: str, amount: float) -> str:
        """Pay fines for a user"""
        user = self.get_user(user_id)
        if not user:
            return f"❌ User {user_id} not found"
        
        if amount <= 0:
            return "❌ Payment amount must be positive"
        
        if amount > user.fines_owed:
            return f"❌ Payment amount (${amount:.2f}) exceeds fines owed (${user.fines_owed:.2f})"
        
        user.fines_owed -= amount
        return f"✅ Payment of ${amount:.2f} successful. Remaining fines: ${user.fines_owed:.2f}"
    
    def get_catalog_stats(self) -> Dict[str, int]:
        """Get catalog statistics"""
        from models.items.book import Book
        from models.items.ebook import EBook
        from models.items.magazine import Magazine
        
        total_items = len(self._items)
        
        # Calculate available items by checking if they're in any user's borrowed_items
        available_items = 0
        for item in self._items.values():
            if self.is_item_available(item):
                available_items += 1
        
        borrowed_items = total_items - available_items
        total_users = len(self._users)
        
        # Add specific counts for each item type
        books = sum(1 for item in self._items.values() if isinstance(item, Book))
        ebooks = sum(1 for item in self._items.values() if isinstance(item, EBook))
        magazines = sum(1 for item in self._items.values() if isinstance(item, Magazine))
        
        return {
            'total_items': total_items,
            'available_items': available_items,
            'borrowed_items': borrowed_items,
            'total_users': total_users,
            'books': books,
            'ebooks': ebooks,
            'magazines': magazines
        }
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics for dashboard"""
        total_users = len(self._users)
        total_librarians = len(self._librarians)
        
        # Calculate active users (users with borrowed items)
        active_users = sum(1 for user in self._users.values() if len(user.borrowed_items) > 0)
        
        # Calculate users with fines
        users_with_fines = sum(1 for user in self._users.values() if user.fines_owed > 0)
        
        # Calculate total fines owed
        total_fines = sum(user.fines_owed for user in self._users.values())
        
        # Calculate membership distribution
        membership_counts = {}
        for user in self._users.values():
            level = user.membership_level
            membership_counts[level] = membership_counts.get(level, 0) + 1
        
        return {
            'total_users': total_users,
            'total_librarians': total_librarians,
            'active_users': active_users,
            'users_with_fines': users_with_fines,
            'total_fines': total_fines,
            'membership_distribution': membership_counts
        }