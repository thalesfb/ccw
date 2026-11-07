"""Synchronize bounded documentary facts; never adjudicate studies or MMAT.

Generated blocks follow the manuscript and versioned evidence. A separate,
explicit review binding detects subsequent changes to manual summaries and
images. It records an assisted consistency review, not scientific approval.
"""

import argparse
import csv
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INTRO = "results/tcc/conteudo/introducao.tex"
MANIFEST = "research/exports/reports/reproducibility_manifest.json"
RECORD_CORRECTIONS = "research/data/adjudicated_record_corrections.csv"
SELECTION_STATUS = "research/data/selection_status_current.json"
CONTRIBUTIONS = "research/data/study_contribution_current.json"
EVIDENCE = "research/data/evidence_sources_current.json"
OVERVIEW = "results/tcc/images/project_overview_2026-11-03.png"
REVIEW_RECORD = "docs/tcc/documentation_consistency_review.json"
INPUTS = (
    INTRO, MANIFEST, CONTRIBUTIONS, EVIDENCE, RECORD_CORRECTIONS, SELECTION_STATUS,
    "results/tcc/conteudo/fundamentacao.tex",
    "results/tcc/conteudo/metodologia.tex",
    "results/tcc/conteudo/resultadosesperados.tex",
    "results/tcc/conteudo/prototipo.tex",
    "results/tcc/conteudo/rastreabilidade-requisitos.tex",
    "results/tcc/conteudo/aceitacao-cenarios.tex",
    "results/tcc/conteudo/arquitetura-figura.tex",
    "results/tcc/conteudo/protocolo-docente.tex",
    "results/tcc/conteudo/estudos-requisitos.tex",
    "results/tcc/conteudo/resultados.tex",
    "results/tcc/conteudo/conclusao.tex",
    "results/tcc/pretextuais/resumo.tex",
    "results/tcc/postextuais/apendice.tex",
    "results/tcc/postextuais/ferramentas-ia.tex",
    "results/tcc/config_inicial.tex",
    "research/src/analysis/mmat_current_tcc_table.py",
    "research/exports/references/mmat_component_details_tcc.tex",
    "scripts/tcc_quadros.json",
    "scripts/validate_tcc_quadros.py",
    "research/data/current_synthesis_scope.csv",
    "research/data/mmat_reassessment_current.csv",
    "research/data/mmat_component_reassessment_current.csv",
    "research/data/study_synthesis_current.csv",
    "research/exports/references/study_synthesis_tcc.tex",
    "research/exports/references/mmat_counts_tcc.tex",
    "research/src/analysis/content_synthesis.py",
    "docs/tcc/ABNT-2025-CORRECOES.md",
    "research/src/cli.py",
)
TARGETS = {
    "README.md": ("snapshot", "goals", "flow"),
    "research/README.md": ("snapshot",),
    "docs/tcc/ESTADO-ATUAL-TCC.md": ("snapshot", "coverage"),
    "docs/tcc/SOURCE-COVERAGE-AND-CONTRIBUTIONS.md": ("coverage", "sources"),
    "docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md": ("flow",),
    "presentation/README.md": ("goals",),
    "results/tcc/README.md": ("goals",),
}
REVIEW_TARGETS = (
    *TARGETS,
    "docs/README.md", "docs/tcc/README.md",
    "docs/tcc/AUDITORIA-ESTUDOS-SINTESE.md",
    "docs/tcc/REUNIAO-DECISAO-ESCOPO.md",
    "docs/tcc/NORMATIVE_GOVERNANCE.md",
    "docs/TCC_REVISION_SCOPE.md",
    "docs/VERIFICACAO-NUMEROS-PRISMA.md",
    "docs/tcc/AUDITORIA-DIVERGENCIAS-ESPECIFICACAO-CODIGO.md",
    "results/tcc/images/README.md",
    "index.html", "research/index.html", "results/tcc/index.html",
    "presentation/slides.md",
    "results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md",
    "scripts/generate_tcc_presentation.py",
    "scripts/sync_project_docs.py",
    "results/tcc/presentation/ensino_personalizado_de_matematica_tcc.pptx",
    OVERVIEW,
)


