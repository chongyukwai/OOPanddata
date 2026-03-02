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
        
        # Create demo items
        book = Book(
            title="Python Programming",
            item_id="BK001",
            author="John Doe",
            isbn="978-0134853987",
            pages=560
        )
        self.library.add_item(book)
        
        ebook = EBook(
            title="Advanced Python",
            item_id="EB001",
            author="Jane Smith",
            isbn="978-0134853988",
            pages=720,
            file_size=2.5,
            format="PDF"
        )
        self.library.add_item(ebook)
        
        magazine = Magazine(
            title="Tech Monthly",
            item_id="MG001",
            issue_number=42,
            publisher="Tech Media Inc."
        )
        self.library.add_item(magazine)
        
        # Create demo users
        user1 = LibraryUser("Alice Johnson", "alice@email.com", "USR001")
        user1.membership_level = "Premium"
        self.library.add_user(user1)
        
        user2 = LibraryUser("Bob Wilson", "bob@email.com", "USR002")
        self.library.add_user(user2)
        
        librarian = Librarian("Carol Davis", "carol@library.com", "EMP001")
        self.library.add_librarian(librarian)
        
        # Set default user
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
        self.current_user = user
        self.status_bar.set_user(user)
        
        # Update all tabs that depend on user
        self.update_all_displays()
        
        # Update window title
        self.root.title(f"Library Management System - {user.name}")