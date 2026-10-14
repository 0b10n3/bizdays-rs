"""Claude Code PreToolUse hook: protect the learner zone (AGENTS.md, section 2).

Reads the hook JSON from stdin. If the target file is in the learner zone and
`.agent-implementation-mode` does not exist at the repository root, exits with
code 2 and a message on stderr (Claude Code blocks the tool call and shows the
message to the agent). Otherwise exits 0 silently.

Standard library only, Python >= 3.10.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path, PurePosixPath

FLAG = ".agent-implementation-mode"
LEARNER_ZONE = (
    "crates/bizdays/src/**",
    "crates/bizdays/tests/**",
    "crates/bizdays/benches/**",
    "py-bizdays/src/**",
    "py-bizdays/python/**",
    "py-bizdays/tests/**",
)
GENERATED = ("crates/bizdays/tests/fixtures/**",)


def _matches(rel: PurePosixPath, patterns: tuple[str, ...]) -> bool:
    return any(rel.is_relative_to(p.removesuffix("/**")) for p in patterns)


def in_learner_zone(rel: PurePosixPath) -> bool:
    return _matches(rel, LEARNER_ZONE) and not _matches(rel, GENERATED)


def main() -> int:
    try:
        event = json.load(sys.stdin)
        tool_input = event.get("tool_input") or {}
        target = tool_input.get("file_path") or tool_input.get("notebook_path")
    except (json.JSONDecodeError, AttributeError):
        return 0
    if not target:
        return 0

    root = Path(
        os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or "."
    ).resolve()
    path = Path(target)
    if not path.is_absolute():
        path = Path(event.get("cwd") or root) / path
    try:
        rel = PurePosixPath(path.resolve().relative_to(root).as_posix())
    except ValueError:  # outside the repository
        return 0

    if not in_learner_zone(rel) or (root / FLAG).exists():
        return 0

    print(
        f"Bloqueado: `{rel}` está na zona do aprendiz (AGENTS.md, seção 2).\n"
        "Aqui o mantenedor escreve o código. Explique o conceito, revise ou dê "
        "uma dica (escada de dicas, seção 2.2) em vez de editar.\n"
        "Para liberar, o mantenedor roda `just modo-implementacao on` "
        "(e `just modo-implementacao off` depois). Não contorne este bloqueio.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
