import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const currentPath = path.join(root, 'research', 'data', 'mmat_reassessment_current.csv');
const registryPath = path.join(root, 'research', 'data', 'mmat_current_study_registry.csv');
const outputPath = path.join(root, 'research', 'exports', 'analysis', 'mmat_current.html');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    const next = text[index + 1];
    if (character === '"' && quoted && next === '"') {
      field += '"';
      index += 1;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (character === ',' && !quoted) {
      row.push(field);
      field = '';
    } else if ((character === '\n' || character === '\r') && !quoted) {
      if (character === '\r' && next === '\n') index += 1;
      row.push(field);
      if (row.some((value) => value.length > 0)) rows.push(row);
      row = [];
      field = '';
    } else {
      field += character;
    }
  }
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }
  const [header, ...data] = rows;
  return data.map((values) => Object.fromEntries(header.map((key, index) => [key, values[index] ?? ''])));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function criterion(value) {
  const normalized = value.toLowerCase();
  const className = normalized === 'y' ? 'criterion-y' : normalized === 'n' ? 'criterion-n' : 'criterion-ct';
  return `<span class="criterion ${className}" title="${escapeHtml(value)}">${escapeHtml(value)}</span>`;
}

function sourceStatus(row) {
  if (row.assessment_basis === 'primary_full_text_reviewed_externally') return '<span class="tag tag-green">texto primário revisado</span>';
  if (row.empirical_status === 'protocol_or_proposal_not_applicable') return '<span class="tag tag-red">protocolo contextual</span>';
  return '<span class="tag tag-amber">abstract/metadados</span>';
}

const current = parseCsv(fs.readFileSync(currentPath, 'utf8'));
const registry = parseCsv(fs.readFileSync(registryPath, 'utf8'));
const registryById = new Map(registry.map((row) => [row.study_id, row]));
const latestSnapshot = current.map((row) => row.snapshot_date).sort().at(-1);
const latestSnapshotLabel = latestSnapshot.split('-').reverse().join('/');
const empirical = current.filter((row) => row.empirical_status !== 'protocol_or_proposal_not_applicable');
const primaryReviewed = current.filter((row) => row.assessment_basis === 'primary_full_text_reviewed_externally');
const abstractOnly = current.filter((row) => row.assessment_basis === 'abstract_and_metadata_only');

const rows = current.map((row) => {
  const study = registryById.get(row.study_id) ?? {};
  const title = study.title || row.study_key;
  const type = row.empirical_status === 'protocol_or_proposal_not_applicable' ? 'fora da síntese empírica' : row.design || 'design não informado';
  return `<tr>
    <td>${escapeHtml(row.study_id)}</td>
    <td><span class="study-title">${escapeHtml(title)}</span><span class="study-meta">${escapeHtml(row.study_key)} · ${escapeHtml(type)}</span></td>
    <td>${sourceStatus(row)}</td>
    <td>${criterion(row.s1)}</td><td>${criterion(row.s2)}</td>
    <td>${criterion(row.q1)}</td><td>${criterion(row.q2)}</td><td>${criterion(row.q3)}</td><td>${criterion(row.q4)}</td><td>${criterion(row.q5)}</td>
  </tr>`;
}).join('\n');

