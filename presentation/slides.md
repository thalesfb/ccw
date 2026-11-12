---
theme: default
layout: default
class: cover-page
colorSchema: light
fonts:
  sans: Times New Roman
  serif: Times New Roman
  provider: none
title: "Ensino Personalizado de Matemática"
info: "Defesa do TCC — revisão sistemática e especificação de protótipo"
author: "Thales Ferreira Batista"
keywords: "TCC, ensino personalizado, matemática, revisão sistemática, PRISMA, especificação"
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

<div class="cover-art cover-art-top-left" aria-hidden="true">∫ f(x) · dx = e<sup>nt</sup> = g(x)<br>f(x) = ∫ f′(x) dx</div>
<div class="cover-art cover-art-top" aria-hidden="true">∂² / ∂x² &nbsp;&nbsp; lim Δx→0</div>
<div class="cover-art cover-art-top-right" aria-hidden="true">P = {2, 1, 3} &nbsp; M = [a<sub>ij</sub>]<br>A = [a₁&nbsp; a₂&nbsp; a₃]</div>
<div class="cover-art cover-art-left" aria-hidden="true">x − z<br>────── · dx<br>2πr + 1</div>
<div class="cover-art cover-art-right" aria-hidden="true">A = [a₁&nbsp; a₂&nbsp; a₃]<br>△ ABC &nbsp;&nbsp; ∂f / ∂x</div>
<div class="cover-art cover-art-bottom-left" aria-hidden="true">R₀ = hθ<sup>2</sup> / 2<br>y = (x − 1)²</div>
<div class="cover-art cover-art-bottom" aria-hidden="true">∫∫ R f(x,y) dA</div>
<div class="cover-art cover-art-bottom-right" aria-hidden="true">n = −√(a²x²)<br>sin(x) = Δπ / n</div>

<div class="ifc-mark" aria-label="Instituto Federal Catarinense — Campus Videira">
  <img class="ifc-logo" src="/branding/ifc-campus-videira-horizontal.png" alt="Instituto Federal Catarinense — Campus Videira">
</div>

<div class="cover-slide">
  <h1>Ensino Personalizado de Matemática:<br>Oportunidades e Técnicas Computacionais</h1>
  <div class="cover-credits">
    <strong>Trabalho de Conclusão de Curso (TCC)</strong><br>
    <span class="cover-author">Thales Ferreira Batista<br>Ciência da Computação</span>
    <span class="cover-supervision">Orientador: Prof. Dr. Rafael Zanin<br>Coorientador: Prof. Dr. Manassés Ribeiro<br>Instituto Federal Catarinense - Campus Videira</span>
  </div>
</div>
<div class="cover-snapshot">Versão para a defesa · apreciação MMAT preliminar · busca até 31/08/2026 · fluxo reconciliado em 31/10/2026; seleção histórica sob o corte 4,0</div>

---
layout: default
class: content-slide tcc-challenge-slide
---

<div class="slide-kicker">01 / CONTEXTO</div>

# O problema: ler a aprendizagem<br>em turmas heterogêneas

<div class="tcc-challenge-layout">
  <div class="tcc-challenge-copy">
    <p>A média da turma não mostra onde cada estudante está, nem quanta evidência sustenta essa leitura.</p>
    <p class="tcc-emphasis">Técnicas computacionais podem organizar essas evidências, desde que o professor continue responsável pela interpretação.</p>
  </div>
  <div class="tcc-challenge-list">
    <div class="tcc-challenge-item tcc-blue"><span class="tcc-line-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><circle cx="11" cy="11" r="3.6"/><circle cx="21" cy="12" r="3"/><path d="M4.5 25c.8-4.1 3.1-6.2 6.5-6.2s5.7 2.1 6.5 6.2M17 20c.9-2.3 2.7-3.6 5.1-3.6 2.5 0 4.4 1.5 5.3 4.4"/></svg></span><p><strong>Turmas heterogêneas:</strong> a média esconde percursos individuais.</p></div>
    <div class="tcc-challenge-item tcc-amber"><span class="tcc-line-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="11"/><path d="M16 9v7l4.8 3M6.5 6.5l2.4 2.4m14.2-2.4-2.4 2.4"/></svg></span><p><strong>Tempo docente:</strong> analisar registros disputa espaço com o planejamento.</p></div>
    <div class="tcc-challenge-item tcc-purple"><span class="tcc-line-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="m4 10 12-6 12 6-12 6zM4 16l12 6 12-6M4 22l12 6 12-6"/></svg></span><p><strong>Ensino uniforme:</strong> a mesma intervenção não atende necessidades distintas.</p></div>
    <div class="tcc-challenge-item tcc-red"><span class="tcc-line-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M6 5h13a4 4 0 0 1 4 4v18H10a4 4 0 0 0-4 4zM23 27h3a2 2 0 0 0 2-2V9a4 4 0 0 0-4-4"/><path d="M10 11h8m-8 5h8m-8 5h5"/></svg></span><p><strong>Literatura dispersa:</strong> técnicas, alvos e contextos variam entre os estudos.</p></div>
  </div>
</div>

---
layout: default
class: content-slide tcc-objective-general-slide
---

<div class="slide-kicker">02 / OBJETIVO GERAL</div>

# O que o trabalho propõe

