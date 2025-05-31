"""
File Manager
Handles loading and managing different file formats
"""
import os
from .readers import EpubReader, PdfReader, TextReader

class FileManager:
    """Manages file loading operations"""
    
    def __init__(self):
        """Initialize file manager"""
        self.readers = {
            '.epub': EpubReader(),
            '.pdf': PdfReader(),
            '.txt': TextReader()
        }
        self.supported_formats = list(self.readers.keys())
    
    def load_file(self, filepath):
        """Load a file and return its content"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Get file extension
        _, ext = os.path.splitext(filepath.lower())
        
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")
        
        # Use appropriate reader
        reader = self.readers[ext]
        return reader.read(filepath)
    
    def is_supported(self, filepath):
        """Check if file format is supported"""
        _, ext = os.path.splitext(filepath.lower())
        return ext in self.supported_formats
    
    def get_supported_formats(self):
        """Get list of supported file formats"""
        return self.supported_formats.copy()
