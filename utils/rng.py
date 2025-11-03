"""Random number generator utilities."""

import random
from typing import Optional


def get_rng(seed: Optional[int] = None) -> random.Random:
    """Return a Random instance for reproducible runs.

    Args:
        seed: Optional seed for reproducibility.

    Returns:
        A random.Random instance.
    """
    rng = random.Random(seed)
    return rng
