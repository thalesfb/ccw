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
  const response = normalized === 'y' ? 'Sim' : normalized === 'n' ? 'Não' : 'Não é possível determinar';
  return `<span class="criterion ${className}" title="Resposta: ${escapeHtml(response)}" aria-label="Resposta: ${escapeHtml(response)}">${escapeHtml(value)}</span>`;
}

function sourceStatus(row) {
  if (row.assessment_basis === 'primary_full_text_reviewed_externally') return '<span class="tag tag-green">texto primário revisado</span>';
  if (row.empirical_status === 'protocol_or_proposal_not_applicable') return '<span class="tag tag-red">protocolo contextual</span>';
  return '<span class="tag tag-amber">abstract/metadados</span>';
}

const MMAT_SCREENING_QUESTIONS = [
  {
    code: 'S1',
    label: 'Há perguntas de pesquisa claras?',
    original: 'Are there clear research questions?',
  },
  {
    code: 'S2',
    label: 'Os dados coletados permitem responder às perguntas de pesquisa?',
    original: 'Do the collected data allow to address the research questions?',
  },
];

const MMAT_CRITERIA_GROUPS = [
  {
    label: 'Estudos qualitativos',
    questions: [
      ['Q1', 'A abordagem qualitativa é apropriada para responder à pergunta de pesquisa?', 'Is the qualitative approach appropriate to answer the research question?'],
      ['Q2', 'Os métodos de coleta de dados qualitativos são adequados para abordar a pergunta de pesquisa?', 'Are the qualitative data collection methods adequate to address the research question?'],
      ['Q3', 'Os achados são adequadamente derivados dos dados?', 'Are the findings adequately derived from the data?'],
      ['Q4', 'A interpretação dos resultados é suficientemente fundamentada nos dados?', 'Is the interpretation of results sufficiently substantiated by data?'],
      ['Q5', 'Há coerência entre fontes de dados qualitativos, coleta, análise e interpretação?', 'Is there coherence between qualitative data sources, collection, analysis and interpretation?'],
    ],
  },
  {
    label: 'Estudos quantitativos randomizados',
    questions: [
      ['Q1', 'A randomização foi realizada de forma adequada?', 'Is randomization appropriately performed?'],
      ['Q2', 'Os grupos são comparáveis no início do estudo?', 'Are the groups comparable at baseline?'],
      ['Q3', 'Os dados de desfecho estão completos?', 'Are there complete outcome data?'],
      ['Q4', 'Os avaliadores dos desfechos estavam cegos para a intervenção recebida?', 'Are outcome assessors blinded to the intervention provided?'],
      ['Q5', 'Os participantes aderiram à intervenção designada?', 'Did the participants adhere to the assigned intervention?'],
    ],
  },
  {
    label: 'Estudos quantitativos não randomizados',
    questions: [
      ['Q1', 'Os participantes são representativos da população-alvo?', 'Are the participants representative of the target population?'],
      ['Q2', 'As medições são apropriadas tanto para o desfecho quanto para a intervenção?', 'Are measurements appropriate regarding both the outcome and intervention?'],
      ['Q3', 'Os dados de desfecho estão completos?', 'Are there complete outcome data?'],
      ['Q4', 'Os fatores de confusão foram considerados no delineamento e na análise?', 'Are the confounders accounted for in the design and analysis?'],
      ['Q5', 'A intervenção ou exposição ocorreu conforme planejado?', 'Did the intervention or exposure occur as intended?'],
    ],
  },
  {
    label: 'Estudos quantitativos descritivos',
    questions: [
      ['Q1', 'A estratégia de amostragem é pertinente à pergunta de pesquisa?', 'Is the sampling strategy relevant to address the research question?'],
      ['Q2', 'A amostra é representativa da população-alvo?', 'Is the sample representative of the target population?'],
      ['Q3', 'As medições são apropriadas?', 'Are the measurements appropriate?'],
      ['Q4', 'O risco de viés de não resposta é baixo?', 'Is the risk of nonresponse bias low?'],
      ['Q5', 'A análise estatística é apropriada para responder à pergunta de pesquisa?', 'Is the statistical analysis appropriate to answer the research question?'],
    ],
  },
  {
    label: 'Estudos de métodos mistos',
    questions: [
      ['Q1', 'Há justificativa adequada para usar um delineamento de métodos mistos?', 'Is there an adequate rationale for using a mixed methods design?'],
      ['Q2', 'Os diferentes componentes do estudo foram efetivamente integrados?', 'Are the different components of the study effectively integrated?'],
      ['Q3', 'Os resultados da integração foram interpretados adequadamente?', 'Are the outputs of the integration adequately interpreted?'],
      ['Q4', 'As divergências entre os resultados quantitativos e qualitativos foram abordadas?', 'Are divergences between quantitative and qualitative results addressed?'],
      ['Q5', 'Os componentes atendem aos critérios de qualidade de cada tradição?', 'Do the components adhere to the quality criteria of each tradition?'],
    ],
  },
];

