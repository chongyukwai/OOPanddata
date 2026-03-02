"""
Borrow/Return tab - handle borrowing and returning items
"""
import sys
import os
# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from config.styles import Colors, Fonts


class BorrowTab(ttk.Frame):
    """Borrow and return items tab"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(style='Card.TFrame')
        self.current_mode = "borrow"  # Default mode
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create borrow/return widgets"""
        # Main container
        main_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="📖 Borrow / Return Items",
                              font=Fonts.TITLE,
                              bg=Colors.BACKGROUND,
                              fg=Colors.PRIMARY)
        title_label.pack(pady=(0, 20))
        
        # Mode selection buttons
        mode_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.borrow_btn = ttk.Button(mode_frame, text="📤 Borrow Items",
                                     command=self.show_available_items,
                                     style='Primary.TButton')
        self.borrow_btn.pack(side=tk.LEFT, padx=5)
        
        self.return_btn = ttk.Button(mode_frame, text="📥 Return Items",
                                     command=self.show_borrowed_items,
                                     style='Secondary.TButton')
        self.return_btn.pack(side=tk.LEFT, padx=5)
        
        # Current mode indicator
        self.mode_label = tk.Label(main_frame, text="Current Mode: Borrow Items",
                                  font=Fonts.SUBHEADER,
                                  bg=Colors.BACKGROUND,
                                  fg=Colors.ACCENT)
        self.mode_label.pack(pady=(0, 10))
        
        # User info display
        user_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        user_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.user_label = tk.Label(user_frame, text="",
                                  font=Fonts.BODY_BOLD,
                                  bg=Colors.BACKGROUND,
                                  fg=Colors.PRIMARY)
        self.user_label.pack(side=tk.LEFT)
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search Items:", 
                font=Fonts.BODY,
                bg=Colors.BACKGROUND,
                fg=Colors.TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_items)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     font=Fonts.BODY, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.filter_items)
        
        self.clear_search_btn = ttk.Button(search_frame, text="Clear",
                                          command=self.clear_search,
                                          style='Secondary.TButton')
        self.clear_search_btn.pack(side=tk.LEFT)
        
        # Treeview for items
        tree_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        columns = ('ID', 'Title', 'Type', 'Author/Publisher', 'Status', 'Due Date')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('ID', text='Item ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Author/Publisher', text='Author/Publisher')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Due Date', text='Due Date')
        
        # Define column widths
        self.tree.column('ID', width=100)
        self.tree.column('Title', width=250)
        self.tree.column('Type', width=100)
        self.tree.column('Author/Publisher', width=200)
        self.tree.column('Status', width=100)
        self.tree.column('Due Date', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action button
        self.action_btn = ttk.Button(main_frame, text="📤 Borrow Selected Item",
                                     command=self.perform_action,
                                     style='Primary.TButton')
        self.action_btn.pack(pady=20)
        
        # Due date info for borrow mode
        self.info_label = tk.Label(main_frame, text="",
                                  font=Fonts.BODY_SMALL,
                                  bg=Colors.BACKGROUND,
                                  fg=Colors.INFO)
        self.info_label.pack()
        
        # Store all items for filtering
        self.all_items = []
        
        # Initialize with available items
        self.show_available_items()
    
    def filter_items(self, *args):
        """Filter items based on search text"""
        search_text = self.search_var.get().lower()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not search_text:
            # Show all items
            items_to_show = self.all_items
        else:
            # Filter items
            items_to_show = []
            for item_data in self.all_items:
                if (search_text in item_data['title'].lower() or 
                    search_text in item_data['id'].lower() or
                    search_text in item_data['author'].lower()):
                    items_to_show.append(item_data)
        
        # Add filtered items to tree
        for item_data in items_to_show:
            self.tree.insert('', tk.END, values=(
                item_data['id'],
                item_data['title'],
                item_data['type'],
                item_data['author'],
                item_data['status'],
                item_data.get('due_date', '')
            ))
    
    def clear_search(self):
        """Clear search field"""
        self.search_var.set("")
        self.filter_items()
    
    def on_item_double_click(self, event):
        """Handle double-click on treeview item"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Get item ID from selection
        item_values = self.tree.item(selection[0])['values']
        if not item_values or len(item_values) < 1:
            return
        
        item_id = item_values[0]
        
        # Verify this is an item ID, not a user ID
        if item_id.startswith(('BK', 'EB', 'MG')):  # Book, EBook, Magazine prefixes
            # Perform action based on current mode
            if self.current_mode == "borrow":
                self.borrow_item(item_id)
            else:
                self.return_item(item_id)
        else:
            messagebox.showerror("Error", f"Invalid item ID format: {item_id}")
    
    def tab_selected(self):
        """Called when this tab is selected"""
        if self.app.current_user:
            if self.current_mode == "borrow":
                self.show_available_items()
            else:
                self.show_borrowed_items()
        else:
            # Clear display if no user
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.all_items = []
            self.user_label.config(text="No user selected", fg=Colors.DANGER)
    
    def show_available_items(self):
        """Show all available items for borrowing"""
        self.current_mode = "borrow"
        self.mode_label.config(text="Current Mode: Borrow Items", fg=Colors.ACCENT)
        self.action_btn.config(text="📤 Borrow Selected Item", style='Primary.TButton')
        self.info_label.config(text="Double-click or select and click button to borrow (14-day borrowing period)")
        
        # Clear tree and stored items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.all_items = []
        
        # Check if user is selected
        if not self.app.current_user:
            self.user_label.config(text="No user selected", fg=Colors.DANGER)
            self.tree.insert('', tk.END, values=('', 'Please select a user first', '', '', '', ''))
            return
        
        # Update user label
        if hasattr(self.app.current_user, 'user_id'):
            user_text = f"Current User: {self.app.current_user.name} (ID: {self.app.current_user.user_id})"
        else:
            user_text = f"Current User: {self.app.current_user.name} (Employee ID: {self.app.current_user.employee_id})"
        self.user_label.config(text=user_text, fg=Colors.SUCCESS)
        
        # Get available items
        available_items = self.app.library.get_available_items()
        
        if not available_items:
            self.tree.insert('', tk.END, values=('', 'No items available', '', '', '', ''))
            return
        
        # Add items to tree and store for filtering
        for item in available_items:
            # Get author/publisher based on item type
            if hasattr(item, 'author'):
                author_publisher = item.author
            elif hasattr(item, 'publisher'):
                author_publisher = item.publisher
            else:
                author_publisher = "N/A"
            
            item_data = {
                'id': item.item_id,
                'title': item.title,
                'type': item.get_item_type(),
                'author': author_publisher,
                'status': "✅ Available",
                'due_date': ''
            }
            self.all_items.append(item_data)
            
            self.tree.insert('', tk.END, values=(
                item.item_id,
                item.title,
                item.get_item_type(),
                author_publisher,
                "✅ Available",
                ""
            ))
    
    def show_borrowed_items(self):
        """Show items borrowed by current user"""
        self.current_mode = "return"
        self.mode_label.config(text="Current Mode: Return Items", fg=Colors.WARNING)
        self.action_btn.config(text="📥 Return Selected Item", style='Secondary.TButton')
        self.info_label.config(text="Double-click or select and click button to return")
        
        # Clear tree and stored items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.all_items = []
        
        # Check if user is selected
        if not self.app.current_user:
            self.user_label.config(text="No user selected", fg=Colors.DANGER)
            self.tree.insert('', tk.END, values=('', 'No user selected', '', '', '', ''))
            return
        
        # Update user label
        if hasattr(self.app.current_user, 'user_id'):
            user_text = f"Current User: {self.app.current_user.name} (ID: {self.app.current_user.user_id})"
        else:
            user_text = f"Current User: {self.app.current_user.name} (Employee ID: {self.app.current_user.employee_id})"
        self.user_label.config(text=user_text, fg=Colors.SUCCESS)
        
        # Check if user has borrowed items
        if not hasattr(self.app.current_user, 'borrowed_items') or not self.app.current_user.borrowed_items:
            self.info_label.config(text=f"{self.app.current_user.name} has no borrowed items", fg=Colors.INFO)
            self.tree.insert('', tk.END, values=('', 'No borrowed items', '', '', '', ''))
            return
        
        # Add borrowed items to tree and store for filtering
        for item in self.app.current_user.borrowed_items:
            # Get author/publisher based on item type
            if hasattr(item, 'author'):
                author_publisher = item.author
            elif hasattr(item, 'publisher'):
                author_publisher = item.publisher
            else:
                author_publisher = "N/A"
            
            # Check if overdue
            status = "❌ Borrowed"
            due_date_str = ""
            if hasattr(item, 'due_date') and item.due_date:
                due_date_str = item.due_date.strftime("%Y-%m-%d")
                if datetime.now() > item.due_date:
                    status = "⚠️ Overdue"
            
            item_data = {
                'id': item.item_id,
                'title': item.title,
                'type': item.get_item_type(),
                'author': author_publisher,
                'status': status,
                'due_date': due_date_str
            }
            self.all_items.append(item_data)
            
            self.tree.insert('', tk.END, values=(
                item.item_id,
                item.title,
                item.get_item_type(),
                author_publisher,
                status,
                due_date_str
            ))
    
    def perform_action(self):
        """Perform borrow or return action based on current mode"""
        if not self.app.current_user:
            messagebox.showwarning("No User", "Please select a user first")
            return
        
        # Get selected item
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item")
            return
        
        # Get item ID from selection
        item_values = self.tree.item(selection[0])['values']
        if not item_values or len(item_values) < 1:
            return
        
        item_id = item_values[0]
        
        # Verify this is an item ID
        if not item_id.startswith(('BK', 'EB', 'MG')):
            messagebox.showerror("Error", f"Invalid item ID format: {item_id}. Please select a valid item.")
            return
        
        if self.current_mode == "borrow":
            self.borrow_item(item_id)
        else:
            self.return_item(item_id)
    
    def _process_service_result(self, result, success_message, error_message="Operation failed"):
        """
        Process different return types from library service methods
        
        Args:
            result: The return value from the service method
            success_message: Message to show on success
            error_message: Message to show on error
            
        Returns:
            tuple: (success, message)
        """
        # Handle different return types
        if isinstance(result, tuple):
            if len(result) == 2:
                # Assume (success, message)
                return result[0], result[1]
            elif len(result) == 1:
                # Single value in tuple
                return result[0], success_message if result[0] else error_message
            elif len(result) >= 3:
                # Take first two values
                return result[0], result[1]
            else:
                # Empty tuple
                return False, error_message
        elif isinstance(result, bool):
            # Direct boolean
            return result, success_message if result else error_message
        elif isinstance(result, str):
            # String message (assume success if not empty)
            return bool(result), result if result else error_message
        elif result is None:
            # None result (assume failure)
            return False, error_message
        else:
            # Any other type (assume success if truthy)
            return bool(result), success_message if result else error_message
    
    def borrow_item(self, item_id):
        """Borrow an item - handles different return types"""
        # Verify item ID format
        if not item_id or not isinstance(item_id, str):
            messagebox.showerror("Error", f"Invalid item ID: {item_id}")
            return
        
        if not item_id.startswith(('BK', 'EB', 'MG')):
            messagebox.showerror("Error", f"Invalid item ID format: {item_id}. Item IDs should start with BK, EB, or MG")
            return
        
        # Find the item from available items
        item = None
        try:
            available_items = self.app.library.get_available_items()
            for available_item in available_items:
                if available_item.item_id == item_id:
                    item = available_item
                    break
            
            if not item:
                messagebox.showerror("Error", f"Item {item_id} not found or not available")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error finding item: {str(e)}")
            return
        
        try:
            # Call the library service method
            print(f"Attempting to borrow item {item_id} for user {self.app.current_user.name}")
            result = self.app.library.borrow_item(item_id, self.app.current_user)
            
            # Debug print to see what's returned
            print(f"Borrow result: {result}, Type: {type(result)}")
            
            # Process the result
            if isinstance(result, tuple) and len(result) == 2:
                success, message = result
            elif isinstance(result, bool):
                success = result
                message = f"Item '{item.title}' borrowed successfully!" if success else f"Failed to borrow '{item.title}'"
            elif isinstance(result, str):
                success = "success" in result.lower() or "borrowed" in result.lower()
                message = result
            else:
                success = False
                message = f"Unexpected return type: {type(result)}"
            
            if success:
                messagebox.showinfo("Success", message)
                # Refresh the display
                self.show_available_items()
                # Update dashboard if it exists
                if hasattr(self.app, 'dashboard_tab'):
                    self.app.dashboard_tab.refresh_stats()
                # Clear search
                self.clear_search()
            else:
                messagebox.showerror("Error", message)
                
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                messagebox.showerror("Error", "The library service returned None. Please check the borrow_item method.")
            else:
                messagebox.showerror("Error", f"Attribute error: {str(e)}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while borrowing: {str(e)}")
            import traceback
            traceback.print_exc()

    def return_item(self, item_id):
        """Return an item - handles different return types"""
        # Verify item ID format
        if not item_id or not isinstance(item_id, str):
            messagebox.showerror("Error", f"Invalid item ID: {item_id}")
            return
        
        if not item_id.startswith(('BK', 'EB', 'MG')):
            messagebox.showerror("Error", f"Invalid item ID format: {item_id}. Item IDs should start with BK, EB, or MG")
            return
        
        # Find the item from user's borrowed items
        item = None
        if hasattr(self.app.current_user, 'borrowed_items'):
            for borrowed_item in self.app.current_user.borrowed_items:
                if borrowed_item.item_id == item_id:
                    item = borrowed_item
                    break
        
        if not item:
            messagebox.showerror("Error", f"Item {item_id} not found in your borrowed items")
            return
        
        try:
            # Call the library service method
            print(f"Attempting to return item {item_id} for user {self.app.current_user.name}")
            result = self.app.library.return_item(item_id, self.app.current_user)
            
            # Debug print to see what's returned
            print(f"Return result: {result}, Type: {type(result)}")
            
            # Process the result
            if isinstance(result, tuple) and len(result) == 2:
                success, message = result
            elif isinstance(result, bool):
                success = result
                message = f"Item '{item.title}' returned successfully!" if success else f"Failed to return '{item.title}'"
            elif isinstance(result, str):
                success = "success" in result.lower() or "returned" in result.lower()
                message = result
            else:
                success = False
                message = f"Unexpected return type: {type(result)}"
            
            if success:
                messagebox.showinfo("Success", message)
                # Refresh the display
                self.show_borrowed_items()
                # Update dashboard if it exists
                if hasattr(self.app, 'dashboard_tab'):
                    self.app.dashboard_tab.refresh_stats()
                # Clear search
                self.clear_search()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while returning: {str(e)}")
            import traceback
            traceback.print_exc()

    def borrow_item_action(self):
        """Handle borrow item action (called from other tabs)"""
        if not self.app.current_user:
            messagebox.showwarning("No User", "Please select a user first")
            return
        
        # Switch to borrow tab
        self.app.notebook.select(3)  # Borrow tab index
        
        # Force the borrow tab to show available items
        if hasattr(self.app, 'borrow_tab'):
            self.app.borrow_tab.current_mode = "borrow"
            self.app.borrow_tab.show_available_items()
    
    def return_item_action(self):
        """Handle return item action (called from other tabs)"""
        if not self.app.current_user:
            messagebox.showwarning("No User", "Please select a user first")
            return
        
        # Check if user has any borrowed items
        if not hasattr(self.app.current_user, 'borrowed_items') or not self.app.current_user.borrowed_items:
            messagebox.showinfo("No Items", f"{self.app.current_user.name} has no borrowed items to return")
            return
        
        # Switch to borrow tab
        self.app.notebook.select(3)  # Borrow tab index
        
        # Force the borrow tab to show this user's borrowed items
        if hasattr(self.app, 'borrow_tab'):
            self.app.borrow_tab.current_mode = "return"
            self.app.borrow_tab.show_borrowed_items()
    
    def show_user_items(self, user):
        """Show borrowed items for a specific user (called from dashboard)"""
        self.app.set_current_user(user)
        self.show_borrowed_items()