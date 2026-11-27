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
  <h1>Ensino Personalizado de Matemática:<br><span class="cover-subtitle">revisão sistemática de técnicas computacionais e especificação de um protótipo de apoio à interpretação docente</span></h1>
  <div class="cover-credits">
    <strong>Trabalho de Conclusão de Curso (TCC)</strong><br>
    <span class="cover-author">Thales Ferreira Batista<br>Ciência da Computação</span>
    <span class="cover-supervision">Orientador: Prof. Dr. Rafael Zanin<br>Coorientador: Prof. Dr. Manassés Ribeiro<br>Instituto Federal Catarinense - Campus Videira</span>
  </div>
</div>
<div class="cover-snapshot">Revisão sistemática · seleção original de 15 estudos · especificação conceitual</div>

<!--
[0:30] MOSTRAR: título e a faixa inferior (revisão, 15 estudos, especificação conceitual).

FALA: Boa tarde. Apresento o TCC Ensino Personalizado de Matemática. O trabalho tem duas entregas ligadas entre si: uma revisão sistemática de técnicas computacionais aplicadas ao ensino de matemática e, a partir dela, a especificação de um protótipo para apoiar a interpretação do professor. É uma entrega documental: não há sistema validado em escola.
-->

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

<!--
[1:00] MOSTRAR: frase em destaque à esquerda; depois os quatro cartões, de cima para baixo.

FALA: Em turmas heterogêneas, a média da turma não mostra onde cada estudante está nem quanta evidência sustenta essa leitura. O professor tem pouco tempo para analisar registros, e a mesma intervenção não atende necessidades distintas. Há literatura sobre técnicas computacionais, mas ela está dispersa em técnicas, alvos e contextos. A premissa do trabalho: a técnica pode organizar evidências, e a interpretação continua com o professor.
-->

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

<!--
[0:45] MOSTRAR: caixa central com o objetivo geral; depois PARA QUÊ e ESCOPO.

FALA: O objetivo geral é propor uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática, fundamentada na literatura. O apoio se limita a mostrar ao professor indícios de desempenho e de incerteza por estudante e habilidade, sem substituir seu julgamento. O escopo é revisão e especificação; protótipo validado e avaliação de eficácia ficam fora.
-->

---
layout: default
class: content-slide tcc-problem-slide
---

<div class="slide-kicker">03 / PROBLEMA DE PESQUISA</div>

# Pergunta de pesquisa

<div class="rq-grid tcc-question-grid"><p class="tcc-question-text">Como estruturar uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática a partir das evidências e técnicas computacionais identificadas na literatura?</p></div>

<!--
[0:30] MOSTRAR: ler a pergunta inteira, sem paráfrase.

FALA: A pergunta de pesquisa é esta. A palavra que orienta a resposta é estruturar: o resultado esperado é uma forma rastreável de organizar a especificação a partir da evidência, e não a escolha de um modelo vencedor.
-->

---
layout: default
class: content-slide
---

<div class="slide-kicker">04 / BASE CONCEITUAL</div>

# Cinco distinções interpretativas

<div class="interpretation-ladder">
  <div class="interpretation-level level-blue"><b>01</b><strong>Desempenho observado</strong><span>Acertos, notas, tentativas, estratégias ou tempo registrados em uma tarefa.</span></div>
  <div class="interpretation-level level-purple"><b>02</b><strong>Probabilidade preditiva</strong><span>Saída de um modelo, para um alvo definido e com os dados usados; não é proficiência.</span></div>
  <div class="interpretation-level level-green"><b>03</b><strong>Proficiência estimada</strong><span>Posição em uma escala; exige modelo de mensuração e evidência de validade.</span></div>
  <div class="interpretation-level level-orange"><b>04</b><strong>Competência</strong><span>Mobilização de conhecimentos, habilidades, atitudes e valores diante de demandas.</span></div>
  <div class="interpretation-level level-red"><b>05</b><strong>Aprendizagem</strong><span>Neste TCC: mudanças no que o estudante sabe e consegue fazer ao longo do tempo.</span></div>
</div>

<div class="concept-note"><strong>Regra de leitura:</strong> uma saída computacional organiza evidências e produz estimativas; sozinha, não observa os processos cognitivos, sociais e afetivos da aprendizagem nem demonstra eficácia pedagógica.</div>

