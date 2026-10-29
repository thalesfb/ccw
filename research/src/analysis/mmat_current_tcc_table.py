"""Render the current preliminary MMAT reassessment for the TCC.

The output is deliberately labelled preliminary. It is generated from the
audit ledger, with separate screening and category-specific response coverage.
Operational category routes remain distinct from confirmed study designs.
Historical reviewer labels do not establish completed human appraisal.
No overall quality score is assigned.
"""

from __future__ import annotations

import argparse
import csv
import difflib
from pathlib import Path

from .mmat_current import (
    CURRENT_MMAT_STUDY_IDS,
    CURRENT_EMPIRICAL_STUDY_IDS,
    PENDING_FULL_TEXT_STUDY_IDS,
    load_component_reassessments,
    validate_current_artifacts,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = REPO_ROOT / "research" / "data" / "mmat_reassessment_current.csv"
COMPONENT_DATA_PATH = REPO_ROOT / "research" / "data" / "mmat_component_reassessment_current.csv"
PAPERS_PATH = REPO_ROOT / "research" / "exports" / "analysis" / "papers.csv"
OUTPUT_PATH = (
    REPO_ROOT / "research" / "exports" / "references" / "mmat_current_tcc_table.tex"
)

CRITERIA = ("s1", "s2", "q1", "q2", "q3", "q4", "q5")
COMPONENT_CRITERIA = ("c1", "c2", "c3", "c4", "c5")
DESIGN_LABELS = {
    "quantitative_descriptive": "Quant. descritivo",
    "quantitative_nonrandomized": "Quant. não rand.",
    "quantitative_randomized": "Quant. rand.",
    "qualitative": "Qualitativo",
    "mixed_methods": "Métodos mistos",
    "metadata_hold": "Não confirmado",
    "not_applicable": "Não aplicável",
    "design_pending": "Pendente",
}
BASIS_LABELS = {
    "primary_full_text_reviewed_externally": "Texto primário externo",
    "primary_full_text_scope_exclusion": "Texto integral; fora do escopo",
    "pending_full_text_not_appraised": "Texto pendente; sem MMAT",
    "abstract_and_metadata_only": "Resumo/metadados",
    "abstract_only": "Resumo",
    "metadata_only": "Metadados",
    "protocol_or_proposal_not_applicable": "Protocolo/proposta",
}
def load_rows(path: Path = DATA_PATH) -> list[dict[str, str]]:
    validate_current_artifacts(reassessment_path=path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    record_ids = [int(row["study_id"]) for row in rows]
    if record_ids != [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 6915, 6916, 6917, 6919, 6920, 6921, 6923]:
        raise ValueError(f"Unexpected 18-record MMAT audit ledger IDs: {record_ids}")
    rows = [row for row in rows if int(row["study_id"]) in CURRENT_MMAT_STUDY_IDS]
    ids = [int(row["study_id"]) for row in rows]
    if ids != list(CURRENT_MMAT_STUDY_IDS):
        raise ValueError(f"Expected empirical MMAT IDs {list(CURRENT_MMAT_STUDY_IDS)}; found {ids}")
    for row in rows:
        if row.get("assessment_status") == "final":
            raise ValueError("The current TCC table cannot render final MMAT claims")
        for criterion in CRITERIA:
            if row.get(criterion) not in {"", "Y", "N", "CT"}:
                raise ValueError(f"Invalid {criterion} value for study {row.get('study_id')}")
    return rows


def load_study_labels(path: Path = PAPERS_PATH) -> dict[str, str]:
    """Return reader-facing author/year labels for the current MMAT rows."""

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))

    labels: dict[str, str] = {}
    for record in records:
        study_id = str(record.get("id", "")).strip()
        if not study_id or not record.get("year"):
            continue
        authors = str(record.get("authors", "")).strip()
        first_author = authors.split(";")[0].strip()
        if "," in first_author:
            family_name = first_author.split(",", 1)[0].strip()
        else:
            family_name = first_author.split()[-1] if first_author else ""
        if not family_name:
            family_name = str(record.get("paper_id", study_id)).strip()
        suffix = " et al." if ";" in authors else ""
        labels[study_id] = f"{family_name}{suffix} ({record['year']})"

    return labels


def _latex_escape(value: object) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "/": r"/\allowbreak{}",
    }
    return "".join(replacements.get(char, char) for char in str(value))


