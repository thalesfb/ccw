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
  <h1>Ensino Personalizado de<br>Matemática:<br>Oportunidades e<br>Técnicas Computacionais</h1>
  <div class="cover-credits">
    <strong>Trabalho de Conclusão de Curso (TCC)</strong><br>
    Acadêmico: Thales Ferreira Batista | Curso: Ciência da Computação<br>
    Orientador: Dr. Rafael Zanin | Coorientador: Dr. Manassés Ribeiro
  </div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">01 / CONTEXTO</div>

# Por que esta revisão?

<div class="problem-hero">
  <div class="problem-lead">
    <div class="visual-marker">01</div>
    <span class="card-label">O DESAFIO</span>
    <h2>Diagnóstico personalizado em larga escala</h2>
    <p>Turmas são heterogêneas. Professores precisam reconhecer necessidades de aprendizagem em tempo hábil para orientar decisões pedagógicas.</p>
    <div class="hand-line">heterogeneidade<br>→ decisão pedagógica</div>
  </div>
  <div class="challenge-grid">
    <div class="challenge-card challenge-blue"><span class="challenge-icon">◌</span><strong>Turmas heterogêneas</strong><span>Necessidades individuais não aparecem em uma média única.</span></div>
    <div class="challenge-card challenge-green"><span class="challenge-icon">◷</span><strong>Tempo docente</strong><span>O diagnóstico manual precisa ser apoiado por evidências organizadas.</span></div>
    <div class="challenge-card challenge-orange"><span class="challenge-icon">⌁</span><strong>Ensino genérico</strong><span>Uma mesma intervenção pode não servir a trajetórias diferentes.</span></div>
    <div class="challenge-card challenge-red"><span class="challenge-icon">?</span><strong>Literatura fragmentada</strong><span>As aplicações estão dispersas entre técnicas, desenhos e contextos.</span></div>
  </div>
</div>

<div class="scope-note"><strong>Questão central</strong> Como técnicas computacionais podem apoiar o diagnóstico e a personalização do ensino de matemática?<br><span>Escopo: mapear evidências e lacunas — não há protótipo validado nem estimativa agregada de eficácia.</span></div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">02 / PERGUNTAS</div>

# Perguntas e objetivo

<div class="rq-grid">
  <div class="rq-card rq-blue"><span>RQ1</span><div><strong>O quê?</strong><p>Quais técnicas computacionais são aplicadas à educação matemática?</p></div></div>
  <div class="rq-card rq-green"><span>RQ2</span><div><strong>Como?</strong><p>Como essas aplicações são avaliadas em contextos educacionais?</p></div></div>
  <div class="rq-card rq-orange"><span>RQ3</span><div><strong>O que falta?</strong><p>Quais lacunas, limitações e desafios são reportados?</p></div></div>
  <div class="rq-card rq-red"><span>RQ4</span><div><strong>E agora?</strong><p>Que direcionamentos podem apoiar ferramentas educacionais mais eficazes?</p></div></div>
</div>

<div class="objective-band"><span class="band-label">OBJETIVO</span><p>Mapear e analisar aplicações de <em>machine learning</em>, <em>learning analytics</em> e sistemas tutores inteligentes na educação matemática, identificando tendências, lacunas e requisitos para uma especificação técnica e pedagógica de protótipo.</p></div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">03 / OBJETIVOS</div>

# O que este trabalho entrega

<div class="objective-callout"><span class="card-label">OBJETIVO GERAL</span><p>Mapear aplicações computacionais no ensino de matemática e derivar uma especificação conceitual de protótipo para apoiar o professor.</p><div class="hand-line">evidência → requisito</div></div>

<div class="objective-roadmap">
  <div class="objective-step step-blue"><div><b>01</b><span>⌕</span></div><strong>Revisar</strong><p>Estudos de 2015 a 2026.</p></div>
  <div class="objective-step step-green"><div><b>02</b><span>⌘</span></div><strong>Categorizar</strong><p>Abordagens computacionais.</p></div>
  <div class="objective-step step-orange"><div><b>03</b><span>◆</span></div><strong>Classificar</strong><p>Finalidades pedagógicas.</p></div>
  <div class="objective-step step-red"><div><b>04</b><span>✓</span></div><strong>Analisar</strong><p>Metodologias e limitações.</p></div>
  <div class="objective-step step-blue"><div><b>05</b><span>⌁</span></div><strong>Mapear</strong><p>Lacunas técnicas e pedagógicas.</p></div>
  <div class="objective-step step-green"><div><b>06</b><span>↻</span></div><strong>Auditar</strong><p>Pipeline e artefatos versionados.</p></div>
  <div class="objective-step step-orange"><div><b>07</b><span>→</span></div><strong>Derivar</strong><p>Requisitos, avaliação e arquitetura.</p></div>
</div>

<div class="roadmap-caption">Busca <span>→</span> classificação <span>→</span> síntese <span>→</span> especificação</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">04 / BASE CONCEITUAL</div>

# Quatro níveis de interpretação

