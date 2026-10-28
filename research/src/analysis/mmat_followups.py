"""Trace unresolved MMAT decisions to prepared, unsent clarification questions."""
from __future__ import annotations

import csv
from pathlib import Path

from .mmat_current import load_current_reassessment, load_component_reassessments

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "research/data/mmat_followup_questions_current.csv"
REPORT = ROOT / "docs/tcc/MMAT-PERGUNTAS-PENDENTES.md"
HOLDS = {("5", "design"), ("7", "design"), ("14", "design"),
         ("8", "unit"), ("3", "access"), ("6919", "access"), ("6923", "access")}
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
             "São 55 critérios indeterminados (37 no registro principal e 18 nos componentes mistos), três decisões de delineamento, uma de unidade de apreciação e três de acesso ao texto: 62 perguntas. A lista não substitui a conferência humana de todos os julgamentos, inclusive Y e N. Não é escore de qualidade.", "",
             "As dúvidas de categoria e unidade exigem adjudicação com a orientação do TCC. As demais foram redigidas para eventual esclarecimento dos autores; destinatários e encaminhamento ainda precisam ser definidos pelo responsável. Nenhum contato externo foi realizado nesta revisão.", "",
             "As fontes 3 e 6919 não foram revalidadas nesta rodada. As perguntas correspondentes derivam dos registros anteriores e exigem recuperação do original antes de qualquer alteração. Simulação pode constituir pesquisa empírica; no estudo 8, a pendência é a unidade/categoria, não a simples presença de simulações.", ""]
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
