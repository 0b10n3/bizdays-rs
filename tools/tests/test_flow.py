"""flow.py: branch names and PR origin/destination (fluxo-git.md, section 2)."""

import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "flow", Path(__file__).resolve().parents[1] / "git" / "flow.py"
)
assert _spec and _spec.loader
flow = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(flow)


@pytest.mark.parametrize(
    "name",
    [
        "main",
        "develop",
        "dependabot/cargo/pyo3-0.30",
        "feature/e1-s03-date-civil",
        "data/e4-s14-ny-calendar",
        "chore/e0-s01-repo-setup",
        "bugfix/csv-header-parsing",
        "spike/cum-u16",
        "release/bizdays-0.1.0",
        "release/bizdays-rs-0.1.0",
        "hotfix/bizdays-0.1.1",
        "support/bizdays-0.1.x",
    ],
)
def test_valid_branch(name: str) -> None:
    assert flow.valid_branch(name)


@pytest.mark.parametrize(
    "name",
    [
        "feature/Date-Civil",  # uppercase
        "feature/e1-s3-date",  # week needs 2 digits
        "feature/e1-s03",  # missing description
        "feature/a-b-c-d-e-f-g",  # more than 6 words
        "fix/typo",  # unknown type
        "release/bizdays-0.1",  # incomplete version
        "release/other-0.1.0",  # unknown package
        "support/bizdays-0.1.0",  # support ends in .x
    ],
)
def test_invalid_branch(name: str) -> None:
    assert not flow.valid_branch(name)


@pytest.mark.parametrize(
    ("head", "base", "ok"),
    [
        ("release/bizdays-0.1.0", "main", True),
        ("hotfix/bizdays-0.1.1", "main", True),
        ("feature/e1-s03-date-civil", "main", False),
        ("develop", "main", False),
        ("feature/e1-s03-date-civil", "develop", True),
        ("dependabot/uv/numpy-2.6", "develop", True),
        ("main", "develop", True),
        ("release/bizdays-0.1.0", "develop", True),
        ("hotfix/bizdays-0.1.1", "develop", False),
        ("spike/cum-u16", "develop", False),
        ("bugfix/rc-fix", "release/bizdays-0.1.0", True),
        ("feature/x", "release/bizdays-0.1.0", False),
        ("hotfix/bizdays-0.1.3", "support/bizdays-0.1.x", True),
        ("feature/x", "feature/y", False),
    ],
)
def test_allowed_pr(head: str, base: str, ok: bool) -> None:
    assert flow.allowed_pr(head, base) is ok


def test_manifest_version() -> None:
    for package in flow.MANIFESTS:
        assert flow.manifest_version(package)
