"""
queue.py: Batch job queue management for Smart Video Reframer Studio.

Key Concepts:
- Queue: A data structure that holds tasks (jobs) to be processed in order (FIFO: First-In, First-Out).
- Job: A single video processing task (input file, export settings, etc.).
- Thread-Safety: Ensures the queue works correctly even if accessed by multiple threads (for parallel processing).
- OOP: Encapsulates queue logic for modularity and future scaling (e.g., cloud worker queues).

How to use:
- Add jobs to the queue with `add_job`.
- Retrieve jobs for processing with `get_next_job`.
- Check if the queue is empty with `is_empty`.
"""

import threading

class BatchQueue:
    """
    Thread-safe batch job queue.
    """
    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()

    def add_job(self, job):
        """
        Add a job to the queue.
        Args:
            job (dict): Job details (e.g., input file, export profile).
        """
        with self._lock:
            self._queue.append(job)

    def get_next_job(self):
        """
        Retrieve and remove the next job from the queue.
        Returns:
            dict or None: The next job, or None if queue is empty.
        """
        with self._lock:
            if self._queue:
                return self._queue.pop(0)
            return None

    def is_empty(self):
        """
        Check if the queue is empty.
        Returns:
            bool: True if empty, False otherwise.
        """
        with self._lock:
            return len(self._queue) == 0
