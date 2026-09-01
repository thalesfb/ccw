---
theme: default
title: "TCC — Ensino Personalizado de Matemática"
info: "Revisão Sistemática da Literatura — PRISMA 2020"
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

**Revisão Sistemática da Literatura — Relato orientado pelo PRISMA 2020**

<small>Baseline vigente (31/08/2026): 11.904 registros no snapshot, 16 estudos incluídos. A execução histórica tinha 17; a nova rodada encontrou 23 candidatos e removeu 7 falsos positivos. A mudança alterou a composição da evidência, não apenas a contagem.</small>

<br>

Thales Ferreira Batista · Ciência da Computação

Prof. Dr. Rafael Zanin (IFC) · Prof. Dr. Manassés Ribeiro (IFC)

IFC — Videira

<br>

<small>Projeto de Trabalho de Conclusão (PTC) → TCC</small>

---
layout: two-cols
---

# Bloco 1 — Problema de PesquisA

::right::

<br>

## Desafio Fundamental

Professores de matemática enfrentam dificuldade em diagnosticar competências individuais em turmas heterogêneas.

**4 Problemas Identificados:**

1. Falta de tempo hábil para intervenções personalizadas
2. Abordagens genéricas prejudicam todos os alunos
3. Literatura científica fragmentada e dispersa
4. Ausência de mapa claro do estado da arte

> Resultados de desempenho reportados em estudos específicos não podem ser tratados como efeito geral: populações, instrumentos, métricas e desenhos variam, e a avaliação MMAT do conjunto atual ainda está pendente.

---

# 4 Perguntas de Pesquisa

As perguntas que fundamentam esta revisão sistemática:

<br>

| # | Pergunta | Foco |
|---|----------|------|
| **RQ1** | Quais técnicas computacionais estão sendo aplicadas na educação matemática? | Estado da arte |
| **RQ2** | Como essas técnicas têm sido validadas em contextos reais? | Metodologias |
| **RQ3** | Que lacunas e desafios existem que precisam ser preenchidos? | Problemas |
| **RQ4** | Quais direcionamentos para desenvolver ferramentas mais eficazes? | Síntese |

<br>

> Estas 4 perguntas são o **fio condutor** de toda apresentação.

---
layout: two-cols
---

# Bloco 2 — Objetivos

::right::

<br>

## Objetivo Geral

> Mapear e analisar sistematicamente as aplicações de técnicas computacionais — especialmente **machine learning**, **learning analytics** e **sistemas tutores inteligentes** — no contexto da educação matemática, identificando **tendências, lacunas de pesquisa e oportunidades** para o desenvolvimento de um modelo computacional (MVP) que auxilie professores na **personalização do ensino** e no **diagnóstico de competências**.

<br>

### Por que PRISMA 2020?

- Padrão internacional para revisões sistemáticas
- Garante **rigor, transparência e reprodutibilidade**
- Resultados são **auditáveis e replicáveis**

---

# 6 Objetivos Específicos

| OE | Objetivo | Descrição |
|----|----------|-----------|
| **OE1** | Revisão sistemática PRISMA 2020 | Literatura 2015-2026 (últimos 12 anos) |
| **OE2** | Identificar categorias de IA/ML | Técnicas computacionais aplicadas |
| **OE3** | Classificar por finalidade | Tutoria, diagnóstico, avaliação, personalização |
| **OE4** | Analisar metodologias de avaliação | Boas práticas e limitações |
| **OE5** | Mapear lacunas de pesquisa | Desafios e direções prioritárias |
| **OE6** | Criar pipeline automatizado | Contribuir para futuras revisões |

<br>

> "Estes 6 objetivos trabalham juntos para responder nossas 4 perguntas de pesquisa."

---
layout: two-cols
---

# Bloco 3 — Metodologia

::right::

<br>

## Relato orientado pelo PRISMA 2020

**Preferred Reporting Items for Systematic Reviews and Meta-Analyses**

<br>

### 4 Etapas do Fluxo Relatado

1. **Identificação** — Busca em múltiplas bases
2. **Triagem** — Filtros iniciais de inclusão/exclusão
3. **Elegibilidade** — Avaliação rigorosa com scoring
4. **Inclusão** — Seleção final dos estudos

