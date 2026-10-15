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
}

const homepage = read('index.html');
assert.match(homepage, /MMAT atual/i, 'the homepage must promote the current MMAT page');
assert.doesNotMatch(homepage, /MMAT histórico \(referência\)/i, 'the homepage must not present the historical page as current');
assert.match(homepage, /15 registros empíricos mantidos provisoriamente/i, 'the homepage must report the provisional empirical inclusion count');
assert.match(homepage, /Um texto integral segue pendente/i, 'the homepage must disclose the unretrieved full text');
assert.match(homepage, /MMAT preliminar: 14 de 15 inclusões empíricas provisórias/i, 'the homepage must distinguish the MMAT denominator from the provisional corpus');
assert.match(homepage, /1 registro excluído após resumo/i, 'the homepage must disclose the abstract-stage exclusion');
assert.match(homepage, /1 protocolo excluído após texto completo/i, 'the homepage must disclose the protocol exclusion');
assert.doesNotMatch(homepage, /17 candidatos empíricos provisórios/i, 'the homepage must not classify the abstract-stage exclusion as an empirical candidate');
assert.match(homepage, /escopo reconciliado/i, 'the homepage must label the current scope status');
assert.match(homepage, /escopo reconciliado em 14 out\. 2026/i, 'the homepage must distinguish the current scope reconciliation date');
assert.match(homepage, /ifc-campus-videira-horizontal\.png/, 'the homepage must use the official IFC mark');
assert.doesNotMatch(homepage, /linear-gradient|Segoe UI.*Tahoma/i, 'the homepage must not retain the legacy visual system');

const researchLanding = read('research/index.html');
assert.match(researchLanding, /15 estudos empíricos mantidos provisoriamente/i, 'the research landing page must report the provisional empirical inclusion count');
assert.match(researchLanding, /MMAT preliminar em 14/i, 'the research landing page must distinguish the MMAT denominator from the provisional corpus');
assert.match(researchLanding, /1 texto integral pendente/i, 'the research landing page must disclose the unretrieved full text');
assert.match(researchLanding, /href="data\/current_synthesis_scope\.csv"/, 'the research landing page must link the current eligibility ledger');
assert.match(researchLanding, /1 registro excluído após resumo/i, 'the research landing page must disclose the abstract-stage exclusion');
assert.match(researchLanding, /1 protocolo excluído após texto completo/i, 'the research landing page must disclose the protocol exclusion');
assert.doesNotMatch(researchLanding, /17 candidatos empíricos provisórios/i, 'the research landing page must not overstate the empirical candidate count');