<div class="interpretation-ladder">
  <div class="interpretation-level level-blue"><b>01</b><strong>Desempenho observado</strong><span>Acertos, notas, tentativas, estratégias ou tempo registrados em uma tarefa.</span></div>
  <div class="interpretation-level level-green"><b>02</b><strong>Proficiência estimada</strong><span>Inferência produzida por um modelo a partir de várias evidências.</span></div>
  <div class="interpretation-level level-orange"><b>03</b><strong>Competência</strong><span>Mobilização de conhecimentos, procedimentos e atitudes para resolver problemas.</span></div>
  <div class="interpretation-level level-red"><b>04</b><strong>Aprendizagem</strong><span>Transformação construída ao longo do tempo, com compreensão, autonomia e transferência.</span></div>
</div>

<div class="concept-note"><strong>Regra de interpretação:</strong> uma saída computacional pode organizar evidências e produzir estimativas, mas não observa sozinha todos os processos cognitivos, sociais e afetivos da aprendizagem.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">06 / MÉTODO</div>

# Protocolo e escopo

<div class="method-layout">
  <div class="method-intro">
    <div class="number-stamp">PRISMA<br><b>2020</b></div>
    <h2>Uma busca em camadas, com escopo explícito.</h2>
    <div class="search-visual" aria-label="Busca em três camadas: matemática, técnicas e educação">
      <div class="search-ring search-ring-outer"><span>EDUCAÇÃO</span>
        <div class="search-ring search-ring-middle"><span>TÉCNICAS</span>
          <div class="search-ring search-ring-core"><span>MATEMÁTICA</span></div>
        </div>
      </div>
    </div>
    <p>O score organiza o processamento. Não substitui a adjudicação de escopo, a avaliação metodológica ou a leitura das fontes primárias.</p>
  </div>
  <div class="method-list">
    <div><span>RECORTE TEMPORAL</span><strong>2015–2026</strong></div>
    <div><span>IDIOMAS PLANEJADOS</span><strong>inglês e português</strong></div>
    <div><span>CONSULTAS CANÔNICAS</span><strong>72 <small>(48 EN + 24 PT)</small></strong></div>
    <div><span>FONTES</span><strong>Semantic Scholar · OpenAlex<br>Crossref · CORE</strong></div>
    <div><span>ESTRUTURA</span><strong>PICOS <small>população · intervenção · comparação · desfecho · desenho</small></strong></div>
    <div><span>LITERATURA CINZENTA</span><strong>Teses e dissertações aceitas<br><small>sob os mesmos critérios</small></strong></div>
    <div><span>FILTRO OPERACIONAL</span><strong>score de relevância ≥ 4,0</strong></div>
  </div>
</div>

---
layout: default
class: content-slide flow-slide
---

<div class="slide-kicker">07 / SELEÇÃO</div>

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

<div class="slide-kicker">08 / FLUXO</div>

# Fluxo PRISMA dos dados da revisão

<img src="./public/images/prisma_flow.png" alt="Fluxo PRISMA dos dados da revisão" class="feature-image prisma-image" />

<small class="source-note">Fonte versionada: `research/exports/visualizations/prisma_flow.png`.</small>

---
layout: default
class: content-slide
---

<div class="slide-kicker">09 / DEDUPLICAÇÃO</div>

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

<div class="slide-kicker">10 / PANORAMA</div>

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

<div class="slide-kicker">11 / DISTRIBUIÇÃO</div>

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

<div class="slide-kicker">12 / RELEVÂNCIA</div>

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

<div class="slide-kicker">13 / RETENÇÃO</div>

# População retida e síntese

<div class="retained-layout">
  <div class="retained-stat"><strong>18</strong><span>registros nos dados da revisão</span><div class="stat-split"><b>17</b> candidatos empíricos provisórios <i></i> <b>1</b> protocolo contextual</div></div>
  <div class="mmat-card"><div class="stamp-outline">17<br><b>+ 1</b></div><div><h2>Dois estratos de leitura</h2><p>Os 17 candidatos empíricos sustentam a síntese. O protocolo ou proposta contextual permanece para rastreabilidade, sem resultado empírico.</p><p class="muted"><strong>Retenção operacional ≠ evidência homogênea.</strong></p></div></div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">14 / MMAT</div>

# Apreciação metodológica sem nota global

<div class="mmat-overview">
  <div class="mmat-principles"><span class="card-label">MMAT 2018</span><strong>Leitura por critério</strong><p>As respostas são registradas como <b>Sim</b>, <b>Não</b> ou <b>Não é possível determinar</b>, conforme o desenho de cada estudo.</p><div class="hand-line">transparência<br>antes do ranking</div></div>
  <div class="mmat-criteria">
    <div><b>S</b><strong>Sim</strong><span>Critério atendido segundo a evidência disponível.</span></div>
    <div><b>N</b><strong>Não</strong><span>Critério não atendido na apreciação documental.</span></div>
    <div><b>ND</b><strong>Indeterminado</strong><span>Informação insuficiente para concluir.</span></div>
  </div>