<div class="tcc-caption">Elaboração do autor com base em National Research Council (2001), OECD (2023) e Brasil / BNCC (2018); não é uma escala validada.</div>

<!--
[1:15] MOSTRAR: a escada de 01 a 05, em ordem; ao final, a regra de leitura.

FALA: Antes da revisão, separo cinco termos que a literatura às vezes mistura. Desempenho observado é o que foi registrado na tarefa. Probabilidade preditiva é a saída de um modelo para um alvo definido e com os dados usados; não é proficiência. Proficiência estimada exige modelo de mensuração e evidência de validade. Competência, no sentido da BNCC, é mobilizar conhecimentos, habilidades, atitudes e valores. Aprendizagem, neste trabalho, é mudança ao longo do tempo. A regra que sai daqui: a saída computacional organiza evidência e produz estimativas, mas sozinha não observa a aprendizagem nem demonstra eficácia.
-->

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

<!--
[1:00] MOSTRAR: o exemplo do 7º ano; depois o cartão 0/1 ≠ diagnóstico.

FALA: Dois referenciais da didática da matemática delimitam o que essa saída não capta. Para Duval, compreender exige coordenar ao menos dois registros de representação. Para Brousseau, um erro pode manifestar um obstáculo. No exemplo, errar a conversão do enunciado para 2x + 5 = 15 é diferente de errar ao isolar x, mas os dois viram o mesmo zero num registro binário. Por isso a especificação organiza indícios por habilidade, com incerteza, e deixa o tipo de erro para o professor, na revisão docente da função F06. Codificar itens por registro de representação fica como trabalho futuro.
-->

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

<div class="tcc-caption">Meios: revisão de 2015–2026 relatada com o PRISMA 2020, apreciação MMAT conferida pelo autor e fluxo de processamento versionado. O protocolo está proposto; sua aplicação está pendente.</div>

<!--
[1:00] MOSTRAR: os quatro passos e, em cada um, o produto indicado pela seta.

FALA: Os quatro objetivos específicos geram quatro produtos. OE1 categoriza técnicas e finalidades: resulta na tipologia dos 15 estudos. OE2 codifica limitações metodológicas e de relato com o MMAT e discute os eixos técnico, pedagógico e ético. OE3 formula a especificação: 26 grupos de requisitos, critérios de dados e modelos e a arquitetura. OE4 propõe o protocolo para avaliar a viabilidade e a coerência da especificação. O protocolo está proposto e não foi aplicado.
-->

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

<!--
[1:00] MOSTRAR: os hexágonos (três camadas); o cartão de 72 consultas; a faixa PRISMA/MMAT.

FALA: A busca combina três camadas: um termo matemático, um termo de técnica computacional e um termo de educação. Foram 72 consultas canônicas, 48 em inglês e 24 em português, em quatro bases, para 2015 a 2026, com busca encerrada em 31 de agosto de 2026. O PRISMA 2020 orienta o relato, e o MMAT 2018 orienta a apreciação metodológica.
-->

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

<!--
[0:40] MOSTRAR: os quatro cartões com as contagens; a legenda.

FALA: As quatro bases são complementares: Semantic Scholar, OpenAlex, Crossref e CORE. Depois da remoção de 29 duplicatas ficaram 11.875 registros. A base indicada em cada cartão é a origem da versão mantida, não a cobertura exclusiva daquela base. Se faltar tempo, este slide pode ser dito em uma frase.
-->

---
layout: center
class: image-slide tcc-prisma-slide
---

<div class="slide-kicker">09 / FLUXO PRISMA</div>

<h1 class="sr-only">Representação operacional do processo de seleção, com referência ao PRISMA 2020</h1>
<p class="sr-only" id="prisma-flow-description">Fluxo: 11.904 registros identificados; 29 duplicatas removidas; 11.875 triados; 9.393 excluídos na triagem; 2.482 priorizados; 2.464 excluídos na priorização; 18 relatórios na lista; 1 excluído após resumo; 17 relatórios procurados; 2 não recuperados; 15 avaliados em texto completo; 1 protocolo excluído; 14 textos recuperados; 15 estudos na seleção original.</p>

<img src="/images/prisma_flow.png" alt="Fluxograma de seleção dos estudos da revisão" aria-describedby="prisma-flow-description" class="feature-image prisma-image tcc-prisma-image" />

<!--
[1:15] MOSTRAR: percorrer o fluxograma de cima para baixo, apontando cada caixa.

