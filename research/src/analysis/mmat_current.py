"""Validation helpers for the current 16-record MMAT reassessment.

The historical 17-row appraisal remains archived in
``mmat_assessments.csv``.  This module deliberately validates a separate
current ledger so a historical table cannot silently become the denominator
of the current review.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any, Iterable


CURRENT_STUDY_IDS: tuple[int, ...] = (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 6916, 6917, 6918, 6920, 6921, 6923
)
VALID_RESPONSES = {"Y", "N", "CT"}
REQUIRED_CRITERIA = ("q1", "q2", "q3", "q4", "q5")
ALL_CRITERIA = ("s1", "s2", *REQUIRED_CRITERIA)
EVIDENCE_PATTERN = re.compile(r"^(S1|S2|Q[1-5])=(Y|N|CT)\s+.+$")
VALID_ASSESSMENT_BASES = {
    "primary_full_text_reviewed_externally",
    "abstract_and_metadata_only",
    "abstract_only",
    "metadata_only",
    "protocol_or_proposal_not_applicable",
}
SOURCE_OR_PERIOD_HOLD_STATUSES = {
    "metadata_year_conflict",
    "publication_type_and_year_hold",
}
DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
REGISTRY_PATH = DATA_ROOT / "mmat_current_study_registry.csv"
PRIMARY_SOURCES_PATH = DATA_ROOT / "mmat_primary_sources_manifest.csv"
REASSESSMENT_PATH = DATA_ROOT / "mmat_reassessment_current.csv"
SYNTHESIS_SCOPE_PATH = DATA_ROOT / "current_synthesis_scope.csv"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _ids(rows: Iterable[dict[str, str]], field: str = "study_id") -> list[int]:
    try:
        return [int(row[field]) for row in rows]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid study identifier in field {field!r}") from exc


def load_current_registry(path: Path | str = REGISTRY_PATH) -> list[dict[str, str]]:
    """Load the exact current-study registry and reject historical leakage."""
    rows = _read_csv(Path(path))
    ids = _ids(rows)
    expected = list(CURRENT_STUDY_IDS)
    if sorted(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError(
            f"Current MMAT registry must contain exactly {expected}; got {ids}"
        )
    if any(row.get("mmat_status") == "final" for row in rows):
        raise ValueError(
            "The current registry cannot claim final MMAT status before the QA gate"
        )
    return rows


def load_current_reassessment(
    path: Path | str = REASSESSMENT_PATH,
) -> list[dict[str, str]]:
    """Load the current criterion-level preliminary ledger.

    ``CT`` is allowed and expected while primary full text and locators are
    unavailable.  The function does not convert this preliminary ledger into a
    final quality judgment.
    """
    rows = _read_csv(Path(path))
    ids = _ids(rows)
    expected = list(CURRENT_STUDY_IDS)
    if sorted(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError(
            f"Current MMAT reassessment must contain exactly {expected}; got {ids}"
        )

    for row in rows:
        for criterion in ALL_CRITERIA:
            if row.get(criterion, "") not in VALID_RESPONSES:
                raise ValueError(
                    f"Invalid {criterion} response for study {row.get('study_id')}: "
                    f"{row.get(criterion)!r}"
                )
        evidence = [part.strip() for part in row.get("criterion_evidence", "").split(";")]
        if len(evidence) != len(ALL_CRITERIA) or not all(
            EVIDENCE_PATTERN.match(part) for part in evidence
        ):
            raise ValueError(
                f"Study {row.get('study_id')} lacks one evidence note per MMAT criterion"
            )
        evidence_values = {
            match.group(1).lower(): match.group(2)
            for part in evidence
            if (match := EVIDENCE_PATTERN.match(part))
        }
        if any(evidence_values.get(key) != row.get(key) for key in ALL_CRITERIA):
            raise ValueError(
                f"Study {row.get('study_id')} has criterion values that disagree "
                "with criterion_evidence"
            )
        if not row.get("source_id") or not row.get("assessment_basis"):
            raise ValueError(
                f"Study {row.get('study_id')} lacks source or assessment basis"
            )
        if row["assessment_basis"] not in VALID_ASSESSMENT_BASES:
            raise ValueError(
                f"Study {row.get('study_id')} uses an unknown assessment basis: "
                f"{row['assessment_basis']!r}"
            )
        if row["assessment_basis"] == "protocol_or_proposal_not_applicable":
            if row.get("design_status") != "not_applicable":
                raise ValueError(
                    f"Study {row.get('study_id')} marks a protocol/proposal as "
                    "applicable to an empirical design"
                )
        if row.get("assessment_status") == "final":
            raise ValueError(
                "A final MMAT assessment requires a separate evidence and "
                "adjudication gate"
            )
    return rows


def load_primary_sources(
    path: Path | str = PRIMARY_SOURCES_PATH,
) -> list[dict[str, str]]:
    """Load one source-ledger row for every current study."""
    rows = _read_csv(Path(path))
    ids = _ids(rows)
    expected = list(CURRENT_STUDY_IDS)
    if sorted(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError(
            f"Primary-source manifest must contain exactly {expected}; got {ids}"
        )
    for row in rows:
        if not row.get("source_id") or not row.get("source_url"):
            raise ValueError(f"Study {row.get('study_id')} lacks a source identifier or URL")
    return rows


def load_current_synthesis_scope(
    path: Path | str = SYNTHESIS_SCOPE_PATH,
) -> list[dict[str, str]]:
    """Load the explicit role of every operationally retained current record."""
    rows = _read_csv(Path(path))
    ids = _ids(rows)
    expected = list(CURRENT_STUDY_IDS)
    if sorted(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError(
            f"Current synthesis scope must contain exactly {expected}; got {ids}"
        )
    for row in rows:
        if row.get("operational_inclusion") != "retained_in_current_snapshot":
            raise ValueError(
                f"Study {row.get('study_id')} lacks an explicit operational inclusion"
            )
        role = row.get("synthesis_role")
        applicability = row.get("empirical_mmat_applicability")
        if role not in {"empirical_evidence", "contextual_protocol"}:
            raise ValueError(f"Unknown synthesis role for study {row.get('study_id')}")
        if applicability not in {"applicable", "not_applicable"}:
            raise ValueError(
                f"Unknown empirical MMAT applicability for study {row.get('study_id')}"
            )
        if role == "contextual_protocol" and applicability != "not_applicable":
            raise ValueError(
                f"Contextual protocol {row.get('study_id')} cannot be MMAT-applicable"
            )
        if role == "empirical_evidence" and applicability != "applicable":
            raise ValueError(
                f"Empirical study {row.get('study_id')} must be MMAT-applicable"
            )
    return rows


def validate_current_artifacts(
    registry_path: Path | str = REGISTRY_PATH,
    primary_sources_path: Path | str = PRIMARY_SOURCES_PATH,
    reassessment_path: Path | str = REASSESSMENT_PATH,
    synthesis_scope_path: Path | str = SYNTHESIS_SCOPE_PATH,
) -> dict[str, Any]:
    """Return QA facts for the current MMAT artifacts without scoring quality."""
    registry = load_current_registry(registry_path)
    primary_sources = load_primary_sources(primary_sources_path)
    reassessment = load_current_reassessment(reassessment_path)
    synthesis_scope = load_current_synthesis_scope(synthesis_scope_path)
    source_ids = {row["source_id"] for row in primary_sources}
    if any(row["source_id"] not in source_ids for row in reassessment):
        raise ValueError("Current MMAT reassessment references an unknown source")
    registry_by_id = {row["study_id"]: row for row in registry}
    scope_by_id = {row["study_id"]: row for row in synthesis_scope}
    for row in reassessment:
        registry_row = registry_by_id[row["study_id"]]
        scope_row = scope_by_id[row["study_id"]]
        basis = row["assessment_basis"]
        if (
            scope_row["synthesis_role"] == "contextual_protocol"
            and basis != "protocol_or_proposal_not_applicable"
        ):
            raise ValueError(
                f"Study {row['study_id']} is contextual but has an empirical MMAT basis"
            )
        if (
            scope_row["synthesis_role"] == "empirical_evidence"
            and basis == "protocol_or_proposal_not_applicable"
        ):
            raise ValueError(
                f"Study {row['study_id']} is empirical but has a protocol MMAT basis"
            )
        if basis == "abstract_and_metadata_only":
            if (
                registry_row.get("empirical_status") != "empirical_abstract_only"
                or registry_row.get("design_status") != "abstract_based"
            ):
                raise ValueError(
                    f"Study {row['study_id']} has an abstract-based MMAT ledger "
                    "that disagrees with the current registry"
                )
        if basis == "metadata_only":
            if registry_row.get("design_status") != "metadata_hold":
                raise ValueError(
                    f"Study {row['study_id']} has a metadata-only MMAT ledger "
                    "that disagrees with the current registry"
                )
        if basis == "protocol_or_proposal_not_applicable":
            if registry_row.get("design_status") != "not_applicable":
                raise ValueError(
                    f"Study {row['study_id']} has a protocol MMAT ledger "
                    "that disagrees with the current registry"
                )
    source_by_id = {row["source_id"]: row for row in primary_sources}
    evidence_levels = {
        "primary_full_text_reviewed_externally": 0,
        "abstract_and_metadata_only": 0,
        "abstract_only": 0,
        "metadata_only": 0,
        "protocol_or_proposal_not_applicable": 0,
    }
    for row in reassessment:
        basis = row.get("assessment_basis", "")
        if basis in evidence_levels:
            evidence_levels[basis] += 1
    primary_text_rows = [
        row for row in reassessment
        if row.get("assessment_basis") == "primary_full_text_reviewed_externally"
    ]
    for row in primary_text_rows:
        source = source_by_id[row["source_id"]]
        if source.get("full_text_status") != "externally_reviewed_not_archived":
            raise ValueError(
                f"Study {row['study_id']} claims primary-text review without a "
                "matching source-manifest status"
            )
    source_or_period_hold_rows = [
        row for row in reassessment
        if row.get("assessment_status") == "hold_source_verification"
        or registry_by_id[row["study_id"]].get("source_status")
        in SOURCE_OR_PERIOD_HOLD_STATUSES
    ]
    non_ct = sum(
        row[criterion] != "CT"
        for row in reassessment
        for criterion in ALL_CRITERIA
    )
    blocking_reasons = [
        "Primary full text, criterion-level locators and adjudication are not complete.",
        "The preliminary ledger must not be interpreted as a quality score or ranking.",
    ]
    if len(primary_text_rows) != len(reassessment):
        blocking_reasons.append(
            f"Only {len(primary_text_rows)} of {len(reassessment)} current studies have "
            "externally reviewed full text recorded."
        )
    if any(row.get("adjudication_status") != "supervisor_reviewed" for row in reassessment):
        blocking_reasons.append("Supervisor adjudication is pending for at least one study.")
    if source_or_period_hold_rows:
        held_ids = ", ".join(row["study_id"] for row in source_or_period_hold_rows)
        blocking_reasons.append(
            "At least one current record has an unresolved source/year eligibility "
            f"hold ({held_ids}); it cannot support a final period-dependent synthesis."
        )
    return {
        "study_count": len(registry),
        "study_ids": list(CURRENT_STUDY_IDS),
        "criterion_rows": len(reassessment),
        "primary_source_rows": len(primary_sources),
        "synthesis_scope_rows": len(synthesis_scope),
        "empirical_evidence_rows": sum(
            row["synthesis_role"] == "empirical_evidence" for row in synthesis_scope
        ),
        "contextual_protocol_rows": sum(
            row["synthesis_role"] == "contextual_protocol" for row in synthesis_scope
        ),
        "historical_denominator": 17,
        "current_denominator": len(CURRENT_STUDY_IDS),
        "evidence_levels": evidence_levels,
        "primary_text_reviewed_rows": len(primary_text_rows),
        "source_or_period_hold_rows": len(source_or_period_hold_rows),
        "source_or_period_hold_ids": [row["study_id"] for row in source_or_period_hold_rows],
        "non_ct_criterion_decisions": non_ct,
        "all_preliminary": all(
            row.get("assessment_status") != "final" for row in reassessment
        ),
        "final_ready": False,
        "blocking_reasons": blocking_reasons,
    }
