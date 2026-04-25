"""
performance_mode.py: Centralized logic for managing performance mode (auto/cpu/gpu) in Smart Video Reframer Studio.

Key Concepts:
- Centralized State: Keeps track of user-selected or auto-detected performance mode.
- Integration: Used by pipeline, models, and encoders to select backend.

How to use:
- Call `get_performance_mode()` to get the current mode ('auto', 'cpu', or 'gpu').
- Call `set_performance_mode(mode)` to update the mode (from GUI or config).
- Call `auto_detect_mode()` to set mode based on hardware detection.
"""

from utils.hardware import detect_gpu

# Global state (could be moved to AppConfig)
PERFORMANCE_MODE = 'auto'  # 'auto', 'cpu', or 'gpu'


def set_performance_mode(mode):
    global PERFORMANCE_MODE
    assert mode in ('auto', 'cpu', 'gpu')
    PERFORMANCE_MODE = mode


def get_performance_mode():
    return PERFORMANCE_MODE


def auto_detect_mode():
    """
    Detect hardware and set mode to 'gpu' if available, else 'cpu'.
    """
    global PERFORMANCE_MODE
    hw = detect_gpu()
    if hw['cuda'] or hw['ffmpeg_nvenc']:
        PERFORMANCE_MODE = 'gpu'
    else:
        PERFORMANCE_MODE = 'cpu'
    return PERFORMANCE_MODE
