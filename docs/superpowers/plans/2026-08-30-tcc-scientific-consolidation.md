# TCC Scientific Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fortalecer cientificamente o TCC e preparar uma decisão informada com a orientação sobre o nível adequado de prototipação/implementação, preservando todo o trabalho experimental já realizado.

**Architecture:** O plano tem duas partes. A Parte I produz evidências independentes do cenário final: auditoria do protocolo da revisão, auditoria científica do texto, avaliação de recursos consolidados na literatura e proposta de atualização para 2026. A Parte II só é executada depois do gate com o orientador e possui três caminhos possíveis: revisão/especificação, demonstração com modelos ou artefatos consolidados, ou experimento próprio. Nenhuma ferramenta ou agente pode escolher esse caminho autonomamente.

**Tech Stack:** LaTeX/abnTeX2-IFC, Python 3.11, SQLite, pytest, GitHub Actions, pipeline `research/`, artefatos `prototype/`, PRISMA 2020, PRISMA-S, MMAT 2018.

**Spec:** issue #24 (escopo científico), issue #7 (linha experimental preservada), issue #25 (título) e issue #26 (possível atualização 2026).

## Global Constraints

- O caminho científico futuro está **pendente de decisão com a orientação**.
- Não remover, arquivar, desativar ou reclassificar como inútil código, testes, documentos ou dados experimentais antes dessa decisão.
- O fato de o TCC ainda não possuir evidência experimental própria não implica que experimentação esteja proibida; implica apenas que ela não pode ser descrita como já realizada.
- Reutilização de modelos, métodos, pesos, notebooks ou artefatos consolidados na literatura é um cenário legítimo a avaliar, desde que licença, proveniência, compatibilidade e limites de inferência sejam explícitos.
- Treinamento do zero só deve ser feito se responder a uma necessidade científica clara e aprovada, não apenas para aumentar volume de implementação.
- Nenhuma métrica técnica será apresentada como evidência automática de aprendizagem ou eficácia pedagógica.
- Desempenho observado, proficiência, competência e aprendizagem permanecem conceitos distintos.
- O limiar de relevância da revisão não será tratado como qualidade metodológica.
- MMAT permanece por critério Q1–Q5, sem escore total ou ranking.
- LLMs/agentes podem auditar, comparar, executar testes e preparar evidências; decisões de escopo, interpretação, inclusão/exclusão, MMAT e redação científica final exigem revisão humana.
- O objetivo da revisão textual é qualidade acadêmica e autoria responsável, não evasão de detectores de IA.
- Nenhum PR será mesclado automaticamente.

---

## File Structure / Responsibilities

### Núcleo acadêmico

- `results/tcc/pretextuais/capa.tex` — título, alterado somente após gate com orientação.
- `results/tcc/pretextuais/resumo.tex` — resumo e abstract, revisados após o escopo final.
- `results/tcc/conteudo/introducao.tex` — problema, objetivos, justificativa e delimitação.
- `results/tcc/conteudo/fundamentacao.tex` — conceitos e fundamentação.
- `results/tcc/conteudo/metodologia.tex` — protocolo realmente executado e, se houver, procedimento experimental efetivamente realizado.
- `results/tcc/conteudo/resultadosesperados.tex` — revisão sistemática e síntese.
- `results/tcc/conteudo/prototipo.tex` — especificação e eventual descrição de demonstração/implementação, conforme gate.
- `results/tcc/conteudo/resultados.tex` — resultados/discussão; não antecipar resultados experimentais.
- `results/tcc/conteudo/conclusao.tex` — conclusões limitadas ao que foi demonstrado.
- `results/tcc/postextuais/apendice.tex` — PRISMA final.

### Revisão sistemática

- `research/src/search_terms.py` — consultas canônicas atuais.
- `research/src/config.py` — configuração atual; contém divergência temporal a ser auditada.
- `research/src/pipeline/run.py` — execução do pipeline.
- `research/systematic_review.sqlite` e `research/exports/` — evidências do corpus, quando disponíveis.
- `research/tests/` — regressões de pesquisa, bibliografia e metodologia.

### Linha experimental existente — preservar

