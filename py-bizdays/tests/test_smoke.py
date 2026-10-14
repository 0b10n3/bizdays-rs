"""Smoke test: the native module imports and reports the Cargo version."""

import re
from pathlib import Path

import bizdays_rs

CARGO_TOML = Path(__file__).parents[2] / "crates" / "bizdays" / "Cargo.toml"


def test_version_matches_cargo() -> None:
    # tomllib only exists on Python >= 3.11; we support 3.10.
    match = re.search(r'^version = "([^"]+)"', CARGO_TOML.read_text(), re.MULTILINE)
    assert match is not None
    assert bizdays_rs.__version__ == match.group(1)
