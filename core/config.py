"""
Application Configuration
Central configuration management
"""
import os

class AppConfig:
    """Application configuration class"""
    
    def __init__(self):
        """Initialize configuration"""
        # Application info
        self.APP_NAME = "Interactive Book Reader"
        self.APP_VERSION = "1.0.0"
        
        # File paths
        self.DATA_DIR = os.path.join(os.path.expanduser("~"), ".book_reader")
        self.HIGHLIGHTS_FILE = os.path.join(self.DATA_DIR, "highlights.json")
        self.NOTES_FILE = os.path.join(self.DATA_DIR, "notes.json")
        self.BOOKMARKS_FILE = os.path.join(self.DATA_DIR, "bookmarks.json")
        self.SETTINGS_FILE = os.path.join(self.DATA_DIR, "settings.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.DATA_DIR, exist_ok=True)
        
        # Reading settings
        self.DEFAULT_FONT_SIZE = 14
        self.DEFAULT_FONT_FAMILY = "Georgia"
        self.DEFAULT_LINE_SPACING = 1.3
        self.DEFAULT_MARGIN = 50
        
        # UI settings
        self.SIDEBAR_WIDTH = 300
        self.TOOLBAR_HEIGHT = 50
        
        # Supported file formats
        self.SUPPORTED_FORMATS = ['.epub', '.pdf', '.txt']
        
        # Color schemes
        self.LIGHT_THEME = {
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8F9FA',
            'text_primary': '#2C3E50',
            'text_secondary': '#6C757D',
            'accent': '#007BFF',
            'highlight': '#FFF3CD',
            'border': '#DEE2E6'
        }
        
        self.DARK_THEME = {
            'bg_primary': '#1A1D23',
            'bg_secondary': '#2C3E50',
            'text_primary': '#E9ECEF',
            'text_secondary': '#ADB5BD',
            'accent': '#0D6EFD',
            'highlight': '#3D4A5C',
            'border': '#495057'
        }
