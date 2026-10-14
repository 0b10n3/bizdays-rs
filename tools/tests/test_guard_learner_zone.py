"""guard_learner_zone.py blocks edits in the learner zone unless the flag exists."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

GUARD = Path(__file__).resolve().parents[1] / "agents" / "guard_learner_zone.py"


def run_guard(root: Path, file_path: str) -> subprocess.CompletedProcess[str]:
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Edit",
        "cwd": str(root),
        "tool_input": {"file_path": file_path},
    }
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(root)},
    )


@pytest.mark.parametrize(
    ("rel", "code"),
    [
        ("crates/bizdays/src/date.rs", 2),
        ("crates/bizdays/tests/fixtures/bizdays.csv", 0),
        ("docs/index.md", 0),
    ],
)
def test_zones(tmp_path: Path, rel: str, code: int) -> None:
    result = run_guard(tmp_path, str(tmp_path / rel))
    assert result.returncode == code
    if code == 2:
        assert "zona do aprendiz" in result.stderr
        assert "just modo-implementacao on" in result.stderr
    else:
        assert result.stdout == result.stderr == ""


def test_relative_path_is_resolved(tmp_path: Path) -> None:
    assert run_guard(tmp_path, "py-bizdays/src/lib.rs").returncode == 2


def test_flag_allows_edit(tmp_path: Path) -> None:
    (tmp_path / ".agent-implementation-mode").touch()
    result = run_guard(tmp_path, str(tmp_path / "crates/bizdays/src/date.rs"))
    assert result.returncode == 0
    assert result.stderr == ""


def test_absolute_path_outside_repo(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "elsewhere" / "crates" / "bizdays" / "src" / "date.rs"
    assert run_guard(root, str(outside)).returncode == 0
