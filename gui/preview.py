"""
preview.py - Smart Video Reframer Studio - Video Preview System (OPTIMIZED VERSION)

This module handles video loading, playback, and preview display with:
- Threaded video loading (progress indicator)
- Smooth playback using threading
- Video info display
- CPU optimization

=========================================================================
USAGE:
    VideoLoader      - Load video files with progress
    VideoDisplay   - Play videos smoothly
=========================================================================
"""

import cv2
import numpy as np
from PIL import Image, ImageTk
import customtkinter as ctk
import threading
import time
import os
from typing import Optional, Dict, Tuple, Callable


class VideoLoader:
    """
    VideoLoader - Loads video files with progress tracking.
    
    OPTIMIZATION: Pre-loads frames into memory for smooth playback.
    """
    
    def __init__(self):
        self.cap = None
        self.path = None
        self.info = {}
        self.frame_buffer = []  # Pre-loaded frames
        self.is_loading = False
        self.load_progress = 0.0
        
    def load(self, video_path: str, preload: bool = True) -> bool:
        """Load a video file with optional preloading."""
        self.close()
        
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open {video_path}")
            self.cap = None
            return False
            
        self.path = video_path
        
        # Get video properties
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate duration
        duration = frame_count / fps if fps > 0 else 0
        
        # Get file size
        file_size = os.path.getsize(video_path) if os.path.exists(video_path) else 0
        
        self.info = {
            'path': video_path,
            'filename': os.path.basename(video_path),
            'fps': fps,
            'frame_count': frame_count,
            'width': width,
            'height': height,
            'duration': duration,
            'aspect_ratio': width / height if height > 0 else 16/9,
            'codec': self._get_codec_name(),
            'resolution': f"{width}x{height}",
            'file_size': file_size,
            'file_size_mb': file_size / (1024 * 1024)
        }
        
        # Pre-load frames for smooth playback (limit to first 500 frames for performance)
        max_preload = min(frame_count, 500)
        self.frame_buffer = []
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        for i in range(max_preload):
            ret, frame = self.cap.read()
            if not ret:
                break
            self.frame_buffer.append(frame)
            self.load_progress = (i + 1) / max_preload
            
            # Release CPU periodically
            if i % 30 == 0:
                time.sleep(0.001)
        
        # If video is shorter than max, it's fully loaded
        if frame_count <= max_preload:
            self.load_progress = 1.0
            
        # Seek back to start
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        return True
    
    def get_loading_progress(self) -> float:
        """Get loading progress (0.0 to 1.0)."""
        return self.load_progress
    
    def is_fully_loaded(self) -> bool:
        """Check if video is fully loaded."""
        return self.load_progress >= 1.0
    
    def _get_codec_name(self) -> str:
        """Get codec name."""
        if not self.cap:
            return "Unknown"
        fourcc = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        return "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
    
    def get_frame(self, frame_number: int) -> Optional[np.ndarray]:
        """Get a specific frame."""
        if not self.cap:
            return None
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def get_current_frame(self) -> int:
        """Get current frame position."""
        if not self.cap:
            return 0
        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
    
    def close(self):
        """Close video."""
        if self.cap:
            self.cap.release()
            self.cap = None
            self.path = None
            self.info = {}


