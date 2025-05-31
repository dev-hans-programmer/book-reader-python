"""
Interactive Book Reader Application
Entry point for the application
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.app import BookReaderApp

def main():
    """Main entry point for the Book Reader application"""
    try:
        app = BookReaderApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
