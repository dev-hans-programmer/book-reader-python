"""
Theme Manager
Handles application theming and appearance
"""
import customtkinter as ctk
from .themes import Themes

class ThemeManager:
    """Manages application themes"""
    
    def __init__(self, root):
        """Initialize theme manager"""
        self.root = root
        self.themes = Themes()
        self.current_theme = "light"
        self.themed_widgets = []
    
    def apply_theme(self, theme_name):
        """Apply a theme to the application"""
        if theme_name not in self.themes.available_themes:
            raise ValueError(f"Theme '{theme_name}' not available")
        
        self.current_theme = theme_name
        theme = self.themes.get_theme(theme_name)
        
        # Set CustomTkinter appearance mode
        ctk.set_appearance_mode(theme_name)
        
        # Update themed widgets
        for widget_data in self.themed_widgets:
            widget = widget_data['widget']
            widget_type = widget_data['type']
            
            if hasattr(widget, 'configure'):
                self.apply_widget_theme(widget, widget_type, theme)
    
    def apply_widget_theme(self, widget, widget_type, theme):
        """Apply theme to a specific widget"""
        if widget_type == "text":
            widget.configure(
                bg=theme['bg_primary'],
                fg=theme['text_primary'],
                selectbackground=theme['highlight'],
                insertbackground=theme['text_primary']
            )
        elif widget_type == "frame":
            widget.configure(fg_color=theme['bg_secondary'])
        elif widget_type == "button":
            widget.configure(
                fg_color=theme['accent'],
                text_color=theme['bg_primary']
            )
        elif widget_type == "label":
            widget.configure(
                text_color=theme['text_primary'],
                fg_color="transparent"
            )
    
    def register_widget(self, widget, widget_type):
        """Register a widget for theming"""
        self.themed_widgets.append({
            'widget': widget,
            'type': widget_type
        })
        
        # Apply current theme to the widget
        theme = self.themes.get_theme(self.current_theme)
        self.apply_widget_theme(widget, widget_type, theme)
    
    def get_current_theme(self):
        """Get current theme data"""
        return self.themes.get_theme(self.current_theme)
    
    def get_color(self, color_name):
        """Get a specific color from current theme"""
        theme = self.get_current_theme()
        return theme.get(color_name, "#000000")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)
        return new_theme
