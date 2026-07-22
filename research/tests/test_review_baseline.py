import json
from datetime import UTC, datetime
from pathlib import Path

from src.validation.review_baseline import (
    build_review_manifest,
    compare_corpora,
    read_bibtex_corpus,
    verify_review_manifest,
)


def test_build_manifest_hashes_artifacts_and_extracts_corpus(tmp_path: Path) -> None:
    bib = tmp_path / "included.bib"
    bib.write_text(
        "@article{Alpha, title={First Study}, year={2024}, doi={10.1/alpha}}\n"
        "@article{Beta, title={Second Study}, year={2025}}\n",
        encoding="utf-8",
    )
    table = tmp_path / "table.csv"
    table.write_text("key,status\nAlpha,yes\nBeta,no\n", encoding="utf-8")
    config = {
        "baseline_id": "review-test",
        "source_commit": "a" * 40,
        "corpus_bib": "included.bib",
        "artifacts": ["included.bib", "table.csv"],
        "reported_counts": {"included": 2},
        "temporal_scope": {
            "status": "discrepancy",
            "methodology": "2016-2025",
            "readme": "2015-2025",
        },
    }

    manifest = build_review_manifest(
        config=config,
        repository_root=tmp_path,
        generated_at=datetime(2026, 7, 22, 12, 0, tzinfo=UTC),
    )

    assert manifest["baseline_id"] == "review-test"
    assert manifest["generated_at"] == "2026-07-22T12:00:00+00:00"
    assert manifest["corpus"]["entry_count"] == 2
    assert [entry["key"] for entry in manifest["corpus"]["entries"]] == [
        "Alpha",
        "Beta",
    ]
    assert manifest["artifacts"][0]["sha256"]
    assert manifest["temporal_scope"]["status"] == "discrepancy"
    assert verify_review_manifest(manifest, tmp_path) == []


def test_verify_manifest_detects_changed_artifact(tmp_path: Path) -> None:
    bib = tmp_path / "included.bib"
    bib.write_text("@article{Alpha,title={First},year={2024}}\n", encoding="utf-8")
    manifest = build_review_manifest(
        config={
            "baseline_id": "review-test",
            "source_commit": "a" * 40,
            "corpus_bib": "included.bib",
            "artifacts": ["included.bib"],
            "reported_counts": {"included": 1},
            "temporal_scope": {"status": "resolved", "value": "2016-2025"},
        },
        repository_root=tmp_path,
        generated_at=datetime(2026, 7, 22, tzinfo=UTC),
    )
    bib.write_text("@article{Alpha,title={Changed},year={2024}}\n", encoding="utf-8")

    errors = verify_review_manifest(manifest, tmp_path)

    assert any("SHA-256 mismatch" in error for error in errors)


def test_compare_corpora_reports_added_removed_and_changed(tmp_path: Path) -> None:
    baseline_bib = tmp_path / "baseline.bib"
    candidate_bib = tmp_path / "candidate.bib"
    baseline_bib.write_text(
        "@article{Alpha,title={First},year={2024},doi={10.1/alpha}}\n"
        "@article{Beta,title={Second},year={2023},doi={10.1/beta}}\n",
        encoding="utf-8",
    )
    candidate_bib.write_text(
        "@article{AlphaNew,title={First revised},year={2025},doi={10.1/alpha}}\n"
        "@article{Gamma,title={Third},year={2026},doi={10.1/gamma}}\n",
        encoding="utf-8",
    )

    comparison = compare_corpora(
        read_bibtex_corpus(baseline_bib),
        read_bibtex_corpus(candidate_bib),
    )

    assert comparison["added"][0]["doi"] == "10.1/gamma"
    assert comparison["removed"][0]["doi"] == "10.1/beta"
    assert comparison["changed"][0]["identity"] == "doi:10.1/alpha"
    assert comparison["unchanged"] == []


def test_manifest_is_json_serializable(tmp_path: Path) -> None:
    bib = tmp_path / "included.bib"
    bib.write_text("@article{Alpha,title={First},year={2024}}\n", encoding="utf-8")
    manifest = build_review_manifest(
        config={
            "baseline_id": "review-test",
            "source_commit": "a" * 40,
            "corpus_bib": "included.bib",
            "artifacts": ["included.bib"],
            "reported_counts": {"included": 1},
            "temporal_scope": {"status": "resolved", "value": "2016-2025"},
        },
        repository_root=tmp_path,
        generated_at=datetime(2026, 7, 22, tzinfo=UTC),
    )

    assert json.loads(json.dumps(manifest))["corpus"]["entry_count"] == 1
