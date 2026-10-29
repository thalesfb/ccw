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
  'results/ptc/index.html',
  'results/tcc/index.html',
];

for (const page of expectedPages) {
  const html = read(page);
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
assert.match(homepage, /Ver MMAT · 20\/10\/2026/i, 'the homepage must promote the dated MMAT scope');
assert.doesNotMatch(homepage, /MMAT histórico \(referência\)/i, 'the homepage must not present the historical page as current');
assert.match(homepage, /15 registros empíricos mantidos provisoriamente/i, 'the homepage must report the provisional empirical inclusion count');
assert.match(homepage, /Um texto integral segue pendente/i, 'the homepage must disclose the unretrieved full text');
assert.match(homepage, /MMAT preliminar: 15 triagens S1\/S2 e 15 apreciações por categoria em 15 inclusões empíricas provisórias/i, 'the homepage must distinguish the MMAT denominator from the provisional corpus');
assert.match(homepage, /1 registro excluído após resumo/i, 'the homepage must disclose the abstract-stage exclusion');
assert.match(homepage, /1 protocolo excluído após texto completo/i, 'the homepage must disclose the protocol exclusion');
assert.doesNotMatch(homepage, /17 candidatos empíricos provisórios/i, 'the homepage must not classify the abstract-stage exclusion as an empirical candidate');
assert.match(homepage, /escopo reconciliado/i, 'the homepage must label the current scope status');
assert.match(homepage, /escopo reconciliado em 20 out\. 2026/i, 'the homepage must distinguish the current scope reconciliation date');
assert.match(homepage, /conferência suplementar do texto integral do registro 9/i, 'the homepage must distinguish supplemental confirmation from a new PRISMA exclusion');
assert.match(homepage, /ifc-campus-videira-horizontal\.png/, 'the homepage must use the official IFC mark');
assert.doesNotMatch(homepage, /linear-gradient|Segoe UI.*Tahoma/i, 'the homepage must not retain the legacy visual system');

const researchLanding = read('research/index.html');
assert.match(researchLanding, /15 estudos empíricos mantidos provisoriamente/i, 'the research landing page must report the provisional empirical inclusion count');
assert.match(researchLanding, /MMAT: 15 triagens S1\/S2 e 15 apreciações por categoria/i, 'the research landing page must distinguish the MMAT denominator from the provisional corpus');
assert.match(researchLanding, /1 texto integral pendente/i, 'the research landing page must disclose the unretrieved full text');
assert.match(researchLanding, /href="data\/current_synthesis_scope\.csv"/, 'the research landing page must link the current eligibility ledger');
assert.match(researchLanding, /1 registro excluído após resumo/i, 'the research landing page must disclose the abstract-stage exclusion');
assert.match(researchLanding, /1 protocolo excluído após texto completo/i, 'the research landing page must disclose the protocol exclusion');
assert.doesNotMatch(researchLanding, /17 candidatos empíricos provisórios/i, 'the research landing page must not overstate the empirical candidate count');

const historicalMmat = read('research/exports/analysis/mmat_visualization.html');
assert.match(historicalMmat, /visualização histórica[^<]*17 registros/i, 'the legacy MMAT visualization must identify its historical 17-study denominator');
assert.match(historicalMmat, /15 registros empíricos mantidos provisoriamente[\s\S]*15 triagens S1\/S2 e 15 apreciações por categoria/i, 'the legacy MMAT visualization must point readers to current scope and appraisal counts');
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
assert.match(functionalRequirements, /deverá permitir revisão humana das recomendações produzidas/i, 'the consolidated section must preserve human review');
assert.match(functionalRequirements, /deverá exportar dados, parâmetros e resultados para auditoria/i, 'the consolidated section must preserve audit export');

const mmat = read('research/exports/analysis/mmat_current.html');
assert.doesNotMatch(mmat, /^[\t ]+$/m, 'generated MMAT page must not contain whitespace-only lines');
assert.match(mmat, /não é uma nota global/i, 'the MMAT page must reject aggregate scoring');
assert.match(mmat, /arquivo histórico/i, 'the current page must preserve historical provenance');
assert.match(mmat, /data de corte 31\/08\/2026/i, 'the MMAT page must identify the review cutoff date');
assert.match(mmat, /escopo reconciliado em 20\/10\/2026/i, 'the MMAT page must distinguish the current reconciled scope date');
assert.match(mmat, /<span class="metric-value">18<\/span><span class="metric-label">itens no registro de apreciação<\/span>/, 'the MMAT page must explain its current 18-record population');
assert.match(mmat, /17 registros MMAT.*escopo vigente contém 18 registros.*15 estudos empíricos foram mantidos provisoriamente/i, 'the MMAT page must distinguish the historical 17-record artifact from the current 18-record disposition');
assert.match(mmat, /current_synthesis_scope\.csv/i, 'the MMAT page must identify the source of its reconciled population');
assert.match(mmat, /reproducibility_manifest\.json/i, 'the MMAT page must identify the source of its cutoff date');
assert.match(historicalMmat, /17 registros.*15 registros empíricos mantidos provisoriamente/i, 'the historical MMAT page must distinguish its archive count from the current empirical population');
assert.match(mmat, /18 registros/i, 'the current page must expose the current denominator');
assert.match(mmat, /arquivo histórico/i, 'the current page must preserve historical provenance');
assert.match(mmat, /O registro de apreciação reúne 18 itens/i, 'the current page must expose the current scope in reader-facing language');
assert.equal((mmat.match(/class="study-title"/g) || []).length, 18, 'the current page must render every current MMAT record');
assert.match(mmat, /<span class="metric-value">15<\/span><span class="metric-label">consultas documentais declaradas<\/span>/, 'historical consultation labels must not certify completed human reading');
assert.match(mmat, /<span class="metric-value">15<\/span><span class="metric-label">registros com triagem MMAT \(S1\/S2\)<\/span>/, 'the current page must distinguish screening records from empirical inclusion');
assert.match(mmat, /<span class="metric-value">1<\/span><span class="metric-label">relatório não recuperado no fluxo<\/span>/, 'the current page must distinguish historical selection from current PDF availability');
assert.match(mmat, /Um relatório permanece não recuperado no fluxo de seleção e não recebeu apreciação MMAT\. Um registro foi excluído após a triagem do resumo e não recebeu MMAT\./, 'the evidence summary must distinguish the unretrieved report from the abstract-stage exclusion');
assert.match(mmat, /O acervo local contém 16 PDFs dos 18 registros\. Faltam os estudos 3 e 6923/, 'the current page must identify both unavailable primary PDFs');
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
assert.equal(echeveriaRatings[4], 'Não é possível determinar', 'mixed-methods Q3 must not use a quantitative-component defect as evidence about interpretation of integrated outputs');
assert.equal(echeveriaRatings[5], 'Não é possível determinar', 'mixed-methods Q4 must remain indeterminate without direct evidence about divergences');
const universityRow = mmat.match(/<tr>\s*<td>6919<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(universityRow, 'mixed-methods study 6919 must be present in the current MMAT table');
const universityRatings = [...universityRow.matchAll(/aria-label="Resposta: ([^"]+)"/g)].map((match) => match[1]);
assert.equal(universityRatings[5], 'Não é possível determinar', 'study 6919 must not treat a difference between initial challenges and outcomes as evidence that quantitative/qualitative divergence was addressed');
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
assert.match(mmat, /Perguntas de triagem do MMAT 2018/i, 'the current page must expose the MMAT screening questions');
assert.match(mmat, /Há perguntas de pesquisa claras\?/i, 'the current page must expose S1');
assert.match(mmat, /Os dados coletados permitem responder às perguntas de pesquisa\?/i, 'the current page must expose S2');
assert.match(mmat, /No recorte atual, S1 e S2 estão preenchidas para 15 estudos empíricos\. Q1–Q5 foram apreciados em 15;/i, 'all current empirical records must expose preliminary appraisals');
assert.match(mmat, /Are there clear research questions\?/i, 'the current page must preserve the original S1 wording');
assert.match(mmat, /Critérios de apreciação por delineamento/i, 'the current page must expose design-specific criteria');
assert.match(mmat, /MMAT 2018<\/a>/i, 'the current page must cite the MMAT 2018 source');
assert.match(mmat, /href="\.\.\/\.\.\/\.\.\/research\/data\/mmat_current_study_registry\.csv"/, 'the current page must link to the versioned registry at its published path');
assert.match(mmat, /href="\.\.\/\.\.\/\.\.\/research\/data\/mmat_primary_sources_manifest\.csv"/, 'the current page must expose the primary-source provenance manifest');
assert.equal((mmat.match(/class="mmat-question-group"/g) || []).length, 5, 'the current page must expose all MMAT design groups');
assert.match(mmat, /O que esta avaliação registra/i, 'the public page must explain the purpose of the appraisal in reader-facing language');
assert.doesNotMatch(mmat, /\b(?:ledger|shortlist|snapshot)\b/i, 'the public page must avoid unexplained development jargon');
assert.match(mmat, /Data de corte da busca: 31\/08\/2026\. Recorte consolidado em 03\/09\/2026\. Escopo MMAT atual reconciliado em 20\/10\/2026; apreciações registradas até 28\/10\/2026\./i, 'the current page must distinguish search cutoff, adjudication and current MMAT review dates');
assert.doesNotMatch(mmat, /Recorte do corpus: 12\/10\/2026/i, 'the scope update date must not be presented as a new search record');
assert.match(mmat, /apreciações registradas até 28\/10\/2026/i, 'the current page must expose the latest appraisal date');
assert.equal((mmat.match(/class="mmat-evidence"/g) || []).length, 18, 'every MMAT record must expose criterion evidence details');
assert.match(mmat, /Ver perguntas, justificativas e localização da evidência/i, 'the evidence disclosure must be clearly labeled');
assert.match(mmat, /nota 95 nas categorias Medium/i, 'the current page must expose the concrete measurement ambiguity for study 2 Q3');
assert.match(mmat, /regra efetivamente usada e a adequação das demais medidas/i, 'the current page must explain why study 2 Q3 remains indeterminate');
assert.match(mmat, /75 perguntas preparadas/i, 'the page must expose the unresolved clarification agenda');
const pagesWorkflow = read('.github/workflows/publish-reports.yml');
for (const asset of ['research/data/mmat_followup_questions_current.csv', 'docs/tcc/MMAT-PERGUNTAS-PENDENTES.md']) {
  assert.ok(pagesWorkflow.includes(`cp ${asset} _site/`), `Pages must package the linked MMAT followup asset: ${asset}`);
}
assert.match(mmat, /class="question-code">3\.1</, 'non-randomized quantitative components must use MMAT category 3');
assert.match(mmat, /Categoria 2 declarada · alocação contraditória/, 'randomized category use must retain the allocation contradiction');
assert.match(mmat, /Protocolo sem resultados empíricos concluídos; critérios MMAT não avaliados\./, 'protocol non-applicability must be explained as record disposition, not a criterion answer');
assert.doesNotMatch(mmat, /aria-label="Resposta: Não se aplica"/, 'N/A must not masquerade as an official MMAT response');
for (const criterion of ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']) {
  assert.match(mmat, new RegExp(`>${criterion}<`), `the current page must expose ${criterion}`);
}

console.log(`site contract passed: ${expectedPages.length} public pages`);
