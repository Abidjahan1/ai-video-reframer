"""
Logger utility for Smart Video Reframer Studio.

Why use a logger?
- Centralizes all status and error messages.
- Helps with debugging and monitoring.
- Can be extended to log to files, GUIs, or remote servers.

Technical Terms:
- Logger: An object that records messages about program execution.
"""

import logging

def get_logger():
    """
    Returns a configured logger instance.
    """
    logger = logging.getLogger("SmartVideoReframer")
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
