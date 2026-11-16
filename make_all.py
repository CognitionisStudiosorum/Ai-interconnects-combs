"""Regenerate every figure and animation in figures/."""
import runpy
import sys
from pathlib import Path

SRC = Path(__file__).parent / "src"
sys.path.insert(0, str(SRC))

for script in sorted(SRC.glob("[0-9][0-9]_*.py")):
    print(f"--- {script.name}")
    runpy.run_path(str(script), run_name="__main__")