<br>

### Recorte Temporal

- **Período**: 2015–2026 (data corte: 31/08/2026)
- **Razão**: Era da IA Educacional, maturidade do ML

---

# Estratégia de Busca — 3 Camadas

### Camada 1: BASE MATEMÁTICA
```
Inglês:    "mathematics", "math"           [2 termos]
Português: "matemática"                    [1 termo]
```

### Camada 2: TÉCNICAS COMPUTACIONAIS (12 termos)
```
adaptive / personalized / tutoring / analytics / mining /
machine learning / ai / assessment / student modeling /
predictive / intelligent tutor / artificial intelligence
+ Equivalentes em português
```

### Camada 3: DOMÍNIO EDUCACIONAL
```
Inglês:    "education", "learning"         [2 termos]
Português: "educacao", "ensino"            [2 termos]
```

### Estrutura da Query
```
"termo_base" AND "termo_tecnica" AND "termo_educacional"
→ 72 consultas bilíngues (48 EN + 24 PT)
```

---

# 4 Bases de Dados Complementares

| Base | Especialidade | Força Principal |
|------|---------------|-----------------|
| **Semantic Scholar** | Ciência da Computação | Métricas de influência |
| **OpenAlex** | Aberta e abrangente | Amplitude de cobertura |
| **Crossref** | Precisão bibliográfica | DOIs, metadados precisos |
| **CORE** | Acesso Aberto | Artigos com acesso livre |

<br>

### Sistema de Cache

- O cache persistente reutiliza respostas quando a entrada ainda está disponível.
- O contador é acumulado por entrada e depende do histórico de execução e expiração.
- Não foi usado como evidência de qualidade, inclusão ou reprodutibilidade exata do snapshot.

---

# Critérios de Seleção — PICOS

| Elemento | Descrição |
|----------|-----------|
| **P — População** | Estudantes de matemática (EF, EM, superior) |
| **I — Intervenção** | Técnicas computacionais (ML, IA, LA, STI) |
| **C — Comparação** | Abordagens tradicionais/quando aplicável |
| **O — Outcomes** | Desempenho, diagnóstico, personalização |
| **S — Study Design** | Empíricos, quasi-experimentais, estudos de caso |

<br>

### Critérios de Inclusão Planejados (6)
1. Artigos peer-reviewed
2. Publicações 2015-2026
3. Foco em técnicas computacionais + educação matemática
4. Dados empíricos e evidências
5. Inglês ou português
6. Pontuação de relevância ≥ 4,0

---

# Fluxo PRISMA 2020 — Baseline vigente

### IDENTIFICAÇÃO
```
11.904 registros no snapshot consolidado (72 queries × 4 APIs)
```

### DEDUPLICAÇÃO & TRIAGEM
```
11.904 → [-9.413 excluídos na triagem] → 2.491 avançaram
2.491 → [-2.475 excluídos na elegibilidade] → 16 incluídos
```

### ELEGIBILIDADE
```
23 candidatos no limiar operacional
23 → [-7 falsos positivos após auditoria] → 16 ESTUDOS INCLUÍDOS
```

### TAXA FINAL
- **16 de 11.904** = **0,13%** no snapshot atual
- A taxa descreve este snapshot; não é uma medida de qualidade científica.

---
layout: two-cols
---

# Funil de Redução

::right::

<br>

```
TOPO     11.904 registros
  ↓ 9.413 excluídos na triagem
         2.491 avançaram
  ↓ 2.475 excluídos na elegibilidade
BASE     16 incluídos
         Taxa: 0,13%
```

<br>

> As exclusões representam decisões de triagem e pertinência. O score é um filtro operacional e não constitui garantia de qualidade metodológica.

---

# Métricas Quantitativas

| Métrica | Valor |
|---------|-------|
| Total no snapshot | 11.904 |
| Remoções pela flag de duplicata | 0 |
| Excluídos na triagem | 9.413 |
| Avançaram à elegibilidade | 2.491 |
| Excluídos na elegibilidade | 2.475 |
| **Total incluído** | **16** |
| Taxa de inclusão final | **0,13%** |
| Bases consultadas | 4 |
| Consultas bilíngues | 72 |
| Período | 2015–2026 |
| Grupos de DOI repetido na auditoria | 24 |

