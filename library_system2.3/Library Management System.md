Library Management System

A comprehensive object-oriented library management system built with Python and Tkinter. This application demonstrates core OOP concepts while providing a functional GUI for managing library operations.

📋 Overview

The Library Management System allows users to:

Browse and search library catalog

Borrow and return items (Books, EBooks, Magazines)

Manage users and librarians

Track borrowed items and due dates

Calculate fines for overdue items

View library statistics and dashboard

🏗️ System Architecture

text

library-management-system/

├── main.py                    # Application entry point

├── config/

│   └── styles.py              # GUI styling configuration

├── gui/

│   ├── main\_window.py         # Main application window

│   ├── components/            # Reusable GUI components

│   │   ├── header.py

│   │   ├── status\_bar.py

│   │   └── item\_tree.py

│   ├── dialogs/               # Modal dialog windows

│   │   ├── add\_item\_dialog.py

│   │   ├── item\_details\_dialog.py

│   │   ├── register\_dialog.py

│   │   ├── search\_dialog.py

│   │   ├── user\_details\_dialog.py

│   │   └── user\_switch\_dialog.py

│   └── tabs/                   # Main interface tabs

│       ├── dashboard\_tab.py

│       ├── catalog\_tab.py

│       ├── users\_tab.py

│       ├── borrow\_tab.py

│       └── oop\_demo\_tab.py

├── models/

│   ├── base.py                 # Base model with timestamps

│   ├── items/                  # Library item hierarchy

│   │   ├── base\_item.py        # Abstract base class

│   │   ├── book.py

│   │   ├── ebook.py

│   │   └── magazine.py

│   └── users/                   # User hierarchy

│       ├── base\_user.py         # Person base class

│       ├── borrower.py          # Borrower mixin

│       ├── library\_user.py      # Multiple inheritance

│       └── librarian.py         # Composition example

└── services/

├── library\_service.py       # Core business logic

├── exceptions.py            # Custom exceptions

├── decorators.py            # Function decorators

└── validators.py            # Input validation

🎯 Object-Oriented Programming Concepts Demonstrated

1. Encapsulation

Encapsulation is demonstrated through private attributes and controlled access via properties:

Private Attributes: Attributes like \_title, \_is\_available, \_checkout\_date are marked with underscores to indicate they should not be accessed directly

Property Getters/Setters: Controlled access with validation logic

Read-Only Properties: Some attributes have only getters without setters

Business Logic Encapsulation: Complex operations like checkout() and return\_item() hide internal implementation details

Composition with Encapsulation: The Librarian class contains an inner LibraryCard class, completely hidden from external code

1. Inheritance

Multiple inheritance hierarchies showcase different types of inheritance:

Single Inheritance: Book inherits from LibraryItem

Multi-Level Inheritance: EBook inherits from Book, which inherits from LibraryItem

Multiple Inheritance: LibraryUser inherits from both Person and Borrower

Abstract Base Classes: LibraryItem defines abstract methods that all subclasses must implement

Class Variables and Methods: Shared across all instances of a class hierarchy

1. Polymorphism

Polymorphism is demonstrated through method overriding and uniform interfaces:

Method Overriding: Each subclass implements its own version of get\_details() and get\_item\_type()

Abstract Methods: Enforce a contract that all subclasses must fulfill

Uniform Treatment: The catalog can display all item types without knowing their specific class

Operator Overloading: The LibraryUser class implements special methods like \_\_len\_\_, \_\_add\_\_, and \_\_iadd\_\_

Polymorphic GUI Components: Each tab implements its own update\_display() method called uniformly by the main window

1. Additional OOP Features

Composition: Librarian has-a LibraryCard relationship

Mixins: Borrower class provides reusable borrowing functionality

Singleton Pattern: LibraryService uses singleton pattern

Decorators: Custom decorators for logging, timing, and validation

Custom Exceptions: Hierarchical exception classes

✨ Features

User Management

Register new users with different membership levels (Basic, Premium, VIP)

Switch between users

View user details and borrowing history

Track fines and make payments

Catalog Management

