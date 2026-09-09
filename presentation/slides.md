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

<div class="cover-art cover-art-top-left">∫ f(x) · dx = e<sup>nt</sup> = g(x)<br>f(x) = ∫ f′(x) dx</div>
<div class="cover-art cover-art-top">∂² / ∂x² &nbsp;&nbsp; lim Δx→0</div>
<div class="cover-art cover-art-top-right">P = {2, 1, 3} &nbsp; M = [a<sub>ij</sub>]<br>A = [a₁&nbsp; a₂&nbsp; a₃]</div>
<div class="cover-art cover-art-left">x − z<br>────── · dx<br>2πr + 1</div>
<div class="cover-art cover-art-right">A = [a₁&nbsp; a₂&nbsp; a₃]<br>△ ABC &nbsp;&nbsp; ∂f / ∂x</div>
<div class="cover-art cover-art-bottom-left">R₀ = hθ<sup>2</sup> / 2<br>y = (x − 1)²</div>
<div class="cover-art cover-art-bottom">∫∫ R f(x,y) dA</div>
<div class="cover-art cover-art-bottom-right">n = −√(a²x²)<br>sin(x) = Δπ / n</div>

<div class="ifc-mark" aria-label="Instituto Federal Catarinense">
  <div class="ifc-symbol"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div><strong>INSTITUTO FEDERAL</strong><span>Catarinense</span></div>
</div>

<div class="cover-slide">
  <h1>Ensino Personalizado de Matemática:<br>Oportunidades e Técnicas Computacionais</h1>
  <div class="cover-credits">
    <strong>Trabalho de Conclusão de Curso (TCC)</strong><br>
    <span class="cover-author">Thales Ferreira Batista<br>Ciência da Computação</span>
    <span class="cover-supervision">Orientador: Prof. Dr. Rafael Zanin<br>Coorientador: Prof. Dr. Manassés Ribeiro<br>Instituto Federal Catarinense - Campus Videira</span>
  </div>
</div>
<div class="cover-snapshot">Snapshot: 03/09/2026 · Data de corte: 31/08/2026</div>

---
layout: default
class: content-slide ptc-challenge-slide
---

<div class="slide-kicker">01 / CONTEXTO</div>

# O desafio fundamental:<br>diagnóstico personalizado com evidências

<div class="ptc-challenge-layout">
  <div class="ptc-challenge-copy">
    <p>Professores de matemática enfrentam uma dificuldade constante: interpretar, em tempo hábil e com precisão, as competências individuais em turmas heterogêneas.</p>
    <p class="ptc-emphasis">O TCC organiza evidências sobre técnicas computacionais que podem apoiar essa interpretação, sem substituir a decisão pedagógica.</p>
  </div>
  <div class="ptc-challenge-list">
    <div class="ptc-challenge-item ptc-blue"><span class="ptc-line-icon">◎</span><p><strong>Turmas heterogêneas:</strong> uma média única não revela trajetórias individuais.</p></div>
    <div class="ptc-challenge-item ptc-amber"><span class="ptc-line-icon">◷</span><p><strong>Tempo docente:</strong> acompanhar evidências compete com o tempo de planejamento.</p></div>
    <div class="ptc-challenge-item ptc-purple"><span class="ptc-line-icon">◈</span><p><strong>Ensino genérico:</strong> uma mesma intervenção pode não atender a necessidades distintas.</p></div>
    <div class="ptc-challenge-item ptc-red"><span class="ptc-line-icon">⌘</span><p><strong>Literatura fragmentada:</strong> aplicações aparecem dispersas entre técnicas e contextos.</p></div>
  </div>
</div>

---
layout: default
class: content-slide ptc-objective-general-slide
---

<div class="slide-kicker">02 / OBJETIVOS</div>

# Objetivo geral