FALA: Este é o fluxo de seleção. Foram 11.904 registros identificados e 29 duplicatas removidas; 11.875 foram triados, e as regras automáticas excluíram 9.393, em boa parte por resumo ausente ou curto. Dos 2.482 priorizados por escore de relevância, o corte 4,0 deixou 18 na lista preliminar. Um saiu após a leitura do resumo; 17 relatórios foram procurados e dois não foram recuperados, Sokkhey e Zeng. Quinze foram avaliados em texto completo, e um protocolo sem resultados foi excluído. A seleção original fica com 15 estudos, e o próximo slide explica por quê.
-->

---
layout: default
class: content-slide tcc-retained-slide
---

<div class="slide-kicker">10 / SELEÇÃO ORIGINAL</div>

# 15 estudos na seleção; 14 textos recuperados

<div class="tcc-retained-layout">
  <div class="tcc-retained-number"><strong>15</strong><span>estudos na<br>seleção original</span><div class="tcc-retained-rule"></div><p>14 com texto recuperado</p></div>
  <div class="tcc-retained-copy">
    <div class="tcc-retained-strata" aria-label="Na seleção original, 14 textos recuperados e Sokkhey sem cópia verificável"><strong>14</strong><span>textos recuperados e conferidos</span><strong>1</strong><span>Sokkhey, sem cópia verificável</span></div>
    <h2>Uma inclusão sem cópia verificável</h2>
    <p>Sokkhey (E10) permanece na seleção original sem apreciação MMAT, por falta de cópia verificável; sua linha na síntese baseia-se no resumo publicado. Zeng não integra os 15 estudos e não recebeu apreciação.</p>
  </div>
</div>

<!--
[0:45] MOSTRAR: o número 15 e a divisão 14 + 1.

FALA: São 15 estudos na seleção original, 14 com texto recuperado e conferido. Sokkhey permanece na seleção, mas sem apreciação MMAT, e sua linha na síntese se baseia só no resumo publicado. Zeng não foi recuperado e não integra os 15.
-->

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

<!--
[1:00] MOSTRAR: as três barras; o número 4,0; o aviso de limitação.

FALA: O corte 4,0 serviu para priorizar a leitura e foi mantido. Explorei o que ficou abaixo dele: 13 de 45 registros elegíveis no censo entre 3,75 e 3,95; 29 de 54 na seleção dirigida entre 3,50 e 3,74; e 5 de 30 na amostra estratificada entre 3,00 e 3,49. Os desenhos são diferentes, então não somo as frações nem estimo a perda total. É uma limitação declarada: o recorte não é um censo da literatura, e o escore mede relevância, não qualidade.
-->

---
layout: default
class: content-slide tcc-mmat-slide
---

<div class="slide-kicker">12 / QUALIDADE METODOLÓGICA</div>

# MMAT conferido: critério a critério, sem nota global

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

<div class="tcc-mmat-result"><strong>Estado:</strong> nos 14 textos recuperados, o autor conferiu S1 (14 Y) e S2 (13 Y; 1 CT). Sokkhey (E10) permanece na seleção original sem apreciação MMAT, por falta de cópia verificável do texto completo. Nos três estudos de métodos mistos, respostas dos componentes qualitativo e quantitativo seguem identificadas como assistidas por IA. Q1–Q5 variam por categoria; sem escore agregado.</div>

<!--
[1:00] MOSTRAR: S1 e S2; a legenda Y/N/CT; a faixa de estado embaixo.

FALA: O MMAT funciona em duas etapas: duas perguntas de triagem e depois cinco critérios próprios da categoria do estudo. Cada resposta é Sim, Não ou Não é possível concluir. Nos 14 textos recuperados, S1 teve 14 Sim e S2 teve 13 Sim e 1 Não é possível concluir. A leitura é critério a critério, sem nota global. Nos três estudos de métodos mistos, as respostas dos componentes qualitativo e quantitativo seguem identificadas como assistidas por IA.
-->

---
layout: default
class: content-slide tcc-typology-slide
---

<div class="slide-kicker">13 / RESULTADO — OE1</div>

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

<!--
[1:15] MOSTRAR: as cinco barras; depois o aviso de categorias não homogêneas.

