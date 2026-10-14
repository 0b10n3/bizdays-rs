"""Git Flow rules from docs/desenvolvimento/fluxo-git.md (branch names, PR flow).

Usage:
  python tools/git/flow.py branch NAME     # valid branch name? (section 2)
  python tools/git/flow.py pr HEAD BASE    # PR from HEAD into BASE allowed?
  python tools/git/flow.py version PACKAGE # print the manifest version

Exits 0 when allowed, 1 otherwise (with the reason on stderr).
Standard library only, Python >= 3.10.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRANCH_RE = re.compile(
    r"^((feature|bugfix|chore|data|spike)/(e[0-9]-s[0-9]{2}-|(?!e[0-9]-s))"
    r"[a-z0-9]+(-[a-z0-9]+){0,5}"
    r"|(release|hotfix)/bizdays(-rs)?-[0-9]+\.[0-9]+\.[0-9]+"
    r"|support/bizdays(-rs)?-[0-9]+\.[0-9]+\.x)$"
)
EXEMPT = ("main", "develop", "dependabot/")
# base prefix -> accepted head prefixes (section 2, "Origem e destino").
PR_FLOW = {
    "main": ("release/", "hotfix/"),
    "develop": (
        "feature/",
        "bugfix/",
        "chore/",
        "data/",
        "dependabot/",
        "main",
        "release/",
    ),
    "release/": ("bugfix/",),
    "support/": ("hotfix/",),
}
MANIFESTS = {
    "bizdays": ROOT / "crates" / "bizdays" / "Cargo.toml",
    "bizdays-rs": ROOT / "py-bizdays" / "Cargo.toml",
}


def _starts(name: str, prefix: str) -> bool:
    return name.startswith(prefix) if prefix.endswith("/") else name == prefix


def valid_branch(name: str) -> bool:
    return any(_starts(name, p) for p in EXEMPT) or bool(BRANCH_RE.match(name))


def allowed_pr(head: str, base: str) -> bool:
    for base_prefix, heads in PR_FLOW.items():
        if _starts(base, base_prefix):
            return any(_starts(head, h) for h in heads)
    return False


def manifest_version(package: str) -> str:
    text = MANIFESTS[package].read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', text, re.MULTILINE)
    if not match:
        raise ValueError(f"no version in {MANIFESTS[package]}")
    return match.group(1)


def main(argv: list[str]) -> int:
    match argv:
        case ["branch", name]:
            if valid_branch(name):
                return 0
            print(
                f"invalid branch name {name!r}; see docs/desenvolvimento/fluxo-git.md",
                file=sys.stderr,
            )
        case ["pr", head, base]:
            if allowed_pr(head, base):
                return 0
            print(
                f"PR {head} -> {base} is not allowed by the Git Flow table "
                "(docs/desenvolvimento/fluxo-git.md, section 2)",
                file=sys.stderr,
            )
        case ["version", package] if package in MANIFESTS:
            print(manifest_version(package))
            return 0
        case _:
            print(__doc__, file=sys.stderr)
            return 2
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
