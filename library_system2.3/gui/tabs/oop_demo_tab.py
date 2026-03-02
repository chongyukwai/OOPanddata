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
           
           @title.setter
           def title(self, value):
               if not value:
                   raise ValueError("Title cannot be empty")
               self._title = value
           ```
        
        
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
        
        
        5. 🏗️ COMPOSITION
           ────────────────────────────────────────────────────────────
           • `Librarian` HAS-A `LibraryCard` (inner class)
           • `Library` contains collections of items and users
           • Building complex objects from simpler ones
           
           Example:
           ```python
           class Librarian(Person):
               class LibraryCard:
                   def __init__(self, card_number):
                       self.card_number = card_number
               
               def __init__(self, name):
                   super().__init__(name)
                   self._library_card = self.LibraryCard("CARD001")
           ```
        
        
        6. 🔄 OPERATOR OVERLOADING
           ────────────────────────────────────────────────────────────
           • `__len__` returns number of borrowed items
           • `__add__` adds days to join date
           • `__iadd__` adds fines
           
           Example:
           ```python
           def __len__(self):
               return len(self.borrowed_items)
           
           def __add__(self, days):
               return self.join_date + timedelta(days=days)
           ```
        
        
        7. 🎨 CLASS METHODS & STATIC METHODS
           ────────────────────────────────────────────────────────────
           • Class method `get_total_items()` tracks all instances
           • Static method `validate_id()` for ID validation
           
           Example:
           ```python
           @classmethod
           def get_total_items(cls):
               return cls.total_items
           
           @staticmethod
           def validate_id(item_id):
               return len(item_id) >= 3
           ```
        
        
        8. 🏭 FACTORY PATTERN (in LibraryService)
           ────────────────────────────────────────────────────────────
           • Creates different item types based on input
           • Centralizes object creation
           
           Example:
           ```python
           @staticmethod
           def create_item(item_type, **kwargs):
               if item_type == "book":
                   return Book(**kwargs)
               elif item_type == "ebook":
                   return EBook(**kwargs)
               elif item_type == "magazine":
                   return Magazine(**kwargs)
           ```
        
        
        9. 🔷 SINGLETON PATTERN
           ────────────────────────────────────────────────────────────
           • `LibraryService` ensures only one instance exists
           • Global access point to library operations
           
           Example:
           ```python
           class LibraryService:
               _instance = None
               
               def __new__(cls):
                   if cls._instance is None:
                       cls._instance = super().__new__(cls)
                   return cls._instance
           ```
        
        
        10. 🎯 DEPENDENCY INJECTION
            ────────────────────────────────────────────────────────────
            • Classes receive dependencies rather than creating them
            • Promotes loose coupling
            
            Example:
            ```python
            class LibraryGUI:
                def __init__(self):
                    self.library = LibraryService.get_instance()
                    # Dependency injected through get_instance()
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