"""
monitor.py: Batch job progress tracking and reporting.

Key Concepts:
- Progress Monitoring: Tracking the status of each job (pending, processing, done, error).
- Reporting: Providing real-time feedback to the user (GUI, logs, etc.).
- OOP: Encapsulates monitoring logic for modularity and future cloud dashboards.

How to use:
- Register jobs with `register_job`.
- Update job status with `update_status`.
- Query job status with `get_status` or `get_all_statuses`.
"""

class BatchMonitor:
    """
    Tracks and reports the status of batch jobs.
    """
    def __init__(self):
        self._statuses = {}

    def register_job(self, job_id, job_info):
        """
        Register a new job for monitoring.
        Args:
            job_id (str): Unique job identifier.
            job_info (dict): Job details.
        """
        self._statuses[job_id] = {'info': job_info, 'status': 'pending'}

    def update_status(self, job_id, status):
        """
        Update the status of a job.
        Args:
            job_id (str): Unique job identifier.
            status (str): New status ('pending', 'processing', 'done', 'error').
        """
        if job_id in self._statuses:
            self._statuses[job_id]['status'] = status

    def get_status(self, job_id):
        """
        Get the status of a specific job.
        Args:
            job_id (str): Unique job identifier.
        Returns:
            str: Current status.
        """
        return self._statuses.get(job_id, {}).get('status', 'unknown')

    def get_all_statuses(self):
        """
        Get the statuses of all jobs.
        Returns:
            dict: Mapping of job_id to status info.
        """
        return self._statuses.copy()
