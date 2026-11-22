"""Check the actual ZIP produced by Git or downloaded from a GitHub source release."""
from pathlib import Path, PurePosixPath
import sys
from zipfile import ZipFile


def check(archive):
    with ZipFile(archive) as bundle:
        names = {PurePosixPath(item.filename) for item in bundle.infolist() if not item.is_dir()}
    roots = [p.parents[3] for p in names if p.match(".agents/skills/*/SKILL.md")]
    if len(roots) != 9 or len(set(roots)) != 1:
        raise ValueError("Expected nine independent skill directories")
    for path in names:
        if (path.suffix.lower() in {".gguf", ".pt", ".pth", ".pyd", ".dll", ".exe", ".whl", ".so", ".dylib", ".zip", ".gz", ".tar", ".pyc"}
                or {".venv", "__pycache__", "site-packages"} & set(path.parts)):
            raise ValueError(f"Unexpected bundled artifact: {path}")
        if path.name == "SKILL.md":
            for child in ("scripts/run.ps1", "scripts/run.sh", "scripts/runtime.py", "references/runtime.json"):
                if path.parent / child not in names:
                    raise ValueError(f"Missing {path.parent / child}")
    if roots[0] / "tools/sync-runtime.py" not in names:
        raise ValueError("Maintenance sources missing from the archive")
    print(f"Verified nine source skills in {Path(archive).name}")


if __name__ == "__main__":
    check(sys.argv[1])
