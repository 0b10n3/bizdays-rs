"""Validate the holiday calendars in crates/bizdays/data/*.cal.

Format: weekday names (non-business days of the week) first, then ISO dates,
one per line. Blank lines are ignored.

Exits with a non-zero status if any check fails. Standard library only.
"""

from __future__ import annotations

import datetime as dt
import sys
from itertools import pairwise
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "crates" / "bizdays" / "data"
WEEKDAYS = {
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
}
# (calendar, date, reason): holidays that must be present.
SANITY = [("ANBIMA", "2024-11-20", "Consciência Negra, Lei 14.759/2023")]


def parse(path: Path) -> tuple[list[str], list[dt.date], list[str]]:
    """Return (weekday header, holidays, errors) for one .cal file."""
    header: list[str] = []
    dates: list[dt.date] = []
    errors: list[str] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if not dates and line in WEEKDAYS:
            header.append(line)
            continue
        try:
            dates.append(dt.date.fromisoformat(line))
        except ValueError:
            errors.append(
                f"{path.name}:{lineno}: not a weekday name or ISO date: {line!r}"
            )
    if not header:
        errors.append(f"{path.name}: missing weekday header")
    if len(set(header)) != len(header):
        errors.append(f"{path.name}: duplicated weekday in header")
    for prev, cur in pairwise(dates):
        if cur <= prev:
            kind = "duplicate" if cur == prev else "out of order"
            errors.append(f"{path.name}: {kind} date {cur} after {prev}")
    if not dates:
        errors.append(f"{path.name}: no holidays")
    return header, dates, errors


def main(data_dir: Path = DATA_DIR) -> int:
    files = sorted(data_dir.glob("*.cal"))
    if not files:
        print(f"no .cal files in {data_dir}", file=sys.stderr)
        return 1
    all_errors: list[str] = []
    holidays: dict[str, set[dt.date]] = {}
    for path in files:
        header, dates, errors = parse(path)
        all_errors += errors
        holidays[path.stem] = set(dates)
        if dates:
            print(
                f"{path.stem}: {len(set(dates))} holidays, {dates[0]} .. {dates[-1]}, "
                f"non-business weekdays: {', '.join(header)}"
            )
    for cal, date, reason in SANITY:
        if dt.date.fromisoformat(date) not in holidays.get(cal, set()):
            all_errors.append(f"{cal}: expected holiday {date} ({reason}) is missing")
    for err in all_errors:
        print(f"ERROR {err}", file=sys.stderr)
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_DIR))
