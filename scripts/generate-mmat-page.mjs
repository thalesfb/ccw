import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const currentPath = path.join(root, 'research', 'data', 'mmat_reassessment_current.csv');
const componentPath = path.join(root, 'research', 'data', 'mmat_component_reassessment_current.csv');
const registryPath = path.join(root, 'research', 'data', 'mmat_current_study_registry.csv');
const scopePath = path.join(root, 'research', 'data', 'current_synthesis_scope.csv');
const reproducibilityManifestPath = path.join(root, 'research', 'exports', 'reports', 'reproducibility_manifest.json');
const outputPath = path.join(root, 'research', 'exports', 'analysis', 'mmat_current.html');
const sourceCoverage = JSON.parse(fs.readFileSync(path.join(root, 'research', 'data', 'study_contribution_current.json'), 'utf8'));
const coverageById = new Map(sourceCoverage.records.map((row) => [row.study_id, row]));

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
  const answer = String(value ?? '').trim();
  if (!answer) {
    return '<span class="criterion criterion-pending" title="Não avaliado" aria-label="Não avaliado">—</span>';
  }
  const normalized = answer.toLowerCase();
  const className = normalized === 'y' ? 'criterion-y' : normalized === 'n' ? 'criterion-n' : normalized === 'n/a' ? 'criterion-na' : 'criterion-ct';
  const response = normalized === 'y' ? 'Sim' : normalized === 'n' ? 'Não' : normalized === 'n/a' ? 'Não se aplica' : 'Não é possível determinar';
  return `<span class="criterion ${className}" title="Resposta: ${escapeHtml(response)}" aria-label="Resposta: ${escapeHtml(response)}">${escapeHtml(answer)}</span>`;
}

function sourceStatus(row, scope) {
  if (row.assessment_basis === 'primary_full_text_scope_exclusion') return '<span class="tag tag-amber">texto integral conferido; fora do escopo matemático</span>';
  if (coverageById.get(row.study_id)?.current_appraisal_verification === 'not_revalidated_without_primary_text') return '<span class="tag tag-amber">MMAT histórico; fonte indisponível nesta revisão</span>';
  if (scope?.empirical_mmat_applicability === 'pending_unit_adjudication') return '<span class="tag tag-amber">MMAT suspenso; unidade de análise pendente</span>';
  if (row.design === 'design_pending' && row.s1) return '<span class="tag tag-amber">texto primário revisado; categoria MMAT pendente</span>';
  if (row.assessment_basis === 'primary_full_text_reviewed_externally') return '<span class="tag tag-green">texto primário revisado</span>';
  if (row.empirical_status === 'protocol_or_proposal_not_applicable') return '<span class="tag tag-red">protocolo contextual</span>';
  if (row.assessment_basis === 'pending_full_text_not_appraised') return '<span class="tag tag-amber">texto integral pendente; MMAT não aplicado</span>';
  if (row.assessment_basis === 'abstract_and_metadata_only') return '<span class="tag tag-amber">excluído após resumo; MMAT não aplicado</span>';
  return '<span class="tag tag-amber">resumo/metadados</span>';
}

function sourceAndAppraisalStatus(row, scope) {
  if (row.assessment_basis === 'primary_full_text_scope_exclusion') {
    return 'Texto integral conferido após a exclusão originalmente registrada na triagem do resumo. Confirmado fora do escopo matemático; MMAT não aplicado. A recuperação suplementar não altera as contagens históricas.';
  }
  if (coverageById.get(row.study_id)?.current_appraisal_verification === 'not_revalidated_without_primary_text') {
    return 'Respostas históricas provisórias, não revalidadas nesta revisão por falta do texto integral. A indisponibilidade de acesso não demonstra baixa qualidade nem confirma inelegibilidade.';
  }
  if (scope?.empirical_mmat_applicability === 'pending_unit_adjudication') {
    return 'Texto integral consultado; MMAT suspenso. Elegibilidade e unidade de apreciação aguardam adjudicação humana; nenhum critério recebeu resposta.';
  }
  if (row.assessment_basis === 'pending_full_text_not_appraised') {
    return 'Texto integral pendente; nenhum critério MMAT foi aplicado.';
  }
  if (row.assessment_basis === 'abstract_and_metadata_only') {
    return 'Registro excluído após resumo; MMAT não aplicado.';
  }
  if (row.empirical_status === 'protocol_or_proposal_not_applicable') {
    return 'Protocolo sem resultados empíricos concluídos; MMAT não aplicável.';
  }
  if (row.assessment_basis === 'primary_full_text_reviewed_externally') {
    if (row.design === 'design_pending') return 'Texto integral consultado; S1/S2 respondidas. Q1–Q5 não avaliados enquanto a categoria MMAT aguarda adjudicação; células vazias não significam CT.';
    return 'Texto integral consultado; apreciação MMAT preliminar.';
  }
  return 'Situação da fonte ou apreciação requer confirmação.';
}

