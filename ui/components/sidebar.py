"""
Sidebar Component
Navigation sidebar with bookmarks and notes
"""
import customtkinter as ctk
import tkinter as tk

class Sidebar(ctk.CTkFrame):
    """Sidebar for navigation and content management"""
    
    def __init__(self, parent, theme_manager, bookmark_manager, notes_manager):
        """Initialize sidebar"""
        super().__init__(parent)
        
        self.theme_manager = theme_manager
        self.bookmark_manager = bookmark_manager
        self.notes_manager = notes_manager
        
        # Register with theme manager
        self.theme_manager.register_widget(self, "frame")
        
        # Configure sidebar
        self.configure(width=300, corner_radius=10)
        self.grid_propagate(False)
        
        # State
        self.is_visible = True
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sidebar UI components"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self,
            text="Navigation",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.theme_manager.register_widget(title, "label")
        
        # Tabs
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        
        # Bookmarks tab
        self.bookmarks_tab = self.tab_view.add("Bookmarks")
        self.setup_bookmarks_tab()
        
        # Notes tab
        self.notes_tab = self.tab_view.add("Notes")
        self.setup_notes_tab()
        
        # Search tab
        self.search_tab = self.tab_view.add("Search")
        self.setup_search_tab()
    
    def setup_bookmarks_tab(self):
        """Setup bookmarks tab"""
        # Configure grid
        self.bookmarks_tab.grid_columnconfigure(0, weight=1)
        self.bookmarks_tab.grid_rowconfigure(1, weight=1)
        
        # Add bookmark button
        add_btn = ctk.CTkButton(
            self.bookmarks_tab,
            text="+ Add Bookmark",
            height=32,
            command=self.add_bookmark
        )
        add_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.theme_manager.register_widget(add_btn, "button")
        
        # Bookmarks list
        self.bookmarks_frame = ctk.CTkScrollableFrame(self.bookmarks_tab)
        self.bookmarks_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.bookmarks_frame.grid_columnconfigure(0, weight=1)
        self.theme_manager.register_widget(self.bookmarks_frame, "frame")
        
        # No bookmarks label
        self.no_bookmarks_label = ctk.CTkLabel(
            self.bookmarks_frame,
            text="No bookmarks yet.\nClick 'Add Bookmark' to get started.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.no_bookmarks_label.grid(row=0, column=0, padx=20, pady=40)
    
    def setup_notes_tab(self):
        """Setup notes tab"""
        # Configure grid
        self.notes_tab.grid_columnconfigure(0, weight=1)
        self.notes_tab.grid_rowconfigure(1, weight=1)
        
        # Add note button
        add_note_btn = ctk.CTkButton(
            self.notes_tab,
            text="+ Add Note",
            height=32,
            command=self.add_note
        )
        add_note_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.theme_manager.register_widget(add_note_btn, "button")
        
        # Notes list
        self.notes_frame = ctk.CTkScrollableFrame(self.notes_tab)
        self.notes_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.notes_frame.grid_columnconfigure(0, weight=1)
        self.theme_manager.register_widget(self.notes_frame, "frame")
        
        # No notes label
        self.no_notes_label = ctk.CTkLabel(
            self.notes_frame,
            text="No notes yet.\nSelect text and add notes.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.no_notes_label.grid(row=0, column=0, padx=20, pady=40)
    
    def setup_search_tab(self):
        """Setup search tab"""
        # Configure grid
        self.search_tab.grid_columnconfigure(0, weight=1)
        self.search_tab.grid_rowconfigure(2, weight=1)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            self.search_tab,
            placeholder_text="Search in book..."
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<Return>", self.perform_search)
        
        # Search button
        search_btn = ctk.CTkButton(
            self.search_tab,
            text="Search",
            height=32,
            command=self.perform_search
        )
        search_btn.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.theme_manager.register_widget(search_btn, "button")
        
        # Search results
        self.search_results_frame = ctk.CTkScrollableFrame(self.search_tab)
        self.search_results_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.search_results_frame.grid_columnconfigure(0, weight=1)
        self.theme_manager.register_widget(self.search_results_frame, "frame")
    
    def add_bookmark(self):
        """Add a new bookmark"""
        # This would typically get the current reading position
        # For now, we'll use a placeholder
        position = "1.0"  # This should come from the reading area
        
        # Simple dialog for bookmark title
        dialog = ctk.CTkInputDialog(
            text="Enter bookmark title:",
            title="Add Bookmark"
        )
        title = dialog.get_input()
        
        if title:
            bookmark_id = self.bookmark_manager.add_bookmark(position, title)
            self.refresh_bookmarks()
    
    def add_note(self):
        """Add a new note"""
        # Simple dialog for note text
        dialog = ctk.CTkInputDialog(
            text="Enter your note:",
            title="Add Note"
        )
        note_text = dialog.get_input()
        
        if note_text:
            position = "1.0"  # This should come from the reading area
            note_id = self.notes_manager.add_note(position, note_text)
            self.refresh_notes()
    
    def perform_search(self, event=None):
        """Perform search"""
        query = self.search_entry.get().strip()
        if not query:
            return
        
        # Clear previous results
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
        
        # TODO: Implement actual search functionality
        # For now, show placeholder
        result_label = ctk.CTkLabel(
            self.search_results_frame,
            text=f"Searching for: '{query}'\n(Search functionality coming soon)",
            font=ctk.CTkFont(size=12)
        )
        result_label.grid(row=0, column=0, padx=10, pady=10)
        self.theme_manager.register_widget(result_label, "label")
    
    def refresh_bookmarks(self):
        """Refresh bookmarks display"""
        # Clear existing bookmarks
        for widget in self.bookmarks_frame.winfo_children():
            if widget != self.no_bookmarks_label:
                widget.destroy()
        
        bookmarks = self.bookmark_manager.get_bookmarks()
        
        if not bookmarks:
            self.no_bookmarks_label.grid(row=0, column=0, padx=20, pady=40)
        else:
            self.no_bookmarks_label.grid_remove()
            
            for i, bookmark in enumerate(bookmarks):
                bookmark_frame = self.create_bookmark_item(bookmark, i)
                bookmark_frame.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
    
    def refresh_notes(self):
        """Refresh notes display"""
        # Clear existing notes
        for widget in self.notes_frame.winfo_children():
            if widget != self.no_notes_label:
                widget.destroy()
        
        notes = self.notes_manager.get_notes()
        
        if not notes:
            self.no_notes_label.grid(row=0, column=0, padx=20, pady=40)
        else:
            self.no_notes_label.grid_remove()
            
            for i, note in enumerate(notes):
                note_frame = self.create_note_item(note, i)
                note_frame.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
    
    def create_bookmark_item(self, bookmark, index):
        """Create a bookmark item widget"""
        frame = ctk.CTkFrame(self.bookmarks_frame)
        frame.grid_columnconfigure(0, weight=1)
        self.theme_manager.register_widget(frame, "frame")
        
        # Title
        title_label = ctk.CTkLabel(
            frame,
            text=bookmark['title'],
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="ew")
        self.theme_manager.register_widget(title_label, "label")
        
        # Position
        pos_label = ctk.CTkLabel(
            frame,
            text=f"Position: {bookmark['position']}",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        pos_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        return frame
    
    def create_note_item(self, note, index):
        """Create a note item widget"""
        frame = ctk.CTkFrame(self.notes_frame)
        frame.grid_columnconfigure(0, weight=1)
        self.theme_manager.register_widget(frame, "frame")
        
        # Note text (truncated)
        text = note['text'][:100] + "..." if len(note['text']) > 100 else note['text']
        
        text_label = ctk.CTkLabel(
            frame,
            text=text,
            font=ctk.CTkFont(size=11),
            anchor="w",
            wraplength=250
        )
        text_label.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="ew")
        self.theme_manager.register_widget(text_label, "label")
        
        # Date
        date_label = ctk.CTkLabel(
            frame,
            text=note['created_at'][:10],  # Just the date part
            font=ctk.CTkFont(size=9),
            text_color="gray",
            anchor="w"
        )
        date_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        return frame
    
    def update_content(self, bookmarks, notes):
        """Update sidebar content with new data"""
        self.refresh_bookmarks()
        self.refresh_notes()
    
    def toggle_visibility(self):
        """Toggle sidebar visibility"""
        if self.is_visible:
            self.grid_remove()
            self.is_visible = False
        else:
            self.grid()
            self.is_visible = True
