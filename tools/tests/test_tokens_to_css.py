"""tokens_to_css: DTCG tokens -> CSS custom properties."""

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "tokens_to_css",
    Path(__file__).resolve().parents[1] / "brand" / "tokens_to_css.py",
)
assert _spec and _spec.loader
tokens_to_css = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tokens_to_css)

TOKENS = {
    "color": {
        "$type": "color",
        "brandBlue": {"500": {"$value": "#123456"}},
        "semantic": {
            "light": {"surface": {"$value": "#ffffff"}},
            "dark": {"surface": {"$value": "{color.brandBlue.500}"}},
        },
    },
    "spacing": {"small": {"$type": "dimension", "$value": "4px"}},
}


def test_convert() -> None:
    css = tokens_to_css.convert(TOKENS)
    assert css.startswith("/* GERADO por just brand")
    root, default, slate = (
        css.split(":root {")[1].split("}")[0],
        css.split('[data-md-color-scheme="default"] {')[1].split("}")[0],
        css.split('[data-md-color-scheme="slate"] {')[1].split("}")[0],
    )
    assert "--sx-color-brand-blue-500: #123456;" in root
    assert "--sx-color-semantic-surface: #ffffff;" in default
    assert "--sx-color-semantic-surface: var(--sx-color-brand-blue-500);" in slate
    assert "spacing" not in css