function parseCriterionEvidence(value = '') {
  return new Map(value.split(';').flatMap((entry) => {
    const separator = entry.indexOf('=');
    if (separator < 1) return [];
    const rationale = entry.slice(separator + 1).trim().replace(/^(?:Y|N|CT)\s+/i, '');
    return [[entry.slice(0, separator).trim().toUpperCase(), rationale]];
  }));
}

function formatDate(value) {
  return value ? value.split('-').reverse().join('/') : 'não registrada';
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
    design: 'qualitative',
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
    design: 'quantitative_randomized',
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
    design: 'quantitative_nonrandomized',
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
    design: 'quantitative_descriptive',
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
    design: 'mixed_methods',
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
const criterionQuestionsByDesign = new Map(MMAT_CRITERIA_GROUPS.map((group) => [
  group.design,
  new Map(group.questions.map(([code, label]) => [code, label])),
]));

const current = parseCsv(fs.readFileSync(currentPath, 'utf8'));
const componentReassessments = parseCsv(fs.readFileSync(componentPath, 'utf8'));
const registry = parseCsv(fs.readFileSync(registryPath, 'utf8'));
const currentScope = parseCsv(fs.readFileSync(scopePath, 'utf8'));
const reproducibilityManifest = JSON.parse(fs.readFileSync(reproducibilityManifestPath, 'utf8'));
const registryById = new Map(registry.map((row) => [row.study_id, row]));
const scopeById = new Map(currentScope.map((row) => [row.study_id, row]));
const searchCutoffLabel = formatDate(reproducibilityManifest.protocol.cutoff_date);
const adjudicatedSnapshotLabel = formatDate(reproducibilityManifest.snapshot_date);
const latestScopeReconciliation = currentScope.map((row) => row.snapshot_date).sort().at(-1);
const latestScopeReconciliationLabel = formatDate(latestScopeReconciliation);
const latestReviewDate = current.map((row) => row.review_date).filter(Boolean).sort().at(-1);
const latestReviewDateLabel = formatDate(latestReviewDate);
const primaryReviewed = current.filter((row) => row.assessment_basis === 'primary_full_text_reviewed_externally');
const empiricalCore = currentScope.filter((row) => row.record_status === 'included_empirical_core');
const mmatAppraisedIds = new Set(currentScope
  .filter((row) => row.empirical_mmat_applicability === 'applicable')
  .map((row) => row.study_id));
const unitHoldRows = currentScope.filter((row) => row.empirical_mmat_applicability === 'pending_unit_adjudication');
const mmatAppraised = current.filter((row) => mmatAppraisedIds.has(row.study_id));
const categoryPending = mmatAppraised.filter((row) => row.design === 'design_pending');
const categoryAppraised = mmatAppraised.filter((row) => row.design !== 'design_pending');
const abstractOnly = currentScope.filter((row) => row.selection_stage === 'abstract_screening' && row.selection_status === 'excluded');
const fullTextScopeChecks = current.filter((row) => row.assessment_basis === 'primary_full_text_scope_exclusion');
const localPrimaryCount = sourceCoverage.records.filter((row) => row.full_text_available_locally).length;
const pendingFullText = current.filter((row) => row.assessment_basis === 'pending_full_text_not_appraised');
const abstractExclusionSummary = abstractOnly.length === 1
  ? 'Um registro foi excluído após a triagem do resumo e não recebeu MMAT.'
  : `${abstractOnly.length} registros foram excluídos após a triagem do resumo e não receberam MMAT.`;
const pendingFullTextSummary = pendingFullText.length === 1
  ? 'Um relatório permanece não recuperado no fluxo de seleção e não recebeu apreciação MMAT.'
  : `${pendingFullText.length} relatórios permanecem não recuperados no fluxo de seleção e não receberam apreciação MMAT.`;
const pendingFullTextLabel = pendingFullText.length === 1
  ? 'relatório não recuperado no fluxo'
  : 'relatórios não recuperados no fluxo';
const pendingFullTextQuestionSummary = pendingFullText.length === 1
  ? '1 registro aguarda texto integral e também não recebe MMAT.'
  : `${pendingFullText.length} registros aguardam texto integral e também não recebem MMAT.`;
const mixedMethodsStudies = current.filter((row) => row.design === 'mixed_methods');
const componentDesignLabels = {
  qualitative: 'Qualitativo',
  quantitative_nonrandomized: 'Quantitativo não randomizado',
  quantitative_descriptive: 'Quantitativo descritivo',
};
const componentCriterionPrefixes = {
  qualitative: '1',
  quantitative_nonrandomized: '3',
  quantitative_descriptive: '4',
};
function componentAppraisalDetails(studyId) {
  const assessments = componentReassessments.filter((row) => row.study_id === studyId);
  if (!assessments.length) return '';
  const rows = assessments.map((assessment) => {
    const prefix = componentCriterionPrefixes[assessment.design];
    const criteria = ['c1', 'c2', 'c3', 'c4', 'c5'].map((criterionKey, index) => {
      const code = `${prefix}.${index + 1}`;
      return `<li class="mmat-evidence-item"><div class="mmat-evidence-heading"><span class="question-code">${code}</span><strong>${escapeHtml(assessment[criterionKey])}</strong>${criterion(assessment[criterionKey])}</div><p>${escapeHtml(assessment[`evidence_${criterionKey}`])}</p></li>`;
    }).join('');
    return `<tr><th scope="row">${escapeHtml(componentDesignLabels[assessment.design])}</th><td colspan="2"><ul class="mmat-evidence-grid">${criteria}</ul><p class="source-note"><strong>Fonte:</strong> ${escapeHtml(assessment.source_id)}; <strong>localizador:</strong> ${escapeHtml(assessment.source_locator)}.</p></td></tr>`;
  }).join('');
  return `<section class="component-assessment" aria-label="Avaliação dos componentes do estudo ${escapeHtml(studyId)}"><h4>Avaliação dos componentes (provisória)</h4><p>Além dos critérios mistos exibidos na linha principal, o MMAT requer apreciação dos componentes qualitativo e quantitativo com categorias apropriadas. Estes julgamentos são de revisor único e aguardam adjudicação independente.</p><table class="mmat-table"><thead><tr><th scope="col">Categoria</th><th scope="col">Critérios, justificativas e fonte</th></tr></thead><tbody>${rows}</tbody></table></section>`;
}
const mixedMethodsNote = mixedMethodsStudies.length
  ? `<section class="section" aria-labelledby="mixed-methods-limit-title">
        <div class="callout callout-blue">
          <h2 id="mixed-methods-limit-title">Limite da apreciação de métodos mistos</h2>
          <p>O guia MMAT recomenda avaliar os componentes qualitativo e quantitativo com as categorias adequadas, além dos critérios da categoria de métodos mistos. Para os registros ${mixedMethodsStudies.map((row) => escapeHtml(row.study_id)).join(', ')}, este recorte apresenta Q1–Q5 da categoria mista e, em cada ficha, uma apreciação preliminar separada dos componentes. Como há um único revisor e a adjudicação independente continua pendente, essas avaliações ainda não são finais; isso não constitui uma avaliação negativa dos estudos.</p>
          <p><a href="https://mixedmethodsappraisaltoolpublic.pbworks.com/w/page/71030694/FAQ" target="_blank" rel="noopener">Orientação dos desenvolvedores do MMAT sobre estudos de métodos mistos</a></p>
        </div>
      </section>`
  : '';

function criterionEvidenceDetails(row, scope) {
  const evidence = parseCriterionEvidence(row.criterion_evidence);
  const designQuestions = criterionQuestionsByDesign.get(row.design);
  const missingEvidence = scope?.empirical_mmat_applicability === 'pending_unit_adjudication'
    ? 'MMAT suspenso: elegibilidade e unidade de apreciação ainda aguardam adjudicação humana; nenhum critério foi avaliado.'
    : row.assessment_basis === 'pending_full_text_not_appraised'
    ? 'Texto integral não recuperado; MMAT não aplicado.'
    : row.assessment_basis === 'primary_full_text_scope_exclusion'
      ? 'Exclusão por escopo matemático confirmada no texto integral; MMAT não aplicado.'
    : row.assessment_basis === 'abstract_and_metadata_only'
      ? 'Registro excluído após a triagem do resumo; MMAT não aplicado.'
      : 'Justificativa não consta no registro disponível.';
  const allQuestions = [
    ...MMAT_SCREENING_QUESTIONS.map(({ code, label }) => ({ code, label })),
    ...['Q1', 'Q2', 'Q3', 'Q4', 'Q5'].map((code) => ({
      code,
      label: row.empirical_status === 'protocol_or_proposal_not_applicable'
        ? 'Não aplicável: protocolo contextual sem resultados empíricos concluídos.'
        : row.assessment_basis === 'primary_full_text_scope_exclusion'
          ? 'Não aplicável neste recorte: exclusão por escopo matemático.'
        : designQuestions?.get(code) ?? 'Pergunta específica não determinada porque o delineamento permanece pendente.',
    })),
  ];
  const items = allQuestions.map(({ code, label }) => `<li class="mmat-evidence-item">
      <div class="mmat-evidence-heading"><span class="question-code">${escapeHtml(code)}</span><strong>${escapeHtml(label)}</strong>${criterion(row[code.toLowerCase()])}</div>
      <p>${escapeHtml(evidence.get(code) || (row.design === 'design_pending' && row.s1 && code.startsWith('Q') ? 'Critério não avaliado: a categoria MMAT ainda não foi definida. Não se trata de resposta CT.' : missingEvidence))}</p>
    </li>`).join('');
  const source = row.source_id ? `<code>${escapeHtml(row.source_id)}</code>` : 'não identificada';
  const locator = row.page_or_section ? escapeHtml(row.page_or_section) : 'não registrado';
  const appraisalNote = row.notes && scope?.empirical_mmat_applicability !== 'pending_unit_adjudication'
    ? `<p class="source-note"><strong>Nota de leitura:</strong> ${escapeHtml(row.notes)}</p>`
    : '';
  const scopeNote = scope?.empirical_mmat_applicability === 'pending_unit_adjudication'
    ? `<p class="source-note"><strong>Decisão provisória de escopo:</strong> ${escapeHtml(scope.disposition_note)}</p>`
    : '';
  return `<tr class="mmat-evidence-row">
    <td colspan="10">
      <details class="mmat-evidence">
        <summary>Ver perguntas, justificativas e localização da evidência</summary>
        <ul class="mmat-evidence-grid">${items}</ul>
        <p class="source-note"><strong>Situação da fonte e da apreciação:</strong> ${escapeHtml(sourceAndAppraisalStatus(row, scope))} <strong>ID da fonte:</strong> ${source} (consulte o manifesto de fontes primárias); <strong>seções/páginas registradas:</strong> ${locator}; <strong>data da apreciação:</strong> ${escapeHtml(formatDate(row.review_date))}.</p>
        ${appraisalNote}
        ${scopeNote}
        ${componentAppraisalDetails(row.study_id)}
      </details>
    </td>
  </tr>`;
}

const rows = current.map((row) => {
  const study = registryById.get(row.study_id) ?? {};
  const scope = scopeById.get(row.study_id) ?? {};
  const unitPending = scope.empirical_mmat_applicability === 'pending_unit_adjudication';
  const title = study.title || row.study_key;
  const type = row.empirical_status === 'protocol_or_proposal_not_applicable'
    ? 'fora da síntese empírica'
    : row.study_id === '6915'
      ? `${row.design} · componente escolar`
      : row.design || 'design não informado';
  return `<tr>
    <td>${escapeHtml(row.study_id)}</td>
    <td><span class="study-title">${escapeHtml(title)}</span><span class="study-meta">${escapeHtml(row.study_key)} · ${escapeHtml(type)}</span></td>
    <td>${sourceStatus(row, scope)}</td>
    <td>${criterion(unitPending ? '' : row.s1)}</td><td>${criterion(unitPending ? '' : row.s2)}</td>
    <td>${criterion(unitPending ? '' : row.q1)}</td><td>${criterion(unitPending ? '' : row.q2)}</td><td>${criterion(unitPending ? '' : row.q3)}</td><td>${criterion(unitPending ? '' : row.q4)}</td><td>${criterion(unitPending ? '' : row.q5)}</td>
  </tr>${criterionEvidenceDetails(row, scope)}`;
}).join('\n');

const page = `<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Apreciação preliminar por critérios do MMAT 2018, com data do corpus, justificativas e localizadores.">
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
        <span class="eyebrow">MMAT 2018 · apreciação preliminar</span>
        <h1 id="page-title">Apreciação preliminar por critérios</h1>
        <p class="lede">A leitura atual registra evidências e limites para cada critério. Ela não é uma nota global, um percentual ou um ranking de qualidade.</p>
        <p class="source-note">Data de corte da busca: ${searchCutoffLabel}. Recorte consolidado em ${adjudicatedSnapshotLabel}. Escopo MMAT atual reconciliado em ${latestScopeReconciliationLabel}; apreciações registradas até ${latestReviewDateLabel}.</p>
        <div class="action-row">
          <a class="btn btn-primary" href="../../index.html">Voltar à revisão</a>
          <a class="btn btn-secondary" href="mmat_visualization.html">Visualização histórica — 17 estudos</a>
        </div>
      </section>

      <section class="section" aria-labelledby="summary-title">
        <div class="section-heading">
          <h2 id="summary-title">O que esta avaliação registra</h2>
          <p>O registro de apreciação reúne ${current.length} itens, entre estudos empíricos e registros com exclusão ou pendências documentais. As contagens abaixo descrevem o escopo atual e não devem ser interpretadas como escore de qualidade.</p>
        </div>
        <div class="data-strip">
          <div class="metric-card"><span class="metric-value">${current.length}</span><span class="metric-label">itens no registro de apreciação</span></div>
          <div class="metric-card"><span class="metric-value">${empiricalCore.length}</span><span class="metric-label">estudos empíricos mantidos provisoriamente</span></div>
          <div class="metric-card"><span class="metric-value">1</span><span class="metric-label">protocolo contextual</span></div>
          <div class="metric-card"><span class="metric-value">${primaryReviewed.length}</span><span class="metric-label">consultas documentais declaradas</span></div>
          <div class="metric-card"><span class="metric-value">${mmatAppraised.length}</span><span class="metric-label">registros com triagem MMAT (S1/S2)</span></div>
          <div class="metric-card"><span class="metric-value">${categoryAppraised.length}</span><span class="metric-label">estudos com critérios por categoria apreciados</span></div>
          <div class="metric-card"><span class="metric-value">${pendingFullText.length}</span><span class="metric-label">${pendingFullTextLabel}</span></div>
        </div>
      </section>

      <section class="section split-grid" aria-label="Método e limites do MMAT">
        <article class="surface-card">
          <span class="eyebrow">Leitura metodológica</span>
          <h3>Critérios, não uma nota</h3>
          <p>O registro de apreciação preserva S1 e S2 como perguntas de triagem e Q1–Q5 como critérios de apreciação. As células usam <strong>Y</strong> (sim), <strong>N</strong> (não), <strong>CT</strong> (não é possível concluir) e <strong>N/A</strong> (não aplicável ao protocolo contextual).</p>
        </article>
        <article class="surface-card">
          <span class="eyebrow">Status da evidência</span>
          <h3>${primaryReviewed.length} registros com consulta documental declarada</h3>
          <p>A reprodução congelada do índice textual abrange 12 fontes. As consultas suplementares e o OCR não ampliam automaticamente esse conjunto reproduzido; ele não deve ser confundido com a disponibilidade atual dos PDFs.</p>
          <p>O acervo local contém ${localPrimaryCount} PDFs dos 18 registros. Faltam os estudos 3 e 6923: o estudo 3 permanece retido provisoriamente, mas sua ficha histórica não foi revalidada sem o original; 6923 é o relatório não recuperado no fluxo. Disponibilidade local não é elegibilidade nem certificação de leitura humana. ${fullTextScopeChecks.length ? 'A conferência suplementar do texto integral do estudo 9 confirmou a exclusão por escopo matemático registrada após o resumo.' : ''}</p>
          <p>Dos ${empiricalCore.length} registros empíricos incluídos provisoriamente, ${mmatAppraised.length} têm S1/S2 respondidas; ${categoryAppraised.length} têm apreciação preliminar dos critérios da categoria. Em ${categoryPending.length} estudos (${categoryPending.map((row) => escapeHtml(row.study_id)).join(', ')}), Q1–Q5 permanecem não avaliados até definir o delineamento, sem resposta CT. ${unitHoldRows.length} registro (${unitHoldRows.map((row) => escapeHtml(row.study_id)).join(', ')}) permanece no corpus e no fluxo PRISMA sem respostas MMAT enquanto se adjudicam elegibilidade e unidade de análise; não se somam suas bases distintas. ${pendingFullTextSummary} ${abstractExclusionSummary} O protocolo 6921 não integra o corpus empírico. Os julgamentos documentais receberam apoio automatizado; o rótulo histórico de revisor único não comprova leitura humana integral. A conferência humana por fonte e critério e a adjudicação metodológica permanecem pendentes.</p>
        </article>
      </section>

      ${mixedMethodsNote}

      <section class="section" aria-labelledby="questions-title">
        <div class="section-heading">
          <h2 id="questions-title">Perguntas de triagem do MMAT 2018</h2>
          <p>No recorte atual, S1 e S2 estão preenchidas para ${mmatAppraised.length} estudos empíricos. Q1–Q5 foram apreciados em ${categoryAppraised.length}; ${categoryPending.length} aguardam definição da categoria. ${unitHoldRows.length} registro com texto consultado está temporariamente sem respostas enquanto se define a unidade de apreciação; ${pendingFullTextQuestionSummary} ${abstractExclusionSummary} O protocolo 6921 não apresenta resultados concluídos e não integra o corpus empírico.</p>
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
          <h2 id="table-title">Apreciação por estudo</h2>
          <p>Registro por estudo, origem da apreciação e critérios MMAT aplicáveis.</p>
        </div>
        <div class="table-wrap">
          <table class="mmat-table">
            <caption>Legenda: Y = sim · N = não · CT = não é possível concluir com a evidência disponível · N/A = não aplicável · — = não avaliado. Nos estudos 5, 7 e 14, apenas S1/S2 foram respondidas; Q1–Q5 aguardam definição da categoria. O relatório 6923 e o estudo 8 (unidade de análise pendente) não receberam respostas MMAT. O estudo 9 está fora do escopo matemático, sem MMAT. As respostas históricas do estudo 3 não foram revalidadas nesta revisão sem o original.</caption>
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
            <p>Completar os localizadores por critério, recuperar o relatório pendente no fluxo (${pendingFullText.length}), revalidar as demais fontes ainda não examináveis nesta auditoria e adjudicar a elegibilidade e unidade de análise do estudo 8. As consultas históricas declaradas não certificam leitura humana; a matriz de cobertura distingue acesso e leitura efetivamente registrados. O protocolo 6921 continua fora da síntese empírica.</p>
          </div>
        </div>
      </section>

      <section class="section surface-card">
        <span class="eyebrow">Proveniência</span>
        <h3>Fontes versionadas</h3>
        <p><a href="../../../research/data/mmat_reassessment_current.csv">Arquivo CSV da apreciação atual</a> · <a href="../../../research/data/mmat_component_reassessment_current.csv">CSV da apreciação por componentes</a> · <a href="../../../research/data/mmat_current_study_registry.csv">registro dos estudos</a> · <a href="../../../research/data/mmat_primary_sources_manifest.csv">manifesto de fontes primárias</a> · <a href="../reports/reproducibility_manifest.json">manifesto de reprodutibilidade</a> · <a href="https://github.com/thalesfb/ccw" target="_blank" rel="noopener">repositório no GitHub</a></p>
        <p><a href="../../../research/data/study_contribution_current.json">Matriz de cobertura das fontes e contribuição dos 18 registros</a></p>
        <p class="source-note">A página foi gerada a partir dos dados versionados da apreciação MMAT e do registro dos estudos. A matriz complementar informa páginas, limites da leitura documental e conferência humana pendente, sem distribuir os textos primários.</p>
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

const normalizedPage = page.replace(/^[\t ]+$/gm, '');
fs.writeFileSync(outputPath, normalizedPage, 'utf8');
console.log(`generated ${path.relative(root, outputPath)} from ${current.length} current MMAT records`);
