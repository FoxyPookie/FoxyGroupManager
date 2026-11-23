"""Discover, import and report plugin modules."""
import importlib
import logging
from pathlib import Path

log=logging.getLogger("Foxy.plugins")
_loaded=set()

def discover():
    root=Path(__file__).resolve().parents[1]/"modules"
    return sorted(p.stem for p in root.glob("*.py") if p.name != "__init__.py" and not p.name.startswith("_"))

def load_all():
    loaded=[]
    for name in discover():
        if name in _loaded: continue
        try:
            importlib.import_module(f"Foxy.modules.{name}")
            _loaded.add(name); loaded.append(name)
        except Exception:
            log.exception("Plugin load failed: %s", name)
    return loaded

def loaded_plugins():
    return sorted(_loaded)