<div class="tcc-objective-layout">
  <div class="tcc-objective-box tcc-action"><span>OBJETO</span><p>Técnicas computacionais aplicadas à educação matemática, 2015–2026.</p></div>
  <div class="tcc-objective-core">Propor uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática, fundamentada no mapeamento e na análise da literatura científica.</div>
  <div class="tcc-objective-box tcc-impact"><span>PARA QUÊ</span><p>Oferecer ao professor indícios de desempenho e de incerteza por habilidade, sem substituir seu julgamento.</p></div>
  <div class="tcc-objective-box tcc-scope"><span>ESCOPO</span><p>Revisão sistemática e especificação documental. Não inclui protótipo validado nem avaliação de eficácia.</p></div>
</div>

---
layout: default
class: content-slide tcc-problem-slide
---

<div class="slide-kicker">03 / PROBLEMA DE PESQUISA</div>

# Como estruturar a especificação a partir da literatura?

<p class="tcc-problem-statement">Como estruturar uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática a partir das evidências e técnicas computacionais identificadas na literatura?</p>

<div class="rq-grid tcc-question-grid">
  <div class="rq-card rq-blue"><span>01</span><div><div class="tcc-q-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><circle cx="13" cy="13" r="7"/><path d="m18.5 18.5 7 7M10 13h6m-3-3v6"/></svg></div><strong>O que a literatura faz? <em>OE1</em></strong><p>Técnicas e finalidades pedagógicas nos estudos selecionados.</p></div></div>
  <div class="rq-card rq-green"><span>02</span><div><div class="tcc-q-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="m16 4 13 24H3z"/><path d="M16 11v8m0 5h.01"/></svg></div><strong>O que falta nos relatos? <em>OE2</em></strong><p>Limitações metodológicas e de relato; dimensões técnica, pedagógica e ética.</p></div></div>
  <div class="rq-card rq-orange"><span>03</span><div><div class="tcc-q-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M5 25h22M7 22V9m0 13 6-7 5 4 7-10"/><path d="m22 8 3-1v3"/></svg></div><strong>Como especificar? <em>OE3</em></strong><p>Requisitos, critérios de dados e modelos e arquitetura de referência.</p></div></div>
  <div class="rq-card rq-red"><span>04</span><div><div class="tcc-q-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="11"/><path d="m16 16 7-6-4 8-7 4zM16 3v3m0 17v3M3 16h3m17 0h3"/></svg></div><strong>Como avaliar a proposta? <em>OE4</em></strong><p>Protocolo para examinar viabilidade e coerência antes de qualquer uso.</p></div></div>
</div>

---
layout: default
class: content-slide
---

<div class="slide-kicker">04 / BASE CONCEITUAL</div>

# Cinco níveis que uma saída não deve confundir

<div class="interpretation-ladder">
  <div class="interpretation-level level-blue"><b>01</b><strong>Desempenho observado</strong><span>Acertos, notas, tentativas, estratégias ou tempo registrados em uma tarefa.</span></div>
  <div class="interpretation-level level-purple"><b>02</b><strong>Probabilidade preditiva</strong><span>Saída de um modelo, para um alvo definido e com os dados usados; não é proficiência.</span></div>
  <div class="interpretation-level level-green"><b>03</b><strong>Proficiência estimada</strong><span>Posição em uma escala; exige modelo de mensuração e evidência de validade.</span></div>
  <div class="interpretation-level level-orange"><b>04</b><strong>Competência</strong><span>Mobilização de conhecimentos, habilidades, atitudes e valores diante de demandas.</span></div>
  <div class="interpretation-level level-red"><b>05</b><strong>Aprendizagem</strong><span>Neste TCC: mudanças no que o estudante sabe e consegue fazer ao longo do tempo.</span></div>
</div>

<div class="concept-note"><strong>Regra de leitura:</strong> uma saída computacional organiza evidências e produz estimativas; sozinha, não observa os processos cognitivos, sociais e afetivos da aprendizagem nem demonstra eficácia pedagógica.</div>

<div class="tcc-caption">Elaboração do autor com base em National Research Council (2001), pp. 42–44, OECD (2023) e Brasil / BNCC (2018); não é uma escala validada.</div>

---
layout: default
class: content-slide tcc-mission-slide
---

<div class="slide-kicker">05 / DIDÁTICA DA MATEMÁTICA</div>

# Acertar ou errar não revela o tipo de erro

<div class="tcc-mission-layout">
  <div class="tcc-mission-copy">
    <p><strong>Duval (2012):</strong> compreender exige coordenar ao menos dois registros de representação, como língua natural, escrita simbólica, figura e gráfico.</p>
    <p><strong>Brousseau (1989):</strong> o erro pode manifestar um obstáculo, e não apenas a falta de um saber.</p>
    <div class="tcc-reading-lens"><span>EXEMPLO DO 7º ANO</span><strong>“O dobro da quantia de Carlos somado a R$ 5,00 resulta em R$ 15,00”</strong><p>Errar a conversão para <em>2x + 5 = 15</em> ou errar ao isolar <em>x</em> são erros distintos, mas ambos viram o mesmo 0 em um registro binário.</p></div>
  </div>
  <div class="tcc-rigor-card">
    <h2>Consequência para a especificação</h2>
    <div class="tcc-rigor-mark">0 / 1<br><b>≠ diagnóstico</b></div>
    <p><span>✓</span> As saídas organizam indícios por habilidade, com incerteza.</p>
    <p><span>✓</span> O tipo de erro e o obstáculo ficam com o professor, na revisão docente (F06).</p>
    <p><span>✓</span> Codificar itens por registro de representação é trabalho futuro.</p>
    <small>Fundamentação: Duval (2012); Brousseau (1989).</small>
  </div>