FALA: Este é o resultado do OE1. Cada estudo recebeu uma finalidade principal: predição ou classificação em 8, personalização ou sistemas tutores em 3, intervenção didática em 2, modelagem cognitiva em 1 e integração curricular em 1. Nos estudos de predição, a finalidade pedagógica aparece apenas pelo alvo previsto, como nota ou desempenho posterior. Há um limite na própria tipologia: predição é uma tarefa computacional, e as outras quatro são finalidades de uso. As frequências descrevem este recorte, não a literatura toda.
-->

---
layout: default
class: content-slide tcc-reporting-slide
---

<div class="slide-kicker">14 / RESULTADO — OE2</div>

# O que falta nos relatos: a resposta mais comum é “não é possível concluir”

<div class="tcc-reporting-layout">
  <div class="tcc-ct-grid" role="table" aria-label="Respostas CT por categoria MMAT e critério">
    <div class="tcc-ct-head" role="row"><span role="columnheader">Categoria (n)</span><span role="columnheader">Q1</span><span role="columnheader">Q2</span><span role="columnheader">Q3</span><span role="columnheader">Q4</span><span role="columnheader">Q5</span></div>
    <div role="row"><span role="rowheader">Quantitativo descritivo (7)</span><b class="ct-mid" role="cell">2</b><b class="ct-all" role="cell">7</b><b class="ct-all" role="cell">7</b><b class="ct-all" role="cell">7</b><b class="ct-high" role="cell">6</b></div>
    <div role="row"><span role="rowheader">Não randomizado (4)</span><b class="ct-all" role="cell">4</b><b class="ct-mid" role="cell">2</b><b class="ct-mid" role="cell">2</b><b class="ct-mid" role="cell">2</b><b class="ct-high" role="cell">3</b></div>
    <div role="row"><span role="rowheader">Métodos mistos (3)</span><b class="ct-none" role="cell">0</b><b class="ct-mid" role="cell">1</b><b class="ct-mid" role="cell">1</b><b class="ct-mid" role="cell">1</b><b class="ct-mid" role="cell">1</b></div>
    <p class="tcc-ct-note">Número de respostas CT em cada critério. Q1–Q5 seguem a rubrica de cada categoria.</p>
  </div>
  <div class="tcc-reporting-copy">
    <h2>Falta informação, mais do que falha demonstrada.</h2>
    <p>CT predomina em representatividade, medidas, completude, controle e análise.</p>
    <p><strong>Consequência:</strong> a especificação exige descrever alvo, população, transformações dos dados e forma de avaliação.</p>
  </div>
</div>

<div class="tcc-caption">Tabela 3 do TCC. Respostas conferidas pelo autor (revisor único); não somadas em escore. Nenhum estudo na categoria randomizada.</div>

<!--
[1:15] MOSTRAR: a grade; destacar a linha quantitativo descritivo (Q2 a Q4 com 7 de 7).

FALA: Este é o resultado do OE2. A grade conta quantas vezes cada critério ficou como Não é possível concluir. Nos sete estudos quantitativos descritivos, Q2, Q3 e Q4 ficaram assim em todos. A leitura é que falta informação nos relatos, mais do que falha demonstrada. A consequência para o projeto é exigir que se declarem alvo, população, transformações dos dados e forma de avaliação.
-->

---
layout: default
class: content-slide tcc-axes-slide
---

<div class="slide-kicker">15 / RESULTADO — OE2</div>

# Três eixos de risco viraram requisitos

<div class="tcc-axes-grid">
  <div class="tcc-axis axis-tech"><span>TÉCNICO</span><h2>Validar sem vazar informação</h2><p>Separar treino, validação e teste por estudante; examinar calibração e não só acurácia.</p><b>→ R20, F03</b></div>
  <div class="tcc-axis axis-ped"><span>PEDAGÓGICO</span><h2>Não chamar previsão de proficiência</h2><p>Declarar o alvo; manter o professor na interpretação; proibir uso somativo.</p><b>→ R02, F05, F06</b></div>
  <div class="tcc-axis axis-eth"><span>ÉTICO</span><h2>Proteger dados de estudantes</h2><p>Finalidade explícita, minimização e pseudonimização; dados de crianças e adolescentes exigem base legal (LGPD, art. 14).</p><b>→ R04, F04, F07</b></div>
</div>

<div class="tcc-axes-foot"><strong>Equidade:</strong> a análise por subgrupos (R23) não foi operacionalizada, pois o contrato de dados vigente não declara colunas de subgrupo aprovadas.</div>

