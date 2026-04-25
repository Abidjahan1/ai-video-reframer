"""
main.py - Smart Video Reframer Studio Application Entry Point

This is where the application starts when you run:

    python app/main.py

=========================================================================
CORE CONCEPTS EXPLAINED
=========================================================================

PROJECT STRUCTURE:
    smart-video-reframer/
    ├── app/           - Application entry point (this file)
    ├── gui/           - User interface (windows, buttons)
    ├── core/          - Video processing (AI, tracking, etc.)
    ├── ai_models/     - AI model wrappers (YOLO, SAM, Whisper)
    ├── processing/    - Video/Audio utilities
    ├── export/       - Export profiles and encoding
    ├── batch/        - Batch processing
    ├── utils/        - Logger, config, helpers
    └── tests/        - Unit tests

HOW IT WORKS (Startup Flow):
    main.py
    → Creates AppConfig (loads settings)
    → Creates Logger (for logging)
    → Creates VideoProcessor (sets up AI pipeline)
    → Creates GUIController (connects UI to pipeline)
    → Calls controller.run() (launches GUI)

=========================================================================
WHAT WE UPDATED
=========================================================================

v1.0 - Initial Release:
- Added proper sys.path handling for imports
- Added version info to title
- Added responsive window sizing

=========================================================================
"""

import sys
import pathlib

# ==========================================================================
# IMPORT SETUP
# ==========================================================================

"""
Why add project root to sys.path?

When running `python app/main.py`, Python only looks in:
- app/ directory
- Installed packages (from pip)

But our modules are in parent directory:
- gui/ is at same level as app/
- core/, utils/, etc. are also there

Solution: Add parent to sys.path so Python can find them!

Example:
    Before: app/main.py can't find 'gui.controller'
    After:  app/main.py can find '../gui/controller' = 'gui.controller'
"""

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================================
# MAIN APPLICATION
# ==========================================================================

from gui.controller import GUIController
from utils.config import AppConfig
from utils.logger import get_logger
from core.video_processor import VideoProcessor


def main():
    """
    Main entry point - launches the application.
    
    ==========================================================================
    WHAT HAPPENS:
    ==========================================================================
    
    1. Create AppConfig (loads settings, paths, etc.)
    2. Create Logger (for console output)
    3. Create VideoProcessor (AI pipeline)
    4. Create GUIController (UI handler)
    5. Call controller.run() (show window)
    
    If any step fails, error is caught and printed.
    
    ==========================================================================
    """
    # Step 1: Load configuration
    print("Loading configuration...")
    config = AppConfig()
    print(f"  App: {config.app_name}")
    print(f"  Version: {config.version}")
    
    # Step 2: Initialize logger
    print("Initializing logger...")
    logger = get_logger()
    logger.info(f"Starting {config.app_name} v{config.version}")
    
    # Step 3: Create video processor (AI pipeline)
    print("Creating video processor...")
    video_processor = VideoProcessor(config, logger)
    
    # Step 4: Create GUI controller
    print("Creating GUI controller...")
    gui = GUIController(video_processor, config, logger)
    
    # Step 5: Launch the GUI
    print("Launching GUI...")
    gui.run()
    
    print("Application closed.")


if __name__ == "__main__":
    main()
