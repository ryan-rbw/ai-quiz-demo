"""Quiz engine with intentional inefficiencies for demo purposes."""

import json
import time
from datetime import datetime
from game.models import Question, Result
from game.config import load_config
from engine.scoring import score_answer


def run_quiz(questions):
    """Run a quiz session with intentional inefficiencies.

    INTENTIONAL ISSUES (for demo purposes):
    1. Repeated JSON file reads inside the loop
    2. O(n^2) duplicate checking for already asked questions
    3. Busy wait for fake delay between questions
    4. Mixed concerns in a single 80+ line function with poor naming
    """
    print("\n" + "="*60)
    print("WELCOME TO THE AI QUIZ GAME!")
    print("="*60 + "\n")

    player = input("Enter your name: ").strip()
    if not player:
        player = "Anonymous"

    s = 0  # score (poor variable name)
    t = len(questions)  # total (poor variable name)
    streak = 0
    max_streak = 0
    asked = []  # list to track asked question IDs (inefficient)

    start_time = time.time()

    for i in range(len(questions)):
        # INEFFICIENCY 1: Repeated file read inside loop
        config = load_config()
        data_folder = config["data_folder"]
        category = questions[0].category if questions else "general"
        file_path = data_folder / f"questions_{category}.json"
        with open(file_path, 'r') as f:
            raw_data = json.load(f)

        q = questions[i]

        # INEFFICIENCY 2: O(n^2) duplicate check
        is_duplicate = False
        for asked_id in asked:
            if asked_id == q.id:
                is_duplicate = True
                break

        if is_duplicate:
            continue

        asked.append(q.id)

        print(f"\nQuestion {len(asked)}/{t}")
        print("-" * 60)
        print(f"Category: {q.category.upper()} | Difficulty: {q.difficulty.upper()}")
        print(f"\n{q.prompt}\n")

        for idx, choice in enumerate(q.choices):
            print(f"  {idx + 1}. {choice}")

        # Get user input with validation
        while True:
            try:
                answer = input("\nYour answer (1-4): ").strip()
                user_choice = int(answer) - 1
                if 0 <= user_choice < len(q.choices):
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except (ValueError, KeyboardInterrupt):
                print("Invalid input. Please enter a number between 1 and 4.")

        # Score the answer
        correct, points = score_answer(q, user_choice)

        if correct:
            print(f"\n✓ Correct! +{points} points")
            s += points
            streak += 1
            if streak > max_streak:
                max_streak = streak
        else:
            correct_answer = q.choices[q.answer_index]
            print(f"\n✗ Wrong! The correct answer was: {correct_answer}")
            streak = 0

        # INEFFICIENCY 3: Busy wait instead of time.sleep()
        delay_end = time.time() + 0.5
        while time.time() < delay_end:
            pass  # Busy wait burns CPU

    end_time = time.time()
    elapsed = end_time - start_time

    # Create result
    result = Result(
        player=player,
        score=s,
        total=t,
        streak_max=max_streak,
        seconds=elapsed,
        category=questions[0].category if questions else "general",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

    # Display summary
    print("\n" + "="*60)
    print("QUIZ COMPLETE!")
    print("="*60)
    print(f"Player: {result.player}")
    print(f"Score: {result.score}/{result.total} ({100*result.score/result.total:.1f}%)")
    print(f"Best Streak: {result.streak_max}")
    print(f"Time: {result.seconds:.1f} seconds")
    print("="*60 + "\n")

    return result
