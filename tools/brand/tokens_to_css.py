"""Convert Syntaxis design tokens (DTCG tokens.json) into CSS custom properties.

- Every token with `$type: color` (own or inherited from its group) becomes
  `--sx-<path-in-kebab-case>`.
- Tokens whose path has a `light` or `dark` segment go to the Material color
  schemes (`default` / `slate`), with that segment removed from the name.
- Everything else goes to `:root`.
- Aliases such as `{color.blue.500}` become `var(--sx-color-blue-500)`.

Usage: python tools/brand/tokens_to_css.py TOKENS_JSON OUTPUT_CSS
Standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HEADER = "/* GERADO por just brand — não edite. Fonte: {source} */\n"
SCHEMES = {"light": "default", "dark": "slate"}


def kebab(segment: str) -> str:
    segment = re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", segment)
    return re.sub(r"[^a-zA-Z0-9]+", "-", segment).strip("-").lower()


def var_name(path: list[str]) -> str:
    return "--sx-" + "-".join(kebab(p) for p in path)


def css_value(value: object) -> str:
    if isinstance(value, dict) and "hex" in value:  # DTCG color object
        value = value["hex"]
    if not isinstance(value, str):
        raise ValueError(f"unsupported color value: {value!r}")
    alias = re.fullmatch(r"\{([^}]+)\}", value.strip())
    if alias:
        path = [p for p in alias.group(1).split(".") if p not in SCHEMES]
        return f"var({var_name(path)})"
    return value


def collect(node: dict, path: list[str], inherited_type: str | None, out: list) -> None:
    group_type = node.get("$type", inherited_type)
    if "$value" in node:
        if group_type == "color":
            out.append((path, css_value(node["$value"])))
        return
    for key, child in node.items():
        if not key.startswith("$") and isinstance(child, dict):
            collect(child, [*path, key], group_type, out)


def convert(tokens: dict, source: str = "tokens.json") -> str:
    found: list[tuple[list[str], str]] = []
    collect(tokens, [], None, found)
    blocks: dict[str, list[str]] = {":root": []}
    for scheme in SCHEMES.values():
        blocks[f'[data-md-color-scheme="{scheme}"]'] = []
    for path, value in found:
        modes = [p for p in path if p in SCHEMES]
        selector = f'[data-md-color-scheme="{SCHEMES[modes[0]]}"]' if modes else ":root"
        name = var_name([p for p in path if p not in SCHEMES])
        blocks[selector].append(f"  {name}: {value};")
    css = [HEADER.format(source=source)]
    for selector, lines in blocks.items():
        if lines:
            css.append(f"\n{selector} {{\n" + "\n".join(lines) + "\n}\n")
    return "".join(css)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    src, dst = Path(argv[1]), Path(argv[2])
    if not src.exists():
        print(
            f"{src} not found: copy the Syntaxis tokens.json there first",
            file=sys.stderr,
        )
        return 1
    css = convert(json.loads(src.read_text(encoding="utf-8")), source=src.as_posix())
    dst.write_text(css, encoding="utf-8")
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
