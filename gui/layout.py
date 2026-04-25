"""
layout.py - Smart Video Reframer Studio GUI Layout

This file defines the visual structure of the application window.
Think of it as the "blueprint" of what the user sees on screen.

=========================================================================
CORE CONCEPTS EXPLAINED FROM SCRATCH
=========================================================================

VISUAL LAYOUT (The "GUI"):
- GUI stands for Graphical User Interface - the windows, buttons, and panels you see
- We use CustomTkinter (a modern fork of Tkinter) for professional look
- The app is divided into PANELS (sections):

  +---------------------+-------------------+---------------------+
  |   LEFT PANEL       |  CENTER PANEL     |   RIGHT PANEL       |
  |   (File List)     |  (Preview)      |   (Options)        |
  |                   |                 |                   |
  |   - Import btn   |   Video        |   - Aspect Ratio |
  |   - File list   |   Player      |   - Export      |
  |   - Batch      |   Timeline    |   - AI Features |
  |                   |                 |   - Quality    |
  +---------------------+-------------------+---------------------+
  |           BOTTOM PANEL (Queue & Progress)                      |
  |   Export Queue | Progress Bar | Status Message          |
  +--------------------------------------------------------+

RESPONSIVE DESIGN:
- The window automatically sizes to fit any screen (laptop to 4K monitor)
- Uses grid system where center expands but side panels stay fixed
- Minimum size: 1280x720 (works on small laptops)

=========================================================================
WHAT WE UPDATED (VERSION HISTORY)
=========================================================================

v1.0 - Initial Release:
- Dark, Light, Ocean Blue, Midnight Purple, Forest Green themes
- 400px wide right panel (was 320px)
- Scrollable options panel
- Performance mode selector (Auto/GPU/CPU)
- Themes selector dropdown

=========================================================================
"""

import customtkinter as ctk
import screeninfo


# ==========================================================================
# THEME SYSTEM - How Colors Work
# ==========================================================================

"""
THEMES: A theme is simply a dictionary of colors that the GUI uses.

Why themes? 
- Different users prefer different looks
- Some work in dark rooms (dark theme)
- Some work in bright offices (light theme)
- Some want brand colors (purple, green, blue)

Structure:
    "ThemeName": {
        "appearance_mode": "dark" or "light",
        "accent": "#RRGGBB",      - Main button color
        "accent_hover": "#RRGGBB", - Button when mouse hovers
        "sidebar_bg": "#RRGGBB",    - Left panel background
        "content_bg": "#RRGGBB",    - Center panel background  
        "panel_bg": "#RRGGBB",    - Right/bottom panel bg
        "text_primary": "#RRGGBB",  - Main text color
        "text_secondary": "#RRGGBB", - Muted text color
        "text_accent": "#RRGGBB",  - Highlighted text
        "status_ready": "#RRGGBB",  - Green status
        "status_warning": "#RRGGBB", - Yellow/orange
        "status_error": "#RRGGBB",   - Red
        "separator": "#RRGGBB",    - Line colors
    }

How to add a new theme:
1. Add entry to APP_THEMES dict below
2. Test both dark and light appearance modes
"""