</div>

---
layout: default
class: content-slide tcc-objectives-slide
---

<div class="slide-kicker">06 / OBJETIVOS ESPECÍFICOS</div>

# Quatro objetivos, quatro produtos

<div class="tcc-objective-roadmap">
  <div class="tcc-objective-step"><span>01</span><strong>Categorizar</strong><p>Técnicas e finalidades pedagógicas na literatura mapeada.</p><em>→ tipologia de finalidades dos 15 estudos</em></div>
  <div class="tcc-objective-step"><span>02</span><strong>Identificar limites</strong><p>Codificação sistemática de limitações metodológicas e de relato; discussão dos eixos técnico, pedagógico e ético.</p><em>→ lacunas de relato pelo MMAT</em></div>
  <div class="tcc-objective-step"><span>03</span><strong>Formular a especificação</strong><p>Requisitos, critérios de dados e modelos e arquitetura de referência.</p><em>→ 26 grupos de requisitos e regra de modelo</em></div>
  <div class="tcc-objective-step"><span>04</span><strong>Propor o protocolo</strong><p>Avaliar viabilidade e coerência da especificação, com fundamentos, requisitos e condições de execução.</p><em>→ regra docente e conferência técnica</em></div>
</div>

<div class="tcc-caption">Meios: revisão de 2015–2026 relatada com o PRISMA 2020, apreciação MMAT preliminar e pipeline versionado. O protocolo está proposto; sua aplicação está pendente.</div>

---
layout: default
class: content-slide tcc-search-slide
---

<div class="slide-kicker">07 / MÉTODO</div>

# Revisão sistemática: busca em três camadas

<div class="tcc-search-layout">
  <div class="tcc-search-figure" aria-label="Busca em três camadas: matemática, técnicas e educação">
    <div class="tcc-search-hex tcc-search-outer"><span>EDUCAÇÃO</span><div class="tcc-search-hex tcc-search-middle"><span>TÉCNICAS</span><div class="tcc-search-hex tcc-search-core"><b>MATEMÁTICA</b></div></div></div>
  </div>
  <div class="tcc-query-card"><strong>72 consultas<br>canônicas</strong><p>48 em inglês + 24 em português</p><small>Quatro bases, 2015–2026, busca até 31/08/2026.</small></div>
</div>

<div class="tcc-method-strip"><span><b>Relato</b> PRISMA 2020 — Page et al. (2021)</span><span><b>Qualidade</b> MMAT 2018 — Hong et al. (2018)</span><span><b>Consulta</b> “matemática” AND “técnica” AND “educação”</span></div>

---
layout: default
class: content-slide tcc-sources-slide
---

<div class="slide-kicker">08 / FONTES</div>

# Quatro bases de indexação complementares

<div class="tcc-source-grid">
  <div><span class="tcc-source-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><circle cx="8" cy="16" r="3"/><circle cx="24" cy="9" r="3"/><circle cx="24" cy="23" r="3"/><path d="m10.8 14.8 10.4-4.6m-10.4 7 10.4 4.6"/></svg></span><p><strong>Semantic Scholar</strong><br>Computação e métricas de influência.<small>1.931 registros</small></p></div>
  <div><span class="tcc-source-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><ellipse cx="16" cy="8" rx="10" ry="4"/><path d="M6 8v14c0 2.2 4.5 4 10 4s10-1.8 10-4V8M6 15c0 2.2 4.5 4 10 4s10-1.8 10-4"/></svg></span><p><strong>OpenAlex</strong><br>Cobertura ampla e aberta.<small>3.057 registros</small></p></div>
  <div><span class="tcc-source-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M12 20 9 23a5 5 0 0 1-7-7l4-4a5 5 0 0 1 7 0m7-4 3-3a5 5 0 0 1 7 7l-4 4a5 5 0 0 1-7 0M11 21l10-10"/></svg></span><p><strong>Crossref</strong><br>Metadados e DOIs.<small>5.049 registros</small></p></div>
  <div><span class="tcc-source-icon" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M4 7h9a4 4 0 0 1 3 1.4A4 4 0 0 1 19 7h9v19h-9a4 4 0 0 0-3 1.4 4 4 0 0 0-3-1.4H4zM16 9v18"/><path d="M8 12h5m-5 4h5m6-4h5m-5 4h5"/></svg></span><p><strong>CORE</strong><br>Literatura de acesso aberto.<small>1.838 registros</small></p></div>
</div>

<div class="tcc-caption">11.875 registros após a remoção histórica de 29 duplicatas (27 por DOI/URL e 2 confirmadas manualmente). A base indicada é a origem da versão mantida; não mede cobertura exclusiva. Teses e dissertações também podiam ser elegíveis.</div>

---
layout: default
class: content-slide flow-slide
---

<div class="slide-kicker">09 / SELEÇÃO</div>

# Fluxo da seleção histórica sob corte 4,0: 11.904 registros → 18 na lista de leitura

