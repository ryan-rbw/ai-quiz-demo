"""File I/O operations for questions and results."""

import json
from pathlib import Path
from typing import List
from game.models import Question, Result
from game.config import load_config


def load_questions(category: str) -> List[Question]:
    config = load_config()
    data_folder = config["data_folder"]
    file_path = data_folder / f"questions_{category}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"No questions found for category: {category}")

    with open(file_path, 'r') as f:
        data = json.load(f)

    questions = []
    for item in data:
        questions.append(Question(
            id=item["id"],
            category=item["category"],
            difficulty=item["difficulty"],
            prompt=item["prompt"],
            choices=item["choices"],
            answer_index=item["answer_index"],
            hint=item.get("hint", "No hint available")
        ))

    return questions


def save_result(result: Result):
    config = load_config()
    leaderboard_path = config["leaderboard_path"]

    result_dict = {
        "player": result.player,
        "score": result.score,
        "total": result.total,
        "streak_max": result.streak_max,
        "seconds": result.seconds,
        "category": result.category,
        "timestamp": result.timestamp,
        "hints_used": result.hints_used
    }

    with open(leaderboard_path, 'a') as f:
        f.write(json.dumps(result_dict) + '\n')
