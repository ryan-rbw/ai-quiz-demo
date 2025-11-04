"""Leaderboard management and display."""

import json
from pathlib import Path
from typing import List
from game.models import Result
from game.config import load_config


def top_n(n: int) -> List[Result]:
    """Return the top n results sorted by score and time.

    Args:
        n: Number of top results to return.

    Returns:
        List of Result objects sorted by score (desc) and seconds (asc).
    """
    config = load_config()
    leaderboard_path = config["leaderboard_path"]

    if not Path(leaderboard_path).exists():
        return []

    results = []
    with open(leaderboard_path, 'r') as f:
        for line in f:
            data = json.loads(line.strip())
            results.append(Result(
                player=data["player"],
                score=data["score"],
                total=data["total"],
                streak_max=data["streak_max"],
                seconds=data["seconds"],
                category=data["category"],
                timestamp=data["timestamp"],
                hints_used=data.get("hints_used", 0)  # Default to 0 for old records
            ))

    # Sort by score descending, then by time ascending
    results.sort(key=lambda r: (-r.score, r.seconds))
    return results[:n]


def format_table(results: List[Result]) -> str:
    """Format results as a printable table.

    Args:
        results: List of Result objects.

    Returns:
        Formatted table string.
    """
    if not results:
        return "No results yet!"

    lines = []
    lines.append("=" * 78)
    lines.append(f"{'Rank':<6} {'Player':<15} {'Score':<10} {'Streak':<8} {'Time (s)':<10} {'Category':<12}")
    lines.append("=" * 78)

    for idx, result in enumerate(results, 1):
        score_display = f"{result.score}/{result.total}"
        lines.append(
            f"{idx:<6} {result.player:<15} {score_display:<10} {result.streak_max:<8} "
            f"{result.seconds:<10.1f} {result.category:<12}"
        )

    lines.append("=" * 78)
    return "\n".join(lines)
