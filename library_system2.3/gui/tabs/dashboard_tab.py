"""
Dashboard tab - shows overview and statistics
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

from config.styles import Colors, Fonts


class DashboardTab(ttk.Frame):
    """Dashboard tab with overview and quick actions"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(style='Card.TFrame')
        
        # Store references to stats labels for refresh_stats method
        self.total_items_label = None
        self.available_items_label = None
        self.total_users_label = None
        self.borrowed_tree = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dashboard widgets"""
        # Create two-column layout
        left_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column: Statistics
        stats_frame = tk.LabelFrame(left_frame, text="📈 Library Statistics",
                                   font=Fonts.SUBHEADER,
                                   bg=Colors.BACKGROUND,
                                   fg=Colors.PRIMARY,
                                   padx=15, pady=15)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stats_display = tk.Frame(stats_frame, bg=Colors.BACKGROUND)
        self.stats_display.pack(fill=tk.BOTH, expand=True)
        
        # Add borrowed items section in left column
        borrowed_frame = tk.LabelFrame(left_frame, text="📚 Your Borrowed Items",
                                      font=Fonts.SUBHEADER,
                                      bg=Colors.BACKGROUND,
                                      fg=Colors.PRIMARY,
                                      padx=15, pady=15)
        borrowed_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create treeview for borrowed items
        columns = ('ID', 'Title', 'Type', 'Due Date', 'Status')
        self.borrowed_tree = ttk.Treeview(borrowed_frame, columns=columns, show='headings', height=5)
        
        # Define headings
        self.borrowed_tree.heading('ID', text='Item ID')
        self.borrowed_tree.heading('Title', text='Title')
        self.borrowed_tree.heading('Type', text='Type')
        self.borrowed_tree.heading('Due Date', text='Due Date')
        self.borrowed_tree.heading('Status', text='Status')
        
        # Define column widths
        self.borrowed_tree.column('ID', width=80)
        self.borrowed_tree.column('Title', width=150)
        self.borrowed_tree.column('Type', width=80)
        self.borrowed_tree.column('Due Date', width=100)
        self.borrowed_tree.column('Status', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(borrowed_frame, orient=tk.VERTICAL, command=self.borrowed_tree.yview)
        self.borrowed_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right column: Quick Actions
        actions_frame = tk.LabelFrame(right_frame, text="⚡ Quick Actions",
                                     font=Fonts.SUBHEADER,
                                     bg=Colors.BACKGROUND,
                                     fg=Colors.PRIMARY,
                                     padx=15, pady=15)
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Regular action buttons
        actions = [
            ("🔍 Search Items", self.show_search_dialog),
            ("📚 Browse Catalog", lambda: self.app.notebook.select(1)),
            ("👥 View Users", lambda: self.app.notebook.select(2)),
            ("➕ Register User", self.show_register_dialog),
            ("📝 Add New Item", self.show_add_item_dialog),
            ("🔄 Refresh Dashboard", self.refresh_stats),
        ]
        
        # Add Borrow/Return section with current user check
        borrow_frame = tk.LabelFrame(actions_frame, text="📖 Borrow/Return Actions",
                                   font=Fonts.BODY_BOLD,
                                   bg=Colors.BACKGROUND,
                                   fg=Colors.ACCENT,
                                   padx=10, pady=10)
        borrow_frame.pack(fill=tk.X, pady=10)
        
        borrow_actions = [
            ("📤 Borrow Item", self.borrow_item_action),
            ("📥 Return Item", self.return_item_action),
            ("📋 View Borrowed", self.view_borrowed_items)
        ]
        
        for text, command in borrow_actions:
            btn = ttk.Button(borrow_frame, text=text, command=command,
                            style='Accent.TButton' if "Borrow" in text else 'Secondary.TButton')
            btn.pack(fill=tk.X, pady=2)
        
        # Regular actions
        for text, command in actions:
            btn = ttk.Button(actions_frame, text=text, command=command,
                            style='Primary.TButton')
            btn.pack(fill=tk.X, pady=2)
        
        # User info section
        user_frame = tk.LabelFrame(right_frame, text="👤 Current User Info",
                                  font=Fonts.SUBHEADER,
                                  bg=Colors.BACKGROUND,
                                  fg=Colors.PRIMARY,
                                  padx=15, pady=15)
        user_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.user_details = tk.Text(user_frame,
                                   height=10,
                                   font=Fonts.BODY,
                                   bg=Colors.WHITE,
                                   wrap=tk.WORD)
        self.user_details.pack(fill=tk.BOTH, expand=True)
        self.user_details.config(state=tk.DISABLED)
        
        # User info label for quick reference
        self.user_info_label = tk.Label(user_frame, text="",
                                       font=Fonts.BODY_BOLD,
                                       bg=Colors.BACKGROUND,
                                       fg=Colors.PRIMARY)
        self.user_info_label.pack(pady=5)
        
        # Initial update
        self.update_display()
    
    def refresh_stats(self):
        """Refresh the dashboard statistics"""
        try:
            self.update_stats()
            self.update_user_details()
            self.update_borrowed_items()
            
            # Show success message in status bar if available
            if hasattr(self.app, 'status_bar'):
                self.app.status_bar.set_message("Dashboard refreshed successfully")
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
            messagebox.showerror("Error", f"Failed to refresh dashboard: {str(e)}")
    
    def update_borrowed_items(self):
        """Update the borrowed items treeview"""
        # Clear existing items
        for item in self.borrowed_tree.get_children():
            self.borrowed_tree.delete(item)
        
        # Check if user has borrowed items
        if self.app.current_user and hasattr(self.app.current_user, 'borrowed_items'):
            for item in self.app.current_user.borrowed_items:
                due_date_str = item.due_date.strftime("%Y-%m-%d") if hasattr(item, 'due_date') and item.due_date else "N/A"
                
                # Check if overdue
                status = "✅ On Time"
                if hasattr(item, 'due_date') and item.due_date:
                    if datetime.now() > item.due_date:
                        status = "⚠️ Overdue"
                
                self.borrowed_tree.insert('', tk.END, values=(
                    item.item_id,
                    item.title,
                    item.get_item_type(),
                    due_date_str,
                    status
                ))
    
    def update_display(self):
        """Update dashboard displays"""
        self.update_stats()
        self.update_user_details()
        self.update_borrowed_items()
    
    def update_stats(self):
        """Update statistics display"""
        # Clear existing
        for widget in self.stats_display.winfo_children():
            widget.destroy()
        
        try:
            stats = self.app.library.get_catalog_stats()
            user_stats = self.app.library.get_user_stats()
            
            # Store values for refresh_stats method
            total_items = stats.get('total_items', 0)
            available_items = stats.get('available_items', 0)
            total_users = user_stats.get('total_users', 0)
            
            # Create stat cards
            display_stats = [
                ("📚 Total Items", total_items, Colors.PRIMARY),
                ("✅ Available", available_items, Colors.SUCCESS),
                ("📖 Borrowed", stats.get('borrowed_items', 0), Colors.WARNING),
                ("📊 Books", stats.get('books', 0), Colors.ACCENT),
                ("💾 EBooks", stats.get('ebooks', 0), Colors.INFO),
                ("📰 Magazines", stats.get('magazines', 0), Colors.SECONDARY),
                ("👥 Users", total_users, Colors.PRIMARY),
                ("👔 Librarians", user_stats.get('total_librarians', 0), Colors.SECONDARY),
                ("💰 Total Fines", f"${user_stats.get('total_fines', 0):.2f}", Colors.DANGER)
            ]
            
            for text, value, color in display_stats:
                stat_frame = tk.Frame(self.stats_display, bg=Colors.BACKGROUND)
                stat_frame.pack(fill=tk.X, pady=5)
                
                tk.Label(stat_frame, text=text, font=Fonts.BODY,
                        bg=Colors.BACKGROUND, fg=color).pack(side=tk.LEFT)
                
                value_label = tk.Label(stat_frame, text=str(value),
                                      font=Fonts.BODY_BOLD,
                                      bg=Colors.BACKGROUND, fg=color)
                value_label.pack(side=tk.RIGHT)
                
                # Store references for quick access
                if text == "📚 Total Items":
                    self.total_items_label = value_label
                elif text == "✅ Available":
                    self.available_items_label = value_label
                elif text == "👥 Users":
                    self.total_users_label = value_label
                    
        except Exception as e:
            # Show error in stats display
            error_label = tk.Label(self.stats_display, 
                                  text=f"Error loading stats: {e}",
                                  font=Fonts.BODY,
                                  bg=Colors.BACKGROUND,
                                  fg=Colors.DANGER)
            error_label.pack(pady=20)
    
    def update_user_details(self):
        """Update user details display"""
        self.user_details.config(state=tk.NORMAL)
        self.user_details.delete(1.0, tk.END)
        
        if self.app.current_user:
            # Update user info label
            if hasattr(self.app.current_user, 'user_id'):
                user_text = f"Current User: {self.app.current_user.name} (ID: {self.app.current_user.user_id})"
            else:
                user_text = f"Current User: {self.app.current_user.name} (Employee ID: {self.app.current_user.employee_id})"
            self.user_info_label.config(text=user_text, fg=Colors.SUCCESS)
            
            # Build user info string
            user_info = f"Name: {self.app.current_user.name}\n"
            
            if hasattr(self.app.current_user, 'user_id'):
                user_info += f"ID: {self.app.current_user.user_id}\n"
                user_info += f"Type: Regular User\n"
            elif hasattr(self.app.current_user, 'employee_id'):
                user_info += f"ID: {self.app.current_user.employee_id}\n"
                user_info += f"Type: Librarian\n"
            
            if hasattr(self.app.current_user, 'email'):
                user_info += f"Email: {self.app.current_user.email}\n"
            
            if hasattr(self.app.current_user, 'membership_level'):
                user_info += f"Membership: {self.app.current_user.membership_level}\n"
            
            if hasattr(self.app.current_user, 'borrowed_items'):
                user_info += f"\n📚 Total Borrowed: {len(self.app.current_user.borrowed_items)} items\n"
                
                # Count overdue items
                overdue_count = 0
                for item in self.app.current_user.borrowed_items:
                    if hasattr(item, 'due_date') and item.due_date and datetime.now() > item.due_date:
                        overdue_count += 1
                
                if overdue_count > 0:
                    user_info += f"⚠️ Overdue: {overdue_count} items\n"
            
            self.user_details.insert(tk.END, user_info)
        else:
            self.user_info_label.config(text="No user selected", fg=Colors.DANGER)
            self.user_details.insert(tk.END, "No user selected\nPlease register or select a user from the Users tab")
        
        self.user_details.config(state=tk.DISABLED)
    
    def show_search_dialog(self):
        """Show search dialog"""
        from gui.dialogs.search_dialog import SearchDialog
        SearchDialog(self.app)
    
    def show_add_item_dialog(self):
        """Show add item dialog"""
        from gui.dialogs.add_item_dialog import AddItemDialog
        AddItemDialog(self.app)
    
    def show_register_dialog(self):
        """Show register dialog"""
        from gui.dialogs.register_dialog import RegisterDialog
        RegisterDialog(self.app)
    
    def borrow_item_action(self):
        """Handle borrow item action"""
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
        """Handle return item action"""
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
    
    def view_borrowed_items(self):
        """View current user's borrowed items"""
        if not self.app.current_user:
            messagebox.showwarning("No User", "Please select a user first")
            return
        
        # Switch to borrow tab
        self.app.notebook.select(3)  # Borrow tab index
        
        # Show borrowed items
        if hasattr(self.app, 'borrow_tab'):
            self.app.borrow_tab.current_mode = "return"
            self.app.borrow_tab.show_borrowed_items()
    
    def tab_selected(self):
        """Called when this tab is selected"""
        self.refresh_stats()