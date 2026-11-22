"""Collect an isolated Windows Python dependency tree from trusted installed wheels."""

from importlib.metadata import distributions
from pathlib import Path, PurePosixPath
import shutil
import sys

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

PAPERS = ("pypdf", "python-docx", "fonttools")
FORCEFIELD = (
    "torch", "torchvision", "torchaudio", "numpy==2.2.6", "ase", "e3nn==0.5.8",
    "torch-geometric", "torchmetrics", "torch-ema", "torch-runstats",
    "deprecated", "seekpath", "loguru", "pymatgen==2025.6.14", "scikit-learn",
)
SKILL_DEPS = {
    "crystal-generation": ("torch", "numpy==2.2.6", "pymatgen==2025.6.14", "pandas"),
    "structure-optimization": FORCEFIELD,
    "phonon-analysis": (*FORCEFIELD, "phonopy", "matplotlib"),
    "thermal-conductivity": ("torch", "numpy==2.2.6", "pymatgen==2025.6.14", "scipy"),
    "materials-search": ("pymatgen==2025.6.14",),
    "literature-search": PAPERS,
    "paper-analysis": PAPERS,
    "research-report": PAPERS,
    "literature-knowledge": (*PAPERS, "chromadb"),
}


def find_packages(requirements, roots):
    candidates = {}
    for root in roots:
        for dist in distributions(path=[str(root)]):
            name = canonicalize_name(dist.metadata["Name"])
            candidates.setdefault(name, []).append(dist)
    remaining = [Requirement(requirement) for requirement in requirements]
    selected = {}
    expanded = set()
    while remaining:
        requirement = remaining.pop(0)
        name = canonicalize_name(requirement.name)
        if name in selected:
            dist = selected[name]
            if dist.version not in requirement.specifier:
                raise ValueError(f"Incompatible pinned wheel: {requirement}, found {dist.version}")
        else:
            dist = next((item for item in candidates.get(name, ())
                         if item.version in requirement.specifier), None)
            if dist is None:
                raise ValueError(f"Missing build dependency: {requirement}")
            if name == "torch" and "+cpu" not in dist.version:
                raise ValueError("Use an official +cpu PyTorch wheel for this package")
            selected[name] = dist
        marker = (name, frozenset(requirement.extras))
        if marker in expanded:
            continue
        expanded.add(marker)
        for raw in dist.requires or []:
            child = Requirement(raw)
            if child.marker is None or any(child.marker.evaluate({"extra": extra})
                                           for extra in ("", *requirement.extras)):
                remaining.append(child)
    return selected


def long_path(path):
    absolute = str(path.absolute())
    if sys.platform == "win32" and not absolute.startswith("\\\\?\\"):
        if absolute.startswith("\\\\"):
            return Path("\\\\?\\UNC\\" + absolute[2:])
        return Path("\\\\?\\" + absolute)
    return path

def install_packages(skill, roots, destination):
    packages = find_packages(SKILL_DEPS[skill], roots)
    for name, dist in sorted(packages.items()):
        if dist.files is None:
            raise ValueError(f"Missing wheel RECORD for {name}")
        for file in dist.files:
            relative = PurePosixPath(str(file))
            if relative.is_absolute() or ".." in relative.parts or "__pycache__" in relative.parts:
                continue
            if relative.suffix in {".pyc", ".pth"} or relative.name == "direct_url.json":
                continue
            source = long_path(Path(dist.locate_file(file)))
            if not source.is_file():
                raise ValueError(f"Wheel RECORD entry is missing: {name}/{file}")
            target = destination.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and source.read_bytes() != target.read_bytes():
                raise ValueError(f"Conflicting bundled dependencies at {relative}")
            shutil.copy2(source, target)
    return {name: dist.version for name, dist in sorted(packages.items())}
