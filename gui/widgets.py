"""
widgets.py: CustomTkinter widgets for Smart Video Reframer Studio.

Key Concepts:
- Widget: A GUI element (button, checkbox, progress bar, etc.).
- CustomTkinter: Provides modern, themed widgets for a professional look.
- Modular Design: Widgets are defined as reusable classes/functions.

How to use:
- Import and add widgets to panels in layout.py or controller.py.
- Extend or customize widgets for new features.
"""

import customtkinter as ctk
from tkinter import filedialog
import os


class FileListWidget(ctk.CTkTextbox):
    """
    Video file list widget for the left panel.
    Supports drag-and-drop and file selection.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_paths = []
        
    def add_file(self, path):
        """Add a file to the list."""
        if os.path.exists(path) and path not in self.file_paths:
            self.file_paths.append(path)
            filename = os.path.basename(path)
            self.insert("end", f"\n{filename}")
            
    def get_files(self):
        """Return list of added file paths."""
        return self.file_paths


class OptionsWidget(ctk.CTkFrame):
    """
    Processing options widget for the right panel.
    Contains all AI feature toggles.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.subtitle_checkbox = ctk.CTkCheckBox(
            self,
            text="Enable Automatic Subtitles",
            fg_color="#00B4D8",
            hover_color="#0096c7"
        )
        self.subtitle_checkbox.pack(anchor="w", pady=5)
        self.subtitle_checkbox.select()
        
        self.tracking_checkbox = ctk.CTkCheckBox(
            self,
            text="Enable AI Subject Tracking",
            fg_color="#00B4D8",
            hover_color="#0096c7"
        )
        self.tracking_checkbox.pack(anchor="w", pady=5)
        self.tracking_checkbox.select()
        
        self.zoom_checkbox = ctk.CTkCheckBox(
            self,
            text="Enable Auto Hook Zoom",
            fg_color="#00B4D8",
            hover_color="#0096c7"
        )
        self.zoom_checkbox.pack(anchor="w", pady=5)
        self.zoom_checkbox.select()
        
        self.bg_checkbox = ctk.CTkCheckBox(
            self,
            text="Generate Cinematic Background",
            fg_color="#00B4D8",
            hover_color="#0096c7"
        )
        self.bg_checkbox.pack(anchor="w", pady=5)
        self.bg_checkbox.select()


