"""
Item Tree component - reusable treeview for displaying library items
"""
import tkinter as tk
from tkinter import ttk

from config.styles import Colors, Fonts
from services.library_service import LibraryService


class ItemTree(tk.Frame):
    """Treeview for displaying library items"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg=Colors.BACKGROUND)
        self.app = app
        self.library = LibraryService.get_instance()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create treeview with scrollbars"""
        # Create treeview
        columns = ('ID', 'Title', 'Type', 'Author', 'Details')
        self.tree = ttk.Treeview(self, columns=columns, show='tree headings')
        
        # Configure columns
        self.tree.heading('#0', text='#')
        self.tree.column('#0', width=50, stretch=False)
        
        column_widths = {
            'ID': 100,
            'Title': 250,
            'Type': 100,
            'Author': 150,
            'Details': 150
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100))
        
        # Add scrollbars
        v_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def populate(self, search_term: str = None):
        """Populate tree with items"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all items
        items = self.library.get_all_items()
        
        # Filter if search term provided
        if search_term:
            search_lower = search_term.lower()
            filtered_items = []
            for item in items:
                if (search_lower in item.title.lower() or
                    (hasattr(item, 'author') and search_lower in item.author.lower()) or
                    search_lower in item.item_id.lower() or
                    search_lower in item.__class__.__name__.lower()):
                    filtered_items.append(item)
            items = filtered_items
        
        # Sort by title
        items.sort(key=lambda x: x.title)
        
        # Add to tree
        for i, item in enumerate(items, 1):
            author = getattr(item, 'author', 'N/A')
            
            details = ""
            if hasattr(item, 'pages'):
                details = f"📄 {item.pages} pages"
            if hasattr(item, 'file_size'):
                details = f"💾 {item.file_size}MB {getattr(item, 'format', '')}"
            if hasattr(item, 'issue_number'):
                details = f"📰 Issue #{item.issue_number}"
            
            values = (
                item.item_id,
                item.title,
                item.__class__.__name__,
                author,
                details
            )
            
            self.tree.insert('', tk.END, text=str(i), values=values)