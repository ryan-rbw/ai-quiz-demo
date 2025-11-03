# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is an **AI Quiz Game demo project** - a Python console application intentionally designed for live coding demonstrations. The codebase contains deliberate code quality issues and inefficiencies in `engine/quiz_engine.py` to showcase code review, refactoring, and testing workflows.

**Critical**: Do NOT "fix" issues in `engine/quiz_engine.py` unless explicitly asked. These are intentional demo artifacts:
- Repeated JSON file reads in loops
- O(n²) duplicate checking
- Busy-wait CPU burning (`while time.time() < t: pass`)
- 100+ line monolithic function with poor variable names

## Development Commands

### Running the application
```bash
# Default 10 question quiz
python3 -m game.app

# Science category with 5 questions
python3 -m game.app --category science --limit 5

# Filter by difficulty
python3 -m game.app --difficulty easy --limit 5

# View leaderboard
python3 -m game.app --leaderboard 10

# Help
python3 -m game.app --help
```

### Testing
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_engine.py -v

# Run single test
python3 -m pytest tests/test_engine.py::test_score_answer_correct -v

# Code coverage (baseline: 45%)
python3 -m pytest --cov=game --cov=engine --cov=utils --cov-report=term-missing tests/

# Generate HTML coverage report
python3 -m pytest --cov=game --cov=engine --cov=utils --cov-report=html tests/
# View at htmlcov/index.html
```

### Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Required packages: rich, typer, pydantic, pytest
```

## Architecture Overview

### Three-Layer Design

**1. Game Layer** (`game/`) - CLI and I/O
- `app.py`: CLI entry point using Typer, handles all command-line flags
- `models.py`: Dataclasses for `Question` and `Result`
- `io_manager.py`: JSON file operations for questions and leaderboard persistence
- `leaderboard.py`: Sorting, filtering, and table formatting for results
- `config.py`: Returns configuration dict with paths and defaults

**2. Engine Layer** (`engine/`) - Quiz logic
- `quiz_engine.py`: **Main orchestration** - contains intentional inefficiencies (see below)
- `question_bank.py`: Question selection and difficulty filtering
- `scoring.py`: Answer validation and point calculation (missing type hints intentionally)

**3. Utils Layer** (`utils/`) - Helpers
- `timers.py`: Context manager for measuring quiz duration
- `rng.py`: Seeded random number generator for reproducible tests
- `text.py`: Text wrapping utility for console output

### Data Flow

```
JSON files (data/)
  → io_manager.load_questions()
  → question_bank.select_questions()
  → quiz_engine.run_quiz()
    ↓ (uses scoring.score_answer() per question)
  → Result object
  → io_manager.save_result()
  → leaderboard.jsonl
```

### Leaderboard Persistence

Results are appended to `leaderboard.jsonl` (one JSON object per line). The file is excluded from git via `.gitignore`.

## Test Structure

**Current coverage: 45%** (15 tests)

**100% covered modules:**
- `engine/question_bank.py`, `engine/scoring.py`
- `game/config.py`, `game/io_manager.py`, `game/leaderboard.py`, `game/models.py`
- `utils/rng.py`

**0% covered modules** (intentional gaps for demo):
- `engine/quiz_engine.py` (75 lines) - main quiz loop
- `game/app.py` (31 lines) - CLI interface
- `utils/timers.py`, `utils/text.py`

**Test patterns:**
- Use `monkeypatch` fixture to mock `load_config()` in I/O tests
- Use `tmp_path` fixture for temporary file operations
- See SPEC.md section 14 for planned additional tests

## Known Quality Issues (For Demo)

Beyond `quiz_engine.py`, these issues exist intentionally:

1. **Missing type hints** in `engine/scoring.py`
2. **Mixed print formatting** styles across modules
3. **Sparse docstrings** in `game/io_manager.py`
4. **Variable shadowing bug** in `question_bank.py` line 23 (`questions = questions`)

## Demo Workflow (See SPEC.md and PROMPTS.md)

The repository is designed for this sequence:
1. Explore codebase and explain data flow
2. Code review to find inefficiencies in `quiz_engine.py`
3. Refactor quiz engine (eliminate file I/O in loops, use sets, replace busy-wait)
4. Add `--hints` feature (see FEATURE.md)
5. Generate documentation (README, USAGE, ARCHITECTURE, CHANGELOG)
6. Commit workflow with conventional commits

## Adding New Question Categories

1. Create `data/questions_<category>.json` following the structure:
```json
[
  {
    "id": "CAT-001",
    "category": "category_name",
    "difficulty": "easy|medium|hard",
    "prompt": "Question text?",
    "choices": ["A", "B", "C", "D"],
    "answer_index": 0,
    "hint": "Optional hint text"
  }
]
```

2. No code changes needed - `io_manager.load_questions(category)` will automatically load it

## Testing with Mocks

When testing functions that call `load_config()`, use monkeypatch:

```python
def test_something(tmp_path, monkeypatch):
    def mock_load_config():
        return {
            "data_folder": Path("data"),
            "leaderboard_path": tmp_path / "test.jsonl"
        }
    monkeypatch.setattr("module.submodule.load_config", mock_load_config)
    # ... test code
```

## Important Files

- **SPEC.md**: Complete specification including intentional issues and refactor acceptance criteria
- **PROMPTS.md**: Verbatim prompts for demo workflow steps
- **FEATURE.md**: Hints feature specification to implement during demo
- **pyproject.toml**: Project metadata and dependencies
