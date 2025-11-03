"""Text formatting utilities."""

import textwrap


def wrap(s: str, width: int = 80) -> str:
    """Wrap text to a specified width for clean console layout.

    Args:
        s: The string to wrap.
        width: The maximum line width (default: 80).

    Returns:
        The wrapped text as a single string.
    """
    return textwrap.fill(s, width=width)
