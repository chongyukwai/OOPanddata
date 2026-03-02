"""
Add Item Dialog
"""
import tkinter as tk
from tkinter import ttk, messagebox

from config.styles import Colors, Fonts
from services.library_service import LibraryService
from models.items import Book, EBook, Magazine


class AddItemDialog:
    """Dialog for adding new library items"""
    
    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel(app.root)
        self.window.title("Add New Item")
        self.window.geometry("500x600")
        self.window.configure(bg=Colors.BACKGROUND)
        self.window.transient(app.root)
        self.window.grab_set()
        
        self.library = LibraryService.get_instance()
        self.specific_vars = {}
        
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """Center window on parent"""
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() // 2) - 250
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() // 2) - 300
        self.window.geometry(f"500x600+{x}+{y}")
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = tk.Frame(self.window, bg=Colors.BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text="Add New Library Item",
                font=Fonts.HEADER,
                bg=Colors.BACKGROUND,
                fg=Colors.PRIMARY).pack(pady=(0, 20))
        
        # Item type selection
        type_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        type_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(type_frame, text="Item Type:",
                font=Fonts.BODY_BOLD,
                bg=Colors.BACKGROUND).pack(anchor=tk.W)
        
        self.item_type = tk.StringVar(value="Book")
        
        types = [("📚 Book", "Book"),
                ("💾 EBook", "EBook"),
                ("📰 Magazine", "Magazine")]
        
        for text, value in types:
            rb = tk.Radiobutton(type_frame, text=text, variable=self.item_type,
                               value=value, bg=Colors.BACKGROUND,
                               font=Fonts.BODY)
            rb.pack(anchor=tk.W, pady=2)
        
        # Common fields
        common_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        common_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(common_frame, text="Common Details:",
                font=Fonts.BODY_BOLD,
                bg=Colors.BACKGROUND).pack(anchor=tk.W)
        
        # Title
        title_frame = tk.Frame(common_frame, bg=Colors.BACKGROUND)
        title_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(title_frame, text="Title:*",
                font=Fonts.BODY,
                bg=Colors.BACKGROUND, width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(title_frame, textvariable=self.title_var, width=30)
        title_entry.pack(side=tk.LEFT)
        
        # Item ID
        id_frame = tk.Frame(common_frame, bg=Colors.BACKGROUND)
        id_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(id_frame, text="Item ID:",
                font=Fonts.BODY,
                bg=Colors.BACKGROUND, width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        self.id_var = tk.StringVar()
        id_entry = ttk.Entry(id_frame, textvariable=self.id_var, width=30)
        id_entry.pack(side=tk.LEFT)
        
        ttk.Button(id_frame, text="Auto-generate",
                  command=self.auto_generate_id,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=10)
        
        # Specific fields frame
        self.specific_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        self.specific_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Update fields when type changes
        self.item_type.trace('w', lambda *args: self.update_specific_fields())
        self.update_specific_fields()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="➕ Add Item",
                  command=self.add_item,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel",
                  command=self.window.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Auto-generate ID
        self.auto_generate_id()
        title_entry.focus_set()
    
    def update_specific_fields(self):
        """Update specific fields based on item type"""
        # Clear existing fields
        for widget in self.specific_frame.winfo_children():
            widget.destroy()
        
        self.specific_vars.clear()
        
        item_type = self.item_type.get()
        fields = []
        
        if item_type == "Book":
            fields = [
                ("Author:", "author", "text"),
                ("ISBN:", "isbn", "text"),
                ("Pages:", "pages", "number")
            ]
        elif item_type == "EBook":
            fields = [
                ("Author:", "author", "text"),
                ("ISBN:", "isbn", "text"),
                ("Pages:", "pages", "number"),
                ("File Size (MB):", "file_size", "decimal"),
                ("Format:", "format", "text")
            ]
        elif item_type == "Magazine":
            fields = [
                ("Issue Number:", "issue_number", "number"),
                ("Publisher:", "publisher", "text")
            ]
        
        # Create fields
        for label, var_name, field_type in fields:
            field_frame = tk.Frame(self.specific_frame, bg=Colors.BACKGROUND)
            field_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(field_frame, text=label,
                    font=Fonts.BODY,
                    bg=Colors.BACKGROUND, width=20, anchor=tk.W).pack(side=tk.LEFT)
            
            var = tk.StringVar()
            self.specific_vars[var_name] = var
            
            entry = ttk.Entry(field_frame, textvariable=var, width=30)
            entry.pack(side=tk.LEFT)
    
    def auto_generate_id(self):
        """Auto-generate item ID"""
        items = self.library.get_all_items()
        prefix = {
            "Book": "BK",
            "EBook": "EB",
            "Magazine": "MG"
        }.get(self.item_type.get(), "IT")
        
        existing_ids = [item.item_id for item in items]
        counter = 1
        while f"{prefix}{counter:03d}" in existing_ids:
            counter += 1
        
        self.id_var.set(f"{prefix}{counter:03d}")
    
    def add_item(self):
        """Add the item to the library"""
        try:
            # Validate title
            title = self.title_var.get().strip()
            if not title:
                messagebox.showerror("Error", "Title is required!")
                return
            
            # Validate ID
            item_id = self.id_var.get().strip().upper()
            if not item_id:
                messagebox.showerror("Error", "Item ID is required!")
                return
            
            # Check if ID exists
            if self.library.get_item(item_id):
                messagebox.showerror("Error", f"Item ID '{item_id}' already exists!")
                return
            
            # Create item based on type
            item_type = self.item_type.get()
            
            if item_type == "Book":
                author = self.specific_vars.get('author', tk.StringVar()).get().strip() or "Unknown"
                isbn = self.specific_vars.get('isbn', tk.StringVar()).get().strip() or "000-0000000000"
                pages = self.specific_vars.get('pages', tk.StringVar()).get().strip() or "100"
                pages_int = int(pages) if pages.isdigit() else 100
                
                item = Book(title, item_id, author, isbn, pages_int)
            
            elif item_type == "EBook":
                author = self.specific_vars.get('author', tk.StringVar()).get().strip() or "Unknown"
                isbn = self.specific_vars.get('isbn', tk.StringVar()).get().strip() or "000-0000000000"
                pages = self.specific_vars.get('pages', tk.StringVar()).get().strip() or "100"
                pages_int = int(pages) if pages.isdigit() else 100
                file_size = self.specific_vars.get('file_size', tk.StringVar()).get().strip() or "1.0"
                file_size_float = float(file_size) if file_size.replace('.', '', 1).isdigit() else 1.0
                format_type = self.specific_vars.get('format', tk.StringVar()).get().strip() or "PDF"
                
                item = EBook(title, item_id, author, isbn, pages_int, file_size_float, format_type)
            
            elif item_type == "Magazine":
                issue = self.specific_vars.get('issue_number', tk.StringVar()).get().strip() or "1"
                issue_num = int(issue) if issue.isdigit() else 1
                publisher = self.specific_vars.get('publisher', tk.StringVar()).get().strip() or "Unknown Publisher"
                
                item = Magazine(title, item_id, issue_num, publisher)
            
            else:
                messagebox.showerror("Error", f"Unknown item type: {item_type}")
                return
            
            # Add to library
            result = self.library.add_item(item)
            
            # Update displays
            self.app.update_all_displays()
            
            messagebox.showinfo("Success", result)
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")