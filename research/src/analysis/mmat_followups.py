"""Trace unresolved MMAT decisions to prepared, unsent clarification questions."""
from __future__ import annotations

import csv
from pathlib import Path

from .mmat_current import load_current_reassessment, load_component_reassessments

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "research/data/mmat_followup_questions_current.csv"
REPORT = ROOT / "docs/tcc/MMAT-PERGUNTAS-PENDENTES.md"
HOLDS = {("3", "access"), ("6919", "access"), ("6923", "access")}
LABELS = {"study": "critérios principais", "record": "pendência do registro",
          "qualitative": "componente qualitativo", "quantitative": "componente quantitativo",
          "unit": "unidade de apreciação", "design": "delineamento", "access": "acesso ao texto"}


def load_questions():
    with DATA.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def validate_questions(questions):
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


def render_markdown(questions):
    validate_questions(questions)
    lines = ["# Perguntas pendentes para completar a apreciação MMAT", "",
             "Revisão documental de 28/10/2026. Perguntas preparadas, não enviadas. Não há respostas de autores registradas neste documento.", "",
             "São 72 critérios indeterminados (54 no registro principal e 18 nos componentes mistos) e três pendências de acesso ao texto: 75 perguntas. A lista não substitui a conferência humana de todos os julgamentos, inclusive Y e N. Não é escore de qualidade.", "",
             "CT é uma conclusão de insuficiência de informação, não uma tarefa necessariamente incompleta. A consolidação não exige eliminar todos os CT ou obter resposta a todas as perguntas. As tarefas efetivas, seus responsáveis, evidências e próximos passos estão em `research/data/mmat_consolidation_actions_current.json` e na seção de consolidação da página MMAT. As correções documentais desta rodada não alteraram respostas por inferência.", "",
             "As rotas de apreciação dos estudos 5, 7, 8 e 14 foram decididas operacionalmente nesta revisão, com limitações explícitas. Alocação e demais lacunas não foram resolvidas por inferência. As perguntas foram redigidas para eventual esclarecimento dos autores; destinatários e encaminhamento ainda precisam ser definidos pelo responsável. Nenhum contato externo foi realizado nesta revisão.", "",
             "As fontes 3 e 6919 não foram revalidadas nesta rodada. As perguntas correspondentes derivam dos registros anteriores e exigem recuperação do original antes de alterar seus julgamentos. Para 6923, a consulta oficial de 28/10/2026 confirmou o embargo até 16/05/2027; o texto integral não foi recuperado e não há apreciação MMAT. Simulação pode constituir pesquisa empírica; no estudo 8, a unidade agora é uma tese/um relatório com componentes matemáticos, sem duplicar os dados de frações reutilizados entre capítulos.", ""]
    previous = None
    for q in questions:
        if q["study_id"] != previous:
            previous = q["study_id"]
            lines += [f"## Estudo {previous}", ""]
        lines += [f"- **{LABELS[q['component']]} · {LABELS.get(q['mmat_criterion'], q['mmat_criterion'])}** — {q['question_pt']}",
                  f"  Fonte: {q['source_id']}; {q['evidence_locator']}. Encaminhamento previsto: {q['intended_recipient']}.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    REPORT.write_text(render_markdown(load_questions()), encoding="utf-8")
