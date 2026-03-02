"""
Header component for the main window
"""
import tkinter as tk
from tkinter import ttk
from config.styles import Colors, Styles


class Header(ttk.Frame):
    """Header component with user info and controls"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, style='TFrame')
        self.controller = controller
        self.current_user = None
        
        # Configure frame
        self.configure(relief='solid', borderwidth=1)
        
        # Create widgets
        self.create_widgets()
        
        # Update display
        self.update_display()
    
    def create_widgets(self):
        """Create header widgets"""
        # Title
        self.title_label = ttk.Label(
            self,
            text="📚 Library Management System",
            style='Title.TLabel'
        )
        self.title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # User info frame
        self.user_frame = ttk.Frame(self, style='TFrame')
        self.user_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # User info labels
        self.user_name_label = ttk.Label(
            self.user_frame,
            text="No user selected",
            style='Subheader.TLabel'
        )
        self.user_name_label.pack(anchor=tk.E)
        
        self.user_role_label = ttk.Label(
            self.user_frame,
            text="Please register or select a user",
            style='TLabel'
        )
        self.user_role_label.pack(anchor=tk.E)
        
        # User actions frame
        self.actions_frame = ttk.Frame(self.user_frame, style='TFrame')
        self.actions_frame.pack(pady=(5, 0))
        
        # Switch user button
        self.switch_user_btn = ttk.Button(
            self.actions_frame,
            text="Switch User",
            command=self.switch_user,
            style='Secondary.TButton',
            width=12
        )
        self.switch_user_btn.pack(side=tk.LEFT, padx=2)
        
        # Register button
        self.register_btn = ttk.Button(
            self.actions_frame,
            text="Register",
            command=self.register_user,
            style='Primary.TButton',
            width=12
        )
        self.register_btn.pack(side=tk.LEFT, padx=2)
    
    def switch_user(self):
        """Switch current user"""
        from gui.dialogs.user_switch_dialog import UserSwitchDialog
        dialog = UserSwitchDialog(self.controller)
        dialog.show()
    
    def register_user(self):
        """Register new user"""
        from gui.dialogs.register_dialog import RegisterDialog
        dialog = RegisterDialog(self.controller)
        dialog.show()
    
    def set_current_user(self, user):
        """Set current user and update display"""
        self.current_user = user
        self.update_display()
    
    def update_display(self):
        """Update user information display"""
        if self.current_user:
            # Update user info
            user_name = getattr(self.current_user, 'name', 'Unknown')
            user_role = self.current_user.get_role()
            
            if hasattr(self.current_user, 'user_id'):
                user_id = self.current_user.user_id
            elif hasattr(self.current_user, 'employee_id'):
                user_id = self.current_user.employee_id
            else:
                user_id = "Unknown"
            
            self.user_name_label.config(text=f"{user_name}")
            self.user_role_label.config(text=f"{user_role} | ID: {user_id}")
            
            # Update button states
            self.switch_user_btn.config(state='normal')
            self.register_btn.config(text="Add User")
        else:
            # No user selected
            self.user_name_label.config(text="No user selected")
            self.user_role_label.config(text="Please register or select a user")
            self.switch_user_btn.config(state='normal')
            self.register_btn.config(text="Register")
    
    def get_current_user(self):
        """Get current user"""
        return self.current_user
