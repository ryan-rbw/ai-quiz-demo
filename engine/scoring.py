"""Scoring logic for quiz answers."""

from game.models import Question


def score_answer(question: Question, user_choice: int, hint_used: bool = False) -> tuple[bool, float]:
    """Score a user's answer to a question.

    Args:
        question: The Question object.
        user_choice: The index of the user's chosen answer.
        hint_used: Whether the user used a hint for this question.

    Returns:
        Tuple of (is_correct, points). Points are 1.0 for correct answer,
        0.5 if hint was used and answer is correct, 0 if incorrect.
    """
    correct = user_choice == question.answer_index

    if not correct:
        points = 0.0
    elif hint_used:
        points = 0.5
    else:
        points = 1.0

    return correct, points