<div class="tcc-funnel-layout">
  <div class="tcc-funnel">
    <div class="tcc-funnel-stage funnel-identification"><span>Identificação</span><strong>11.904</strong><small>registros coletados</small></div>
    <div class="tcc-funnel-stage funnel-dedup"><span>Após deduplicação</span><strong>11.875</strong><small>29 duplicatas removidas</small></div>
    <div class="tcc-funnel-stage funnel-screening"><span>Após triagem</span><strong>2.482</strong><small>9.393 excluídos</small></div>
    <div class="tcc-funnel-stage funnel-inclusion"><span>Lista de leitura</span><strong>18</strong><small>2.464 abaixo do corte ou fora do escopo</small></div>
  </div>
  <div class="tcc-funnel-notes">
    <p><strong>Triagem:</strong> critérios automatizados de escopo, resumo e termos metodológicos.</p>
    <p><strong>Priorização:</strong> escore de relevância com corte 4,0; não equivale a elegibilidade.</p>
    <p><strong>Resultado:</strong> 15 estudos empíricos, 14 com texto recuperado; Sokkhey permanece sem cópia verificável.</p>
  </div>
</div>

<div class="tcc-funnel-caption"><strong>Seleção relatada com referência ao PRISMA 2020.</strong> Após uma exclusão após resumo, dos 17 relatórios procurados, dois não foram recuperados (Sokkhey e Zeng) e 15 foram avaliados em texto completo; um protocolo foi excluído e 14 relatórios empíricos foram recuperados.</div>

---
layout: center
class: image-slide tcc-prisma-slide
---

<div class="slide-kicker">10 / FLUXO PRISMA</div>

<h1 class="sr-only">Representação operacional do processo de seleção, com referência ao PRISMA 2020</h1>

<img src="/images/prisma_flow.png" alt="Representação operacional do processo de seleção; não corresponde ao diagrama PRISMA completo" class="feature-image prisma-image tcc-prisma-image" />

<small class="source-note">Fluxograma 1 do TCC. Fonte versionada: <code>research/exports/visualizations/prisma_flow.png</code>.</small>

---
layout: default
class: content-slide tcc-score-slide
---

<div class="slide-kicker">11 / CORTE DE RELEVÂNCIA</div>

# O corte 4,0 é heurístico: havia elegíveis abaixo dele

<div class="tcc-score-layout">
  <div class="tcc-sensitivity" aria-label="Exploração abaixo do corte 4,0 em três estratos">
    <div class="tcc-sensitivity-row"><span>3,75–3,95<small>censo</small></span><div class="tcc-sensitivity-bar"><i style="width: 28.9%"></i></div><b>13 de 45</b></div>
    <div class="tcc-sensitivity-row"><span>3,50–3,74<small>seleção dirigida</small></span><div class="tcc-sensitivity-bar"><i style="width: 53.7%"></i></div><b>29 de 54</b></div>
    <div class="tcc-sensitivity-row"><span>3,00–3,49<small>amostra estratificada</small></span><div class="tcc-sensitivity-bar"><i style="width: 16.7%"></i></div><b>5 de 30</b></div>
    <p class="tcc-sensitivity-note">Registros classificados como elegíveis em cada estrato explorado.</p>
  </div>
  <div class="tcc-score-copy">
    <div class="tcc-score-threshold">4,0</div>
    <h2>Recorte, não censo da literatura.</h2>
    <p>O corte priorizou a leitura e foi mantido. A exploração mostra que ele deixou estudos elegíveis de fora.</p>
    <div class="tcc-guardrail"><span>!</span><strong>Limitação declarada, sem estimativa de perda</strong></div>
  </div>
</div>

<div class="tcc-caption">Os estratos usam desenhos amostrais diferentes; as frações não se somam nem estimam a perda total. O escore não mede qualidade metodológica.</div>

---
layout: default
class: content-slide tcc-retained-slide
---

<div class="slide-kicker">12 / LISTA DE LEITURA</div>

# O destino dos 18 registros

<div class="tcc-retained-layout">
  <div class="tcc-retained-number"><strong>18</strong><span>registros da<br>lista de leitura</span><div class="tcc-retained-rule"></div><p>Lista de leitura não é inclusão final.</p></div>
  <div class="tcc-retained-copy">
    <div class="tcc-retained-strata" aria-label="Quatro destinos históricos dos 18 registros: 15 estudos, um relatório Zeng, uma exclusão após resumo e um protocolo"><strong>15</strong><span>estudos empíricos da seleção histórica, incluindo Sokkhey sem cópia verificável</span><strong>1</strong><span>relatório Zeng não recuperado, fora dos 15</span><strong>1</strong><span>exclusão após resumo</span><strong>1</strong><span>protocolo excluído após texto completo</span></div>
    <h2>Desfechos da seleção</h2>
    <p>Dos 17 relatórios procurados, 15 foram avaliados em texto completo. Sokkhey permanece na seleção histórica sem cópia verificável; Zeng não recebeu MMAT.</p>
    <div class="tcc-guardrail"><span>↗</span><strong>Estudos retidos ≠ evidência homogênea</strong></div>
  </div>
</div>

---
layout: default
class: content-slide tcc-mmat-slide
---

