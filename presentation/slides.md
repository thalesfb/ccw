---
theme: default
layout: default
class: cover-page
colorSchema: light
fonts:
  sans: Barlow
  serif: Asap
title: "Ensino Personalizado de Matemática"
info: "Revisão Sistemática da Literatura — dados da revisão"
author: "Thales Ferreira Batista"
keywords: "TCC, ensino personalizado, matemática, revisão sistemática, PRISMA"
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

<div class="cover-art cover-art-top">∫ f(x) dx · ∑ yᵢ · lim Δx→0</div>
<div class="cover-art cover-art-left">y = mx + b<br>f(x) = x² + 2x</div>
<div class="cover-art cover-art-right">2√(y² − x²)<br>∂f / ∂x</div>
<div class="cover-art cover-art-bottom">∫∫ R f(x,y) dA</div>

<div class="ifc-mark" aria-label="Instituto Federal Catarinense">
  <div class="ifc-symbol"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div><strong>INSTITUTO FEDERAL</strong><span>Catarinense</span></div>
</div>

<div class="cover-slide">
  <div class="cover-kicker">TRABALHO DE CONCLUSÃO DE CURSO · 2026</div>
  <h1>Ensino Personalizado de<br>Matemática:</h1>
  <h2>Oportunidades e Técnicas<br>Computacionais</h2>
  <div class="cover-rule"></div>
  <div class="cover-subtitle">Revisão Sistemática da Literatura<br><span>relato orientado pelo PRISMA 2020</span></div>
  <div class="cover-credits">
    <strong>Thales Ferreira Batista</strong> · Ciência da Computação<br>
    <span>Orientador: Dr. Rafael Zanin</span> · <span>Coorientador: Dr. Manassés Ribeiro</span>
  </div>
  <div class="cover-footer"><span>IFC — Videira</span><span>Dados da revisão: 03/09/2026 · recorte temporal: 2015–2026</span></div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">01 / CONTEXTO</div>

# Por que esta revisão?

<div class="context-grid">
  <div class="statement-card statement-card-dark">
    <span class="card-label">PONTO DE PARTIDA</span>
    <p>Turmas são heterogêneas. Professores precisam reconhecer necessidades de aprendizagem em tempo hábil.</p>
    <div class="hand-line">heterogeneidade<br>→ decisão pedagógica</div>
  </div>
  <div class="context-stack">
    <div class="statement-card">
      <span class="card-label">QUESTÃO CENTRAL</span>
      <h3>Como técnicas computacionais podem apoiar o diagnóstico e a personalização do ensino de matemática?</h3>
    </div>
    <div class="scope-note"><strong>Escopo da revisão</strong><br>Mapear evidências e lacunas. Não há protótipo validado nem estimativa agregada de eficácia.</div>
  </div>
</div>

<div class="bottom-caption">Ensino personalizado começa com uma leitura melhor da aprendizagem.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">02 / PERGUNTAS</div>

# Perguntas e objetivo

<div class="rq-grid">
  <div class="rq-card"><span>RQ1</span><p>Quais técnicas computacionais são aplicadas à educação matemática?</p></div>
  <div class="rq-card"><span>RQ2</span><p>Como essas aplicações são avaliadas em contextos educacionais?</p></div>
  <div class="rq-card"><span>RQ3</span><p>Quais lacunas, limitações e desafios são reportados?</p></div>
  <div class="rq-card"><span>RQ4</span><p>Que direcionamentos podem apoiar ferramentas educacionais mais eficazes?</p></div>
</div>

<div class="objective-band"><span class="band-label">OBJETIVO</span><p>Mapear e analisar aplicações de <em>machine learning</em>, <em>learning analytics</em> e sistemas tutores inteligentes na educação matemática, identificando tendências, lacunas e requisitos para uma especificação técnica e pedagógica de protótipo.</p></div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">03 / MÉTODO</div>

# Protocolo e escopo

<div class="method-layout">
  <div class="method-intro">
    <div class="number-stamp">PRISMA<br><b>2020</b></div>
    <h2>Um recorte explícito para organizar a busca.</h2>
    <p>O score organiza o processamento. Ele não substitui a adjudicação de escopo, a avaliação metodológica ou a leitura das fontes primárias.</p>
  </div>
  <div class="method-list">
    <div><span>RECORTE TEMPORAL</span><strong>2015–2026</strong></div>
    <div><span>IDIOMAS PLANEJADOS</span><strong>inglês e português</strong></div>
    <div><span>CONSULTAS CANÔNICAS</span><strong>72 <small>(48 EN + 24 PT)</small></strong></div>
    <div><span>FONTES</span><strong>Semantic Scholar · OpenAlex<br>Crossref · CORE</strong></div>
    <div><span>LITERATURA CINZENTA</span><strong>Teses e dissertações aceitas<br><small>sob os mesmos critérios</small></strong></div>
    <div><span>FILTRO OPERACIONAL</span><strong>score de relevância ≥ 4,0</strong></div>
  </div>