class ProgressBarWidget(ctk.CTkProgressBar):
    """
    Progress bar widget for the bottom panel.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.set(0)


class QueueItemWidget(ctk.CTkFrame):
    """
    Queue item widget showing a single export task.
    """
    def __init__(self, master, filename, target, **kwargs):
        super().__init__(master, **kwargs)
        
        self.filename = filename
        self.target = target
        
        # Thumbnail placeholder
        self.thumb = ctk.CTkLabel(
            self,
            text="🎬",
            width=50,
            height=40,
            fg_color="#333333"
        )
        self.thumb.pack(side="left", padx=5, pady=5)
        
        # Info labels
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(side="left", fill="both", expand=True)
        
        self.name_label = ctk.CTkLabel(
            self.info_frame,
            text=filename,
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w"
        )
        self.name_label.pack(anchor="w", padx=5)
        
        self.target_label = ctk.CTkLabel(
            self.info_frame,
            text=target,
            font=ctk.CTkFont(size=10),
            text_color="#888888",
            anchor="w"
        )
        self.target_label.pack(anchor="w", padx=5)
        
        # Status indicator
        self.status = ctk.CTkLabel(
            self,
            text="⏳",
            width=30
        )
        self.status.pack(side="right", padx=5)


class AspectRatioSelector(ctk.CTkFrame):
    """
    Aspect ratio selector widget.
    """
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_change = on_change
        
        self.label = ctk.CTkLabel(
            self,
            text="Target Aspect Ratio",
            font=ctk.CTkFont(size=12)
        )
        self.label.pack(anchor="w", pady=(0, 5))
        
        self.var = ctk.StringVar(value="9:16")
        self.menu = ctk.CTkOptionMenu(
            self,
            values=["9:16", "16:9", "1:1", "4:5", "4:3"],
            variable=self.var,
            fg_color=("#1a1a2e", "#16213e"),
            button_color="#00B4D8",
            button_hover_color="#0096c7",
            dropdown_fg_color=("#1a1a2e", "#16213e")
        )
        self.menu.pack(anchor="w", fill="x")
        
        if on_change:
            self.var.trace_add('write', lambda *_: on_change(self.var.get()))
            
    def get(self):
        return self.var.get()


class ExportTargetSelector(ctk.CTkFrame):
    """
    Export target selector widget.
    """
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_change = on_change
        
        self.label = ctk.CTkLabel(
            self,
            text="Export Target",
            font=ctk.CTkFont(size=12)
        )
        self.label.pack(anchor="w", pady=(0, 5))
        
        self.var = ctk.StringVar(value="TikTok (9:16)")
        self.menu = ctk.CTkOptionMenu(
            self,
            values=["YouTube Long (16:9)", "YouTube Shorts (9:16)", "TikTok (9:16)", "Facebook Reels (9:16)", "Instagram Reels (9:16)"],
            variable=self.var,
            fg_color=("#1a1a2e", "#16213e"),
            button_color="#00B4D8",
            button_hover_color="#0096c7",
            dropdown_fg_color=("#1a1a2e", "#16213e")
        )
        self.menu.pack(anchor="w", fill="x")
        
        if on_change:
            self.var.trace_add('write', lambda *_: on_change(self.var.get()))
            
    def get(self):
        return self.var.get()


class PerformanceModeWidget(ctk.CTkFrame):
    """
    GUI widget for selecting performance mode (Auto, CPU Only, GPU Only).
    
    Key Concepts:
    - User Choice: Allows user to select best performance for their hardware.
    - Auto Mode: Uses hardware detection to select GPU if available, else CPU.
    - Compatibility Mode: Forces CPU-only for maximum compatibility.
    
    How to use:
    - Place in the right panel (options) of the GUI.
    - Bind to config or callback to update pipeline mode.
    """
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_change = on_change
        
        self.label = ctk.CTkLabel(
            self,
            text="⚡ Performance Mode",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label.pack(anchor="w", pady=(0, 5))
        
        self.var = ctk.StringVar(value="Auto (GPU if available)")
        self.menu = ctk.CTkOptionMenu(
            self,
            values=["Auto (GPU if available)", "GPU Only", "CPU Only"],
            variable=self.var,
            fg_color=("#1a1a2e", "#16213e"),
            button_color="#00B4D8",
            button_hover_color="#0096c7",
            dropdown_fg_color=("#1a1a2e", "#16213e")
        )
        self.menu.pack(anchor="w", fill="x")
        
        if on_change:
            self.var.trace_add('write', lambda *_: on_change(self.var.get()))
            
    def get(self):
        mode = self.var.get()
        if "CPU" in mode:
            return "cpu"
        elif "GPU" in mode:
            return "gpu"
        return "auto"


class ImportButton(ctk.CTkButton):
    """
    Import button that opens file dialog.
    """
    def __init__(self, master, on_files_selected=None, **kwargs):
        super().__init__(
            master,
            text="+ Import Videos",
            height=36,
            fg_color=("#00B4D8", "#0096c7"),
            hover_color=("#0096c7", "#0077b6"),
            **kwargs
        )
        
        self.on_files_selected = on_files_selected
        self.configure(command=self._open_dialog)
        
    def _open_dialog(self):
        files = filedialog.askopenfilenames(
            title="Select Videos",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.webm"),
                ("All files", "*.*")
            ]
        )
        if files and self.on_files_selected:
            self.on_files_selected(list(files))


class ProcessButton(ctk.CTkButton):
    """
    Main process button with disabled state management.
    """
    def __init__(self, master, on_click=None, **kwargs):
        super().__init__(
            master,
            text="▶ Process Video",
            height=44,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#00B4D8", "#0096c7"),
            hover_color=("#0096c7", "#0077b6"),
            state="disabled",
            **kwargs
        )
        
        self.on_click = on_click
        self.configure(command=self._on_click)
        
    def _on_click(self):
        if self.on_click and self.cget("state") != "disabled":
            self.on_click()
            
    def enable(self):
        self.configure(state="normal")
        
    def disable(self):
        self.configure(state="disabled")


class StatusIndicator(ctk.CTkLabel):
    """
    Status indicator label with color states.
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=("#00ff88", "#00ff88"),
            **kwargs
        )
        self._state = "ready"
        
    def set_state(self, state):
        """Set status state: ready, processing, complete, error"""
        self._state = state
        
        states = {
            "ready": ("Ready", "#00ff88"),
            "processing": ("Processing...", "#ffaa00"),
            "complete": ("Complete", "#00ff88"),
            "error": ("Error", "#ff4444")
        }
        
        text, color = states.get(state, ("Unknown", "#888888"))
        self.configure(text=text, text_color=(color, color))


