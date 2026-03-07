# BytePulse: Daily Contribution Project

A minimal project that creates one meaningful daily log entry and can auto-commit via GitHub Actions.

## What this project does
- Generates a daily markdown note under `logs/YYYY-MM/YYYY-MM-DD.md`
- Updates `logs/INDEX.md` so each day has a visible trail
- Supports manual notes (`--note`) or automatic prompts (`--auto`)
- Includes a scheduled GitHub Action that commits only when files changed

## Quick start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

python daily_pulse.py --note "Today I learned about list comprehensions"
```

## Run modes
```bash
# manual entry
python daily_pulse.py --note "Refactored API validation"

# auto prompt mode
python daily_pulse.py --auto

# backfill a specific date
python daily_pulse.py --date 2026-03-01 --note "Backfill note"
```

## GitHub setup (for contributions)
1. Create a new repo on GitHub.
2. Push this folder as that repo.
3. In GitHub repo Settings -> Actions -> General:
   - Ensure workflow permissions allow write access to contents.
4. In Actions tab, enable workflows if prompted.
5. The workflow in `.github/workflows/daily-pulse.yml` will run every day and commit changes.

## Notes
- Only non-empty changes are committed.
- Use `--note` for real progress to keep history meaningful.