<!--
[1:00] MOSTRAR: as três colunas e os códigos R e F de cada uma; o rodapé de equidade.

FALA: Os três eixos de risco discutidos no OE2 viraram requisitos. No eixo técnico, validar sem vazar informação: R20 registra quando o desfecho é definido e quais atributos existem nesse momento, e F03 bloqueia a saída que viole isso. No pedagógico, não chamar previsão de proficiência e manter o professor na interpretação. No ético, finalidade, minimização e pseudonimização, com atenção ao art. 14 da LGPD para crianças e adolescentes. A análise de equidade, R23, não foi operacionalizada porque os dados não têm colunas de subgrupo aprovadas.
-->

---
layout: default
class: content-slide tcc-synthesis-slide
---

<div class="slide-kicker">16 / SÍNTESE</div>

# O que a evidência permite especificar

<div class="tcc-synthesis-layout">
  <div class="tcc-synthesis-orbit" aria-label="Relação entre desempenho, proficiência e modelagem"><div class="tcc-orbit-ring ring-one"></div><div class="tcc-orbit-ring ring-two"></div><div class="tcc-orbit-ring ring-three"></div><strong>15</strong><span>estudos na<br>seleção original</span><i>evidências<br>relacionadas</i></div>
  <div class="tcc-synthesis-copy">
    <h2>Condições de projeto, não ranking de modelos.</h2>
    <p>Os estudos classificam e predizem resultados matemáticos com populações, alvos e métricas diferentes. Categorias operacionais de desempenho não equivalem a níveis de proficiência validados.</p>
    <div class="tcc-synthesis-points"><div><b>01</b><span><strong>Alvo explícito</strong> o que a saída prevê, para quem e com que dados.</span></div><div><b>02</b><span><strong>Modelo simples primeiro</strong> regressão logística como referência; outro só com ganho e explicação.</span></div><div><b>03</b><span><strong>Incerteza visível</strong> poucas respostas não sustentam conclusões sobre o estudante.</span></div></div>
  </div>
</div>

<div class="tcc-caption">A síntese organiza o recorte examinado; não estabelece eficácia pedagógica geral.</div>

<!--
[1:00] MOSTRAR: a frase de título do bloco e os três pontos numerados.

FALA: Como os estudos usam populações, alvos e métricas diferentes, não faz sentido ranquear modelos. O que a evidência permite é fixar condições de projeto: alvo explícito, modelo simples como referência, com a regressão logística, e incerteza visível, porque poucas respostas não sustentam conclusão sobre o estudante.
-->

---
layout: default
class: content-slide tcc-boundary-slide
---

<div class="slide-kicker">17 / ALCANCE</div>

# O que o TCC entrega, e o que não entrega

<div class="tcc-boundary-layout">
  <div class="tcc-boundary-column boundary-yes"><div class="tcc-boundary-mark">✓</div><span>ENTREGA</span><h2>Um mapa auditável e uma especificação</h2><p>Seleção documentada, síntese, lacunas de relato, requisitos rastreáveis e regras de avaliação definidas antes dos dados.</p></div>
  <div class="tcc-boundary-divider"></div>
  <div class="tcc-boundary-column boundary-no"><div class="tcc-boundary-mark">?</div><span>NÃO ENTREGA</span><h2>Evidência de eficácia</h2><p>Não compara modelos em dados reais, não valida um protótipo em escolas e não mede efeito sobre a aprendizagem.</p></div>
</div>

<div class="tcc-boundary-foot"><strong>Limitações:</strong> revisor único, com triagem e extração produzidas por IA e MMAT conferido pelo autor; 14 de 15 com texto recuperado; sensibilidade abaixo de 4,0 com 13/45, 29/54 e 5/30; sem aplicação com participantes.</div>

<!--
[0:50] MOSTRAR: as duas colunas; o rodapé de limitações.

FALA: O TCC entrega um mapa auditável da literatura e uma especificação com requisitos rastreáveis e regras de avaliação definidas antes dos dados. Não entrega evidência de eficácia: não compara modelos em dados reais, não valida protótipo em escola e não mede efeito na aprendizagem. As limitações principais são o revisor único, a triagem em texto completo e a extração produzidas por modelos de IA, com o MMAT conferido pelo autor, 14 de 15 textos recuperados, a sensibilidade abaixo do corte e a ausência de aplicação com participantes.
-->

