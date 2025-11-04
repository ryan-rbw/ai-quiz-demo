"""Basic unit tests for leaderboard functionality."""

import json
import pytest
from pathlib import Path
from game.models import Result
from game.leaderboard import top_n, format_table


def test_top_n_sorting(tmp_path, monkeypatch):
    """Test that top_n sorts by score and time."""
    temp_leaderboard = tmp_path / "test_leaderboard.jsonl"

    # Create test data
    results = [
        {"player": "Player1", "score": 5, "total": 10, "streak_max": 3, "seconds": 30.0, "category": "test", "timestamp": "2025-11-03T10:00:00Z"},
        {"player": "Player2", "score": 8, "total": 10, "streak_max": 5, "seconds": 45.0, "category": "test", "timestamp": "2025-11-03T11:00:00Z"},
        {"player": "Player3", "score": 8, "total": 10, "streak_max": 4, "seconds": 40.0, "category": "test", "timestamp": "2025-11-03T12:00:00Z"},
    ]

    with open(temp_leaderboard, 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

    # Mock the config
    def mock_load_config():
        return {
            "data_folder": Path("data"),
            "leaderboard_path": temp_leaderboard
        }

    monkeypatch.setattr("game.leaderboard.load_config", mock_load_config)

    top_results = top_n(10)

    # Player3 should be first (score 8, time 40s)
    # Player2 should be second (score 8, time 45s)
    # Player1 should be third (score 5)
    assert len(top_results) == 3
    assert top_results[0].player == "Player3"
    assert top_results[1].player == "Player2"
    assert top_results[2].player == "Player1"


def test_top_n_limit(tmp_path, monkeypatch):
    """Test that top_n respects the limit."""
    temp_leaderboard = tmp_path / "test_leaderboard.jsonl"

    results = [
        {"player": f"Player{i}", "score": i, "total": 10, "streak_max": i, "seconds": 30.0, "category": "test", "timestamp": "2025-11-03T10:00:00Z"}
        for i in range(5)
    ]

    with open(temp_leaderboard, 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

    def mock_load_config():
        return {
            "data_folder": Path("data"),
            "leaderboard_path": temp_leaderboard
        }

    monkeypatch.setattr("game.leaderboard.load_config", mock_load_config)

    top_results = top_n(3)
    assert len(top_results) == 3


def test_top_n_empty_leaderboard(tmp_path, monkeypatch):
    """Test that top_n handles empty leaderboard."""
    temp_leaderboard = tmp_path / "nonexistent.jsonl"

    def mock_load_config():
        return {
            "data_folder": Path("data"),
            "leaderboard_path": temp_leaderboard
        }

    monkeypatch.setattr("game.leaderboard.load_config", mock_load_config)

    top_results = top_n(10)
    assert len(top_results) == 0


def test_format_table_with_results():
    """Test formatting a table with results."""
    results = [
        Result("Player1", 8.0, 10, 5, 45.0, "test", "2025-11-03T10:00:00Z", hints_used=0),
        Result("Player2", 6.0, 10, 3, 50.0, "test", "2025-11-03T11:00:00Z", hints_used=2),
    ]

    table = format_table(results)

    assert "Player1" in table
    assert "Player2" in table
    assert "8.0/10" in table
    assert "6.0/10" in table
    # Check that lines are not too wide (under 80 columns)
    for line in table.split('\n'):
        assert len(line) <= 80


def test_format_table_empty():
    """Test formatting an empty table."""
    table = format_table([])
    assert "No results yet!" in table


def test_top_n_with_hints(tmp_path, monkeypatch):
    """Test that top_n handles results with hints_used field."""
    temp_leaderboard = tmp_path / "test_leaderboard.jsonl"

    results = [
        {"player": "Player1", "score": 8.5, "total": 10, "streak_max": 5, "seconds": 40.0, "category": "test", "timestamp": "2025-11-03T10:00:00Z", "hints_used": 1},
        {"player": "Player2", "score": 9.0, "total": 10, "streak_max": 6, "seconds": 45.0, "category": "test", "timestamp": "2025-11-03T11:00:00Z", "hints_used": 2},
    ]

    with open(temp_leaderboard, 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

    def mock_load_config():
        return {
            "data_folder": Path("data"),
            "leaderboard_path": temp_leaderboard
        }

    monkeypatch.setattr("game.leaderboard.load_config", mock_load_config)

    top_results = top_n(10)

    assert len(top_results) == 2
    assert top_results[0].score == 9.0
    assert top_results[0].hints_used == 2
    assert top_results[1].score == 8.5
    assert top_results[1].hints_used == 1


def test_top_n_backward_compatibility(tmp_path, monkeypatch):
    """Test that top_n handles old results without hints_used field."""
    temp_leaderboard = tmp_path / "test_leaderboard.jsonl"

    # Old format without hints_used
    results = [
        {"player": "OldPlayer", "score": 7, "total": 10, "streak_max": 4, "seconds": 35.0, "category": "test", "timestamp": "2025-11-03T09:00:00Z"},
    ]

    with open(temp_leaderboard, 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

    def mock_load_config():
        return {
            "data_folder": Path("data"),
            "leaderboard_path": temp_leaderboard
        }

    monkeypatch.setattr("game.leaderboard.load_config", mock_load_config)

    top_results = top_n(10)

    assert len(top_results) == 1
    assert top_results[0].hints_used == 0  # Default value
