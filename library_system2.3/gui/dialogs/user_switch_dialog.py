"""
Dialog for switching between users
"""
import tkinter as tk
from tkinter import ttk, messagebox
from config.styles import Colors, Styles


class UserSwitchDialog:
    """Dialog for switching between users"""
    
    def __init__(self, controller):
        self.controller = controller
        self.dialog = None
        self.result = None
    
    def show(self):
        """Show the dialog"""
        self.dialog = tk.Toplevel(self.controller.root)
        self.dialog.title("Switch User")
        self.dialog.geometry("400x500")
        self.dialog.configure(bg=Colors.BACKGROUND)
        self.dialog.resizable(False, False)
        self.dialog.transient(self.controller.root)
        self.dialog.grab_set()
        
        # Center dialog
        self.center_dialog()
        
        # Create widgets
        self.create_widgets()
        
        # Wait for dialog to close
        self.controller.root.wait_window(self.dialog)
        
        return self.result
    
    def center_dialog(self):
        """Center the dialog on parent window"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = self.controller.root.winfo_x() + (self.controller.root.winfo_width() // 2) - (width // 2)
        y = self.controller.root.winfo_y() + (self.controller.root.winfo_height() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, style='TFrame', padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Select User",
            style='Header.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Get current user
        current_user = None
        if hasattr(self.controller, 'header'):
            current_user = self.controller.header.get_current_user()
        
        # Get all users
        users = []
        if hasattr(self.controller, 'library_service'):
            users = self.controller.library_service.get_all_users()
        
        if not users:
            # No users message
            no_users_label = ttk.Label(
                main_frame,
                text="No users available.\nPlease register a user first.",
                style='Info.TLabel',
                justify=tk.CENTER
            )
            no_users_label.pack(expand=True)
            
            # Register button
            register_btn = ttk.Button(
                main_frame,
                text="➕ Register User",
                command=self.register_user,
                style='Primary.TButton'
            )
            register_btn.pack(pady=20)
            
            # Close button
            close_btn = ttk.Button(
                main_frame,
                text="Close",
                command=self.dialog.destroy,
                style='Secondary.TButton'
            )
            close_btn.pack()
            
            return
        
        # Users listbox frame
        listbox_frame = ttk.Frame(main_frame, style='TFrame')
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Listbox with scrollbar
        listbox_container = ttk.Frame(listbox_frame, style='TFrame')
        listbox_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(listbox_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.users_listbox = tk.Listbox(
            listbox_container,
            yscrollcommand=scrollbar.set,
            font=Styles.get_font(11),
            bg=Colors.SURFACE,
            selectmode=tk.SINGLE,
            height=15
        )
        self.users_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.users_listbox.yview)
        
        # Add users to listbox
        current_user_index = -1
        for i, user in enumerate(users):
            user_name = getattr(user, 'name', 'Unknown')
            user_role = user.get_role()
            
            # Mark current user
            if user == current_user:
                display_text = f"👤 {user_name} ({user_role}) - CURRENT"
                current_user_index = i
            else:
                display_text = f"👤 {user_name} ({user_role})"
            
            self.users_listbox.insert(tk.END, display_text)
        
        # Select current user if exists
        if current_user_index >= 0:
            self.users_listbox.selection_set(current_user_index)
            self.users_listbox.see(current_user_index)
        
        # Bind double-click
        self.users_listbox.bind('<Double-Button-1>', lambda e: self.switch_to_selected_user())
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack()
        
        # Switch button
        switch_btn = ttk.Button(
            button_frame,
            text="🔄 Switch",
            command=self.switch_to_selected_user,
            style='Primary.TButton',
            width=15
        )
        switch_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            style='Secondary.TButton',
            width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def switch_to_selected_user(self):
        """Switch to selected user"""
        selection = self.users_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user.")
            return
        
        index = selection[0]
        
        # Get selected user
        if hasattr(self.controller, 'library_service'):
            users = self.controller.library_service.get_all_users()
            if 0 <= index < len(users):
                selected_user = users[index]
                
                # Check if already current user
                current_user = None
                if hasattr(self.controller, 'header'):
                    current_user = self.controller.header.get_current_user()
                
                if selected_user == current_user:
                    messagebox.showinfo("Already Selected", 
                                      f"{selected_user.name} is already the current user.")
                    return
                
                # Switch to selected user
                if hasattr(self.controller, 'header'):
                    self.controller.header.set_current_user(selected_user)
                    self.controller.set_status(f"Switched to user: {selected_user.name}", "success")
                    
                    # Update all tabs
                    if hasattr(self.controller, 'update_all_tabs'):
                        self.controller.update_all_tabs()
                    
                    # Close dialog
                    self.dialog.destroy()
    
    def register_user(self):
        """Register new user"""
        from gui.dialogs.register_dialog import RegisterDialog
        dialog = RegisterDialog(self.controller)
        if dialog.show():
            # Refresh dialog
            self.dialog.destroy()
            self.show()
