"""Generate golden test fixtures for the bizdays crate from trusted oracles.

Oracles:
- NumPy (`busday_count`, `is_busday`, `busday_offset`) for counts and rolls.
  Inverted pairs (from > to) follow ADR-0001: `-busday_count(to, from)`, so
  counts are antisymmetric (NumPy itself counts `(to, from]` there);
- python-bizdays (`offset`, `getdate`) for offsets and the getdate DSL.

Holidays come from crates/bizdays/data/*.cal (the same data the library
embeds) and feed both oracles; the script aborts if the calendars bundled
with python-bizdays differ from them (ignoring upstream duplicates).

Deterministic and idempotent: fixed seed, sorted output, no timestamps.

Usage: python tools/oracle/generate_fixtures.py [--out DIR]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import random
import sys
from collections import Counter
from importlib.metadata import version
from pathlib import Path

import bizdays
import numpy as np

GENERATOR_VERSION = "1.1.0"
SEED = 20261013
CALENDARS = ("ANBIMA", "B3")

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "crates" / "bizdays" / "data"
OUT_DIR = ROOT / "crates" / "bizdays" / "tests" / "fixtures"

N_RANDOM_PAIRS = 5_000
N_INVERTED_PAIRS = 1_000
DENSE_START, DENSE_END = dt.date(2024, 1, 1), dt.date(2026, 12, 31)
ROLLS = {
    "following": "following",
    "preceding": "preceding",
    "modified_following": "modifiedfollowing",
    "modified_preceding": "modifiedpreceding",
}
OFFSET_N = range(-30, 31)
N_OFFSET_DATES = 300
N_DIVERGENCE_PAIRS = 20_000
MAX_DIVERGENCE_ROWS_PER_CALENDAR = 250  # 500 rows in total
GETDATE_YEARS = range(2024, 2028)
GETDATE_EXPRS = (
    "first day",
    "last day",
    "first bizday",
    "last bizday",
    "15th day",
    "first mon",
    "last fri",
    "third wed",
    "first bizday after 15th day",
    "second bizday before last bizday",
)
GETDATE_ANNUAL = GETDATE_EXPRS[:4]
# (from, to) edge cases for bizdays.csv; expected values come from `Cal.count`.
EDGE_PAIRS = (
    ("2026-10-13", "2026-10-13"),  # same business day
    ("2026-10-12", "2026-10-12"),  # same non-business day (holiday)
    ("2026-10-16", "2026-10-17"),  # Friday -> Saturday
    ("2026-10-17", "2026-10-18"),  # Saturday -> Sunday
    ("2026-10-17", "2026-10-19"),  # Saturday -> Monday
    ("2026-10-09", "2026-10-13"),  # across the 2026-10-12 holiday
    ("2026-10-10", "2026-10-17"),  # weekend + holiday at the start
    ("2026-02-13", "2026-02-19"),  # Carnival 2026
    ("2024-11-19", "2024-11-21"),  # Consciência Negra (national since 2024)
    ("2025-12-31", "2026-01-02"),  # year turn: differs between ANBIMA and B3
)


class Cal:
    """One calendar: holidays, weekmask, range and its NumPy busdaycalendar."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.path = DATA_DIR / f"{name}.cal"
        self.weekdays: list[str] = []
        self.holidays: list[dt.date] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            if line[0].isdigit():
                self.holidays.append(dt.date.fromisoformat(line))
            else:
                self.weekdays.append(line)
        names = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        nonbiz = {names.index(w.lower()) for w in self.weekdays}
        self.weekmask = "".join("0" if i in nonbiz else "1" for i in range(7))
        # Range: complete years covered by the data.
        self.start = dt.date(self.holidays[0].year, 1, 1)
        self.end = dt.date(self.holidays[-1].year, 12, 31)
        self.np = np.busdaycalendar(
            weekmask=self.weekmask,
            holidays=np.array(sorted(set(self.holidays)), dtype="datetime64[D]"),
        )
        self.py = bizdays.Calendar(
            holidays=self.holidays, weekdays=self.weekdays, name=name
        )
        # python-bizdays indexes only [first holiday, last holiday].
        self.py_start, self.py_end = self.py.startdate, self.py.enddate

    def check_against_python_bizdays(self) -> None:
        bundled = bizdays.Calendar.load(self.name)
        if (
            sorted(set(bundled.holidays)) != self.holidays
            or list(bundled.weekdays) != self.weekdays
        ):
            sys.exit(
                f"{self.name}: holidays in {self.path} differ from python-bizdays "
                f"{version('bizdays')}; refusing to generate fixtures"
            )

    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()

    def count(self, a: dt.date, b: dt.date) -> int:
        if a > b:  # ADR-0001: antisymmetric, unlike NumPy's (b, a]
            return -self.count(b, a)
        return int(np.busday_count(a, b, busdaycal=self.np))

    def is_biz(self, d: dt.date) -> bool:
        return bool(np.is_busday(d, busdaycal=self.np))

    def roll(self, d: dt.date, roll: str) -> dt.date:
        return np.busday_offset(d, 0, roll=roll, busdaycal=self.np).astype(dt.date)