def marker(name, content):
    return f"<!-- ccw-sync:start {name} -->\n{content}\n<!-- ccw-sync:end {name} -->"


def read_json(root, relative):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def day(value):
    return date.fromisoformat(value).strftime("%d/%m/%Y")


def number(value):
    return f"{value:,}".replace(",", ".")


def percentage(numerator, denominator):
    return f"{100 * numerator / denominator:.2f}".replace(".", ",") if denominator else "0,00"


def plain_tex(value):
    value = " ".join(value.split())
    if "\\" in value or "{" in value or "}" in value:
        raise ValueError("unsupported TeX in goals; review the extraction explicitly")
    return value


def goals(root):
    intro = (root / INTRO).read_text(encoding="utf-8")
    section = intro.split(r"\section{Objetivos}", 1)[1].split(
        r"\section{Estrutura do Trabalho}", 1
    )[0].strip()
    general_source = section.split("\n\n", 1)[0]
    general_match = re.search(r"definiu-se como objetivo geral (.+?)\.\s*$", general_source)
    if not general_match:
        raise ValueError("cannot extract the manuscript's general objective")
    general = plain_tex(general_match.group(1).strip())
    general = general[:1].upper() + general[1:] + "."
    objectives = re.findall(
        r"^\\item \((OE\d+)\) ([^;\n]+)[;.]\s*$",
        section,
        re.M,
    )
    if [key for key, _ in objectives] != [f"OE{i}" for i in range(1, 5)]:
        raise ValueError("cannot extract sequential manuscript objectives")
    parts = ["### Objetivo geral", plain_tex(general), "### Objetivos específicos"]
    for key, description in objectives:
        clean_description = plain_tex(description).rstrip("; .")
        parts.append(f"**{key}:** {clean_description}.")
    return "\n\n".join(parts)


def page_ranges(pages):
    runs = []
    for page in sorted(set(pages)):
        if runs and page == runs[-1][-1] + 1:
            runs[-1].append(page)
        else:
            runs.append([page])
    return ", ".join(str(run[0]) if len(run) == 1 else f"{run[0]}–{run[-1]}" for run in runs) or "nenhuma"


