# AI Quiz Game

An interactive command-line quiz application built with Python, featuring multiple categories, difficulty levels, and an optional hints system.

## Features

- **Multiple Categories**: Choose from general knowledge, science, and more
- **Difficulty Filtering**: Filter questions by easy, medium, or hard difficulty
- **Hints System**: Get help with challenging questions (with a scoring penalty)
- **Leaderboard**: Track high scores across quiz sessions
- **Streak Tracking**: Monitor consecutive correct answers
- **Timed Sessions**: See how quickly you complete quizzes

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run a standard 10-question quiz
python3 -m game.app

# Run with hints enabled
python3 -m game.app --hints

# View the leaderboard
python3 -m game.app --leaderboard 10
```

## Installation

### Requirements

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd ai-quiz-demo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python3 -m game.app --help
   ```

### Dependencies

- **rich** (≥13.0.0) - Rich text formatting for terminal output
- **typer** (≥0.9.0) - CLI framework for building command-line interfaces
- **pydantic** (≥2.0.0) - Data validation library
- **pytest** (≥7.4.0) - Testing framework

## Usage

### Basic Usage

Run a standard quiz with default settings (10 questions from general category):

```bash
python3 -m game.app
```

### Command-Line Options

| Flag | Short | Type | Description | Default |
|------|-------|------|-------------|---------|
| `--category` | `-c` | TEXT | Question category (general, science) | general |
| `--limit` | `-l` | INTEGER | Number of questions | 10 |
| `--difficulty` | `-d` | TEXT | Filter by difficulty (easy/medium/hard) | None |
| `--hints` | `-h` | FLAG | Enable hints (halves points when used) | False |
| `--leaderboard` | `-b` | INTEGER | Show top N scores and exit | None |

### Usage Examples

**Science quiz with 5 questions:**
```bash
python3 -m game.app --category science --limit 5
```

**Easy difficulty questions:**
```bash
python3 -m game.app --difficulty easy --limit 5
```

**Quiz with hints enabled:**
```bash
python3 -m game.app --hints
```

**Combined options:**
```bash
python3 -m game.app --category science --difficulty medium --limit 10 --hints
```

**View top 10 scores:**
```bash
python3 -m game.app --leaderboard 10
```

## How to Play

### Starting a Quiz

1. Run the command with your desired options
2. Enter your player name when prompted (or press Enter for "Anonymous")
3. Questions will be presented one at a time

### Answering Questions

For each question:
- Read the question and four answer choices
- Enter the number (1-4) corresponding to your answer
- If hints are enabled, you can type `h` to see a hint (once per question)

**Example question:**
```
Question 1/10
------------------------------------------------------------
Category: SCIENCE | Difficulty: MEDIUM

What is the speed of light in a vacuum?

  1. 299,792 km/s
  2. 300,000 km/s
  3. 150,000 km/s
  4. 400,000 km/s

Your answer (1-4, or 'h' for hint):
```

### Using Hints

When hints are enabled (`--hints` flag):

1. Type `h` when prompted for your answer
2. A hint will be displayed immediately
3. Enter your answer (1-4) after reading the hint
4. **Penalty**: Correct answers with hints earn **0.5 points** instead of 1.0
5. **Limit**: One hint per question

**Example with hint:**
```
Your answer (1-4, or 'h' for hint): h

Hint: Remember that light travels at approximately 300,000 kilometers per second.

Your answer (1-4): 1

✓ Correct! +0.5 points
```

### Scoring

- **Correct answer (no hint)**: 1.0 point
- **Correct answer (with hint)**: 0.5 points
- **Incorrect answer**: 0 points
- **Streak bonus**: Track consecutive correct answers

### Results

After completing the quiz, you'll see:
- Final score and percentage
- Best streak achieved
- Number of hints used (if any)
- Total time taken
- Results are automatically saved to the leaderboard

**Example summary:**
```
============================================================
QUIZ COMPLETE!
============================================================
Player: Alice
Score: 7.5/10 (75.0%)
Best Streak: 4
Hints Used: 3
Time: 42.3 seconds
============================================================
```

## Available Categories

The quiz currently includes the following categories:

- **general** - General knowledge questions across various topics
- **science** - Science-focused questions (physics, chemistry, biology)

### Adding New Categories

To add a new category:

1. Create a JSON file: `data/questions_<category>.json`
2. Follow this structure:

