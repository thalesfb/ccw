"""Exercise canonical-PDF checks against disposable real Git repositories."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "check_canonical_pdf.py"


class CanonicalPdfTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Fixture Author")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.pdf = self.root / "results/tcc/main.pdf"
        self.pdf.parent.mkdir(parents=True)
        self.pdf.write_bytes(b"%PDF-1.4\nfixture\n")
        (self.pdf.parent / "main.tex").write_text("original source\n", encoding="utf-8")
        self.commit()

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(self.root), *args], text=True, stderr=subprocess.STDOUT
        ).strip()

    def commit(self) -> None:
        self.git("add", ".")
        self.git("commit", "-m", "fixture update")

    def check(self) -> subprocess.CompletedProcess[str]:
        before = (self.git("rev-parse", "HEAD"), self.git("status", "--porcelain"), self.pdf.read_bytes())
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.root)],
            capture_output=True, text=True, check=False,
        )
        after = (self.git("rev-parse", "HEAD"), self.git("status", "--porcelain"), self.pdf.read_bytes())
        self.assertEqual(before, after, "validation must not edit files or create commits")
        return result

    def test_current_pdf_passes_without_writing(self) -> None:
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_changed_committed_source_requires_manual_refresh(self) -> None:
        (self.pdf.parent / "main.tex").write_text("updated source\n", encoding="utf-8")
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("stale", result.stderr.lower())

    def test_dirty_source_is_not_treated_as_current(self) -> None:
        (self.pdf.parent / "main.tex").write_text("uncommitted source\n", encoding="utf-8")
        self.assertEqual(self.check().returncode, 1)

    def test_non_compilation_documents_do_not_require_pdf_refresh(self) -> None:
        (self.pdf.parent / "README.md").write_text("web documentation\n", encoding="utf-8")
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_public_overview_assets_do_not_require_pdf_refresh(self) -> None:
        images = self.pdf.parent / "images"
        images.mkdir()
        (images / "README.md").write_text("overview notes\n", encoding="utf-8")
        (images / "project_overview_2026-10-20.png").write_bytes(b"overview fixture\n")
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_manuscript_figures_still_require_pdf_refresh(self) -> None:
        images = self.pdf.parent / "images"
        images.mkdir()
        (images / "prisma_flow.png").write_bytes(b"figure fixture\n")
        self.commit()
        self.assertEqual(self.check().returncode, 1)

    def test_invalid_pdf_header_is_rejected(self) -> None:
        self.pdf.write_bytes(b"not a PDF\n")
        self.commit()
        self.assertEqual(self.check().returncode, 1)

    def test_uncommitted_pdf_is_rejected(self) -> None:
        self.pdf.write_bytes(b"%PDF-1.4\nnew uncommitted PDF\n")
        self.assertEqual(self.check().returncode, 1)

    def test_untracked_pdf_is_rejected(self) -> None:
        self.git("rm", "--cached", "results/tcc/main.pdf")
        self.assertEqual(self.check().returncode, 1)


if __name__ == "__main__":
    unittest.main()
