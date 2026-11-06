"""Trace unresolved MMAT decisions to prepared, unsent clarification questions."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .mmat_current import load_current_reassessment, load_component_reassessments

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "research/data/mmat_followup_questions_current.csv"
REPORT = ROOT / "docs/tcc/MMAT-PERGUNTAS-PENDENTES.md"
HOLDS = {("3", "access"), ("6923", "access")}
COVERAGE_LABELS = {
    "insufficient_in_examined_material": "Informação insuficiente no material examinado",
    "criterion_review_incomplete": "Exame do critério ainda incompleto",
    "historical_copy_unavailable": "Cópia histórica indisponível para revalidação",
    "document_not_recovered": "Documento não recuperado; sem MMAT",
    "basis_not_established": "Origem da insuficiência não distinguível no registro público",
}
LABELS = {"study": "critérios principais", "record": "pendência do registro",
          "qualitative": "componente qualitativo", "quantitative": "componente quantitativo",
          "unit": "unidade de apreciação", "design": "delineamento", "access": "acesso ao texto"}


def load_questions():
    with DATA.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def validate_questions(questions):
    coverage_records = json.loads((ROOT / "research/data/study_contribution_current.json").read_text(encoding="utf-8"))["records"]
    expected = {
        (r["study_id"], "study", k.upper())
        for r in load_current_reassessment()
        for k in ("s1", "s2", "q1", "q2", "q3", "q4", "q5") if r[k] == "CT"
    } | {
        (r["study_id"], r["component"], k.upper())
        for r in load_component_reassessments()
        for k in ("c1", "c2", "c3", "c4", "c5") if r[k] == "CT"
    } | {(sid, "record", criterion) for sid, criterion in HOLDS}
    keys = [(q["study_id"], q["component"], q["criterion"]) for q in questions]
    if len(set(keys)) != len(keys) or set(keys) != expected:
        raise ValueError("MMAT followup coverage differs from unresolved ledger criteria/holds")
    for q in questions:
        if q["status"] != "prepared_not_sent" or not all(
            q.get(k, "").strip() for k in ("request_id", "source_id", "evidence_locator", "question_pt", "intended_recipient")
        ):
            raise ValueError("MMAT followup lacks provenance or unsent status")
        prefix = "research/data/study_contribution_current.json#/records/"
        reference = q.get("coverage_reference", "")
        if (q.get("coverage_status") not in COVERAGE_LABELS
                or not reference.startswith(prefix)
                or not reference[len(prefix):].isdigit()
                or not q.get("coverage_notes", "").strip()):
            raise ValueError("MMAT followup lacks valid coverage metadata")
        index = int(reference[len(prefix):])
        if index >= len(coverage_records) or coverage_records[index]["study_id"] != q["study_id"]:
            raise ValueError("MMAT followup coverage points to a different source")
        record = coverage_records[index]
        unavailable = not record["full_text_available_locally"]
        if unavailable != (q["coverage_status"] in {"historical_copy_unavailable", "document_not_recovered"}):
            raise ValueError("MMAT followup coverage disagrees with source access")
        if (q["coverage_status"] == "document_not_recovered") != (record["record_status"] == "awaiting_full_text"):
            raise ValueError("MMAT followup coverage confuses a historical appraisal with a non-appraised report")


def render_markdown(questions):
    validate_questions(questions)
    lines = ["# Perguntas pendentes para completar a apreciação MMAT", "",
             "Revisão documental iniciada em 28/10/2026, atualizada em 06/11/2026 após as decisões sobre os estudos mistos. Perguntas preparadas, não enviadas. Não há respostas de autores registradas neste documento.", "",
             "As perguntas abaixo correspondem aos critérios ainda indeterminados, separados entre apreciação principal e componentes, e às pendências de acesso ao texto. Não constituem escore de qualidade.", "",
             "Cada pergunta identifica a fonte, o critério e o limite da evidência disponível. Informação insuficiente no material examinado é distinta de exame ainda incompleto ou cópia indisponível. Quando a cobertura pública é parcial e não permite distinguir essas origens, essa incerteza fica explícita. Leitura do texto extraível não certifica exame integral de figuras, tabelas e fórmulas.", "",
             "CT é uma conclusão de insuficiência de informação, não uma tarefa necessariamente incompleta. A consolidação não exige eliminar todos os CT ou obter resposta a todas as perguntas. As tarefas efetivas, seus responsáveis, evidências e próximos passos estão em `research/data/mmat_consolidation_actions_current.json` e na seção de consolidação da página MMAT. As perguntas sobre Q4 de 6919 e Q3/Q4 de 6920 foram retiradas após a revisão das fontes e as decisões do autor, registradas com suas justificativas no CSV da apreciação atual.", "",
             "As rotas de apreciação dos estudos 5, 7, 8 e 14 foram decididas operacionalmente nesta revisão, com limitações explícitas. Alocação e demais lacunas não foram resolvidas por inferência. As perguntas foram redigidas para eventual esclarecimento dos autores; destinatários e encaminhamento ainda precisam ser definidos pelo responsável. Nenhum contato externo foi realizado nesta revisão.", "",
             "A fonte 3 não foi revalidada nesta rodada; suas perguntas derivam dos registros anteriores e exigem recuperação do original antes de alterar os julgamentos. O estudo 6919 foi revalidado no PDF primário em 29/10/2026: as respostas foram mantidas e os localizadores passaram a páginas físicas. Para 6923, a consulta oficial de 28/10/2026 confirmou o embargo até 16/05/2027; o texto integral não foi recuperado e não há apreciação MMAT. Simulação pode constituir pesquisa empírica; no estudo 8, a unidade agora é uma tese/um relatório com componentes matemáticos, sem duplicar os dados de frações reutilizados entre capítulos.", ""]
    previous = None
    for q in questions:
        if q["study_id"] != previous:
            previous = q["study_id"]
            lines += [f"## Estudo {previous}", ""]
        lines += [f"- **{LABELS[q['component']]} · {LABELS.get(q['mmat_criterion'], q['mmat_criterion'])}** — {q['question_pt']}",
                  f"  Fonte: {q['source_id']}; {q['evidence_locator']}. Encaminhamento previsto: {q['intended_recipient']}.",
                  f"  Cobertura: **{COVERAGE_LABELS[q['coverage_status']]}**. {q['coverage_notes']} Registro público: `{q['coverage_reference']}`.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    REPORT.write_text(render_markdown(load_questions()), encoding="utf-8")