<div class="ptc-objective-layout">
  <div class="ptc-objective-box ptc-action"><span>AÇÃO CENTRAL</span><p>Mapear e analisar sistematicamente aplicações de técnicas computacionais na educação matemática.</p></div>
  <div class="ptc-objective-core">Mapear e analisar sistematicamente as aplicações de técnicas computacionais — especialmente <em>machine learning</em>, <em>learning analytics</em> e sistemas tutores inteligentes — no contexto da educação matemática, identificando tendências, lacunas e oportunidades.</div>
  <div class="ptc-objective-box ptc-impact"><span>IMPACTO (PARA QUÊ?)</span><p>Fundamentar uma especificação conceitual, explicável e orientada ao apoio do professor.</p></div>
  <div class="ptc-objective-box ptc-scope"><span>ESCOPO (O QUÊ?)</span><p>Revisão sistemática da literatura, com síntese de evidências e requisitos; não é protótipo funcional nem avaliação de eficácia.</p></div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">03 / PERGUNTAS</div>

# Quatro perguntas fundamentam a nossa<br>busca por clareza

<div class="rq-grid ptc-question-grid">
  <div class="rq-card rq-blue"><span>01</span><div><div class="ptc-q-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><circle cx="12" cy="14" r="6"/><circle cx="23" cy="11" r="4"/><path d="M7 19c-3 1-4 3-4 6m11-1c1-4 3-6 7-6 4 0 7 2 8 6M17 13l2-2m-3 7 3 1"/></svg></div><strong>Pergunta 1 (O quê?)</strong><p>Quais técnicas computacionais são aplicadas à educação matemática para identificar o estado da arte?</p></div></div>
  <div class="rq-card rq-green"><span>02</span><div><div class="ptc-q-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><circle cx="14" cy="15" r="9"/><path d="M14 10v6l4 3m7-6v10m4-6v6M24 23h7"/><path d="M23 12l2-3 2 2"/></svg></div><strong>Pergunta 2 (Como?)</strong><p>Como essas técnicas têm sido avaliadas em contextos educacionais reais?</p></div></div>
  <div class="rq-card rq-orange"><span>03</span><div><div class="ptc-q-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M5 8h9l3 3 3-3h7v8l-3 3 3 3v6h-8l-3-3-3 3H5v-8l3-3-3-3z"/><path d="M17 11v10m-5-5h10"/></svg></div><strong>Pergunta 3 (O que falta?)</strong><p>Quais lacunas, limitações e desafios precisam ser preenchidos por novas pesquisas?</p></div></div>
  <div class="rq-card rq-red"><span>04</span><div><div class="ptc-q-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="11"/><path d="m16 16 7-6-4 8-7 4zM16 3v3m0 17v3M3 16h3m17 0h3"/></svg></div><strong>Pergunta 4 (E agora?)</strong><p>Quais direcionamentos podemos estabelecer para desenvolver ferramentas alinhadas à realidade?</p></div></div>
</div>

<div class="ptc-caption">Estas quatro perguntas orientam a análise dos achados do TCC.</div>

---
layout: default
class: content-slide ptc-mission-slide
---

<div class="slide-kicker">04 / RIGOR</div>

# Missão: mapear o terreno com rigor e transparência

<div class="ptc-mission-layout">
  <div class="ptc-mission-copy">
    <p>Mapear sistematicamente aplicações de <strong>machine learning</strong>, <strong>learning analytics</strong> e sistemas tutores inteligentes em educação matemática para identificar tendências, lacunas e oportunidades.</p>
    <div class="ptc-reading-lens"><span>LEITURA RESPONSÁVEL</span><strong>Desempenho observado ≠ aprendizagem</strong><p>Saídas computacionais organizam evidências e podem produzir estimativas; não observam sozinhas os processos cognitivos, sociais e afetivos.</p></div>
  </div>
  <div class="ptc-rigor-card">
    <h2>A ferramenta de rigor</h2>
    <div class="ptc-rigor-mark">PRISMA<br><b>2020</b></div>
    <p><span>✓</span> Protocolo explícito para orientar identificação, seleção e relato.</p>
    <p><span>✓</span> Decisões documentadas para favorecer transparência e rastreabilidade.</p>
    <p><span>✓</span> Resultados apresentados com limites, sem ranking ou inferência de eficácia.</p>
  </div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">05 / BASE CONCEITUAL</div>

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
class: content-slide ptc-objectives-slide
---

