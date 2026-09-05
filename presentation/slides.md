---
theme: default
title: "Ensino Personalizado de Matemática"
info: "Revisão Sistemática da Literatura — snapshot adjudicado"
author: "Thales Ferreira Batista"
keywords: "TCC, ensino personalizado, matemática, revisão sistemática, PRISMA"
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

# Ensino Personalizado de Matemática

## Oportunidades e Técnicas Computacionais

<br>

**Revisão Sistemática da Literatura — relato orientado pelo PRISMA 2020**

<br>

Thales Ferreira Batista · Ciência da Computação

Prof. Dr. Rafael Zanin (IFC) · Prof. Dr. Manassés Ribeiro (IFC)

IFC — Videira

<br>

<small>Snapshot adjudicado: 03/09/2026 · recorte temporal: 2015–2026</small>

---
layout: two-cols
---

# Por que esta revisão?

::right::

<br>

## Problema de pesquisa

Professores lidam com turmas heterogêneas e precisam identificar necessidades de aprendizagem em tempo hábil.

<br>

## Questão central

Como técnicas computacionais podem apoiar o diagnóstico e a personalização do ensino de matemática?

<br>

<small>O trabalho mapeia evidências e lacunas. Não apresenta ainda um protótipo validado ou uma estimativa agregada de eficácia.</small>

---

# Perguntas e objetivo

| Pergunta | Foco da revisão |
| --- | --- |
| **RQ1** | Quais técnicas computacionais são aplicadas à educação matemática? |
| **RQ2** | Como essas aplicações são avaliadas em contextos educacionais? |
| **RQ3** | Quais lacunas, limitações e desafios são reportados? |
| **RQ4** | Que direcionamentos podem apoiar ferramentas educacionais mais eficazes? |

<br>

> Objetivo: mapear e analisar aplicações de *machine learning*, *learning analytics* e sistemas tutores inteligentes na educação matemática, identificando tendências, lacunas e requisitos para uma futura especificação técnica e pedagógica.

---
layout: two-cols
---

# Protocolo e escopo

::right::

### Relato orientado pelo PRISMA 2020

- **Recorte temporal:** 2015–2026
- **Idiomas planejados:** inglês e português
- **Consultas canônicas:** 72 (48 EN + 24 PT)
- **Fontes:** Semantic Scholar, OpenAlex, Crossref e CORE
- **Filtro operacional:** score de relevância ≥ 4,0

<br>

> O score organiza o processamento. Ele não substitui a adjudicação de escopo, a avaliação metodológica ou a leitura das fontes primárias.

---

# Do registro bruto à população retida

<div class="flow-grid">
  <div class="flow-card blue"><strong>11.904</strong><span>identificados</span></div>
  <div class="flow-arrow">→</div>
  <div class="flow-card teal"><strong>27</strong><span>remoções determinísticas<br>(25 DOI + 2 URL)</span></div>
  <div class="flow-arrow">→</div>
  <div class="flow-card green"><strong>11.877</strong><span>na triagem</span></div>
</div>

<div class="flow-grid">
  <div class="flow-card amber"><strong>9.391</strong><span>excluídos na triagem</span></div>
  <div class="flow-arrow">→</div>
  <div class="flow-card orange"><strong>2.486</strong><span>na elegibilidade</span></div>
  <div class="flow-arrow">→</div>
  <div class="flow-card violet"><strong>2.468</strong><span>excluídos na elegibilidade</span></div>
</div>

<div class="flow-grid flow-final">
  <div></div><div></div>
  <div class="flow-card indigo"><strong>18</strong><span>retidos no snapshot</span></div>
</div>

<small>O fluxo atual registra identidade bibliográfica de forma determinística. Igualdade de título permanece como candidato à auditoria semântica, não como remoção automática.</small>

---
layout: center
---

# Fluxo PRISMA do snapshot

<img src="./public/images/prisma_flow.png" alt="Fluxo PRISMA do snapshot adjudicado" style="max-height: 480px; width: auto; margin: 0 auto; display: block;" />

<small>Fonte versionada: `research/exports/visualizations/prisma_flow.png`.</small>

---
layout: two-cols
---

# O que a deduplicação significa

::right::

<img src="./public/images/selection_funnel.png" alt="Funil de seleção da revisão" style="max-height: 410px; width: 100%; object-fit: contain;" />

### Leitura correta

- 27 registros foram removidos por identidade DOI/URL.
- Não há remoção automática apenas por igualdade de título.
- Há 232 excedentes apenas por título após a remoção determinística.
- Esses títulos são candidatos a revisão semântica; não equivalem a duplicatas confirmadas.

---

# Panorama descritivo do snapshot

<div class="metric-grid">
  <div><strong>6.399</strong><span>técnica não especificada</span></div>
  <div><strong>1.073</strong><span>assessment</span></div>
  <div><strong>863</strong><span>IA / inteligência artificial</span></div>
  <div><strong>771</strong><span>machine learning</span></div>
  <div><strong>345</strong><span>análise preditiva</span></div>
</div>

<br>

<img src="./public/images/techniques_distribution.png" alt="Distribuição de técnicas no snapshot" style="max-height: 265px; width: 100%; object-fit: contain;" />

<small>Frequências calculadas sobre os 11.877 registros após remoção determinística. As categorias podem se sobrepor e não representam apenas os 18 retidos, qualidade ou eficácia.</small>

---

# Distribuição temporal e fontes

