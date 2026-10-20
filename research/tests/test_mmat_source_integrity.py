"""Reject plausible-looking ledger corruption without editing research data."""
import csv

import pytest
from src.analysis import mmat_current as current


@pytest.mark.parametrize("field,value,message", [
    ("source_id", "PS-002", "does not belong"),
    ("source_id", "unknown", "does not belong"),
    ("design", "banana", "Invalid design"),
    ("design", "", "Invalid design"),
    ("design", None, "Invalid design"),
])
def test_reassessment_rejects_invalid_source_or_design(monkeypatch, field, value, message):
    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            next(row for row in rows if row["study_id"] == "1")[field] = value
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match=message):
        current.validate_current_artifacts()
    from src.analysis.mmat_current_tcc_table import load_rows
    with pytest.raises(ValueError, match=message):
        load_rows()


def test_primary_source_ids_must_be_unique(tmp_path):
    with current.PRIMARY_SOURCES_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows[0]["source_id"] = rows[1]["source_id"]
    corrupted_sources = tmp_path / "duplicate-source-ids.csv"
    with corrupted_sources.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="duplicate source_id"):
        current.validate_current_artifacts(primary_sources_path=corrupted_sources)


def test_current_ledger_remains_provisional():
    facts = current.validate_current_artifacts()
    assert facts["final_ready"] is False


def test_full_text_scope_exclusion_is_not_an_empirical_appraisal(monkeypatch):
    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            row = next(row for row in rows if row["study_id"] == "9")
            row["assessment_basis"] = "primary_full_text_scope_exclusion"
            row["design"] = "not_applicable"
            row["design_status"] = "not_applicable"
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    row = next(row for row in current.load_current_reassessment() if row["study_id"] == "9")
    assert all(row[key] == "" for key in current.ALL_CRITERIA)
    assert row["criterion_evidence"] == ""


@pytest.mark.parametrize("criterion", current.ALL_CRITERIA)
def test_full_text_scope_exclusion_rejects_fabricated_screening(monkeypatch, criterion):
    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            row = next(row for row in rows if row["study_id"] == "9")
            row["assessment_basis"] = "primary_full_text_scope_exclusion"
            row["design"] = "not_applicable"
            row["design_status"] = "not_applicable"
            row[criterion] = "Y"
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="must not contain MMAT responses"):
        current.load_current_reassessment()


def test_full_text_scope_exclusion_rejects_fabricated_criterion_evidence(monkeypatch):
    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.REASSESSMENT_PATH:
            row = next(row for row in rows if row["study_id"] == "9")
            row["criterion_evidence"] = "S1=Y fabricated appraisal"
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="must not contain criterion-level MMAT"):
        current.load_current_reassessment()


@pytest.mark.parametrize("field,value", [
    ("sha256", ""),
    ("full_text_status", "not_retrieved"),
])
def test_full_text_scope_exclusion_requires_matching_primary_source(monkeypatch, field, value):
    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.PRIMARY_SOURCES_PATH:
            next(row for row in rows if row["study_id"] == "9")[field] = value
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="inconsistent full-text scope exclusion"):
        current.validate_current_artifacts()