<div class="slide-kicker">06 / OBJETIVOS ESPECÍFICOS</div>

# Estruturando a execução em 7 objetivos específicos

<div class="ptc-objective-roadmap">
  <svg class="ptc-roadmap-streams" viewBox="0 0 1000 420" preserveAspectRatio="none" aria-hidden="true"><path d="M0 88 C150 20 180 156 330 88 S510 20 660 88 S840 156 1000 88"/><path d="M0 235 C150 170 180 300 330 235 S510 170 660 235 S840 300 1000 235"/><path d="M0 365 C150 300 180 420 330 365 S510 300 660 365 S840 420 1000 365"/></svg>
  <div class="ptc-objective-step"><span>01</span><strong>Revisar</strong><p>Literatura de 2015–2026 conforme o protocolo.</p></div>
  <div class="ptc-objective-step"><span>02</span><strong>Identificar</strong><p>Técnicas computacionais utilizadas.</p></div>
  <div class="ptc-objective-step"><span>03</span><strong>Classificar</strong><p>Finalidades pedagógicas das aplicações.</p></div>
  <div class="ptc-objective-step"><span>04</span><strong>Analisar</strong><p>Metodologias de avaliação e limitações.</p></div>
  <div class="ptc-objective-step"><span>05</span><strong>Mapear</strong><p>Lacunas e desafios reportados.</p></div>
  <div class="ptc-objective-step"><span>06</span><strong>Auditar</strong><p>Pipeline, decisões e artefatos versionados.</p></div>
  <div class="ptc-objective-step"><span>07</span><strong>Derivar</strong><p>Requisitos, avaliação e arquitetura conceitual.</p></div>
</div>

<div class="ptc-caption">Juntos, estes objetivos conectam a busca, a síntese e a especificação do TCC.</div>

---
layout: default
class: content-slide ptc-search-slide
---

<div class="slide-kicker">07 / MÉTODO</div>

# Estratégia de busca: uma rede de captura em 3 camadas

<div class="ptc-search-layout">
  <div class="ptc-search-figure" aria-label="Busca em três camadas: matemática, técnicas e educação">
    <div class="ptc-search-hex ptc-search-outer"><span>EDUCAÇÃO</span><div class="ptc-search-hex ptc-search-middle"><span>TÉCNICAS</span><div class="ptc-search-hex ptc-search-core"><b>MATEMÁTICA</b></div></div></div>
  </div>
  <div class="ptc-query-card"><strong>72 consultas<br>canônicas</strong><p>48 em inglês + 24 em português</p><small>Composição versionada; não é contagem retrospectiva de chamadas HTTP.</small></div>
</div>

<div class="ptc-query-line">Consulta = <b>“matemática”</b> AND <b>“técnica”</b> AND <b>“educação”</b></div>

---
layout: default
class: content-slide ptc-sources-slide
---

<div class="slide-kicker">08 / FONTES</div>

# Quatro fontes de indexação complementares

<div class="ptc-source-grid">
  <div><span class="ptc-source-icon">⌘</span><p><strong>Semantic Scholar</strong><br>Ciência da Computação e métricas de influência.<small>1.931 registros</small></p></div>
  <div><span class="ptc-source-icon">▤</span><p><strong>OpenAlex</strong><br>Cobertura ampla e aberta da literatura.<small>3.057 registros</small></p></div>
  <div><span class="ptc-source-icon">⛓</span><p><strong>Crossref</strong><br>Precisão de metadados e DOIs.<small>5.049 registros</small></p></div>
  <div><span class="ptc-source-icon">⌑</span><p><strong>CORE</strong><br>Foco em artigos e literatura de acesso aberto.<small>1.840 registros</small></p></div>