APP_THEMES = {
    "Dark": {
        "appearance_mode": "dark",
        "accent": "#00B4D8",        # Cyan - our brand color
        "accent_hover": "#0096c7",   # Darker cyan
        "sidebar_bg": "#0f0f1a",     # Very dark gray
        "content_bg": "#1a1a2e",     # Dark blue-gray
        "panel_bg": "#0f0f1a",
        "text_primary": "#ffffff",    # White
        "text_secondary": "#aaaaaa",  # Gray
        "text_accent": "#00B4D8",
        "status_ready": "#00ff88",     # Green
        "status_warning": "#ffaa00",  # Orange
        "status_error": "#ff4444",  # Red
        "separator": "#333333",
    },
    "Light": {
        "appearance_mode": "light",
        "accent": "#0077B6",        # Professional blue
        "accent_hover": "#005f91",
        "sidebar_bg": "#f0f0f0",    # Light gray
        "content_bg": "#ffffff",     # White
        "panel_bg": "#f0f0f0",
        "text_primary": "#1a1a1a",   # Near black
        "text_secondary": "#666666",  # Medium gray
        "text_accent": "#0077B6",
        "status_ready": "#00aa55",
        "status_warning": "#ff8800",
        "status_error": "#cc0000",
        "separator": "#cccccc",
    },
    "Ocean Blue": {
        "appearance_mode": "dark",
        "accent": "#0078D4",
        "accent_hover": "#005a9e",
        "sidebar_bg": "#0d1b2a",    # Navy
        "content_bg": "#1b263b",
        "panel_bg": "#0d1b2a",
        "text_primary": "#e0e1dd",
        "text_secondary": "#778da9",
        "text_accent": "#0078D4",
        "status_ready": "#00d26a",
        "status_warning": "#ffb700",
        "status_error": "#ff4757",
        "separator": "#415a77",
    },
    "Midnight Purple": {
        "appearance_mode": "dark",
        "accent": "#9D4EDD",        # Purple
        "accent_hover": "#7b2cbf",
        "sidebar_bg": "#10002b",    # Deep purple
        "content_bg": "#240046",
        "panel_bg": "#10002b",
        "text_primary": "#e0aaff",
        "text_secondary": "#c77dff",
        "text_accent": "#9D4EDD",
        "status_ready": "#b5179e",
        "status_warning": "#ff9f1c",
        "status_error": "#e63946",
        "separator": "#5a189a",
    },
    "Forest Green": {
        "appearance_mode": "dark",
        "accent": "#52b788",
        "accent_hover": "#2d6a4f",
        "sidebar_bg": "#081c15",     # Dark green
        "content_bg": "#1b4332",
        "panel_bg": "#081c15",
        "text_primary": "#d8f3dc",
        "text_secondary": "#95d5b2",
        "text_accent": "#52b788",
        "status_ready": "#74c69d",
        "status_warning": "#ffb703",
        "status_error": "#e63946",
        "separator": "#2d6a4f",
    },
}


# ==========================================================================
# SCREEN SIZE DETECTION - How Responsive Scaling Works
# ==========================================================================

"""
RESPONSIVE GUI: Why it matters

On a 13" laptop: 1366x768 pixels
On a 27" monitor: 2560x1440 pixels  
On a 4K display: 3840x2160 pixels

If we use fixed size (1400x900):
- Too big for laptop (cuts off, scrollbars everywhere)
- Too small for 4K (wasted space)

Our solution: Detect screen and scale accordingly.

How get_optimal_window_size() works:
1. screeninfo.get_monitors() gets all displays
2. Take the primary monitor (index 0)
3. Calculate 95% of screen size
4. Enforce minimum 1280x720

This ensures:
- Enough space to see all features
- Works on projector/laptop/monitor
- Doesn't overflow tiny screens
"""

def get_screen_size():
    """
    Get the primary monitor's width and height.
    
    Returns:
        tuple: (width_pixels, height_pixels)
    
    Example:
        >>> w, h = get_screen_size()
        >>> print(f"My screen is {w}x{h}")
        My screen is 1920x1080
    """
    try:
        monitors = screeninfo.get_monitors()
        if monitors:
            m = monitors[0]
            return m.width, m.height
    except Exception:
        pass
    return 1920, 1080  # Default fallback


def get_optimal_window_size():
    """
    Calculate best window size for current screen.
    
    Returns:
        tuple: (window_width, window_height)
    
    Logic:
        - Use 95% of available screen
        - Minimum = 1280x720 (basic functionality)
        - Maximum = 1920x1080 (reasonable for most)
    """
    screen_w, screen_h = get_screen_size()
    
    # Use 90% of screen with max limits
    window_w = min(int(screen_w * 0.95), 1920)
    window_h = min(int(screen_h * 0.95), 1080)
    
    # Ensure minimum for basic functionality
    window_w = max(window_w, 1280)
    window_h = max(window_h, 720)
    
    return window_w, window_h


# ==========================================================================
# MAIN WINDOW - The Application Shell
# ==========================================================================