<div class="slide-kicker">13 / QUALIDADE METODOLÓGICA</div>

# MMAT preliminar: critério a critério, sem nota global

<div class="tcc-mmat-layout">
  <div class="tcc-mmat-visual" aria-hidden="true"><div class="tcc-mmat-scale">⚖</div><span>MMAT 2018</span><small>leitura por critério</small></div>
  <div class="tcc-mmat-copy">
    <h2>Duas perguntas de triagem, depois os critérios da categoria</h2>
    <div class="tcc-mmat-screening" aria-label="Perguntas de triagem do MMAT 2018">
      <div><b>S1</b><span>Há perguntas de pesquisa claras?</span></div>
      <div><b>S2</b><span>Os dados coletados permitem responder às perguntas de pesquisa?</span></div>
    </div>
    <div class="tcc-mmat-key">
      <div><b>Y</b><span><strong>Y = Sim</strong> critério atendido segundo a evidência disponível.</span></div>
      <div><b>N</b><span><strong>N = Não</strong> critério não atendido na apreciação documental.</span></div>
      <div><b>CT</b><span><strong>CT = Não é possível concluir</strong> informação insuficiente para concluir.</span></div>
    </div>
  </div>
</div>

<div class="tcc-mmat-result"><strong>Estado preliminar:</strong> 15 registros provisórios, com S1/S2 e critérios da categoria; S2: 14 respostas Y e 1 CT no estudo 5, porque a origem dos dados não foi confirmada. Estudos 5 e 7: categoria 3 operacional, alocação desconhecida. Estudo 14: categoria 2 declarada e contraditória. Estudo 8: categoria 4 adaptada para modelagem. Texto não recuperado: sem apreciação. Sem escore agregado. Instrumento: Hong et al. (2018); respostas produzidas por IA e em conferência pelo autor.</div>

---
layout: default
class: content-slide tcc-typology-slide
---

<div class="slide-kicker">14 / RESULTADO — OE1</div>

# Para que as técnicas são usadas nos 15 estudos

<div class="tcc-typology-layout">
  <div class="tcc-typology-bars" aria-label="Finalidade principal dos 15 estudos">
    <div class="tcc-typology-row"><span>Predição/classificação</span><div><i style="width: 100%"></i><b>8</b></div><small>árvores de decisão, Random Forest, SVM, redes neurais, regressão logística, Naive Bayes</small></div>
    <div class="tcc-typology-row"><span>Personalização ou STI</span><div><i style="width: 37.5%"></i><b>3</b></div><small>grafos de conhecimento, redes profundas, aprendizagem por reforço</small></div>
    <div class="tcc-typology-row"><span>Intervenção didática</span><div><i style="width: 25%"></i><b>2</b></div><small>animação com aprendizagem cooperativa; GeoGebra</small></div>
    <div class="tcc-typology-row"><span>Modelagem cognitiva</span><div><i style="width: 12.5%"></i><b>1</b></div><small>agentes simulados de aprendizagem (Apprentice Learner)</small></div>
    <div class="tcc-typology-row"><span>Integração curricular</span><div><i style="width: 12.5%"></i><b>1</b></div><small>análise de Fourier e PCA em contexto aplicado</small></div>
  </div>
  <div class="tcc-typology-copy">
    <h2>Predição domina; a finalidade pedagógica aparece indiretamente.</h2>
    <p>Nos estudos de predição, a finalidade pedagógica só aparece pelo alvo previsto, como nota ou desempenho posterior.</p>
    <div class="tcc-guardrail"><span>!</span><strong>Categorias não homogêneas: uma é tarefa computacional; quatro são finalidades de uso</strong></div>
  </div>
</div>

<div class="tcc-caption">Uma finalidade principal por estudo, sem dupla contagem (Tabela 2 e Quadro 4 do TCC). Frequências descrevem o recorte; não indicam eficácia nem predominância na literatura.</div>

---
layout: default
class: content-slide tcc-reporting-slide
---

<div class="slide-kicker">15 / RESULTADO — OE2</div>

# O que falta nos relatos: a resposta mais comum é “não é possível concluir”

<div class="tcc-reporting-layout">
  <div class="tcc-ct-grid" role="table" aria-label="Respostas CT por categoria MMAT e critério">
    <div class="tcc-ct-head" role="row"><span role="columnheader">Categoria (n)</span><span role="columnheader">Q1</span><span role="columnheader">Q2</span><span role="columnheader">Q3</span><span role="columnheader">Q4</span><span role="columnheader">Q5</span></div>
    <div role="row"><span role="rowheader">Quantitativo descritivo (8)</span><b class="ct-mid" role="cell">3</b><b class="ct-all" role="cell">8</b><b class="ct-all" role="cell">8</b><b class="ct-all" role="cell">8</b><b class="ct-high" role="cell">6</b></div>
    <div role="row"><span role="rowheader">Não randomizado (3)</span><b class="ct-all" role="cell">3</b><b class="ct-high" role="cell">2</b><b class="ct-all" role="cell">3</b><b class="ct-high" role="cell">2</b><b class="ct-high" role="cell">2</b></div>
    <div role="row"><span role="rowheader">Randomizado (1)</span><b class="ct-all" role="cell">1</b><b class="ct-none" role="cell">0</b><b class="ct-none" role="cell">0</b><b class="ct-all" role="cell">1</b><b class="ct-all" role="cell">1</b></div>
    <div role="row"><span role="rowheader">Métodos mistos (3)</span><b class="ct-none" role="cell">0</b><b class="ct-none" role="cell">0</b><b class="ct-mid" role="cell">1</b><b class="ct-mid" role="cell">1</b><b class="ct-mid" role="cell">1</b></div>
    <p class="tcc-ct-note">Número de respostas CT em cada critério. Q1–Q5 seguem a rubrica de cada categoria.</p>
  </div>
  <div class="tcc-reporting-copy">
    <h2>Falta informação, mais do que falha demonstrada.</h2>
    <p>CT predomina em representatividade, medidas, completude, controle e análise.</p>
    <p><strong>Consequência:</strong> a especificação exige descrever alvo, população, transformações dos dados e forma de avaliação.</p>
  </div>
