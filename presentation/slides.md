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

<small>Baseline vigente (31/08/2026): 11.904 registros no snapshot, 16 registros retidos (15 empíricos + 1 protocolo contextual). A execução histórica tinha 17; a nova rodada encontrou 23 candidatos e registrou 7 overrides manuais, dos quais 4 aguardam adjudicação de escopo. A mudança alterou a composição da evidência, não apenas a contagem.</small>

<br>

Thales Ferreira Batista · Ciência da Computação

Prof. Dr. Rafael Zanin (IFC) · Prof. Dr. Manassés Ribeiro (IFC)

IFC — Videira

<br>

<small>Projeto de Trabalho de Conclusão (PTC) → TCC</small>

---
layout: two-cols
---

# Bloco 1 — Problema de Pesquisa

::right::

<br>

## Desafio Fundamental

Professores de matemática enfrentam dificuldade em diagnosticar competências individuais em turmas heterogêneas.

**4 Problemas Identificados:**

1. Falta de tempo hábil para intervenções personalizadas
2. Abordagens genéricas prejudicam todos os alunos
3. Literatura científica fragmentada e dispersa
4. Ausência de mapa claro do estado da arte

> Resultados de desempenho reportados em estudos específicos não podem ser tratados como efeito geral: populações, instrumentos, métricas e desenhos variam. A reaplicação documental preliminar do MMAT ao conjunto atual foi registrada por critério; confirmação de fontes, localizadores e adjudicação final ainda estão pendentes.

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
- Apoia um **relato transparente e completo**
- O snapshot é **auditável e reconstruível** a partir dos artefatos versionados

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
3. **Elegibilidade** — Aplicação do filtro operacional e auditoria
4. **Retenção** — Registros mantidos para síntese provisória e rastreabilidade

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

### Critérios de Inclusão Planejados (6; não equivalentes aos gates executados)
1. Publicações acadêmicas revisadas por pares
2. Publicações 2015-2026
3. Foco em técnicas computacionais + educação matemática
4. Dados empíricos e evidências
5. Inglês ou português
6. Pontuação de relevância ≥ 4,0

> Estes são critérios planejados. No snapshot executado, o seletor automatizado exigiu apenas `year_range`, `math_focus` e `computational_techniques`; idioma, tipo documental, revisão por pares e texto completo não foram gates obrigatórios para todos os registros. O score é um filtro operacional, não uma medida de qualidade. A avaliação MMAT atual é preliminar e ainda depende de fontes, localizadores e adjudicação.

---

# Fluxo PRISMA 2020 — Baseline vigente

### IDENTIFICAÇÃO
```
11.904 registros no snapshot consolidado, coletados por 72 consultas canônicas distribuídas entre quatro APIs
```

### DEDUPLICAÇÃO & TRIAGEM
```
11.904 → [-27 DOI/URL redundantes] → 11.877 na triagem
11.877 → [-9.391 excluídos na triagem] → 2.486 na elegibilidade
2.486 → [-2.470 excluídos na elegibilidade] → 16 registros retidos
        (15 empíricos + 1 protocolo contextual)
```

### ELEGIBILIDADE
```
23 candidatos no limiar operacional
23 → [-7 overrides manuais após auditoria] → 16 REGISTROS RETIDOS
                               (15 empíricos + 1 protocolo contextual)
```

### TAXA FINAL
- **16 de 11.904** = **0,13%** de retenção no snapshot atual
- A taxa descreve este snapshot; não é uma medida de qualidade científica.

---
layout: center
---

# Fluxo PRISMA — visualização auditável

<img src="./public/images/prisma_flow.png" alt="Fluxo PRISMA do snapshot operacional atual" style="max-height: 430px; width: auto; margin: 0 auto; display: block;" />

<small>Fonte: `research/exports/visualizations/prisma_flow.png`. O diagrama separa a identificação bruta (11.904) do corpus após remoções determinísticas por DOI/URL (11.877).</small>

---
layout: two-cols
---

# Funil de Redução

::right::

<br>

```
TOPO     11.904 registros
  ↓ 27 DOI/URL redundantes removidos
  ↓ 9.391 excluídos na triagem
         2.486 avançaram
  ↓ 2.470 excluídos na elegibilidade
BASE     16 registros retidos
         15 empíricos + 1 protocolo contextual
         Taxa: 0,13%
```