def render_blocks(root):
    manifest = read_json(root, MANIFEST)
    matrix = read_json(root, CONTRIBUTIONS)
    evidence = read_json(root, EVIDENCE)
    counts = manifest["snapshot"]["counts"]["prisma"]
    deduplication = manifest["snapshot"]["deduplication_audit"]
    qa = manifest["methodological_appraisal"]["current_mmat_qa"]
    status = read_json(root, SELECTION_STATUS)
    retrieval = status["current_source_retrieval"]
    if status["status"] != "historical_snapshot_unchanged" or status["eligibility_criteria_changed"]:
        raise ValueError("selection status must describe the unchanged current snapshot")
    with (root / RECORD_CORRECTIONS).open("r", encoding="utf-8-sig", newline="") as handle:
        corrections = list(csv.DictReader(handle))
    identity_reconciliation_date = max(row["decision_date"] for row in corrections)
    deterministic_duplicates = int(deduplication["deterministic_identity_duplicate_rows"])
    same_report_duplicates = int(deduplication["adjudicated_same_report_duplicate_rows"])
    if deterministic_duplicates + same_report_duplicates != int(counts["duplicates_removed"]):
        raise ValueError("PRISMA duplicate total disagrees with the record-correction ledgers")
    records = matrix["records"]
    local = sum(record["full_text_available_locally"] for record in records)
    missing = [record["study_id"] for record in records if not record["full_text_available_locally"]]
    coverage = evidence["source_coverage"]
    if local != coverage["identified_local_pdf_count"] or set(missing) != set(coverage["missing_study_ids"]):
        raise ValueError("source availability disagrees across the versioned manifests")
    dates = (f"Corte da busca: {day(manifest['protocol']['cutoff_date'])}; "
             f"adjudicação inicial: {day(manifest['snapshot_date'])}; "
             f"reconciliação do escopo: {day(manifest['scope_updated_at'])}; "
             f"reconciliação de identidade e ano: {day(identity_reconciliation_date)}; "
             f"cobertura documental: {day(matrix['review_date'])}.")
    snapshot = (
        f"{dates}\n\n"
        f"O snapshot registra {number(counts['identification'])} registros identificados e "
        f"{counts['duplicates_removed']} duplicatas removidas: {deterministic_duplicates} por identidade DOI/URL "
        f"e {same_report_duplicates} relatórios confirmados manualmente como repetidos. Foram "
        f"{number(counts['screening'])} registros únicos na triagem, dos quais "
        f"{number(counts['screening_excluded'])} foram excluídos ({percentage(counts['screening_excluded'], counts['screening'])}%). "
        f"{number(counts['prioritization'])} avançaram à priorização histórica "
        f"({percentage(counts['prioritization'], counts['screening'])}% da triagem); "
        f"{number(counts['prioritization_excluded'])} não avançaram sob a regra histórica "
        f"({percentage(counts['prioritization_excluded'], counts['prioritization'])}%). "
        f"O corte 4,0 permanece inalterado e o relato descreve o conjunto adotado nesta versão. A priorização histórica "
        f"encaminhou {counts['shortlisted']} registros à lista preliminar "
        f"({percentage(counts['shortlisted'], counts['prioritization'])}%), não a inclusões finais: "
        f"{counts['included']} estudos empíricos mantidos na seleção histórica, dos quais "
        f"{retrieval['recovered_empirical_reports']} têm relatório recuperado; Sokkhey permanece "
        f"sem cópia verificável, como inclusão histórica. Houve "
        f"{counts['abstract_screening_excluded']} exclusão após resumo. Dos "
        f"{retrieval['reports_sought']} relatórios procurados, {retrieval['reports_not_retrieved']} não foram recuperados "
        f"({' e '.join(retrieval['not_retrieved_labels'])}); "
        f"{retrieval['reports_assessed_at_full_text']} foram avaliados em texto completo, incluindo "
        f"{retrieval['full_text_exclusions']} protocolo excluído. "
        f"No MMAT preliminar, há {qa['screening_rows']} triagens S1/S2 e "
        f"{qa['category_appraised_rows']} apreciações por categoria; "
        f"não há escore agregado nem aprovação científica final."
    )
    flow_rows = [
        ("Identificação", counts["identification"], "Registros no snapshot versionado"),
        ("Duplicatas removidas", counts["duplicates_removed"], f"{deterministic_duplicates} por DOI/URL; {same_report_duplicates} relatórios iguais confirmados manualmente"),
        ("Triagem", counts["screening"], f"{number(counts['screening_excluded'])} excluídos"),
        ("Priorização histórica", counts["prioritization"], f"{number(counts['prioritization_excluded'])} não avançaram sob as regras históricas: 2.459 por pontuação e cinco por escopo"),
        ("Lista preliminar", counts["shortlisted"], f"{counts['abstract_screening_excluded']} exclusão após resumo"),
        ("Relatórios procurados", retrieval["reports_sought"], f"{retrieval['reports_not_retrieved']} não recuperados: Sokkhey e Zeng"),
        ("Relatórios avaliados em texto completo", retrieval["reports_assessed_at_full_text"], f"{retrieval['full_text_exclusions']} protocolo excluído; 14 relatórios empíricos recuperados"),
        ("Relatórios empíricos recuperados", retrieval["recovered_empirical_reports"], "Os 14 relatórios com texto recuperado; protocolo excluído não incluído"),
        ("Seleção histórica de estudos empíricos", retrieval["historical_empirical_selection"], "Inclui Sokkhey sem cópia verificável; seleção e corte 4,0 preservados"),
    ]
    flow = "| Etapa | Quantidade | Interpretação |\n| --- | --- | --- |\n" + "\n".join(
        f"| {label} | {number(value)} | {meaning} |" for label, value, meaning in flow_rows
    )
    replay = evidence["replay_validation"]
    coverage_text = (
        f"Em {day(matrix.get('availability_check_date', matrix['review_date']))}, há **{local} de {len(records)} PDFs locais** "
        f"identificados por hash; faltam os registros **{' e '.join(missing)}**. "
        f"Essa disponibilidade não altera retroativamente as etapas PRISMA nem comprova leitura humana integral. "
        f"O replay textual congelado de {day(replay['validation_date'])} abrange "
        f"**{replay['checked_source_count']} fontes e {replay['checked_chunk_count']} trechos**, "
        f"não os {local} PDFs atuais. As fontes suplementares não foram incorporadas a esse replay. "
        f"A leitura documental assistida e a revisão científica humana são estados distintos."
    )
    table = ["| ID e referência primária | Páginas físicas com texto examinado | Contribuição delimitada |",
             "| --- | --- | --- |"]
    for record in records:
        link = record["source_url"]
        pages = page_ranges(record["physical_text_pages_read"])
        contribution = record["contribution"].replace("|", r"\|").replace("\n", " ")
        table.append(f"| {record['study_id']} — [{record['study_key']}]({link}) | {pages} | {contribution} |")
    return {"goals": goals(root), "snapshot": snapshot, "flow": flow,
            "coverage": coverage_text, "sources": "\n".join(table)}


