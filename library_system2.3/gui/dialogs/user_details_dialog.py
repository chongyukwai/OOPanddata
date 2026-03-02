"""
User Details Dialog - View and manage user details
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from config.styles import Colors, Fonts


class UserDetailsDialog:
    """Dialog for viewing and managing user details"""
    
    def __init__(self, app, user_id):
        self.app = app
        self.user_id = user_id
        self.user = app.library.get_user(user_id)
        
        if not self.user:
            messagebox.showerror("Error", f"User with ID {user_id} not found!")
            return
        
        self.window = tk.Toplevel(app.root)
        self.window.title(f"User Details - {self.user.name}")
        self.window.geometry("600x500")
        self.window.configure(bg=Colors.BACKGROUND)
        self.window.transient(app.root)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.center_window()
        self.create_widgets()
    
    def on_close(self):
        """Handle window close event"""
        try:
            self.window.destroy()
        except:
            pass  # Window might already be destroyed
    
    def center_window(self):
        """Center window on parent"""
        try:
            self.window.update_idletasks()
            x = self.app.root.winfo_x() + (self.app.root.winfo_width() // 2) - (self.window.winfo_width() // 2)
            y = self.app.root.winfo_y() + (self.app.root.winfo_height() // 2) - (self.window.winfo_height() // 2)
            self.window.geometry(f"+{x}+{y}")
        except:
            pass  # Window might be closed during centering
    
    def create_widgets(self):
        """Create dialog widgets"""
        try:
            main_frame = tk.Frame(self.window, bg=Colors.BACKGROUND, padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Title
            tk.Label(main_frame, text=f"User Details: {self.user.name}",
                    font=Fonts.HEADER,
                    bg=Colors.BACKGROUND,
                    fg=Colors.PRIMARY).pack(pady=(0, 20))
            
            # User info frame
            info_frame = tk.LabelFrame(main_frame, text="User Information",
                                      font=Fonts.SUBHEADER,
                                      bg=Colors.BACKGROUND,
                                      fg=Colors.PRIMARY,
                                      padx=15, pady=15)
            info_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Create info grid
            info_grid = tk.Frame(info_frame, bg=Colors.BACKGROUND)
            info_grid.pack(fill=tk.X)
            
            # User ID
            tk.Label(info_grid, text="User ID:",
                    font=Fonts.BODY_BOLD,
                    bg=Colors.BACKGROUND).grid(row=0, column=0, sticky=tk.W, pady=2)
            tk.Label(info_grid, text=self.user.user_id if hasattr(self.user, 'user_id') else self.user.employee_id,
                    font=Fonts.BODY,
                    bg=Colors.BACKGROUND).grid(row=0, column=1, sticky=tk.W, pady=2, padx=(10, 0))
            
            # Name
            tk.Label(info_grid, text="Name:",
                    font=Fonts.BODY_BOLD,
                    bg=Colors.BACKGROUND).grid(row=1, column=0, sticky=tk.W, pady=2)
            tk.Label(info_grid, text=self.user.name,
                    font=Fonts.BODY,
                    bg=Colors.BACKGROUND).grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
            
            # Email
            tk.Label(info_grid, text="Email:",
                    font=Fonts.BODY_BOLD,
                    bg=Colors.BACKGROUND).grid(row=2, column=0, sticky=tk.W, pady=2)
            tk.Label(info_grid, text=self.user.email,
                    font=Fonts.BODY,
                    bg=Colors.BACKGROUND).grid(row=2, column=1, sticky=tk.W, pady=2, padx=(10, 0))
            
            # Membership (if applicable)
            if hasattr(self.user, 'membership_level'):
                tk.Label(info_grid, text="Membership:",
                        font=Fonts.BODY_BOLD,
                        bg=Colors.BACKGROUND).grid(row=3, column=0, sticky=tk.W, pady=2)
                tk.Label(info_grid, text=self.user.membership_level,
                        font=Fonts.BODY,
                        bg=Colors.BACKGROUND).grid(row=3, column=1, sticky=tk.W, pady=2, padx=(10, 0))
            
            # Fines
            tk.Label(info_grid, text="Fines Owed:",
                    font=Fonts.BODY_BOLD,
                    bg=Colors.BACKGROUND).grid(row=4, column=0, sticky=tk.W, pady=2)
            tk.Label(info_grid, text=f"${self.user.fines_owed:.2f}",
                    font=Fonts.BODY,
                    bg=Colors.BACKGROUND,
                    fg=Colors.DANGER if self.user.fines_owed > 0 else Colors.SUCCESS).grid(row=4, column=1, sticky=tk.W, pady=2, padx=(10, 0))
            
            # Borrowed items frame
            items_frame = tk.LabelFrame(main_frame, text="Borrowed Items",
                                       font=Fonts.SUBHEADER,
                                       bg=Colors.BACKGROUND,
                                       fg=Colors.PRIMARY,
                                       padx=15, pady=15)
            items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            # Create Treeview for borrowed items
            columns = ('ID', 'Title', 'Due Date', 'Status')
            self.items_tree = ttk.Treeview(items_frame, columns=columns, 
                                          show='headings', height=8)
            
            # Define headings
            self.items_tree.heading('ID', text='Item ID')
            self.items_tree.heading('Title', text='Title')
            self.items_tree.heading('Due Date', text='Due Date')
            self.items_tree.heading('Status', text='Status')
            
            # Set column widths
            self.items_tree.column('ID', width=80)
            self.items_tree.column('Title', width=200)
            self.items_tree.column('Due Date', width=100)
            self.items_tree.column('Status', width=100)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL,
                                     command=self.items_tree.yview)
            self.items_tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate borrowed items
            self.populate_borrowed_items()
            
            # Close button
            button_frame = tk.Frame(main_frame, bg=Colors.BACKGROUND)
            button_frame.pack(pady=10)
            
            ttk.Button(button_frame, text="Close",
                      command=self.on_close,
                      style='Primary.TButton').pack()
                      
        except Exception as e:
            # If there's an error creating widgets, close the window
            print(f"Error creating user details dialog: {e}")
            self.on_close()
            messagebox.showerror("Error", f"Failed to create user details dialog: {e}")
    
    def populate_borrowed_items(self):
        """Populate borrowed items list"""
        try:
            now = datetime.now()
            
            for item in self.user.borrowed_items:
                due_date = item.due_date.strftime('%Y-%m-%d') if item.due_date else 'Unknown'
                
                # Check if overdue
                if hasattr(item, 'is_overdue') and item.is_overdue:
                    status = f"⚠️ OVERDUE ({item.days_overdue} days)"
                    tags = ('overdue',)
                else:
                    status = "Borrowed"
                    tags = ('borrowed',)
                
                self.items_tree.insert('', tk.END,
                                      values=(item.item_id, item.title, due_date, status),
                                      tags=tags)
            
            # Configure tag colors
            self.items_tree.tag_configure('overdue', foreground='red')
            self.items_tree.tag_configure('borrowed', foreground='blue')
        except:
            pass  # Silently fail if tree doesn't exist