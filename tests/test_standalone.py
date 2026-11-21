"""Exercise actual entry points from copied skill directories."""
import ast
import csv
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"


class StandaloneTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="skills stand-alone ")
        self.addCleanup(self.directory.cleanup)
        self.workspace = Path(self.directory.name)
        self.env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        self.env.update(PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")

    def copy(self, name):
        return shutil.copytree(SKILLS / name, self.workspace / name,
                               ignore=shutil.ignore_patterns("__pycache__", ".venv"))

    def invoke(self, skill, entry, *args):
        return subprocess.run([sys.executable, str(skill / "scripts" / entry), *map(str, args)],
                              cwd=self.workspace, env=self.env, capture_output=True, text=True,
                              encoding="utf-8", timeout=35, check=False)

    def json_result(self, skill, entry, *args, code=0):
        process = self.invoke(skill, entry, *args)
        self.assertEqual(process.returncode, code, process.stderr + process.stdout)
        return json.loads(process.stdout)

    def test_frontmatter_links_and_all_entry_help(self):
        folders = list(SKILLS.iterdir())
        self.assertEqual(len(folders), 9)
        for folder in folders:
            skill = self.copy(folder.name)
            spec = (skill / "SKILL.md").read_text(encoding="utf-8")
            header = spec.split("---", 2)[1]
            self.assertIn(f"\nname: {folder.name}\n", header)
            self.assertRegex(header, r"(?m)^description: .+")
            for path in re.findall(r"\]\((references/[^)]+)\)", spec):
                self.assertTrue((skill / path).is_file(), path)
            for entry in re.findall(r"scripts/([a-z_]+\.py)", spec):
                self.assertTrue((skill / "scripts" / entry).is_file(), entry)
            self.assertTrue((skill / "requirements.txt").is_file())
            commands = 0
            for path in (skill / "scripts").glob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                if not any(isinstance(node, ast.If) and "__main__" in ast.unparse(node.test)
                           for node in tree.body):
                    continue
                commands += 1
                with self.subTest(skill=folder.name, entry=path.name):
                    result = self.invoke(skill, path.name, "--help")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("usage:", result.stdout)
            self.assertGreater(commands, 0)

    def test_local_paper_export_selection_and_cleanup(self):
        skill = self.copy("literature-search")
        document = self.workspace / "samples & 中文.txt"
        document.write_text("A stable identifier\nFollowed by a second line.", encoding="utf-8")
        output = self.workspace / "results"
        response = self.json_result(skill, "import_papers.py", "--input", document, "--out-dir", output)
        catalog = Path(response["data"])
        paper = json.loads(catalog.read_text(encoding="utf-8"))["papers"][0]
        ident = paper["paper_id"]
        selection = self.workspace / "selection.json"
        selected = self.json_result(skill, "select_papers.py", "--input", catalog,
                                    "--paper-id", ident, "--selection", selection)
        self.assertEqual(selected["paper_ids"], [ident])
        self.assertEqual(self.json_result(skill, "select_papers.py", "--selection", selection)["paper_ids"], [ident])
        self.assertEqual(self.json_result(skill, "select_papers.py", "--clear",
                                          "--selection", selection)["paper_ids"], [])
        csv_file = self.workspace / "papers.csv"
        self.json_result(skill, "export_csv.py", "--input", catalog, "--output", csv_file,
                         "--fields", "paper_id", "title")
        with csv_file.open(encoding="utf-8", newline="") as handle:
            self.assertEqual(next(csv.DictReader(handle)), {"paper_id": ident, "title": document.stem})
        self.assertEqual(self.json_result(skill, "clean_csv.py", "--input", csv_file)["valid"], 1)

    def test_unicode_offsets_and_literal_search(self):
        skill = self.copy("paper-analysis")
        document = self.workspace / "论文.txt"
        document.write_text("结构 Si+Si；测试。", encoding="utf-8")
        response = self.json_result(skill, "read_segment.py", "--input", document,
                                    "--start", 3, "--length", 5)
        self.assertEqual(response["text"], "Si+Si")
        self.assertEqual(response["next_start"], 8)
        results = self.json_result(skill, "find_in_text.py", "--input", document, "--term", "Si+Si")
        self.assertEqual(results["matches"][0]["start"], 3)
        self.json_result(skill, "read_segment.py", "--input", document, "--start", -1, code=1)

    def test_missing_checkpoint_is_actionable(self):
        skill = self.copy("crystal-generation")
        result = self.json_result(skill, "generate_crystals.py", "--formula", "NaCl",
                                  "--model-dir", self.workspace, "--out-dir", self.workspace / "out", code=1)
        self.assertIn("ckpt.pt", result["error"])
        self.assertFalse((self.workspace / "out").exists())

    def test_temperature_is_enforced_before_loading_model(self):
        skill = self.copy("thermal-conductivity")
        result = self.json_result(skill, "predict_conductivity.py", "--input", "test.cif",
                                  "--model-dir", self.workspace, "--out-dir", self.workspace / "out",
                                  "--temperature", 500, code=1)
        self.assertIn("300 K", result["error"])