def random_date(rng: random.Random, start: dt.date, end: dt.date) -> dt.date:
    return start + dt.timedelta(days=rng.randrange((end - start).days + 1))


def days(start: dt.date, end: dt.date) -> list[dt.date]:
    return [start + dt.timedelta(n) for n in range((end - start).days + 1)]


def gen_bizdays(cal: Cal, rng: random.Random) -> list[tuple]:
    pairs = set()
    random_pairs = []
    for _ in range(N_RANDOM_PAIRS):
        a, b = sorted(
            (random_date(rng, cal.start, cal.end), random_date(rng, cal.start, cal.end))
        )
        random_pairs.append((a, b))
    pairs.update(random_pairs)
    pairs.update((b, a) for a, b in random_pairs[:N_INVERTED_PAIRS])
    pairs.update(
        (dt.date.fromisoformat(a), dt.date.fromisoformat(b)) for a, b in EDGE_PAIRS
    )
    first_biz = cal.roll(cal.start, "following")
    last_biz = cal.roll(cal.end, "preceding")
    pairs.update({(first_biz, last_biz), (last_biz, first_biz)})
    return [(cal.name, a, b, cal.count(a, b)) for a, b in pairs]


def gen_isbizday(cal: Cal) -> list[tuple]:
    return [(cal.name, d, cal.is_biz(d)) for d in days(DENSE_START, DENSE_END)]


def gen_roll(cal: Cal, skipped: Counter) -> list[tuple]:
    rows = []
    for d in days(DENSE_START, DENSE_END):
        for conv, np_roll in ROLLS.items():
            expected = cal.roll(d, np_roll)
            # Beyond the data NumPy would treat unknown holidays as business days.
            if not cal.start <= expected <= cal.end:
                skipped[f"roll:{cal.name}"] += 1
                continue
            rows.append((cal.name, d, conv, expected))
    return rows


def gen_offset(cal: Cal, rng: random.Random, skipped: Counter) -> list[tuple]:
    rows = []
    dates = {random_date(rng, cal.py_start, cal.py_end) for _ in range(N_OFFSET_DATES)}
    for d in sorted(dates):
        for n in OFFSET_N:
            try:
                expected = cal.py.offset(d, n)
            except (IndexError, bizdays.DateOutOfRange):
                skipped[f"offset:{cal.name}"] += 1
                continue
            # python-bizdays silently wraps around on negative list indices.
            if (n > 0 and expected <= d) or (n < 0 and expected >= d):
                skipped[f"offset:{cal.name}"] += 1
                continue
            rows.append((cal.name, d, n, expected))
    return rows


def gen_getdate(cal: Cal, skipped: Counter) -> list[tuple]:
    rows = []
    queries = [
        (e, y, m) for e in GETDATE_EXPRS for y in GETDATE_YEARS for m in range(1, 13)
    ]
    queries += [(e, y, None) for e in GETDATE_ANNUAL for y in GETDATE_YEARS]
    for expr, year, month in queries:
        try:
            expected = cal.py.getdate(expr, year, month)
        except Exception:  # python-bizdays raises bare KeyError/IndexError/ValueError
            skipped[f"getdate:{cal.name}"] += 1
            continue
        rows.append((cal.name, expr, year, "" if month is None else month, expected))
    return rows


