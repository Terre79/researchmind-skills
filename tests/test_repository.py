from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
IGNORE = {".git"}


class RepositoryTests(unittest.TestCase):
    def test_versioned_text_file_line_limit(self):
        result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True)
        count = 0
        for name in result.stdout.decode("utf-8").split("\0"):
            if not name:
                continue
            file = ROOT / name
            if not file.is_file():
                continue
            lines = len(file.read_text(encoding="utf-8-sig").splitlines())
            self.assertLessEqual(lines, 500, f"{name} has {lines} physical lines")
            count += 1
        self.assertGreater(count, 0)