</div>

<div class="scope-note"><strong>Estado da apreciação:</strong> nove registros tiveram texto primário revisado e oito foram apreciados com resumo/metadados. O trabalho foi conduzido por um único revisor; recuperação de fontes, localizadores e adjudicação ainda precisam ser consolidados.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">15 / SÍNTESE</div>

# O que emerge nos 17 candidatos empíricos

<div class="synthesis-layout">
  <div class="synthesis-lead"><span class="card-label">PADRÃO DOMINANTE</span><strong>Predição e estimativa</strong><p>A síntese aponta recorrência de tarefas de predição de desempenho e estimativa de proficiência, com uso frequente de modelos supervisionados.</p><div class="hand-line">resultado ≠ aprendizagem</div></div>
  <div class="synthesis-grid">
    <div><span>FINALIDADE</span><strong>Predição de desempenho</strong><small>Reconhecer padrões em registros de avaliação.</small></div>
    <div><span>FINALIDADE</span><strong>Estimativa de proficiência</strong><small>Inferir níveis a partir de evidências observadas.</small></div>
    <div><span>MODELOS RECORRENTES</span><strong>RF, SVM e redes neurais</strong><small>Alternativas com pressupostos e explicabilidade distintos.</small></div>
    <div><span>LEITURA CRÍTICA</span><strong>Comparabilidade limitada</strong><small>Populações, instrumentos, variáveis e métricas variam entre estudos.</small></div>
  </div>
</div>

<div class="bottom-caption">A síntese organiza o estado da literatura; não estabelece ranking de modelos nem eficácia pedagógica geral.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">16 / INTERPRETAÇÃO</div>

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

<div class="slide-kicker">17 / LACUNAS</div>

# Lacunas documentadas

<div class="gap-grid">
  <div class="gap-card gap-blue"><span>01</span><strong>Explicabilidade</strong><p>Resultados precisam ser compreensíveis e acompanhados de incerteza.</p></div>
  <div class="gap-card gap-green"><span>02</span><strong>Integração curricular</strong><p>Indicadores devem se relacionar a objetivos e descritores matemáticos.</p></div>
  <div class="gap-card gap-orange"><span>03</span><strong>Participação docente</strong><p>A interpretação e a decisão pedagógica não podem ser automatizadas.</p></div>
  <div class="gap-card gap-red"><span>04</span><strong>Equidade</strong><p>Erros sistemáticos entre grupos precisam ser investigados.</p></div>
  <div class="gap-card gap-blue"><span>05</span><strong>Reprodutibilidade</strong><p>Dados, código, parâmetros e decisões devem permanecer rastreáveis.</p></div>
  <div class="gap-card gap-green"><span>06</span><strong>Validação contextual</strong><p>Resultados dependem da população, do instrumento e do ambiente educacional.</p></div>
</div>

<div class="scope-note"><strong>Como a revisão usa essas lacunas:</strong> elas orientam requisitos da especificação; não são apresentadas como prova de que uma solução futura será eficaz.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">18 / ESPECIFICAÇÃO</div>

# Da evidência à especificação

<div class="derivation-flow">
  <div><span>01</span><strong>Evidências</strong><small>literatura + fundamentação</small></div><i>→</i>
  <div><span>02</span><strong>Lacunas</strong><small>riscos e necessidades</small></div><i>→</i>
  <div><span>03</span><strong>Requisitos</strong><small>funções e restrições</small></div><i>→</i>
  <div><span>04</span><strong>Protocolo</strong><small>critérios de avaliação</small></div><i>→</i>
  <div><span>05</span><strong>Arquitetura</strong><small>referência conceitual</small></div>
</div>

<div class="derivation-note"><strong>Entrega do TCC:</strong> uma especificação técnica e pedagógica auditável. O artefato não é uma aplicação funcional, não usa uma base definitiva e não possui validação com participantes.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">19 / ARQUITETURA</div>

# Arquitetura de referência em cinco componentes

<div class="architecture-stack">
  <div class="architecture-layer layer-present"><b>05</b><strong>Apresentação</strong><span>indicadores, explicações e limitações para análise docente</span></div>
  <div class="architecture-layer layer-eval"><b>04</b><strong>Avaliação e explicabilidade</strong><span>métricas, erros, incerteza e explicações</span></div>
  <div class="architecture-layer layer-model"><b>03</b><strong>Modelagem</strong><span>treino e comparação de modelos candidatos</span></div>
  <div class="architecture-layer layer-prep"><b>02</b><strong>Preparação</strong><span>ausentes, codificação, transformação e documentação</span></div>
  <div class="architecture-layer layer-data"><b>01</b><strong>Ingestão</strong><span>leitura e validação das fontes de dados</span></div>
</div>

<div class="bottom-caption">A separação favorece testabilidade, rastreabilidade e substituição controlada de técnicas.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">20 / REPRODUTIBILIDADE</div>

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

<div class="slide-kicker">21 / CONTINUIDADE</div>

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
