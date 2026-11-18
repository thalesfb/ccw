import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8');

const expectedPages = [
  'index.html',
  'research/index.html',
  'research/exports/analysis/mmat_current.html',
  'research/exports/analysis/mmat_visualization.html',
  'research/exports/reports/summary_report.html',
  'research/exports/reports/papers_report_included.html',
  'research/exports/reports/gap_analysis.html',
  'results/ptc/index.html',
  'results/tcc/index.html',
];

for (const page of expectedPages) {
  const html = read(page);
  assert.match(html, /<link rel="icon"[^>]*site-favicon\.svg/i, `${page} must link the shared site favicon`);
  assert.match(html, /public-site\/assets\/site\.css/, `${page} must use the shared site stylesheet`);
  assert.match(html, /site-nav/, `${page} must expose the shared navigation`);
  assert.match(html, /site-nav-desktop/, `${page} must expose the desktop navigation variant`);
  assert.match(html, /class="site-menu"/, `${page} must expose the responsive disclosure menu`);
  assert.match(html, /site-nav-mobile/, `${page} must expose the mobile navigation variant`);
  assert.match(html, /aria-controls="site-primary-nav"/, `${page} must associate the menu toggle with its navigation`);
  assert.match(html, /Revisão sistemática/i, `${page} must link to the research area`);
  assert.match(html, /<a href="[^"]*mmat_current\.html"[^>]*>MMAT(?: reconciliado)?<\/a>/i, `${page} must provide a concise MMAT navigation link`);
}

const homepage = read('index.html');
assert.match(homepage, /Ver MMAT · conferido em 13\/11\/2026/i, 'the homepage must promote the current dated MMAT review');
assert.doesNotMatch(homepage, /MMAT histórico \(referência\)/i, 'the homepage must not present the historical page as current');
assert.match(homepage, /15 estudos empíricos integram a seleção histórica/i, 'the homepage must identify the 15-study selection as historical');
assert.match(homepage, /com 14 relatórios recuperados/i, 'the homepage must distinguish recovered reports from the historical selection');
assert.match(homepage, /dois não foram recuperados \(Sokkhey e Zeng\)/i, 'the homepage must disclose both reports without a verifiable copy');
assert.match(homepage, /15 foram avaliados em texto completo/i, 'the homepage must report the current full-text denominator');
assert.match(homepage, /MMAT: 14 estudos com texto recuperado conferidos pelo autor; Sokkhey mantém respostas históricas não revalidadas; componentes mistos preliminares; sem nota global/i, 'the homepage must state the reviewed MMAT scope and its limits');
assert.match(homepage, /O corte 4,0 e a seleção permanecem inalterados/i, 'the homepage must describe the unchanged selection');
assert.doesNotMatch(homepage, /população vigente|snapshot vigente/i, 'the homepage must not present the pre-amendment snapshot as current');
assert.match(homepage, /um registro foi excluído após resumo/i, 'the homepage must disclose the abstract-stage exclusion');
assert.match(homepage, /um protocolo foi excluído após essa avaliação/i, 'the homepage must disclose the full-text protocol exclusion');
assert.doesNotMatch(homepage, /revisão final com a orientação/i, 'the public homepage must not describe the advisor review state');
assert.doesNotMatch(homepage, /17 candidatos empíricos provisórios/i, 'the homepage must not classify the abstract-stage exclusion as an empirical candidate');
assert.match(homepage, /escopo reconciliado/i, 'the homepage must label the current scope status');
assert.match(homepage, /escopo reconciliado em 20\/10\/2026/i, 'the homepage must distinguish the historical scope reconciliation date');
assert.match(homepage, /ifc-campus-videira-horizontal\.png/, 'the homepage must use the official IFC mark');
assert.doesNotMatch(homepage, /linear-gradient|Segoe UI.*Tahoma/i, 'the homepage must not retain the legacy visual system');