<br>

> As exclusões representam decisões de triagem e pertinência. O score é um filtro operacional e não constitui garantia de qualidade metodológica.

---
layout: center
---

# Funil de seleção — visualização auditável

<img src="./public/images/selection_funnel.png" alt="Funil de seleção do snapshot operacional atual" style="max-height: 430px; width: auto; margin: 0 auto; display: block;" />

<small>Fonte: `research/exports/visualizations/selection_funnel.png`. As etapas mostram registros, não estudos únicos semanticamente deduplicados por título.</small>

---

# Métricas Quantitativas

| Métrica | Valor |
|---------|-------|
| Total no snapshot | 11.904 |
| Remoções determinísticas por DOI/URL | 27 |
| Excluídos na triagem | 9.391 |
| Avançaram à elegibilidade | 2.486 |
| Excluídos na elegibilidade | 2.470 |
| **Registros retidos no snapshot** | **16** |
| Estudos empíricos na síntese | 15 |
| Protocolo contextual fora da síntese empírica | 1 |
| Taxa de inclusão final | **0,13%** |
| Excluídos na triagem / identificação | 78,89% |
| Avançaram da triagem / identificação | 20,88% |
| Excluídos na elegibilidade / elegibilidade | 99,36% |
| Incluídos / elegibilidade | 0,64% |
| Bases consultadas | 4 |
| Consultas bilíngues | 72 |
| Período | 2015–2026 |
| Grupos de DOI repetido na auditoria | 25 |

---
layout: center
---

# Perfil do corpus — ano e relevância

<div style="display: flex; gap: 1.5rem; align-items: center; justify-content: center;">
  <img src="./public/images/papers_by_year.png" alt="Distribuição dos registros por ano" style="width: 48%; max-height: 360px; object-fit: contain;" />
  <img src="./public/images/relevance_distribution.png" alt="Distribuição dos escores de relevância" style="width: 48%; max-height: 360px; object-fit: contain;" />
</div>

<small>Fontes: `research/exports/visualizations/papers_by_year.png` e `research/exports/visualizations/relevance_distribution.png`. O score descreve a seleção operacional, não a qualidade metodológica.</small>

---
layout: two-cols
---

# Bloco 4 — Resultados

::right::

<br>

## Distribuição por Base no corpus analítico

Após a remoção determinística das identidades DOI/URL, o corpus analítico
possui 11.877 registros. As contagens abaixo não são uma segunda identificação
de 11.904 registros; são a distribuição do conjunto que segue para triagem.

```
Crossref:         5.049 (42,5%)
OpenAlex:         3.057 (25,7%)
Semantic Scholar: 1.931 (16,3%)
CORE:             1.840 (15,5%)
──────────────────────────
TOTAL:            11.877
```

<br>

### Insights

1. Crossref é a maior contribuição do corpus analítico
2. OpenAlex amplia a cobertura multidisciplinar
3. Semantic Scholar complementa a descoberta em computação e educação
4. CORE menor (foco acesso aberto)

---
layout: center
---

# Distribuição do corpus por base

<img src="./public/images/database_coverage.png" alt="Distribuição de registros por base no corpus analítico" style="max-height: 430px; width: auto; margin: 0 auto; display: block;" />

<small>Fonte: `research/exports/visualizations/database_coverage.png`. Denominador: 11.877 registros após a remoção determinística de identidades DOI/URL.</small>

---

# Os 16 Registros — Síntese e Contexto

O snapshot operacional retém 16 registros: 15 estudos empíricos compõem
provisoriamente o escopo da síntese, e o protocolo 6921 é mantido apenas para
contexto e rastreabilidade, sem resultados empíricos ou avaliação MMAT empírica.

### Exemplos Representativos

**Pejic et al. (2021)** — modelo multiclasses de ML
- Finalidade: Estimar proficiência matemática
- Limite: resultado vinculado a avaliação internacional específica

**Zhang et al. (2025)** — Deep Learning + Knowledge Graph
- Finalidade: Personalização de trajetórias
- Limite: registro atual requer confirmação em fonte primária

