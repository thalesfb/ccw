from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest

from src.analysis import mmat_current, study_scope
from src.analysis.mmat_current import validate_current_artifacts


def _read_rows(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_rows(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def test_neutral_module_loads_candidate_scope_and_source_ledgers():
    scope = study_scope.load_candidate_scope()
    sources = study_scope.load_primary_sources()
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 6915, 6916, 6917, 6919, 6920, 6921, 6923]

    assert len(expected) == 18
    assert [int(row["study_id"]) for row in scope] == expected
    assert [int(row["study_id"]) for row in sources] == expected


def test_neutral_candidate_loader_does_not_require_mmat_decisions(tmp_path):
    rows = [
        {"study_id": str(study_id), "screening_state": "candidate"}
        for study_id in study_scope.CANDIDATE_STUDY_IDS
    ]
    candidate_ledger = tmp_path / "candidate-ledger.csv"
    _write_rows(candidate_ledger, rows)

    loaded = study_scope.load_candidate_scope(candidate_ledger)

    assert [int(row["study_id"]) for row in loaded] == list(study_scope.CANDIDATE_STUDY_IDS)
    assert all("empirical_mmat_applicability" not in row for row in loaded)


def test_mmat_module_reexports_scope_api_for_existing_callers():
    assert mmat_current.CURRENT_STUDY_IDS == study_scope.CANDIDATE_STUDY_IDS
    assert mmat_current.load_primary_sources is study_scope.load_primary_sources
    assert len(mmat_current.load_current_synthesis_scope()) == 18


def test_neutral_loader_does_not_import_the_mmat_evaluator():
    result = subprocess.run(
        [sys.executable, "-c", (
            "import sys; "
            "from src.analysis.study_scope import load_candidate_scope; "
            "assert len(load_candidate_scope()) == 18; "
            "assert 'src.analysis.mmat_current' not in sys.modules"
        )],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_neutral_scope_loader_rejects_malformed_ids(tmp_path):
    source_scope = study_scope.CANDIDATE_SCOPE_PATH

    rows = _read_rows(source_scope)
    rows[-1]["study_id"] = "not-an-id"
    malformed_ids = tmp_path / "malformed-ids.csv"
    _write_rows(malformed_ids, rows)
    with pytest.raises(ValueError, match="Invalid study identifier"):
        study_scope.load_candidate_scope(malformed_ids)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("synthesis_role", "unknown", "Unknown synthesis role"),
        ("empirical_mmat_applicability", "applicable", "cannot be MMAT-applicable"),
    ],
)
def test_legacy_mmat_scope_adapter_keeps_its_existing_validation(tmp_path, field, value, message):
    rows = _read_rows(study_scope.CANDIDATE_SCOPE_PATH)
    if field == "empirical_mmat_applicability":
        protocol = next(row for row in rows if int(row["study_id"]) == 6921)
        protocol[field] = value
    else:
        rows[0][field] = value
    malformed = tmp_path / "malformed-legacy-mmat-scope.csv"
    _write_rows(malformed, rows)

    with pytest.raises(ValueError, match=message):
        mmat_current.load_current_synthesis_scope(malformed)


def test_neutral_primary_source_loader_rejects_missing_source_identity(tmp_path):
    rows = _read_rows(study_scope.PRIMARY_SOURCES_PATH)
    rows[0]["source_url"] = ""
    malformed = tmp_path / "malformed-sources.csv"
    _write_rows(malformed, rows)

    with pytest.raises(ValueError, match="lacks a source identifier or URL"):
        study_scope.load_primary_sources(malformed)


def test_legacy_mmat_quality_gate_remains_not_ready():
    report = validate_current_artifacts()

    assert report["final_ready"] is False
