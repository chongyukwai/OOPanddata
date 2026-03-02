"""
Users Tab - Manage and select users
"""
import tkinter as tk
from tkinter import ttk, messagebox

from config.styles import Colors, Fonts
from models.users.library_user import LibraryUser
from gui.dialogs.user_details_dialog import UserDetailsDialog
from gui.dialogs.register_dialog import RegisterDialog


class UsersTab(ttk.Frame):
    """Users management tab"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(style='Card.TFrame')
        
        self.create_widgets()
        self.refresh_user_list()
        
        # Select a default user after the UI is created
        self.after(100, self.select_default_user)  # Wait 100ms for UI to fully load
    
    def create_widgets(self):
        """Create user management widgets"""
        # Top frame for actions
        action_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="➕ Add User",
                  command=self.add_user,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="🔄 Refresh",
                  command=self.refresh_user_list,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:",
                font=Fonts.BODY,
                bg=Colors.BACKGROUND).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_users())
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # User list with details
        list_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create Treeview
        columns = ('ID', 'Name', 'Email', 'Membership', 'Borrowed', 'Fines', 'Status')
        self.user_tree = ttk.Treeview(list_frame, columns=columns, 
                                      show='headings', height=20)
        
        # Define headings
        self.user_tree.heading('ID', text='User ID')
        self.user_tree.heading('Name', text='Name')
        self.user_tree.heading('Email', text='Email')
        self.user_tree.heading('Membership', text='Membership')
        self.user_tree.heading('Borrowed', text='Borrowed')
        self.user_tree.heading('Fines', text='Fines ($)')
        self.user_tree.heading('Status', text='Status')
        
        # Set column widths
        self.user_tree.column('ID', width=80)
        self.user_tree.column('Name', width=150)
        self.user_tree.column('Email', width=180)
        self.user_tree.column('Membership', width=80)
        self.user_tree.column('Borrowed', width=70)
        self.user_tree.column('Fines', width=70)
        self.user_tree.column('Status', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                  command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to select user
        self.user_tree.bind('<Double-Button-1>', self.on_double_click)
        
        # Bind single click to show selection
        self.user_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # Right-click menu
        self.create_context_menu()
        
        # Bottom frame for user selection
        select_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        select_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.selected_user_label = tk.Label(select_frame,
                                           text="Current User: None",
                                           font=Fonts.BODY_BOLD,
                                           bg=Colors.BACKGROUND,
                                           fg=Colors.PRIMARY)
        self.selected_user_label.pack(side=tk.LEFT, padx=5)
        
        # Add a small indicator for selected user
        self.selection_indicator = tk.Label(select_frame,
                                          text="",
                                          font=Fonts.BODY,
                                          bg=Colors.BACKGROUND,
                                          fg=Colors.SUCCESS)
        self.selection_indicator.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(select_frame, text="👤 Select User",
                  command=self.select_current_user,
                  style='Primary.TButton').pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(select_frame, text="📋 View Details",
                  command=self.view_user_details,
                  style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)
    
    def select_default_user(self):
        """Select the first user as default"""
        try:
            # Get all users
            users = self.app.library.get_all_users()
            
            if users:
                # Select the first user
                default_user = users[0]
                
                # Set as current user
                self.app.set_current_user(default_user)
                
                # Update labels
                self.selected_user_label.config(
                    text=f"Current User: {default_user.name} ({default_user.membership_level})",
                    fg=Colors.SUCCESS
                )
                
                # Find and highlight the user in the tree
                self.highlight_user_in_tree(default_user.user_id)
                
                # Update status bar - use set_message instead of set_status
                if hasattr(self.app, 'status_bar'):
                    self.app.status_bar.set_message(f"✅ Default user selected: {default_user.name}")
                    self.app.status_bar.set_user(default_user)
                
                print(f"Default user selected: {default_user.name}")
            else:
                print("No users found to select as default")
                if hasattr(self.app, 'status_bar'):
                    self.app.status_bar.set_message("No users available")
                
        except Exception as e:
            print(f"Error selecting default user: {e}")
            if hasattr(self.app, 'status_bar'):
                self.app.status_bar.set_message(f"Error: {e}")
    
    def highlight_user_in_tree(self, user_id):
        """Highlight a specific user in the tree"""
        # Search for the user in the tree
        for item in self.user_tree.get_children():
            item_values = self.user_tree.item(item)['values']
            if item_values and item_values[0] == user_id:
                self.user_tree.selection_set(item)
                self.user_tree.see(item)  # Scroll to the item
                self.user_tree.focus(item)  # Set focus to the item
                break
    
    def create_context_menu(self):
        """Create right-click context menu"""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="👤 Select User", 
                                      command=self.select_current_user)
        self.context_menu.add_command(label="📋 View Details", 
                                      command=self.view_user_details)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📚 View Borrowed Items", 
                                      command=self.view_borrowed_items)
        self.context_menu.add_command(label="💰 Manage Fines", 
                                      command=self.manage_fines)
        
        # Bind right-click
        self.user_tree.bind('<Button-3>', self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the item under cursor
        item = self.user_tree.identify_row(event.y)
        if item:
            self.user_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def on_tree_select(self, event):
        """Handle tree selection change"""
        selection = self.user_tree.selection()
        if selection:
            # Get the selected item's values
            item_values = self.user_tree.item(selection[0])['values']
            if item_values:
                self.selection_indicator.config(text=f"✓ Selected: {item_values[1]}")
        else:
            self.selection_indicator.config(text="")
    
    def on_double_click(self, event):
        """Handle double-click on tree item"""
        try:
            # Get the item that was double-clicked
            item = self.user_tree.identify_row(event.y)
            if not item:
                return
            
            # Select the item
            self.user_tree.selection_set(item)
            
            # Get the item's values
            item_values = self.user_tree.item(item)['values']
            if not item_values:
                return
            
            user_id = item_values[0]
            user_name = item_values[1]
            
            # Get user from library
            user = self.app.library.get_user(user_id)
            if user:
                # Set as current user
                self.app.set_current_user(user)
                
                # Update labels
                self.selected_user_label.config(
                    text=f"Current User: {user.name} ({user.membership_level})",
                    fg=Colors.SUCCESS
                )
                
                # Update status if available - check if status_bar exists
                if hasattr(self.app, 'status_bar'):
                    self.app.status_bar.set_message(f"✅ Selected user: {user.name}")
                    self.app.status_bar.set_user(user)
                elif hasattr(self.app, 'status_label'):
                    self.app.status_label.config(text=f"Current User: {user.name}")
                
                # Optional: Highlight the selected row
                self.user_tree.selection_set(item)
                
                print(f"User selected via double-click: {user.name}")
            else:
                print(f"User not found: {user_id}")
                if hasattr(self.app, 'status_bar'):
                    self.app.status_bar.set_message(f"❌ User not found: {user_id}")
                    
        except Exception as e:
            print(f"Error in double-click handler: {e}")
            # Safe error handling
            if hasattr(self.app, 'status_bar'):
                self.app.status_bar.set_message(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to select user: {e}")
    
    def refresh_user_list(self):
        """Refresh the user list"""
        # Clear current items
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # Get all users
        users = self.app.library.get_all_users()
        
        # Add users to tree
        for user in users:
            # Determine status
            overdue_count = len(user.get_overdue_items()) if hasattr(user, 'get_overdue_items') else 0
            if overdue_count > 0:
                status = f"⚠️ {overdue_count} overdue"
                tags = ('overdue',)
            elif user.fines_owed > 0:
                status = f"💰 ${user.fines_owed:.2f}"
                tags = ('fines',)
            else:
                status = "✅ Active"
                tags = ('active',)
            
            # Insert user
            self.user_tree.insert('', tk.END,
                                 values=(
                                     user.user_id,
                                     user.name,
                                     user.email,
                                     user.membership_level,
                                     f"{len(user.borrowed_items)}/{user.get_max_borrow_limit()}",
                                     f"{user.fines_owed:.2f}",
                                     status
                                 ),
                                 tags=tags)
        
        # Configure tag colors
        self.user_tree.tag_configure('overdue', foreground='red')
        self.user_tree.tag_configure('fines', foreground='orange')
        self.user_tree.tag_configure('active', foreground='green')
        
        # Update current user display if exists
        if self.app.current_user:
            self.selected_user_label.config(
                text=f"Current User: {self.app.current_user.name} ({self.app.current_user.membership_level})",
                fg=Colors.SUCCESS
            )
            
            # Find and highlight the current user in the tree
            if hasattr(self.app.current_user, 'user_id'):
                self.highlight_user_in_tree(self.app.current_user.user_id)
    
    def filter_users(self):
        """Filter users based on search"""
        keyword = self.search_var.get().lower()
        
        # Clear current items
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # Get all users
        users = self.app.library.get_all_users()
        
        # Filter and add users
        for user in users:
            if (keyword in user.name.lower() or 
                keyword in user.email.lower() or 
                keyword in user.user_id.lower()):
                
                # Determine status
                overdue_count = len(user.get_overdue_items()) if hasattr(user, 'get_overdue_items') else 0
                if overdue_count > 0:
                    status = f"⚠️ {overdue_count} overdue"
                    tags = ('overdue',)
                elif user.fines_owed > 0:
                    status = f"💰 ${user.fines_owed:.2f}"
                    tags = ('fines',)
                else:
                    status = "✅ Active"
                    tags = ('active',)
                
                # Insert user
                self.user_tree.insert('', tk.END,
                                     values=(
                                         user.user_id,
                                         user.name,
                                         user.email,
                                         user.membership_level,
                                         f"{len(user.borrowed_items)}/{user.get_max_borrow_limit()}",
                                         f"{user.fines_owed:.2f}",
                                         status
                                     ),
                                     tags=tags)
        
        # After filtering, try to highlight current user again
        if self.app.current_user and hasattr(self.app.current_user, 'user_id'):
            self.highlight_user_in_tree(self.app.current_user.user_id)
    
    def add_user(self):
        """Add a new user"""
        dialog = RegisterDialog(self.app, mode='user')
        self.wait_window(dialog.window)
        self.refresh_user_list()
    
    def select_current_user(self):
        """Select the current user"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user")
            return
        
        # Get user ID from selected row
        item_values = self.user_tree.item(selection[0])['values']
        user_id = item_values[0]
        
        # Get user from library
        user = self.app.library.get_user(user_id)
        if user:
            self.app.set_current_user(user)
            self.selected_user_label.config(
                text=f"Current User: {user.name} ({user.membership_level})",
                fg=Colors.SUCCESS
            )
            if hasattr(self.app, 'status_bar'):
                self.app.status_bar.set_message(f"✅ Selected user: {user.name}")
                self.app.status_bar.set_user(user)
            messagebox.showinfo("Success", f"Selected user: {user.name}")
    
    def view_user_details(self):
        """View selected user details"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user")
            return
        
        # Get user ID from selected row
        item_values = self.user_tree.item(selection[0])['values']
        user_id = item_values[0]
        
        try:
            # Open user details dialog
            dialog = UserDetailsDialog(self.app, user_id)
            
            # Check if dialog was created successfully
            if hasattr(dialog, 'window') and dialog.window:
                self.wait_window(dialog.window)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open user details: {e}")
        finally:
            # Refresh the user list to show any changes
            self.refresh_user_list()
    
    def view_borrowed_items(self):
        """View borrowed items for selected user"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user")
            return
        
        # Get user ID from selected row
        item_values = self.user_tree.item(selection[0])['values']
        user_id = item_values[0]
        
        # Switch to borrow tab
        self.app.notebook.select(3)  # Index of borrow tab
        
        # Select the user if not already selected
        user = self.app.library.get_user(user_id)
        if user:
            self.app.set_current_user(user)
            messagebox.showinfo("Info", f"Viewing borrowed items for: {user.name}")
    
    def manage_fines(self):
        """Manage fines for selected user"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user")
            return
        
        # Get user ID from selected row
        item_values = self.user_tree.item(selection[0])['values']
        user_id = item_values[0]
        
        # Get user
        user = self.app.library.get_user(user_id)
        if not user:
            return
        
        # Show fine management dialog
        self.show_fine_dialog(user)
    
    def show_fine_dialog(self, user):
        """Show dialog to manage fines"""
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Manage Fines")
        dialog.geometry("400x200")
        dialog.configure(bg=Colors.BACKGROUND)
        dialog.transient(self.app.root)
        dialog.grab_set()
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
        
        # Center window
        dialog.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = tk.Frame(dialog, bg=Colors.BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # User info
        tk.Label(main_frame, text=f"User: {user.name}",
                font=Fonts.HEADER,
                bg=Colors.BACKGROUND,
                fg=Colors.PRIMARY).pack(pady=(0, 10))
        
        tk.Label(main_frame, text=f"Current Fines: ${user.fines_owed:.2f}",
                font=Fonts.BODY_BOLD,
                bg=Colors.BACKGROUND,
                fg=Colors.DANGER if user.fines_owed > 0 else Colors.SUCCESS).pack(pady=(0, 20))
        
        # Payment frame
        pay_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        pay_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(pay_frame, text="Payment Amount: $",
                font=Fonts.BODY,
                bg=Colors.BACKGROUND).pack(side=tk.LEFT)
        
        amount_var = tk.StringVar(value="0.00")
        amount_entry = ttk.Entry(pay_frame, textvariable=amount_var, width=15)
        amount_entry.pack(side=tk.LEFT, padx=5)
        amount_entry.focus_set()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(pady=20)
        
        def make_payment():
            try:
                amount = float(amount_var.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Please enter a positive amount")
                    return
                    
                success, message = user.pay_fines(amount)
                if success:
                    messagebox.showinfo("Success", message)
                    self.refresh_user_list()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        ttk.Button(button_frame, text="Pay Fines",
                  command=make_payment,
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel",
                  command=dialog.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)