const page = `<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Apreciação preliminar por critérios do MMAT 2018 para o snapshot vigente do CCW.">
  <title>MMAT atual · CCW</title>
  <link rel="stylesheet" href="../../../public-site/assets/site.css">
</head>
<body>
  <header class="site-header">
    <div class="site-shell site-header-inner">
      <a class="site-brand" href="../../../" aria-label="CCW — voltar à visão geral">
        <img src="../../../public-site/assets/ifc-campus-videira-horizontal.png" alt="Instituto Federal Catarinense — Campus Videira">
        <span class="site-brand-copy"><strong>CCW</strong><small>Pesquisa versionada<br>Ciência da Computação</small></span>
      </a>
      <nav class="site-nav site-nav-desktop" aria-label="Navegação principal">
        <a href="../../../">Visão geral</a>
        <a href="../../index.html">Revisão sistemática</a>
        <a href="./mmat_current.html" aria-current="page">MMAT atual</a>
        <a href="../../../presentation/">Apresentação</a>
        <a href="../../../results/ptc/index.html">PTC</a>
        <a href="../../../results/tcc/index.html">TCC</a>
        <a href="https://github.com/thalesfb/ccw" target="_blank" rel="noopener">Repositório</a>
      </nav>
      <details class="site-menu">
        <summary class="site-menu-toggle" aria-label="Menu principal" aria-controls="site-primary-nav">Menu</summary>
        <nav id="site-primary-nav" class="site-nav site-nav-mobile" aria-label="Navegação principal">
          <a href="../../../">Visão geral</a>
          <a href="../../index.html">Revisão sistemática</a>
          <a href="./mmat_current.html" aria-current="page">MMAT atual</a>
          <a href="../../../presentation/">Apresentação</a>
          <a href="../../../results/ptc/index.html">PTC</a>
          <a href="../../../results/tcc/index.html">TCC</a>
          <a href="https://github.com/thalesfb/ccw" target="_blank" rel="noopener">Repositório</a>
        </nav>
      </details>
    </div>
  </header>

  <main>
    <div class="site-shell">
      <p class="breadcrumb"><a href="../../../">Visão geral</a> / <a href="../../index.html">Revisão</a> / <strong>MMAT atual</strong></p>
      <section class="page-hero" aria-labelledby="page-title">
        <span class="eyebrow">MMAT 2018 · snapshot vigente de ${latestSnapshotLabel}</span>
        <h1 id="page-title">Apreciação preliminar por critérios</h1>
        <p class="lede">A leitura atual registra evidências e limites para cada critério. Ela não é uma nota global, um percentual ou um ranking de qualidade.</p>
        <div class="action-row">
          <a class="btn btn-primary" href="../../index.html">Voltar à revisão</a>
          <a class="btn btn-secondary" href="mmat_visualization.html">Visualização histórica — 17 estudos</a>
        </div>
      </section>

      <section class="section" aria-labelledby="summary-title">
        <div class="section-heading">
          <h2 id="summary-title">O que este ledger representa</h2>
          <p>O ledger atual contém ${current.length} registros. Os valores abaixo são contagens do registro atual e não devem ser interpretados como escore de qualidade.</p>
        </div>
        <div class="data-strip">
          <div class="metric-card"><span class="metric-value">${current.length}</span><span class="metric-label">registros no ledger</span></div>
          <div class="metric-card"><span class="metric-value">${empirical.length}</span><span class="metric-label">candidatos empíricos</span></div>
          <div class="metric-card"><span class="metric-value">1</span><span class="metric-label">protocolo contextual</span></div>
          <div class="metric-card"><span class="metric-value">${primaryReviewed.length}</span><span class="metric-label">textos primários revisados</span></div>
          <div class="metric-card"><span class="metric-value">${abstractOnly.length}</span><span class="metric-label">abstracts/metadados</span></div>
        </div>
      </section>

      <section class="section split-grid" aria-label="Método e limites do MMAT">
        <article class="surface-card">
          <span class="eyebrow">Leitura metodológica</span>
          <h3>Critérios, não uma nota</h3>
          <p>O ledger preserva S1 e S2 como perguntas de triagem e Q1–Q5 como critérios de apreciação. Cada célula usa <strong>Y</strong> (sim), <strong>N</strong> (não) ou <strong>CT</strong> (não é possível concluir com a fonte disponível).</p>
        </article>
        <article class="surface-card">
          <span class="eyebrow">Status da evidência</span>
          <h3>${primaryReviewed.length} textos revisados externamente</h3>
          <p>${abstractOnly.length} registros ainda dependem de fonte primária ou têm somente abstract/metadados disponíveis. A revisão foi registrada por um único revisor e a adjudicação metodológica final permanece pendente.</p>
        </article>
      </section>

      <section class="section" aria-labelledby="table-title">
        <div class="section-heading">
          <h2 id="table-title">Ledger atual</h2>
          <p>Registro por estudo, origem da apreciação e critérios MMAT aplicáveis.</p>
        </div>
        <div class="table-wrap">
          <table class="mmat-table">
            <caption>Legenda: Y = sim · N = não · CT = não é possível concluir com a evidência disponível.</caption>
            <thead><tr><th>ID</th><th>Registro</th><th>Fonte disponível</th><th>S1</th><th>S2</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>Q5</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </section>

      <section class="section" aria-labelledby="pending-title">
        <div class="callout callout-amber notice">
          <span class="notice-mark" aria-hidden="true">!</span>
          <div>
            <h3 id="pending-title">Pendências antes da consolidação</h3>
            <p>Recuperar fontes primárias restantes, registrar localizadores para os julgamentos e concluir a adjudicação com a orientação. O protocolo 6921 continua fora da síntese empírica.</p>
          </div>
        </div>
      </section>

      <section class="section surface-card">
        <span class="eyebrow">Proveniência</span>
        <h3>Fontes versionadas</h3>
        <p><a href="../../../data/mmat_reassessment_current.csv">CSV do ledger atual</a> · <a href="../../../data/mmat_current_study_registry.csv">registro dos estudos</a> · <a href="../reports/reproducibility_manifest.json">manifesto de reprodutibilidade</a> · <a href="https://github.com/thalesfb/ccw" target="_blank" rel="noopener">repositório no GitHub</a></p>
        <p class="source-note">A página foi gerada a partir de <code>research/data/mmat_reassessment_current.csv</code> e <code>research/data/mmat_current_study_registry.csv</code>.</p>
      </section>
    </div>
  </main>

  <footer class="site-footer">
    <div class="site-shell site-footer-inner">
      <p><strong>MMAT atual · CCW</strong><br>Apreciação preliminar por critérios</p>
      <p><a href="../../index.html">Revisão</a> · <a href="../../../">Visão geral</a> · <a href="https://github.com/thalesfb/ccw" target="_blank" rel="noopener">Repositório</a></p>
    </div>
  </footer>
</body>
</html>`;

fs.writeFileSync(outputPath, page, 'utf8');
console.log(`generated ${path.relative(root, outputPath)} from ${current.length} current MMAT records`);
