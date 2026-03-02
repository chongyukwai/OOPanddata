"""
Catalog tab - browse and search library items
"""
import tkinter as tk
from tkinter import ttk

from config.styles import Colors, Fonts
from gui.components import ItemTree


class CatalogTab(ttk.Frame):
    """Catalog browsing tab"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(style='Card.TFrame')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create catalog widgets"""
        # Search bar
        search_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="Search:", font=Fonts.BODY,
                bg=Colors.BACKGROUND).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var,
                                font=Fonts.BODY, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<Return>', lambda e: self.search())
        
        ttk.Button(search_frame, text="🔍 Search",
                  command=self.search,
                  style='Primary.TButton').pack(side=tk.LEFT)
        
        ttk.Button(search_frame, text="Clear",
                  command=self.clear_search,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(search_frame, text="🔄 Refresh",
                  command=self.refresh,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=(10, 0))
        
        # Item tree
        tree_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.item_tree = ItemTree(tree_frame, self.app)
        self.item_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click
        self.item_tree.tree.bind('<Double-Button-1>', self.on_item_double_click)
        
        # Populate initially
        self.refresh()
    
    def update_display(self):
        """Update catalog display"""
        self.refresh()
    
    def refresh(self):
        """Refresh the item list"""
        self.item_tree.populate()
        self.app.set_status(f"Showing {len(self.item_tree.tree.get_children())} items")
    
    def refresh_catalog(self):
        """Alias for refresh() - for backward compatibility"""
        self.refresh()
    
    def search(self):
        """Search for items"""
        search_term = self.search_var.get().strip()
        if search_term:
            self.item_tree.populate(search_term)
            self.app.set_status(f"Found {len(self.item_tree.tree.get_children())} items matching '{search_term}'")
        else:
            self.refresh()
    
    def clear_search(self):
        """Clear search and show all"""
        self.search_var.set("")
        self.refresh()
    
    def on_item_double_click(self, event):
        """Handle item double-click"""
        selection = self.item_tree.tree.selection()
        if selection:
            item = self.item_tree.tree.item(selection[0])
            item_id = item['values'][0] if item['values'] else None
            if item_id:
                from gui.dialogs import ItemDetailsDialog
                ItemDetailsDialog(self.app, item_id)