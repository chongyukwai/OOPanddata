"""
Style configuration for the GUI
"""


class Colors:
    """Color scheme for the application"""
    
    # Primary colors
    PRIMARY = '#2c3e50'
    SECONDARY = '#34495e'
    ACCENT = '#3498db'
    
    # Status colors
    SUCCESS = '#27ae60'
    WARNING = '#f39c12'
    DANGER = '#e74c3c'
    ERROR = '#e74c3c'  # Alias for DANGER
    INFO = '#3498db'
    
    # Neutral colors
    LIGHT = '#ecf0f1'
    DARK = '#2c3e50'
    BACKGROUND = '#f0f0f0'
    WHITE = '#ffffff'
    BLACK = '#000000'
    
    # Text colors
    TEXT_PRIMARY = '#2c3e50'
    TEXT_SECONDARY = '#7f8c8d'
    TEXT_LIGHT = '#ecf0f1'
    
    # Border colors
    BORDER = '#bdc3c7'
    BORDER_LIGHT = '#ecf0f1'
    BORDER_DARK = '#7f8c8d'


class Fonts:
    """Font configuration"""
    
    TITLE = ('Arial', 24, 'bold')
    HEADER = ('Arial', 16, 'bold')
    SUBHEADER = ('Arial', 14, 'bold')
    BODY = ('Arial', 11)
    BODY_SMALL = ('Arial', 9)
    BODY_BOLD = ('Arial', 11, 'bold')
    
    # For buttons
    BUTTON = ('Arial', 10, 'bold')
    BUTTON_SMALL = ('Arial', 9)


class Styles:
    """Style configuration for ttk widgets"""
    
    @staticmethod
    def configure(style):
        """Configure ttk styles"""
        
        # Title style
        style.configure('Title.TLabel', font=Fonts.TITLE, foreground=Colors.PRIMARY)
        
        # Header styles
        style.configure('Header.TLabel', font=Fonts.HEADER, foreground=Colors.SECONDARY)
        style.configure('Subheader.TLabel', font=Fonts.SUBHEADER, foreground=Colors.SECONDARY)
        
        # Status styles
        style.configure('Success.TLabel', foreground=Colors.SUCCESS)
        style.configure('Warning.TLabel', foreground=Colors.WARNING)
        style.configure('Danger.TLabel', foreground=Colors.DANGER)
        style.configure('Error.TLabel', foreground=Colors.ERROR)
        style.configure('Info.TLabel', foreground=Colors.INFO)
        
        # Button styles
        style.configure('Primary.TButton', 
                       font=Fonts.BUTTON,
                       background=Colors.ACCENT,
                       foreground=Colors.WHITE)
        style.map('Primary.TButton',
                 background=[('active', Colors.PRIMARY)],
                 foreground=[('active', Colors.WHITE)])
        
        style.configure('Secondary.TButton',
                       font=Fonts.BUTTON,
                       background=Colors.LIGHT,
                       foreground=Colors.DARK)
        style.map('Secondary.TButton',
                 background=[('active', Colors.BORDER)],
                 foreground=[('active', Colors.DARK)])
        
        style.configure('Success.TButton',
                       font=Fonts.BUTTON,
                       background=Colors.SUCCESS,
                       foreground=Colors.WHITE)
        
        style.configure('Danger.TButton',
                       font=Fonts.BUTTON,
                       background=Colors.DANGER,
                       foreground=Colors.WHITE)
        
        # Treeview styles
        style.configure('Treeview', 
                       background=Colors.WHITE,
                       foreground=Colors.TEXT_PRIMARY,
                       rowheight=25,
                       fieldbackground=Colors.WHITE)
        style.map('Treeview',
                 background=[('selected', Colors.ACCENT)],
                 foreground=[('selected', Colors.WHITE)])
        
        style.configure('Treeview.Heading',
                       font=Fonts.BODY_BOLD,
                       background=Colors.LIGHT,
                       foreground=Colors.TEXT_PRIMARY)
        
        # Frame styles
        style.configure('Card.TFrame', 
                       background=Colors.WHITE,
                       relief='solid',
                       borderwidth=1)
        
        # LabelFrame styles
        style.configure('Card.TLabelframe',
                       background=Colors.WHITE,
                       relief='solid',
                       borderwidth=1)
        style.configure('Card.TLabelframe.Label',
                       font=Fonts.SUBHEADER,
                       foreground=Colors.PRIMARY,
                       background=Colors.WHITE)