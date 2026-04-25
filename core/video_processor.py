"""
VideoProcessor: Core pipeline orchestrator for Smart Video Reframer Studio.

This class demonstrates OOP (Object-Oriented Programming) principles:
- Encapsulation: Groups related methods/data for video processing.
- Modularity: Can be extended with more pipeline stages.
- Dependency Injection: Receives config/logger for flexibility/testing.

Technical Terms:
- Pipeline: A sequence of processing steps (scene detection, tracking, etc.).
- Orchestrator: A class that manages and coordinates other components.

AI Pipeline Modules:
- SceneDetector: Detects scene boundaries using PySceneDetect.
- SubjectTracker: Detects and tracks the main subject using YOLO, SAM, Optical Flow, MediaPipe.
- BackgroundGenerator: Creates cinematic backgrounds for aspect ratio conversion.
- SubtitleGenerator: Generates subtitles using Whisper.
- ReframingEngine: Calculates optimal crop and camera motion.

Each module is a class with a clear interface, making the system modular and easy to extend or test.
"""


# Import all pipeline modules
from core.scene_detector import SceneDetector
from core.subject_tracker import SubjectTracker
from core.background_generator import BackgroundGenerator
from core.subtitle_generator import SubtitleGenerator

from core.reframing_engine import ReframingEngine
from core.export_engine import ExportEngine
from core.batch_manager import BatchManager
from utils.performance_mode import get_performance_mode, auto_detect_mode

class VideoProcessor:
    """
    The VideoProcessor class orchestrates the entire AI video processing pipeline.
    It composes all core modules as class attributes, demonstrating OOP composition.

    Why composition?
    - Each module (SceneDetector, SubjectTracker, etc.) is a separate class.
    - VideoProcessor creates and manages these modules, calling their methods as needed.
    - This makes the system modular, testable, and easy to extend (e.g., swap out SubjectTracker for a new version).

    ---
    # LEARNING & CAREER VISION
    By understanding and building this architecture, you gain:
    - Deep knowledge of OOP, modular design, and scalable AI pipelines
    - Hands-on experience with video, audio, and AI processing tools
    - The ability to explain, extend, and maintain complex systems
    - Skills valued for roles such as:
        * AI Solution Architect
        * AI Engineer
        * AI Architect
        * Automation Architect
        * AI Software Engineer
    You will be able to:
    - Train others on this architecture
    - Confidently modify and scale the system for new requirements
    - Lead technical discussions and design reviews
    ---
    """

    def __init__(self, config, logger):
        """
        Initialize the video processor and all pipeline modules.
        Args:
            config (AppConfig): Application configuration object.
            logger (Logger): Logger for status and debugging.
        """
        self.config = config
        self.logger = logger

        # Auto-detect or load performance mode
        self.performance_mode = get_performance_mode()
        if self.performance_mode == 'auto':
            self.performance_mode = auto_detect_mode()
        logger.info(f"Performance mode: {self.performance_mode}")

        # Initialize all pipeline modules (composition)
        self.scene_detector = SceneDetector(config, logger)
        self.subject_tracker = SubjectTracker(config, logger)
        self.background_generator = BackgroundGenerator(config, logger)
        self.subtitle_generator = SubtitleGenerator(config, logger)
        self.reframing_engine = ReframingEngine(config, logger)
        self.export_engine = ExportEngine(config, logger)
        self.batch_manager = BatchManager(config, logger)

        self.logger.info("VideoProcessor initialized with all pipeline modules.")

    def process_video(self, video_path):
        """
        Main method to process a video through the AI pipeline.
        This is a high-level overview; each step will be implemented in detail later.

        Args:
            video_path (str): Path to the input video file.
        """
        self.logger.info(f"Processing video: {video_path}")

        # 1. Scene Detection
        scenes = self.scene_detector.detect_scenes(video_path)
        self.logger.info(f"Detected {len(scenes)} scenes.")

        # 2. For each scene, process further (stubbed for now)
        for scene in scenes:
            # 2a. Subject Tracking (stub: pass empty frames list)
            subject_tracks = self.subject_tracker.track_subject([])
            # 2b. Background Generation (stub: pass None)
            background = self.background_generator.generate_background(None)
            # 2c. Reframing (stub: pass empty frames and subject_tracks)
            reframed_frames = self.reframing_engine.reframe([], subject_tracks)
            # 2d. Subtitle Generation (stub: pass empty audio path)
            subtitles = self.subtitle_generator.generate_subtitles("")
            # 2e. (Future) Export reframed video and subtitles
            self.logger.info("Processed scene (pipeline steps stubbed)")

        self.logger.info("Video processing complete (pipeline steps stubbed)")
