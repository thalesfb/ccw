"""Generate an accessible standalone HTML report for teacher review."""

from __future__ import annotations

import hashlib
import html
import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_PROFILE_COLUMNS = {
    "student_id",
    "skill_id",
    "evidence_count",
    "predicted_probability",
    "prediction_std",
    "observed_accuracy",
    "observed_accuracy_lower",
    "observed_accuracy_upper",
    "evidence_status",
    "level",
    "threshold_version",
    "interpretation_limit",
}
REQUIRED_IMPORTANCE_COLUMNS = {
    "feature",
    "importance_mean",
    "importance_std",
}


def _pseudonym(student_id: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}:{student_id}".encode("utf-8")).hexdigest()
    return f"Estudante-{digest[:8].upper()}"


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if hasattr(value, "item"):
        return _json_safe(value.item())
    return value


def _embedded_json(payload: dict[str, Any]) -> str:
    serialized = json.dumps(
        _json_safe(payload),
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )
    return (
        serialized.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def build_teacher_report(
    *,
    profiles: pd.DataFrame,
    metrics: dict[str, Any],
    importance: pd.DataFrame,
    output_path: Path,
    pseudonym_salt: str,
    dataset_label: str,
    model_version: str,
) -> Path:
    """Write a self-contained HTML report without exposing raw student IDs."""

    missing_profiles = sorted(REQUIRED_PROFILE_COLUMNS.difference(profiles.columns))
    if missing_profiles:
        raise ValueError("missing profile columns: " + ", ".join(missing_profiles))
    missing_importance = sorted(
        REQUIRED_IMPORTANCE_COLUMNS.difference(importance.columns)
    )
    if missing_importance:
        raise ValueError(
            "missing importance columns: " + ", ".join(missing_importance)
        )
    if not pseudonym_salt:
        raise ValueError("pseudonym_salt must not be empty")

    pseudonyms = {
        str(student_id): _pseudonym(str(student_id), pseudonym_salt)
        for student_id in profiles["student_id"].astype(str).unique()
    }
    profile_records = json.loads(
        profiles.where(pd.notna(profiles), None).to_json(
            orient="records", force_ascii=False
        )
    )
    for record in profile_records:
        raw_id = str(record.pop("student_id"))
        record["student"] = pseudonyms[raw_id]

    importance_records = json.loads(
        importance.where(pd.notna(importance), None).to_json(
            orient="records", force_ascii=False
        )
    )
    payload = {
        "profiles": profile_records,
        "importance": importance_records,
        "metrics": metrics,
        "students": sorted(pseudonyms.values()),
        "metadata": {
            "dataset_label": dataset_label,
            "model_version": model_version,
        },
    }
    data_json = _embedded_json(payload)
    dataset_text = html.escape(dataset_label)
    version_text = html.escape(model_version)
    student_count = len(pseudonyms)
    skill_count = profiles["skill_id"].nunique()
    insufficient_count = int(
        (profiles["evidence_status"] == "insufficient_evidence").sum()
    )

    document = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Perfil por habilidade — protótipo do TCC</title>
  <style>
    :root {{ color-scheme: light; --ink:#172033; --muted:#586174; --line:#d8dde8; --surface:#fff; --soft:#f4f6fa; --accent:#244a8f; --warning:#7a3e00; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:system-ui,-apple-system,"Segoe UI",sans-serif; color:var(--ink); background:var(--soft); line-height:1.5; }}
    header, main, footer {{ width:min(1180px, calc(100% - 32px)); margin-inline:auto; }}
    header {{ padding:32px 0 18px; }}
    h1 {{ margin:0 0 8px; font-size:clamp(1.8rem,4vw,2.7rem); }}
    h2 {{ margin-top:0; }}
    .subtitle, .meta {{ color:var(--muted); }}
    .warning {{ background:#fff5e8; border-left:5px solid #b35a00; padding:16px; margin:18px 0; color:var(--warning); }}
    .grid {{ display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); margin:18px 0; }}
    .card {{ background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:18px; box-shadow:0 2px 8px rgb(20 33 61 / 6%); }}
    .metric {{ font-size:1.7rem; font-weight:700; margin-top:6px; }}
    label {{ display:block; font-weight:650; margin-bottom:6px; }}
    select, button, textarea {{ font:inherit; }}
    select {{ width:min(100%,420px); padding:10px 12px; border:1px solid var(--line); border-radius:8px; background:#fff; }}
    button {{ border:0; border-radius:8px; padding:10px 14px; background:var(--accent); color:white; cursor:pointer; font-weight:650; }}
    button:focus-visible, select:focus-visible, textarea:focus-visible {{ outline:3px solid #8db4ff; outline-offset:2px; }}
    .toolbar {{ display:flex; flex-wrap:wrap; align-items:end; gap:12px; margin-bottom:16px; }}
    .table-wrap {{ overflow:auto; border:1px solid var(--line); border-radius:10px; }}
    table {{ width:100%; border-collapse:collapse; background:#fff; }}
    th, td {{ text-align:left; padding:11px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
    th {{ background:#eef2f8; position:sticky; top:0; }}
    .badge {{ display:inline-block; padding:3px 8px; border-radius:999px; background:#e9eef8; font-size:.85rem; }}
    .badge.insufficient {{ background:#fff1d6; color:#6d4300; }}
    .muted {{ color:var(--muted); }}
    textarea {{ width:100%; min-height:100px; border:1px solid var(--line); border-radius:8px; padding:10px; }}
    footer {{ padding:24px 0 40px; color:var(--muted); font-size:.9rem; }}
    @media print {{ button, .no-print {{ display:none !important; }} body {{ background:#fff; }} .card {{ box-shadow:none; }} }}
  </style>
</head>
<body>
<header>
  <h1>Perfil por habilidade</h1>
  <p class="subtitle">Protótipo de apoio à interpretação docente</p>
  <p class="meta"><strong>Base:</strong> {dataset_text} · <strong>Versão do modelo:</strong> {version_text}</p>
  <div class="warning" role="alert"><strong>Atenção:</strong> este perfil reúne evidências observadas e estimativas computacionais. Ele não constitui diagnóstico definitivo de competência, aprendizagem ou dificuldade e deve ser interpretado por um professor.</div>
</header>
<main>
  <section aria-labelledby="resumo-title">
    <h2 id="resumo-title">Resumo do artefato</h2>
    <div class="grid">
      <article class="card"><span class="muted">Estudantes pseudonimizados</span><div class="metric">{student_count}</div></article>
      <article class="card"><span class="muted">Habilidades representadas</span><div class="metric">{skill_count}</div></article>
      <article class="card"><span class="muted">Perfis com evidência insuficiente</span><div class="metric">{insufficient_count}</div></article>
      <article class="card"><span class="muted">Estratégia de divisão</span><div class="metric" id="split-strategy">—</div></article>
    </div>
  </section>

  <section class="card" aria-labelledby="student-title">
    <h2 id="student-title">Análise individual</h2>
    <div class="toolbar no-print">
      <div>
        <label for="student-select">Estudante</label>
        <select id="student-select" aria-label="Selecionar estudante"></select>
      </div>
      <button id="export-button" type="button">Exportar perfil selecionado</button>
      <button type="button" onclick="window.print()">Imprimir</button>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Habilidade</th><th>Probabilidade estimada</th><th>Evidências</th><th>Desempenho observado</th><th>Estado</th><th>Nível</th></tr></thead>
        <tbody id="profile-body"></tbody>
      </table>
    </div>
    <p class="muted">O intervalo exibido refere-se à proporção observada; não é um intervalo de confiança completo da previsão do modelo.</p>
    <label for="teacher-notes">Notas de revisão docente</label>
    <textarea id="teacher-notes" placeholder="Registre contexto, discordâncias, novas evidências ou decisões. As notas permanecem somente neste navegador e não são enviadas pelo relatório."></textarea>
  </section>

  <section class="card" aria-labelledby="models-title">
    <h2 id="models-title">Comparação técnica dos modelos</h2>
    <div class="table-wrap"><table><thead><tr><th>Modelo</th><th>Log-loss</th><th>Brier Score</th><th>ROC-AUC</th><th>Calibração</th></tr></thead><tbody id="models-body"></tbody></table></div>
    <p class="muted">As métricas descrevem desempenho preditivo no conjunto de teste e não comprovam eficácia pedagógica.</p>
  </section>

  <section class="card" aria-labelledby="importance-title">
    <h2 id="importance-title">Dependência preditiva global</h2>
    <div class="table-wrap"><table><thead><tr><th>Variável</th><th>Importância média</th><th>Desvio</th></tr></thead><tbody id="importance-body"></tbody></table></div>
    <p class="muted">A importância por permutação não estabelece relação causal e pode ser afetada por variáveis correlacionadas.</p>
  </section>
</main>
<footer>Relatório autônomo: nenhum dado é enviado a serviços externos. Identificadores são pseudonimizados para esta exportação.</footer>
<script id="report-data" type="application/json">{data_json}</script>
<script>
  const DATA = JSON.parse(document.getElementById('report-data').textContent);
  const fmt = value => value === null || value === undefined ? '—' : Number(value).toLocaleString('pt-BR', {{maximumFractionDigits:3}});
  const pct = value => value === null || value === undefined ? '—' : (Number(value) * 100).toLocaleString('pt-BR', {{maximumFractionDigits:1}}) + '%';
  const statusLabel = value => value === 'insufficient_evidence' ? 'Evidência insuficiente' : 'Estimativa disponível';
  const levelLabel = value => ({{high_fragility:'Fragilidade elevada',monitoring:'Acompanhamento',developing:'Em desenvolvimento',probable_mastery:'Domínio provável'}}[value] || 'Não ativado');
  const select = document.getElementById('student-select');
  DATA.students.forEach(student => {{ const option=document.createElement('option'); option.value=student; option.textContent=student; select.appendChild(option); }});
  document.getElementById('split-strategy').textContent = DATA.metrics.split_strategy || 'não informado';

  function renderProfiles() {{
    const rows = DATA.profiles.filter(row => row.student === select.value);
    const body = document.getElementById('profile-body'); body.textContent='';
    rows.forEach(row => {{
      const tr=document.createElement('tr');
      const interval = pct(row.observed_accuracy_lower) + ' – ' + pct(row.observed_accuracy_upper);
      const statusClass = row.evidence_status === 'insufficient_evidence' ? 'badge insufficient' : 'badge';
      [row.skill_id, pct(row.predicted_probability), String(row.evidence_count), pct(row.observed_accuracy) + ' (' + interval + ')'].forEach(value => {{ const td=document.createElement('td'); td.textContent=value; tr.appendChild(td); }});
      const status=document.createElement('td'); status.innerHTML='<span class="'+statusClass+'"></span>'; status.firstChild.textContent=statusLabel(row.evidence_status); tr.appendChild(status);
      const level=document.createElement('td'); level.textContent=levelLabel(row.level); tr.appendChild(level);
      body.appendChild(tr);
    }});
  }}

  function renderModels() {{
    const body=document.getElementById('models-body'); body.textContent='';
    Object.entries(DATA.metrics.models || {{}}).forEach(([name, values]) => {{
      const tr=document.createElement('tr');
      [name, fmt(values.log_loss), fmt(values.brier_score), fmt(values.roc_auc), fmt(values.expected_calibration_error)].forEach(value => {{ const td=document.createElement('td'); td.textContent=value; tr.appendChild(td); }});
      body.appendChild(tr);
    }});
  }}

  function renderImportance() {{
    const body=document.getElementById('importance-body'); body.textContent='';
    DATA.importance.forEach(row => {{ const tr=document.createElement('tr'); [row.feature, fmt(row.importance_mean), fmt(row.importance_std)].forEach(value => {{ const td=document.createElement('td'); td.textContent=value; tr.appendChild(td); }}); body.appendChild(tr); }});
  }}

  function exportSelected() {{
    const rows=DATA.profiles.filter(row => row.student === select.value);
    const headers=['student','skill_id','predicted_probability','evidence_count','observed_accuracy','observed_accuracy_lower','observed_accuracy_upper','evidence_status','level','threshold_version'];
    const quote=value => '"' + String(value ?? '').replaceAll('"','""') + '"';
    const csv=[headers.join(','), ...rows.map(row => headers.map(header => quote(row[header])).join(','))].join('\n');
    const link=document.createElement('a'); link.href=URL.createObjectURL(new Blob([csv],{{type:'text/csv;charset=utf-8'}})); link.download=select.value+'-perfil.csv'; link.click(); URL.revokeObjectURL(link.href);
  }}

  select.addEventListener('change', renderProfiles);
  document.getElementById('export-button').addEventListener('click', exportSelected);
  renderProfiles(); renderModels(); renderImportance();
</script>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
    return output_path