</div>

<div class="ptc-caption">Teses e dissertações também podem ser aceitas quando atendem aos mesmos critérios de elegibilidade.</div>

---
layout: default
class: content-slide flow-slide
---

<div class="slide-kicker">09 / SELEÇÃO</div>

# O funil da descoberta: de 11.904 registros a 18 estudos retidos

<div class="ptc-funnel-layout">
  <div class="ptc-funnel">
    <div class="ptc-funnel-stage funnel-identification"><span>Identificação</span><strong>11.904</strong><small>registros coletados</small></div>
    <div class="ptc-funnel-stage funnel-dedup"><span>Após identidade</span><strong>11.877</strong><small>27 remoções determinísticas</small></div>
    <div class="ptc-funnel-stage funnel-screening"><span>Triagem</span><strong>2.486</strong><small>9.391 excluídos</small></div>
    <div class="ptc-funnel-stage funnel-inclusion"><span>Retenção</span><strong>18</strong><small>2.468 excluídos na elegibilidade</small></div>
  </div>
  <div class="ptc-funnel-notes">
    <p><strong>Identidade:</strong> 25 DOI + 2 URL são removidos de forma determinística.</p>
    <p><strong>Títulos repetidos:</strong> permanecem como candidatos à auditoria semântica.</p>
    <p><strong>Conjunto retido:</strong> 17 candidatos empíricos provisórios + 1 protocolo contextual.</p>
  </div>
</div>

<div class="ptc-funnel-caption"><strong>Taxa de retenção final: 0,15%.</strong> A baixa retenção descreve o filtro aplicado; não é medida de qualidade nem de eficácia pedagógica.</div>

---
layout: center
class: image-slide ptc-prisma-slide
---

<div class="slide-kicker">10 / FLUXO</div>

<h1 class="sr-only">Fluxo PRISMA dos dados da revisão</h1>

<img src="./public/images/prisma_flow.png" alt="Fluxo PRISMA dos dados da revisão" class="feature-image prisma-image ptc-prisma-image" />

<small class="source-note">Fonte versionada: `research/exports/visualizations/prisma_flow.png`.</small>

---
layout: default
class: content-slide
---

<div class="slide-kicker">11 / DEDUPLICAÇÃO</div>

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

<div class="slide-kicker">12 / PANORAMA</div>

# O volume de registros cresce no recorte observado

<div class="ptc-growth-layout">
  <div class="ptc-growth-chart"><img src="./public/images/papers_by_year.png" alt="Distribuição de registros por ano" /></div>
  <div class="ptc-growth-copy"><h2>Uma literatura em expansão</h2><p>O snapshot reúne registros publicados entre 2015 e 2026. A concentração nos anos mais recentes torna o mapeamento atual e relevante para orientar novas perguntas.</p><small>Leitura descritiva do conjunto coletado; não infere representatividade, causalidade ou qualidade dos estudos.</small></div>
</div>

<div class="ptc-caption">Distribuição anual dos registros no recorte temporal do protocolo.</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">13 / TÉCNICAS</div>

# Técnicas encontradas no conjunto triado

<div class="ptc-technique-layout">
  <div class="ptc-technique-chart"><img src="./public/images/techniques_distribution.png" alt="Distribuição de técnicas nos dados da revisão" /></div>
  <div class="ptc-technique-copy"><div class="ptc-technique-stat"><strong>6.399</strong><span>técnica não especificada</span></div><p>As categorias descrevem os 11.877 registros após remoção determinística. Podem se sobrepor e não representam apenas os 18 retidos.</p><div class="ptc-technique-tags"><span>1.073 assessment</span><span>863 IA</span><span>771 ML</span><span>345 preditiva</span></div></div>
