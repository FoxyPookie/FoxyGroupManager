"""Auto-discover Python plugins in this directory."""
from pathlib import Path

ALL_MODULES = sorted(
    path.stem
    for path in Path(__file__).parent.glob("*.py")
    if path.name != "__init__.py" and not path.name.startswith("_")
)
