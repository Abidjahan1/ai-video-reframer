"""
hardware.py: Hardware detection utilities for Smart Video Reframer Studio.

Key Concepts:
- Hardware Detection: Identifying available hardware (GPU, CPU, encoders) at runtime.
- CUDA: NVIDIA's GPU computing platform, used by PyTorch and FFmpeg for acceleration.
- Cross-Platform: Works on Windows, Mac, Linux.

How to use:
- Call `detect_gpu()` at startup to check for GPU availability.
- Use the result to select the best backend for AI models and encoding.
"""

def detect_gpu():
    """
    Detect if a compatible GPU is available (NVIDIA CUDA, Intel, AMD).
    Returns:
        dict: { 'cuda': bool, 'cuda_name': str or None, 'ffmpeg_nvenc': bool }
    """
    cuda_available = False
    cuda_name = None
    ffmpeg_nvenc = False
    # Check PyTorch CUDA
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            cuda_name = torch.cuda.get_device_name(0)
    except ImportError:
        pass
    # Check FFmpeg NVENC
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-encoders'], capture_output=True, text=True)
        ffmpeg_nvenc = 'h264_nvenc' in result.stdout
    except Exception:
        pass
    return {
        'cuda': cuda_available,
        'cuda_name': cuda_name,
        'ffmpeg_nvenc': ffmpeg_nvenc
    }