**Tjahyadi (2025)** — ML Supervisionado
- Finalidade: Predição de desempenho
- Resultado reportado no registro: 75% de acurácia; não é efeito geral

<br>

### Padrões Visíveis
- As etiquetas do pipeline registram Machine Learning em 11/16 registros do snapshot (68,8%)
- Predictive Analytics aparece em 9/16 registros do snapshot (56,3%)
- No subconjunto empírico (n=15), essas frequências são 11/15 (73,3%) e 9/15 (60,0%)
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

> Denominador: a tabela preserva as frequências do snapshot operacional (n=16), para manter a rastreabilidade do export. Para a síntese empírica (n=15), os respectivos valores são ML 11 (73,3%), Predictive Analytics 9 (60,0%), Assessment 7 (46,7%), Learning Analytics 7 (46,7%), Adaptive Learning 5 (33,3%), IA 3 (20,0%) e Intelligent Tutoring 3 (20,0%).

---
layout: center
---

# Técnicas identificadas — visualização

<img src="./public/images/techniques_distribution.png" alt="Distribuição das técnicas computacionais identificadas" style="max-height: 430px; width: auto; margin: 0 auto; display: block;" />

<small>Fonte: `research/exports/visualizations/techniques_distribution.png`. As categorias são sobrepostas e derivadas dos metadados do snapshot.</small>

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

As categorias são sobrepostas e foram extraídas dos metadados do snapshot. Não foi calculada acurácia média, ganho médio ou efeito agregado: as métricas, populações e tarefas são heterogêneas, a confirmação em fonte primária ainda é necessária para parte dos registros, a reaplicação documental preliminar do MMAT está registrada e sua consolidação depende de fontes, localizadores e adjudicação; o protocolo 6921 está fora da síntese empírica.

### ⚠️ Limite da inferência

Não é possível concluir, a partir deste snapshot, que os sistemas produzem ganhos de 10–20%, que uma acurácia é transferível entre escolas ou que há uma estimativa confiável de viés de publicação. Essas hipóteses exigem leitura completa, avaliação metodológica e síntese apropriada.

---

# EIXO 4 — Limitações Identificadas

### 4 Categorias de Limitações

| Categoria | Principais | Impacto |
|-----------|-----------|---------|
| **Técnicas** | Explicabilidade e transferibilidade dos modelos precisam de validação | Alto |
| **Pedagógicas** | Relação entre indicador computacional e aprendizagem exige interpretação docente | Crítico |
| **Metodológicas** | Desenhos, populações e métricas heterogêneos; MMAT preliminar registrado e aguardando adjudicação | Alto |
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

# Cronograma — estado do projeto

::right::

<br>

```text
31/08/2026
FASE 1  Baseline da revisão reconciliado: 11.904 registros, 16 retidos (15 empíricos + 1 protocolo contextual)
        MMAT preliminar registrado; adjudicação e fontes restantes pendentes
FASE 2  Protótipo: sequência e prazo aguardam decisão científica
FASE 3  Validação experimental: não iniciada; prazo não definido
```

<br>

| Fase | Período | Status |
|------|---------|--------|
| **1** | Até 31/08/2026 | ✅ Baseline reconciliado; MMAT preliminar |
| **2** | A definir | ⏳ Aguardando cenário científico |
| **3** | A definir | ⏳ Não iniciada |

---

# Impacto pretendido — hipóteses para validação

### Para Professores
- Possível redução do tempo de avaliação, a validar em contexto real
- Apoio à precisão diagnóstica, sem substituir a interpretação docente
- Recomendações explicáveis, cuja confiança ainda precisa ser avaliada

### Para Alunos
- Possibilidade de intervenções mais contextualizadas, a validar
- Engajamento e motivação como desfechos a medir
- Autonomia de aprendizagem como hipótese pedagógica, não resultado observado

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
- 11.904 registros → 16 registros atuais (15 empíricos + 1 protocolo contextual)
- 23 candidatos no limiar operacional → 7 overrides manuais registrados (4 pendentes) → 16 retidos operacionalmente
- 4 bases · 72 queries · PRISMA 2020

**Achados principais:**
1. No snapshot, Machine Learning aparece em 11/16 registros e Predictive Analytics em 9/16; na síntese empírica, 11/15 e 9/15
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
