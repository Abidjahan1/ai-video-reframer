"""
encoder.py: FFmpeg/NVENC/QuickSync/AMD VCE encoding wrappers.

Key Concepts:
- Encoder: Software or hardware that compresses video into a specific format (codec).
- FFmpeg: Used to invoke hardware encoders (NVIDIA NVENC, Intel QuickSync, AMD VCE) for fast, high-quality export.
- Wrapper: Python function/class that builds and runs the correct FFmpeg command for the chosen export profile.

How to use:
- Call `encode_video` with input/output paths and a profile from profiles.py.
- Handles all command construction and error logging.
"""

import subprocess
from utils.performance_mode import get_performance_mode

class Encoder:
    """
    Encoder class for hardware-accelerated video export.
    """
    def __init__(self, logger):
        self.logger = logger
        self.performance_mode = get_performance_mode()

    def encode_video(self, input_path, output_path, profile):
        """
        Encode video using the specified export profile.
        Args:
            input_path (str): Path to input video.
            output_path (str): Path to output video.
            profile (dict): Export profile from profiles.py.
        """
        # Select codec based on performance mode
        codec = profile['codec']
        if self.performance_mode == 'cpu':
            codec = 'libx264'  # CPU fallback
        cmd = [
            'ffmpeg', '-i', input_path,
            '-c:v', codec,
            '-b:v', profile['bitrate'],
            '-s', f"{profile['resolution'][0]}x{profile['resolution'][1]}",
            '-aspect', profile['aspect_ratio'],
            '-y', output_path
        ]
        if self.performance_mode == 'gpu':
            cmd.insert(1, '-hwaccel')
            cmd.insert(2, 'cuda')
        self.logger.info(f"Encoding video: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            self.logger.error(result.stderr.decode())
        return result.returncode
