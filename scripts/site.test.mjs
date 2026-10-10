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
assert.match(homepage, /ifc-campus-videira-horizontal\.png/, 'the homepage must use the official IFC mark');
assert.doesNotMatch(homepage, /linear-gradient|Segoe UI.*Tahoma/i, 'the homepage must not retain the legacy visual system');

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
assert.match(mmat, /não é uma nota global/i, 'the MMAT page must reject aggregate scoring');
assert.match(mmat, /visualização histórica/i, 'the current page must preserve historical provenance');
assert.match(mmat, /18 registros/i, 'the current page must expose the current denominator');
assert.equal((mmat.match(/class="study-title"/g) || []).length, 18, 'the current page must render every current MMAT record');
assert.match(mmat, /<span class="metric-value">12<\/span><span class="metric-label">textos primários revisados<\/span>/, 'the current page must report all externally reviewed primary texts');
assert.match(mmat, /<span class="metric-value">5<\/span><span class="metric-label">abstracts\/metadados<\/span>/, 'the current page must report the remaining abstract-only assessments');
assert.match(mmat, /<td>6919<\/td>[\s\S]{0,1200}texto primário revisado/, 'study 6919 must be identified as externally reviewed in the current table');
assert.match(mmat, /Perguntas de triagem do MMAT 2018/i, 'the current page must expose the MMAT screening questions');
assert.match(mmat, /Há perguntas de pesquisa claras\?/i, 'the current page must expose S1');
assert.match(mmat, /Os dados coletados permitem responder às perguntas de pesquisa\?/i, 'the current page must expose S2');
assert.match(mmat, /Are there clear research questions\?/i, 'the current page must preserve the original S1 wording');
assert.match(mmat, /Critérios de apreciação por delineamento/i, 'the current page must expose design-specific criteria');
assert.match(mmat, /MMAT 2018<\/a>/i, 'the current page must cite the MMAT 2018 source');
assert.match(mmat, /href="\.\.\/\.\.\/\.\.\/research\/data\/mmat_current_study_registry\.csv"/, 'the current page must link to the versioned registry at its published path');
assert.match(mmat, /href="\.\.\/\.\.\/\.\.\/research\/data\/mmat_primary_sources_manifest\.csv"/, 'the current page must expose the primary-source provenance manifest');
assert.equal((mmat.match(/class="mmat-question-group"/g) || []).length, 5, 'the current page must expose all MMAT design groups');
for (const criterion of ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']) {
  assert.match(mmat, new RegExp(`>${criterion}<`), `the current page must expose ${criterion}`);
}

console.log(`site contract passed: ${expectedPages.length} public pages`);
