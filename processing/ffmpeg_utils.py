"""
ffmpeg_utils.py: GPU-accelerated video/audio processing utilities.

Key Concepts:
- FFmpeg: Industry-standard command-line tool for video/audio processing (transcoding, filtering, encoding).
- GPU Acceleration: Using hardware encoders (NVIDIA NVENC, Intel QuickSync, AMD VCE) for faster processing.
- Wrapper: A Python function/class that calls FFmpeg commands, making them easier to use in code.

Why is this important?
- Enables high-performance video processing for large files and batch jobs.
- Abstracts complex FFmpeg commands into reusable Python functions.
- Essential for both desktop and cloud/SaaS scalability.
"""

import subprocess

class FFmpegUtils:
    """
    Utility class for FFmpeg-based video/audio processing.
    """
    def __init__(self, logger):
        self.logger = logger

    def run_ffmpeg(self, cmd_args):
        """
        Run an FFmpeg command with logging.
        Args:
            cmd_args (list): List of command-line arguments for FFmpeg.
        Returns:
            int: Return code from FFmpeg.
        """
        self.logger.info(f"Running FFmpeg: {' '.join(cmd_args)}")
        result = subprocess.run(cmd_args, capture_output=True)
        if result.returncode != 0:
            self.logger.error(result.stderr.decode())
        return result.returncode

    def encode_with_gpu(self, input_path, output_path, codec='h264_nvenc'):
        """
        Example: Encode video using GPU acceleration.
        Args:
            input_path (str): Path to input video.
            output_path (str): Path to output video.
            codec (str): GPU codec (default: NVIDIA NVENC).
        """
        cmd = [
            'ffmpeg', '-hwaccel', 'cuda', '-i', input_path,
            '-c:v', codec, output_path
        ]
        return self.run_ffmpeg(cmd)
