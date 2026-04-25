"""
color_utils.py: Dominant color detection and blending utilities.

Key Concepts:
- Dominant Color Detection: Finding the most prominent color(s) in an image (for background synthesis).
- Color Blending: Mixing colors for smooth transitions and cinematic backgrounds.
- OpenCV & NumPy: Used for image processing and color calculations.
- Wrapper: Python functions/classes for color analysis and manipulation.

Why is this important?
- Enables creation of visually appealing backgrounds for reframed videos.
- Supports advanced effects like color-matched blur and overlays.
"""

import cv2
import numpy as np

class ColorUtils:
    """
    Utility class for color detection and blending.
    """
    def __init__(self, logger):
        self.logger = logger

    def get_dominant_color(self, frame):
        """
        Find the dominant color in a frame using k-means clustering.
        Args:
            frame (np.ndarray): Image array.
        Returns:
            tuple: Dominant color (B, G, R).
        """
        self.logger.info("Detecting dominant color in frame")
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = img.reshape((-1, 3))
        img = np.float32(img)
        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 4
        _, labels, centers = cv2.kmeans(img, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        counts = np.bincount(labels.flatten())
        dominant = centers[np.argmax(counts)]
        return tuple(map(int, dominant))

    def blend_colors(self, color1, color2, alpha=0.5):
        """
        Blend two colors together.
        Args:
            color1 (tuple): First color (B, G, R).
            color2 (tuple): Second color (B, G, R).
            alpha (float): Blend ratio (0.0-1.0).
        Returns:
            tuple: Blended color.
        """
        blended = tuple([int(c1 * alpha + c2 * (1 - alpha)) for c1, c2 in zip(color1, color2)])
        return blended
