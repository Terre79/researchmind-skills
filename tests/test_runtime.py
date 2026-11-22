"""Portable entry point, isolation, diagnostics and retry regression tests."""
import json
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"


def launcher(skill, *args):
    if os.name == "nt":
        return [shutil.which("pwsh") or "powershell", "-NoProfile", "-File", str(skill / "scripts/run.ps1"), *args]
    return ["sh", str(skill / "scripts/run.sh"), *args]


class RuntimeTests(unittest.TestCase):
    def test_corrupt_or_interrupted_model_can_be_retried(self):
        module_spec = importlib.util.spec_from_file_location("runtime_assets", ROOT / "tools/runtime-template/runtime_assets.py")
        assets = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(assets)
        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch)
            target = path / "cache/model"
            source = path / "upstream"
            expected = b"verified model contents"
            spec = {"archive": source.name, "sha256": hashlib.sha256(expected).hexdigest()}
            with patch.dict(os.environ, RM_ASSET_DIR=scratch):
                source.write_bytes(b"incomplete")
                with self.assertRaisesRegex(ValueError, "SHA-256"):
                    assets.install_file(spec, target, True)
                self.assertFalse(target.exists())
                source.write_bytes(expected)
                self.assertTrue(assets.install_file(spec, target, True))
                target.write_bytes(b"corrupt cache")
                self.assertFalse(assets.install_file(spec, target, False))
                with patch.object(assets, "fetch", side_effect=OSError("interrupted")):
                    with self.assertRaisesRegex(OSError, "interrupted"):
                        assets.install_file(spec, target, True)
                self.assertEqual(list(target.parent.iterdir()), [target])
                self.assertTrue(assets.install_file(spec, target, True))
                source.unlink()
                self.assertTrue(assets.install_file(spec, target, False))
                self.assertEqual(target.read_bytes(), expected)

    def test_selected_provider_credentials(self):
        for skill, op, key, source in [
            ("materials-search", "search-materials", "MP_API_KEY", "mp"),
            ("literature-search", "search-papers", "TAVILY_API_KEY", "tavily"),
        ]:
            with tempfile.TemporaryDirectory() as scratch:
                env = dict(os.environ, RM_CACHE_DIR=str(Path(scratch) / "cache"))
                env.pop(key, None)
                result = subprocess.run(launcher(SKILLS / skill, "doctor", op, "--sources", source),
                                        env=env, capture_output=True)
                self.assertEqual(result.returncode, 3)
                self.assertIn(key, json.loads(result.stdout)["reason"])
                self.assertFalse(Path(env["RM_CACHE_DIR"]).exists())

    def test_single_directory(self):
        with tempfile.TemporaryDirectory(prefix="技能 test ") as temp:
            path = Path(temp)
            skill = path / "standalone"
            shutil.copytree(SKILLS / "paper-analysis", skill)
            env = dict(os.environ, RM_CACHE_DIR=str(path / "cache"), PYTHONUTF8="1")
            source = path / "输入 A.txt"
            source.write_text("source citation A", encoding="utf8")
            args = ["extract-text", "--input", source.name, "--out-dir", "输出 A"]
            def call(action):
                result = subprocess.run(launcher(skill, action, *args), env=env, cwd=path,
                                      capture_output=True, text=True, encoding="utf8")
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                return result
            self.assertEqual(json.loads(call("doctor").stdout)["status"], "ready")
            self.assertFalse((path / "cache").exists())
            for _ in range(2):
                self.assertEqual(json.loads(call("run").stdout)["paper_count"], 1)
            self.assertEqual((path / "输出 A/paper.txt").read_text().strip(), "source citation A")
            self.assertFalse((path / "cache").exists())

    def test_every_cli_is_mapped(self):
        for skill in SKILLS.iterdir():
            config = json.loads((skill / "references/runtime.json").read_text(encoding="utf8"))
            entries = {p.name for p in (skill / "scripts").glob("*.py") if p.name not in {"runtime.py", "build_matter_windows.py"}
                       and "if __name__" in p.read_text(encoding="utf8")}
            self.assertEqual(entries, {s["script"] for s in config["operations"].values()}, skill.name)
            self.assertIn("scripts", (skill / "SKILL.md").read_text(encoding="utf8"))
            for spec in config["assets"].values():
                for asset in spec:
                    self.assertRegex(asset["sha256"], "^[a-f0-9]{64}$")
                    self.assertNotIn("/Terre79/researchmind-skills/releases", asset["url"])

    def test_diagnostic_missing_then_blocked_credentials(self):
        with tempfile.TemporaryDirectory() as temp:
            skill = SKILLS / "paper-analysis"
            env = dict(os.environ, RM_CACHE_DIR=str(Path(temp) / "absent"), RM_CHAT_BACKEND="remote")
            env.pop("OPENAI_API_KEY", None)
            for op, expected in [("extract-text", "missing"), ("analyze-paper", "blocked")]:
                args = ["--input", "file.pdf"] if op == "extract-text" else []
                result = subprocess.run(launcher(skill, "doctor", op, "--json", *args), env=env,
                                        capture_output=True, text=True, encoding="utf8")
                self.assertEqual(json.loads(result.stdout)["status"], expected)
                self.assertNotEqual(result.returncode, 0)
            self.assertFalse(Path(env["RM_CACHE_DIR"]).exists())

    def test_shared_sources(self):
        subprocess.run([sys.executable, str(ROOT / "tools/sync-runtime.py"), "--check"], check=True)


if __name__ == "__main__":
    unittest.main()