---
layout: default
class: content-slide tcc-gaps-slide
---

<div class="slide-kicker">18 / EVIDÊNCIAS E LIMITES</div>

# Exemplos de limitações nos estudos consultados

<p class="tcc-gaps-intro">Dois exemplos dos textos recuperados; ilustram limites, não sua frequência no corpus.</p>
<div class="tcc-gaps-grid">
  <div><h2>He et al. (2025)</h2><p><strong>Relato:</strong> oito turmas de 45 estudantes e amostra de 90 por comparação, sem explicitar a relação; um professor responde pelas duas turmas de controle.</p><p><strong>Implicação:</strong> explicitar denominadores e unidade de análise ao interpretar resultados.</p></div>
  <div><h2>Nyantah et al. (2025)</h2><p><strong>Relato:</strong> alocação das escolas descrita como aleatória e depois como quase-experimental; grupos já diferiam no pré-teste; animação combinada com jigsaw.</p><p><strong>Implicação:</strong> não presumir randomização nem atribuir o resultado à animação isoladamente.</p></div>
</div>

<div class="tcc-gaps-foot"><strong>Escopo:</strong> exemplos ilustrativos, sem estimativa de prevalência.</div>

<!--
[1:00] MOSTRAR: os dois cartões: relato e implicação de cada um.

FALA: Dois exemplos mostram o tipo de limite encontrado, sem indicar frequência. Em He e colaboradores, há oito turmas de 45 estudantes e uma amostra de 90 por comparação, sem que o texto explicite essa relação, e um único professor responde pelas duas turmas de controle; por isso a especificação exige declarar denominadores e unidade de análise. Em Nyantah e colaboradores, a alocação aparece como aleatória e depois como quase-experimental, os grupos já diferiam no pré-teste e a intervenção combina animação e jigsaw; não se pode atribuir o resultado à animação isoladamente.
-->

---
layout: default
class: content-slide tcc-specification-slide
---

<div class="slide-kicker">19 / RESULTADO — OE3</div>

# Da evidência aos requisitos: uma cadeia rastreável

<div class="tcc-chain" aria-label="Cadeia de rastreabilidade da revisão à avaliação">
  <div class="chain-node"><small>OE1 · OE2</small><strong>Revisão</strong><span>15 estudos</span></div><i>→</i>
  <div class="chain-node chain-key"><small>OE3</small><strong>Requisitos</strong><span>26 grupos (R01–R26)</span></div><i>→</i>
  <div class="chain-node"><small>OE3</small><strong>Funções</strong><span>F01–F07</span></div><i>→</i>
  <div class="chain-node"><small>OE3</small><strong>Aceitação</strong><span>critérios e cenários</span></div><i>→</i>
  <div class="chain-node"><small>OE4</small><strong>Protocolo</strong><span>não aplicado</span></div>
</div>

<div class="tcc-spec-layout">
  <div class="tcc-requirement-examples"><h2>Exemplo: proteção de dados</h2><p><strong>R04:</strong> finalidade, minimização e controle de acesso.</p><p><strong>Funções:</strong> F04 limita a consulta individual; F07 registra e exporta versões, decisões e saídas.</p><p><strong>Aceitação proposta:</strong> perfil autorizado, identificadores pseudonimizados e sem dados pessoais desnecessários.</p><small>Vínculos parciais; critérios ainda não testados.</small></div>
  <div class="tcc-spec-delivery"><h2>Duas matrizes, duas leituras</h2><p>Os 15 estudos se relacionam a 18 grupos R; outra matriz cita diretamente seis estudos em sete grupos.</p><small>Esses vínculos motivam decisões de projeto; não demonstram validação empírica dos requisitos.</small></div>
</div>

<!--
[1:15] MOSTRAR: a cadeia da esquerda para a direita; depois o exemplo R04 e o quadro das duas matrizes.

FALA: O OE3 se organiza como uma cadeia rastreável, que é a Figura 3 do TCC: revisão, 26 grupos de requisitos, sete funções, critérios de aceitação e o protocolo do OE4. No exemplo de proteção de dados, R04 exige finalidade, minimização e controle de acesso; F04 limita a consulta individual e F07 registra e exporta versões; o critério de aceitação pede perfil autorizado e identificadores pseudonimizados. Há duas matrizes: os 15 estudos se relacionam a 18 grupos de requisitos, e seis estudos são citados diretamente em sete grupos. Esses vínculos motivam decisões de projeto; não validam os requisitos.
-->

