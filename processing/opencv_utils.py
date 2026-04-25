"""
opencv_utils.py: Frame extraction and overlay utilities using OpenCV.

Key Concepts:
- OpenCV: Open Source Computer Vision Library for image/video processing.
- Frame Extraction: Reading individual frames from a video file.
- Overlay: Drawing graphics (e.g., bounding boxes, masks) on frames for visualization.
- Wrapper: Python functions/classes that simplify OpenCV usage.

Why is this important?
- Enables manipulation and analysis of video frames for AI processing.
- Provides tools for visual debugging and preview in the GUI.
"""

import cv2

class OpenCVUtils:
    """
    Utility class for OpenCV-based frame extraction and overlays.
    """
    def __init__(self, logger):
        self.logger = logger

    def extract_frames(self, video_path):
        """
        Extract all frames from a video file.
        Args:
            video_path (str): Path to the video file.
        Returns:
            list: List of frames (as numpy arrays).
        """
        self.logger.info(f"Extracting frames from {video_path}")
        cap = cv2.VideoCapture(video_path)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames

    def draw_overlay(self, frame, bbox=None, mask=None):
        """
        Draw overlays (bounding box, mask) on a frame.
        Args:
            frame (np.ndarray): Image array.
            bbox (tuple): Bounding box (x, y, w, h).
            mask (np.ndarray): Segmentation mask.
        Returns:
            np.ndarray: Frame with overlays.
        """
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        if mask is not None:
            frame[mask > 0] = (0, 255, 255)  # Example: yellow mask
        return frame
