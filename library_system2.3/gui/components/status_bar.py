"""
Status bar component
"""
import tkinter as tk

from config.styles import Colors, Fonts


class StatusBar(tk.Frame):
    """Status bar at bottom of window"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg=Colors.DARK, height=30)
        self.app = app
        self.pack_propagate(False)
        
        self.create_widgets()
        self.update()
    
    def create_widgets(self):
        """Create status bar widgets"""
        # Status message
        self.status_label = tk.Label(self,
                                    text="Ready",
                                    font=Fonts.BODY_SMALL,
                                    bg=Colors.DARK,
                                    fg=Colors.WHITE)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Current user display
        self.user_label = tk.Label(self,
                                  text="No user selected",
                                  font=Fonts.BODY_SMALL,
                                  bg=Colors.DARK,
                                  fg=Colors.WHITE)
        self.user_label.pack(side=tk.LEFT, padx=20)
        
        # Stats
        self.stats_label = tk.Label(self,
                                   font=Fonts.BODY_SMALL,
                                   bg=Colors.DARK,
                                   fg=Colors.WHITE)
        self.stats_label.pack(side=tk.RIGHT, padx=10)
    
    def update(self):
        """Update status bar info"""
        stats = self.app.library.get_catalog_stats()
        
        # Get values with defaults
        total_items = stats.get('total_items', 0)
        available_items = stats.get('available_items', 0)
        total_users = stats.get('total_users', 0)
        
        self.stats_label.config(
            text=f"📚 Items: {total_items} | "
                 f"✅ Available: {available_items} | "
                 f"👥 Users: {total_users}"
        )
        
        # Update user display if there's a current user
        if hasattr(self.app, 'current_user') and self.app.current_user:
            user = self.app.current_user
            self.user_label.config(
                text=f"👤 Current: {user.name} ({user.membership_level if hasattr(user, 'membership_level') else 'Staff'})",
                fg=Colors.SUCCESS
            )
        else:
            self.user_label.config(text="👤 No user selected", fg=Colors.WHITE)
    
    def set_message(self, message: str):
        """Set status message"""
        self.status_label.config(text=message)
        # Clear after 5 seconds
        self.after(5000, lambda: self.status_label.config(text="Ready"))
    
    def set_user(self, user):
        """Set current user display"""
        if user:
            self.user_label.config(
                text=f"👤 Current: {user.name} ({user.membership_level if hasattr(user, 'membership_level') else 'Staff'})",
                fg=Colors.SUCCESS
            )
        else:
            self.user_label.config(text="👤 No user selected", fg=Colors.WHITE)