- `prototype/` — código, contratos, configuração e testes experimentais já produzidos.
- `docs/TCC_PROTOTYPE_DELIVERY_PLAN.md` — plano experimental histórico/possível.
- `docs/TCC_PROTOTYPE_SCIENTIFIC_DECISIONS.md` — decisões da linha experimental.
- `docs/TCC_EXPERIMENTAL_DESIGN.md` — desenho experimental.
- `docs/TCC_DATA_SOURCE_DECISION.md` — análise/decisão de dados.
- `docs/TCC_PROFILE_AND_EXPLAINABILITY.md` — perfil e explicabilidade.
- `research/tests/test_experiment_contract.py` — contrato do experimento; manter ativo enquanto a orientação não decidir o contrário.
- `.github/workflows/tcc-quality.yml` — manter testes de `research/` e `prototype/` por enquanto.

---

# PARTE I — trabalho que pode avançar antes da decisão de escopo

### Task 1: Registrar governança correta e preservar o trabalho existente

**Files:**
- Modify: `docs/TCC_REVISION_SCOPE.md`
- Review only: `.github/workflows/tcc-quality.yml`
- Review only: `docs/TCC_PROTOTYPE_*.md`, `docs/TCC_EXPERIMENTAL_DESIGN.md`, `docs/TCC_DATA_SOURCE_DECISION.md`

**Produces:** uma regra única: o estado atual do TCC é factual; a estratégia futura depende da orientação.

- [ ] **Step 1: Confirmar que issue #7 está aberta e marcada como decisão pendente de orientação**

Expected: nenhum lote experimental pendente aparece como cancelado.

- [ ] **Step 2: Verificar que a CI continua executando os testes experimentais existentes**

Run/inspect: `.github/workflows/tcc-quality.yml`.

Expected: não remover instalação de `prototype`, `test_experiment_contract.py` nem `prototype/tests` antes do gate.

- [ ] **Step 3: Atualizar a governança textual**

Registrar três cenários A/B/C e a proibição de destruir trabalho antes da decisão.

- [ ] **Step 4: Executar regressões existentes**

Run:
```bash
cd research
python -m pytest tests/test_bibliography_audit.py tests/test_experiment_contract.py tests/test_mmat.py tests/test_mmat_artifacts.py tests/test_tcc_advisor_feedback.py -q
cd ..
python -m pytest prototype/tests -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/TCC_REVISION_SCOPE.md
git commit -m ":memo: docs(tcc): gate scientific scope on advisor decision"
```

---

### Task 2: Reconstruir forensicamente o protocolo original da revisão

**Files:**
- Inspect history: `research/src/search_terms.py`
- Inspect history: `research/src/config.py`
- Inspect: `research/README.md`
- Inspect: `results/tcc/conteudo/metodologia.tex`
- Inspect: `research/exports/`, banco e logs disponíveis
- Create: `research/data/review_protocol_manifest.json`
- Create: `research/tests/test_review_protocol_manifest.py`

**Produces:** manifesto canônico do protocolo realmente executado.

- [ ] **Step 1: Escrever teste inicialmente falho para exigir o manifesto**

O teste deve exigir pelo menos:
```json
{
  "search_date": "...",
  "year_min": 0,
  "year_max": 0,
  "query_count": 0,
  "queries_sha256": "...",
  "sources": [],
  "identified_records": 0,
  "deduplicated_records": 0,
  "eligible_records": 0,
  "included_records": 0,
  "evidence_commit": "..."
}
```

- [ ] **Step 2: Rodar o teste e confirmar FAIL**

Run:
```bash
cd research
python -m pytest tests/test_review_protocol_manifest.py -v
```

Expected: FAIL porque o manifesto ainda não existe.

- [ ] **Step 3: Investigar histórico e artefatos sem escolher números por conveniência**

Verificar especificamente:
- 72 versus 108 consultas;
- 2015 versus 2016 como ano inicial;
- participação real de Semantic Scholar, OpenAlex, Crossref e CORE;
- origem das contagens 9.431 / 2.517 / 6.914 / 1.883 / 17;
- data real ou faixa temporal da execução canônica.

- [ ] **Step 4: Criar o manifesto apenas com valores suportados por evidência**

Campos não recuperáveis devem ser documentados como `unknown`/limitação, nunca inventados.

- [ ] **Step 5: Corrigir texto/configuração somente quando a evidência justificar**

Não alterar retrospectivamente o protocolo histórico apenas para fazê-lo coincidir com a configuração atual.

