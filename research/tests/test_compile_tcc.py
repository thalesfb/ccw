"""Regression protection for isolated, convergent TCC builds."""

import importlib.util
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("compile_tcc", ROOT / "scripts/compile_tcc.py")
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


def test_staging_excludes_old_include_aux_without_modifying_source(tmp_path):
    source = tmp_path / "repo/results/tcc"
    source.mkdir(parents=True)
    (source / "conteudo").mkdir()
    (source / "abnetx2").mkdir()
    (source / "main.tex").write_text("document", encoding="utf-8")
    (source / "conteudo/chapter.tex").write_text("chapter", encoding="utf-8")
    (source / "conteudo/chapter.aux").write_text("OBSOLETE", encoding="utf-8")
    (source / "main.toc").write_text("OBSOLETE", encoding="utf-8")
    (source / "main.pdf").write_bytes(b"old pdf")
    (source / "abnetx2/abntex2.cls").write_text("class", encoding="utf-8")
    references = tmp_path / "repo/research/exports/references"
    references.mkdir(parents=True)
    (references / "table.tex").write_text("generated table", encoding="utf-8")
    staged = BUILD.stage_sources(tmp_path / "repo", tmp_path / "stage")
    assert (staged / "conteudo/chapter.tex").is_file()
    assert (staged / "abntex2/abntex2.cls").is_file()
    assert not (staged / "conteudo/chapter.aux").exists()
    assert not (staged / "main.toc").exists()
    assert not (staged / "main.pdf").exists()
    assert (staged / "../../research/exports/references/table.tex").is_file()
    assert (source / "conteudo/chapter.aux").read_text() == "OBSOLETE"
    assert (source / "main.pdf").read_bytes() == b"old pdf"


def test_aux_fingerprint_detects_include_and_list_changes(tmp_path):
    (tmp_path / "conteudo").mkdir()
    aux = tmp_path / "conteudo/chapter.aux"
    aux.write_text("first", encoding="utf-8")
    initial = BUILD.aux_fingerprint(tmp_path)
    aux.write_text("second", encoding="utf-8")
    assert BUILD.aux_fingerprint(tmp_path) != initial
    stable = BUILD.aux_fingerprint(tmp_path)
    (tmp_path / "main.loq").write_text("new list", encoding="utf-8")
    assert BUILD.aux_fingerprint(tmp_path) != stable


def test_latex_gate_rejects_unresolved_references_and_rerun_requests():
    for log in ("LaTeX Warning: There were undefined references.",
                "LaTeX Warning: Label(s) may have changed. Rerun", "Rerun to get cross-references right"):
        with pytest.raises(RuntimeError):
            BUILD.validate_log(log)
    BUILD.validate_log("Output written on main.pdf (70 pages).")


def test_main_generates_study_codes_without_importing_analysis_package(monkeypatch, tmp_path):
    root = tmp_path / "repo"
    generated_calls = []
    compile_calls = []
    monkeypatch.setattr(BUILD.sys, "argv", [
        "compile_tcc.py", "--root", str(root), "--output", str(root / "results/tcc/main.pdf")
    ])
    monkeypatch.setattr(
        BUILD.subprocess,
        "run",
        lambda command, **kwargs: generated_calls.append((command, kwargs)),
    )
    monkeypatch.setattr(
        BUILD,
        "compile_document",
        lambda root, output, diagnostics: compile_calls.append((root, output, diagnostics)),
    )

    BUILD.main()

    assert generated_calls == [(
        [sys.executable, str(root / "research/src/analysis/study_codes.py")],
        {"cwd": root / "research", "check": True},
    )]
    assert compile_calls == [(root, root / "results/tcc/main.pdf", None)]
