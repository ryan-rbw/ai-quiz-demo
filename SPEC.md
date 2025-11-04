# SPEC.md — AI Quiz Game

## 1. Overview

A simple, console based quiz game in Python that is easy for a mixed skill audience to understand. The project is intentionally split across multiple files and folders. One module contains inefficient code to set up a meaningful code review and refactor during the live demo.

## 2. Demo goals

1. Explore the codebase and ask the assistant to summarize modules and data flow (without revealing intentional flaws)
2. Run a code review that finds the inefficient area and quality issues (assistant discovers and reports them naturally)
3. Refactor and update the code to improve performance and readability
4. Add a new feature using spec driven prompts
5. Generate documentation and tests
6. Commit and push with an updated README and changelog

## 3. User story

As a player I want to take a multiple choice quiz, see my score, and save my result so I can compare with friends later.

## 4. High level features

1. Load questions from a JSON file with categories and difficulty
2. Present questions with four choices and a single correct answer
3. Track score, streaks, and time taken
4. Save results to a local leaderboard
5. Optional hints and category filters
6. Export a session summary to Markdown

## 5. Project structure

```
ai_quiz_game/
  README.md
  SPEC.md
  CHANGELOG.md
  pyproject.toml
  requirements.txt
  data/
    questions_general.json
    questions_science.json
  game/
    __init__.py
    app.py                 # CLI entry point
    config.py
    models.py              # dataclasses for Question and Result
    io_manager.py          # file read and write operations
    leaderboard.py
  engine/
    __init__.py
    quiz_engine.py         # contains the intentional inefficient code
    question_bank.py
    scoring.py
  utils/
    __init__.py
    timers.py
    rng.py
    text.py
  docs/
    ARCHITECTURE.md
    USAGE.md
  tests/
    test_engine.py
    test_io.py
    test_leaderboard.py
```

## 6. Data model

**Question**

```
{
  "id": "SCI-001",
  "category": "science",
  "difficulty": "easy",
  "prompt": "What gas do plants absorb?",
  "choices": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Helium"],
  "answer_index": 1,
  "hint": "Humans exhale this gas"
}
```

**Result**

```
{
  "player": "Alex",
  "score": 8,
  "total": 10,
  "streak_max": 5,
  "seconds": 94,
  "category": "science",
  "timestamp": "2025-11-03T13:15:00Z"
}
```

## 7. Module responsibilities and key functions

**game.app**
`main()` run the CLI, parse simple flags like `--category` and `--limit` and start a session

**game.config**
`load_config()` return defaults such as data folder and leaderboard path

**game.models**
`Question`, `Result` as dataclasses

**game.io_manager**
`load_questions(category)` read a JSON file and return a list of `Question`
`save_result(result)` append to a results JSON lines file

**game.leaderboard**
`top_n(n)` return the top results
`format_table(results)` return a printable table

**engine.question_bank**
`select_questions(questions, limit, difficulty)` choose a subset

**engine.quiz_engine**
`run_quiz(questions)` orchestrate a session, return `Result`

**engine.scoring**
`score_answer(question, user_choice)` return boolean and points

**utils.timers**
`Timer()` context helper to measure session time

**utils.rng**
`get_rng(seed=None)` return a `random.Random` for reproducible runs

**utils.text**
`wrap(s, width)` for clean console layout

## 8. Intentional inefficient code hotspot

File: `engine/quiz_engine.py`

Symptoms to plant

1. Repeated reads of the same JSON file inside the loop
2. O(n^2) duplicate check for already asked questions
3. Busy wait for a fake delay between questions using `while time.time() < t: pass`
4. Mixed concerns in a single function more than 80 lines and poor naming

Why this is good for the demo

1. Review can surface I O duplication and algorithmic complexity
2. Refactor can move loading to `io_manager`, use a set for seen ids, and replace busy wait with `time.sleep`
3. Extract small functions and add docstrings and type hints

Refactor acceptance

1. No repeated file reads
2. Selection and ask loop are separate functions with tests
3. CPU usage falls during waits
4. Cyclomatic complexity reduced and function length under 25 lines

## 9. CLI

Run a default 10 question session

