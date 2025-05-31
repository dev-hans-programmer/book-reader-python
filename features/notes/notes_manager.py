"""
Notes Manager
Manages margin notes and annotations
"""
import uuid
from datetime import datetime

class NotesManager:
    """Manages text notes and annotations"""
    
    def __init__(self, storage):
        """Initialize notes manager"""
        self.storage = storage
        self.notes = {}  # {note_id: note_data}
        self.text_viewer = None
    
    def set_text_viewer(self, text_viewer):
        """Set the text viewer reference"""
        self.text_viewer = text_viewer
    
    def add_note(self, position, text, note_type="margin"):
        """Add a new note"""
        note_id = str(uuid.uuid4())
        
        note_data = {
            'id': note_id,
            'position': position,
            'text': text,
            'type': note_type,  # margin, inline, popup
            'created_at': datetime.now().isoformat(),
            'modified_at': datetime.now().isoformat()
        }
        
        self.notes[note_id] = note_data
        return note_id
    
    def add_note_to_highlight(self, highlight_id, note_text):
        """Add a note to an existing highlight"""
        note_id = str(uuid.uuid4())
        
        note_data = {
            'id': note_id,
            'highlight_id': highlight_id,
            'text': note_text,
            'type': 'highlight_note',
            'created_at': datetime.now().isoformat(),
            'modified_at': datetime.now().isoformat()
        }
        
        self.notes[note_id] = note_data
        return note_id
    
    def update_note(self, note_id, new_text):
        """Update an existing note"""
        if note_id in self.notes:
            self.notes[note_id]['text'] = new_text
            self.notes[note_id]['modified_at'] = datetime.now().isoformat()
            return True
        return False
    
    def remove_note(self, note_id):
        """Remove a note"""
        if note_id in self.notes:
            del self.notes[note_id]
            return True
        return False
    
    def get_note(self, note_id):
        """Get note data by ID"""
        return self.notes.get(note_id)
    
    def get_notes(self):
        """Get all notes"""
        return list(self.notes.values())
    
    def get_notes_for_highlight(self, highlight_id):
        """Get all notes associated with a highlight"""
        notes = []
        for note in self.notes.values():
            if note.get('highlight_id') == highlight_id:
                notes.append(note)
        return notes
    
    def load_notes(self, notes_data):
        """Load notes from saved data"""
        self.notes = {}
        for note in notes_data:
            self.notes[note['id']] = note
    
    def search_notes(self, query):
        """Search notes by text content"""
        results = []
        query_lower = query.lower()
        
        for note in self.notes.values():
            if query_lower in note['text'].lower():
                results.append(note)
        
        return results
    
    def get_notes_by_position(self, start_pos, end_pos):
        """Get notes within a specific text range"""
        results = []
        
        for note in self.notes.values():
            if 'position' in note:
                # Extract line number from position
                try:
                    note_line = float(note['position'].split('.')[0])
                    if start_pos <= note_line <= end_pos:
                        results.append(note)
                except (ValueError, IndexError):
                    continue
        
        return results
    
    def export_notes(self, format_type="text"):
        """Export notes in various formats"""
        if format_type == "text":
            return self._export_as_text()
        elif format_type == "json":
            return self._export_as_json()
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def _export_as_text(self):
        """Export notes as plain text"""
        output = []
        output.append("=== NOTES EXPORT ===\n")
        
        for note in sorted(self.notes.values(), key=lambda x: x['created_at']):
            output.append(f"Note ID: {note['id']}")
            output.append(f"Created: {note['created_at']}")
            output.append(f"Type: {note['type']}")
            if 'position' in note:
                output.append(f"Position: {note['position']}")
            output.append(f"Text: {note['text']}")
            output.append("-" * 40)
        
        return "\n".join(output)
    
    def _export_as_json(self):
        """Export notes as JSON"""
        import json
        return json.dumps(list(self.notes.values()), indent=2)