Browse all library items

Search by title, author, or ID

View item details

Add new items (Books, EBooks, Magazines)

Borrowing System

Borrow available items (14-day borrowing period)

Return borrowed items

Automatic fine calculation for overdue items

View borrowed items with due dates

Dashboard

Library statistics (total items, available items, borrowed items)

User statistics (active users, total fines)

Quick access to common actions

Current user information

🚀 Getting Started

Prerequisites

Python 3.7 or higher

Tkinter (usually included with Python)

Installation

Clone the repository:

bash

git clone https://github.com/chongyukwai/OOPanddata/tree/main/library\_system2.3

cd library\_system2.3

Run the application:

bash

python main.py

The application comes with pre-loaded demo data, so you can start exploring immediately.

Demo Data

The system initializes with:

Users: Alice Johnson (Premium)

Items: "Python Programming" (Book), "Advanced Python" (EBook), "Tech Monthly" (Magazine)

🎮 Usage Guide

Selecting a User

Go to the Users tab

Can switch between self enrolled Liberian and user

Browsing the Catalog

Go to the Catalog tab

Use the search bar to find specific items

Double-click on an item to view details

Borrowing an Item

Has a default user

Go to the Borrow/Return tab

Click "Borrow Items" to see available items

Double-click an item or select it and click "Borrow Selected Item"

Returning an Item

Select the user who borrowed the item

Go to the Borrow/Return tab

Click "Return Items" to see borrowed items

Double-click an item or select it and click "Return Selected Item"

Adding New Items

Go to the Dashboard tab

Click "Add New Item" in Quick Actions

Select item type and fill in the details

Click "Add Item"

Registering New Users

Go to the Dashboard tab

Click "Register User" in Quick Actions

Fill in user details

Click "Register"

🧪 Testing OOP Concepts

The OOP Concepts tab provides interactive demonstrations of:

Inheritance hierarchies

Polymorphic behavior

Encapsulation examples

Operator overloading

Class methods and variables

📁 Key Code Examples

Inheritance Hierarchy

python

\# Base abstract class

class LibraryItem(ABC):

def \_\_init\_\_(self, title, item\_id):

self.\_title = title

self.\_item\_id = item\_id

@abstractmethod

def get\_details(self):

pass

\# Single inheritance

class Book(LibraryItem):

def \_\_init\_\_(self, title, item\_id, author):

super().\_\_init\_\_(title, item\_id)

self.author = author

\# Multi-level inheritance

class EBook(Book):

def \_\_init\_\_(self, title, item\_id, author, file\_size):

super().\_\_init\_\_(title, item\_id, author)

self.file\_size = file\_size

Multiple Inheritance

python

class Person:

def \_\_init\_\_(self, name, email):

self.name = name

self.email = email

class Borrower:

def \_\_init\_\_(self):

self.borrowed\_items = []

def borrow\_item(self, item):

self.borrowed\_items.append(item)

class LibraryUser(Person, Borrower):

def \_\_init\_\_(self, name, email, user\_id):

Person.\_\_init\_\_(self, name, email)

Borrower.\_\_init\_\_(self)

self.user\_id = user\_id

Encapsulation with Properties

python

class LibraryItem:

def \_\_init\_\_(self, title):

self.\_title = title

self.\_is\_available = True

@property

def title(self):

return self.\_title

@title.setter

def title(self, value):

if not value or len(value.strip()) < 1:

raise ValueError("Title cannot be empty")

self.\_title = value

def checkout(self):

if self.\_is\_available:

self.\_is\_available = False

return True

return False

Polymorphism

python

\# Different implementations of the same interface

class Book(LibraryItem):

def get\_details(self):

return f"Book: {self.title} by {self.author}"

class Magazine(LibraryItem):

def get\_details(self):

return f"Magazine: {self.title} Issue #{self.issue\_number}"

\# Uniform treatment

for item in library\_items:

print(item.get\_details())  # Polymorphic call

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

Built as a demonstration of Object-Oriented Programming concepts

Uses Python's Tkinter for the graphical user interface

Inspired by real-world library management needs
