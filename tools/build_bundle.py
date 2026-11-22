"""Build one movable and self-contained Windows x64 CPU Agent Skill ZIP."""

import argparse
import json
from pathlib import Path
import shutil
import struct
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED

from bundle_assets import CHAT_SKILLS, ENGINE, ENGINE_HASH, MATTER_SKILLS, PYTHON, PYTHON_HASH
from bundle_assets import checked, copy_models, sha256
from windows_deps import SKILL_DEPS, install_packages, long_path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
SKILL_IGNORES = shutil.ignore_patterns("__pycache__", "*.pyc", "models", "python", "engine", "results")


def embedded_python(asset, destination):
    with ZipFile(checked(asset, PYTHON_HASH)) as archive:
        archive.extractall(destination)
    settings = "python312.zip\n.\nLib\\site-packages\n..\\scripts\n"
    (destination / "python312._pth").write_text(settings, encoding="ascii", newline="\n")


def inference_engine(assets, destination):
    destination.mkdir()
    with ZipFile(checked(assets / ENGINE, ENGINE_HASH)) as archive:
        for entry in archive.namelist():
            name = Path(entry).name
            if name.endswith(".dll") or name == "llama-server.exe" or name.startswith("LICENSE"):
                with archive.open(entry) as source, (destination / name).open("wb") as output:
                    shutil.copyfileobj(source, output)
    shutil.copyfile(assets / "llama.cpp-LICENSE", destination / "LICENSE-llama.cpp")
    shutil.copyfile(assets / "Apache-2.0.txt", destination / "LICENSE-model-Apache-2.0")


def install_matter(source, destination):
    package = source / "src" / "mattersim"
    extension = package / "datasets" / "utils"
    if not list(extension.glob("threebody_indices*.pyd")):
        raise ValueError("Compile the MatterSim 1.2.2 CPython 3.12 x64 extension first")
    shutil.copytree(package, destination / "mattersim",
                    ignore=shutil.ignore_patterns("__pycache__", "*.c", "*.pyx", "*.lib", "*.pdb"))
    shutil.copyfile(source / "LICENSE.txt", destination / "mattersim" / "LICENSE.txt")


def build(args):
    if sys.platform != "win32" or sys.version_info[:2] != (3, 12) or struct.calcsize("P") != 8:
        raise RuntimeError("Build on Windows using CPython 3.12 x64")
    if args.skill == "thermal-conductivity" and not args.kappa_permission:
        raise ValueError("AI4Kappa redistribution requires written permission from the rights holder")
    if args.skill in MATTER_SKILLS and not args.mattersim_source:
        raise ValueError("Provide the compiled official MatterSim 1.2.2 source directory")
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / f"{args.skill}-win-x64-cpu-{args.version}.zip"
    with TemporaryDirectory(prefix="bundle-", dir=long_path(args.output)) as temporary:
        stage = long_path(Path(temporary) / args.skill)
        shutil.copytree(SKILLS / args.skill, stage, ignore=SKILL_IGNORES)
        python = stage / "python"
        embedded_python(args.assets / PYTHON, python)
        dependencies = install_packages(args.skill, args.wheels, python / "Lib" / "site-packages")
        if args.skill in MATTER_SKILLS:
            install_matter(args.mattersim_source, python / "Lib" / "site-packages")
            dependencies["mattersim"] = "1.2.2"
        if args.skill in CHAT_SKILLS or args.skill == "literature-knowledge":
            inference_engine(args.assets, stage / "engine")
        if args.skill == "thermal-conductivity":
            licenses = stage / "licenses"
            licenses.mkdir()
            shutil.copyfile(args.kappa_permission, licenses / "AI4Kappa.txt")
        copy_models(args.skill, args.assets, stage)
        metadata = {
            "version": args.version, "skill": args.skill, "platform": "windows-x64-cpu",
            "python": "3.12.10", "dependencies": dependencies,
            "files": {file.relative_to(stage).as_posix(): sha256(file)
                      for file in sorted(stage.rglob("*")) if file.is_file()},
        }
        (stage / "bundle-manifest.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        packed = Path(temporary) / archive.name
        with ZipFile(packed, "w", compression=ZIP_DEFLATED, compresslevel=3) as bundle:
            for file in sorted(stage.rglob("*")):
                if file.is_file():
                    bundle.write(file, file.relative_to(stage.parent))
        packed.replace(long_path(archive))
    print(f"{sha256(archive)}  {archive.name}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", required=True, choices=SKILL_DEPS)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--wheels", type=Path, nargs="+", required=True, help="Trusted pip target directories")
    parser.add_argument("--mattersim-source", type=Path)
    parser.add_argument("--kappa-permission", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version", default="v1")
    args = parser.parse_args()
    if not args.version.isascii() or not args.version.replace(".", "").replace("-", "").isalnum():
        parser.error("Use a simple alphanumeric release version")
    build(args)


if __name__ == "__main__":
    main()
