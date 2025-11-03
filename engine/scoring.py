"""Scoring logic for quiz answers.

INTENTIONAL ISSUE: Missing type hints for demo purposes.
"""

from game.models import Question


def score_answer(question, user_choice):
    """Score a user's answer to a question.

    Args:
        question: The Question object.
        user_choice: The index of the user's chosen answer.

    Returns:
        Tuple of (is_correct, points).
    """
    correct = user_choice == question.answer_index
    points = 1 if correct else 0
    return correct, points