---
layout: default
class: content-slide tcc-architecture-slide
---

<div class="slide-kicker">20 / ARQUITETURA E SAÍDA</div>

# O professor vê indícios e incerteza, não um veredito

<div class="tcc-architecture-layout">
  <div class="tcc-architecture-path"><div class="arch-node arch-data"><b>F01</b><strong>Ingestão</strong><span>fonte, licença, dicionário</span></div><i>↓</i><div class="arch-node arch-prep"><b>F02</b><strong>Preparação</strong><span>vínculo curricular</span></div><i>↓</i><div class="arch-node arch-model"><b>F03</b><strong>Modelagem</strong><span>alvo e candidatos</span></div><i>↓</i><div class="arch-node arch-eval"><b>F05</b><strong>Avaliação</strong><span>métricas e explicações</span></div><i>↓</i><div class="arch-node arch-present"><b>F04·F06</b><strong>Apresentação</strong><span>revisão docente</span></div></div>
  <div class="tcc-output-card" aria-label="Exemplo fictício de saída por estudante e habilidade">
    <div class="tcc-output-head">F07 · registro e exportação · saída fictícia, sem treino real</div>
    <p class="tcc-output-who"><strong>Estudante A</strong> · comparação de frações</p>
    <div class="tcc-output-metric"><span>Taxa de acertos observada</span><strong>4 de 6 = 0,67</strong><small>intervalo de Wilson de 95%: 0,30–0,90</small></div>
    <div class="tcc-output-scale" aria-hidden="true"><i class="scale-band" style="left: 30%; width: 60%"></i><i class="scale-dot" style="left: 66.7%"></i><i class="scale-cross" style="left: 65%">×</i><span style="left: 0">0</span><span style="left: 50%">0,5</span><span style="left: 100%">1</span></div>
    <div class="tcc-output-metric"><span>Média das probabilidades previstas</span><strong>0,65</strong><small>sem intervalo próprio</small></div>
    <ul><li>calibração não examinada; validação externa pendente</li><li>alerta de risco desabilitado; não usar como nota</li><li>professora registra: examinar as estratégias escritas (F06)</li></ul>
  </div>
</div>

<div class="tcc-caption">Figuras 4 e 5 do TCC. Com 6 respostas, o intervalo cobre de 0,30 a 0,90: pouca evidência não sustenta conclusão sobre o estudante.</div>

<!--
[1:15] MOSTRAR: o fluxo F01 a F06 à esquerda; no cartão, apontar o intervalo 0,30–0,90 na régua.

FALA: A arquitetura vai da ingestão com fonte, licença e dicionário, F01, à preparação com vínculo curricular, F02, à modelagem, F03, à avaliação com métricas e explicações, F05, e à apresentação com revisão docente, F04 e F06. F07 registra e exporta tudo. À direita, uma saída fictícia: o estudante A acertou 4 de 6 itens de comparação de frações, taxa de 0,67, mas o intervalo de Wilson de 95% vai de 0,30 a 0,90. Com tão poucas respostas, não há conclusão sobre o estudante. A média das probabilidades previstas aparece sem intervalo próprio, a calibração não foi examinada e o alerta de risco fica desabilitado. Quem decide o próximo passo é a professora.
-->

---
layout: default
class: content-slide tcc-rules-slide
---

<div class="slide-kicker">21 / OE3 E OE4</div>

# Regras do protocolo proposto

<div class="tcc-rules-layout">
  <div class="tcc-rule-panel">
    <h2>Escolha de modelo <em>OE3</em></h2>
    <p class="tcc-rule-start">Referência: regressão logística regularizada</p>
    <ol class="tcc-rule-steps"><li><b>i</b> melhora a perda logarítmica, com IC 95% por estudante</li><li><b>ii</b> Brier não piora; ECE não aumenta</li><li><b>iii</b> explicação local conferível (F05)</li></ol>
    <div class="tcc-rule-outcomes"><span class="ok">três condições → adota o candidato</span><span class="keep">se falhar → mantém a referência</span></div>
    <small>Regra para um único candidato; não aplicada a dados educacionais reais.</small>
  </div>
  <div class="tcc-rule-panel">
    <h2>Avaliação da especificação <em>OE4</em></h2>
    <div class="tcc-rule-tracks">
      <div><strong>Regra docente</strong><p>5 docentes, duas rodadas; coerente se ao menos 4 de 5 derem 3 ou 4 em cada dimensão, sem problema crítico.</p><span class="ok">coerente</span><span class="keep">revisar</span></div>
      <div><strong>Conferência técnica</strong><p>Examina rastreabilidade, consistência da arquitetura e condições de viabilidade.</p><span class="ok">atendido</span><span class="keep">pendente</span></div>
    </div>
    <small>A regra docente também examina a correspondência conceitual com a fonte. A aplicação exige parecer ético.</small>
  </div>
