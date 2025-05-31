"""
Reading Area Component
Main text display area with reading controls
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext

class ReadingArea(ctk.CTkFrame):
    """Main reading area with text display and controls"""
    
    def __init__(self, parent, theme_manager, highlight_manager, notes_manager):
        """Initialize reading area"""
        super().__init__(parent)
        
        self.theme_manager = theme_manager
        self.highlight_manager = highlight_manager
        self.notes_manager = notes_manager
        
        # Register with theme manager
        self.theme_manager.register_widget(self, "frame")
        
        # Configure reading area
        self.configure(corner_radius=10)
        
        # Current content
        self.current_content = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup reading area UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Reading controls frame
        self.controls_frame = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_propagate(False)
        
        # Navigation controls
        nav_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=0, sticky="w")
        
        # Previous/Next buttons (for chapters)
        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="◀ Prev",
            width=70,
            height=30,
            state="disabled"
        )
        self.prev_btn.grid(row=0, column=0, padx=(0, 5))
        self.theme_manager.register_widget(self.prev_btn, "button")
        
        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="Next ▶",
            width=70,
            height=30,
            state="disabled"
        )
        self.next_btn.grid(row=0, column=1)
        self.theme_manager.register_widget(self.next_btn, "button")
        
        # Reading progress
        self.progress_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.progress_frame.grid(row=0, column=1, sticky="ew", padx=20)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="0%",
            font=ctk.CTkFont(size=10)
        )
        self.progress_label.grid(row=1, column=0)
        self.theme_manager.register_widget(self.progress_label, "label")
        
        # Reading actions
        actions_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e")
        
        # Highlight button
        self.highlight_btn = ctk.CTkButton(
            actions_frame,
            text="🖍️ Highlight",
            width=90,
            height=30,
            command=self.add_highlight
        )
        self.highlight_btn.grid(row=0, column=0, padx=(0, 5))
        self.theme_manager.register_widget(self.highlight_btn, "button")
        
        # Note button
        self.note_btn = ctk.CTkButton(
            actions_frame,
            text="📝 Note",
            width=80,
            height=30,
            command=self.add_note
        )
        self.note_btn.grid(row=0, column=1)
        self.theme_manager.register_widget(self.note_btn, "button")
        
        # Text display area
        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.theme_manager.register_widget(self.text_frame, "frame")
        
        # Create text widget
        self.text_widget = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            padx=40,
            pady=30,
            font=("Georgia", 14),
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED,
            cursor="arrow",
            selectbackground="#B3D4FC"
        )
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(self.text_frame, command=self.text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        
        # Register text widget with theme manager
        self.theme_manager.register_widget(self.text_widget, "text")
        
        # Bind text selection events
        self.text_widget.bind("<Button-1>", self.on_text_click)
        self.text_widget.bind("<ButtonRelease-1>", self.on_text_release)
        self.text_widget.bind("<Double-Button-1>", self.on_double_click)
        
        # Show placeholder text
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder text when no book is loaded"""
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        
        placeholder_text = """
📚 Welcome to Interactive Book Reader

To get started:
1. Click "Open Book" to load an EPUB, PDF, or TXT file
2. Use highlighting tools to mark important text
3. Add notes and bookmarks for reference
4. Switch between light and dark reading modes

Features:
• Support for EPUB, PDF, and TXT formats
• Text highlighting with color options
• Margin notes and annotations
• Bookmarking system
• Reading progress tracking
• Customizable themes for comfortable reading

Click "Open Book" in the toolbar to begin reading!
        """
        
        self.text_widget.insert("1.0", placeholder_text.strip())
        self.text_widget.configure(state=tk.DISABLED)
    
    def get_text_widget(self):
        """Get the text widget for external use"""
        return self.text_widget
    
    def update_navigation(self, content):
        """Update navigation controls based on content"""
        # Enable/disable navigation buttons based on content structure
        has_chapters = content and len(content.get('chapters', [])) > 1
        
        if has_chapters:
            self.prev_btn.configure(state="normal")
            self.next_btn.configure(state="normal")
        else:
            self.prev_btn.configure(state="disabled")
            self.next_btn.configure(state="disabled")
    
    def on_text_click(self, event):
        """Handle text click events"""
        # Clear any existing selection highlights
        pass
    
    def on_text_release(self, event):
        """Handle text release events"""
        # Check if text is selected
        try:
            selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text.strip():
                # Enable highlight and note buttons
                self.highlight_btn.configure(state="normal")
                self.note_btn.configure(state="normal")
            else:
                # Disable buttons if no selection
                self.highlight_btn.configure(state="disabled")
                self.note_btn.configure(state="disabled")
        except tk.TclError:
            # No selection
            self.highlight_btn.configure(state="disabled")
            self.note_btn.configure(state="disabled")
    
    def on_double_click(self, event):
        """Handle double-click events (select word)"""
        # Word selection is handled automatically by tkinter
        self.on_text_release(event)
    
    def add_highlight(self):
        """Add highlight to selected text"""
        try:
            # Get selected text and indices
            start_index = self.text_widget.index(tk.SEL_FIRST)
            end_index = self.text_widget.index(tk.SEL_LAST)
            selected_text = self.text_widget.get(start_index, end_index)
            
            if selected_text.strip():
                # Add highlight using highlight manager
                highlight_id = self.highlight_manager.add_highlight(
                    start_index, end_index, selected_text
                )
                
                # Apply visual highlight
                tag_name = f"highlight_{highlight_id}"
                self.text_widget.tag_add(tag_name, start_index, end_index)
                self.text_widget.tag_configure(
                    tag_name,
                    background=self.theme_manager.get_color('highlight'),
                    borderwidth=1,
                    relief=tk.SOLID
                )
                
                print(f"Added highlight: {selected_text[:50]}...")
                
        except tk.TclError:
            print("No text selected for highlighting")
    
    def add_note(self):
        """Add note to selected text or current position"""
        try:
            # Try to get selected text first
            start_index = self.text_widget.index(tk.SEL_FIRST)
            selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            position = start_index
        except tk.TclError:
            # No selection, use current cursor position
            position = self.text_widget.index(tk.INSERT)
            selected_text = ""
        
        # Simple dialog for note text
        dialog = ctk.CTkInputDialog(
            text="Enter your note:",
            title="Add Note"
        )
        note_text = dialog.get_input()
        
        if note_text:
            # Add note using notes manager
            if selected_text:
                # Add highlight first, then note to highlight
                highlight_id = self.highlight_manager.add_highlight(
                    start_index, self.text_widget.index(tk.SEL_LAST), selected_text
                )
                note_id = self.notes_manager.add_note_to_highlight(highlight_id, note_text)
            else:
                # Add standalone note
                note_id = self.notes_manager.add_note(position, note_text)
            
            print(f"Added note: {note_text}")
    
    def update_progress(self, current_line, total_lines):
        """Update reading progress"""
        if total_lines > 0:
            progress = min(1.0, current_line / total_lines)
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"{int(progress * 100)}%")
