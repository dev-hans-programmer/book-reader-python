"""
Data Storage
Handles persistence of highlights, notes, bookmarks, and settings
"""
import os
import json
from datetime import datetime
from utils.helpers import safe_json_load, safe_json_save, get_file_hash

class DataStorage:
    """Handles data persistence for the application"""
    
    def __init__(self):
        """Initialize data storage"""
        # Create data directory
        self.data_dir = os.path.join(os.path.expanduser("~"), ".book_reader")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # File paths
        self.highlights_file = os.path.join(self.data_dir, "highlights.json")
        self.notes_file = os.path.join(self.data_dir, "notes.json")
        self.bookmarks_file = os.path.join(self.data_dir, "bookmarks.json")
        self.settings_file = os.path.join(self.data_dir, "settings.json")
        self.library_file = os.path.join(self.data_dir, "library.json")
        
        # Initialize data structures
        self.highlights_data = safe_json_load(self.highlights_file, {})
        self.notes_data = safe_json_load(self.notes_file, {})
        self.bookmarks_data = safe_json_load(self.bookmarks_file, {})
        self.settings_data = safe_json_load(self.settings_file, {})
        self.library_data = safe_json_load(self.library_file, {})
    
    def get_book_id(self, filepath):
        """Generate a unique identifier for a book"""
        # Use a combination of filename and file hash for uniqueness
        filename = os.path.basename(filepath)
        file_hash = get_file_hash(filepath)
        return f"{filename}_{file_hash[:8]}"
    
    # Highlights management
    def save_highlights(self, book_id, highlights):
        """Save highlights for a book"""
        self.highlights_data[book_id] = highlights
        return safe_json_save(self.highlights_file, self.highlights_data)
    
    def load_highlights(self, book_id):
        """Load highlights for a book"""
        return self.highlights_data.get(book_id, [])
    
    def delete_highlights(self, book_id):
        """Delete all highlights for a book"""
        if book_id in self.highlights_data:
            del self.highlights_data[book_id]
            return safe_json_save(self.highlights_file, self.highlights_data)
        return True
    
    # Notes management
    def save_notes(self, book_id, notes):
        """Save notes for a book"""
        self.notes_data[book_id] = notes
        return safe_json_save(self.notes_file, self.notes_data)
    
    def load_notes(self, book_id):
        """Load notes for a book"""
        return self.notes_data.get(book_id, [])
    
    def delete_notes(self, book_id):
        """Delete all notes for a book"""
        if book_id in self.notes_data:
            del self.notes_data[book_id]
            return safe_json_save(self.notes_file, self.notes_data)
        return True
    
    # Bookmarks management
    def save_bookmarks(self, book_id, bookmarks):
        """Save bookmarks for a book"""
        self.bookmarks_data[book_id] = bookmarks
        return safe_json_save(self.bookmarks_file, self.bookmarks_data)
    
    def load_bookmarks(self, book_id):
        """Load bookmarks for a book"""
        return self.bookmarks_data.get(book_id, [])
    
    def delete_bookmarks(self, book_id):
        """Delete all bookmarks for a book"""
        if book_id in self.bookmarks_data:
            del self.bookmarks_data[book_id]
            return safe_json_save(self.bookmarks_file, self.bookmarks_data)
        return True
    
    # Settings management
    def save_settings(self, settings):
        """Save application settings"""
        self.settings_data.update(settings)
        self.settings_data['last_updated'] = datetime.now().isoformat()
        return safe_json_save(self.settings_file, self.settings_data)
    
    def load_settings(self):
        """Load application settings"""
        return self.settings_data.copy()
    
    def get_setting(self, key, default=None):
        """Get a specific setting value"""
        return self.settings_data.get(key, default)
    
    def set_setting(self, key, value):
        """Set a specific setting value"""
        self.settings_data[key] = value
        return self.save_settings({})
    
    # Library management
    def add_book_to_library(self, filepath, metadata=None):
        """Add a book to the library"""
        book_id = self.get_book_id(filepath)
        
        book_info = {
            'id': book_id,
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'added_at': datetime.now().isoformat(),
            'last_opened': None,
            'reading_position': '1.0',
            'reading_progress': 0.0,
            'metadata': metadata or {}
        }
        
        self.library_data[book_id] = book_info
        return safe_json_save(self.library_file, self.library_data)
    
    def update_book_progress(self, book_id, position, progress):
        """Update reading progress for a book"""
        if book_id in self.library_data:
            self.library_data[book_id]['reading_position'] = position
            self.library_data[book_id]['reading_progress'] = progress
            self.library_data[book_id]['last_opened'] = datetime.now().isoformat()
            return safe_json_save(self.library_file, self.library_data)
        return False
    
    def get_library(self):
        """Get all books in the library"""
        return list(self.library_data.values())
    
    def get_book_info(self, book_id):
        """Get information about a specific book"""
        return self.library_data.get(book_id)
    
    def remove_book_from_library(self, book_id):
        """Remove a book from the library and all associated data"""
        # Remove from library
        if book_id in self.library_data:
            del self.library_data[book_id]
            safe_json_save(self.library_file, self.library_data)
        
        # Remove associated data
        self.delete_highlights(book_id)
        self.delete_notes(book_id)
        self.delete_bookmarks(book_id)
        
        return True
    
    # Data export/import
    def export_book_data(self, book_id):
        """Export all data for a specific book"""
        book_info = self.get_book_info(book_id)
        highlights = self.load_highlights(book_id)
        notes = self.load_notes(book_id)
        bookmarks = self.load_bookmarks(book_id)
        
        export_data = {
            'book_info': book_info,
            'highlights': highlights,
            'notes': notes,
            'bookmarks': bookmarks,
            'exported_at': datetime.now().isoformat(),
            'export_version': '1.0'
        }
        
        return export_data
    
    def import_book_data(self, book_id, import_data):
        """Import data for a specific book"""
        try:
            if 'highlights' in import_data:
                self.save_highlights(book_id, import_data['highlights'])
            
            if 'notes' in import_data:
                self.save_notes(book_id, import_data['notes'])
            
            if 'bookmarks' in import_data:
                self.save_bookmarks(book_id, import_data['bookmarks'])
            
            if 'book_info' in import_data:
                self.library_data[book_id] = import_data['book_info']
                safe_json_save(self.library_file, self.library_data)
            
            return True
        except Exception as e:
            print(f"Error importing book data: {e}")
            return False
    
    # Data maintenance
    def cleanup_orphaned_data(self):
        """Remove data for books that no longer exist"""
        valid_book_ids = set(self.library_data.keys())
        
        # Clean highlights
        orphaned_highlights = set(self.highlights_data.keys()) - valid_book_ids
        for book_id in orphaned_highlights:
            del self.highlights_data[book_id]
        
        # Clean notes
        orphaned_notes = set(self.notes_data.keys()) - valid_book_ids
        for book_id in orphaned_notes:
            del self.notes_data[book_id]
        
        # Clean bookmarks
        orphaned_bookmarks = set(self.bookmarks_data.keys()) - valid_book_ids
        for book_id in orphaned_bookmarks:
            del self.bookmarks_data[book_id]
        
        # Save cleaned data
        safe_json_save(self.highlights_file, self.highlights_data)
        safe_json_save(self.notes_file, self.notes_data)
        safe_json_save(self.bookmarks_file, self.bookmarks_data)
        
        return len(orphaned_highlights) + len(orphaned_notes) + len(orphaned_bookmarks)
    
    def get_data_stats(self):
        """Get statistics about stored data"""
        stats = {
            'total_books': len(self.library_data),
            'total_highlights': sum(len(highlights) for highlights in self.highlights_data.values()),
            'total_notes': sum(len(notes) for notes in self.notes_data.values()),
            'total_bookmarks': sum(len(bookmarks) for bookmarks in self.bookmarks_data.values()),
            'data_dir_size': self._get_directory_size(self.data_dir)
        }
        return stats
    
    def _get_directory_size(self, directory):
        """Calculate total size of directory in bytes"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except Exception:
            pass
        return total_size
