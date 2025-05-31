"""
Bookmark Manager
Manages bookmarks and reading positions
"""
import uuid
from datetime import datetime

class BookmarkManager:
    """Manages bookmarks and reading progress"""
    
    def __init__(self, storage):
        """Initialize bookmark manager"""
        self.storage = storage
        self.bookmarks = {}  # {bookmark_id: bookmark_data}
        self.current_position = "1.0"
        self.reading_progress = 0.0  # Percentage of book read
    
    def add_bookmark(self, position, title=None, note=None):
        """Add a new bookmark"""
        bookmark_id = str(uuid.uuid4())
        
        if not title:
            title = f"Bookmark at {position}"
        
        bookmark_data = {
            'id': bookmark_id,
            'position': position,
            'title': title,
            'note': note,
            'created_at': datetime.now().isoformat()
        }
        
        self.bookmarks[bookmark_id] = bookmark_data
        return bookmark_id
    
    def remove_bookmark(self, bookmark_id):
        """Remove a bookmark"""
        if bookmark_id in self.bookmarks:
            del self.bookmarks[bookmark_id]
            return True
        return False
    
    def get_bookmark(self, bookmark_id):
        """Get bookmark data by ID"""
        return self.bookmarks.get(bookmark_id)
    
    def get_bookmarks(self):
        """Get all bookmarks sorted by position"""
        bookmarks = list(self.bookmarks.values())
        return sorted(bookmarks, key=lambda x: self._position_to_float(x['position']))
    
    def update_bookmark(self, bookmark_id, title=None, note=None):
        """Update bookmark title or note"""
        if bookmark_id in self.bookmarks:
            if title is not None:
                self.bookmarks[bookmark_id]['title'] = title
            if note is not None:
                self.bookmarks[bookmark_id]['note'] = note
            return True
        return False
    
    def load_bookmarks(self, bookmarks_data):
        """Load bookmarks from saved data"""
        self.bookmarks = {}
        for bookmark in bookmarks_data:
            self.bookmarks[bookmark['id']] = bookmark
    
    def set_current_position(self, position):
        """Update current reading position"""
        self.current_position = position
    
    def get_current_position(self):
        """Get current reading position"""
        return self.current_position
    
    def update_reading_progress(self, current_line, total_lines):
        """Update reading progress percentage"""
        if total_lines > 0:
            self.reading_progress = min(100.0, (current_line / total_lines) * 100)
        else:
            self.reading_progress = 0.0
    
    def get_reading_progress(self):
        """Get reading progress percentage"""
        return self.reading_progress
    
    def find_nearest_bookmark(self, position):
        """Find the bookmark closest to the given position"""
        if not self.bookmarks:
            return None
        
        current_pos = self._position_to_float(position)
        nearest_bookmark = None
        min_distance = float('inf')
        
        for bookmark in self.bookmarks.values():
            bookmark_pos = self._position_to_float(bookmark['position'])
            distance = abs(current_pos - bookmark_pos)
            
            if distance < min_distance:
                min_distance = distance
                nearest_bookmark = bookmark
        
        return nearest_bookmark
    
    def get_bookmarks_in_range(self, start_pos, end_pos):
        """Get bookmarks within a specific range"""
        start_float = self._position_to_float(start_pos)
        end_float = self._position_to_float(end_pos)
        
        results = []
        for bookmark in self.bookmarks.values():
            bookmark_pos = self._position_to_float(bookmark['position'])
            if start_float <= bookmark_pos <= end_float:
                results.append(bookmark)
        
        return sorted(results, key=lambda x: self._position_to_float(x['position']))
    
    def _position_to_float(self, position):
        """Convert text position to float for comparison"""
        try:
            parts = position.split('.')
            line = int(parts[0])
            char = int(parts[1]) if len(parts) > 1 else 0
            return line + (char / 1000.0)  # Simple conversion for sorting
        except (ValueError, IndexError):
            return 0.0
    
    def export_bookmarks(self):
        """Export bookmarks as text"""
        output = []
        output.append("=== BOOKMARKS EXPORT ===\n")
        
        for bookmark in self.get_bookmarks():
            output.append(f"Title: {bookmark['title']}")
            output.append(f"Position: {bookmark['position']}")
            output.append(f"Created: {bookmark['created_at']}")
            if bookmark.get('note'):
                output.append(f"Note: {bookmark['note']}")
            output.append("-" * 40)
        
        return "\n".join(output)