</div>

<div class="tcc-caption">Tabela 3 do TCC. Apreciação preliminar, assistida por IA e em conferência pelo autor; respostas não somadas em escore.</div>

---
layout: default
class: content-slide tcc-axes-slide
---

<div class="slide-kicker">16 / RESULTADO — OE2</div>

# Três eixos de risco viraram requisitos

<div class="tcc-axes-grid">
  <div class="tcc-axis axis-tech"><span>TÉCNICO</span><h2>Validar sem vazar informação</h2><p>Separar treino, validação e teste por estudante; examinar calibração e não só acurácia.</p><b>→ R20, F03</b></div>
  <div class="tcc-axis axis-ped"><span>PEDAGÓGICO</span><h2>Não chamar previsão de proficiência</h2><p>Declarar o alvo; manter o professor na interpretação; proibir uso somativo.</p><b>→ R02, F05, F06</b></div>
  <div class="tcc-axis axis-eth"><span>ÉTICO</span><h2>Proteger dados de estudantes</h2><p>Finalidade explícita, minimização e pseudonimização; dados de crianças e adolescentes exigem base legal (LGPD, art. 14).</p><b>→ R04, F04, F07</b></div>
</div>

<div class="tcc-axes-foot"><strong>Equidade:</strong> a análise por subgrupos (R23) não foi operacionalizada, pois o contrato de dados vigente não declara colunas de subgrupo aprovadas.</div>

---
layout: default
class: content-slide tcc-synthesis-slide
---

<div class="slide-kicker">17 / SÍNTESE</div>

# O que a evidência permite especificar

<div class="tcc-synthesis-layout">
  <div class="tcc-synthesis-orbit" aria-label="Relação entre desempenho, proficiência e modelagem"><div class="tcc-orbit-ring ring-one"></div><div class="tcc-orbit-ring ring-two"></div><div class="tcc-orbit-ring ring-three"></div><strong>15</strong><span>estudos<br>provisórios</span><i>evidências<br>relacionadas</i></div>
  <div class="tcc-synthesis-copy">
    <h2>Condições de projeto, não ranking de modelos.</h2>
    <p>Os estudos classificam e predizem resultados matemáticos com populações, alvos e métricas diferentes. Categorias operacionais de desempenho não equivalem a níveis de proficiência validados.</p>
    <div class="tcc-synthesis-points"><div><b>01</b><span><strong>Alvo explícito</strong> o que a saída prevê, para quem e com que dados.</span></div><div><b>02</b><span><strong>Modelo simples primeiro</strong> regressão logística como referência; outro só com ganho e explicação.</span></div><div><b>03</b><span><strong>Incerteza visível</strong> poucas respostas não sustentam conclusões sobre o estudante.</span></div></div>
  </div>
</div>

<div class="tcc-caption">A síntese organiza o recorte examinado; não estabelece eficácia pedagógica geral.</div>

---
layout: default
class: content-slide tcc-boundary-slide
---

<div class="slide-kicker">18 / ALCANCE</div>

# O que o TCC entrega, e o que não entrega

<div class="tcc-boundary-layout">
  <div class="tcc-boundary-column boundary-yes"><div class="tcc-boundary-mark">✓</div><span>ENTREGA</span><h2>Um mapa auditável e uma especificação</h2><p>Seleção documentada, síntese, lacunas de relato, requisitos rastreáveis e regras de avaliação definidas antes dos dados.</p></div>
  <div class="tcc-boundary-divider"></div>
  <div class="tcc-boundary-column boundary-no"><div class="tcc-boundary-mark">?</div><span>NÃO ENTREGA</span><h2>Evidência de eficácia</h2><p>Não compara modelos em dados reais, não valida um protótipo em escolas e não mede efeito sobre a aprendizagem.</p></div>
</div>

<div class="tcc-boundary-foot"><strong>Limitações:</strong> revisor único, com triagem, extração e MMAT produzidos por IA, em conferência pelo autor; 14 de 15 com texto recuperado; sensibilidade abaixo de 4,0 com 13/45, 29/54 e 5/30; sem aplicação com participantes.</div>

---
layout: default
class: content-slide tcc-gaps-slide
---

<div class="slide-kicker">19 / EVIDÊNCIAS E LIMITES</div>

# Exemplos de limitações nos estudos consultados

