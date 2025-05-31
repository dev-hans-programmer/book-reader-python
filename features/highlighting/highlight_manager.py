"""
Highlight Manager
Manages text highlighting functionality
"""
import uuid
from datetime import datetime

class HighlightManager:
    """Manages text highlights"""
    
    def __init__(self, storage):
        """Initialize highlight manager"""
        self.storage = storage
        self.highlights = {}  # {highlight_id: highlight_data}
        self.text_viewer = None
    
    def set_text_viewer(self, text_viewer):
        """Set the text viewer reference"""
        self.text_viewer = text_viewer
    
    def add_highlight(self, start_index, end_index, text, color="yellow"):
        """Add a new highlight"""
        highlight_id = str(uuid.uuid4())
        
        highlight_data = {
            'id': highlight_id,
            'start_index': start_index,
            'end_index': end_index,
            'text': text,
            'color': color,
            'created_at': datetime.now().isoformat(),
            'notes': []
        }
        
        self.highlights[highlight_id] = highlight_data
        
        # Apply highlight to text viewer if available
        if self.text_viewer:
            self.text_viewer.highlight_text(start_index, end_index, highlight_id)
        
        return highlight_id
    
    def remove_highlight(self, highlight_id):
        """Remove a highlight"""
        if highlight_id in self.highlights:
            # Remove from text viewer if available
            if self.text_viewer:
                self.text_viewer.remove_highlight(highlight_id)
            
            del self.highlights[highlight_id]
            return True
        return False
    
    def get_highlight(self, highlight_id):
        """Get highlight data by ID"""
        return self.highlights.get(highlight_id)
    
    def get_highlights(self):
        """Get all highlights"""
        return list(self.highlights.values())
    
    def load_highlights(self, highlights_data):
        """Load highlights from saved data"""
        self.highlights = {}
        for highlight in highlights_data:
            self.highlights[highlight['id']] = highlight
            
            # Apply to text viewer if available
            if self.text_viewer:
                self.text_viewer.highlight_text(
                    highlight['start_index'],
                    highlight['end_index'],
                    highlight['id']
                )
    
    def search_highlights(self, query):
        """Search highlights by text content"""
        results = []
        query_lower = query.lower()
        
        for highlight in self.highlights.values():
            if query_lower in highlight['text'].lower():
                results.append(highlight)
        
        return results
    
    def get_highlights_by_position(self, start_pos, end_pos):
        """Get highlights within a specific text range"""
        results = []
        
        for highlight in self.highlights.values():
            # Simple overlap check
            h_start = float(highlight['start_index'].split('.')[0])
            h_end = float(highlight['end_index'].split('.')[0])
            
            if (h_start <= end_pos and h_end >= start_pos):
                results.append(highlight)
        
        return results
    
    def update_highlight_color(self, highlight_id, color):
        """Update highlight color"""
        if highlight_id in self.highlights:
            self.highlights[highlight_id]['color'] = color
            
            # Update in text viewer if available
            if self.text_viewer:
                # Remove old highlight and add new one with new color
                highlight = self.highlights[highlight_id]
                self.text_viewer.remove_highlight(highlight_id)
                self.text_viewer.highlight_text(
                    highlight['start_index'],
                    highlight['end_index'],
                    highlight_id
                )
            
            return True
        return False
