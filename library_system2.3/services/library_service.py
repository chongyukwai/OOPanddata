"""
Library Service - Core service for library operations
"""
import sys
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models.items.book import Book
from models.items.ebook import EBook
from models.items.magazine import Magazine
from models.users.library_user import LibraryUser
from models.users.librarian import Librarian


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
        self._items: Dict[str, Any] = {}
        self._users: Dict[str, LibraryUser] = {}
        self._librarians: Dict[str, Librarian] = {}
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data for testing"""
        from datetime import datetime, timedelta
        
        # Create items
        items = []
        for i in range(1, 11):
            book = Book(
                title=f"Python Programming Vol {i}",
                item_id=f"BK{i:03d}",
                author=f"Author {i}",
                isbn=f"978-01348539{i:02d}",
                pages=500 + i
            )
            self._items[book.item_id] = book
            items.append(book)
        
        # Add ebooks
        ebook1 = EBook("Advanced Python", "EB001", "Jane Smith", "978-0134853988", 720, 2.5, "PDF")
        ebook2 = EBook("Python Data Science", "EB002", "Jake VanderPlas", "978-7654321", 450, 8.5, "EPUB")
        self._items[ebook1.item_id] = ebook1
        self._items[ebook2.item_id] = ebook2
        items.extend([ebook1, ebook2])
        
        # Add magazines
        magazine1 = Magazine("Tech Monthly", "MG001", 42, "Tech Media")
        magazine2 = Magazine("Science Weekly", "MG002", 15, "Science Publications")
        self._items[magazine1.item_id] = magazine1
        self._items[magazine2.item_id] = magazine2
        items.extend([magazine1, magazine2])
        
        # Create users
        # Premium user - Alice (can borrow)
        alice_items = [items[0], items[1], items[2]]
        user1 = LibraryUser(
            "Alice Johnson", 
            "alice@email.com", 
            "USR001", 
            membership_level="Premium",
            borrowed_items=alice_items
        )
        for item in alice_items:
            item.due_date = datetime.now() + timedelta(days=14)
        self._users[user1.user_id] = user1
        
        # Basic user - Bob (cannot borrow)
        user2 = LibraryUser("Bob Wilson", "bob@email.com", "USR002", membership_level="Basic")
        self._users[user2.user_id] = user2
        
        # Premium user - Charlie (can borrow)
        charlie_items = [items[3], items[4]]
        user3 = LibraryUser(
            "Charlie Brown", 
            "charlie@email.com", 
            "USR003", 
            membership_level="Premium",
            borrowed_items=charlie_items
        )
        for item in charlie_items:
            item.due_date = datetime.now() + timedelta(days=14)
        self._users[user3.user_id] = user3
        
        # Create librarian
        librarian_items = [items[5], items[6], items[7], items[8], items[9]]
        librarian = Librarian(
            "Carol Davis", 
            "carol@library.com", 
            "EMP001",
            borrowed_items=librarian_items
        )
        for i, item in enumerate(librarian_items):
            if i < 3:
                item.due_date = datetime.now() + timedelta(days=14)
            else:
                item.due_date = datetime.now() - timedelta(days=5)
        self._librarians[librarian.employee_id] = librarian
        
        # Add one more Basic user
        user4 = LibraryUser("David Miller", "david@email.com", "USR004", membership_level="Basic")
        self._users[user4.user_id] = user4
    
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
        available_items = []
        for item in self._items.values():
            if self.is_item_available(item):
                available_items.append(item)
        return available_items
    
    def get_user(self, user_id: str) -> Optional[LibraryUser]:
        """Get a user by ID"""
        return self._users.get(user_id)
    
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
        return self._items.get(item_id)
    
    def is_item_available(self, item):
        """Check if an item is available"""
        for user in self._users.values():
            if item in user.borrowed_items:
                return False
        for librarian in self._librarians.values():
            if item in librarian.borrowed_items:
                return False
        return True
    
    def borrow_item(self, item_id, user):
        """Borrow an item"""
        try:
            from datetime import datetime, timedelta
            
            item = self._items.get(item_id)
            
            if not item:
                return False, f"Item {item_id} not found"
            
            # Check if user is a Basic member
            if hasattr(user, 'membership_level') and user.membership_level == "Basic":
                return False, f"❌ Basic members ({user.name}) are not allowed to borrow items. Please upgrade to Premium membership."
            
            # Check if item is available
            if not self.is_item_available(item):
                return False, f"Item {item_id} is not available"
            
            # Check if user can borrow more items
            if len(user.borrowed_items) >= user.max_borrow_limit:
                return False, f"User {user.name} has reached maximum borrow limit of {user.max_borrow_limit}"
            
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
            from datetime import datetime
            
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
                    days_overdue = (datetime.now() - item.due_date).days
                    fine_amount = days_overdue * 0.50
                    user.fines_owed += fine_amount
                    fine_message = f" Late fee: ${fine_amount:.2f}"
            
            # Clear the due date
            item.due_date = None
            
            # Debug print to verify user still exists
            print(f"DEBUG - After return, user: {user.name}, still has {len(user.borrowed_items)} items")
            print(f"DEBUG - User object still valid: {user is not None}")
            
            return True, f"Item '{item.title}' returned successfully.{fine_message}"
                
        except Exception as e:
            print(f"DEBUG - Error in return_item: {e}")
            return False, f"Error: {str(e)}"
    
    def pay_fines(self, user_id: str, amount: float) -> str:
        """Pay fines for a user"""
        user = self.get_user(user_id)
        if user:
            if amount <= 0:
                return "❌ Payment amount must be positive"
            if amount > user.fines_owed:
                return f"❌ Payment amount (${amount:.2f}) exceeds fines owed (${user.fines_owed:.2f})"
            user.fines_owed -= amount
            return f"✅ Payment of ${amount:.2f} successful. Remaining fines: ${user.fines_owed:.2f}"
        
        librarian = self.get_librarian(user_id)
        if librarian:
            if amount <= 0:
                return "❌ Payment amount must be positive"
            if amount > librarian.fines_owed:
                return f"❌ Payment amount (${amount:.2f}) exceeds fines owed (${librarian.fines_owed:.2f})"
            librarian.fines_owed -= amount
            return f"✅ Payment of ${amount:.2f} successful. Remaining fines: ${librarian.fines_owed:.2f}"
        
        return f"❌ User with ID {user_id} not found"
    
    def get_catalog_stats(self) -> Dict[str, int]:
        """Get catalog statistics"""
        from models.items.book import Book
        from models.items.ebook import EBook
        from models.items.magazine import Magazine
        
        total_items = len(self._items)
        
        available_items = 0
        for item in self._items.values():
            if self.is_item_available(item):
                available_items += 1
        
        borrowed_items = total_items - available_items
        total_users = len(self._users)
        total_librarians = len(self._librarians)
        
        books = sum(1 for item in self._items.values() if isinstance(item, Book))
        ebooks = sum(1 for item in self._items.values() if isinstance(item, EBook))
        magazines = sum(1 for item in self._items.values() if isinstance(item, Magazine))
        
        return {
            'total_items': total_items,
            'available_items': available_items,
            'borrowed_items': borrowed_items,
            'total_users': total_users + total_librarians,
            'books': books,
            'ebooks': ebooks,
            'magazines': magazines
        }
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics for dashboard"""
        total_users = len(self._users)
        total_librarians = len(self._librarians)
        
        active_users = sum(1 for user in self._users.values() if len(user.borrowed_items) > 0)
        active_librarians = sum(1 for lib in self._librarians.values() if len(lib.borrowed_items) > 0)
        
        users_with_fines = sum(1 for user in self._users.values() if user.fines_owed > 0)
        librarians_with_fines = sum(1 for lib in self._librarians.values() if lib.fines_owed > 0)
        
        total_fines = sum(user.fines_owed for user in self._users.values())
        total_fines += sum(lib.fines_owed for lib in self._librarians.values())
        
        premium_count = sum(1 for user in self._users.values() if user.membership_level == "Premium")
        basic_count = sum(1 for user in self._users.values() if user.membership_level == "Basic")
        
        return {
            'total_users': total_users,
            'total_librarians': total_librarians,
            'active_users': active_users + active_librarians,
            'users_with_fines': users_with_fines + librarians_with_fines,
            'total_fines': total_fines,
            'premium_users': premium_count,
            'basic_users': basic_count
        }