"""
Theme Definitions
Color schemes and styling for the application
"""

class Themes:
    """Theme definitions and management"""
    
    def __init__(self):
        """Initialize themes"""
        self.available_themes = ["light", "dark", "sepia"]
        
        self.light_theme = {
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8F9FA',
            'bg_tertiary': '#E9ECEF',
            'text_primary': '#212529',
            'text_secondary': '#6C757D',
            'text_muted': '#ADB5BD',
            'accent': '#0D6EFD',
            'accent_hover': '#0B5ED7',
            'success': '#198754',
            'warning': '#FFC107',
            'danger': '#DC3545',
            'highlight': '#FFF3CD',
            'highlight_border': '#FFEAA7',
            'selection': '#B3D4FC',
            'border': '#DEE2E6',
            'shadow': 'rgba(0,0,0,0.1)'
        }
        
        self.dark_theme = {
            'bg_primary': '#1E1E1E',
            'bg_secondary': '#2D2D30',
            'bg_tertiary': '#3C3C3C',
            'text_primary': '#F0F0F0',
            'text_secondary': '#CCCCCC',
            'text_muted': '#808080',
            'accent': '#0078D4',
            'accent_hover': '#106EBE',
            'success': '#16A085',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'highlight': '#3C3C3C',
            'highlight_border': '#5A5A5A',
            'selection': '#264F78',
            'border': '#484848',
            'shadow': 'rgba(0,0,0,0.3)'
        }
        
        self.sepia_theme = {
            'bg_primary': '#F4F1E8',
            'bg_secondary': '#EDE7D3',
            'bg_tertiary': '#E6DCC6',
            'text_primary': '#2C1810',
            'text_secondary': '#5D4E37',
            'text_muted': '#8B7355',
            'accent': '#8B4513',
            'accent_hover': '#A0522D',
            'success': '#228B22',
            'warning': '#DAA520',
            'danger': '#B22222',
            'highlight': '#FFFACD',
            'highlight_border': '#DEB887',
            'selection': '#D2B48C',
            'border': '#D2B48C',
            'shadow': 'rgba(139,69,19,0.1)'
        }
    
    def get_theme(self, theme_name):
        """Get theme data by name"""
        if theme_name == "light":
            return self.light_theme
        elif theme_name == "dark":
            return self.dark_theme
        elif theme_name == "sepia":
            return self.sepia_theme
        else:
            return self.light_theme
    
    def get_reading_font_config(self, theme_name):
        """Get font configuration optimized for reading"""
        base_config = {
            'family': 'Georgia',
            'size': 14,
            'weight': 'normal'
        }
        
        if theme_name == "sepia":
            base_config['family'] = 'Times New Roman'
        elif theme_name == "dark":
            base_config['size'] = 15  # Slightly larger for dark theme
        
        return base_config
