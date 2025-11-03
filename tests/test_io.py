"""Basic unit tests for I/O operations."""

import json
import pytest
from pathlib import Path
from game.models import Question, Result
from game.io_manager import load_questions, save_result


def test_load_questions_general():
    """Test loading questions from general category."""
    questions = load_questions("general")

    assert len(questions) > 0
    assert all(isinstance(q, Question) for q in questions)
    assert all(q.category == "general" for q in questions)


def test_load_questions_science():
    """Test loading questions from science category."""
    questions = load_questions("science")

    assert len(questions) > 0
    assert all(isinstance(q, Question) for q in questions)
    assert all(q.category == "science" for q in questions)


def test_load_questions_unknown_category():
    """Test that loading unknown category raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_questions("nonexistent")


def test_load_questions_structure():
    """Test that loaded questions have correct structure."""
    questions = load_questions("general")

    q = questions[0]
    assert hasattr(q, 'id')
    assert hasattr(q, 'category')
    assert hasattr(q, 'difficulty')
    assert hasattr(q, 'prompt')
    assert hasattr(q, 'choices')
    assert hasattr(q, 'answer_index')
    assert hasattr(q, 'hint')
    assert len(q.choices) == 4
    assert 0 <= q.answer_index < len(q.choices)


def test_save_result(tmp_path, monkeypatch):
    """Test saving a result to the leaderboard."""
    # Create a temporary leaderboard file
    temp_leaderboard = tmp_path / "test_leaderboard.jsonl"

    # Mock the config
    def mock_load_config():
        return {
            "data_folder": Path("data"),
            "leaderboard_path": temp_leaderboard
        }

    monkeypatch.setattr("game.io_manager.load_config", mock_load_config)

    result = Result(
        player="TestPlayer",
        score=8,
        total=10,
        streak_max=5,
        seconds=45.5,
        category="test",
        timestamp="2025-11-03T12:00:00Z"
    )

    save_result(result)

    # Verify the file was created and contains the result
    assert temp_leaderboard.exists()

    with open(temp_leaderboard, 'r') as f:
        line = f.readline()
        data = json.loads(line)
        assert data["player"] == "TestPlayer"
        assert data["score"] == 8
        assert data["total"] == 10
        assert data["streak_max"] == 5
        assert data["seconds"] == 45.5
        assert data["category"] == "test"
