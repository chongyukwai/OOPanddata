"""
Main GUI window for Library Management System
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from config.styles import Colors, Fonts, Styles
from services.library_service import LibraryService
from gui.tabs.dashboard_tab import DashboardTab
from gui.tabs.catalog_tab import CatalogTab
from gui.tabs.users_tab import UsersTab
from gui.tabs.borrow_tab import BorrowTab
from gui.tabs.oop_demo_tab import OOPDemoTab
from gui.components.header import Header
from gui.components.status_bar import StatusBar


class LibraryGUI:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg=Colors.BACKGROUND)
        
        # Initialize services
        self.library = LibraryService.get_instance()
        self.current_user = None
        
        # Setup demo data
        self.setup_demo_data()
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI components
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        Styles.configure(style)
    
    def setup_demo_data(self):
        """Setup initial demo data"""
        from models.items import Book, EBook, Magazine
        from models.users import LibraryUser, Librarian
        from datetime import datetime, timedelta
        
        # Create more demo items
        items = []
        for i in range(1, 11):
            book = Book(
                title=f"Python Programming Vol {i}",
                item_id=f"BK{i:03d}",
                author=f"Author {i}",
                isbn=f"978-01348539{i:02d}",
                pages=500 + i
            )
            self.library.add_item(book)
            items.append(book)
        
        # Add ebooks
        ebook1 = EBook("Advanced Python", "EB001", "Jane Smith", "978-0134853988", 720, 2.5, "PDF")
        ebook2 = EBook("Python Data Science", "EB002", "Jake VanderPlas", "978-7654321", 450, 8.5, "EPUB")
        self.library.add_item(ebook1)
        self.library.add_item(ebook2)
        items.extend([ebook1, ebook2])
        
        # Add magazines
        magazine1 = Magazine("Tech Monthly", "MG001", 42, "Tech Media")
        magazine2 = Magazine("Science Weekly", "MG002", 15, "Science Publications")
        self.library.add_item(magazine1)
        self.library.add_item(magazine2)
        items.extend([magazine1, magazine2])
        
        # Create users
        # Premium user - Alice (can borrow)
        user1 = LibraryUser("Alice Johnson", "alice@email.com", "USR001", membership_level="Premium")
        for i in range(3):
            user1.borrowed_items.append(items[i])
            items[i].due_date = datetime.now() + timedelta(days=14)
        self.library.add_user(user1)
        
        # Basic user - Bob (cannot borrow)
        user2 = LibraryUser("Bob Wilson", "bob@email.com", "USR002", membership_level="Basic")
        self.library.add_user(user2)
        
        # Premium user - Charlie (can borrow)
        user3 = LibraryUser("Charlie Brown", "charlie@email.com", "USR003", membership_level="Premium")
        for i in range(3, 5):
            user3.borrowed_items.append(items[i])
            items[i].due_date = datetime.now() + timedelta(days=14)
        self.library.add_user(user3)
        
        # Create librarian
        librarian = Librarian("Carol Davis", "carol@library.com", "EMP001")
        for i in range(5, 10):
            librarian.borrowed_items.append(items[i])
            if i < 8:
                items[i].due_date = datetime.now() + timedelta(days=14)
            else:
                items[i].due_date = datetime.now() - timedelta(days=5)
        self.library.add_librarian(librarian)
        
        # Add one more Basic user
        user4 = LibraryUser("David Miller", "david@email.com", "USR004", membership_level="Basic")
        self.library.add_user(user4)
        
        # Set default user to Alice (Premium)
        self.current_user = user1
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=Colors.BACKGROUND)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header = Header(self.main_container, self)
        self.header.pack(fill=tk.X, pady=(0, 20))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Bind tab selection event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_selected)
        
        # Create tabs
        self.dashboard_tab = DashboardTab(self.notebook, self)
        self.notebook.add(self.dashboard_tab, text="📊 Dashboard")
        
        self.catalog_tab = CatalogTab(self.notebook, self)
        self.notebook.add(self.catalog_tab, text="📚 Catalog")
        
        self.users_tab = UsersTab(self.notebook, self)
        self.notebook.add(self.users_tab, text="👥 Users")
        
        self.borrow_tab = BorrowTab(self.notebook, self)
        self.notebook.add(self.borrow_tab, text="📖 Borrow/Return")
        
        self.oop_tab = OOPDemoTab(self.notebook, self)
        self.notebook.add(self.oop_tab, text="🎓 OOP Concepts")
        
        # Status bar
        self.status_bar = StatusBar(self.main_container, self)
        self.status_bar.pack(fill=tk.X, pady=(20, 0))
        
        # Update displays
        self.update_all_displays()
    
    def on_tab_selected(self, event):
        """Handle tab selection"""
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        
        # If borrow tab is selected, update it
        if "Borrow/Return" in tab_name and hasattr(self, 'borrow_tab'):
            self.borrow_tab.tab_selected()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def update_all_displays(self):
        """Update all displays"""
        if hasattr(self, 'header'):
            self.header.update_user_display()
        if hasattr(self, 'status_bar'):
            self.status_bar.update()
        
        # Update each tab if they have update methods
        for tab_name in ['dashboard_tab', 'catalog_tab', 'users_tab', 'borrow_tab']:
            if hasattr(self, tab_name):
                tab = getattr(self, tab_name)
                if hasattr(tab, 'update_display'):
                    tab.update_display()
    
    def set_status(self, message: str):
        """Set status bar message"""
        if hasattr(self, 'status_bar'):
            self.status_bar.set_message(message)
    
    # ========== Dialog Methods ==========
    
    def show_user_switch_dialog(self):
        """Show user switch dialog"""
        from gui.dialogs.user_switch_dialog import UserSwitchDialog
        UserSwitchDialog(self)
    
    def show_register_dialog(self):
        """Show register dialog"""
        from gui.dialogs.register_dialog import RegisterDialog
        RegisterDialog(self)
    
    def show_add_item_dialog(self):
        """Show add item dialog"""
        from gui.dialogs.add_item_dialog import AddItemDialog
        AddItemDialog(self)
    
    def show_search_dialog(self):
        """Show search dialog"""
        from gui.dialogs.search_dialog import SearchDialog
        SearchDialog(self)
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()
    
    def set_current_user(self, user):
        """Set the current user"""
        print(f"DEBUG - Setting current user to: {user.name if user else 'None'}")
        self.current_user = user
    
        if user:
            self.status_bar.set_user(user)
        # Update window title - handle both user types
            if hasattr(user, 'user_id'):
                title_text = f"Library Management System - {user.name} (User)"
            elif hasattr(user, 'employee_id'):
                title_text = f"Library Management System - {user.name} (Librarian)"
            else:
                title_text = f"Library Management System - {user.name}"
        else:
            self.status_bar.set_user(None)
            title_text = "Library Management System"
    
        self.root.title(title_text)
    
    # Update all tabs that depend on user
        self.update_all_displays()
    
    # If this is called from somewhere, make sure the borrow tab knows
        if hasattr(self, 'borrow_tab'):
        # Don't automatically switch mode, just update the display
            if self.borrow_tab.current_mode == "borrow":
               self.borrow_tab.show_available_items()
            else:
               self.borrow_tab.show_borrowed_items()