```json
[
  {
    "id": "CAT-001",
    "category": "category_name",
    "difficulty": "easy",
    "prompt": "Your question text?",
    "choices": [
      "Choice A",
      "Choice B",
      "Choice C",
      "Choice D"
    ],
    "answer_index": 0,
    "hint": "Optional hint text"
  }
]
```

3. The category will automatically be available via `--category <category_name>`

## Leaderboard

Results are persisted to `leaderboard.jsonl` in the project root.

### Viewing the Leaderboard

```bash
# Show top 10 scores
python3 -m game.app --leaderboard 10

# Show top 5 scores
python3 -m game.app --leaderboard 5
```

**Example output:**
```
==============================================================================
Rank   Player          Score      Streak   Time (s)   Category
==============================================================================
1      Alice           9.5/10     7        38.2       science
2      Bob             9.0/10     6        45.1       general
3      Charlie         8.5/10     5        52.3       science
==============================================================================
```

### Leaderboard Sorting

Results are sorted by:
1. **Score** (descending) - Higher scores first
2. **Time** (ascending) - Faster times break ties

## Development

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_engine.py -v

# Run with coverage
python3 -m pytest --cov=game --cov=engine --cov=utils --cov-report=term-missing tests/
```

### Test Coverage

Current test coverage: **43%** (21 tests)

**Fully covered modules:**
- `engine/scoring.py` - Answer scoring logic
- `engine/question_bank.py` - Question selection and filtering
- `game/config.py` - Configuration management
- `game/io_manager.py` - File I/O operations
- `game/leaderboard.py` - Leaderboard management
- `game/models.py` - Data models

**Uncovered modules** (interactive/CLI):
- `engine/quiz_engine.py` - Main quiz loop (requires user input)
- `game/app.py` - CLI interface

### Project Structure

```
ai-quiz-demo/
├── game/               # CLI and I/O layer
│   ├── app.py         # CLI entry point (Typer)
│   ├── models.py      # Data models (Question, Result)
│   ├── io_manager.py  # JSON file operations
│   ├── leaderboard.py # Leaderboard formatting
│   └── config.py      # Configuration settings
├── engine/            # Quiz logic layer
│   ├── quiz_engine.py # Main quiz orchestration
│   ├── question_bank.py # Question selection
│   └── scoring.py     # Answer scoring
├── utils/             # Helper utilities
│   ├── timers.py      # Time measurement
│   ├── rng.py         # Random number generation
│   └── text.py        # Text formatting
├── data/              # Question data files
│   ├── questions_general.json
│   └── questions_science.json
├── tests/             # Unit tests
└── leaderboard.jsonl  # Persistent leaderboard (gitignored)
```

## Architecture

### Three-Layer Design

1. **Game Layer** (`game/`) - User interface and I/O
   - CLI argument parsing
   - Question/result persistence
   - Leaderboard display

2. **Engine Layer** (`engine/`) - Core quiz logic
   - Quiz orchestration and flow control
   - Question selection and filtering
   - Answer validation and scoring

3. **Utils Layer** (`utils/`) - Shared utilities
   - Timing, random number generation, text formatting

### Data Flow

```
JSON files → load_questions() → select_questions()
    → run_quiz() → score_answer() → Result
    → save_result() → leaderboard.jsonl
```

## Performance

Recent optimizations include:

- **O(1) duplicate checking** using sets instead of O(n²) list searches
- **Eliminated repeated file I/O** - Questions loaded once per session
- **CPU-friendly delays** - Using `time.sleep()` instead of busy-waiting
- **Modular design** - Smaller, focused functions for better maintainability

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'typer'**
```bash
pip install -r requirements.txt
```

**FileNotFoundError: No questions found for category**
```bash
# Check available categories
ls data/questions_*.json
# Use a valid category name
python3 -m game.app --category general
```

**Quiz doesn't show hints when pressing 'h'**
```bash
# Make sure --hints flag is enabled
python3 -m game.app --hints
```

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Include docstrings with Args/Returns sections
- Maintain test coverage for new features

### Testing New Features

1. Write unit tests first (TDD approach)
2. Ensure all tests pass: `python3 -m pytest tests/ -v`
3. Verify integration with manual testing
4. Update documentation (README, CHANGELOG)

## License

This project is for educational and demonstration purposes.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Support

For issues, questions, or contributions, please refer to the project documentation in the repository.
