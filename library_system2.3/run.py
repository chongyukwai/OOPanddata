"""
Run script for Library Management System
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the LibraryGUI class from main
from main import main

if __name__ == "__main__":
    # Create and run the application
    main()