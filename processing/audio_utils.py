"""
audio_utils.py: Audio normalization and silence removal utilities.

Key Concepts:
- Audio Normalization: Adjusting audio levels for consistent loudness.
- Silence Removal: Trimming silent sections from audio (e.g., at the start).
- Wrapper: Python functions/classes that use FFmpeg or other libraries for audio processing.

Why is this important?
- Ensures professional, platform-ready audio quality.
- Removes unwanted silence for better viewer engagement.
"""

import subprocess

class AudioUtils:
    """
    Utility class for audio normalization and silence removal.
    """
    def __init__(self, logger):
        self.logger = logger

    def normalize_audio(self, input_path, output_path):
        """
        Normalize audio using FFmpeg's loudnorm filter.
        Args:
            input_path (str): Path to input audio/video.
            output_path (str): Path to output audio/video.
        """
        cmd = [
            'ffmpeg', '-i', input_path, '-af', 'loudnorm', output_path
        ]
        self.logger.info(f"Normalizing audio: {' '.join(cmd)}")
        subprocess.run(cmd)

    def remove_silence(self, input_path, output_path):
        """
        Remove silence from the beginning of audio using FFmpeg's silenceremove filter.
        Args:
            input_path (str): Path to input audio/video.
            output_path (str): Path to output audio/video.
        """
        cmd = [
            'ffmpeg', '-i', input_path, '-af', 'silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB', output_path
        ]
        self.logger.info(f"Removing silence: {' '.join(cmd)}")
        subprocess.run(cmd)