const reportPages = [
  'research/exports/reports/summary_report.html',
  'research/exports/reports/papers_report_included.html',
  'research/exports/reports/gap_analysis.html',
];
for (const page of reportPages) {
  const html = read(page);
  assert.doesNotMatch(html, /linear-gradient|#667eea|#764ba2|font-family:\s*['"]?Segoe UI/i, `${page} must use the shared visual system`);
  assert.match(html, /Relatórios do processamento/i, `${page} must identify the report area`);
  assert.equal((html.match(/<h1\b/gi) || []).length, 1, `${page} must have a single page heading`);
}
const reportGenerator = read('research/src/analysis/reports.py');
assert.doesNotMatch(reportGenerator, /def _create_summary_html|#667eea|#764ba2|Segoe UI/i, 'the report generator must not retain its unused legacy summary renderer');

const summaryReport = read('research/exports/reports/summary_report.html');
assert.match(summaryReport, /exportação operacional/i, 'the generated summary must distinguish its export from the current scientific record');
assert.match(summaryReport, /Snapshot do export operacional: \d{2}\/\d{2}\/\d{4}/i, 'the report must identify the date as the source snapshot, not the current HTML generation date');
assert.doesNotMatch(summaryReport, /Gerado em:|Data de Geração:/i, 'the report must not present the snapshot date as the HTML generation time');
assert.match(summaryReport, /2 relatório\(s\) não recuperado\(s\), 15 avaliado\(s\) e 14 relatório\(s\) empírico\(s\) recuperado\(s\)/i, 'the generated summary must retain the reconciled retrieval counts');
assert.match(summaryReport, /11\.76%/, 'the summary must use the reconciled report-retrieval percentage');
assert.match(summaryReport, /6\.67%/, 'the summary must use the reconciled full-text exclusion percentage');
assert.match(summaryReport, /registro de escopo[\s\S]*registro de recuperação/i, 'the summary must link the versioned selection and retrieval records');
assert.match(summaryReport, /04\/12\/2026|TCC|MMAT/i, 'the generated summary must point readers to the current TCC or MMAT record');
assert.match(summaryReport, /Registros por ano de publicação/i, 'the summary charts must use reader-facing Portuguese labels');
assert.match(summaryReport, /Escores de priorização do export; não são medida de qualidade metodológica/i, 'the relevance chart must explain the limits of the score');
assert.doesNotMatch(summaryReport, /Database Coverage|Selection Funnel|Papers by Year|Relevance Distribution/i, 'the summary must not expose raw chart identifiers as reader-facing labels');

const gapReport = read('research/exports/reports/gap_analysis.html');
assert.match(gapReport, /exploração automatizada/i, 'the gap report must be labeled as an automated exploration');
assert.match(gapReport, /não avalia rigor metodológico/i, 'the gap report must not infer study rigor from operational labels');
assert.match(gapReport, /distribuição geográfica não é calculada/i, 'the gap report must not claim an uncomputed geographic result');
assert.match(gapReport, /11\.875 registros/, 'the gap report must format counts using Brazilian Portuguese conventions');
assert.match(gapReport, /Nenhum dos 11\.875 registros recebeu a etiqueta operacional “longitudinal”/, 'the gap report must describe a zero count in natural language');
assert.doesNotMatch(gapReport, /Poucos estudos experimentais rigorosos|Nenhuma lacuna significativa identificada|Recomendações para Pesquisas Futuras/i, 'the gap report must not retain unsupported conclusions or generic recommendations');

const papersReport = read('research/exports/reports/papers_report_included.html');
assert.match(papersReport, /exportação operacional/i, 'the retained-record report must identify its processing source');
assert.match(papersReport, /não equivale à seleção científica/i, 'the retained-record report must distinguish pipeline retention from scientific inclusion');

function collectHtmlFiles(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name === '.git' || entry.name === 'node_modules') return [];
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory()) return collectHtmlFiles(absolutePath);
    return entry.isFile() && entry.name.endsWith('.html') ? [absolutePath] : [];
  });
}