def gen_divergences(cal: Cal, rng: random.Random) -> tuple[list[tuple], dict]:
    """Compare python-bizdays counts with ours (ADR-0001) on random pairs."""
    by_kind: dict[str, Counter] = {}
    rows = []
    for _ in range(N_DIVERGENCE_PAIRS):
        a = random_date(rng, cal.py_start, cal.py_end)
        b = random_date(rng, cal.py_start, cal.py_end)
        expected, got = cal.count(a, b), cal.py.bizdays(a, b)
        a_biz, b_biz = cal.is_biz(a), cal.is_biz(b)
        direction = "forward" if a <= b else "backward"
        ends = f"from_{'biz' if a_biz else 'nonbiz'}__to_{'biz' if b_biz else 'nonbiz'}"
        kind = f"{direction}:{ends}"
        stats = by_kind.setdefault(kind, Counter())
        stats["pairs"] += 1
        if got != expected:
            stats["divergent"] += 1
            stats[f"python_bizdays_minus_expected={got - expected:+d}"] += 1
            rows.append((cal.name, a, b, expected, got, a_biz, b_biz))
    rows = sorted(rows, key=lambda r: (r[1], r[2]))[:MAX_DIVERGENCE_ROWS_PER_CALENDAR]
    return rows, {k: dict(sorted(v.items())) for k, v in sorted(by_kind.items())}


def fmt(v: object) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, dt.date):
        return v.isoformat()
    return str(v)


def write_csv(path: Path, header: tuple[str, ...], rows: list[tuple]) -> int:
    lines = sorted({tuple(fmt(v) for v in row) for row in rows})
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(lines)
    return len(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    out: Path = parser.parse_args().out
    out.mkdir(parents=True, exist_ok=True)

    cals = [Cal(name) for name in CALENDARS]
    for cal in cals:
        cal.check_against_python_bizdays()

    rng = random.Random(SEED)
    skipped: Counter = Counter()
    files: dict[str, tuple[tuple[str, ...], list[tuple]]] = {
        "bizdays.csv": (("calendar", "from", "to", "expected"), []),
        "isbizday.csv": (("calendar", "date", "expected"), []),
        "roll.csv": (("calendar", "date", "convention", "expected"), []),
        "offset.csv": (("calendar", "date", "n", "expected"), []),
        "getdate.csv": (("calendar", "expr", "year", "month", "expected"), []),
        "divergences_python_bizdays.csv": (
            (
                "calendar",
                "from",
                "to",
                "expected",
                "python_bizdays",
                "from_is_biz",
                "to_is_biz",
            ),
            [],
        ),
    }
    divergences = {}
    for cal in cals:  # fixed order keeps the RNG stream deterministic
        files["bizdays.csv"][1].extend(gen_bizdays(cal, rng))
        files["isbizday.csv"][1].extend(gen_isbizday(cal))
        files["roll.csv"][1].extend(gen_roll(cal, skipped))
        files["offset.csv"][1].extend(gen_offset(cal, rng, skipped))
        files["getdate.csv"][1].extend(gen_getdate(cal, skipped))
        rows, summary = gen_divergences(cal, rng)
        files["divergences_python_bizdays.csv"][1].extend(rows)
        divergences[cal.name] = {
            "pairs_sampled": N_DIVERGENCE_PAIRS,
            "by_endpoint_kind": summary,
        }

    row_counts = {
        name: write_csv(out / name, hdr, rows) for name, (hdr, rows) in files.items()
    }
    manifest = {
        "generator_version": GENERATOR_VERSION,
        "seed": SEED,
        "oracles": {"numpy": np.__version__, "python-bizdays": version("bizdays")},
        "calendars": {
            cal.name: {
                "sha256": cal.sha256(),
                "weekmask": cal.weekmask,
                "range": [cal.start.isoformat(), cal.end.isoformat()],
                "python_bizdays_range": [
                    cal.py_start.isoformat(),
                    cal.py_end.isoformat(),
                ],
            }
            for cal in cals
        },
        "rows": row_counts,
        "skipped": dict(sorted(skipped.items())),
        "divergences_python_bizdays": divergences,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rows": row_counts, "skipped": manifest["skipped"]}, indent=2))


if __name__ == "__main__":
    main()
