
from pathlib import Path

def ensure_dir(p: str | Path) -> Path:
    path = Path(p)
    path.mkdir(parents=True, exist_ok=True)
    return path

def project_root() -> Path:
    return Path(__file__).resolve().parents[2]

def reports_dir(base: str | Path) -> Path:
    return ensure_dir(base)
