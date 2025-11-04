"""Quiz engine for running interactive quiz sessions."""

import time
from datetime import datetime
from typing import List
from game.models import Question, Result
from engine.scoring import score_answer


def get_player_name() -> str:
    """Prompt for and return the player's name.

    Returns:
        The player's name, or "Anonymous" if no name provided.
    """
    player = input("Enter your name: ").strip()
    if not player:
        player = "Anonymous"
    return player


def display_question(question: Question, question_num: int, total: int) -> None:
    """Display a quiz question with its choices.

    Args:
        question: The Question object to display.
        question_num: Current question number (1-indexed).
        total: Total number of questions in the quiz.
    """
    print(f"\nQuestion {question_num}/{total}")
    print("-" * 60)
    print(f"Category: {question.category.upper()} | Difficulty: {question.difficulty.upper()}")
    print(f"\n{question.prompt}\n")

    for idx, choice in enumerate(question.choices):
        print(f"  {idx + 1}. {choice}")


def get_user_answer(num_choices: int, hints_enabled: bool = False, hint_text: str = None) -> tuple[int, bool]:
    """Prompt user for their answer choice with validation.

    Args:
        num_choices: Number of available choices.
        hints_enabled: Whether hints are enabled for this quiz.
        hint_text: The hint text to display if user requests it.

    Returns:
        Tuple of (zero-indexed choice, whether hint was requested).
    """
    hint_requested = False

    while True:
        try:
            if hints_enabled and not hint_requested:
                answer = input("\nYour answer (1-4, or 'h' for hint): ").strip().lower()
            else:
                answer = input("\nYour answer (1-4): ").strip()

            if hints_enabled and answer == 'h' and not hint_requested:
                hint_requested = True
                if hint_text:
                    print(f"\nHint: {hint_text}")
                continue

            user_choice = int(answer) - 1
            if 0 <= user_choice < num_choices:
                return user_choice, hint_requested
            else:
                print(f"Please enter a number between 1 and {num_choices}.")
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {num_choices}.")


def display_feedback(correct: bool, points: float, correct_answer: str = None) -> None:
    """Display feedback for the user's answer.

    Args:
        correct: Whether the answer was correct.
        points: Points earned for the answer.
        correct_answer: The correct answer text (shown if incorrect).
    """
    if correct:
        print(f"\n✓ Correct! +{points} points")
    else:
        print(f"\n✗ Wrong! The correct answer was: {correct_answer}")


def display_result_summary(result: Result) -> None:
    """Display the final quiz results.

    Args:
        result: The Result object containing quiz statistics.
    """
    print("\n" + "=" * 60)
    print("QUIZ COMPLETE!")
    print("=" * 60)
    print(f"Player: {result.player}")
    print(f"Score: {result.score}/{result.total} ({100*result.score/result.total:.1f}%)")
    print(f"Best Streak: {result.streak_max}")
    if result.hints_used > 0:
        print(f"Hints Used: {result.hints_used}")
    print(f"Time: {result.seconds:.1f} seconds")
    print("=" * 60 + "\n")


def run_quiz(questions: List[Question], hints_enabled: bool = False) -> Result:
    """Run an interactive quiz session.

    Args:
        questions: List of Question objects to ask the user.
        hints_enabled: Whether to allow users to request hints.

    Returns:
        Result object containing quiz statistics and score.
    """
    print("\n" + "=" * 60)
    print("WELCOME TO THE AI QUIZ GAME!")
    print("=" * 60 + "\n")

    player = get_player_name()

    score = 0.0
    total_questions = len(questions)
    streak = 0
    max_streak = 0
    hints_used = 0
    asked_ids = set()  # Use set for O(1) duplicate checking

    start_time = time.time()

    for i, question in enumerate(questions):
        # Skip duplicate questions using O(1) set lookup
        if question.id in asked_ids:
            continue

        asked_ids.add(question.id)

        # Display the question
        display_question(question, len(asked_ids), total_questions)

        # Get user's answer (and check if hint was requested)
        user_choice, hint_used = get_user_answer(len(question.choices), hints_enabled, question.hint)

        # Track hints used
        if hint_used:
            hints_used += 1

        # Score the answer
        correct, points = score_answer(question, user_choice, hint_used)

        # Update score and streak
        if correct:
            score += points
            streak += 1
            if streak > max_streak:
                max_streak = streak
            display_feedback(True, points)
        else:
            streak = 0
            correct_answer = question.choices[question.answer_index]
            display_feedback(False, points, correct_answer)

        # Brief delay between questions (yields CPU)
        time.sleep(0.5)

    end_time = time.time()
    elapsed = end_time - start_time

    # Create result
    result = Result(
        player=player,
        score=score,
        total=total_questions,
        streak_max=max_streak,
        seconds=elapsed,
        category=questions[0].category if questions else "general",
        timestamp=datetime.utcnow().isoformat() + "Z",
        hints_used=hints_used
    )

    # Display summary
    display_result_summary(result)

    return result
