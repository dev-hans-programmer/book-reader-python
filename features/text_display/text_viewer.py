"""
Text Viewer
Handles text display and formatting in the reading area
"""
import tkinter as tk
from tkinter import font
import re

class TextViewer:
    """Text display and formatting manager"""
    
    def __init__(self, text_widget, theme_manager):
        """Initialize text viewer"""
        self.text_widget = text_widget
        self.theme_manager = theme_manager
        self.current_content = None
        
        # Configure text widget
        self.setup_text_widget()
        
        # Font settings
        self.font_family = "Georgia"
        self.font_size = 16
        self.line_spacing = 1.6
        
        # Create tags for formatting
        self.create_text_tags()
    
    def setup_text_widget(self):
        """Configure the text widget"""
        # Register with theme manager
        self.theme_manager.register_widget(self.text_widget, "text")
        
        # Configure text widget properties
        self.text_widget.configure(
            wrap=tk.WORD,
            padx=60,
            pady=30,
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED,
            cursor="arrow",
            spacing1=4,
            spacing2=8,
            spacing3=12
        )
        
        # Remove default bindings that might interfere
        self.text_widget.bindtags((str(self.text_widget), str(self.text_widget.winfo_class()), ".", "all"))
    
    def create_text_tags(self):
        """Create text formatting tags"""
        # Create font objects
        self.update_fonts()
        
        # Configure tags
        self.text_widget.tag_configure("normal", font=self.normal_font, spacing1=3, spacing2=6, spacing3=10)
        self.text_widget.tag_configure("heading", font=self.heading_font, spacing1=20, spacing3=15, justify=tk.CENTER)
        self.text_widget.tag_configure("paragraph", spacing1=3, spacing2=6, spacing3=10)
        self.text_widget.tag_configure("highlight", background=self.theme_manager.get_color('highlight'))
        self.text_widget.tag_configure("selection", background=self.theme_manager.get_color('selection'))
        self.text_widget.tag_configure("center", justify=tk.CENTER)
    
    def update_fonts(self):
        """Update font objects based on current settings"""
        self.normal_font = font.Font(
            family=self.font_family,
            size=self.font_size
        )
        
        self.heading_font = font.Font(
            family=self.font_family,
            size=self.font_size + 4,
            weight="bold"
        )
        
        # Update line spacing
        self.text_widget.configure(spacing1=int(self.font_size * 0.2))
        self.text_widget.configure(spacing2=int(self.font_size * (self.line_spacing - 1)))
        self.text_widget.configure(spacing3=int(self.font_size * 0.2))
    
    def display_content(self, content_data):
        """Display content in the text widget"""
        self.current_content = content_data
        
        # Enable text widget for editing
        self.text_widget.configure(state=tk.NORMAL)
        
        # Clear existing content
        self.text_widget.delete("1.0", tk.END)
        
        # Insert title if available
        if content_data.get('title'):
            self.text_widget.insert(tk.END, content_data['title'], "heading center")
            self.text_widget.insert(tk.END, "\n\n")
        
        # Insert author if available
        if content_data.get('author'):
            self.text_widget.insert(tk.END, f"by {content_data['author']}", "center")
            self.text_widget.insert(tk.END, "\n\n" + "="*50 + "\n\n")
        
        # Insert content
        content = content_data.get('content', '')
        self.format_and_insert_text(content)
        
        # Disable text widget to prevent editing
        self.text_widget.configure(state=tk.DISABLED)
        
        # Scroll to top
        self.text_widget.see("1.0")
    
    def format_and_insert_text(self, text):
        """Format and insert text with proper styling"""
        # Clean up the text first - remove excessive whitespace but preserve paragraph breaks
        text = re.sub(r'\r\n', '\n', text)  # Normalize line endings
        text = re.sub(r'\r', '\n', text)    # Handle old Mac line endings
        
        # Split text into paragraphs (double newlines or more)
        paragraphs = re.split(r'\n\s*\n', text)
        
        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Replace single newlines with spaces within paragraphs
            paragraph = re.sub(r'\n+', ' ', paragraph)
            # Clean up multiple spaces
            paragraph = re.sub(r'\s+', ' ', paragraph)
            
            # Check if it looks like a heading
            if self.is_heading(paragraph):
                self.text_widget.insert(tk.END, paragraph, "heading")
                self.text_widget.insert(tk.END, "\n\n")
            else:
                # Insert as normal paragraph
                self.text_widget.insert(tk.END, paragraph, "normal paragraph")
                # Add paragraph spacing except for the last paragraph
                if i < len(paragraphs) - 1:
                    self.text_widget.insert(tk.END, "\n\n")
    
    def is_heading(self, text):
        """Determine if text looks like a heading"""
        # Simple heuristics for heading detection
        if len(text) < 100 and (
            text.isupper() or
            text.startswith("Chapter") or
            text.startswith("CHAPTER") or
            re.match(r'^[A-Z][^.!?]*$', text.strip())
        ):
            return True
        return False
    
    def get_selected_text(self):
        """Get currently selected text"""
        try:
            return self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return ""
    
    def get_selection_indices(self):
        """Get selection start and end indices"""
        try:
            return (
                self.text_widget.index(tk.SEL_FIRST),
                self.text_widget.index(tk.SEL_LAST)
            )
        except tk.TclError:
            return None, None
    
    def highlight_text(self, start_index, end_index, highlight_id):
        """Add highlight to text range"""
        tag_name = f"highlight_{highlight_id}"
        self.text_widget.tag_add(tag_name, start_index, end_index)
        self.text_widget.tag_configure(
            tag_name,
            background=self.theme_manager.get_color('highlight'),
            borderwidth=1,
            relief=tk.SOLID
        )
    
    def remove_highlight(self, highlight_id):
        """Remove highlight by ID"""
        tag_name = f"highlight_{highlight_id}"
        self.text_widget.tag_delete(tag_name)
    
    def scroll_to_position(self, position):
        """Scroll to a specific position in the text"""
        self.text_widget.see(position)
    
    def search_text(self, query, start_pos="1.0"):
        """Search for text and return position"""
        pos = self.text_widget.search(query, start_pos, tk.END)
        return pos if pos else None
    
    def set_font_size(self, size):
        """Change font size"""
        self.font_size = size
        self.update_fonts()
        self.create_text_tags()
        
        # Refresh content if available
        if self.current_content:
            self.display_content(self.current_content)
    
    def set_font_family(self, family):
        """Change font family"""
        self.font_family = family
        self.update_fonts()
        self.create_text_tags()
        
        # Refresh content if available
        if self.current_content:
            self.display_content(self.current_content)
    
    def set_line_spacing(self, spacing):
        """Change line spacing"""
        self.line_spacing = spacing
        self.update_fonts()
        
        # Refresh content if available
        if self.current_content:
            self.display_content(self.current_content)
