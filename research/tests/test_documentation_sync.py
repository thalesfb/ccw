"""Exercise documentation synchronization, not scientific adjudication."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "sync_project_docs", ROOT / "scripts/sync_project_docs.py"
)
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


@pytest.fixture
def project(tmp_path):
    for relative in sync.INPUTS:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    for relative, names in sync.TARGETS.items():
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "Historical snapshot: 17 included.\n\n"
            + "\n\n".join(sync.marker(name, "stale") for name in names)
            + "\n\nManual interpretation stays here.\n",
            encoding="utf-8",
        )
    for relative in sync.REVIEW_TARGETS:
        target = tmp_path / relative
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"A manually reviewed summary or image.\n")
    return tmp_path


def test_goals_are_extracted_from_the_manuscript_not_retyped(project):
    blocks = sync.render_blocks(project)
    assert "Propor uma especificação técnica e pedagógica" in blocks["goals"]
    assert all(f"**OE{i}:**" in blocks["goals"] for i in range(1, 5))
    assert "**OE5:**" not in blocks["goals"]
    assert "viabilidade e a coerência da especificação conceitual" in blocks["goals"]
    intro = project / sync.INTRO
    intro.write_text(intro.read_text(encoding="utf-8").replace(
        "Propor uma especificação", "Documentar uma especificação", 1
    ), encoding="utf-8")
    assert "Documentar uma especificação" in sync.render_blocks(project)["goals"]


def test_generated_blocks_update_all_consumers_and_preserve_manual_history(project):
    assert sync.synchronize(project, write=False)
    sync.synchronize(project, write=True)
    assert sync.synchronize(project, write=False) == []
    blocks = sync.render_blocks(project)
    for relative, names in sync.TARGETS.items():
        text = (project / relative).read_text(encoding="utf-8")
        assert "Historical snapshot: 17 included." in text
        assert "Manual interpretation stays here." in text
        for name in names:
            assert sync.marker(name, blocks[name]) in text


def test_source_table_reflects_available_pdfs_without_changing_inclusion(project):
    blocks = sync.render_blocks(project)
    assert "16 de 18" in blocks["coverage"]
    assert "3 e 6923" in blocks["coverage"]
    assert "12 fontes" in blocks["coverage"] and "484" in blocks["coverage"]
    assert "15 estudos empíricos mantidos provisoriamente" in blocks["snapshot"]
    assert "85,62%" in blocks["sources"]
    assert "1–5" in blocks["sources"]
    assert "nenhuma" in blocks["sources"]


def test_write_does_not_silently_approve_manual_summaries(project):
    sync.synchronize(project, write=True)
    assert sync.review_issues(project)
    sync.record_review(project)
    assert sync.review_issues(project) == []
    intro = project / sync.INTRO
    intro.write_text(intro.read_text(encoding="utf-8").replace(
        "Propor uma especificação", "Documentar uma especificação", 1
    ), encoding="utf-8")
    sync.synchronize(project, write=True)
    assert "canonical inputs changed" in " ".join(sync.review_issues(project))


def test_review_binding_detects_changes_to_manual_text_and_binary_images(project):
    sync.synchronize(project, write=True)
    sync.record_review(project)
    for relative in ("presentation/slides.md", sync.OVERVIEW):
        target = project / relative
        original = target.read_bytes()
        target.write_bytes(original + b"changed")
        assert relative in " ".join(sync.review_issues(project))
        target.write_bytes(original)
    assert sync.review_issues(project) == []


def test_review_record_does_not_claim_human_or_scientific_approval(project):
    sync.synchronize(project, write=True)
    sync.record_review(project)
    record = json.loads((project / sync.REVIEW_RECORD).read_text(encoding="utf-8"))
    assert record["human_scientific_approval"] == "pending"
    assert record["review_kind"] == "assisted_consistency_review"


def test_bad_markers_fail_before_any_document_is_written(project):
    targets = list(sync.TARGETS)
    damaged = project / targets[-1]
    damaged.write_text("missing markers", encoding="utf-8")
    first = project / targets[0]
    original = first.read_bytes()
    with pytest.raises(ValueError, match="marker"):
        sync.synchronize(project, write=True)
    assert first.read_bytes() == original


def test_cannot_record_review_with_stale_generated_text(project):
    with pytest.raises(ValueError, match="stale"):
        sync.record_review(project)
    assert not (project / sync.REVIEW_RECORD).exists()


def test_cli_check_is_read_only_and_fails_until_synchronized_and_reviewed(project):
    def run(*args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/sync_project_docs.py"),
             "--root", str(project), *args],
            capture_output=True, text=True, encoding="utf-8",
        )

    before = {relative: (project / relative).read_bytes()
              for relative in sync.REVIEW_TARGETS}
    assert run("--check").returncode == 1
    assert {relative: (project / relative).read_bytes()
            for relative in sync.REVIEW_TARGETS} == before
    assert run("--write").returncode == 0
    assert run("--check").returncode == 1
    assert run("--record-review").returncode == 0
    assert run("--check").returncode == 0


def test_checked_in_documents_are_synchronized_and_review_bound():
    assert sync.synchronize(ROOT, write=False) == []
    assert sync.review_issues(ROOT) == []


def test_current_scope_and_historical_warning_notes_are_review_bound():
    assert {"docs/TCC_REVISION_SCOPE.md", "docs/VERIFICACAO-NUMEROS-PRISMA.md",
            "docs/tcc/NORMATIVE_GOVERNANCE.md"} <= set(sync.REVIEW_TARGETS)


def test_documented_offline_command_uses_the_declared_api_test_marker():
    configuration = (ROOT / "research/pytest.ini").read_text(encoding="utf-8")
    assert "integration: integration tests (require API access)" in configuration
    for relative in ("README.md", "research/README.md"):
        document = (ROOT / relative).read_text(encoding="utf-8")
        assert '-m "not integration"' in document
        assert '-m "not network"' not in document