- [ ] **Step 6: Rodar regressões**

Expected: manifesto e números acadêmicos consistentes.

- [ ] **Step 7: Commit**

```bash
git add research/data/review_protocol_manifest.json research/tests/test_review_protocol_manifest.py research/src/config.py research/README.md results/tcc/conteudo/metodologia.tex
git commit -m ":mag: docs(tcc): reconstruct executed review protocol"
```

---

### Task 3: Auditoria científica de afirmações do TCC

**Files:**
- Create/extend: `docs/TCC_CLAIM_EVIDENCE_MATRIX.md` ou artefato equivalente já existente
- Review: todos os capítulos `.tex`
- Review: `results/tcc/referencias*.bib`

**Produces:** matriz rastreável entre afirmação e evidência.

- [ ] **Step 1: Classificar afirmações por tipo**

Categorias mínimas:
- definição conceitual;
- dado quantitativo da revisão;
- descrição de estudo primário;
- síntese do autor;
- inferência/limitação;
- proposta técnica futura;
- eventual resultado experimental.

- [ ] **Step 2: Para cada afirmação importante, registrar suporte**

Colunas mínimas:
`location | claim | evidence/source | evidence_type | support_strength | allowed_wording | notes`.

- [ ] **Step 3: Priorizar riscos**

Marcar como alto risco:
- causalidade não demonstrada;
- generalização para contexto brasileiro sem base;
- equivalência entre previsão e aprendizagem;
- superioridade de modelo inferida por frequência ou métricas incomparáveis;
- especificação técnica escrita como resultado experimental.

- [ ] **Step 4: Corrigir texto somente após a matriz**

- [ ] **Step 5: Revisão humana**

Autor/orientação valida interpretações substantivas.

---

### Task 4: Avaliar reutilização de modelos e artefatos consolidados

**Files:**
- Create: `docs/TCC_REUSE_FEASIBILITY_MATRIX.md`
- Inspect: 17 estudos incluídos, referências adicionais e artefatos públicos ligados às fontes
- Inspect: `prototype/` e contratos existentes

**Produces:** evidência para discutir o Cenário B com a orientação.

- [ ] **Step 1: Identificar candidatos de reutilização**

Para cada referência relevante, procurar:
- código oficial ou dos autores;
- modelo/pesos publicados;
- notebook reproduzível;
- implementação canônica de biblioteca;
- dataset/contrato de entrada documentado.

- [ ] **Step 2: Registrar proveniência e licença**

Nenhum artefato entra como candidato `viável` sem fonte e condição de uso.

- [ ] **Step 3: Avaliar compatibilidade científica**

Colunas mínimas:
`reference | technique | available_artifact | license | expected_input | mathematical_domain | training_required | adaptation_required | compute_cost | reproducibility | what_it_can_demonstrate | limitations`.

- [ ] **Step 4: Classificar formas de uso**

Separar:
1. uso direto de modelo/peso publicado;
2. uso de algoritmo implementado em biblioteca com parâmetros da literatura;
3. reprodução de treinamento descrito no artigo;
4. novo treinamento/novo desenho experimental.

- [ ] **Step 5: Preparar recomendação para orientação**

A recomendação deve comparar esforço científico, custo computacional e força da conclusão, sem escolher automaticamente o menor esforço.

---

### Task 5: Preparar decisão sobre atualização da revisão em 2026

**Files:**
- Issue: #26
- No corpus changes before approval.

- [ ] **Step 1: Usar o manifesto da Task 2 para estimar esforço**
- [ ] **Step 2: Verificar disponibilidade atual das fontes**
- [ ] **Step 3: Estimar quantidade de triagem humana necessária**
- [ ] **Step 4: Levar custo/benefício à orientação**

Expected outcome: `aprovar atualização`, `adiar` ou `não executar`, todos válidos se justificados.

---

### Task 6: Revisão de qualidade textual e voz acadêmica

**Files:**
- Review: `results/tcc/conteudo/*.tex`
- Review: `results/tcc/pretextuais/resumo.tex`

**Produces:** texto preciso, menos formulaico e mais ancorado na evidência.

