"""Reject plausible-looking ledger corruption without editing research data."""
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


def test_primary_source_ids_must_be_unique(monkeypatch):
    original_read = current._read_csv

    def read(path):
        rows = original_read(path)
        if path == current.PRIMARY_SOURCES_PATH:
            rows[0]["source_id"] = rows[1]["source_id"]
        return rows

    monkeypatch.setattr(current, "_read_csv", read)
    with pytest.raises(ValueError, match="duplicate source_id"):
        current.validate_current_artifacts()


def test_current_ledger_remains_provisional():
    facts = current.validate_current_artifacts()
    assert facts["final_ready"] is False
