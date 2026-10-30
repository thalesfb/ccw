"""Check manuscript summaries against the unchanged study-level evidence."""

import csv
from collections import Counter
from pathlib import Path

from src.analysis.content_synthesis import build_outputs, component_counts, mmat_counts, study_rows

ROOT = Path(__file__).resolve().parents[2]


def test_typology_covers_each_included_study_once():
    rows = study_rows(ROOT)
    with (ROOT / "research/data/current_synthesis_scope.csv").open(encoding="utf-8", newline="") as handle:
        included = {row["study_key"] for row in csv.DictReader(handle)
                    if row["record_status"] == "included_empirical_core"}
    assert len(rows) == 15
    assert {row["study_key"] for row in rows} == included
    assert len({row["study_key"] for row in rows}) == len(rows)
    assert sum(Counter(row["purpose"] for row in rows).values()) == 15
    assert all(row["source"] and row["validation"] and row["sample"] for row in rows)
    assert Counter(row["purpose"] for row in rows) == {
        "Predição/classificação": 8, "Personalização/STI": 3,
        "Intervenção didática": 2, "Modelagem cognitiva": 1, "Integração curricular": 1,
    }


def test_mmat_counts_preserve_each_category_and_criterion():
    counts = mmat_counts(ROOT)
    with (ROOT / "research/data/mmat_reassessment_current.csv").open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["s1"] and row["s2"]]
    for group, criteria in counts.items():
        expected = rows if group == "screening" else [row for row in rows if row["design"] == group]
        for criterion, values in criteria.items():
            assert values == dict(Counter(row[criterion] for row in expected))
            assert sum(values.values()) == len(expected)
            assert set(values) <= {"Y", "N", "CT"}
    assert len(rows) == 15
    assert sum(counts["screening"]["s1"].values()) == 15


def test_checked_in_content_tables_match_the_evidence():
    for path, text in build_outputs(ROOT).items():
        assert (ROOT / path).read_text(encoding="utf-8") == text


def test_component_counts_do_not_add_studies_to_the_corpus():
    with (ROOT / "research/data/mmat_component_reassessment_current.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6
    assert len({row["study_key"] for row in rows}) == 3
    for design, criteria in component_counts(ROOT).items():
        selected = [row for row in rows if row["design"] == design]
        for criterion, counts in criteria.items():
            assert counts == dict(Counter(row[criterion] for row in selected))


def test_study_requirement_matrix_covers_the_same_fifteen_studies():
    import re

    matrix = (ROOT / "results/tcc/conteudo/estudos-requisitos.tex").read_text(encoding="utf-8")
    keys = re.findall(r"\\citeonline\{([^}]+)\}", matrix)
    assert len(keys) == len(set(keys)) == 15
    assert set(keys) == {row["study_key"] for row in study_rows(ROOT)}
    missing_source_row = next(line for line in matrix.splitlines() if "Multimodels2020_002" in line)
    assert "sem requisito técnico específico derivado" in missing_source_row
