"""Verify one published ZIP using its embedded interpreter and actual local workflows."""

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from zipfile import ZipFile


def digest(file):
    with file.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def extract(archive, destination):
    with ZipFile(archive) as bundle:
        root, = {name.split("/")[0] for name in bundle.namelist()}
        manifest = json.loads(bundle.read(root + "/bundle-manifest.json"))
        expected = {root + "/" + path for path in manifest["files"]}
        assert expected == set(bundle.namelist()) - {root + "/bundle-manifest.json"}
        for name in bundle.namelist():
            candidate = destination / name
            assert candidate.resolve().is_relative_to(destination.resolve()), name
        bundle.extractall(destination)
    skill = destination / root
    assert manifest["skill"] == root
    assert all(digest(skill / path) == sha for path, sha in manifest["files"].items())
    return skill, root


def call(skill, workspace, online, script, *args):
    system_root = os.environ.get("SystemRoot", r"C:\Windows")
    env = {key: os.environ[key] for key in ("SystemRoot", "WINDIR", "TEMP", "TMP", "USERPROFILE",
                                           "LOCALAPPDATA", "APPDATA") if key in os.environ}
    env.update(PATH=str(Path(system_root) / "System32"), OMP_NUM_THREADS="2", MKL_NUM_THREADS="2")
    if online:
        for variable in ("HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY"):
            if variable in os.environ:
                env[variable] = os.environ[variable]
    else:
        for variable in ("HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY"):
            env[variable] = "http://127.0.0.1:1"
    result = subprocess.run([str(skill / "python" / "python.exe"), "-X", "utf8",
                             str(skill / "scripts" / script), *map(str, args)],
                            cwd=workspace, env=env, capture_output=True, text=True,
                            encoding="utf-8", timeout=600, check=False)
    if result.returncode:
        raise RuntimeError(f"{script} returned {result.returncode}: {result.stdout}\n{result.stderr}")
    output = json.loads(result.stdout)
    assert output["status"] == "completed", output
    return output


def science(name, run, workspace, fixtures):
    output = workspace / "result"
    silicon = fixtures / "clean-si.cif"
    if name == "crystal-generation":
        result = run("generate_crystals.py", "--formula", "NaCl", "--num-samples", 2,
                     "--seed", 1337, "--out-dir", output)
        paths = [output / row["cif"] for row in result["structures"]]
        assert len(paths) == 2 and len({digest(path) for path in paths}) == 2
        for path in paths:
            row = run("validate_cif.py", "--input", path)
            assert row["formula"] == "NaCl" and row["sites"] >= 2 and row["volume_A3"] > 0
        return {"candidates": len(paths), "device": result["device"], "sha256": [digest(path) for path in paths]}
    if name == "structure-optimization":
        energy = run("calculate_energy.py", "--input", silicon, "--out-dir", output)
        relaxation = run("relax_structure.py", "--input", fixtures / "perturbed-si.cif",
                         "--max-steps", 60, "--out-dir", output)
        assert math.isfinite(energy["energy_eV"]) and relaxation["converged"]
        assert relaxation["final_max_force_eV_A"] < relaxation["initial_max_force_eV_A"]
        assert run("validate_cif.py", "--input", relaxation["structure"])["sites"] == energy["sites"]
        return {"energy_eV": energy["energy_eV"], "initial_force": relaxation["initial_max_force_eV_A"],
                "final_force": relaxation["final_max_force_eV_A"]}
    if name == "phonon-analysis":
        result = run("calculate_phonon.py", "--input", silicon, "--out-dir", output)
        assert Path(result["plot"]).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        with Path(result["csv"]).open(encoding="utf-8", newline="") as stream:
            frequencies = [float(row["frequency_THz"]) for row in csv.DictReader(stream)]
        assert len(frequencies) == result["frequency_values"] > 0 and all(map(math.isfinite, frequencies))
        return {"frequency_values": len(frequencies), "unit": result["frequency_unit"]}
    if name == "materials-search":
        result = run("search_materials.py", "--formula", "Si", "--sources", "oqmd", "--limit", 2,
                     "--out-dir", output)
        rows = json.loads(Path(result["data"]).read_text(encoding="utf-8"))["records"]
        assert len(rows) == 2 and result["structures"] == 2
        assert all((output / row["cif"]).is_file() and row["source"] == "oqmd" for row in rows)
        return {"records": len(rows), "source": "oqmd", "structures": result["structures"]}
    result = run("predict_conductivity.py", "--input", silicon, "--out-dir", output)
    assert {row["method"] for row in result["results"]} == {"kappa_p", "kappa_mtp"}
    assert all(math.isfinite(row["thermal_conductivity_W_mK"]) and row["thermal_conductivity_W_mK"] > 0
               for row in result["results"])
    return {"methods": 2, "temperature_K": 300}