</div>

---
layout: default
class: content-slide flow-slide
---

<div class="slide-kicker">04 / SELEÇÃO</div>

# Do registro bruto à população retida

<div class="flow-board">
  <div class="flow-row">
    <div class="flow-card flow-blue"><strong>11.904</strong><span>identificados</span></div><div class="flow-arrow">→</div>
    <div class="flow-card flow-teal"><strong>27</strong><span>remoções determinísticas<br>(25 DOI + 2 URL)</span></div><div class="flow-arrow">→</div>
    <div class="flow-card flow-green"><strong>11.877</strong><span>na triagem</span></div>
  </div>
  <div class="flow-row">
    <div class="flow-card flow-amber"><strong>9.391</strong><span>excluídos na triagem</span></div><div class="flow-arrow">→</div>
    <div class="flow-card flow-orange"><strong>2.486</strong><span>na elegibilidade</span></div><div class="flow-arrow">→</div>
    <div class="flow-card flow-violet"><strong>2.468</strong><span>excluídos na elegibilidade</span></div>
  </div>
  <div class="flow-final"><div class="flow-card flow-indigo"><strong>18</strong><span>retidos no conjunto analisado</span></div></div>
</div>

<div class="flow-note"><span class="note-mark">!</span> Identidade DOI/URL é tratada de forma determinística. Igualdade de título permanece como candidato à auditoria semântica, não como remoção automática.</div>

---
layout: center
class: image-slide
---

<div class="slide-kicker">05 / FLUXO</div>

# Fluxo PRISMA dos dados da revisão

<img src="./public/images/prisma_flow.png" alt="Fluxo PRISMA dos dados da revisão" class="feature-image prisma-image" />

<small class="source-note">Fonte versionada: `research/exports/visualizations/prisma_flow.png`.</small>

---
layout: default
class: content-slide
---

<div class="slide-kicker">06 / DEDUPLICAÇÃO</div>

# O que a deduplicação significa

<div class="dedupe-layout">
  <div class="dedupe-copy">
    <div class="big-number"><strong>27</strong><span>registros removidos<br>por identidade DOI/URL</span></div>
    <div class="reading-list">
      <div><b>01</b><span>Não há remoção automática apenas por igualdade de título.</span></div>
      <div><b>02</b><span>Há 232 excedentes apenas por título após a remoção determinística.</span></div>
      <div><b>03</b><span>Excedentes são candidatos a revisão semântica; não equivalem a duplicatas confirmadas.</span></div>
    </div>
  </div>
  <div class="image-frame"><img src="./public/images/selection_funnel.png" alt="Funil de seleção da revisão" /></div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">07 / PANORAMA</div>

# Panorama descritivo dos dados da revisão

<div class="metric-grid">
  <div><strong>6.399</strong><span>técnica não especificada</span></div>
  <div><strong>1.073</strong><span>assessment</span></div>
  <div><strong>863</strong><span>IA / inteligência artificial</span></div>
  <div><strong>771</strong><span>machine learning</span></div>
  <div><strong>345</strong><span>análise preditiva</span></div>
</div>

<div class="chart-frame"><img src="./public/images/techniques_distribution.png" alt="Distribuição de técnicas nos dados da revisão" /></div>

<small class="source-note">Frequências calculadas sobre os 11.877 registros após remoção determinística. Categorias podem se sobrepor e não representam apenas os 18 retidos, qualidade ou eficácia.</small>

---
layout: default
class: content-slide
---

<div class="slide-kicker">08 / DISTRIBUIÇÃO</div>

# Distribuição temporal e fontes

<div class="two-images">
  <div class="chart-panel"><img src="./public/images/papers_by_year.png" alt="Distribuição de registros por ano" /><small>Registros por ano nos dados versionados da revisão.</small></div>
  <div class="chart-panel"><img src="./public/images/database_coverage.png" alt="Cobertura por base de dados" /><small>Registros associados às quatro fontes consultadas.</small></div>
</div>

<div class="bottom-caption">Visualizações descritivas. Não inferem representatividade, qualidade ou efeito pedagógico.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">09 / RELEVÂNCIA</div>

