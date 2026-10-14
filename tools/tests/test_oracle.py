"""The fixture generator must be deterministic."""

import subprocess
import sys
from pathlib import Path

GENERATOR = Path(__file__).resolve().parents[1] / "oracle" / "generate_fixtures.py"


def test_generator_is_deterministic(tmp_path: Path) -> None:
    runs = []
    for name in ("a", "b"):
        out = tmp_path / name
        subprocess.run([sys.executable, str(GENERATOR), "--out", str(out)], check=True)
        runs.append({p.name: p.read_bytes() for p in sorted(out.iterdir())})
    assert runs[0].keys() == runs[1].keys()
    assert any(name.endswith(".csv") for name in runs[0])
    assert runs[0] == runs[1]
