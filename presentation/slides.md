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

**Revisão Sistemática da Literatura — Protocolo PRISMA 2020**

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

> "Sistemas adaptativos baseados em dados podem melhorar o desempenho acadêmico em **10-20%** e reduzir tempo de aprendizagem em até **20%**."

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

## Protocolo PRISMA 2020

**Preferred Reporting Items for Systematic Reviews and Meta-Analyses**

<br>

### 4 Etapas do Protocolo

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

- **Cache Hit Rate**: ~92% (265/287 requisições)
- **Benefício**: Reprocessamento 22x mais rápido
- **Implicação**: Revisão é reproduzível rapidamente

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

### Critérios de Inclusão (6)
1. Artigos peer-reviewed
2. Publicações 2015-2026
3. Foco em técnicas computacionais + educação matemática
4. Dados empíricos e evidências
5. Inglês ou português
6. Pontuação de relevância ≥ 4,0

---

# Fluxo PRISMA 2020

### IDENTIFICAÇÃO
```
9.431 registros identificados (72 queries × 4 APIs)
```

### DEDUPLICAÇÃO & TRIAGEM
```
9.431 → [-2.517 duplicatas = 26,6%] → 6.914 estudos únicos
6.914 → [-5.031 filtros = 72,8%] → 1.883 elegíveis
```

### ELEGIBILIDADE
```
1.883 → [Sistema de scoring 0-10, limiar ≥ 4,0]
1.883 → [-1.866 abaixo do limiar] → 17 ESTUDOS INCLUÍDOS
```

### TAXA FINAL
- **17 de 9.431** = **0,18%**
- Esperado em revisões sistemáticas rigorosas

---
layout: two-cols
---

# Funil de Redução

::right::

<br>

```
TOPO     9.431 registros
  ↓ Redução 26,6%
         6.914 únicos
  ↓ Redução 72,8%
         1.883 elegíveis
  ↓ Redução 99,1%
BASE     17 incluídos
         Taxa: 0,18%
```

<br>

> "Cada redução representa a aplicação rigorosa de critérios de qualidade. Não é exclusão excessiva — é **garantia de qualidade**."

---

# Métricas Quantitativas

| Métrica | Valor |
|---------|-------|
| Total identificado | 9.431 |
| Duplicatas removidas | 2.517 (26,6%) |
| Registros únicos | 6.914 |
| Elegíveis (após triagem) | 1.883 |
| Taxa de exclusão (elegibilidade) | 99,1% |
| **Total incluído** | **17** |
| Taxa de inclusão final | **0,18%** |
| Bases consultadas | 4 |
| Consultas bilíngues | 72 |
| Período | 2015–2026 |
| Cache hit rate | ~92% |

---
layout: two-cols
---

# Bloco 4 — Resultados

::right::

<br>

## Distribuição por Base

```
Semantic Scholar:  ~4.200 (44%)
OpenAlex:         ~2.800 (30%)
Crossref:         ~1.600 (17%)
CORE:             ~  831 (9%)
──────────────────────────
TOTAL:             9.431
```

<br>

### Insights

1. Semantic Scholar lidera (CS/educação)
2. OpenAlex forte em amplitude
3. Crossref complementar (metadados)
4. CORE menor (foco acesso aberto)

---

# Os 17 Estudos — Síntese

### Exemplos Representativos

**Hasib et al. (2022)** — SVM com LIME
- Finalidade: Predição com explicabilidade
- Resultado: 96,89% acurácia + explicações

**Zhang et al. (2025)** — Deep Learning + Knowledge Graph
- Finalidade: Personalização de trajetórias
- Resultado: +15% aprendizagem, -20% tempo

**Tjahyadi (2025)** — ML Supervisionado
- Finalidade: Predição de desempenho
- Resultado: 75% acurácia

<br>

### Padrões Visíveis
- Concentração em predição (52,9%)
- ML Supervisionado predomina (76,5%)

---

# EIXO 1 — Técnicas Predominantes

