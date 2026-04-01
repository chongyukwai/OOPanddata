"""
Register User Dialog
"""
import tkinter as tk
from tkinter import ttk, messagebox
from config.styles import Colors, Fonts 
from services.library_service import LibraryService
from models.users.library_user import LibraryUser
from models.users.librarian import Librarian


class RegisterDialog:
    """Dialog for registering new users"""
    
    def __init__(self, app, mode='user'):  # Added mode parameter with default value
        self.app = app
        self.mode = mode  # Store mode
        self.result = None  # Store result
        self.window = tk.Toplevel(app.root)
        self.window.title("Register New User")
        self.window.geometry("500x450")
        self.window.configure(bg=Colors.BACKGROUND)
        self.window.transient(app.root)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.library = LibraryService.get_instance()
        
        # Set title based on mode
        if mode == 'user':
            self.window.title("Register New User")
        elif mode == 'librarian':
            self.window.title("Register New Librarian")
        
        self.center_window()
        self.create_widgets()
    
    def on_close(self):
        """Handle window close event"""
        self.window.destroy()
    
    def center_window(self):
        """Center window on parent"""
        self.window.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = tk.Frame(self.window, bg=Colors.BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title based on mode
        if self.mode == 'user':
            title_text = "Register New User"
        else:
            title_text = "Register New Librarian"
            
        tk.Label(main_frame, text=title_text,
                font=Fonts.HEADER,
                bg=Colors.BACKGROUND,
                fg=Colors.PRIMARY).pack(pady=(0, 20))
        
        # Only show user type selection if mode is 'user'
        # If mode is 'librarian', default to librarian type
        if self.mode == 'user':
            type_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
            type_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(type_frame, text="User Type:",
                    font=Fonts.BODY_BOLD,
                    bg=Colors.BACKGROUND).pack(anchor=tk.W)
            
            self.user_type = tk.StringVar(value="Regular User")
            
            types = [
                ("👤 Regular User ", "Regular User"),
                ("👔 Librarian (Library staff)", "Librarian")
            ]
            
            for text, value in types:
                rb = tk.Radiobutton(type_frame, text=text, variable=self.user_type,
                                   value=value, bg=Colors.BACKGROUND,
                                   font=Fonts.BODY)
                rb.pack(anchor=tk.W, pady=2)
        else:
            # For librarian mode, set fixed user type
            self.user_type = tk.StringVar(value="Librarian")
        
        # Form fields
        form_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Name
        name_frame = tk.Frame(form_frame, bg=Colors.BACKGROUND)
        name_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(name_frame, text="Full Name:*",
                font=Fonts.BODY,
                bg=Colors.BACKGROUND, width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=30)
        name_entry.pack(side=tk.LEFT)
        name_entry.focus_set()
        
        # Email
        email_frame = tk.Frame(form_frame, bg=Colors.BACKGROUND)
        email_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(email_frame, text="Email:",
                font=Fonts.BODY,
                bg=Colors.BACKGROUND, width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=self.email_var, width=30)
        email_entry.pack(side=tk.LEFT)
        
        # ID field
        id_frame = tk.Frame(form_frame, bg=Colors.BACKGROUND)
        id_frame.pack(fill=tk.X, pady=5)
        
        self.id_label = tk.Label(id_frame, text="User ID:",
                                font=Fonts.BODY,
                                bg=Colors.BACKGROUND, width=15, anchor=tk.W)
        self.id_label.pack(side=tk.LEFT)
        
        self.id_var = tk.StringVar()
        id_entry = ttk.Entry(id_frame, textvariable=self.id_var, width=30)
        id_entry.pack(side=tk.LEFT)
        
        ttk.Button(id_frame, text="Auto-generate",
                  command=self.auto_generate_id,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=10)
        
        # Update ID label when type changes (only if in user mode)
        if self.mode == 'user':
            self.user_type.trace('w', lambda *args: self.update_id_label())
        self.update_id_label()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(pady=20)
        
        button_text = "👤 Register" if self.mode == 'user' else "👔 Register Librarian"
        ttk.Button(button_frame, text=button_text,
                  command=self.register_user,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel",
                  command=self.on_close,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Auto-generate ID
        self.auto_generate_id()
    
    def update_id_label(self):
        """Update ID label based on user type"""
        if self.mode == 'librarian' or self.user_type.get() == "Librarian":
            self.id_label.config(text="Employee ID:")
        else:
            self.id_label.config(text="User ID:")
    
    def auto_generate_id(self):
        """Auto-generate user ID"""
        users = self.library.get_all_users()
        librarians = self.library.get_all_librarians()
        
        # Determine user type
        if self.mode == 'librarian':
            user_type = "Librarian"
        else:
            user_type = self.user_type.get()
        
        if user_type == "Regular User":
            existing_ids = [user.user_id for user in users]
            prefix = "USR"
        else:
            existing_ids = [lib.employee_id for lib in librarians]
            prefix = "EMP"
        
        counter = 1
        while f"{prefix}{counter:03d}" in existing_ids:
            counter += 1
        
        self.id_var.set(f"{prefix}{counter:03d}")
    
    def register_user(self):
        """Register the user"""
        try:
            # Validate name
            name = self.name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Name is required!")
                return
            
            # Validate ID
            user_id = self.id_var.get().strip().upper()
            if not user_id:
                messagebox.showerror("Error", "User ID is required!")
                return
            
            # Email (optional)
            email = self.email_var.get().strip() or f"{name.lower().replace(' ', '.')}@example.com"
            
            # Determine user type
            if self.mode == 'librarian':
                user_type = "Librarian"
            else:
                user_type = self.user_type.get()
            
            # Create user based on type
            if user_type == "Regular User":
                # Check if ID exists
                if self.library.get_user(user_id):
                    messagebox.showerror("Error", f"User ID '{user_id}' already exists!")
                    return
                
                # Set membership level based on mode or default to Basic
                # You can add logic here to determine membership level if needed
                user = LibraryUser(name, email, user_id, membership_level="Basic")
                result = self.library.add_user(user)
            
            else:  # Librarian
                # Check if ID exists
                for lib in self.library.get_all_librarians():
                    if lib.employee_id == user_id:
                        messagebox.showerror("Error", f"Employee ID '{user_id}' already exists!")
                        return
                
                user = Librarian(name, email, user_id)
                result = self.library.add_librarian(user)
            
            # Set as current user if appropriate (only in user mode maybe)
            if self.mode == 'user':
                self.app.current_user = user
            
            # Update displays
            self.app.update_all_displays()
            
            messagebox.showinfo("Success", result)
            self.result = True
            self.on_close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")