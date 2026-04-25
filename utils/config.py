"""
AppConfig: Centralized configuration for the application.

Why use a config class?
- Keeps settings in one place for easy management.
- Makes code more maintainable and testable.
- Can be extended to load from files or environment variables.
"""

import os
from pathlib import Path


class AppConfig:
    def __init__(self):
        """
        Initialize default configuration values.
        """
        self.app_name = "Smart Video Reframer Studio"
        self.version = "1.0.0"
        
        # Project paths
        self.project_root = Path(__file__).resolve().parents[1]
        self.models_dir = self.project_root / "models"
        self.output_dir = self.project_root / "output"
        self.temp_dir = self.project_root / "temp"
        
        # Ensure directories exist
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        
        # Video settings
        self.supported_formats = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
        self.max_video_size_mb = 2000
        
        # Export profiles
        self.export_profiles = {
            "youtube_long": {"width": 1920, "height": 1080, "fps": 30, "bitrate": "8M"},
            "youtube_shorts": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "8M"},
            "tiktok": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "8M"},
            "facebook_reels": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "8M"},
            "instagram_reels": {"width": 1080, "height": 1920, "fps": 30, "bitrate": "8M"},
        }
        
        # Aspect ratios
        self.aspect_ratios = {
            "9:16": (9, 16),
            "16:9": (16, 9),
            "1:1": (1, 1),
            "4:5": (4, 5),
            "4:3": (4, 3),
        }
        
        # AI Model settings
        self.yolo_model = "yolov8n.pt"
        self.sam_model = "sam_vit_h_4b8939.pth"
        self.whisper_model = "base"
        
        # Processing settings
        self.scene_threshold = 30.0
        self.tracking_confidence = 0.5
        self.background_blur_radius = 25
        self.auto_zoom_duration = 3.0
        
        # Performance settings
        self.gpu_acceleration = True
        self.batch_size = 4
        self.worker_threads = 2
        
        # GUI settings
        self.window_width = 1400
        self.window_height = 900
        self.theme = "dark"
        self.accent_color = "#00B4D8"
        
        # Logging
        self.log_level = "INFO"
        self.log_file = self.project_root / "logs" / "app.log"
        
        # FFmpeg path (auto-detect)
        self.ffmpeg_path = "ffmpeg"
        self.ffprobe_path = "ffprobe"