def load_component_rows(path: Path = COMPONENT_DATA_PATH) -> list[dict[str, str]]:
    load_component_reassessments(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if int(row["study_id"]) in CURRENT_MMAT_STUDY_IDS]


def render_component_table(
    components: list[dict[str, str]], labels: dict[str, str] | None = None
) -> str:
    if not components:
        return ""
    labels = labels or load_study_labels()
    category_labels = {
        "qualitative": "Qualitativo",
        "quantitative_nonrandomized": "Quant. não rand.",
        "quantitative_descriptive": "Quant. descritivo",
    }
    criterion_prefix = {
        "qualitative": "1",
        "quantitative_nonrandomized": "3",
        "quantitative_descriptive": "4",
    }
    lines = [
        "% Quadro gerado de research/data/mmat_component_reassessment_current.csv",
        r"\clearpage",  # Keep legacy longtable anchors with the first-page caption.
        r"\begingroup",
        r"\SingleSpacing",
        r"\def\LTcaptype{quadro}",
        r"\fontsize{10}{11.5}\selectfont",
        r"\setlength{\tabcolsep}{2pt}",
        r"\renewcommand{\arraystretch}{1.15}",
        r"\begin{longtable}{|>{\raggedright\arraybackslash}p{2.2cm}|>{\raggedright\arraybackslash}p{2.2cm}|ccccc|>{\raggedright\arraybackslash}p{6.1cm}|}",
        r"\caption{Apreciação preliminar dos componentes qualitativos e quantitativos em estudos de métodos mistos.}\label{qua:mmat-componentes}\\",
        r"\hline",
        r"\textbf{Estudo} & \textbf{Componente} & \textbf{C1} & \textbf{C2} & \textbf{C3} & \textbf{C4} & \textbf{C5} & \textbf{Síntese dos julgamentos e localizador} \\",
        r"\hline",
        r"\endfirsthead",
        r"\multicolumn{8}{c}{\quadroname\ \thequadro\ -- Continuação}\\",
        r"\hline",
        r"\textbf{Estudo} & \textbf{Componente} & \textbf{C1} & \textbf{C2} & \textbf{C3} & \textbf{C4} & \textbf{C5} & \textbf{Síntese dos julgamentos e localizador} \\",
        r"\hline",
        r"\endhead",
        r"\hline",
        r"\multicolumn{8}{r}{\textit{Continua na próxima página}}\\",
        r"\endfoot",
        r"\hline",
        r"\endlastfoot",
    ]
    for row in components:
        prefix = criterion_prefix[row["design"]]
        rationales = [
            f"{prefix}.{index} ({row[criterion]}): {row[f'evidence_{criterion}']}"
            for index, criterion in enumerate(COMPONENT_CRITERIA, start=1)
        ]
        rationales.append(f"Localizador: {row['source_locator']}")
        values = [
            _latex_escape(labels.get(row["study_id"], row["study_key"])),
            _latex_escape(category_labels[row["design"]]),
            *[row[criterion] for criterion in COMPONENT_CRITERIA],
            _latex_escape(" ".join(rationales)),
        ]
        lines.append(" & ".join(values) + r" \\")
    lines.extend([
        r"\end{longtable}",
        r"\fonte{Elaborado pelo autor (2026).}",
        r"\textit{Nota:} C1--C5 correspondem aos cinco critérios da categoria indicada: 1.1--1.5 (qualitativo), 3.1--3.5 (quantitativo não randomizado) e 4.1--4.5 (quantitativo descritivo). Y = sim; N = não; CT = não é possível concluir. Os registros documentais são provisórios, sem pontuação global; a conferência humana permanece pendente.",
        r"\endgroup",
    ])
    return "\n".join(lines)


