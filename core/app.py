"""
Core Application Class
Main application window and coordination
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

from features.theming.theme_manager import ThemeManager
from features.file_loader.file_manager import FileManager
from features.text_display.text_viewer import TextViewer
from features.highlighting.highlight_manager import HighlightManager
from features.notes.notes_manager import NotesManager
from features.bookmarks.bookmark_manager import BookmarkManager
from ui.components.sidebar import Sidebar
from ui.components.toolbar import Toolbar
from ui.components.reading_area import ReadingArea
from data.storage import DataStorage
from core.config import AppConfig

class BookReaderApp:
    """Main application class for the Book Reader"""
    
    def __init__(self):
        """Initialize the application"""
        # Set CustomTkinter appearance
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("Interactive Book Reader")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # Initialize configuration
        self.config = AppConfig()
        
        # Initialize data storage
        self.storage = DataStorage()
        
        # Initialize theme manager
        self.theme_manager = ThemeManager(self.root)
        
        # Initialize managers
        self.file_manager = FileManager()
        self.highlight_manager = HighlightManager(self.storage)
        self.notes_manager = NotesManager(self.storage)
        self.bookmark_manager = BookmarkManager(self.storage)
        
        # Current book state
        self.current_book = None
        self.current_book_path = None
        
        # Setup UI
        self.setup_ui()
        
        # Apply initial theme
        self.theme_manager.apply_theme("light")
        
        # Bind events
        self.bind_events()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Create toolbar
        self.toolbar = Toolbar(
            self.root, 
            self.theme_manager,
            self.open_file,
            self.toggle_theme,
            self.toggle_sidebar
        )
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 0))
        
        # Create sidebar
        self.sidebar = Sidebar(
            self.root,
            self.theme_manager,
            self.bookmark_manager,
            self.notes_manager
        )
        self.sidebar.grid(row=1, column=0, sticky="nsw", padx=(10, 5), pady=10)
        
        # Create reading area
        self.reading_area = ReadingArea(
            self.root,
            self.theme_manager,
            self.highlight_manager,
            self.notes_manager
        )
        self.reading_area.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        
        # Initialize text viewer
        self.text_viewer = TextViewer(
            self.reading_area.get_text_widget(),
            self.theme_manager
        )
    
    def bind_events(self):
        """Bind application events"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-q>", lambda e: self.on_closing())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("<Control-t>", lambda e: self.toggle_theme())
    
    def open_file(self):
        """Open a book file"""
        file_types = [
            ("All Supported", "*.epub;*.pdf;*.txt"),
            ("EPUB files", "*.epub"),
            ("PDF files", "*.pdf"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Open Book",
            filetypes=file_types
        )
        
        if filename:
            self.load_book(filename)
    
    def load_book(self, filepath):
        """Load a book from file"""
        try:
            # Load book content
            content = self.file_manager.load_file(filepath)
            
            if content:
                self.current_book_path = filepath
                self.current_book = content
                
                # Display content in text viewer
                self.text_viewer.display_content(content)
                
                # Update window title
                filename = os.path.basename(filepath)
                self.root.title(f"Interactive Book Reader - {filename}")
                
                # Load saved data for this book
                self.load_book_data(filepath)
                
                # Update UI
                self.reading_area.update_navigation(content)
                
                print(f"Successfully loaded: {filename}")
            else:
                messagebox.showerror("Error", "Failed to load the selected file")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {str(e)}")
    
    def load_book_data(self, filepath):
        """Load saved highlights, notes, and bookmarks for the book"""
        book_id = self.get_book_id(filepath)
        
        # Load highlights
        highlights = self.storage.load_highlights(book_id)
        self.highlight_manager.load_highlights(highlights)
        
        # Load notes
        notes = self.storage.load_notes(book_id)
        self.notes_manager.load_notes(notes)
        
        # Load bookmarks
        bookmarks = self.storage.load_bookmarks(book_id)
        self.bookmark_manager.load_bookmarks(bookmarks)
        
        # Update sidebar
        self.sidebar.update_content(bookmarks, notes)
    
    def get_book_id(self, filepath):
        """Generate a unique ID for the book"""
        return os.path.basename(filepath)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_theme = self.theme_manager.current_theme
        new_theme = "dark" if current_theme == "light" else "light"
        self.theme_manager.apply_theme(new_theme)
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        self.sidebar.toggle_visibility()
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def on_closing(self):
        """Handle application closing"""
        # Save current state
        if self.current_book_path:
            book_id = self.get_book_id(self.current_book_path)
            
            # Save highlights
            highlights = self.highlight_manager.get_highlights()
            self.storage.save_highlights(book_id, highlights)
            
            # Save notes
            notes = self.notes_manager.get_notes()
            self.storage.save_notes(book_id, notes)
            
            # Save bookmarks
            bookmarks = self.bookmark_manager.get_bookmarks()
            self.storage.save_bookmarks(book_id, bookmarks)
        
        # Save application settings
        self.storage.save_settings({
            'theme': self.theme_manager.current_theme,
            'window_geometry': self.root.geometry()
        })
        
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