def synchronize(root, write=False):
    blocks = render_blocks(root)
    updates = {}
    for relative, names in TARGETS.items():
        path = root / relative
        original = text = path.read_text(encoding="utf-8")
        for name in names:
            start, end = f"<!-- ccw-sync:start {name} -->", f"<!-- ccw-sync:end {name} -->"
            if text.count(start) != 1 or text.count(end) != 1 or text.index(start) > text.index(end):
                raise ValueError(f"missing, duplicated or reversed marker {name}: {relative}")
            first, last = text.index(start), text.index(end) + len(end)
            text = text[:first] + marker(name, blocks[name]) + text[last:]
        if text != original:
            updates[relative] = text
    if write:
        for relative, text in updates.items():
            (root / relative).write_text(text, encoding="utf-8", newline="\n")
    return list(updates)


def fingerprint(root, relative):
    content = (root / relative).read_bytes()
    if Path(relative).suffix in {".md", ".tex", ".json", ".csv", ".html", ".py"}:
        content = content.replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()


def bindings(root):
    return {
        "canonical_inputs": {relative: fingerprint(root, relative) for relative in INPUTS},
        "reviewed_surfaces": {relative: fingerprint(root, relative) for relative in REVIEW_TARGETS},
    }


def review_issues(root):
    path = root / REVIEW_RECORD
    if not path.exists():
        return ["manual summaries and images require an explicit consistency review"]
    record, current = read_json(root, REVIEW_RECORD), bindings(root)
    issues = []
    if record.get("canonical_inputs") != current["canonical_inputs"]:
        issues.append("canonical inputs changed; review all current summaries and images")
    for relative, digest in current["reviewed_surfaces"].items():
        if record.get("reviewed_surfaces", {}).get(relative) != digest:
            issues.append(f"review binding changed: {relative}")
    if record.get("review_kind") != "assisted_consistency_review" or record.get("human_scientific_approval") != "pending":
        issues.append("invalid consistency-review disclosure")
    return issues


def record_review(root):
    if synchronize(root):
        raise ValueError("generated blocks are stale; synchronize before recording review")
    record = {"schema_version": 1, "review_kind": "assisted_consistency_review",
              "human_scientific_approval": "pending", **bindings(root)}
    (root / REVIEW_RECORD).write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--record-review", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.record_review:
            record_review(args.root)
            print("Assisted consistency review recorded; human scientific approval remains pending.")
        else:
            stale = synchronize(args.root, write=args.write)
            issues = [] if args.write else review_issues(args.root)
            for relative in stale:
                print(f"{'Updated' if args.write else 'Stale generated blocks'}: {relative}")
            for issue in issues:
                print(issue)
            if args.check and (stale or issues):
                return 1
            print("Generated blocks updated; manual review is separate." if args.write
                  else "Documentation bindings are current; scientific approval is not certified.")
    except (OSError, ValueError, KeyError) as error:
        print(f"Documentation check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