def render_table(
    rows: list[dict[str, str]], labels: dict[str, str] | None = None
) -> str:
    labels = labels or load_study_labels()
    lines = [
        "% Quadro gerado de research/data/mmat_reassessment_current.csv",
        "% Reavaliação documental preliminar; não representa score nem avaliação final.",
        "% Não editar manualmente; execute: python -m src.analysis.mmat_current_tcc_table",
        r"\clearpage",  # Keep the legacy CI destination on the caption page.
        r"\begingroup",
        r"\SingleSpacing",
        r"\fontsize{10}{11.5}\selectfont",
        r"\def\LTcaptype{quadro}",
        r"\setlength{\tabcolsep}{2pt}",
        r"\setlength{\LTcapwidth}{\textwidth}",
        r"\begin{longtable}{|>{\raggedright\arraybackslash}p{3.0cm}|"
        r">{\raggedright\arraybackslash}p{2.5cm}|ccccccc|"
        r">{\raggedright\arraybackslash}p{3.6cm}|}",
        rf"\caption{{Triagem e respostas documentais preliminares ao MMAT 2018 de {len(rows)} registros do corpus.}}\label{{qua:mmat-reavaliacao-atual}}\\",
        r"\hline",
        r"\textbf{Estudo} & \textbf{Desenho} & "
        r"\textbf{S1} & \textbf{S2} & \textbf{Q1} & \textbf{Q2} & "
        r"\textbf{Q3} & \textbf{Q4} & \textbf{Q5} & \textbf{Base} \\",
        r"\hline",
        r"\endfirsthead",
        r"\multicolumn{10}{c}{\quadroname\ \thequadro\ -- Continuação}\\",
        r"\hline",
        r"\textbf{Estudo} & \textbf{Desenho} & "
        r"\textbf{S1} & \textbf{S2} & \textbf{Q1} & \textbf{Q2} & "
        r"\textbf{Q3} & \textbf{Q4} & \textbf{Q5} & \textbf{Base} \\",
        r"\hline",
        r"\endhead",
        r"\hline",
        r"\multicolumn{10}{r}{\textit{Continua na próxima página}}\\",
        r"\endfoot",
        r"\hline",
        r"\endlastfoot",
    ]
    for row in rows:
        design = row.get("design") or row.get("design_status") or "not_applicable"
        if row.get("assessment_status") == "hold_source_verification":
            design = "metadata_hold"
        design_label = DESIGN_LABELS.get(design, design)
        if row.get('design_status') == 'operational_category_inferred_allocation_unknown':
            design_label = 'Cat. 3 operacional (alocação incerta)'
        elif row.get('design_status') == 'operational_category_adaptation':
            design_label = 'Cat. 4 adaptada (modelagem)'
        elif row.get('design_status') == 'design_reassessed_provisional_with_allocation_conflict':
            design_label = 'Cat. 2 declarada (contraditória)'
        if row["study_id"] == "6915":
            design_label += " (componente escolar)"
        values = [
            _latex_escape(labels.get(row["study_id"], row["study_key"])),
            _latex_escape(design_label),
            *[row[criterion] or "---" for criterion in CRITERIA],
            _latex_escape(BASIS_LABELS.get(row["assessment_basis"], row["assessment_basis"])),
        ]
        lines.append(" & ".join(values) + r" \\")
    note = (
        r"\textit{Nota:} Registros provisórios, conferência humana pendente, sem escore agregado. "
        r"S1 e S2 são perguntas de triagem. "
        r"Q1--Q5 correspondem aos critérios MMAT da categoria; "
        r"Y/N/CT = sim/não/não é possível concluir. "
        r"Quant. = quantitativo; rand. = randomizado. "
        r"Base = fonte consultada. "
        r"Ver Seção~\ref{sec:qualidade-estudos}. "
        rf"Denominador: {len(rows)} registros."
    )
    lines.extend([
        r"\end{longtable}",
        r"\fonte{Elaborado pelo autor (2026).}",
        r"\textit{Cobertura:} S1/S2 e Q1--Q5 apreciados para 15 registros. As categorias 3 dos estudos 5 e 7 são rotas operacionais com alocação desconhecida; a categoria 4 do estudo 8 é adaptação para modelagem computacional; a categoria 2 do estudo 14 corresponde ao sorteio declarado, mas contraditório. Não são classificações confirmadas. --- significa não avaliado, não CT.",
        note,
        r"\endgroup",
    ])
    component_table = render_component_table(load_component_rows(), labels)
    if component_table:
        lines.extend(["", component_table])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render_table(load_rows())
    if args.check:
        actual = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if actual != expected:
            diff = "".join(
                difflib.unified_diff(
                    actual.splitlines(keepends=True),
                    expected.splitlines(keepends=True),
                    fromfile=str(OUTPUT_PATH),
                    tofile="generated",
                )
            )
            raise SystemExit(f"Current MMAT TCC export is stale:\n{diff}")
        return
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(expected, encoding="utf-8")


if __name__ == "__main__":
    main()