</div>

<div class="tcc-caption">Fluxogramas 2 e 3 do TCC. Nenhuma das regras foi aplicada: não houve treinamento com dados reais nem painel docente.</div>

<!--
[1:15] MOSTRAR: painel esquerdo, condições i a iii; painel direito, regra docente e conferência técnica.

FALA: As regras foram fixadas antes de qualquer dado real. Para o modelo, a referência é a regressão logística regularizada. Um candidato mais complexo só é adotado se cumprir três condições: melhorar a perda logarítmica, com intervalo de 95% por reamostragem pareada por estudante; não piorar o Brier nem aumentar o erro de calibração esperado; e oferecer explicação local conferível. Se falhar, mantém-se a referência. Para o OE4, um painel de cinco docentes avalia cada grupo de requisitos em duas rodadas; o grupo é coerente se ao menos quatro dos cinco derem 3 ou 4 em cada dimensão, sem problema crítico. A conferência técnica é separada. As fichas estão no Apêndice C. Nada disso foi aplicado, e a aplicação depende de parecer ético.
-->

---
layout: default
class: content-slide tcc-next-slide
---

<div class="slide-kicker">22 / CONCLUSÃO</div>

# Resposta: uma especificação verificável antes dos dados

<div class="tcc-next-layout">
  <div class="tcc-next-list"><div><b>01</b><span><strong>Tipologia</strong> de finalidades, com limite declarado (OE1).</span></div><div><b>02</b><span><strong>Rastreabilidade</strong> da evidência a 26 grupos de requisitos (OE2, OE3).</span></div><div><b>03</b><span><strong>Regras pré-fixadas</strong> de escolha de modelo e de avaliação (OE3, OE4).</span></div><div><b>04</b><span><strong>Lacunas de relato</strong> como orientação para estudos primários (MMAT conferido pelo autor).</span></div></div>
  <div class="tcc-next-decision"><span>PRÓXIMOS PASSOS</span><ul><li>Aplicar o protocolo com docentes, após parecer ético.</li><li>Testar a regra de modelo em dados reais documentados.</li><li>Codificar itens por registro de representação.</li></ul></div>
</div>

<div class="tcc-caption">Contribuições delimitadas pelo escopo documental. Dados, código e testes versionados permitem reproduzir as contagens e os quadros.</div>

<!--
[1:15] MOSTRAR: as quatro contribuições; depois os próximos passos.

FALA: Respondendo à pergunta: a especificação se estrutura ligando alvo e população à evidência disponível, convertendo os achados em requisitos e definindo como o professor examina as saídas. O OE1 mostrou que a literatura se concentra em predição, com finalidade pedagógica indireta. O OE2 mostrou que o desempenho reportado não se transfere para a sala de aula sem alvo, população, validação e incerteza. O OE3 converteu essas lacunas em exigências verificáveis. O OE4 fixou os critérios de avaliação antes da aplicação. Os próximos passos são aplicar o protocolo com docentes após parecer ético, testar a regra de modelo em dados reais documentados, construir a correspondência com as habilidades da BNCC e codificar itens por registro de representação.
-->

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
<p class="close-title"><strong>Ensino Personalizado de Matemática</strong><br>Revisão sistemática de técnicas computacionais e especificação de um protótipo de apoio à interpretação docente</p>
<p class="close-sources">Fonte pública do TCC: <a href="https://thalesfb.github.io/ccw/results/tcc/main.pdf">thalesfb.github.io/ccw/results/tcc/main.pdf</a> · repositório: <a href="https://github.com/thalesfb/ccw">github.com/thalesfb/ccw</a></p>
</div>

<!--
[0:15] MOSTRAR: o QR do repositório.

FALA: Obrigado. O texto, os dados derivados e o código estão no repositório público, acessível pelo QR. Fico à disposição para as perguntas.
-->