<div class="two-images">
  <div>
    <img src="./public/images/papers_by_year.png" alt="Distribuição de registros por ano" />
    <small>Registros por ano no snapshot versionado.</small>
  </div>
  <div>
    <img src="./public/images/database_coverage.png" alt="Cobertura por base de dados" />
    <small>Registros associados às quatro fontes consultadas.</small>
  </div>
</div>

<small>As visualizações são descritivas; não inferem representatividade, qualidade ou efeito pedagógico.</small>

---
layout: two-cols
---

# Score de relevância: filtro operacional

<img src="./public/images/relevance_distribution.png" alt="Distribuição do score de relevância" style="max-height: 440px; width: 100%; object-fit: contain;" />

<br>

<div class="callout caution">
  <h3>Interpretação</h3>
  <p>O score organiza o processamento automatizado. Ele não é uma medida de qualidade metodológica, não produz ranking e não substitui a leitura das fontes primárias.</p>
</div>

---
layout: two-cols
---

# População retida e MMAT

::right::

## 18 registros

- **17** candidatos empíricos provisórios
- **1** protocolo contextual
- O protocolo contextual não sustenta resultado empírico.

<br>

## MMAT 2018

O ledger atual é uma avaliação por critério, ainda preliminar. A recuperação das fontes, os localizadores e a adjudicação final permanecem necessários.

<br>

> Portanto, não há nota média, ranking ou conclusão global de qualidade metodológica.

---

# O que podemos concluir — e o que não podemos

<div class="conclusion-grid">
  <div class="callout positive">
    <h3>Podemos afirmar</h3>
    <p>O snapshot oferece um mapa auditável das aplicações encontradas, das etapas de seleção e das lacunas documentadas.</p>
  </div>
  <div class="callout caution">
    <h3>Ainda não podemos afirmar</h3>
    <p>Que as técnicas sejam eficazes em geral, que exista superioridade entre modelos ou que o protótipo esteja validado em escolas.</p>
  </div>
</div>

<br>

<small>Resultados de estudos individuais devem ser interpretados nas fontes primárias, considerando população, instrumento, métrica e desenho de avaliação.</small>

---

# Reprodutibilidade sem distribuir o SQLite

<div class="artifact-grid">
  <div><strong>CSV / JSON</strong><span>snapshot e ledgers de decisão</span></div>
  <div><strong>BibTeX</strong><span>referências derivadas do pipeline</span></div>
  <div><strong>Manifesto</strong><span>hashes e escopo dos artefatos</span></div>
  <div><strong>PNG / HTML</strong><span>relatórios e visualizações públicas</span></div>
</div>

<br>

- `research/exports/analysis/papers.csv`
- `research/exports/reports/summary.json`
- `research/exports/reports/reproducibility_manifest.json`

<br>

<small>A bibliografia derivada do pipeline permanece separada das referências teóricas, pedagógicas, metodológicas e técnicas usadas na fundamentação do TCC.</small>

---

# Próximos passos científicos

1. Consolidar a recuperação das fontes e a adjudicação final do MMAT.
2. Revisar as lacunas à luz dos 17 estudos empíricos provisórios.
3. Especificar o protótipo somente após a decisão de escopo e orientação.
4. Definir protocolo e autorização antes de qualquer validação experimental.

<br>

> A revisão sistemática fundamenta as próximas decisões; ela não substitui o protocolo do experimento.

---
layout: center
---

# Obrigado

## Perguntas e discussão

<br>

**Ensino Personalizado de Matemática**

Oportunidades e Técnicas Computacionais

<br>

<small>Fontes públicas: `/research/exports/reports/summary_report.html` · `/results/tcc/` · `/docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md`</small>

<style>
.flow-grid { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 0.55rem; align-items: center; margin: 1rem 0; }
.flow-card { border-radius: 0.8rem; padding: 1rem 0.65rem; text-align: center; color: white; min-height: 5.2rem; display: flex; flex-direction: column; justify-content: center; }
.flow-card strong { font-size: 2rem; line-height: 1.1; }
.flow-card span { font-size: 0.78rem; margin-top: 0.35rem; }
.flow-arrow { font-size: 1.7rem; color: #64748b; }
.blue { background: #2563eb; } .teal { background: #0f766e; } .green { background: #16a34a; }
.amber { background: #d97706; } .orange { background: #ea580c; } .violet { background: #7c3aed; } .indigo { background: #4f46e5; }
.metric-grid, .artifact-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.7rem; }
.metric-grid div, .artifact-grid div { background: #eef2ff; border-radius: 0.7rem; padding: 0.75rem; text-align: center; }
.metric-grid strong, .artifact-grid strong { display: block; font-size: 1.45rem; color: #3730a3; }
.metric-grid span, .artifact-grid span { display: block; font-size: 0.72rem; color: #475569; margin-top: 0.25rem; }
.artifact-grid { grid-template-columns: repeat(4, 1fr); }
.two-images { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; align-items: center; }
.two-images img { max-height: 360px; width: 100%; object-fit: contain; }
.two-images small { display: block; text-align: center; color: #64748b; }
.conclusion-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.callout { border-radius: 0.9rem; padding: 1rem 1.2rem; min-height: 8rem; }
.callout h3 { margin: 0 0 0.45rem; } .callout p { margin: 0; }
.positive { background: #dcfce7; border-left: 0.45rem solid #16a34a; }
.caution { background: #fef3c7; border-left: 0.45rem solid #d97706; }
</style>
