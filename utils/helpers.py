"""
Utility Helper Functions
Common utility functions used throughout the application
"""
import os
import hashlib
import re
from datetime import datetime
import json

def get_file_hash(filepath):
    """Generate a hash for a file to use as unique identifier"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        # Fallback to filename-based hash
        return hashlib.md5(os.path.basename(filepath).encode()).hexdigest()

def sanitize_filename(filename):
    """Sanitize filename for safe file operations"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    # Ensure it's not empty
    if not filename:
        filename = "untitled"
    return filename

def format_datetime(dt_string):
    """Format datetime string for display"""
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return dt_string

def truncate_text(text, max_length=100):
    """Truncate text to specified length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def extract_text_preview(text, position, context_length=50):
    """Extract text preview around a specific position"""
    try:
        # Convert position to character index
        lines = text.split('\n')
        line_num, char_num = map(int, position.split('.'))
        
        # Find the character position in the full text
        char_pos = sum(len(line) + 1 for line in lines[:line_num-1]) + char_num
        
        # Extract context around the position
        start = max(0, char_pos - context_length)
        end = min(len(text), char_pos + context_length)
        
        preview = text[start:end]
        
        # Add ellipsis if truncated
        if start > 0:
            preview = "..." + preview
        if end < len(text):
            preview = preview + "..."
            
        return preview
    except Exception:
        return text[:context_length] + "..." if len(text) > context_length else text

def safe_json_load(filepath, default=None):
    """Safely load JSON file with fallback"""
    if default is None:
        default = {}
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {filepath}: {e}")
    
    return default

def safe_json_save(filepath, data):
    """Safely save data to JSON file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write to temporary file first
        temp_filepath = filepath + '.tmp'
        with open(temp_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Replace original file
        os.replace(temp_filepath, filepath)
        return True
    except Exception as e:
        print(f"Error saving JSON to {filepath}: {e}")
        # Clean up temp file if it exists
        try:
            os.remove(temp_filepath)
        except:
            pass
        return False

def word_count(text):
    """Count words in text"""
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def estimate_reading_time(text, words_per_minute=200):
    """Estimate reading time in minutes"""
    word_count_value = word_count(text)
    minutes = word_count_value / words_per_minute
    return max(1, round(minutes))

def find_text_position(text, search_text, start_line=1):
    """Find the position of text within the document"""
    lines = text.split('\n')
    
    for line_num, line in enumerate(lines[start_line-1:], start_line):
        char_pos = line.find(search_text)
        if char_pos != -1:
            return f"{line_num}.{char_pos}"
    
    return None

def validate_position(position, text):
    """Validate that a position string is valid for the given text"""
    try:
        line_num, char_num = map(int, position.split('.'))
        lines = text.split('\n')
        
        if line_num < 1 or line_num > len(lines):
            return False
        
        line = lines[line_num - 1]
        if char_num < 0 or char_num > len(line):
            return False
        
        return True
    except Exception:
        return False

def create_backup(filepath):
    """Create a backup of a file"""
    if not os.path.exists(filepath):
        return False
    
    try:
        backup_path = filepath + '.backup'
        with open(filepath, 'rb') as src, open(backup_path, 'wb') as dst:
            dst.write(src.read())
        return True
    except Exception as e:
        print(f"Error creating backup of {filepath}: {e}")
        return False