const historicalMmat = read('research/exports/analysis/mmat_visualization.html');
assert.match(historicalMmat, /visualização histórica[^<]*17 registros/i, 'the legacy MMAT visualization must identify its historical 17-study denominator');
assert.match(historicalMmat, /15 registros empíricos mantidos provisoriamente[\s\S]*MMAT preliminar em 14/i, 'the legacy MMAT visualization must point readers to current scope and appraisal counts');
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
assert.match(mmat, /visualização histórica/i, 'the current page must preserve historical provenance');
assert.match(mmat, /O registro de apreciação reúne 18 itens/i, 'the current page must expose the current scope in reader-facing language');
assert.equal((mmat.match(/class="study-title"/g) || []).length, 18, 'the current page must render every current MMAT record');
assert.match(mmat, /<span class="metric-value">15<\/span><span class="metric-label">textos primários revisados<\/span>/, 'the current page must report all externally reviewed primary texts');
assert.match(mmat, /<span class="metric-value">14<\/span><span class="metric-label">estudos com apreciação MMAT preliminar<\/span>/, 'the current page must distinguish MMAT-appraised studies from empirical inclusion');
assert.match(mmat, /<span class="metric-value">1<\/span><span class="metric-label">texto integral pendente<\/span>/, 'the current page must report shortlisted full texts that remain unretrieved');
assert.match(mmat, /Um texto integral ainda não foi recuperado e não recebeu apreciação MMAT\. Um registro foi excluído após a triagem do resumo e não recebeu MMAT\./, 'the evidence summary must distinguish the unretrieved full text from the abstract-stage exclusion');
assert.doesNotMatch(mmat, /abstracts?\/metadados/i, 'the current page should use Portuguese for source-availability labels');
const zengRow = mmat.match(/<tr>\s*<td>6923<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(zengRow, 'study 6923 must be present in the current MMAT table');
assert.match(zengRow, /texto integral pendente; MMAT não aplicado/, 'study 6923 must be held without MMAT appraisal until its primary text is retrieved');
assert.equal([...zengRow.matchAll(/aria-label="Não avaliado"/g)].length, 7, 'pending study 6923 must leave S1, S2 and Q1–Q5 unappraised');
assert.doesNotMatch(zengRow, /aria-label="Resposta:/, 'pending study 6923 must not expose MMAT responses');
const abstractExcludedRow = mmat.match(/<tr>\s*<td>9<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(abstractExcludedRow, 'the abstract-stage exclusion must remain visible in the 18-record ledger');
assert.match(abstractExcludedRow, /excluído após resumo; MMAT não aplicado/, 'the abstract-stage exclusion must not appear appraised');
assert.equal([...abstractExcludedRow.matchAll(/aria-label="Não avaliado"/g)].length, 7, 'the abstract-stage exclusion must leave all MMAT responses unappraised');
const unitHoldRow = mmat.match(/<tr>\s*<td>8<\/td>[\s\S]*?<\/tr>/)?.[0];
assert.ok(unitHoldRow, 'study 8 must remain visible in the current 18-record ledger');
assert.match(unitHoldRow, /MMAT suspenso; unidade de análise pendente/, 'study 8 must be retained but visibly held from MMAT appraisal');
assert.equal([...unitHoldRow.matchAll(/aria-label="Não avaliado"/g)].length, 7, 'study 8 must expose no S1/S2/Q1-Q5 responses while its appraisal unit is pending');
assert.doesNotMatch(unitHoldRow, /aria-label="Resposta:/, 'study 8 must not present provisional MMAT responses as decisions');
const unitHoldEvidence = mmat.slice(mmat.indexOf(unitHoldRow));
assert.match(unitHoldEvidence, /componentes distintos e não devem ser somados/i, 'study 8 must state that its datasets are distinct and must not be combined');
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
assert.equal([...protocolRow.matchAll(/aria-label="Resposta: ([^"]+)"/g)].length, 7, 'protocol screening and appraisal cells must remain explicit');
assert.equal([...protocolRow.matchAll(/aria-label="Resposta: Não se aplica"/g)].length, 7, 'all protocol criteria must be visibly marked not applicable');
for (const studyId of ['6916', '6919', '6920']) {
  const mixedRow = mmat.match(new RegExp(`<tr>\\s*<td>${studyId}<\\/td>[\\s\\S]*?<\\/tr>[\\s\\S]*?<tr class="mmat-evidence-row">[\\s\\S]*?<\\/tr>`))?.[0];
  assert.ok(mixedRow, `mixed-methods study ${studyId} must expose its evidence row`);
  assert.match(mixedRow, /Avaliação dos componentes/, `mixed-methods study ${studyId} must disclose component appraisals`);
  assert.match(mixedRow, /qualitativo|quantitativo/i, `mixed-methods study ${studyId} must identify component types`);
}
assert.match(mmat, /<td>6919<\/td>[\s\S]{0,1200}texto primário revisado/, 'study 6919 must be identified as externally reviewed in the current table');
assert.match(mmat, /He2025_6915 · quantitative_nonrandomized · componente escolar/, 'study 6915 must identify the classroom component as its appraisal unit');
assert.match(mmat, /Perguntas de triagem do MMAT 2018/i, 'the current page must expose the MMAT screening questions');
assert.match(mmat, /Há perguntas de pesquisa claras\?/i, 'the current page must expose S1');
assert.match(mmat, /Os dados coletados permitem responder às perguntas de pesquisa\?/i, 'the current page must expose S2');
assert.match(mmat, /No recorte atual, S1 e S2 estão preenchidas para 14 estudos empíricos com apreciação MMAT\. 1 registro com texto consultado está temporariamente sem respostas enquanto se define a unidade de apreciação; 1 registro aguarda texto integral e também não recebe MMAT\. Um registro foi excluído após a triagem do resumo e não recebeu MMAT\./i, 'the current page must distinguish MMAT appraisal from empirical inclusion, unretrieved reports and abstract-stage exclusion');
assert.match(mmat, /Are there clear research questions\?/i, 'the current page must preserve the original S1 wording');
assert.match(mmat, /Critérios de apreciação por delineamento/i, 'the current page must expose design-specific criteria');
assert.match(mmat, /MMAT 2018<\/a>/i, 'the current page must cite the MMAT 2018 source');
assert.match(mmat, /href="\.\.\/\.\.\/\.\.\/research\/data\/mmat_current_study_registry\.csv"/, 'the current page must link to the versioned registry at its published path');
assert.match(mmat, /href="\.\.\/\.\.\/\.\.\/research\/data\/mmat_primary_sources_manifest\.csv"/, 'the current page must expose the primary-source provenance manifest');
assert.equal((mmat.match(/class="mmat-question-group"/g) || []).length, 5, 'the current page must expose all MMAT design groups');
assert.match(mmat, /O que esta avaliação registra/i, 'the public page must explain the purpose of the appraisal in reader-facing language');
assert.doesNotMatch(mmat, /\b(?:ledger|shortlist|snapshot)\b/i, 'the public page must avoid unexplained development jargon');
assert.match(mmat, /Data de corte da busca: 31\/08\/2026\. Recorte consolidado em 03\/09\/2026\. Escopo MMAT atual reconciliado em 14\/10\/2026; apreciações registradas até 14\/10\/2026\./i, 'the current page must distinguish search cutoff, adjudication and current MMAT scope dates');
assert.doesNotMatch(mmat, /Recorte do corpus: 12\/10\/2026/i, 'the scope update date must not be presented as a new search record');
assert.match(mmat, /apreciações registradas até 14\/10\/2026/i, 'the current page must expose the latest appraisal date');
assert.equal((mmat.match(/class="mmat-evidence"/g) || []).length, 18, 'every MMAT record must expose criterion evidence details');
assert.match(mmat, /Ver perguntas, justificativas e localização da evidência/i, 'the evidence disclosure must be clearly labeled');
assert.match(mmat, /medidas acadêmicas e demográficas/i, 'the current page must expose the evidence note for study 2 Q3');
assert.match(mmat, /não preserva evidência ou localizador suficiente para julgar a adequação da mensuração/i, 'the current page must explain why study 2 Q3 remains indeterminate');
assert.match(mmat, /class="question-code">3\.1</, 'non-randomized quantitative components must use MMAT category 3');
assert.doesNotMatch(mmat, /class="question-code">2\.1</, 'non-randomized quantitative components must not use randomized category 2');
assert.equal((mmat.match(/Não aplicável: protocolo contextual sem resultados empíricos concluídos\./g) || []).length, 5, 'all protocol MMAT criteria must explain why N/A applies');
for (const criterion of ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']) {
  assert.match(mmat, new RegExp(`>${criterion}<`), `the current page must expose ${criterion}`);
}

console.log(`site contract passed: ${expectedPages.length} public pages`);