class VideoDisplay:
    """
    VideoDisplay - Smooth video playback using pre-loaded frames.
    
    OPTIMIZATIONS:
    - Pre-loads frames into memory buffer
    - Plays from memory (no disk I/O during playback)
    - Shows loading progress indicator
    - Uses actual FPS timing for smooth playback
    """
    
    def __init__(self, preview_frame, time_label, timeline, play_btn, info_label=None, progress_callback=None):
        self.preview_frame = preview_frame
        self.time_label = time_label
        self.timeline = timeline
        self.play_btn = play_btn
        self.info_label = info_label
        self.progress_callback = progress_callback  # Callback for loading progress
        
        self.loader = VideoLoader()
        self.tk_image = None
        self.is_playing = False
        self.is_loading = False
        
        # Playback state
        self.frame_number = 0
        self.fps = 30
        self.total_frames = 0
        self.duration = 0
        self.video_path = None
        
        self.timer_id = None
        self._stop_event = threading.Event()
        
        # Loading indicator
        self.loading_label = None
        self.display_label = None
        
        if preview_frame:
            self.display_label = ctk.CTkLabel(preview_frame, text="")
            self.display_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Loading text
            self.loading_label = ctk.CTkLabel(
                preview_frame,
                text="Loading video...",
                font=ctk.CTkFont(size=14),
                text_color="#ffffff"
            )
            self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def load_video(self, path: str) -> bool:
        """Load video with progress indicator."""
        self.pause()
        
        # Show loading
        if self.loading_label:
            self.loading_label.configure(text="⏳ Loading video...")
            self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Load in background thread
        def load_thread():
            success = self.loader.load(path)
            
            if success:
                self.fps = self.loader.info['fps']
                self.total_frames = self.loader.info['frame_count']
                self.duration = self.loader.info['duration']
                self.frame_number = 0
                self.video_path = path
                
                if self.timeline:
                    self.timeline.configure(to=self.total_frames)
                    self.timeline.set(0)
                
                # Update on main thread
                if self.preview_frame:
                    self.preview_frame.after(0, self._finish_loading)
            else:
                if self.preview_frame:
                    self.preview_frame.after(0, lambda: self.loading_label.configure(text="❌ Load failed"))
        
        thread = threading.Thread(target=load_thread, daemon=True)
        thread.start()
        return True
    
    def _finish_loading(self):
        """Finish loading and show first frame."""
        # Hide loading
        if self.loading_label:
            self.loading_label.place_forget()
        
        # Update info
        self._update_info_display()
        
        # Show first frame
        self._update_frame_display()
        
        if self.play_btn:
            self.play_btn.configure(state="normal", text="▶ Play")
    
    def _update_info_display(self):
        """Update video info display."""
        if self.info_label and self.loader.info:
            info = self.loader.info
            size_mb = info.get('file_size_mb', 0)
            duration = info.get('duration', 0)
            mins = int(duration // 60)
            secs = int(duration % 60)
            
            info_text = f"📹 {info.get('filename', 'Unknown')} | {info.get('resolution', '?')} | {info.get('fps', 0):.1f} fps | {mins:02d}:{secs:02d} | {size_mb:.1f} MB"
            self.info_label.configure(text=info_text)
    
def _update_frame_display(self):
        """Display current frame from buffer."""
        # Try to get from buffer first
        frame = None
        
        if self.frame_number < len(self.loader.frame_buffer):
            frame = self.loader.frame_buffer[self.frame_number]
        elif self.loader.cap:
            # Fallback to seeking (for frames beyond buffer)
            self.loader.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
            ret, frame = self.loader.cap.read()
        
        if frame is None:
            return
            
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Get preview size
        preview_w, preview_h = 640, 360
        
        if self.preview_frame:
            try:
                w = self.preview_frame.winfo_width()
                h = self.preview_frame.winfo_height()
                if w > 10 and h > 10:
                    preview_w, preview_h = w - 20, h - 20
            except:
                pass
        
        # Resize maintaining aspect ratio
        h_img, w_img = frame_rgb.shape[:2]
        scale = min(preview_w / w_img, preview_h / h_img)
        
        if scale < 1:
            new_w = int(w_img * scale)
            new_h = int(h_img * scale)
            frame_rgb = cv2.resize(frame_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Convert to PhotoImage - MUST keep a reference!
        pil_image = Image.fromarray(frame_rgb)
        self.tk_image = ImageTk.PhotoImage(pil_image)
        
        if self.display_label:
            self.display_label.configure(image=self.tk_image, text="")
        
        self._update_time_display()
    
    def _update_time_display(self):
        """Update time label."""
        if not self.time_label or self.fps == 0:
            return
            
        current = self.frame_number / self.fps
        total = self.duration
        
        curr_str = self._format_time(current)
        total_str = self._format_time(total)
        
        self.time_label.configure(text=f"{curr_str} / {total_str}")
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds as MM:SS.ms"""
        millis = int((seconds % 1) * 100)
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}.{millis:02d}"
    
    def play(self):
        """Start playback."""
        if self.is_playing:
            return
            
        self.is_playing = True
        self._stop_event.clear()
        
        if self.play_btn:
            self.play_btn.configure(text="⏸ Pause")
        
        self._play_loop()
    
    def _play_loop(self):
        """Playback loop - advances frames based on FPS."""
        if not self.is_playing:
            return
        
        # Advance frame
        self.frame_number += 1
        
        # Loop at end
        if self.frame_number >= self.total_frames:
            self.frame_number = 0
        
        # Update display
        self._update_frame_display()
        
        # Update timeline
        if self.timeline:
            self.timeline.set(self.frame_number)
        
        # Schedule next frame - use actual FPS timing
        if self.preview_frame and self.is_playing:
            frame_time = 1000.0 / self.fps  # milliseconds per frame
            delay = max(1, int(frame_time))
            self.timer_id = self.preview_frame.after(delay, self._play_loop)
    
    def pause(self):
        """Pause playback."""
        self.is_playing = False
        self._stop_event.set()
        
        if self.play_btn:
            self.play_btn.configure(text="▶ Play")
        
        if self.timer_id:
            try:
                self.preview_frame.after_cancel(self.timer_id)
            except:
                pass
            self.timer_id = None
    
    def seek(self, frame_number: int):
        """Seek to frame."""
        if not self.loader.cap and not self.loader.frame_buffer:
            return
        
        frame_number = max(0, min(frame_number, self.total_frames - 1))
        self.frame_number = frame_number
        self._update_frame_display()
        
        if self.timeline:
            self.timeline.set(frame_number)
    
    def seek_to_position(self, position: float):
        """Seek to position (0.0 to 1.0)."""
        if self.total_frames == 0:
            return
        frame = int(position * self.total_frames)
        self.seek(frame)
    
    def step_forward(self):
        """Step forward 5 seconds."""
        self.pause()
        skip_frames = int(self.fps * 5)
        self.frame_number = min(self.frame_number + skip_frames, self.total_frames - 1)
        self._update_frame_display()
        if self.timeline:
            self.timeline.set(self.frame_number)
    
    def step_backward(self):
        """Step backward 5 seconds."""
        self.pause()
        skip_frames = int(self.fps * 5)
        self.frame_number = max(self.frame_number - skip_frames, 0)
        self._update_frame_display()
        if self.timeline:
            self.timeline.set(self.frame_number)
    
    def close(self):
        """Stop and close video."""
        self.pause()
        if self.loader:
            self.loader.close()
        if self.display_label:
            self.display_label.configure(image=None, text="")


class VideoQueueManager:
    """Manage video queue."""
    
    def __init__(self):
        self.queue = []
        self.current_index = -1
    
    def add(self, paths):
        for path in paths:
            if is_supported_format(path) and path not in self.queue:
                self.queue.append(path)
        
        if self.current_index < 0 and self.queue:
            self.current_index = 0
    
    def clear(self):
        self.queue = []
        self.current_index = -1
    
    def get_current(self):
        if 0 <= self.current_index < len(self.queue):
            return self.queue[self.current_index]
        return None
    
    def next(self):
        if self.queue:
            self.current_index = (self.current_index + 1) % len(self.queue)
            return self.get_current()
        return None
    
    def previous(self):
        if self.queue:
            self.current_index = (self.current_index - 1) % len(self.queue)
            return self.get_current()
        return None
    
    def count(self):
        return len(self.queue)


def is_supported_format(path: str) -> bool:
    """Check if file is supported video format."""
    supported = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v', '.flv', '.wmv']
    return any(path.lower().endswith(ext) for ext in supported)


def format_video_info(info: Dict) -> str:
    """Format video info as string."""
    if not info:
        return "No video"
    
    size_mb = info.get('file_size_mb', 0)
    duration = info.get('duration', 0)
    
    return f"{info.get('filename', '?')} | {info.get('resolution', '?')} | {size_mb:.1f} MB | {duration:.1f}s"