"""Timer utilities for measuring session time."""

import time
from typing import Optional


class Timer:
    """Context manager for measuring elapsed time."""

    def __init__(self):
        """Initialize the timer."""
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.elapsed: float = 0.0

    def __enter__(self):
        """Start the timer."""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the timer."""
        self.end_time = time.time()
        if self.start_time:
            self.elapsed = self.end_time - self.start_time
        return False