<p class="tcc-gaps-intro">Quatro exemplos localizados nos textos primários; não são contagem de frequência nem afirmação sobre toda a literatura.</p>
<div class="tcc-gaps-grid">
  <div><h2>He et al. (2025)<small>pp. 1, 16, 31–35</small></h2><p><strong>Relato:</strong> oito turmas × 45 = 360, mas amostra declarada n=90; docentes distribuídos de modo desigual entre condições.</p><p><strong>Implicação:</strong> denominador, unidade de análise e confundimento exigem cautela.</p></div>
  <div><h2>Villegas-Ch et al. (2025)<small>pp. 2, 14, 22</small></h2><p><strong>Relato:</strong> a introdução menciona um semestre; os métodos, seis semanas; a subanálise de programação chega à semana 8.</p><p><strong>Implicação:</strong> não atribuir a semana 8 à matemática nem inferir duração única.</p></div>
  <div><h2>Nyantah et al. (2025)<small>pp. 101–105</small></h2><p><strong>Relato:</strong> alocação descrita de modo incompatível; diferença no pré-teste; intervenção combina animação e jigsaw.</p><p><strong>Implicação:</strong> não atribuir o resultado à animação isoladamente.</p></div>
  <div><h2>Echeveria et al. (2025)<small>pp. 65, 69–70</small></h2><p><strong>Relato:</strong> anos letivos 2023–2024 e 2022–2023 em seções diferentes; oito itens do alvo também são preditores.</p><p><strong>Implicação:</strong> coorte ambígua; a classificação não é diagnóstico independente.</p></div>
</div>

<div class="tcc-gaps-foot"><strong>Escopo:</strong> exemplos localizados no material associado aos 15 registros da seleção histórica, não estimativa de prevalência. O MMAT contém 15 triagens S1/S2 e 15 conjuntos de critérios preliminares, incluindo adaptações de categoria. Zeng, fora da seleção e sem texto recuperado, não recebeu apreciação; as respostas de Sokkhey são históricas e não foram revalidadas.</div>

---
layout: default
class: content-slide tcc-specification-slide
---

<div class="slide-kicker">20 / RESULTADO — OE3</div>

# Da evidência aos requisitos: uma cadeia rastreável

<div class="tcc-chain" aria-label="Cadeia de rastreabilidade da revisão à avaliação">
  <div class="chain-node"><small>OE1 · OE2</small><strong>Revisão</strong><span>15 estudos</span></div><i>→</i>
  <div class="chain-node chain-key"><small>OE3</small><strong>Requisitos</strong><span>26 grupos (R01–R26)</span></div><i>→</i>
  <div class="chain-node"><small>OE3</small><strong>Funções</strong><span>F01–F07</span></div><i>→</i>
  <div class="chain-node"><small>OE3</small><strong>Aceitação</strong><span>critérios e cenários</span></div><i>→</i>
  <div class="chain-node"><small>OE4</small><strong>Protocolo</strong><span>não aplicado</span></div>
</div>

<div class="tcc-spec-layout">
  <div class="tcc-requirement-examples"><h2>Dois exemplos</h2><p><strong>R02 — separar os conceitos.</strong> Origem: NRC (2001), OECD (2023), BNCC (2018). Decisão: distinguir desempenho, previsão e aprendizagem nas saídas. Limite: não valida uma escala.</p><p><strong>R20 — prevenir vazamento de dados.</strong> Origem: relato ambíguo de Pejić et al. (2021, pp. 50–51), James et al. (2021) e decisão autoral. Decisão: separar treino, validação e teste. Limite: não afirma o que o artigo executou.</p></div>
  <div class="tcc-spec-delivery"><h2>Origens distintas</h2><p>Seis estudos são citados diretamente em sete grupos; os 15 estudos se ligam a 18 grupos. Fundamentos teóricos e decisões autorais completam a rastreabilidade.</p><small>Vínculo com um estudo é decisão de projeto: não significa que o estudo validou o requisito. Figura 1 e Quadros 9 e 10 do TCC.</small></div>
</div>

---
layout: default
class: content-slide tcc-architecture-slide
---

<div class="slide-kicker">21 / ARQUITETURA E SAÍDA</div>

# O professor vê indícios e incerteza, não um veredito

<div class="tcc-architecture-layout">
  <div class="tcc-architecture-path"><div class="arch-node arch-data"><b>F01</b><strong>Ingestão</strong><span>fonte, licença, dicionário</span></div><i>↓</i><div class="arch-node arch-prep"><b>F02</b><strong>Preparação</strong><span>vínculo curricular</span></div><i>↓</i><div class="arch-node arch-model"><b>F03</b><strong>Modelagem</strong><span>alvo e candidatos</span></div><i>↓</i><div class="arch-node arch-eval"><b>F05</b><strong>Avaliação</strong><span>métricas e explicações</span></div><i>↓</i><div class="arch-node arch-present"><b>F04·F06</b><strong>Apresentação</strong><span>revisão docente</span></div></div>
  <div class="tcc-output-card" aria-label="Exemplo fictício de saída por estudante e habilidade">
    <div class="tcc-output-head">Exemplo fictício · sem dados reais nem modelo treinado</div>
    <p class="tcc-output-who"><strong>Estudante A</strong> · comparação de frações</p>
    <div class="tcc-output-metric"><span>Taxa de acertos observada</span><strong>4 de 6 = 0,67</strong><small>intervalo de Wilson de 95%: 0,30–0,90</small></div>
    <div class="tcc-output-scale" aria-hidden="true"><i class="scale-band" style="left: 30%; width: 60%"></i><i class="scale-dot" style="left: 66.7%"></i><i class="scale-cross" style="left: 65%">×</i><span style="left: 0">0</span><span style="left: 50%">0,5</span><span style="left: 100%">1</span></div>
    <div class="tcc-output-metric"><span>Média das probabilidades previstas</span><strong>0,65</strong><small>sem intervalo próprio</small></div>
    <ul><li>calibração não examinada; validação externa pendente</li><li>alerta de risco desabilitado; não usar como nota</li><li>professora registra: examinar as estratégias escritas (F06)</li></ul>
  </div>