- [ ] **Step 1: Detectar parágrafos genéricos**
- [ ] **Step 2: Detectar metadiscurso repetitivo e conectivos formulaicos**
- [ ] **Step 3: Detectar repetição semântica entre capítulos**
- [ ] **Step 4: Substituir somente quando houver ganho de precisão**
- [ ] **Step 5: Conferir toda reescrita substantiva contra a matriz de evidência**
- [ ] **Step 6: Revisão humana do autor**

Do not: introduzir imperfeições artificiais ou variar estilo apenas para aparentar escrita humana.

---

# GATE COM A ORIENTAÇÃO

### Task 7: Decidir o caminho científico

**Inputs:**
- issue #24;
- issue #7;
- `TCC_CLAIM_EVIDENCE_MATRIX`;
- `TCC_REUSE_FEASIBILITY_MATRIX`;
- diagnóstico do protocolo original;
- estimativa da atualização 2026.

- [ ] **Step 1: Apresentar Cenário A** — revisão/síntese/especificação.
- [ ] **Step 2: Apresentar Cenário B** — demonstração baseada em recursos consolidados.
- [ ] **Step 3: Apresentar Cenário C** — experimento próprio.
- [ ] **Step 4: Registrar decisão e justificativa na issue #24**.
- [ ] **Step 5: Reclassificar issue #7 e #26 conforme a decisão**.
- [ ] **Step 6: Só então alterar governança, CI ou capítulos para refletir o cenário final**.

---

# PARTE II — executar somente o cenário aprovado

### Task 8A: Cenário A — revisão/especificação

Executar se aprovado.

- [ ] consolidar auditoria científica;
- [ ] executar atualização 2026 somente se aprovada separadamente;
- [ ] fortalecer taxonomia e matriz `problema × dados × técnica × evidência × risco`;
- [ ] manter `prototype/` como artefato histórico/exploratório sem apresentá-lo como resultado;
- [ ] revisar título #25;
- [ ] finalizar PRISMA/MMAT/ABNT.

### Task 8B: Cenário B — demonstração com modelos/artefatos consolidados

Executar se aprovado.

- [ ] selecionar candidato a partir da matriz de viabilidade;
- [ ] congelar versão, licença, fonte e parâmetros;
- [ ] definir conjunto de dados de demonstração e suas limitações;
- [ ] criar teste de reprodução mínima;
- [ ] executar o artefato sem modificar parâmetros para buscar resultado favorável;
- [ ] registrar logs, ambiente e saída;
- [ ] avaliar apenas o que a demonstração suporta;
- [ ] atualizar metodologia/protótipo/resultados com distinção explícita entre artefato reutilizado e contribuição própria;
- [ ] não chamar a demonstração de validação pedagógica.

### Task 8C: Cenário C — experimento próprio

Executar se aprovado.

- [ ] retomar os lotes da issue #7;
- [ ] usar `docs/TCC_EXPERIMENTAL_DESIGN.md` como contrato prévio;
- [ ] manter testes de vazamento, seeds, métricas e calibração;
- [ ] registrar resultados somente depois de reprodução automatizada;
- [ ] atualizar texto do TCC apenas com artefatos versionados.

---

### Task 9: Título final

**Issue:** #25

- [ ] escolher título após o cenário estar definido;
- [ ] obter aprovação da orientação;
- [ ] atualizar capa e elementos derivados;
- [ ] revisar resumo/abstract e PRISMA item 1;
- [ ] recompilar.

---

### Task 10: Validação final

- [ ] `git diff --check origin/main...HEAD`;
- [ ] testes `research/` pertinentes ao cenário;
- [ ] testes `prototype/` se o artefato continuar ativo/relevante;
- [ ] auditoria bibliográfica;
- [ ] MMAT canônico;
- [ ] compilação LaTeX;
- [ ] inspeção visual do PDF completo;
- [ ] conferência ABNT/IFC/template;
- [ ] conferência de números contra artefatos;
- [ ] revisão final do orientador;
- [ ] nenhuma mesclagem automática.

## Self-review

- **Spec coverage:** escopo, revisão científica, atualização 2026, qualidade textual, título e três cenários cobertos.
- **Preservação:** nenhum passo manda remover trabalho experimental antes do gate.
- **Human gates:** orientação decide cenário e título; autor valida interpretação e redação substantiva.
- **Scientific boundary:** demonstração técnica, desempenho preditivo e eficácia pedagógica permanecem separados.
