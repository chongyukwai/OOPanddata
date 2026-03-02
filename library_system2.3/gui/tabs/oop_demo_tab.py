"""
OOP Concepts demonstration tab
"""
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from typing import Optional
from config.styles import Colors, Fonts


class OOPDemoTab(ttk.Frame):
    """OOP concepts demonstration tab"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(style='Card.TFrame')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create OOP demo widgets"""
        # Text widget with scrollbar
        text_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_widget = scrolledtext.ScrolledText(text_frame,
                                               font=('Courier', 11),
                                               bg=Colors.WHITE,
                                               wrap=tk.WORD,
                                               padx=20,
                                               pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # OOP content
        content = """
        🎯 OBJECT-ORIENTED PROGRAMMING CONCEPTS DEMONSTRATION
        ====================================================
        
        📚 This Library Management System demonstrates key OOP principles:
        
        
        1. ✅ INHERITANCE
           ────────────────────────────────────────────────────────────
           • `LibraryItem` is an abstract base class
           • `Book`, `EBook`, and `Magazine` inherit from `LibraryItem`
           • `EBook` inherits from `Book` (multi-level inheritance)
           • `LibraryUser` inherits from both `Person` and `Borrower` (multiple inheritance)
           
           Example:
           ```python
           class LibraryItem(ABC):
               def __init__(self, title, item_id):
                   self._title = title
                   self._item_id = item_id
           
           class Book(LibraryItem):
               def __init__(self, title, item_id, author):
                   super().__init__(title, item_id)
                   self.author = author
           ```
        
        
        2. 🔒 ENCAPSULATION
           ────────────────────────────────────────────────────────────
           • Private attributes with leading underscore: `_title`, `_is_available`
           • Property decorators for controlled access
           • Validation in setters
           
           Example:
           ```python
           @property
           def title(self):
               return self._title
           
                   
        
        3. 🎭 POLYMORPHISM
           ────────────────────────────────────────────────────────────
           • Same method names with different implementations
           • `get_details()` behaves differently for each item type
           • `__str__` method overridden in each class
           
           Example:
           ```python
           def get_details(self):  # Same method name
               # Different implementations in each class
               pass
           ```
        
        
        4. 🧩 ABSTRACTION
           ────────────────────────────────────────────────────────────
           • Abstract base class `LibraryItem` with abstract methods
           • Complex implementation details hidden from users
           • Simple interfaces for borrowing/returning
           
           Example:
           ```python
           from abc import ABC, abstractmethod
           
           class LibraryItem(ABC):
               @abstractmethod
               def get_details(self):
                   pass  # Must be implemented by subclasses
           ```
        
        
 
        💡 REAL-WORLD BENEFITS:
        ────────────────────────────────────────────────────────────
        • ✅ **Reusability**: Base classes can be extended for new item types
        • ✅ **Maintainability**: Changes in one class don't affect others
        • ✅ **Flexibility**: Easy to add new features without breaking existing code
        • ✅ **Security**: Encapsulation prevents unauthorized data access
        • ✅ **Scalability**: Can handle growing number of items and users
        • ✅ **Testability**: Each class can be tested independently
        
        
        🔧 TRY IT YOURSELF:
        ────────────────────────────────────────────────────────────
        • Switch users to see different borrowing limits
        • Add different item types to see inheritance in action
        • Check user details to see encapsulation at work
        • Try borrowing limits with different membership levels
        """
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)