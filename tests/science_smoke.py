"""End-to-end CPU tasks through installed source skill launchers. Uses real providers/models."""
import argparse
import csv
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile

from test_runtime import SKILLS, launcher


def silicon(path, perturb=False):
    coords = [(0,0,0),(0,.5,.5),(.5,0,.5),(.5,.5,0),(.25,.25,.25),
              (.25,.75,.75),(.75,.25,.75),(.75,.75,.25)]
    text = """data_silicon
_cell_length_a 5.431
_cell_length_b 5.431
_cell_length_c 5.431
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_symmetry_space_group_name_H-M 'P 1'
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
"""
    for i, (x,y,z) in enumerate(coords):
        text += f"Si{i+1} Si {x+(.02 if perturb and i==0 else 0)} {y} {z}\n"
    path.write_text(text)


def pdf(path):
    stream = b"BT /F1 12 Tf 40 700 Td (Silicon has a diamond structure.) Tj ET"
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
               b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
               b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"]
    buf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(buf))
        buf.extend(f"{i} 0 obj\n".encode() + obj + b"\nendobj\n")
    start = len(buf)
    buf.extend(b"xref\n0 6\n0000000000 65535 f \n")
    for n in offsets[1:]:
        buf.extend(f"{n:010d} 00000 n \n".encode())
    buf.extend(f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{start}\n%%EOF".encode())
    path.write_bytes(buf)


def verify(name, run, folder):
    output = ["--out-dir", "result"]
    if name == "crystal-generation":
        r = run("generate-crystals", "--formula", "NaCl", "--num-samples", "1", "--seed", "1337", *output)
        assert run("validate-cif", "--input", "result/" + r["structures"][0]["cif"])["formula"] == "NaCl"
    elif name == "structure-optimization":
        r = run("calculate-energy", "--input", "Si.cif", *output)
        assert math.isfinite(r["energy_eV"]) and r["sites"] == 8
        r = run("relax-structure", "--input", "distorted.cif", *output)
        assert r["converged"] and r["final_max_force_eV_A"] < r["initial_max_force_eV_A"]
    elif name == "phonon-analysis":
        r = run("calculate-phonon", "--input", "Si.cif", "--supercell","2","2","2", *output)
        with Path(r["csv"]).open(encoding="utf8", newline="") as f:
            values = [float(row["frequency_THz"]) for row in csv.DictReader(f)]
        assert len(values) == r["frequency_values"] > 0 and all(map(math.isfinite, values))
        assert Path(r["plot"]).read_bytes().startswith(b"\x89PNG")
    elif name == "thermal-conductivity":
        r = run("predict-conductivity", "--input", "Si.cif", "--method", "both", *output)
        assert {v["method"] for v in r["results"]} == {"kappa_p","kappa_mtp"}
        assert all(math.isfinite(v["thermal_conductivity_W_mK"]) and v["thermal_conductivity_W_mK"] > 0 for v in r["results"])
    elif name == "materials-search":
        r = run("search-materials", "--formula", "Si", "--sources", "oqmd", "--limit", "1", *output)
        rows = json.loads(Path(r["data"]).read_text(encoding="utf8"))["records"]
        assert rows[0]["source_id"] and (folder / "result" / rows[0]["cif"]).is_file()
    elif name == "literature-search":
        r = run("import-papers", "--input", "input.pdf", *output)
        assert r["paper_count"] == 1 and Path(r["csv"]).is_file()
        r = run("plan-search", "--query", "Find studies on silicon crystal structures.", "--max-tokens","160", *output)
        assert Path(r["report"]).stat().st_size > 20
    elif name == "paper-analysis":
        r = run("extract-text", "--input", "input.pdf", *output)
        assert "diamond" in (folder / "result/paper.txt").read_text()
        r = run("analyze-paper","--papers","papers.json","--paper-id","Si1","--instruction","Summarize the structure in one sentence.","--max-tokens","200",*output)
        assert r["analyzed"] == 1 and (folder / "result/analysis.md").is_file()
    elif name == "research-report":
        r = run("write-report","--papers","papers.json","--paper-id","Si1","--topic","Silicon structure","--language","English","--max-tokens","300",*output)
        assert r["citations"] == ["Si1"] and "[Si1]" in Path(r["report"]).read_text(encoding="utf8")
    else:
        index = ["--index-dir","index","--collection","materials","--chunk-size","512"]
        r = run("index-papers","--papers","papers.json",*index)
        assert len(r["paper_ids"]) == 2
        r = run("search-knowledge","--query","silicon diamond crystal structure","--top-k","2",*index)
        assert any(m["paper_id"] == "Si1" and m["end"] > m["start"] for m in r["matches"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="+", choices=sorted(p.name for p in SKILLS.iterdir()))
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args()
    for name in args.skills:
        with tempfile.TemporaryDirectory(prefix="RM source ") as scratch:
            folder = Path(scratch)
            skill = folder / name
            shutil.copytree(SKILLS / name, skill)
            silicon(folder / "Si.cif")
            silicon(folder / "distorted.cif", True)
            pdf(folder / "input.pdf")
            papers = {"papers": [{"paper_id":"Si1","title":"Silicon crystal","abstract":"Silicon at ambient pressure forms a diamond cubic crystal structure."},
                                 {"paper_id":"Al2","title":"Liquid aluminum","abstract":"Molten aluminum is a conducting liquid."}]}
            (folder / "papers.json").write_text(json.dumps(papers))
            def run(op, *values):
                result = subprocess.run(launcher(skill,"run",op,*values), cwd=folder, stdout=subprocess.PIPE, check=True)
                data = json.loads(result.stdout)
                assert data.get("status") == "completed", data
                return data
            for iteration in range(args.repeat):
                verify(name, run, folder)
                print(f"PASS {name} {iteration+1}", flush=True)


if __name__ == "__main__":
    main()
