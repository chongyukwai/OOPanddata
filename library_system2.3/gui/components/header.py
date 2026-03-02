"""
Header component for main window
"""
import tkinter as tk

from config.styles import Colors, Fonts


class Header(tk.Frame):
    """Header component with title only (no user switching)"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg=Colors.PRIMARY, height=80)
        self.app = app
        self.pack_propagate(False)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create header widgets - title only"""
        # Title
        title_label = tk.Label(self, 
                              text="📚 Library Management System",
                              font=Fonts.TITLE,
                              bg=Colors.PRIMARY,
                              fg=Colors.WHITE)
        title_label.pack(side=tk.LEFT, padx=20)
    
    def update_user_display(self):
        """Empty method to maintain compatibility"""
        pass