function screeningQuestionCard(question) {
  return `<article class="surface-card mmat-question-card">
    <span class="question-code">${escapeHtml(question.code)}</span>
    <h3>${escapeHtml(question.label)}</h3>
    <p class="question-original" lang="en">${escapeHtml(question.original)}</p>
  </article>`;
}

function criteriaGroup(group) {
  const questions = group.questions.map(([code, label, original]) => `<li class="mmat-question-item">
      <span class="question-code">${escapeHtml(code)}</span>
      <div><strong>${escapeHtml(label)}</strong><span class="question-original" lang="en">${escapeHtml(original)}</span></div>
    </li>`).join('');
  return `<details class="mmat-question-group" open>
    <summary>${escapeHtml(group.label)} <span>Q1–Q5</span></summary>
    <ol class="mmat-question-list">${questions}</ol>
  </details>`;
}

const screeningQuestions = MMAT_SCREENING_QUESTIONS.map(screeningQuestionCard).join('');
const criteriaGroups = MMAT_CRITERIA_GROUPS.map(criteriaGroup).join('');

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

      <section class="section" aria-labelledby="questions-title">
        <div class="section-heading">
          <h2 id="questions-title">Perguntas de triagem do MMAT 2018</h2>
          <p>Estas duas perguntas são aplicadas a todos os estudos antes da apreciação específica do delineamento.</p>
        </div>
        <div class="mmat-screening-grid">${screeningQuestions}</div>
        <div class="callout callout-blue mmat-question-note">
          <div><strong>Como interpretar S1 e S2.</strong> Se a resposta for N ou CT em uma ou nas duas perguntas, a apreciação adicional pode não ser viável ou apropriada. Isso não é uma nota: é uma condição de leitura e transparência metodológica.</div>
        </div>
      </section>

      <section class="section" aria-labelledby="criteria-title">
        <div class="section-heading">
          <h2 id="criteria-title">Critérios de apreciação por delineamento</h2>
          <p>Os códigos Q1–Q5 mudam de formulação conforme o delineamento identificado para o estudo.</p>
        </div>
        <div class="mmat-criteria-groups">${criteriaGroups}</div>
      </section>

      <section class="section" aria-labelledby="table-title">
        <div class="section-heading">
          <h2 id="table-title">Ledger atual</h2>
          <p>Registro por estudo, origem da apreciação e critérios MMAT aplicáveis.</p>
        </div>
        <div class="table-wrap">
          <table class="mmat-table">
            <caption>Legenda: Y = sim · N = não · CT = não é possível concluir com a evidência disponível.</caption>
            <thead><tr><th scope="col">ID</th><th scope="col">Registro</th><th scope="col">Fonte disponível</th><th scope="col" title="Pergunta de triagem S1">S1</th><th scope="col" title="Pergunta de triagem S2">S2</th><th scope="col" title="Critério específico do delineamento">Q1</th><th scope="col" title="Critério específico do delineamento">Q2</th><th scope="col" title="Critério específico do delineamento">Q3</th><th scope="col" title="Critério específico do delineamento">Q4</th><th scope="col" title="Critério específico do delineamento">Q5</th></tr></thead>
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
        <p class="source-note">As perguntas seguem o <a href="https://doi.org/10.3233/EFI-180221" target="_blank" rel="noopener">MMAT 2018</a>; a tradução em português é acompanhada pela formulação original em inglês para manter a rastreabilidade do instrumento.</p>
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