---
layout: two-cols
---

# Bloco 4 — Resultados

::right::

<br>

## Distribuição por Base

```
Crossref:         5.055 (42,5%)
OpenAlex:         3.064 (25,7%)
Semantic Scholar: 1.940 (16,3%)
CORE:             1.845 (15,5%)
──────────────────────────
TOTAL:            11.904
```

<br>

### Insights

1. Semantic Scholar lidera (CS/educação)
2. OpenAlex forte em amplitude
3. Crossref complementar (metadados)
4. CORE menor (foco acesso aberto)

---

# Os 16 Estudos — Síntese

### Exemplos Representativos

**Pejic et al. (2021)** — modelo multiclasses de ML
- Finalidade: Estimar proficiência matemática
- Limite: resultado vinculado a avaliação internacional específica

**Zhang et al. (2025)** — Deep Learning + Knowledge Graph
- Finalidade: Personalização de trajetórias
- Limite: registro atual requer confirmação em fonte primária

**Tjahyadi (2025)** — ML Supervisionado
- Finalidade: Predição de desempenho
- Resultado: 75% acurácia

<br>

### Padrões Visíveis
- As etiquetas do pipeline registram Machine Learning em 11/16 estudos (68,8%)
- Predictive Analytics aparece em 9/16 (56,3%)
- As categorias são sobrepostas e descrevem metadados, não qualidade metodológica

---

# EIXO 1 — Técnicas Predominantes

| Técnica | Nº Estudos | % |
|---------|-----------|---|
| **Machine Learning** | 11 | **68,8%** |
| Predictive Analytics | 9 | 56,3% |
| Assessment | 8 | 50,0% |
| Learning Analytics | 7 | 43,8% |
| Adaptive Learning | 6 | 37,5% |
| AI/Artificial Intelligence | 4 | 25,0% |
| Intelligent Tutoring | 3 | 18,8% |

<br>

> As etiquetas podem coexistir no mesmo estudo. A classificação foi extraída de título/resumo e precisa ser confirmada na leitura primária; ela não permite concluir que todos os modelos sejam supervisionados.

---

# EIXO 2 — Finalidades e funções representadas

| Finalidade | Nº | % | Descrição |
|------------|---|---|-----------|
| **Predictive Analytics** | 9 | **56,3%** | Estimar desempenho ou proficiência |
| Assessment | 8 | 50,0% | Avaliar desempenho ou estados do estudante |
| Learning Analytics | 7 | 43,8% | Analisar dados educacionais |
| Adaptive Learning | 6 | 37,5% | Apoiar personalização ou adaptação |
| Intelligent Tutoring | 3 | 18,8% | Apoiar tutoria ou feedback |

<br>

> **Leitura crítica:** o snapshot concentra etiquetas preditivas, mas elas não demonstram resolução de problemas pedagógicos nem eficácia de intervenção. A síntese não deve transformar frequência de técnica em recomendação automática.

---

# EIXO 3 — Evidência de avaliação

| Método de avaliação identificado | Nº de estudos | % |
|----------------------------------|---------------|---:|
| Desempenho | 10 | 62,5% |
| Análise estatística | 9 | 56,3% |
| Feedback de usuários | 5 | 31,3% |

As categorias são sobrepostas e foram extraídas dos metadados do snapshot. Não foi calculada acurácia média, ganho médio ou efeito agregado: as métricas, populações e tarefas são heterogêneas, a confirmação em fonte primária ainda é necessária para seis registros e a reaplicação do MMAT está pendente.

### ⚠️ Limite da inferência

Não é possível concluir, a partir deste snapshot, que os sistemas produzem ganhos de 10–20%, que uma acurácia é transferível entre escolas ou que há uma estimativa confiável de viés de publicação. Essas hipóteses exigem leitura completa, avaliação metodológica e síntese apropriada.

---

# EIXO 4 — Limitações Identificadas

### 4 Categorias de Limitações

