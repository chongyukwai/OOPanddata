#!/usr/bin/env python3
"""
Library Management System - Main Entry Point
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import LibraryGUI


def main():
    """Main entry point for the application"""
    try:
        print("=" * 60)
        print("📚 Library Management System Starting...")
        print("=" * 60)
        
        app = LibraryGUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Application terminated by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()