</div>

<div class="ptc-caption">Frequências descritivas: não medem qualidade, eficácia ou predominância entre os estudos incluídos.</div>

---
layout: default
class: content-slide ptc-score-slide
---

<div class="slide-kicker">14 / RELEVÂNCIA</div>

# Um filtro operacional antes da leitura em profundidade

<div class="ptc-score-layout">
  <div class="ptc-score-visual"><img src="./public/images/relevance_distribution.png" alt="Distribuição do score de relevância" /></div>
  <div class="ptc-score-copy">
    <div class="ptc-score-threshold">≥ 4,0</div>
    <h2>O score organiza o processamento.</h2>
    <p>Ele prioriza a leitura dos registros, mas não mede qualidade metodológica, não produz ranking e não substitui a leitura das fontes primárias.</p>
    <div class="ptc-guardrail"><span>!</span><strong>Filtro operacional ≠ conclusão científica</strong></div>
  </div>
</div>

<div class="ptc-caption">A pontuação é uma regra de processamento documentada, não uma conclusão sobre os estudos.</div>

---
layout: default
class: content-slide ptc-retained-slide
---

<div class="slide-kicker">15 / RETENÇÃO</div>

# População retida: dois estratos de leitura

<div class="ptc-retained-layout">
  <div class="ptc-retained-number"><strong>18</strong><span>registros retidos<br>na revisão</span><div class="ptc-retained-rule"></div><p>O conjunto final não é homogêneo.</p></div>
  <div class="ptc-retained-copy">
    <div class="ptc-retained-strata"><strong>17</strong><span>candidatos empíricos provisórios</span><strong>+</strong><strong>1</strong><span>protocolo contextual</span></div>
    <h2>Dois estratos de leitura</h2>
    <p>Os candidatos empíricos sustentam a síntese. O protocolo contextual permanece para rastreabilidade, sem resultado empírico.</p>
    <div class="ptc-guardrail"><span>↗</span><strong>Retenção operacional ≠ evidência homogênea</strong></div>
  </div>
</div>

<div class="ptc-caption">A separação preserva a rastreabilidade sem apresentar o protocolo como evidência de eficácia.</div>

---
layout: default
class: content-slide ptc-mmat-slide
---

<div class="slide-kicker">16 / MMAT</div>

# Nosso filtro de qualidade: critérios, não uma nota global

<div class="ptc-mmat-layout">
  <div class="ptc-mmat-visual" aria-hidden="true"><div class="ptc-mmat-scale">⚖</div><span>MMAT 2018</span><small>leitura por critério</small></div>
  <div class="ptc-mmat-copy">
    <h2>Apreciação por critério</h2>
    <p>As respostas são registradas como <b>Sim</b>, <b>Não</b> ou <b>Não é possível determinar</b>, conforme o desenho de cada estudo.</p>
    <div class="ptc-mmat-key">
      <div><b>S</b><span><strong>Sim</strong> critério atendido segundo a evidência disponível.</span></div>
      <div><b>N</b><span><strong>Não</strong> critério não atendido na apreciação documental.</span></div>
      <div><b>ND</b><span><strong>Indeterminado</strong> informação insuficiente para concluir.</span></div>
    </div>
  </div>
</div>

<div class="ptc-mmat-result"><strong>Estado da apreciação:</strong> nove registros tiveram texto primário revisado e oito foram apreciados com resumo/metadados. A leitura foi conduzida por um único revisor; recuperação de fontes, localizadores e adjudicação ainda precisam ser consolidados.</div>

---
layout: default
class: content-slide ptc-synthesis-slide
---

<div class="slide-kicker">17 / SÍNTESE</div>

# O que emerge entre os candidatos empíricos

