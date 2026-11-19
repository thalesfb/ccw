from __future__ import annotations

import re
from pathlib import Path

from src.analysis.study_codes import load_study_codes, render_latex_mapping


EXPECTED_CODES = [
    ("E01", "6920", "Echeveria2025_6920"),
    ("E02", "6915", "He2025_6915"),
    ("E03", "6", "Identifying2017_006"),
    ("E04", "4", "Analysis2022_003"),
    ("E05", "8", "Computational2017_008"),
    ("E06", "10", "Machine2024_009"),
    ("E07", "14", "Enhancing2025_012"),
    ("E08", "6917", "Ozseven2026_6917"),
    ("E09", "1", "Math2021_001"),
    ("E10", "3", "Multimodels2020_002"),
    ("E11", "2", "Implementation2025_000"),
    ("E12", "6916", "Villegas2025_6916"),
    ("E13", "6919", "UniversityMathematics2026_6919"),
    ("E14", "5", "Design2025_004"),
    ("E15", "7", "Innovative2023_005"),
]


def test_study_codes_match_the_reference_order_and_original_selection() -> None:
    rows = load_study_codes()
    assert [(row["code"], row["study_id"], row["study_key"]) for row in rows] == EXPECTED_CODES


def test_generated_latex_mapping_is_current_and_provides_reader_commands() -> None:
    from src.analysis.study_codes import OUTPUT_PATH

    generated = Path(OUTPUT_PATH).read_text(encoding="utf-8")
    assert generated == render_latex_mapping()
    assert r"\newcommand{\estudo}" in generated
    assert r"\newcommand{\estudocite}" in generated
    for code, _, study_key in EXPECTED_CODES:
        assert rf"\csname TCCstudy@{study_key}\endcsname{{{code}}}" in generated


def test_quadro_three_is_the_alphabetical_reader_facing_master_list() -> None:
    root = Path(__file__).resolve().parents[2]
    chapter = (root / "results/tcc/conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
    table = chapter.split(r"\label{qua:sintese-estudos-empiricos}", 1)[1].split(r"\end{longtable}", 1)[0]
    coded_keys = re.findall(r"\\estudo\{([^}]+)\}", table)
    assert coded_keys == [row[2] for row in EXPECTED_CODES]
    assert re.findall(r"\\estudo\{([^}]+)\} & \\citeonline\{([^}]+)\}", table) == [
        (row[2], row[2]) for row in EXPECTED_CODES
    ]
    assert r"\textbf{ID}" in table
    expected_reference_order = [
        "Echeveria2025_6920", "He2025_6915", "Imperatrice2025_6921",
        "Identifying2017_006", "Analysis2022_003", "Computational2017_008",
        "Machine2024_009", "Enhancing2025_012", "Ozseven2026_6917",
        "Math2021_001", "Multimodels2020_002", "Implementation2025_000",
        "Machine2019_007", "Villegas2025_6916", "UniversityMathematics2026_6919",
        "Zeng2025_6923", "Design2025_004", "Innovative2023_005",
    ]
    assert re.findall(r"\\citeonline\{([^}]+)\}", table) == expected_reference_order
    for _, _, study_key in EXPECTED_CODES:
        assert rf"\citeonline{{{study_key}}}" in table
    for excluded_key in ("Imperatrice2025_6921", "Machine2019_007", "Zeng2025_6923"):
        row = next(line for line in table.splitlines() if rf"\citeonline{{{excluded_key}}}" in line)
        assert row.startswith("-- & ")


def test_study_list_generators_use_registry_citations() -> None:
    from src.analysis.content_synthesis import build_outputs
    from src.analysis.mmat_current_tcc_table import load_component_rows, load_rows, render_component_table, render_table

    synthesis = build_outputs()["research/exports/references/study_synthesis_tcc.tex"]
    mmat = render_table(load_rows())
    for _, _, study_key in EXPECTED_CODES:
        assert rf"\estudocite{{{study_key}}}" in synthesis
    assert r"\citeonline{Multimodels2020_002}" in mmat
    assert r"\estudocite{Multimodels2020_002}" not in mmat
    assert r"\estudocite{He2025_6915}" in mmat
    components = render_component_table(load_component_rows())
    assert r"\estudocite{Echeveria2025_6920}" in components
    assert r"\estudocite{UniversityMathematics2026_6919}" in components


def test_slide_generator_reads_current_registry_and_uses_reader_codes() -> None:
    root = Path(__file__).resolve().parents[2]
    import sys

    sys.path.insert(0, str(root))
    from scripts.generate_tcc_presentation import build_deck, study_codes_by_id

    codes = study_codes_by_id()
    assert [codes[study_id] for _, study_id, _ in EXPECTED_CODES] == [row[0] for row in EXPECTED_CODES]
    deck_text = "\n".join(
        shape.text for slide in build_deck().slides for shape in slide.shapes if shape.has_text_frame
    )
    for code in ("E05", "E07", "E10", "E14", "E15"):
        assert code in deck_text
    assert "estudo 5" not in deck_text.lower()
    assert "estudo 8" not in deck_text.lower()


def test_study_tables_list_rows_in_code_order() -> None:
    root = Path(__file__).resolve().parents[2]
    code_by_key = {key: code for code, _, key in EXPECTED_CODES}
    tables = {
        "research/exports/references/mmat_current_tcc_table.tex": None,
        "research/exports/references/mmat_component_details_tcc.tex": None,
        "research/exports/references/study_synthesis_tcc.tex": None,
        "results/tcc/conteudo/estudos-requisitos.tex": None,
    }
    for relative in tables:
        text = (root / relative).read_text(encoding="utf-8")
        for block in re.split(r"\\end\{longtable\}", text):
            row_codes = [
                code_by_key[key]
                for key in re.findall(r"^\\estudocite(?:\[[^\]]*\])?\{([^}]+)\}", block, re.M)
            ]
            assert row_codes == sorted(row_codes), f"{relative} rows are not in study-code order: {row_codes}"