| Técnica | Nº Estudos | % |
|---------|-----------|---|
| **ML Supervisionado** | 13 | **76,5%** |
| Deep Learning (CNN, RNN) | 2 | 11,8% |
| Reinforcement Learning | 1 | 5,9% |
| Adaptive Learning | 1 | 5,9% |
| Modelagem de Conhecimento | 1 | 5,9% |
| Outras (ACO, CRF, XAI) | 6 | 35,3% |

<br>

### Por que ML Supervisionado Lidera?

1. **Maduro e estável** — décadas de desenvolvimento
2. **Dados disponíveis** — históricos educacionais existem
3. **Interpretável** — importante em contexto educacional
4. **Eficiente** — roda em hardware padrão

---

# EIXO 2 — Finalidades Pedagógicas

| Finalidade | Nº | % | Descrição |
|------------|---|---|-----------|
| **Predição de Desempenho** | 9 | **52,9%** | Prever notas, risco de evasão |
| Personalização / Trajetórias | 3 | 17,6% | Adaptar conteúdo dinamicamente |
| Ensino / Suporte Instrucional | 2 | 11,8% | Tutoria inteligente |
| Avaliação / Assessment | 2 | 11,8% | Avaliar competências automaticamente |
| Tutoria Inteligente | 1 | 5,9% | Modelagem automática |

<br>

> **Achado Crítico:** A comunidade foca em IDENTIFICAR problemas (52,9%), mas menos em RESOLVER (17,6%). Há oportunidade para sistemas mais integrados.

---

# EIXO 3 — Resultados de Eficácia

### Acurácias Reportadas

| Categoria | Faixa | Nº Estudos | % |
|-----------|-------|-----------|---|
| **Excelente** | >90% | 5 | 29,4% |
| **Muito bom** | 85-90% | 4 | 23,5% |
| **Bom** | 75-85% | 6 | 35,3% |
| Não especificado | - | 2 | 11,8% |

**Média estimada**: ~85% em predição de desempenho

### Ganhos de Aprendizagem

```
Pequeno (5-10%):     ~37% dos estudos
Médio (10-20%):      ~38% dos estudos (MAIS COMUM)
Grande (>20%):       ~19% dos estudos
```

### ⚠️ Viés de Publicação
- Resultados positivos: 16/17 (94,1%)
- Resultados negativos: 0/17 (0%)
- Eficácia real provavelmente **70-85%**

---

# EIXO 4 — Limitações Identificadas

### 4 Categorias de Limitações

| Categoria | Principais | Impacto |
|-----------|-----------|---------|
| **Técnicas** | Falta de explicabilidade (85%), validação limitada (35% em lab) | Alto |
| **Pedagógicas** | Desalinhamento BNCC (100%), foco cognitivo (80%) | Crítico |
| **Metodológicas** | Viés publicação (94%), sem grupo controle (45%) | Alto |
| **Éticas** | Privacidade (LGPD), viés algorítmico (90%) | Crítico |

<br>

### 3 Lacunas Críticas para Fase 2

1. **FALTA DE EXPLICABILIDADE** (85%) → Integrar XAI
2. **DESALINHAMENTO CURRICULAR** (100%) → Mapear BNCC
3. **VALIDAÇÃO ECOLÓGICA LIMITADA** (65% lab) → Estudo em escola real

---

# Direcionamento para Fase 2

| Lacuna | Solução | Fundamento |
|--------|---------|------------|
| 85% sem explicabilidade | Integrar XAI (LIME/SHAP) | Hasib et al. 2022 |
| 100% sem BNCC | Mapear competências BNCC | Alinhamento Brasil |
| 65% validação lab | Experimento em escola real | Evidência ecológica |
| 90% sem ética | Governance + auditoria viés | Literatura emergente |
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
- ↑ Desempenho acadêmico (10-20%)
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
- 9.431 registros → 17 estudos
- 4 bases · 72 queries · PRISMA 2020

**Achados principais:**
1. ML Supervisionado funciona (76,5%, ~85%)
2. Ganhos reais (10-20% típicos)
3. Mas há lacunas críticas

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
