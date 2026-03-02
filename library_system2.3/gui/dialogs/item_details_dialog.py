"""
Item Details Dialog
"""
import tkinter as tk
from tkinter import ttk, messagebox

from config.styles import Colors, Fonts
from services.library_service import LibraryService


class ItemDetailsDialog:
    """Dialog for viewing item details"""
    
    def __init__(self, app, item_id):
        self.app = app
        self.window = tk.Toplevel(app.root)
        self.window.title("Item Details")
        self.window.geometry("500x450")
        self.window.configure(bg=Colors.BACKGROUND)
        self.window.transient(app.root)
        self.window.grab_set()
        
        self.library = LibraryService.get_instance()
        self.item_id = item_id
        
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """Center window on parent"""
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() // 2) - 250
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() // 2) - 225
        self.window.geometry(f"500x450+{x}+{y}")
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = tk.Frame(self.window, bg=Colors.BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get item
        item = self.library.get_item(self.item_id)
        
        if not item:
            messagebox.showerror("Error", f"Item not found: {self.item_id}")
            self.window.destroy()
            return
        
        # Title
        tk.Label(main_frame, text=item.title,
                font=Fonts.HEADER,
                bg=Colors.BACKGROUND,
                fg=Colors.PRIMARY).pack(pady=(0, 20))
        
        # Item details
        details_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get details from item
        if hasattr(item, 'get_details'):
            details_text = item.get_details()
        else:
            details_text = str(item)
        
        details_label = tk.Label(details_frame, text=details_text,
                                font=Fonts.BODY,
                                bg=Colors.BACKGROUND,
                                justify=tk.LEFT)
        details_label.pack(anchor=tk.W, pady=10)
        
        # REMOVED THE BORROW BUTTON - Only Close button remains
        button_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(pady=20)
        
        # Just the Close button
        ttk.Button(button_frame, text="Close",
                  command=self.window.destroy,
                  style='Secondary.TButton').pack()