<div class="ptc-synthesis-layout">
  <div class="ptc-synthesis-orbit" aria-label="Relação entre desempenho, proficiência e modelagem"><div class="ptc-orbit-ring ring-one"></div><div class="ptc-orbit-ring ring-two"></div><div class="ptc-orbit-ring ring-three"></div><strong>17</strong><span>candidatos<br>empíricos</span><i>evidências<br>relacionadas</i></div>
  <div class="ptc-synthesis-copy">
    <h2>Predição e estimativa aparecem como eixo recorrente.</h2>
    <p>Os estudos organizam evidências de desempenho e inferem proficiência a partir de registros observados, frequentemente com modelos supervisionados.</p>
    <div class="ptc-synthesis-points"><div><b>01</b><span><strong>Finalidade</strong> reconhecer padrões em registros de avaliação.</span></div><div><b>02</b><span><strong>Modelos</strong> RF, SVM e redes neurais aparecem como alternativas.</span></div><div><b>03</b><span><strong>Limite</strong> populações, instrumentos e métricas variam entre estudos.</span></div></div>
  </div>
</div>

<div class="ptc-caption">A síntese organiza o estado da literatura; não estabelece ranking de modelos nem eficácia pedagógica geral.</div>

---
layout: default
class: content-slide ptc-boundary-slide
---

<div class="slide-kicker">18 / INTERPRETAÇÃO</div>

# O que podemos concluir — e o que permanece aberto

<div class="ptc-boundary-layout">
  <div class="ptc-boundary-column boundary-yes"><div class="ptc-boundary-mark">✓</div><span>O TCC ENTREGA</span><h2>Um mapa auditável</h2><p>Aplicações encontradas, etapas de seleção, síntese interpretativa e lacunas documentadas.</p></div>
  <div class="ptc-boundary-divider"></div>
  <div class="ptc-boundary-column boundary-no"><div class="ptc-boundary-mark">?</div><span>O TCC NÃO ENTREGA</span><h2>Eficácia geral</h2><p>Não há base para afirmar superioridade entre modelos ou protótipo validado em escolas.</p></div>
</div>

<div class="ptc-boundary-foot"><strong>Leitura obrigatória:</strong> resultados individuais exigem população, instrumento, métrica e desenho de avaliação nas fontes primárias.</div>

---
layout: default
class: content-slide ptc-gaps-slide
---

<div class="slide-kicker">19 / LACUNAS</div>

# As lacunas que orientam a especificação

<p class="ptc-gaps-intro">Seis lacunas documentadas são agrupadas em quatro eixos para conduzir a próxima decisão científica.</p>
<div class="ptc-gaps-grid">
  <div><b>1</b><h2>Explicabilidade</h2><p>Resultados compreensíveis, com incerteza e participação docente.</p></div>
  <div><b>2</b><h2>Contexto curricular</h2><p>Indicadores relacionados a objetivos e descritores matemáticos.</p></div>
  <div><b>3</b><h2>Validação real</h2><p>População, ambiente educacional e equidade precisam ser investigados.</p></div>
  <div><b>4</b><h2>Reprodutibilidade</h2><p>Dados, código, parâmetros e decisões permanecem rastreáveis.</p></div>
</div>

<div class="ptc-gaps-foot"><strong>Como a revisão usa essas lacunas:</strong> elas orientam requisitos da especificação; não são apresentadas como prova de que uma solução futura será eficaz.</div>

---
layout: default
class: content-slide ptc-specification-slide
---

<div class="slide-kicker">20 / ESPECIFICAÇÃO</div>

# Da evidência à especificação — sem saltar para a implementação

<div class="ptc-spec-layout">
  <div class="ptc-spec-path"><div><b>01</b><strong>Evidências</strong><span>literatura + fundamentação</span></div><i>→</i><div><b>02</b><strong>Lacunas</strong><span>riscos e necessidades</span></div><i>→</i><div><b>03</b><strong>Requisitos</strong><span>funções e restrições</span></div></div>
  <div class="ptc-spec-delivery"><div class="ptc-paper-icon">▤</div><h2>Entrega do TCC</h2><p>Uma especificação técnica e pedagógica auditável, com protocolo e arquitetura de referência.</p><small>Não é aplicação funcional, não usa base definitiva e não possui validação com participantes.</small></div>
