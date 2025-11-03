"""Configuration settings for the AI Quiz Game."""

from pathlib import Path


def load_config():
    """Return default configuration settings.

    Returns:
        dict: Configuration dictionary with data_folder and leaderboard_path.
    """
    base_dir = Path(__file__).parent.parent
    return {
        "data_folder": base_dir / "data",
        "leaderboard_path": base_dir / "leaderboard.jsonl",
        "default_limit": 10,
        "default_category": "general"
    }
