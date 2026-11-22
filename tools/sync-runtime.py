"""Keep individually installable skills in sync with their maintained launcher and locks."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    mismatches = []
    for skill in sorted((ROOT / ".agents/skills").iterdir()):
        config = json.loads((skill / "references/runtime.json").read_text(encoding="utf8"))
        copies = [(p, skill / "scripts" / p.name) for p in (ROOT / "tools/runtime-template").glob("*") if p.is_file() and (p.name != "build_matter_windows.py" or skill.name in ("phonon-analysis", "structure-optimization"))]
        profiles = {s.get("profile") for s in config["operations"].values()} - {None}
        if "by-input" in profiles:
            profiles.remove("by-input")
            profiles.update(["pdf", "docx", "documents"])
        for profile in sorted(profiles):
            for name in ("pyproject.toml", "uv.lock"):
                copies.append((ROOT / "tools/profiles" / profile / name, skill / "references/locks" / profile / name))
        for source, dest in copies:
            data = source.read_bytes()
            if dest.is_file() and dest.read_bytes() == data:
                continue
            if args.check:
                mismatches.append(str(dest.relative_to(ROOT)))
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
    if mismatches:
        sys.exit("Run tools/sync-runtime.py: " + ", ".join(mismatches))


if __name__ == "__main__":
    main()