</div>

<div class="ptc-spec-caption">A evidência orienta requisitos; os requisitos orientam um futuro protocolo de avaliação.</div>

---
layout: default
class: content-slide ptc-architecture-slide
---

<div class="slide-kicker">21 / ARQUITETURA</div>

# Arquitetura de referência: da fonte à decisão docente

<div class="ptc-architecture-layout">
  <div class="ptc-architecture-path"><div class="arch-node arch-data"><b>01</b><strong>Ingestão</strong><span>fontes</span></div><i>→</i><div class="arch-node arch-prep"><b>02</b><strong>Preparação</strong><span>dados documentados</span></div><i>→</i><div class="arch-node arch-model"><b>03</b><strong>Modelagem</strong><span>modelos candidatos</span></div><i>→</i><div class="arch-node arch-eval"><b>04</b><strong>Avaliação</strong><span>métricas e explicações</span></div><i>→</i><div class="arch-node arch-present"><b>05</b><strong>Apresentação</strong><span>decisão docente</span></div></div>
  <div class="ptc-architecture-copy"><h2>Componentes separáveis</h2><p>A separação favorece testabilidade, rastreabilidade e substituição controlada de técnicas.</p><div class="ptc-architecture-note">A arquitetura é uma referência conceitual do TCC, não a descrição de um sistema implementado.</div></div>
</div>

<div class="ptc-caption">A apresentação finaliza no apoio à análise docente; não automatiza a decisão pedagógica.</div>

---
layout: default
class: content-slide ptc-open-slide
---

<div class="slide-kicker">22 / REPRODUTIBILIDADE</div>

# Ciência aberta como trilha de auditoria

<div class="ptc-open-layout">
  <div class="ptc-open-visual"><div class="ptc-open-center">TCC</div><div class="ptc-open-artifact artifact-csv">CSV<br><small>dados</small></div><div class="ptc-open-artifact artifact-bib">BibTeX<br><small>fontes</small></div><div class="ptc-open-artifact artifact-manifest">#<br><small>hashes</small></div><div class="ptc-open-artifact artifact-report">PNG / HTML<br><small>relatórios</small></div></div>
  <div class="ptc-open-copy"><h2>Reprodutibilidade sem distribuir o SQLite</h2><p>A trilha pública reúne dados derivados, referências e artefatos versionados, preservando a separação entre a bibliografia do pipeline e as referências teóricas do TCC.</p><div class="ptc-paths"><code>research/exports/analysis/papers.csv</code><code>research/exports/reports/summary.json</code><code>research/exports/reports/reproducibility_manifest.json</code></div></div>
</div>

<div class="ptc-caption">Referências teóricas, pedagógicas, metodológicas e técnicas permanecem separadas das referências derivadas do pipeline.</div>

---
layout: default
class: content-slide ptc-next-slide
---

<div class="slide-kicker">23 / CONTINUIDADE</div>

# Próximos passos científicos

<div class="ptc-next-layout">
  <div class="ptc-next-list"><div><b>01</b><span>Consolidar recuperação das fontes e adjudicação final do MMAT.</span></div><div><b>02</b><span>Revisar lacunas à luz dos 17 estudos empíricos provisórios.</span></div><div><b>03</b><span>Revisar a especificação conceitual à luz da adjudicação final.</span></div><div><b>04</b><span>Qualquer validação experimental exigirá novo protocolo e autorização.</span></div></div>
  <div class="ptc-next-decision"><span>PRÓXIMA DECISÃO</span><strong>evidência<br>antes da<br>implementação</strong><i>→</i></div>
</div>

<div class="ptc-caption">A revisão sistemática fundamenta próximas decisões; não substitui o protocolo do experimento.</div>

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
