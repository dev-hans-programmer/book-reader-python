"""
Toolbar Component
Main application toolbar with file operations and controls
"""
import customtkinter as ctk
import tkinter as tk

class Toolbar(ctk.CTkFrame):
    """Main application toolbar"""
    
    def __init__(self, parent, theme_manager, open_file_callback, toggle_theme_callback, toggle_sidebar_callback):
        """Initialize toolbar"""
        super().__init__(parent)
        
        self.theme_manager = theme_manager
        self.open_file_callback = open_file_callback
        self.toggle_theme_callback = toggle_theme_callback
        self.toggle_sidebar_callback = toggle_sidebar_callback
        
        # Register with theme manager
        self.theme_manager.register_widget(self, "frame")
        
        # Configure toolbar
        self.configure(height=60, corner_radius=10)
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup toolbar UI components"""
        # Configure grid
        self.grid_columnconfigure(2, weight=1)  # Middle section expands
        
        # Left section - File operations
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Open file button
        open_btn = ctk.CTkButton(
            left_frame,
            text="📖 Open Book",
            width=120,
            height=35,
            command=self.open_file_callback
        )
        open_btn.grid(row=0, column=0, padx=(0, 10))
        self.theme_manager.register_widget(open_btn, "button")
        
        # Center section - Book info
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        self.center_frame.grid_columnconfigure(0, weight=1)
        
        # Book title label
        self.book_title_label = ctk.CTkLabel(
            self.center_frame,
            text="No book loaded",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.book_title_label.grid(row=0, column=0)
        self.theme_manager.register_widget(self.book_title_label, "label")
        
        # Right section - View controls
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        
        # Sidebar toggle button
        sidebar_btn = ctk.CTkButton(
            right_frame,
            text="📋",
            width=40,
            height=35,
            command=self.toggle_sidebar_callback
        )
        sidebar_btn.grid(row=0, column=0, padx=(0, 5))
        self.theme_manager.register_widget(sidebar_btn, "button")
        
        # Font size controls
        font_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        font_frame.grid(row=0, column=1, padx=(0, 10))
        
        font_minus_btn = ctk.CTkButton(
            font_frame,
            text="A-",
            width=30,
            height=35,
            command=self.decrease_font_size
        )
        font_minus_btn.grid(row=0, column=0)
        self.theme_manager.register_widget(font_minus_btn, "button")
        
        font_plus_btn = ctk.CTkButton(
            font_frame,
            text="A+",
            width=30,
            height=35,
            command=self.increase_font_size
        )
        font_plus_btn.grid(row=0, column=1, padx=(2, 0))
        self.theme_manager.register_widget(font_plus_btn, "button")
        
        # Theme toggle button
        theme_btn = ctk.CTkButton(
            right_frame,
            text="🌙",
            width=40,
            height=35,
            command=self.toggle_theme
        )
        theme_btn.grid(row=0, column=2)
        self.theme_manager.register_widget(theme_btn, "button")
        
        # Store reference to theme button for icon updates
        self.theme_btn = theme_btn
    
    def update_book_title(self, title):
        """Update the displayed book title"""
        if len(title) > 50:
            title = title[:47] + "..."
        self.book_title_label.configure(text=title)
    
    def toggle_theme(self):
        """Toggle theme and update button icon"""
        new_theme = self.toggle_theme_callback()
        
        # Update theme button icon
        if new_theme == "dark":
            self.theme_btn.configure(text="☀️")
        else:
            self.theme_btn.configure(text="🌙")
    
    def increase_font_size(self):
        """Increase font size"""
        # This will be connected to the text viewer
        print("Increase font size")
    
    def decrease_font_size(self):
        """Decrease font size"""
        # This will be connected to the text viewer
        print("Decrease font size")