class MainWindow(ctk.CTkFrame):
    """
    The main application window frame.
    
    This is the CONTAINER that holds all GUI elements.
    Think of it as the "walls" of your house.
    
    ==========================================================================
    WIDGET HIERARCHY (How things nest):
    ==========================================================================
    
    MainWindow (CTkFrame)
    ├── Title Bar (top header)
    │   ├── App Title Label
    │   ├── Theme Dropdown
    │   └── Performance Indicator
    ├── Sidebar (left panel)
    │   ├── Import Button
    │   ├── File List (text box)
    │   └── Batch Button
    ├── Content Frame (center)
    │   ├── Preview Label
    │   ├── Preview Area (video display)
    │   └── Playback Controls
    ├── Right Panel (options)
    │   └── Scrollable Frame
    │       ├── Aspect Ratio Dropdown
    │       ├── Export Target Dropdown
    │       ├── AI Feature Checkboxes
    │       ├── Performance Dropdown
    │       ├── Quality Dropdown
    │       ├── Bitrate Dropdown
    │       └── Process Button
    └── Bottom Panel
        ├── Queue Label
        ├── Clear Button
        ├── Queue Scroll
        ├── Progress Bar
        └── Status Label
    
    ==========================================================================
    KEY METHODS EXPLAINED:
    ==========================================================================
    
    __init__(master, theme_name):
        - Called when window is created
        - Sets up grid layout for responsive design
        - Calls each _create_* method to build panels
        
    _create_title_bar():
        - Top section with app name
        - Theme selector (dropdown)
        - Performance indicator (● Auto)
        - Height: 45px (fixed, doesn't expand)
        
    _create_sidebar():
        - Left panel: 300px width
        - Contains file library
        - Import and batch processing buttons
        - Stays same width on all screens
        
    _create_main_content():
        - Center panel: EXPANDS to fill space
        - Video preview area
        - Play/timeline controls
        - This is what grows/shrinks
        
    _create_right_panel():
        - Right panel: 400px width
        - All processing options
        - SCROLLABLE FRAME - can scroll if needed
        - Fixed width but internal scroll
        
    _create_bottom_panel():
        - Bottom section: 130px height
        - Export queue display
        - Progress bar
        - Status messages
        - Fixed height
        
    ==========================================================================
    GRID LAYOUT EXPLAINED:
    ==========================================================================
    
    We use grid (like a spreadsheet):
    
        Col 0     Col 1       Col 2
    Row 0 | Title Bar | Title Bar | Title Bar |
    Row 1 | Sidebar  | Preview  | Options   |
    Row 2 | Sidebar  | Preview  | Options   |
    Row 3 | Sidebar  | Preview  | Options   |
    Row 4 | Bottom  | Bottom   | Bottom    |
    
    Weight determines expansion:
    - Column 0 weight=0 (fixed sidebar)
    - Column 1 weight=5 (preview expands 5x more)
    - Column 2 weight=0 (fixed options)
    
    ==========================================================================
    """
    
    def __init__(self, master=None, theme_name="Dark"):
        """
        Create the main application window.
        
        Args:
            master: Parent widget (usually None for root window)
            theme_name: "Dark", "Light", "Ocean Blue", "Midnight Purple", "Forest Green"
        
        Example:
            >>> window = MainWindow(theme_name="Ocean Blue")
            >>> window.pack()
        """
        # Initialize parent frame with default background
        super().__init__(master, fg_color="#1a1a2e")
        
        # Store references
        self.controller = None  # Will be set by controller
        self.theme_name = theme_name
        self.theme = APP_THEMES.get(theme_name, APP_THEMES["Dark"])
        
        # ==========================================================================
        # GRID CONFIGURATION FOR RESPONSIVE LAYOUT
        # ==========================================================================
        # 
        # Row 0: Title bar (weight 0 = doesn't stretch)
        # Row 1: Main content (weight 1 = stretches)
        # Row 2: Bottom panel (weight 0 = doesn't stretch)
        #
        # Column 0: Sidebar (weight 0 = fixed)
        # Column 1: Preview (weight 1 = stretches)
        # Column 2: Options (weight 0 = fixed)
        #
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)  # Main area stretches
        self.grid_rowconfigure(2, weight=0)
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=5)  # Preview gets 5x space
        self.grid_columnconfigure(2, weight=0)
        
        # Build all panels
        self._create_title_bar()
        self._create_sidebar()
        self._create_main_content()
        self._create_right_panel()
        self._create_bottom_panel()
        
    def _create_title_bar(self):
        """
        Create the top header bar.
        
        Contains:
        - App title with lightning emoji
        - Theme dropdown selector
        - Performance status indicator
        
        The indicator shows:
        - "● Auto" (green) = Auto-detect GPU
        - "● GPU" (green) = GPU available
        - "● CPU" (orange) = CPU only mode
        """
        theme = self.theme
        
        # Title bar frame - spans all columns
        self.title_bar = ctk.CTkFrame(
            self, height=45, corner_radius=0, 
            fg_color=theme.get("sidebar_bg", "#0f0f1a")
        )
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        # Allow title to expand and push indicators to edges
        self.title_bar.grid_columnconfigure(0, weight=1)
        
        # App title (left-aligned)
        self.app_title = ctk.CTkLabel(
            self.title_bar,
            text="⚡ Smart Video Reframer Studio",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=theme.get("text_accent", "#00B4D8")
        )
        self.app_title.pack(side="left", padx=25, pady=8)
        
        # "Theme:" label
        self.theme_label = ctk.CTkLabel(
            self.title_bar,
            text="Theme:",
            font=ctk.CTkFont(size=12),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.theme_label.pack(side="left", padx=(40, 5))
        
        # Theme dropdown (lets user pick theme)
        self.theme_var = ctk.StringVar(value=self.theme_name)
        self.theme_menu = ctk.CTkOptionMenu(
            self.title_bar,
            values=list(APP_THEMES.keys()),
            variable=self.theme_var,
            fg_color=theme.get("content_bg", "#1a1a2e"),
            button_color=theme.get("accent", "#00B4D8"),
            button_hover_color=theme.get("accent_hover", "#0096c7"),
            dropdown_fg_color=theme.get("content_bg", "#1a1a2e"),
            width=130,
            height=30
        )
        self.theme_menu.pack(side="left", padx=5)
        
        # Performance indicator (right-aligned)
        self.perf_indicator = ctk.CTkLabel(
            self.title_bar,
            text="● Auto",
            font=ctk.CTkFont(size=13),
            text_color=theme.get("status_ready", "#00ff88")
        )
        self.perf_indicator.pack(side="right", padx=25, pady=8)

    def _create_sidebar(self):
        """
        Left sidebar panel - Video Library.
        
        Contains:
        - "Video Library" title
        - "+ Import Videos" button
        - File list text box (shows imported videos)
        - "Batch Processing" section
        - "Process All" button
        
        Purpose:
        - Import videos to process
        - View list of imported files
        - Batch process multiple videos
        """
        theme = self.theme
        
        # Sidebar frame - fixed width, full height
        self.sidebar = ctk.CTkFrame(
            self, width=300, corner_radius=0, 
            fg_color=theme.get("sidebar_bg", "#0f0f1a")
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)  # Allow internal expansion
        
        # Section title
        self.library_label = ctk.CTkLabel(
            self.sidebar,
            text="📁 Video Library",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=theme.get("text_primary", "#ffffff")
        )
        self.library_label.pack(anchor="w", padx=25, pady=(18, 8))
        
        # Import button - opens file dialog
        self.import_btn = ctk.CTkButton(
            self.sidebar,
            text="+ Import Videos",
            height=40,
            fg_color=theme.get("accent", "#00B4D8"),
            hover_color=theme.get("accent_hover", "#0096c7"),
            font=ctk.CTkFont(size=13)
        )
        self.import_btn.pack(fill="x", padx=25, pady=8)
        
        # Visual separator line
        self.separator1 = ctk.CTkFrame(
            self.sidebar, height=2, 
            fg_color=theme.get("separator", "#333333")
        )
        self.separator1.pack(fill="x", padx=25, pady=12)
        
        # Files section
        self.file_list_label = ctk.CTkLabel(
            self.sidebar,
            text="Files",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.file_list_label.pack(anchor="w", padx=25, pady=(8, 0))
        
        # File list - scrollable text box
        # CTkTextbox is like a text editor
        self.file_list = ctk.CTkTextbox(
            self.sidebar,
            activate_scrollbars=True,
            font=ctk.CTkFont(size=13),
            height=250
        )
        self.file_list.pack(fill="both", padx=25, pady=8, expand=True)
        # Default placeholder text
        self.file_list.insert("1.0", "Drop videos here or click Import")
        
        # Another separator
        self.separator2 = ctk.CTkFrame(
            self.sidebar, height=2, 
            fg_color=theme.get("separator", "#333333")
        )
        self.separator2.pack(fill="x", padx=25, pady=12)
        
        # Batch processing section
        self.batch_label = ctk.CTkLabel(
            self.sidebar,
            text="⚙️ Batch Processing",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.batch_label.pack(anchor="w", padx=25, pady=(8, 0))
        
        # Batch process all button
        self.batch_btn = ctk.CTkButton(
            self.sidebar,
            text="Process All",
            height=36,
            fg_color="#6c757d",
            hover_color="#5a6268",
            state="disabled",  # Starts disabled until files imported
            font=ctk.CTkFont(size=13)
        )
        self.batch_btn.pack(fill="x", padx=25, pady=8)
        
    def _create_main_content(self):
        """
        Center panel - Video Preview.
        
        This is where:
        - Video plays (placeholder now, will show frames)
        - Play/pause controls
        - Timeline slider
        - Time display (00:00 / 00:00)
        
        This panel EXPANDS to fill available space.
        """
        theme = self.theme
        
        # Content frame - fills center column
        self.content_frame = ctk.CTkFrame(
            self, corner_radius=0, 
            fg_color=theme.get("content_bg", "#1a1a2e")
        )
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Preview section title
        self.preview_label = ctk.CTkLabel(
            self.content_frame,
            text="▶ Preview",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=theme.get("text_primary", "#ffffff")
        )
        self.preview_label.pack(anchor="w", padx=25, pady=(12, 8))
        
        # Video preview area (black background)
        self.preview_area = ctk.CTkFrame(
            self.content_frame,
            fg_color="#000000",  # Black for video
            corner_radius=10
        )
        self.preview_area.pack(fill="both", expand=True, padx=25, pady=12)
        
        # Video info label (filename, resolution, fps, duration, size)
        self.video_info_label = ctk.CTkLabel(
            self.content_frame,
            text="No video loaded",
            font=ctk.CTkFont(size=12),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.video_info_label.pack(anchor="w", padx=25, pady=(0, 5))
        
        # Placeholder text (shows when no video)
        self.preview_placeholder = ctk.CTkLabel(
            self.preview_area,
            text="No video loaded\n\nDrag & drop a video file here\nor use Import button",
            font=ctk.CTkFont(size=15),
            text_color="#666666",
            justify="center"
        )
        self.preview_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
        # Playback controls frame
        self.playback_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.playback_frame.pack(fill="x", padx=25, pady=(0, 18))
        
        # Frame step backward button
        self.step_back_btn = ctk.CTkButton(
            self.playback_frame,
            text="⏮",
            width=36,
            height=36,
            fg_color=theme.get("accent", "#00B4D8"),
            hover_color=theme.get("accent_hover", "#0096c7"),
            state="disabled",
            font=ctk.CTkFont(size=14)
        )
        self.step_back_btn.pack(side="left")
        
        # Play/Pause button
        self.play_btn = ctk.CTkButton(
            self.playback_frame,
            text="▶ Play",
            width=80,
            height=36,
            fg_color=theme.get("accent", "#00B4D8"),
            hover_color=theme.get("accent_hover", "#0096c7"),
            state="disabled",
            font=ctk.CTkFont(size=13)
        )
        self.play_btn.pack(side="left", padx=5)
        
        # Frame step forward button
        self.step_forward_btn = ctk.CTkButton(
            self.playback_frame,
            text="⏭",
            width=36,
            height=36,
            fg_color=theme.get("accent", "#00B4D8"),
            hover_color=theme.get("accent_hover", "#0096c7"),
            state="disabled",
            font=ctk.CTkFont(size=14)
        )
        self.step_forward_btn.pack(side="left")
        
        # Timeline slider (for seeking)
        accent = theme.get("accent", "#00B4D8")
        self.timeline = ctk.CTkSlider(
            self.playback_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            progress_color=accent,
            button_color=accent,
            button_hover_color=theme.get("accent_hover", "#0096c7")
        )
        self.timeline.pack(side="left", fill="x", expand=True, padx=15)
        self.timeline.set(0)
        
        # Time display ("00:00 / 00:00")
        self.time_label = ctk.CTkLabel(
            self.playback_frame,
            text="00:00 / 00:00",
            font=ctk.CTkFont(size=13),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.time_label.pack(side="left", padx=(10, 0))
        
        # Fullscreen button
        self.fullscreen_btn = ctk.CTkButton(
            self.playback_frame,
            text="⛶",
            width=36,
            height=36,
            fg_color="#6c757d",
            hover_color="#5a6268",
            state="disabled",
            font=ctk.CTkFont(size=14)
        )
        self.fullscreen_btn.pack(side="left", padx=(10, 0))
        
    def _create_right_panel(self):
        """
        Right panel - Processing Options.
        
        This is where user configures:
        1. OUTPUT SETTINGS
           - Target Aspect Ratio (9:16, 16:9, 1:1, 4:5, 4:3)
           - Export Target (YouTube, TikTok, Reels, etc.)
        
        2. AI FEATURES (checkboxes)
           - Auto Subtitles (Whisper AI)
           - AI Subject Tracking  
           - Auto Hook Zoom
           - Cinematic Background
           - Scene Detection
        
        3. PERFORMANCE
           - Auto/GPU/CPU mode selector
        
        4. OUTPUT QUALITY
           - Resolution (720p, 1080p, 4K)
           - Bitrate (4-25 Mbps)
        
        5. PROCESS BUTTON
           - Big button to start processing
        
        Uses CTkScrollableFrame so options can scroll if needed.
        """
        theme = self.theme
        
        # Right panel - fixed width but scrollable
        self.right_panel = ctk.CTkFrame(
            self, width=400, corner_radius=0, 
            fg_color=theme.get("panel_bg", "#0f0f1a")
        )
        self.right_panel.grid(row=1, column=2, sticky="nsew")
        self.right_panel.grid_rowconfigure(1, weight=1)
        
        accent = theme.get("accent", "#00B4D8")
        accent_hover = theme.get("accent_hover", "#0096c7")
        
        # Scrollable frame - handles overflow
        self.scrollable_panel = ctk.CTkScrollableFrame(
            self.right_panel,
            label_text="⚡ Processing Options",
            label_font=ctk.CTkFont(size=15, weight="bold"),
            label_text_color=theme.get("text_primary", "#ffffff")
        )
        self.scrollable_panel.pack(fill="both", expand=True, padx=8, pady=8)
        
        # ===== OUTPUT SETTINGS =====
        self.aspect_label = ctk.CTkLabel(
            self.scrollable_panel,
            text="Target Aspect Ratio",
            font=ctk.CTkFont(size=13),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.aspect_label.pack(anchor="w", padx=15, pady=(12, 6))
        
        self.aspect_var = ctk.StringVar(value="9:16")
        self.aspect_menu = ctk.CTkOptionMenu(
            self.scrollable_panel,
            values=["9:16", "16:9", "1:1", "4:5", "4:3"],
            variable=self.aspect_var,
            fg_color=theme.get("content_bg", "#1a1a2e"),
            button_color=accent,
            button_hover_color=accent_hover,
            dropdown_fg_color=theme.get("content_bg", "#1a1a2e"),
            font=ctk.CTkFont(size=13)
        )
        self.aspect_menu.pack(fill="x", padx=15, pady=6)
        
        self.target_label = ctk.CTkLabel(
            self.scrollable_panel,
            text="Export Target",
            font=ctk.CTkFont(size=13),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.target_label.pack(anchor="w", padx=15, pady=(18, 6))
        
        self.target_var = ctk.StringVar(value="TikTok (9:16)")
        self.target_menu = ctk.CTkOptionMenu(
            self.scrollable_panel,
            values=["YouTube Long (16:9)", "YouTube Shorts (9:16)", "TikTok (9:16)", 
                   "Facebook Reels (9:16)", "Instagram Reels (9:16)"],
            variable=self.target_var,
            fg_color=theme.get("content_bg", "#1a1a2e"),
            button_color=accent,
            button_hover_color=accent_hover,
            dropdown_fg_color=theme.get("content_bg", "#1a1a2e"),
            font=ctk.CTkFont(size=13)
        )
        self.target_menu.pack(fill="x", padx=15, pady=6)
        
        # Separator
        self.sep2 = ctk.CTkFrame(
            self.scrollable_panel, height=2, 
            fg_color=theme.get("separator", "#333333")
        )
        self.sep2.pack(fill="x", padx=15, pady=18)
        
        # ===== AI FEATURES =====
        self.ai_label = ctk.CTkLabel(
            self.scrollable_panel,
            text="🤖 AI Features",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.ai_label.pack(anchor="w", padx=15, pady=(6, 6))
        
        # Checkbox = opt-in features
        self.subtitle_checkbox = ctk.CTkCheckBox(
            self.scrollable_panel,
            text="Auto Subtitles (Whisper)",
            fg_color=accent,
            hover_color=accent_hover,
            font=ctk.CTkFont(size=13)
        )
        self.subtitle_checkbox.pack(anchor="w", padx=15, pady=6)
        self.subtitle_checkbox.select()  # Default ON
        
        self.tracking_checkbox = ctk.CTkCheckBox(
            self.scrollable_panel,
            text="AI Subject Tracking",
            fg_color=accent,
            hover_color=accent_hover,
            font=ctk.CTkFont(size=13)
        )
        self.tracking_checkbox.pack(anchor="w", padx=15, pady=6)
        self.tracking_checkbox.select()
        
        self.zoom_checkbox = ctk.CTkCheckBox(
            self.scrollable_panel,
            text="Auto Hook Zoom",
            fg_color=accent,
            hover_color=accent_hover,
            font=ctk.CTkFont(size=13)
        )
        self.zoom_checkbox.pack(anchor="w", padx=15, pady=6)
        self.zoom_checkbox.select()
        
        self.bg_checkbox = ctk.CTkCheckBox(
            self.scrollable_panel,
            text="Cinematic Background",
            fg_color=accent,
            hover_color=accent_hover,
            font=ctk.CTkFont(size=13)
        )
        self.bg_checkbox.pack(anchor="w", padx=15, pady=6)
        self.bg_checkbox.select()
        
        self.scene_checkbox = ctk.CTkCheckBox(
            self.scrollable_panel,
            text="Scene Detection",
            fg_color=accent,
            hover_color=accent_hover,
            font=ctk.CTkFont(size=13)
        )
        self.scene_checkbox.pack(anchor="w", padx=15, pady=6)
        self.scene_checkbox.select()
        
        # Separator
        self.sep3 = ctk.CTkFrame(
            self.scrollable_panel, height=2, 
            fg_color=theme.get("separator", "#333333")
        )
        self.sep3.pack(fill="x", padx=15, pady=18)
        
        # ===== PERFORMANCE =====
        self.perf_label = ctk.CTkLabel(
            self.scrollable_panel,
            text="⚡ Performance",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.perf_label.pack(anchor="w", padx=15, pady=(6, 6))
        
        self.perf_var = ctk.StringVar(value="Auto (GPU if available)")
        self.perf_menu = ctk.CTkOptionMenu(
            self.scrollable_panel,
            values=["Auto (GPU if available)", "GPU Only", "CPU Only"],
            variable=self.perf_var,
            fg_color=theme.get("content_bg", "#1a1a2e"),
            button_color=accent,
            button_hover_color=accent_hover,
            dropdown_fg_color=theme.get("content_bg", "#1a1a2e"),
            font=ctk.CTkFont(size=13)
        )
        self.perf_menu.pack(fill="x", padx=15, pady=6)
        
        # Separator
        self.sep4 = ctk.CTkFrame(
            self.scrollable_panel, height=2, 
            fg_color=theme.get("separator", "#333333")
        )
        self.sep4.pack(fill="x", padx=15, pady=18)
        
        # ===== OUTPUT QUALITY =====
        self.quality_label = ctk.CTkLabel(
            self.scrollable_panel,
            text="🎬 Output Quality",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.quality_label.pack(anchor="w", padx=15, pady=(6, 6))
        
        self.quality_var = ctk.StringVar(value="High (1080p)")
        self.quality_menu = ctk.CTkOptionMenu(
            self.scrollable_panel,
            values=["Low (720p)", "Medium (1080p)", "High (1080p)", "Ultra (4K)"],
            variable=self.quality_var,
            fg_color=theme.get("content_bg", "#1a1a2e"),
            button_color=accent,
            button_hover_color=accent_hover,
            dropdown_fg_color=theme.get("content_bg", "#1a1a2e"),
            font=ctk.CTkFont(size=13)
        )
        self.quality_menu.pack(fill="x", padx=15, pady=6)
        
        self.bitrate_label = ctk.CTkLabel(
            self.scrollable_panel,
            text="Bitrate",
            font=ctk.CTkFont(size=12),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.bitrate_label.pack(anchor="w", padx=15, pady=(12, 0))
        
        self.bitrate_var = ctk.StringVar(value="8 Mbps")
        self.bitrate_menu = ctk.CTkOptionMenu(
            self.scrollable_panel,
            values=["4 Mbps", "8 Mbps", "12 Mbps", "16 Mbps", "25 Mbps"],
            variable=self.bitrate_var,
            fg_color=theme.get("content_bg", "#1a1a2e"),
            button_color=accent,
            button_hover_color=accent_hover,
            dropdown_fg_color=theme.get("content_bg", "#1a1a2e"),
            font=ctk.CTkFont(size=13)
        )
        self.bitrate_menu.pack(fill="x", padx=15, pady=6)
        
        # Separator before button
        self.sep5 = ctk.CTkFrame(
            self.scrollable_panel, height=2, 
            fg_color=theme.get("separator", "#333333")
        )
        self.sep5.pack(fill="x", padx=15, pady=18)
        
        # Process button - THE MAIN ACTION
        self.process_btn = ctk.CTkButton(
            self.scrollable_panel,
            text="▶ Process Video",
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=accent,
            hover_color=accent_hover,
            state="disabled"  # Enable when file selected
        )
        self.process_btn.pack(fill="x", padx=15, pady=25)
        
    def _create_bottom_panel(self):
        """
        Bottom panel - Export Queue & Progress.
        
        Shows:
        - Export queue (list of videos to process)
        - Clear button (remove all from queue)
        - Progress bar (shows processing status)
        - Status text (Ready, Processing, Complete, Error)
        
        Fixed height, spans full width.
        """
        theme = self.theme
        
        # Bottom panel - spans all columns
        self.bottom_panel = ctk.CTkFrame(
            self, height=130, corner_radius=0, 
            fg_color=theme.get("panel_bg", "#0f0f1a")
        )
        self.bottom_panel.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.bottom_panel.grid_columnconfigure(1, weight=1)
        
        # Queue title
        self.queue_label = ctk.CTkLabel(
            self.bottom_panel,
            text="📤 Export Queue",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=theme.get("text_primary", "#ffffff")
        )
        self.queue_label.grid(row=0, column=0, padx=25, pady=(12, 6), sticky="w")
        
        # Clear queue button
        self.clear_btn = ctk.CTkButton(
            self.bottom_panel,
            text="Clear",
            width=70,
            height=32,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=12)
        )
        self.clear_btn.grid(row=0, column=1, padx=25, pady=6, sticky="e")
        
        # Queue scroll area (horizontal for items)
        self.queue_scroll = ctk.CTkScrollableFrame(
            self.bottom_panel,
            orientation="horizontal",
            height=75,
            fg_color="transparent"
        )
        self.queue_scroll.grid(row=1, column=0, columnspan=2, padx=20, pady=6, sticky="ew")
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            self.bottom_panel,
            text="Progress:",
            font=ctk.CTkFont(size=13),
            text_color=theme.get("text_secondary", "#aaaaaa")
        )
        self.progress_label.grid(row=2, column=0, padx=25, pady=(12, 0), sticky="w")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.bottom_panel,
            height=22,
            progress_color=theme.get("accent", "#00B4D8")
        )
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=25, pady=(6, 12), sticky="ew")
        self.progress_bar.set(0)  # Start at 0%
        
        # Status message
        self.status_label = ctk.CTkLabel(
            self.bottom_panel,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color=theme.get("status_ready", "#00ff88")
        )
        self.status_label.grid(row=4, column=0, padx=25, pady=(0, 12), sticky="w")


class Layout:
    """
    Legacy compatibility wrapper.
    
    Old code used pack() geometry manager.
    This class maintains compatibility.
    
    Note: New code should use MainWindow directly.
    """
    def __init__(self, root):
        """Create legacy layout (not recommended for new code)."""
        self.root = root
        self.root.title("Smart Video Reframer Studio")
        self.root.geometry("1600x900")
        
        self.left_panel = ctk.CTkFrame(self.root, width=300)
        self.left_panel.pack(side="left", fill="y")
        
        self.center_panel = ctk.CTkFrame(self.root)
        self.center_panel.pack(side="left", fill="both", expand=True)
        
        self.right_panel = ctk.CTkFrame(self.root, width=400)
        self.right_panel.pack(side="right", fill="y")
        
        self.bottom_panel = ctk.CTkFrame(self.root, height=130)
        self.bottom_panel.pack(side="bottom", fill="x")