</div>

<div class="tcc-caption">Figuras 2 e 3 do TCC. Com 6 respostas, o intervalo cobre de 0,30 a 0,90: pouca evidência não sustenta conclusão sobre o estudante.</div>

---
layout: default
class: content-slide tcc-rules-slide
---

<div class="slide-kicker">22 / OE3 E OE4</div>

# Regras fixadas antes de qualquer dado real

<div class="tcc-rules-layout">
  <div class="tcc-rule-panel">
    <h2>Escolha de modelo <em>OE3</em></h2>
    <p class="tcc-rule-start">Referência: regressão logística regularizada</p>
    <ol class="tcc-rule-steps"><li><b>i</b> perda logarítmica menor: limite superior do IC 95% abaixo de zero (reamostragem por estudante)</li><li><b>ii</b> Brier não piora e ECE não aumenta</li><li><b>iii</b> explicação implementada e conferível (F05)</li></ol>
    <div class="tcc-rule-outcomes"><span class="ok">três condições → adota o candidato</span><span class="keep">qualquer falha → mantém a referência</span></div>
    <small>Teste usado uma única vez, para relatar o modelo escolhido. Hoje o <em>gradient boosting</em> falharia em (iii).</small>
  </div>
  <div class="tcc-rule-panel">
    <h2>Avaliação da especificação <em>OE4</em></h2>
    <div class="tcc-rule-tracks">
      <div><strong>Regra docente</strong><p>5 docentes, duas rodadas; coerente se ao menos 4 de 5 derem 3 ou 4 em cada dimensão, sem problema crítico.</p><span class="ok">coerente</span><span class="keep">revisar</span></div>
      <div><strong>Conferência técnica</strong><p>Autor registra e orientador revisa: rastreabilidade, consistência arquitetural e condições de viabilidade.</p><span class="ok">atendido</span><span class="keep">pendente</span></div>
    </div>
    <small>Viável e coerente só se todos os requisitos passarem nas duas regras. As dimensões docentes incluem a correspondência conceitual com a fonte. Exige parecer ético antes de recrutar.</small>
  </div>
</div>

<div class="tcc-caption">Fluxogramas 2 e 3 do TCC. Nenhuma das regras foi aplicada: não houve treinamento com dados reais nem painel docente.</div>

---
layout: default
class: content-slide tcc-next-slide
---

<div class="slide-kicker">23 / CONCLUSÃO</div>

# Resposta: uma especificação verificável antes dos dados

<div class="tcc-next-layout">
  <div class="tcc-next-list"><div><b>01</b><span><strong>Tipologia</strong> de finalidades, com limite declarado (OE1).</span></div><div><b>02</b><span><strong>Rastreabilidade</strong> da evidência a 26 grupos de requisitos (OE2, OE3).</span></div><div><b>03</b><span><strong>Regras pré-fixadas</strong> de escolha de modelo e de avaliação (OE3, OE4).</span></div><div><b>04</b><span><strong>Lacunas de relato</strong> como orientação para estudos primários (MMAT preliminar).</span></div></div>
  <div class="tcc-next-decision"><span>PRÓXIMOS PASSOS</span><ul><li>Conferir as 15 apreciações preliminares e suas rotas operacionais.</li><li>Aplicar o protocolo com docentes, após parecer ético.</li><li>Testar a regra de modelo em dados reais documentados.</li><li>Codificar itens por registro de representação.</li></ul></div>
</div>

<div class="tcc-caption">Contribuições delimitadas pelo escopo documental. Dados, código e testes versionados permitem reproduzir as contagens e os quadros.</div>

---
layout: center
class: closing-slide
---

<div class="closing-slide-content">
<div class="close-mark" aria-hidden="true">∫</div>

<h1>Obrigado</h1>

<h2>Perguntas e discussão</h2>

<div class="close-rule"></div>
<div class="close-repository">
  <img class="repo-qr" src="/branding/ccw-repository-qr.svg" alt="QR code que abre o repositório público do projeto no GitHub">
  <div class="close-repository-copy"><strong>Aponte a câmera para a fonte pública</strong><span>código, dados derivados e apresentação versionados</span></div>
</div>
<p class="close-title"><strong>Ensino Personalizado de Matemática</strong><br>Oportunidades e Técnicas Computacionais</p>
<p class="close-sources">Fonte pública do TCC: <a href="https://thalesfb.github.io/ccw/results/tcc/main.pdf">thalesfb.github.io/ccw/results/tcc/main.pdf</a> · repositório: <a href="https://github.com/thalesfb/ccw">github.com/thalesfb/ccw</a></p>
</div>