for (const absolutePage of collectHtmlFiles(root)) {
  const page = path.relative(root, absolutePage);
  const html = read(page);
  assert.doesNotMatch(html, /(?:href|src)=["']\s*javascript:/i, `${page} must not expose a script URL`);
  for (const [, anchor] of html.matchAll(/<a\b[^>]*>/gi)) {
    if (/\btarget=["']_blank["']/i.test(anchor)) {
      assert.match(anchor, /\brel=["'][^"']*noopener/i, `${page} must isolate links opened in a new tab`);
    }
  }
  for (const [, rawTarget] of html.matchAll(/(?:href|src)=["']([^"']+)["']/gi)) {
    const target = rawTarget.trim();
    if (!target || target.startsWith('#') || /^(?:https?:|mailto:|tel:|data:|javascript:)/i.test(target)) continue;
    const pathname = decodeURIComponent(target.split(/[?#]/, 1)[0]);
    if (!pathname) continue;
    const absoluteTarget = path.resolve(path.dirname(absolutePage), pathname);
    const relativeTarget = path.relative(root, absoluteTarget);
    assert.ok(relativeTarget === '' || (!relativeTarget.startsWith('..') && !path.isAbsolute(relativeTarget)), `${page} must not link outside the public repository: ${target}`);
    assert.ok(fs.existsSync(absoluteTarget), `${page} must not contain a broken local link: ${target}`);
  }
}

const researchLanding = read('research/index.html');
assert.match(researchLanding, /A seleção histórica sob o corte 4,0 reúne 15 estudos empíricos, com 14 relatórios recuperados/i, 'the research landing page must distinguish the historical selection from retrieved reports');
assert.match(researchLanding, /O registro de apreciação descreve a seleção histórica sob o corte 4,0: 15 estudos empíricos/i, 'the research landing page must identify the MMAT denominator as historical');
assert.match(researchLanding, /dois dos 17 relatórios procurados não foram recuperados \(Sokkhey e Zeng\)/i, 'the research landing page must disclose both reports without a verifiable copy');
assert.match(researchLanding, /O corte 4,0 permanece inalterado/i, 'the research landing page must describe the applied cutoff');
assert.doesNotMatch(researchLanding, /escopo vigente|população retida/i, 'the research landing page must not label the pre-amendment selection as current');
assert.match(researchLanding, /href="data\/current_synthesis_scope\.csv"/, 'the research landing page must link the current eligibility ledger');
assert.match(researchLanding, /um registro foi excluído após resumo/i, 'the research landing page must disclose the abstract-stage exclusion');
assert.match(researchLanding, /um protocolo foi excluído após essa avaliação/i, 'the research landing page must disclose the full-text protocol exclusion');
assert.doesNotMatch(researchLanding, /17 candidatos empíricos provisórios/i, 'the research landing page must not overstate the empirical candidate count');

const historicalMmat = read('research/exports/analysis/mmat_visualization.html');
assert.match(historicalMmat, /visualização histórica[^<]*17 registros/i, 'the legacy MMAT visualization must identify its historical 17-study denominator');
assert.match(historicalMmat, /seleção histórica sob o corte 4,0[\s\S]*15 estudos empíricos com 15 triagens S1\/S2 e 15 apreciações por categoria/i, 'the legacy MMAT visualization must label the linked appraisal counts as historical');
assert.doesNotMatch(historicalMmat, /população vigente contém 18 registros: 17 candidatos empíricos/i, 'the legacy MMAT visualization must not describe its historical denominator as current');

const siteCss = read('public-site/assets/site.css');
const responsiveSiteCss = siteCss.slice(siteCss.indexOf('@media (max-width: 1099px)'));
assert.match(responsiveSiteCss, /\.site-nav-mobile\s*\{[\s\S]*grid-template-columns:\s*minmax\(0,\s*1fr\);/, 'the mobile menu must use the full available column');
assert.match(responsiveSiteCss, /\.site-nav-mobile\s*\{[\s\S]*justify-content:\s*stretch;/, 'the mobile menu must not preserve right-only alignment');
assert.match(responsiveSiteCss, /\.site-header-inner\s*\{[^}]*position:\s*relative;/, 'the mobile navigation panel must be anchored to the full header shell');
assert.match(responsiveSiteCss, /\.site-nav-mobile\s*\{[^}]*left:\s*0;[\s\S]*right:\s*0;[\s\S]*width:\s*auto;/, 'the mobile navigation panel must use the available header width');
const mobileNavLinkStyles = responsiveSiteCss.match(/\.site-nav-mobile a\s*\{([^}]*)\}/)?.[1] ?? '';
assert.match(mobileNavLinkStyles, /width:\s*100%;/, 'mobile navigation links must fill the panel');
assert.match(mobileNavLinkStyles, /justify-content:\s*flex-start;/, 'mobile navigation link text must align from the left edge');
assert.match(mobileNavLinkStyles, /text-align:\s*left;/, 'mobile navigation labels must be left aligned');

const prototype = read('results/tcc/conteudo/prototipo.tex').replace(/\s+/g, ' ');
const functionalRequirements = prototype
  .split('\\section{Princípios e Requisitos}', 2)[1]
  ?.split('\\section{Arquitetura de Referência}', 2)[0];
assert.ok(functionalRequirements, 'the consolidated principles and requirements section must exist');
assert.doesNotMatch(functionalRequirements, /\\begin\{enumerate\}|\\item\s/, 'the consolidated requirements must be continuous academic prose');
assert.match(functionalRequirements, /No plano funcional, a futura implementação deverá importar dados documentados e relacionados a objetivos curriculares/i, 'the consolidated section must preserve the data-import requirement');
assert.match(functionalRequirements, /A revisão humana deverá permanecer integrada ao uso das recomendações/i, 'the consolidated section must preserve human review');
assert.match(functionalRequirements, /deverá exportar dados, parâmetros e resultados para auditoria/i, 'the consolidated section must preserve audit export');

const mmat = read('research/exports/analysis/mmat_current.html');
assert.doesNotMatch(mmat, /^[\t ]+$/m, 'generated MMAT page must not contain whitespace-only lines');
assert.match(mmat, /não é uma nota global/i, 'the MMAT page must reject aggregate scoring');
assert.match(mmat, /arquivo histórico/i, 'the current page must preserve historical provenance');
assert.match(mmat, /<title>MMAT · critérios Q1–Q5 por categoria · escopo histórico 20\/10\/2026 · CCW<\/title>/, 'the MMAT browser title must identify the criteria and historical scope');
assert.match(mmat, /<h1 id="page-title">Apreciação MMAT do recorte histórico: triagem S1\/S2 e critérios Q1–Q5<\/h1>/, 'the MMAT page heading must identify screening and category-specific criteria');
assert.match(mmat, /O corte 4,0 e os 15 estudos permanecem inalterados/i, 'the MMAT page must describe the actual selection without a promised new review');
assert.match(mmat, /data de corte 31\/08\/2026/i, 'the MMAT page must identify the review cutoff date');
assert.match(mmat, /recorte histórico reconciliado em 20\/10\/2026/i, 'the MMAT page must distinguish the historical reconciled scope date');
assert.match(mmat, /<span class="metric-value">18<\/span><span class="metric-label">itens no registro de apreciação<\/span>/, 'the MMAT page must explain its current 18-record population');
assert.match(mmat, /arquivo legado preserva 17 registros MMAT.*registro histórico contém 18 itens.*15 estudos empíricos na seleção histórica sob o corte 4,0/i, 'the MMAT page must distinguish the legacy artifact from the historical 18-item appraisal register');
assert.match(mmat, /current_synthesis_scope\.csv/i, 'the MMAT page must identify the source of its reconciled population');
assert.match(mmat, /reproducibility_manifest\.json/i, 'the MMAT page must identify the source of its cutoff date');
assert.match(historicalMmat, /17 registros[\s\S]*15 estudos empíricos com 15 triagens S1\/S2/i, 'the historical MMAT page must identify the linked appraisal set as historical');
assert.match(historicalMmat, /descreve a seleção histórica sob o corte 4,0: 15 estudos empíricos com 15 triagens S1\/S2 e 15 apreciações por categoria/i, 'the archived MMAT page must distinguish its earlier records from the adopted selection');
assert.doesNotMatch(historicalMmat, /reaplicação da emenda|emenda ainda não foi reaplicada/i, 'the archived MMAT page must not claim an approved amendment');
assert.match(mmat, /18 registros/i, 'the current page must expose the current denominator');
assert.match(mmat, /arquivo histórico/i, 'the current page must preserve historical provenance');
assert.match(mmat, /O registro de apreciação reúne 18 itens da seleção histórica sob o corte 4,0/i, 'the MMAT page must describe its 18-item scope as historical');
assert.doesNotMatch(mmat, /estudos empíricos mantidos provisoriamente/i, 'the MMAT page must not describe the pre-amendment selection as provisional/current');
assert.equal((mmat.match(/class="study-title"/g) || []).length, 18, 'the current page must render every current MMAT record');
assert.match(mmat, /<span class="metric-value">14<\/span><span class="metric-label">fichas com consulta histórica declarada<\/span>/, 'historical consultation labels must not certify completed human reading');
assert.match(mmat, /<span class="metric-value">14<\/span><span class="metric-label">registros com triagem MMAT \(S1\/S2\)<\/span>/, 'the current page must distinguish screening records from empirical inclusion');
assert.match(mmat, /<span class="metric-value">2<\/span><span class="metric-label">relatórios sem cópia verificável na recuperação atual<\/span>/, 'the current page must show both reports without verifiable copies');
assert.match(mmat, /Dois relatórios não têm cópia verificável: Sokkhey permanece na seleção original; suas respostas MMAT históricas não foram revalidadas por falta de cópia verificável\. Zeng não recebeu MMAT e não integra os 15 estudos históricos\./, 'the current page must distinguish historical Sokkhey responses from the unrecovered Zeng report');
assert.doesNotMatch(mmat, /Sokkhey[^.]*sem apreciação MMAT|Sokkhey[^.]*não recebeu respostas MMAT/i, 'the current page must not erase Sokkhey historical responses');
assert.match(mmat, /Zeng \(1 registro\) aguarda texto integral e não recebe MMAT\./, 'the no-MMAT statement must refer to Zeng rather than Sokkhey');
assert.match(mmat, /o acervo local contém 16 PDFs dos 18 registros, identificados por hash\. Faltam os estudos 3 e 6923/, 'the current page must identify both unavailable primary PDFs');
assert.match(mmat, /A reprodução congelada do índice textual abrange 12 fontes/, 'current PDF availability must not imply a larger retrieval replay');
const historicalUnverifiedRow = mmat.match(/<tr>\s*<td>3<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.match(historicalUnverifiedRow, /MMAT histórico; fonte indisponível nesta revisão/, 'historical responses must not imply source-bound revalidation');
assert.doesNotMatch(mmat, /abstracts?\/metadados/i, 'the current page should use Portuguese for source-availability labels');
const zengRow = mmat.match(/<tr>\s*<td>6923<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(zengRow, 'study 6923 must be present in the current MMAT table');
assert.match(zengRow, /texto integral pendente; MMAT não aplicado/, 'study 6923 must be held without MMAT appraisal until its primary text is retrieved');
assert.equal([...zengRow.matchAll(/aria-label="Não avaliado"/g)].length, 7, 'pending study 6923 must leave S1, S2 and Q1–Q5 unappraised');
assert.doesNotMatch(zengRow, /aria-label="Resposta:/, 'pending study 6923 must not expose MMAT responses');
const abstractExcludedRow = mmat.match(/<tr>\s*<td>9<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(abstractExcludedRow, 'the abstract-stage exclusion must remain visible in the 18-record ledger');
assert.match(abstractExcludedRow, /texto integral conferido; fora do escopo matemático/, 'supplementary full-text recovery must be distinguished from an MMAT appraisal');
assert.equal([...abstractExcludedRow.matchAll(/aria-label="Não avaliado"/g)].length, 7, 'the abstract-stage exclusion must leave all MMAT responses unappraised');
const unitHoldRow = mmat.match(/<tr>\s*<td>8<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(unitHoldRow, 'study 8 must remain visible in the current 18-record ledger');
assert.match(unitHoldRow, /Categoria 4 adaptada/, 'the thesis must expose an adapted route rather than a confirmed descriptive design');
assert.equal([...unitHoldRow.matchAll(/aria-label="Resposta:/g)].length, 7, 'the thesis route must have screening and five criterion responses');
assert.match(mmat, /Frações são reutilizadas/, 'the thesis must disclose reused fractions');
const echeveriaRow = mmat.match(/<tr>\s*<td>6920<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(echeveriaRow, 'study 6920 must be present in the current MMAT table');
const echeveriaRatings = [...echeveriaRow.matchAll(/aria-label="Resposta: ([^"]+)"/g)].map((match) => match[1]);
assert.equal(echeveriaRatings[4], 'Não', 'mixed-methods Q3 must reflect the unmeasured performance claim in the integrated interpretation');
assert.equal(echeveriaRatings[5], 'Sim', 'mixed-methods Q4 must apply the manual rule when no quantitative/qualitative divergence is reported');
const universityRow = mmat.match(/<tr>\s*<td>6919<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(universityRow, 'mixed-methods study 6919 must be present in the current MMAT table');
const universityRatings = [...universityRow.matchAll(/aria-label="Resposta: ([^"]+)"/g)].map((match) => match[1]);
assert.equal(universityRatings[4], 'Não', 'study 6919 must retain its negative appraisal of integrated interpretation');
assert.equal(universityRatings[5], 'Sim', 'study 6919 interviews corroborate the negative result and do not report quantitative/qualitative divergence');
const protocolRow = mmat.match(/<tr>\s*<td>6921<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(protocolRow, 'contextual protocol 6921 must be present in the current MMAT table');
assert.doesNotMatch(protocolRow, />CT</, 'a protocol must not be presented as an indeterminate empirical MMAT appraisal');
assert.doesNotMatch(protocolRow, /aria-label="Resposta:/, 'a non-empirical protocol must not receive empirical criterion answers');
assert.equal([...protocolRow.matchAll(/aria-label="Não avaliado"/g)].length, 7, 'protocol cells must state that no empirical appraisal was undertaken');
for (const studyId of ['6916', '6919', '6920']) {
  const mixedRow = mmat.match(new RegExp(`<tr>\\s*<td>${studyId}<\\/td>[\\s\\S]*?<\\/tr>[\\s\\S]*?<tr class="mmat-evidence-row">[\\s\\S]*?<\\/tr>`))?.[0];
  assert.ok(mixedRow, `mixed-methods study ${studyId} must expose its evidence row`);
  assert.match(mixedRow, /Avaliação dos componentes/, `mixed-methods study ${studyId} must disclose component appraisals`);
  assert.match(mixedRow, /qualitativo|quantitativo/i, `mixed-methods study ${studyId} must identify component types`);
}
assert.match(mmat, /<td>6919<\/td>[\s\S]{0,1200}texto primário revisado/, 'study 6919 must be identified as externally reviewed in the current table');
assert.match(mmat, /He2025_6915 · Quantitativo não randomizado · componente escolar/, 'study 6915 must identify the classroom component and design in Portuguese');
for (const metadata of mmat.matchAll(/class="study-meta">([^<]+)</g)) {
  assert.doesNotMatch(metadata[1], /quantitative_|design_pending|mixed_methods|metadata_hold|not_applicable/, 'reader-facing classifications must not expose internal design codes');
}
assert.match(mmat, /Design2025_004 · Categoria 3 operacional · alocação desconhecida/, 'a pending category must remain explicit rather than being inferred');
const designStudyRow = mmat.match(/<tr>\s*<td>5<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(designStudyRow, 'Design2025_004 must remain in the current MMAT table');
const designScreeningAnswers = [...designStudyRow.matchAll(/class="criterion criterion-(?:y|ct|n)"[^>]*>(Y|CT|N)<\/span>/g)].map(match => match[1]);
assert.deepEqual(designScreeningAnswers.slice(0, 2), ['Y', 'CT'], 'Design2025_004 must retain S1=Y and report S2=CT');
assert.match(mmat, /Perguntas de triagem do MMAT 2018/i, 'the current page must expose the MMAT screening questions');
assert.match(mmat, /Há perguntas de pesquisa claras\?/i, 'the current page must expose S1');
assert.match(mmat, /Os dados coletados permitem responder às perguntas de pesquisa\?/i, 'the current page must expose S2');
assert.match(mmat, /Na seleção histórica sob o corte 4,0, S1 e S2 estão preenchidas para 14 estudos empíricos\. Q1–Q5 foram apreciados em 14;/i, 'the historical empirical records must expose their preliminary appraisals');
assert.match(mmat, /Are there clear research questions\?/i, 'the current page must preserve the original S1 wording');
assert.match(mmat, /Critérios Q1–Q5 por categoria de delineamento/i, 'the current page must expose design-specific criteria');
assert.match(mmat, /MMAT 2018<\/a>/i, 'the current page must cite the MMAT 2018 source');
assert.match(mmat, /href="\.\.\/\.\.\/\.\.\/research\/data\/mmat_current_study_registry\.csv"/, 'the current page must link to the versioned registry at its published path');
assert.match(mmat, /href="\.\.\/\.\.\/\.\.\/research\/data\/mmat_primary_sources_manifest\.csv"/, 'the current page must expose the primary-source provenance manifest');
assert.equal((mmat.match(/class="mmat-question-group"/g) || []).length, 5, 'the current page must expose all MMAT design groups');
assert.match(mmat, /O que esta avaliação registra/i, 'the public page must explain the purpose of the appraisal in reader-facing language');
assert.doesNotMatch(mmat, /\b(?:ledger|shortlist|snapshot)\b/i, 'the public page must avoid unexplained development jargon');
assert.match(mmat, /Data de corte da busca: 31\/08\/2026\. Recorte consolidado em 03\/09\/2026\. Registro MMAT da seleção histórica sob o corte 4,0, reconciliado em 20\/10\/2026; apreciações registradas até 07\/11\/2026\./i, 'the MMAT page must distinguish search cutoff, historical scope reconciliation and appraisal dates');
assert.doesNotMatch(mmat, /Recorte do corpus: 12\/10\/2026/i, 'the scope update date must not be presented as a new search record');
assert.match(mmat, /apreciações registradas até 07\/11\/2026/i, 'the current page must expose the latest appraisal date');
assert.match(mmat, /14 estudos com texto recuperado têm triagem e critérios da categoria conferidos/i, 'the MMAT table caption must distinguish checked responses from the full historical selection');
assert.doesNotMatch(mmat, /98 respostas|95 mantidas|3 alteradas|aprovação científica humana/i, 'the public MMAT page must not publish a change tally or imply an approval stage');
assert.equal((mmat.match(/class="mmat-evidence"/g) || []).length, 18, 'every MMAT record must expose criterion evidence details');
assert.match(mmat, /Ver perguntas, justificativas e localização da evidência/i, 'the evidence disclosure must be clearly labeled');
assert.match(mmat, /nota 95 nas categorias Medium/i, 'the current page must expose the concrete measurement ambiguity for study 2 Q3');
assert.match(mmat, /regra efetivamente usada e a adequação das demais medidas/i, 'the current page must explain why study 2 Q3 remains indeterminate');
assert.match(mmat, /67 perguntas preparadas/i, 'the page must expose the unresolved clarification agenda after the three ratified mixed-methods decisions');
const pagesWorkflow = read('.github/workflows/publish-reports.yml');
for (const asset of ['research/data/mmat_followup_questions_current.csv', 'research/data/mmat_consolidation_actions_current.json', 'docs/tcc/MMAT-PERGUNTAS-PENDENTES.md']) {
  assert.ok(pagesWorkflow.includes(`cp ${asset} _site/`), `Pages must package the linked MMAT followup asset: ${asset}`);
}
assert.match(mmat, /class="question-code">3\.1</, 'non-randomized quantitative components must use MMAT category 3');
assert.match(mmat, /Categoria 3 · quase-experimento com sorteio contraditório/, 'the quasi-experimental study must retain the allocation contradiction');
assert.match(mmat, /Protocolo sem resultados empíricos concluídos; critérios MMAT não avaliados\./, 'protocol non-applicability must be explained as record disposition, not a criterion answer');
assert.doesNotMatch(mmat, /aria-label="Resposta: Não se aplica"/, 'N/A must not masquerade as an official MMAT response');
for (const criterion of ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']) {
  assert.match(mmat, new RegExp(`>${criterion}<`), `the current page must expose ${criterion}`);
}

console.log(`site contract passed: ${expectedPages.length} public pages`);
