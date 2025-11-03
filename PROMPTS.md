# Demo Prompts

Verbatim prompts for the 5-step demo workflow. Copy and paste these exactly during your presentation.

## Step 1: Explore & Review

**Prompt:**
```
Review the codebase and explain the architecture. Then run a code review on engine/quiz_engine.py and identify all performance and code quality issues. Be specific about the problems and their impact.
```

**Expected Output:**
- Architecture summary with data flow
- Identification of repeated file I/O, O(n²) duplicate checking, busy-wait CPU burning
- Poor variable names (`s`, `t`) and monolithic function issues

---

## Step 2: Measure & Refactor

**Prompt:**
```
First, run code coverage to establish a baseline. Then refactor engine/quiz_engine.py to fix all the performance issues you identified. Eliminate repeated file reads, replace the O(n²) duplicate check with a set, replace busy-wait with time.sleep(), and extract smaller functions with proper type hints and docstrings. Verify tests still pass after refactoring.
```

**Expected Output:**
- Coverage report showing 45% baseline with quiz_engine.py at 0%
- Refactored code with improved performance
- All existing tests passing
- Improved coverage for quiz_engine.py

---

## Step 3: Add Hints Feature

**Prompt:**
```
Implement the hints feature as described in FEATURE.md. Add a --hints flag that enables one hint per question, with half points when used. Write comprehensive tests for the new functionality. Ensure the feature is fully tested before proceeding.
```

**Expected Output:**
- New `--hints` CLI flag
- Hint display and penalty logic in quiz engine
- Updated scoring with half-points for hint usage
- New tests for hint functionality
- Updated help text

---

## Step 4: Improve Test Coverage

**Prompt:**
```
Run code coverage again and identify the remaining gaps. Write additional tests to get coverage above 70%. Focus on edge cases and the previously untested modules like utils/timers.py, utils/text.py, and game/app.py CLI interface.
```

**Expected Output:**
- Coverage report showing gaps
- New tests for untested modules
- Coverage improved to 70%+ target
- Edge case coverage

---

## Step 5: Documentation & Commit

**Prompt:**
```
Generate a comprehensive README.md with quickstart, installation, usage examples, and all CLI flags. Create a CHANGELOG.md documenting the refactoring and hints feature. Then create a git commit with conventional commit format and push the changes.
```

**Expected Output:**
- Professional README.md with examples
- CHANGELOG.md with version history
- Clean git commit with proper message
- Changes pushed to repository

---

## Quick Reference Commands

**Run the game:**
```bash
python3 -m game.app --category science --limit 5
```

**Run tests with coverage:**
```bash
python3 -m pytest --cov=game --cov=engine --cov=utils --cov-report=term-missing tests/
```

**View leaderboard:**
```bash
python3 -m game.app --leaderboard 10
```
