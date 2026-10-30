"""Render content summaries from the existing corpus, without running a search."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GROUPS = {
    "quantitative_descriptive": "Quantitativo descritivo",
    "quantitative_nonrandomized": "Quantitativo não randomizado",
    "quantitative_randomized": "Quantitativo randomizado",
    "mixed_methods": "Métodos mistos",
    "qualitative": "Qualitativo",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def study_rows(root: Path = ROOT) -> list[dict[str, str]]:
    return read_csv(root / "research/data/study_synthesis_current.csv")


def mmat_counts(root: Path = ROOT) -> dict[str, dict[str, dict[str, int]]]:
    included = {row["study_key"] for row in read_csv(root / "research/data/current_synthesis_scope.csv")
                if row["record_status"] == "included_empirical_core"}
    rows = [row for row in read_csv(root / "research/data/mmat_reassessment_current.csv")
            if row["study_key"] in included]
    groups = {"screening": rows}
    groups.update({key: [row for row in rows if row["design"] == key]
                   for key in sorted({row["design"] for row in rows})})
    return {group: {criterion: dict(Counter(row[criterion] for row in selected))
                    for criterion in (("s1", "s2") if group == "screening"
                                      else ("q1", "q2", "q3", "q4", "q5"))}
            for group, selected in groups.items()}


def tex(value: str) -> str:
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
                    "_": r"\_", "#": r"\#", "$": r"\$", "{": r"\{", "}": r"\}"}
    escaped = "".join(replacements.get(char, char) for char in value)
    escaped = escaped.replace("/", r"/\allowbreak{}")
    return re.sub(r"\b(Random Forest|Naive Bayes|feedforward|wrapper|jigsaw|stacking|feedback|deep learning|transformers|macro-average)\b",
                  lambda match: r"\textit{" + match[0] + "}", escaped)


def component_counts(root: Path = ROOT) -> dict[str, dict[str, dict[str, int]]]:
    rows = read_csv(root / "research/data/mmat_component_reassessment_current.csv")
    return {design: {f"c{i}": dict(Counter(row[f"c{i}"] for row in rows if row["design"] == design))
                     for i in range(1, 6)} for design in sorted({row["design"] for row in rows})}


def longtable(caption: str, label: str, widths: str, headers: list[str], rows: list[list[str]]) -> str:
    heading = " & ".join(r"\textbf{" + header + "}" for header in headers) + r" \\ \hline"
    return "\n".join([
        r"\begingroup\small\setlength{\tabcolsep}{3pt}\def\LTcaptype{quadro}",
        r"\setlength{\LTleft}{0pt}",
        r"\setlength{\LTcapwidth}{\textwidth}\renewcommand{\arraystretch}{1.12}",
        r"\begin{longtable}{" + widths + "}",
        r"\caption{" + caption + r"}\label{" + label + r"}\\\hline",
        heading, r"\endfirsthead",
        r"\multicolumn{" + str(len(headers)) + r"}{c}{\quadroname\ \thequadro\ -- Continuação}\\\hline",
        heading, r"\endhead", r"\hline\endfoot\hline\endlastfoot",
        *[" & ".join(row) + r" \\ \hline" for row in rows],
        r"\end{longtable}\endgroup", r"\fonte{Elaborado pelo autor (2026).}", "",
    ])


def build_outputs(root: Path = ROOT) -> dict[str, str]:
    studies = study_rows(root)
    widths = "|" + "|".join(r">{\raggedright\arraybackslash}p{" + width + "cm}"
                             for width in ("2.8", "3.3", "4.1", "4.5")) + "|"
    first = [[rf"\citeonline{{{row['study_key']}}}", tex(row["purpose"]),
              tex(row["technique"]), tex(row["level"] + "; " + row["sample"])] for row in studies]
    second = [[rf"\citeonline{{{row['study_key']}}}", tex(row["target"]),
               tex(row["validation"] + " (" + row["source"] + ")"), tex(row["metric"])] for row in studies]
    text = longtable("Finalidade, técnica e população dos estudos incluídos.", "qua:sintese-tipologia", widths,
                     ["Estudo", "Finalidade principal", "Família de técnica", "Nível e n (unidade)"], first)
    text += longtable("Alvos, validação e métricas dos estudos incluídos.", "qua:sintese-validacao", widths,
                      ["Estudo", "Alvo", "Validação e fonte", "Métrica ou resultado reportado"], second)
    frequencies = Counter(row["purpose"] for row in studies)
    text += "\n".join([
        r"\begin{table}[htbp]\centering",
        r"\caption{Frequência da finalidade principal no corpus de 15 estudos.}\label{tab:tipologia-frequencias}",
        r"\begin{tabular}{lr}\hline Finalidade & Estudos (n) \\ \hline",
        *[f"{tex(purpose)} & {count}" + r" \\" for purpose, count in frequencies.items()],
        r"\hline Total & 15 \\ \hline\end{tabular}",
        r"\fonte{Elaborado pelo autor (2026).}\end{table}", "",
    ])
    count_rows = []
    for group, criteria in mmat_counts(root).items():
        group_name = "Triagem (todos os estudos)" if group == "screening" else GROUPS[group]
        for criterion, values in criteria.items():
            count_rows.append([tex(group_name), criterion.upper(),
                               *[str(values.get(answer, 0)) for answer in ("Y", "N", "CT")],
                               str(sum(values.values()))])
    counts_tex = longtable("Respostas MMAT por critério e categoria de desenho.", "qua:mmat-contagens",
                           "|p{6.3cm}|c|r|r|r|r|", ["Categoria", "Critério", "Y", "N", "CT", "n"], count_rows)
    component_rows = [[tex(GROUPS[group]), criterion.upper(),
                       *[str(values.get(answer, 0)) for answer in ("Y", "N", "CT")],
                       str(sum(values.values()))]
                      for group, criteria in component_counts(root).items()
                      for criterion, values in criteria.items()]
    counts_tex += longtable("Contagens separadas dos componentes dos três estudos mistos.",
                            "qua:mmat-contagens-componentes", "|p{6.3cm}|c|r|r|r|r|",
                            ["Categoria do componente", "Critério", "Y", "N", "CT", "n"], component_rows)
    return {"research/exports/references/study_synthesis_tcc.tex": text,
            "research/exports/references/mmat_counts_tcc.tex": counts_tex}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for relative, text in build_outputs().items():
        path = ROOT / relative
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(relative)
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
    if stale:
        print("Stale content tables: " + ", ".join(stale))
        return 1
    print("Content synthesis tables match the corpus and MMAT responses.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
