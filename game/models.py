"""Data models for the AI Quiz Game."""

from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    """Represents a quiz question with multiple choices."""
    id: str
    category: str
    difficulty: str
    prompt: str
    choices: List[str]
    answer_index: int
    hint: str


@dataclass
class Result:
    """Represents a quiz session result."""
    player: str
    score: float
    total: int
    streak_max: int
    seconds: float
    category: str
    timestamp: str
    hints_used: int = 0