```
python -m game.app
```

Filter by category and question count

```
python -m game.app --category science --limit 5
```

Show top scores

```
python -m game.app --leaderboard 10
```

## 10. Functional requirements

1. The game loads at least one category file and can run with default settings
2. The player is shown a question prompt and four choices
3. Input is validated and errors do not crash the game
4. Score increments on correct answers and tracks a max correct streak
5. A summary prints at the end and writes to leaderboard storage
6. Optional hint can be requested once per question and reduces points
7. Category filter and limit flags are honored

## 11. Non functional requirements

1. Works on Python 3.10 or later
2. No network calls
3. Clear function and module docstrings
4. Unit test coverage for the engine and I O helpers

## 12. Feature to add during the demo

**Hints with penalty**
Prompt the assistant with this spec

* Add a `--hints` flag that enables one hint per question
* When a hint is used the correct answer is worth half points
* Update the summary to show how many hints were used
* Update README and docs with usage and example

Acceptance

* New flag appears in `--help` output
* Using a hint changes scoring and is reflected in the summary
* Unit tests cover hint scoring and limit of one per question

## 13. Quality issues to seed besides the hotspot

1. Missing type hints in `engine.scoring`
2. Mixed print formatting styles
3. Sparse docstrings in `game.io_manager`
4. A small variable shadowing bug in `question_bank.select_questions`

## 14. Test plan

**Initial baseline tests** (implemented before demo):

1. `test_engine.py` - Basic engine functionality
   * Test scoring correct and incorrect answers
   * Test question selection with limits
   * Test difficulty filtering

2. `test_io.py` - I/O operations
   * Loading returns `Question` objects from both categories
   * Handles unknown category with FileNotFoundError
   * Writing a `Result` appends a line safely

3. `test_leaderboard.py` - Leaderboard functionality
   * `top_n` sorts by score (desc) and time (asc) tiebreaker
   * Respects limit parameter
   * Handles empty leaderboard
   * Table formatting width stays under 80 columns

**Additional tests to develop during demo** (after measuring code coverage):

1. `test_engine.py` additions
   * Validate end to end run with a seeded RNG
   * Confirm streak behavior with multiple correct/incorrect sequences
   * Assert no repeated JSON reads during the quiz (post-refactor validation)

2. `test_io.py` additions
   * Test question validation and data integrity
   * Test concurrent writes to leaderboard

3. `test_leaderboard.py` additions
   * Test edge cases for sorting with identical scores and times
   * Test table formatting with long player names

## 15. Documentation to generate with the assistant

1. README with quick start, examples, and flags
2. USAGE with screenshots of the console
3. ARCHITECTURE showing data flow and module boundaries
4. CHANGELOG with a summary of refactors and the hint feature

## 16. Prompts you can use verbatim during the demo

**Explore**
“Summarize this repository and explain how questions flow from file loading to scoring to leaderboard save. List modules and their roles in one paragraph each.”

**Review**
“Review `engine/quiz_engine.py` and identify performance and code quality issues. Suggest refactors and estimate complexity reductions.”

**Refactor**
“Refactor `engine/quiz_engine.py` to eliminate repeated file reads and busy wait. Extract functions for ask loop and selection. Keep behavior the same and add type hints and docstrings.”

**New feature**
“Implement a `--hints` flag as described in SPEC.md section Feature to add during the demo. Update docs and tests accordingly.”

**Docs**
“Generate README and USAGE based on the code and flags. Include examples and a short troubleshooting section.”

**Git**
“Create a branch `feature/hints`, commit the changes with conventional commit messages, and prepare a pull request description summarizing the refactor and new feature.”

## 17. Dependencies

```
rich                # for colored console text
typer               # CLI
pydantic            # optional validation of loaded questions
pytest              # testing
```

## 18. Acceptance checklist for the workshop

1. Runs locally from the command line
2. At least two categories of questions
3. Leaderboard persists in a simple file
4. Inefficient code exists in `engine/quiz_engine.py` before refactor
5. After refactor tests pass and CPU usage during waits is low
6. README and CHANGELOG updated
7. Commit history shows review, refactor, feature, and docs steps

---
