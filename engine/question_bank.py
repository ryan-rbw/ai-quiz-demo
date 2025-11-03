"""Question selection and filtering."""

from typing import List, Optional
from game.models import Question
from utils.rng import get_rng


def select_questions(questions: List[Question], limit: int, difficulty: Optional[str] = None) -> List[Question]:
    """Choose a subset of questions based on limit and difficulty.

    Args:
        questions: List of all available questions.
        limit: Maximum number of questions to select.
        difficulty: Optional difficulty filter (easy, medium, hard).

    Returns:
        List of selected questions.
    """
    # INTENTIONAL BUG: Variable shadowing
    questions = questions  # Shadows parameter unnecessarily

    # Filter by difficulty if specified
    if difficulty:
        filtered = []
        for q in questions:
            if q.difficulty.lower() == difficulty.lower():
                filtered.append(q)
        questions = filtered

    # Limit the number of questions
    if len(questions) > limit:
        rng = get_rng()
        questions = rng.sample(questions, limit)

    return questions