| Categoria | Principais | Impacto |
|-----------|-----------|---------|
| **Técnicas** | Explicabilidade e transferibilidade dos modelos precisam de validação | Alto |
| **Pedagógicas** | Relação entre indicador computacional e aprendizagem exige interpretação docente | Crítico |
| **Metodológicas** | Desenhos, populações e métricas heterogêneos; MMAT atual pendente | Alto |
| **Documentais** | Seis registros atuais ainda exigem confirmação bibliográfica primária | Alto |

<br>

### 3 Lacunas Críticas para Fase 2

1. **EXPLICABILIDADE E INCERTEZA** → Integrar explicações e comunicar limites
2. **ALINHAMENTO CURRICULAR** → Mapear BNCC sem inferir equivalência automática
3. **VALIDAÇÃO ECOLÓGICA** → Testar em contextos escolares diversos

---

# Direcionamento para Fase 2

| Lacuna | Solução | Fundamento |
|--------|---------|------------|
| Explicabilidade e incerteza não consolidadas | Integrar explicações e auditoria de viés | Avaliação metodológica futura |
| Ausência de alinhamento curricular explícito | Mapear competências BNCC | Fundamentação pedagógica |
| Validação contextual limitada | Experimento em escola real | Evidência ecológica |
| Metadados e DOI ainda pendentes em seis registros | Confirmar fontes primárias | Auditoria bibliográfica |
| Foco cognitivo | Módulo metacognitivo | Autonomia estudantil |

<br>

### 5 Direcionamentos

1. **Sistema Explicável** — XAI integrada desde design
2. **Alinhamento BNCC** — Competências matemáticas
3. **Validação Ecológica** — Grupo controle em escola real
4. **Módulo Metacognitivo** — Ensinar como aprender
5. **Reprodutibilidade** — Código e dados abertos

---
layout: two-cols
---

# Cronograma — 3 Fases

::right::

<br>

```
2025                                    2026
Mar└─────────────────────────────┘Nov  Feb└────────────────┘Jul  Jul└──────────────┘Nov
│ FASE 1: Revisão Sistemática      │     │ FASE 2: Protótipo      │  │ FASE 3: Validação │
│ PTC Defendido                    │     │ Em planejamento        │  │ Em planejamento   │
└──────────────────────────────────┘     └────────────────────────┘  └──────────────────┘
```

<br>

| Fase | Período | Status |
|------|---------|--------|
| **1** | Mar-Nov 2025 | ✅ Concluída |
| **2** | Fev-Jul 2026 | 🟢 Planejada |
| **3** | Jul-Nov 2026 | ⏳ Planejada |

---

# Impacto Esperado

### Para Professores
- ↓ Tempo em avaliação (libera para ensino)
- ↑ Precisão diagnóstica
- ↑ Confiança em recomendações (XAI)

### Para Alunos
- ↑ Possibilidade de intervenções mais contextualizadas (a validar)
- ↑ Engajamento e motivação
- ↑ Autonomia de aprendizagem

### Para Comunidade Científica
- Referência em revisão sistemática
- Protótipo com código aberto
- Validação em contexto brasileiro

---
layout: two-cols
---

# Síntese Final

::right::

<br>

## Recapitulação

> "Como diagnosticar e personalizar o ensino de matemática em larga escala?"

**Consultamos a literatura:**
- 11.904 registros → 16 estudos atuais
- 23 candidatos no limiar operacional → 7 falsos positivos removidos → 16 incluídos
- 4 bases · 72 queries · PRISMA 2020

**Achados principais:**
1. Machine Learning aparece em 11/16 registros e Predictive Analytics em 9/16
2. As medidas de avaliação são heterogêneas e não sustentam efeito agregado
3. Permanecem lacunas de explicabilidade, contexto, currículo e avaliação metodológica

**Nossa contribuição:**
- XAI integrada · Alinhamento BNCC
- Validação em escola real · Dados abertos

---

# Agradecimentos

<br>

## Obrigado pela atenção!

**Contatos:**

- 📧 thales.batista@estudantes.ifc.edu.br
- 💻 https://github.com/thalesfb

<br>

### Perguntas & Discussão

<br>

<small>IFC — Videira · Ciência da Computação · 2026</small>
