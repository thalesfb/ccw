"""Validation helpers for the current 18-record MMAT reassessment.

The historical 17-row appraisal remains archived in
``mmat_assessments.csv``.  This module deliberately validates a separate
current ledger so a historical table cannot silently become the denominator
of the current review.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .study_scope import (
    CANDIDATE_SCOPE_PATH,
    CANDIDATE_STUDY_IDS,
    PRIMARY_SOURCES_PATH,
    _ids,
    _read_csv,
    load_candidate_scope,
    load_primary_sources,
)


CURRENT_RECORD_IDS = CANDIDATE_STUDY_IDS
CURRENT_EMPIRICAL_STUDY_IDS: tuple[int, ...] = (
    1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 6915, 6916, 6917, 6919, 6920
)
PENDING_UNIT_ADJUDICATION_STUDY_IDS: tuple[int, ...] = ()
CURRENT_MMAT_STUDY_IDS: tuple[int, ...] = (
    1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 6915, 6916, 6917, 6919, 6920
)
# Compatibility alias: historical callers use this for the 18-record ledger.
CURRENT_STUDY_IDS = CURRENT_RECORD_IDS
CONTEXT_ONLY_STUDY_IDS = (9,)
PENDING_FULL_TEXT_STUDY_IDS = (6923,)
CONTEXTUAL_PROTOCOL_STUDY_IDS = (6921,)
SYNTHESIS_SCOPE_PATH = CANDIDATE_SCOPE_PATH
VALID_RESPONSES = {"", "Y", "N", "CT"}
VALID_DESIGNS = {
    "qualitative", "quantitative_randomized", "quantitative_nonrandomized",
    "quantitative_descriptive", "mixed_methods", "metadata_hold", "not_applicable",
    "design_pending",
}
PENDING_DESIGN_STATUSES = {
    "allocation_conflict_pending",
    "allocation_unreported_pending",
    "allocation_sequence_unreported_pending",
    "unit_of_appraisal_pending",
    "primary_text_not_retrieved_pending",
}
VALID_DESIGN_STATUSES = {
    "operational_category_inferred_allocation_unknown",
    "operational_category_adaptation",
    "abstract_based",
    "allocation_conflict_pending",
    "allocation_sequence_unreported_pending",
    "allocation_unreported_pending",
    "design_reassessed_provisional",
    "design_reassessed_provisional_with_allocation_conflict",
    "metadata_hold",
    "not_applicable",
    "primary_text_not_retrieved_pending",
    "unit_of_appraisal_pending",
}
REQUIRED_CRITERIA = ("q1", "q2", "q3", "q4", "q5")
COMPONENT_CRITERIA = ("c1", "c2", "c3", "c4", "c5")
ALL_CRITERIA = ("s1", "s2", *REQUIRED_CRITERIA)
EVIDENCE_PATTERN = re.compile(r"^(S1|S2|Q[1-5])=(Y|N|CT)\s+.+$")
VALID_ASSESSMENT_BASES = {
    "primary_full_text_reviewed_externally",
    "primary_full_text_scope_exclusion",
    "pending_full_text_not_appraised",
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
HISTORICAL_MMAT_PATH = DATA_ROOT / "mmat_assessments.csv"
REASSESSMENT_PATH = DATA_ROOT / "mmat_reassessment_current.csv"
SYNTHESIS_SCOPE_PATH = DATA_ROOT / "current_synthesis_scope.csv"
COMPONENT_REASSESSMENT_PATH = DATA_ROOT / "mmat_component_reassessment_current.csv"


def load_current_registry(path: Path | str = REGISTRY_PATH) -> list[dict[str, str]]:
    """Load the exact current-study registry and reject historical leakage."""
    rows = _read_csv(Path(path))
    ids = _ids(rows)
    expected = list(CURRENT_RECORD_IDS)
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

    Blank criterion cells are required when a primary full text was not
    retrieved or a record was excluded during abstract screening. Those
    records have not received an MMAT appraisal. ``CT`` is reserved for
    criteria that were actually considered but cannot be determined from the
    consulted source.
    """
    rows = _read_csv(Path(path))
    ids = _ids(rows)
    expected = list(CURRENT_RECORD_IDS)
    if sorted(ids) != expected or len(ids) != len(set(ids)):
        raise ValueError(
            f"Current MMAT reassessment must contain exactly {expected}; got {ids}"
        )

    for row in rows:
        source_pending = row["study_id"] in {
            str(value) for value in PENDING_FULL_TEXT_STUDY_IDS
        }
        unit_pending = row.get("design_status") == "unit_of_appraisal_pending"
        not_appraised = (
            source_pending
            or row.get("assessment_basis") in {
                "abstract_and_metadata_only", "primary_full_text_scope_exclusion",
                "protocol_or_proposal_not_applicable",
            }
            or unit_pending
        )
        if (
            row.get("assessment_basis") == "primary_full_text_scope_exclusion"
            and int(row["study_id"]) not in CONTEXT_ONLY_STUDY_IDS
        ):
            raise ValueError("Full-text scope exclusion is not an empirical appraisal basis")
        for criterion in ALL_CRITERIA:
            if row.get(criterion, "") not in VALID_RESPONSES:
                raise ValueError(
                    f"Invalid {criterion} response for study {row.get('study_id')}: "
                    f"{row.get(criterion)!r}"
                )
        if row.get("design") not in VALID_DESIGNS:
            raise ValueError(f"Invalid design for study {row.get('study_id')}: {row.get('design')!r}")
        if row.get("design_status") not in VALID_DESIGN_STATUSES:
            raise ValueError(
                f"Invalid design status for study {row.get('study_id')}: "
                f"{row.get('design_status')!r}"
            )
        if row.get("design") != "design_pending" and row.get("design_status") in PENDING_DESIGN_STATUSES:
            raise ValueError(
                f"Study {row.get('study_id')} has a pending design status but "
                "requires a pending MMAT design"
            )
        category_pending = row.get("design") == "design_pending" and not not_appraised
        if category_pending and any(row.get(key, "").strip() for key in REQUIRED_CRITERIA):
            raise ValueError(
                f"Study {row['study_id']} has an unresolved MMAT design; "
                "category-specific criteria must remain unappraised, not CT"
            )
        if not_appraised:
            if any(row.get(criterion, "").strip() for criterion in ALL_CRITERIA):
                raise ValueError(
                    f"Study {row['study_id']} must not contain MMAT responses "
                    "when no MMAT appraisal was undertaken"
                )
            if row.get("criterion_evidence", "").strip():
                raise ValueError(
                    f"Study {row['study_id']} must not contain criterion-level MMAT "
                    "evidence without an eligible appraisal source"
                )
        else:
            evidence = [
                part.strip()
                for part in row.get("criterion_evidence", "").split(";")
            ]
            appraised_criteria = ("s1", "s2") if category_pending else ALL_CRITERIA
            if len(evidence) != len(appraised_criteria) or not all(
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
            if set(evidence_values) != set(appraised_criteria) or any(
                evidence_values.get(key) != row.get(key) for key in appraised_criteria
            ):
                raise ValueError(
                    f"Study {row.get('study_id')} has criterion values that disagree "
                    "with criterion_evidence"
                )
        if not row.get("source_id") or not row.get("assessment_basis"):
            raise ValueError(
                f"Study {row.get('study_id')} lacks source or assessment basis"
            )
        for field in ("reviewer", "review_date", "adjudication_status", "assessment_status"):
            if not row.get(field, "").strip():
                raise ValueError(
                    f"Study {row.get('study_id')} lacks review provenance field {field}"
                )
        if row["assessment_basis"] not in VALID_ASSESSMENT_BASES:
            raise ValueError(
                f"Study {row.get('study_id')} uses an unknown assessment basis: "
                f"{row['assessment_basis']!r}"
            )
        if row["assessment_basis"] == "protocol_or_proposal_not_applicable":
            if row.get("design_status") != "not_applicable" or row.get("design") != "not_applicable":
                raise ValueError(
                    f"Study {row.get('study_id')} marks a protocol/proposal as "
                    "applicable to an empirical design"
                )
        if row["study_id"] in {str(value) for value in PENDING_FULL_TEXT_STUDY_IDS}:
            if row.get("assessment_basis") != "pending_full_text_not_appraised":
                raise ValueError(
                    f"Study {row['study_id']} cannot be treated as appraised before "
                    "its primary full text is retrieved"
                )
        if row.get("assessment_status") == "final":
            raise ValueError(
                "A final MMAT assessment requires a separate evidence and "
                "adjudication gate"
            )
        if row.get("design") == "design_pending":
            if row.get("design_status") not in PENDING_DESIGN_STATUSES:
                raise ValueError(
                    f"Study {row.get('study_id')} has an unresolved MMAT design "
                    "without a documented pending-design rationale"
                )
            if not source_pending and not unit_pending and any(
                row.get(criterion, "").strip() for criterion in REQUIRED_CRITERIA
            ):
                raise ValueError(
                    f"Study {row.get('study_id')} has an unresolved MMAT design "
                    "but category-specific criteria were rated"
                )
        if row["study_id"] in {str(value) for value in PENDING_FULL_TEXT_STUDY_IDS}:
            if (
                row.get("design") != "design_pending"
                or row.get("design_status") != "primary_text_not_retrieved_pending"
                or row.get("assessment_status") != "hold_source_verification"
                or any(row.get(criterion, "") for criterion in ALL_CRITERIA)
                or row.get("criterion_evidence", "").strip()
            ):
                raise ValueError(
                    f"Study {row['study_id']} lacks the explicit no-appraisal hold "
                    "required while primary full text is unavailable"
                )
        if unit_pending and (
            row.get("assessment_status") != "hold_unit_of_appraisal"
            or row.get("assessment_basis") != "primary_full_text_reviewed_externally"
            or row.get("design") != "design_pending"
            or any(row.get(criterion, "").strip() for criterion in ALL_CRITERIA)
            or row.get("criterion_evidence", "").strip()
        ):
            raise ValueError(
                f"Study {row.get('study_id')} has an unresolved appraisal unit; "
                "it must remain explicitly held with no MMAT responses"
            )
    return rows


def load_component_reassessments(
    path: Path | str = COMPONENT_REASSESSMENT_PATH,
) -> list[dict[str, str]]:
    """Load provisional MMAT appraisals for components of mixed-methods studies."""
    rows = _read_csv(Path(path))
    expected = {
        ("6916", "quantitative", "quantitative_nonrandomized"),
        ("6916", "qualitative", "qualitative"),
        ("6919", "quantitative", "quantitative_nonrandomized"),
        ("6919", "qualitative", "qualitative"),
        ("6920", "quantitative", "quantitative_descriptive"),
        ("6920", "qualitative", "qualitative"),
    }
    observed = {
        (row.get("study_id", ""), row.get("component", ""), row.get("design", ""))
        for row in rows
    }
    if len(rows) != len(expected) or observed != expected:
        raise ValueError("Mixed-methods component reassessment must contain the six expected component rows")
    for row in rows:
        for criterion in COMPONENT_CRITERIA:
            if row.get(criterion) not in {"Y", "N", "CT"}:
                raise ValueError(
                    f"Invalid {criterion} component response for study {row.get('study_id')}"
                )
            if not row.get(f"evidence_{criterion}"):
                raise ValueError(
                    f"Missing {criterion} component rationale for study {row.get('study_id')}"
                )
        if not row.get("source_id") or not row.get("source_locator"):
            raise ValueError(f"Component appraisal for study {row.get('study_id')} lacks source location")
        if row.get("review_status") != "provisional_single_reviewer":
            raise ValueError("Mixed-methods component appraisals must remain provisional")
    main_rows = {row["study_id"]: row for row in load_current_reassessment()}
    if any(main_rows[row["study_id"]]["design"] != "mixed_methods" for row in rows):
        raise ValueError("Component-level appraisals are allowed only for mixed-methods studies")
    return rows


def load_current_synthesis_scope(
    path: Path | str = SYNTHESIS_SCOPE_PATH,
) -> list[dict[str, str]]:
    """Load and validate the explicit role of every current candidate record."""
    rows = load_candidate_scope(path)
    expected_dispositions = {
        **{
            study_id: (
                "included_empirical_core", "empirical_evidence",
                "pending_unit_adjudication"
                if study_id in PENDING_UNIT_ADJUDICATION_STUDY_IDS
                else "applicable",
                "included", "included",
            )
            for study_id in CURRENT_EMPIRICAL_STUDY_IDS
        },
        9: (
            "context_only", "contextual_study", "context_only",
            "abstract_screening", "excluded",
        ),
        **{
            study_id: (
                "awaiting_full_text", "pending_full_text", "pending_full_text",
                "not_retrieved", "not_retrieved",
            )
            for study_id in PENDING_FULL_TEXT_STUDY_IDS
        },
        6921: (
            "protocol_context_only", "contextual_protocol", "not_applicable",
            "eligibility", "excluded",
        ),
    }
    for row in rows:
        study_id = int(row["study_id"])
        role = row.get("synthesis_role")
        applicability = row.get("empirical_mmat_applicability")
        if role not in {
            "empirical_evidence", "contextual_study", "contextual_protocol",
            "pending_full_text",
        }:
            raise ValueError(f"Unknown synthesis role for study {study_id}")
        if applicability not in {
            "applicable", "pending_unit_adjudication", "context_only",
            "pending_full_text", "not_applicable",
        }:
            raise ValueError(f"Unknown empirical MMAT applicability for study {study_id}")
        if role == "contextual_protocol" and applicability != "not_applicable":
            raise ValueError(f"Contextual protocol {study_id} cannot be MMAT-applicable")
        expected_disposition = expected_dispositions[study_id]
        observed = (
            row.get("record_status"), row.get("synthesis_role"),
            row.get("empirical_mmat_applicability"), row.get("selection_stage"),
            row.get("selection_status"),
        )
        if observed != expected_disposition:
            raise ValueError(
                f"Study {study_id} has scope disposition {observed!r}; "
                f"expected {expected_disposition!r}"
            )
        if row.get("candidate_set_membership") != "shortlisted_record":
            raise ValueError(f"Study {study_id} is not explicitly identified as shortlisted")
        if not row.get("selection_reason", "").strip():
            raise ValueError(f"Study {study_id} lacks a selection rationale")
        if not row.get("source_id", "").strip() or not row.get("evidence_locator", "").strip():
            raise ValueError(f"Study {study_id} lacks a source-linked scope decision")
    return rows


def validate_current_artifacts(
    registry_path: Path | str = REGISTRY_PATH,
    primary_sources_path: Path | str = PRIMARY_SOURCES_PATH,
    reassessment_path: Path | str = REASSESSMENT_PATH,
    synthesis_scope_path: Path | str = SYNTHESIS_SCOPE_PATH,
    historical_mmat_path: Path | str = HISTORICAL_MMAT_PATH,
) -> dict[str, Any]:
    """Return QA facts for the current MMAT artifacts without scoring quality."""
    registry = load_current_registry(registry_path)
    historical_mmat_rows = _read_csv(Path(historical_mmat_path))
    primary_sources = load_primary_sources(primary_sources_path)
    reassessment = load_current_reassessment(reassessment_path)
    component_reassessment = load_component_reassessments()
    synthesis_scope = load_current_synthesis_scope(synthesis_scope_path)
    source_ids = [row["source_id"] for row in primary_sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Primary-source manifest contains duplicate source_id")
    source_pairs = {(row["study_id"], row["source_id"]) for row in primary_sources}
    for row in reassessment:
        if (row["study_id"], row["source_id"]) not in source_pairs:
            raise ValueError(f"Source {row['source_id']!r} does not belong to study {row['study_id']}")
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
                or row.get("assessment_status") != "not_assessed_after_abstract_exclusion"
            ):
                raise ValueError(
                    f"Study {row['study_id']} has an abstract-excluded record that "
                    "must remain unassessed"
                )
        if basis == "metadata_only":
            if registry_row.get("design_status") != "metadata_hold":
                raise ValueError(
                    f"Study {row['study_id']} has a metadata-only MMAT ledger "
                    "that disagrees with the current registry"
                )
        if basis == "primary_full_text_scope_exclusion":
            source_row = next(
                source for source in primary_sources
                if source["source_id"] == row["source_id"]
            )
            if (
                scope_row["synthesis_role"] != "contextual_study"
                or registry_row.get("empirical_status") != "empirical_outside_mathematics_scope"
                or registry_row.get("design_status") != "not_applicable"
                or row.get("design") != "not_applicable"
                or row.get("design_status") != "not_applicable"
                or row.get("assessment_status") != "not_assessed_scope_exclusion_confirmed"
                or source_row.get("full_text_status") != "externally_reviewed_not_archived"
                or not re.fullmatch(r"[a-f0-9]{64}", source_row.get("sha256", ""))
            ):
                raise ValueError(
                    f"Study {row['study_id']} has an inconsistent full-text scope exclusion"
                )
        if basis == "protocol_or_proposal_not_applicable":
            if registry_row.get("design_status") != "not_applicable":
                raise ValueError(
                    f"Study {row['study_id']} has a protocol MMAT ledger "
                    "that disagrees with the current registry"
                )
    source_by_id = {row["source_id"]: row for row in primary_sources}
    scope_by_id = {row["study_id"]: row for row in synthesis_scope}
    reassessment_by_id = {row["study_id"]: row for row in reassessment}
    for study_id in PENDING_FULL_TEXT_STUDY_IDS:
        scope_row = scope_by_id[str(study_id)]
        assessment_row = reassessment_by_id[str(study_id)]
        source_row = source_by_id[assessment_row["source_id"]]
        if (
            scope_row["record_status"] != "awaiting_full_text"
            or source_row.get("full_text_status") != "not_retrieved"
            or assessment_row["assessment_basis"] != "pending_full_text_not_appraised"
            or assessment_row["assessment_status"] != "hold_source_verification"
        ):
            raise ValueError(
                f"Study {study_id} must remain pending until its primary full text is retrieved"
            )
    core_reassessment = [
        reassessment_by_id[str(study_id)] for study_id in CURRENT_MMAT_STUDY_IDS
    ]
    unit_hold_rows = [
        reassessment_by_id[str(study_id)]
        for study_id in PENDING_UNIT_ADJUDICATION_STUDY_IDS
    ]
    protocol_reassessment = [
        reassessment_by_id[str(study_id)] for study_id in CONTEXTUAL_PROTOCOL_STUDY_IDS
    ]
    scored_population = [*core_reassessment, *protocol_reassessment]
    evidence_levels = {
        "primary_full_text_reviewed_externally": 0,
        "primary_full_text_scope_exclusion": 0,
        "abstract_and_metadata_only": 0,
        "abstract_only": 0,
        "metadata_only": 0,
        "protocol_or_proposal_not_applicable": 0,
    }
    for row in scored_population:
        basis = row.get("assessment_basis", "")
        if basis in evidence_levels:
            evidence_levels[basis] += 1
    primary_text_rows = [
        row for row in core_reassessment
        if row.get("assessment_basis") == "primary_full_text_reviewed_externally"
    ]
    for row in primary_text_rows:
        source = source_by_id[row["source_id"]]
        if source.get("full_text_status") != "externally_reviewed_not_archived":
            raise ValueError(
                f"Study {row['study_id']} claims primary-text review without a "
                "matching source-manifest status"
            )
    historical_ids = [row.get("ID", "").strip() for row in historical_mmat_rows]
    if (
        not historical_ids
        or any(not study_id for study_id in historical_ids)
        or len(historical_ids) != len(set(historical_ids))
    ):
        raise ValueError("Historical MMAT ledger must contain unique, non-empty IDs")
    source_or_period_hold_rows = [
        row for row in core_reassessment
        if row.get("assessment_status") == "hold_source_verification"
        or registry_by_id[row["study_id"]].get("source_status")
        in SOURCE_OR_PERIOD_HOLD_STATUSES
    ]
    non_ct = sum(
        row[criterion] in {"Y", "N"}
        for row in core_reassessment
        for criterion in ALL_CRITERIA
    )
    category_pending_rows = [row for row in core_reassessment if row["design"] == "design_pending"]
    category_appraised_rows = [row for row in core_reassessment if row["design"] != "design_pending"]
    blocking_reasons = [
        "The empirical corpus retains 15 studies provisionally; all have preliminary screening and category-specific appraisals, including explicitly operational routes. These are not final design or eligibility decisions.",
        "Studies 5 and 7 use an inferred category-3 route with allocation unknown; study 8 uses an explicitly adapted category-4 route for computational models.",
        "The preliminary ledger must not be interpreted as a quality score or ranking.",
        "Study 8 is one thesis/report with mathematical components; fractions reused across chapters must not be counted twice and seven-domain results are not mathematics-only estimates.",
    ]
    if len(primary_text_rows) != len(CURRENT_MMAT_STUDY_IDS):
        blocking_reasons.append(
            f"Only {len(primary_text_rows)} of {len(CURRENT_MMAT_STUDY_IDS)} empirical-core "
            "studies have externally reviewed full text recorded."
        )
    if any(row.get("adjudication_status") != "supervisor_reviewed" for row in core_reassessment):
        blocking_reasons.append("Supervisor adjudication is pending for at least one study.")
    if len(PENDING_FULL_TEXT_STUDY_IDS):
        blocking_reasons.append(
            "One shortlisted empirical record remains pending primary full text and is excluded from the MMAT denominator."
        )
    if source_or_period_hold_rows:
        held_ids = ", ".join(row["study_id"] for row in source_or_period_hold_rows)
        blocking_reasons.append(
            "At least one current record has an unresolved source/year eligibility "
            f"hold ({held_ids}); it cannot support a final period-dependent synthesis."
        )
    return {
        "study_count": len(registry),
        "study_ids": list(CURRENT_RECORD_IDS),
        "included_empirical_study_ids": list(CURRENT_EMPIRICAL_STUDY_IDS),
        "mmat_study_ids": list(CURRENT_MMAT_STUDY_IDS),
        "mmat_unit_hold_ids": [row["study_id"] for row in unit_hold_rows],
        "mmat_unit_hold_rows": len(unit_hold_rows),
        "criterion_rows": len(category_appraised_rows),
        "screening_rows": len(core_reassessment),
        "category_appraised_rows": len(category_appraised_rows),
        "category_pending_ids": [row["study_id"] for row in category_pending_rows],
        "assessment_registry_rows": len(reassessment),
        "component_criterion_rows": sum(
            row["study_id"] in {str(study_id) for study_id in CURRENT_MMAT_STUDY_IDS}
            for row in component_reassessment
        ),
        "component_assessment_registry_rows": len(component_reassessment),
        "primary_source_rows": len(primary_sources),
        "synthesis_scope_rows": len(synthesis_scope),
        "empirical_evidence_rows": sum(
            row["record_status"] == "included_empirical_core" for row in synthesis_scope
        ),
        "contextual_study_rows": sum(
            row["record_status"] == "context_only" for row in synthesis_scope
        ),
        "awaiting_full_text_rows": sum(
            row["record_status"] == "awaiting_full_text" for row in synthesis_scope
        ),
        "contextual_protocol_rows": sum(
            row["synthesis_role"] == "contextual_protocol" for row in synthesis_scope
        ),
        "historical_mmat_assessment_rows": len(historical_mmat_rows),
        "current_mmat_ledger_rows": len(reassessment),
        "historical_denominator": 17,
        "current_denominator": len(CURRENT_MMAT_STUDY_IDS),
        "denominator_meaning": "S1/S2 screening records; use category_appraised_rows for Q1-Q5 coverage",
        "evidence_levels": evidence_levels,
        "record_evidence_levels": {
            basis: sum(row.get("assessment_basis") == basis for row in reassessment)
            for basis in (*evidence_levels, "pending_full_text_not_appraised")
        },
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
