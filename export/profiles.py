"""
profiles.py: Platform-specific export profiles for Smart Video Reframer Studio.

Key Concepts:
- Export Profile: A set of settings (resolution, aspect ratio, codec, bitrate, etc.) optimized for a specific platform (YouTube, TikTok, Instagram, etc.).
- Why profiles? Each platform has unique requirements for video uploads. Profiles ensure compatibility and best quality.
- Dictionary/Data Structure: Profiles are stored as Python dictionaries for easy access and extension.

How to use:
- Select a profile by name (e.g., 'youtube_long', 'tiktok') and pass its settings to the export engine.
- Easily add or modify profiles as platforms evolve.
"""

EXPORT_PROFILES = {
    'youtube_long': {
        'resolution': (1920, 1080),
        'aspect_ratio': '16:9',
        'codec': 'h264_nvenc',
        'bitrate': '8M',
        'container': 'mp4',
        'description': 'YouTube Long Video (16:9, 1920x1080)'
    },
    'youtube_shorts': {
        'resolution': (1080, 1920),
        'aspect_ratio': '9:16',
        'codec': 'h264_nvenc',
        'bitrate': '6M',
        'container': 'mp4',
        'description': 'YouTube Shorts (9:16, 1080x1920)'
    },
    'tiktok': {
        'resolution': (1080, 1920),
        'aspect_ratio': '9:16',
        'codec': 'h264_nvenc',
        'bitrate': '6M',
        'container': 'mp4',
        'description': 'TikTok (9:16, 1080x1920)'
    },
    'instagram_reels': {
        'resolution': (1080, 1920),
        'aspect_ratio': '9:16',
        'codec': 'h264_nvenc',
        'bitrate': '6M',
        'container': 'mp4',
        'description': 'Instagram Reels (9:16, 1080x1920)'
    },
    'facebook_reels': {
        'resolution': (1080, 1920),
        'aspect_ratio': '9:16',
        'codec': 'h264_nvenc',
        'bitrate': '6M',
        'container': 'mp4',
        'description': 'Facebook Reels (9:16, 1080x1920)'
    },
}
