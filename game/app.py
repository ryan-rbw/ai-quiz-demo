"""CLI entry point for the AI Quiz Game."""

import sys
from pathlib import Path
from typing import Optional
import typer
from game.config import load_config
from game.io_manager import load_questions, save_result
from game.leaderboard import top_n, format_table
from engine.question_bank import select_questions
from engine.quiz_engine import run_quiz


app = typer.Typer()


def get_available_categories():
    """Get list of available question categories from data folder."""
    config = load_config()
    data_folder = config["data_folder"]
    category_files = list(data_folder.glob("questions_*.json"))
    categories = [f.stem.replace("questions_", "") for f in category_files]
    return sorted(categories)


@app.command()
def main(
    category: str = typer.Option("general", "--category", "-c", help="Question category (general, science)"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of questions"),
    difficulty: Optional[str] = typer.Option(None, "--difficulty", "-d", help="Filter by difficulty (easy/medium/hard)"),
    hints: bool = typer.Option(False, "--hints", "-h", help="Enable hints (halves points when used)"),
    leaderboard: Optional[int] = typer.Option(None, "--leaderboard", "-b", help="Show top N scores and exit")
):
    """Run the AI Quiz Game.

    Examples:
        python -m game.app
        python -m game.app --category science --limit 5
        python -m game.app --hints
        python -m game.app --leaderboard 10
    """
    config = load_config()

    # Show leaderboard and exit if requested
    if leaderboard is not None:
        results = top_n(leaderboard)
        print(format_table(results))
        return

    # Load questions
    try:
        questions = load_questions(category)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        available = get_available_categories()
        print(f"Available categories: {', '.join(available)}")
        sys.exit(1)

    # Select questions based on filters
    selected = select_questions(questions, limit, difficulty)

    if not selected:
        print(f"No questions found matching your criteria.")
        sys.exit(1)

    # Run the quiz
    result = run_quiz(selected, hints_enabled=hints)

    # Save the result
    save_result(result)
    print("Your result has been saved to the leaderboard!")


if __name__ == "__main__":
    app()