class TimelineSlider(ctk.CTkSlider):
    """
    Video timeline slider with time display.
    """
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(
            master,
            from_=0,
            to=100,
            number_of_steps=100,
            progress_color="#00B4D8",
            button_color="#00B4D8",
            button_hover_color="#0096c7",
            **kwargs
        )
        
        self.on_change = on_change
        self.bind("<ButtonRelease-1>", self._on_release)
        
    def _on_release(self, event):
        if self.on_change:
            self.on_change(self.get())
            
    def set_time(self, current, total):
        """Update slider and time display."""
        if total > 0:
            self.configure(to=total)
            self.set(current)
            return f"{self._format_time(current)} / {self._format_time(total)}"
        return "00:00 / 00:00"
        
    def _format_time(self, seconds):
        """Format seconds to MM:SS or HH:MM:SS"""
        mins, secs = divmod(int(seconds), 60)
        hours, mins = divmod(mins, 60)
        if hours > 0:
            return f"{hours:02d}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"


class PlaybackControls(ctk.CTkFrame):
    """
    Video playback controls with play/pause, timeline, and time display.
    """
    def __init__(self, master, on_play=None, on_pause=None, on_seek=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_seek = on_seek
        
        self.is_playing = False
        
        self.play_btn = ctk.CTkButton(
            self,
            text="▶ Play",
            width=80,
            height=32,
            fg_color=("#00B4D8", "#0096c7"),
            hover_color=("#0096c7", "#0077b6"),
            state="disabled",
            command=self._toggle_play
        )
        self.play_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.timeline = TimelineSlider(self, on_change=on_seek)
        self.timeline.grid(row=0, column=1, padx=10, sticky="ew")
        
        self.time_label = ctk.CTkLabel(
            self,
            text="00:00 / 00:00",
            font=ctk.CTkFont(size=12),
            text_color=("#aaaaaa", "#aaaaaa")
        )
        self.time_label.grid(row=0, column=2, padx=(10, 0))
        
        self.grid_columnconfigure(1, weight=1)
        
    def _toggle_play(self):
        if self.is_playing:
            if self.on_pause:
                self.on_pause()
            self.play_btn.configure(text="▶ Play")
        else:
            if self.on_play:
                self.on_play()
            self.play_btn.configure(text="⏸ Pause")
        self.is_playing = not self.is_playing
        
    def update_time(self, current, total):
        """Update time display."""
        return self.timeline.set_time(current, total)
        
    def enable(self):
        self.play_btn.configure(state="normal")
        
    def disable(self):
        self.play_btn.configure(state="disabled")
        self.is_playing = False