def literature(name, run, workspace, fixtures):
    output = workspace / "result"
    pdf = fixtures / "acceptance-paper.pdf"
    paper_id = "cond-mat/0211520v2"
    if name == "literature-search":
        imported = run("import_papers.py", "--input", pdf, "--out-dir", output)
        plan = run("plan_search.py", "--query", "Suggest search terms for perovskite charge order. Keep it short.",
                   "--max-tokens", 400, "--out-dir", output)
        assert imported["paper_count"] == 1 and Path(imported["csv"]).is_file()
        assert Path(plan["report"]).stat().st_size > 100
        return {"imported": 1, "plan_model": plan["inference"]["model"]}
    papers = workspace / "papers.json"
    papers.write_text(json.dumps({"papers": [
        {"paper_id": paper_id, "title": "Two-dimensional charge order in layered 2-1-4 perovskite oxides",
         "content_file": str(pdf), "url": "https://arxiv.org/abs/" + paper_id},
        {"paper_id": "2601.11793v1", "title": "Optical constants for metal halide perovskites",
         "content_file": str(fixtures / "standalone-evidence" / "text" / "0002.txt")},
    ]}), encoding="utf-8")
    if name == "paper-analysis":
        extract = run("extract_text.py", "--input", pdf, "--out-dir", output / "text")
        extracted = run("read_segment.py", "--input", output / "text" / "paper.txt", "--length", 512)
        assert "charge order" in extracted["text"].lower()
        result = run("analyze_paper.py", "--papers", papers, "--paper-id", paper_id, "--language", "English",
                     "--instruction", "Use three sentences in your own words", "--max-characters", 2800,
                     "--max-tokens", 800, "--out-dir", output)
        assert extract["paper_count"] == result["analyzed"] == 1 and (output / "analysis.md").is_file()
        return {"analyzed": result["analyzed"], "extracted_characters": extracted["total_length"]}
    if name == "research-report":
        result = run("write_report.py", "--papers", papers, "--paper-id", paper_id,
                     "--topic", "Charge-order evidence in layered perovskites", "--language", "English",
                     "--max-characters", 1800, "--max-tokens", 1000, "--out-dir", output)
        text = Path(result["report"]).read_text(encoding="utf-8")
        assert result["citations"] == [paper_id] and f"[{paper_id}]" in text
        assert "charge" in text.lower()
        return {"citations": result["citations"], "model": result["inference"]["model"]}
    index = workspace / "index"
    result = run("index_papers.py", "--papers", papers, "--index-dir", index, "--chunk-size", 512)
    assert len(result["paper_ids"]) == 2 and result["chunks"] > 0
    zh = run("search_knowledge.py", "--index-dir", index, "--chunk-size", 512,
             "--query", "二维电荷有序 层状氧化物", "--top-k", 2)
    en = run("search_knowledge.py", "--index-dir", index, "--chunk-size", 512,
             "--query", "two dimensional charge order in layered oxides", "--top-k", 2)
    for retrieval in (zh, en):
        assert any(row["paper_id"] == paper_id for row in retrieval["matches"])
        assert all(row["end"] > row["start"] for row in retrieval["matches"])
    return {"indexed": 2, "chunks": result["chunks"], "queries": ["zh", "en"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--online", action="store_true", help="Required for materials-search")
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    with TemporaryDirectory(prefix="验证 Skill ", dir=args.scratch) as temporary:
        workspace = Path(temporary).resolve()
        skill, name = extract(args.archive.resolve(), workspace)
        if (name == "materials-search") != args.online:
            parser.error("Only materials-search needs --online")

        def run(entry, *values):
            return call(skill, workspace, args.online, entry, *values)

        workflow = literature if name.startswith(("literature-", "paper-", "research-")) else science
        result = workflow(name, run, workspace, args.fixtures.resolve())
        print(json.dumps({"skill": name, "archive_sha256": digest(args.archive),
                          "details": result}, ensure_ascii=True))


if __name__ == "__main__":
    main()
