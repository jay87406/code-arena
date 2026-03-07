#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import random
from pathlib import Path

ROOT = Path(__file__).parent
LOG_DIR = ROOT / "logs"
INDEX_FILE = LOG_DIR / "INDEX.md"

PROMPTS = [
    "Learn one Python standard library feature and summarize it.",
    "Solve one small algorithm problem and write key takeaway.",
    "Refactor a function and document before/after differences.",
    "Read one API doc page and note practical usage.",
    "Write one test case for a bug you found today.",
    "Optimize one query or loop and record measured result.",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create one daily contribution log")
    parser.add_argument("--date", help="Date in YYYY-MM-DD. Defaults to today.")
    parser.add_argument("--note", help="Manual note for today's progress.")
    parser.add_argument("--auto", action="store_true", help="Generate using prompt template.")
    return parser.parse_args()


def resolve_date(raw: str | None) -> dt.date:
    if raw:
        return dt.date.fromisoformat(raw)
    return dt.date.today()


def build_note(day: dt.date, note: str | None, auto: bool) -> str:
    if note and note.strip():
        return note.strip()

    seed = int(day.strftime("%Y%m%d"))
    prompt = random.Random(seed).choice(PROMPTS)
    if auto:
        return f"Prompt: {prompt}\n\nResult: (fill your real outcome here)"

    return "No note provided. Run again with --note \"...\" for meaningful logs."


def write_daily_file(day: dt.date, content: str) -> Path:
    month_dir = LOG_DIR / day.strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)

    daily_path = month_dir / f"{day.isoformat()}.md"
    body = (
        f"# Daily Log - {day.isoformat()}\n\n"
        f"## Focus\n{content}\n\n"
        "## Next step\n- "
        "Continue with one concrete improvement tomorrow.\n"
    )
    daily_path.write_text(body, encoding="utf-8")
    return daily_path


def update_index(day: dt.date, entry_path: Path) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    rel = entry_path.relative_to(ROOT).as_posix()

    if INDEX_FILE.exists():
        lines = INDEX_FILE.read_text(encoding="utf-8").splitlines()
    else:
        lines = ["# Daily Index", "", "| Date | Entry |", "|---|---|"]

    row = f"| {day.isoformat()} | [{day.isoformat()}]({rel}) |"
    if row not in lines:
        lines.append(row)
        lines = dedupe_index(lines)
        INDEX_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def dedupe_index(lines: list[str]) -> list[str]:
    head = lines[:4]
    rows = sorted(set(lines[4:]), reverse=True)
    return head + rows


def main() -> int:
    args = parse_args()
    day = resolve_date(args.date)
    note = build_note(day, args.note, args.auto)

    path = write_daily_file(day, note)
    update_index(day, path)

    print(f"Updated: {path}")
    print(f"Updated: {INDEX_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