# Score de relevância: filtro operacional

<div class="score-layout">
  <div class="score-chart"><img src="./public/images/relevance_distribution.png" alt="Distribuição do score de relevância" /></div>
  <div class="score-copy">
    <div class="score-badge">≥ 4,0</div>
    <h2>Organiza o processamento.</h2>
    <p>O score não é medida de qualidade metodológica. Não produz ranking. Não substitui a leitura das fontes primárias.</p>
    <div class="caution-line"><span>!</span><strong>Filtro operacional ≠ conclusão científica</strong></div>
  </div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">10 / RETENÇÃO</div>

# População retida e MMAT

<div class="retained-layout">
  <div class="retained-stat"><strong>18</strong><span>registros nos dados da revisão</span><div class="stat-split"><b>17</b> candidatos empíricos provisórios <i></i> <b>1</b> protocolo contextual</div></div>
  <div class="mmat-card"><div class="stamp-outline">MMAT<br><b>2018</b></div><div><h2>Leitura por critério</h2><p>O ledger atual é preliminar. Recuperação das fontes, localizadores e adjudicação final permanecem necessários.</p><p class="muted"><strong>Sem nota média.</strong> Sem ranking. Sem conclusão global de qualidade metodológica.</p></div></div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">11 / INTERPRETAÇÃO</div>

# O que podemos concluir — e o que não podemos

<div class="conclusion-grid">
  <div class="conclusion-card can"><div class="conclusion-icon">✓</div><div><span>PODEMOS AFIRMAR</span><h2>Mapa auditável</h2><p>Os dados da revisão organizam aplicações encontradas, etapas de seleção e lacunas documentadas.</p></div></div>
  <div class="conclusion-card cannot"><div class="conclusion-icon">×</div><div><span>AINDA NÃO PODEMOS AFIRMAR</span><h2>Eficácia geral</h2><p>Não há base para afirmar superioridade entre modelos ou protótipo validado em escolas.</p></div></div>
</div>

<div class="bottom-caption">Resultados individuais exigem leitura das fontes primárias: população, instrumento, métrica e desenho de avaliação.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">12 / REPRODUTIBILIDADE</div>

# Reprodutibilidade sem distribuir o SQLite

<div class="artifact-grid">
  <div><span class="artifact-icon">CSV</span><strong>CSV / JSON</strong><small>dados da revisão e ledgers de decisão</small></div>
  <div><span class="artifact-icon">Bib</span><strong>BibTeX</strong><small>referências derivadas do pipeline</small></div>
  <div><span class="artifact-icon">#</span><strong>Manifesto</strong><small>hashes e escopo dos artefatos</small></div>
  <div><span class="artifact-icon">▧</span><strong>PNG / HTML</strong><small>relatórios e visualizações públicas</small></div>
</div>

<div class="path-list"><code>research/exports/analysis/papers.csv</code><code>research/exports/reports/summary.json</code><code>research/exports/reports/reproducibility_manifest.json</code></div>

<div class="scope-note">A bibliografia derivada do pipeline permanece separada das referências teóricas, pedagógicas, metodológicas e técnicas usadas na fundamentação do TCC.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">13 / CONTINUIDADE</div>

# Próximos passos científicos

<div class="next-layout">
  <div class="next-list">
    <div><b>01</b><span>Consolidar recuperação das fontes e adjudicação final do MMAT.</span></div>
    <div><b>02</b><span>Revisar lacunas à luz dos 17 estudos empíricos provisórios.</span></div>
    <div><b>03</b><span>Revisar especificação conceitual do protótipo à luz da adjudicação final.</span></div>
    <div><b>04</b><span>Qualquer validação experimental exigirá novo protocolo e autorização.</span></div>
  </div>
  <div class="next-note"><span>PRÓXIMA DECISÃO</span><strong>evidência<br>antes da implementação</strong><i>∴</i></div>
</div>

<div class="objective-band compact"><p>A revisão sistemática fundamenta próximas decisões; não substitui o protocolo do experimento.</p></div>

---
layout: center
class: closing-slide
---

<div class="close-mark">∫</div>

# Obrigado

## Perguntas e discussão

<div class="close-rule"></div>
<p class="close-title"><strong>Ensino Personalizado de Matemática</strong><br>Oportunidades e Técnicas Computacionais</p>
<p class="close-sources">Fonte pública do TCC: <a href="https://thalesfb.github.io/ccw/results/tcc/main.pdf">thalesfb.github.io/ccw/results/tcc/main.pdf</a> · visualizações versionadas no repositório</p>
