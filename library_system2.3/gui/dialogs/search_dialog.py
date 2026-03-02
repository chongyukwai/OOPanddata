"""
Search Dialog
"""
import tkinter as tk
from tkinter import ttk, messagebox

from config.styles import Colors, Fonts


class SearchDialog:
    """Dialog for searching items"""
    
    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel(app.root)
        self.window.title("Search Items")
        self.window.geometry("400x200")
        self.window.configure(bg=Colors.BACKGROUND)
        self.window.transient(app.root)
        self.window.grab_set()
        
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """Center window on parent"""
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() // 2) - 200
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() // 2) - 100
        self.window.geometry(f"400x200+{x}+{y}")
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = tk.Frame(self.window, bg=Colors.BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Search Items",
                font=Fonts.SUBHEADER,
                bg=Colors.BACKGROUND,
                fg=Colors.PRIMARY).pack(pady=(0, 20))
        
        tk.Label(main_frame, text="Enter search term:",
                font=Fonts.BODY,
                bg=Colors.BACKGROUND).pack(anchor=tk.W)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(main_frame, textvariable=self.search_var,
                                font=Fonts.BODY, width=40)
        search_entry.pack(pady=10)
        search_entry.focus_set()
        search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="🔍 Search",
                  command=self.perform_search,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel",
                  command=self.window.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
    
    def perform_search(self):
        """Perform the search"""
        term = self.search_var.get().strip()
        if term:
            # Set search in catalog tab
            catalog_tab = self.app.catalog_tab
            catalog_tab.search_var.set(term)
            self.app.notebook.select(1)  # Switch to catalog tab
            catalog_tab.search()
            self.window.destroy()
        else:
            messagebox.showwarning("Warning", "Please enter a search term!")