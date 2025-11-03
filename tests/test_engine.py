"""Basic unit tests for engine module."""

import pytest
from game.models import Question
from engine.scoring import score_answer
from engine.question_bank import select_questions


def test_score_answer_correct():
    """Test scoring a correct answer."""
    question = Question(
        id="TEST-001",
        category="test",
        difficulty="easy",
        prompt="Test question?",
        choices=["A", "B", "C", "D"],
        answer_index=2,
        hint="Test hint"
    )

    correct, points = score_answer(question, 2)
    assert correct is True
    assert points == 1


def test_score_answer_incorrect():
    """Test scoring an incorrect answer."""
    question = Question(
        id="TEST-002",
        category="test",
        difficulty="easy",
        prompt="Test question?",
        choices=["A", "B", "C", "D"],
        answer_index=1,
        hint="Test hint"
    )

    correct, points = score_answer(question, 3)
    assert correct is False
    assert points == 0


def test_select_questions_limit():
    """Test that select_questions respects the limit."""
    questions = [
        Question(f"Q{i}", "test", "easy", f"Question {i}", ["A", "B"], 0, "hint")
        for i in range(10)
    ]

    selected = select_questions(questions, limit=5)
    assert len(selected) == 5


def test_select_questions_difficulty_filter():
    """Test filtering by difficulty."""
    questions = [
        Question("Q1", "test", "easy", "Q1", ["A", "B"], 0, "hint"),
        Question("Q2", "test", "hard", "Q2", ["A", "B"], 0, "hint"),
        Question("Q3", "test", "easy", "Q3", ["A", "B"], 0, "hint"),
    ]

    selected = select_questions(questions, limit=10, difficulty="easy")
    assert len(selected) == 2
    assert all(q.difficulty == "easy" for q in selected)


def test_select_questions_no_filter():
    """Test selecting questions without difficulty filter."""
    questions = [
        Question(f"Q{i}", "test", "medium", f"Question {i}", ["A", "B"], 0, "hint")
        for i in range(3)
    ]

    selected = select_questions(questions, limit=10)
    assert len(selected) == 3
