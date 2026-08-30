# TCC Scientific Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidar o TCC como revisão sistemática, apreciação metodológica, síntese crítica e especificação conceitual cientificamente rastreável, sem transformar treinamento de modelos ou implementação funcional em requisito de conclusão.

**Architecture:** O texto do TCC, o pipeline de revisão e os documentos de governança devem convergir para uma única linha de base científica. O trabalho será executado em PRs pequenos: primeiro governança e reconstrução do protocolo original; depois auditoria de evidências; em seguida, se aprovada, atualização incremental da literatura de 2026; por fim síntese, redação acadêmica, título e validação final. Agentes podem executar auditorias e produzir evidências em paralelo, mas decisões de inclusão/exclusão, MMAT, alteração de protocolo, interpretação científica e título exigem gate humano.

**Tech Stack:** LaTeX/abnTeX2-IFC, Python 3.11, SQLite, pytest, GitHub Actions, pipeline `research/`, PRISMA 2020, PRISMA-S, MMAT 2018.

**Spec:** `docs/TCC_REVISION_SCOPE.md`, issue #24, issue #25 e issue #26.

## Global Constraints

- O escopo final não exige protótipo funcional, treinamento de modelos ou validação experimental própria.
- Código existente em `prototype/` pode permanecer como histórico/artefato exploratório, mas não constitui evidência de resultado do TCC.
- Nenhum resultado, número ou conclusão pode ser criado retrospectivamente para preencher lacunas do PRISMA.
- Nenhuma divergência do protocolo original será resolvida por preferência editorial; prevalece evidência versionada da execução real.
- O limiar de relevância temática não será tratado como qualidade metodológica.
- MMAT permanece por critério Q1–Q5, sem escore total, média, ranking ou medida global de certeza da evidência.
- Desempenho observado, proficiência, competência e aprendizagem permanecem conceitos distintos.
- A eventual busca de 2026 será uma atualização controlada e separada do corpus original até a deduplicação.
- LLMs e agentes podem sugerir texto, detectar inconsistências e localizar evidência; não tomam autonomamente decisões científicas finais.
- O objetivo da revisão de escrita é qualidade acadêmica e autoria responsável, não evasão de detectores de IA.
- Nenhum PR será mesclado automaticamente.

---

## File Structure / Responsibilities

### Texto acadêmico

- `results/tcc/pretextuais/capa.tex` — título e metadados de capa.
- `results/tcc/pretextuais/resumo.tex` — resumo/abstract e palavras-chave.
- `results/tcc/conteudo/introducao.tex` — problema, objetivos, justificativa e estrutura.
- `results/tcc/conteudo/fundamentacao.tex` — conceitos e fundamentação pedagógica/computacional.
- `results/tcc/conteudo/metodologia.tex` — protocolo realmente executado, PRISMA, seleção e MMAT.
- `results/tcc/conteudo/resultadosesperados.tex` — revisão sistemática/síntese dos estudos.
- `results/tcc/conteudo/prototipo.tex` — especificação conceitual, não implementação.
- `results/tcc/conteudo/resultados.tex` — resultados e discussão integrada.
- `results/tcc/conteudo/conclusao.tex` — conclusões, limites e continuidade.
- `results/tcc/postextuais/apendice.tex` — checklist PRISMA.
- `results/tcc/referencias.bib` e `results/tcc/referencias_pedagogicas.bib` — referências canônicas.

### Governança

- `docs/TCC_REVISION_SCOPE.md` — única fonte ativa para delimitação do escopo final.
- `docs/TCC_REFERENCE_AUDIT.md` — auditoria bibliográfica.
- `docs/TCC_PROTOTYPE_DELIVERY_PLAN.md` — documento experimental antigo a arquivar/reclassificar.
- `docs/TCC_PROTOTYPE_SCIENTIFIC_DECISIONS.md` — decisão experimental antiga a arquivar/reclassificar.
- `docs/TCC_EXPERIMENTAL_DESIGN.md` — desenho experimental antigo a arquivar/reclassificar.
- `docs/TCC_DATA_SOURCE_DECISION.md` — decisão de base para experimento antigo a arquivar/reclassificar.
- `docs/TCC_PROFILE_AND_EXPLAINABILITY.md` — especificação experimental antiga a arquivar/reclassificar.
- `prototype/README.md` — deve declarar o caráter histórico/fora do escopo final se o código for preservado.

### Pipeline da revisão

- `research/src/search_terms.py` — gerador canônico atual de 72 consultas.
- `research/src/config.py` — critérios atuais; contém `year_min=2015`/`year_max=2025` e precisa ser reconciliado com a execução real.
- `research/src/pipeline/run.py` — orquestração da revisão.
- `research/src/processing/dedup.py` — deduplicação.
- `research/src/processing/selection.py` — seleção/triagem.
- `research/src/analysis/mmat_assessment.py` — avaliação MMAT.
- `research/src/analysis/mmat_tcc_table.py` — tabela MMAT usada no TCC.
- `research/exports/` — artefatos derivados.
- `research/data/` — dados de auditoria/versionados.
- `research/README.md` — documentação histórica que atualmente contém divergências 108/72 e 2015/2016.

### Validação

- `.github/workflows/tcc-quality.yml` — CI do TCC; atualmente ainda instala/testa `prototype/` e deve ser desacoplado.
- `research/tests/test_tcc_advisor_feedback.py` — regressões textuais/metodológicas.
- `research/tests/test_bibliography_audit.py` — integridade bibliográfica.
- `research/tests/test_mmat.py` e `research/tests/test_mmat_artifacts.py` — MMAT.
- `research/tests/test_experiment_contract.py` — contrato experimental antigo; não deve continuar como gate do TCC documental.
- `prototype/tests/` — suíte do protótipo; pode continuar existindo, mas não deve ser requisito de `TCC quality` após a mudança de escopo.

---

### Task 1: Retirar formalmente o roadmap experimental do escopo ativo

**Files:**
- Modify: `docs/TCC_REVISION_SCOPE.md`
- Modify: `docs/README.md`
- Modify: `README.md`
- Modify: `prototype/README.md`
- Archive/reclassify: `docs/TCC_PROTOTYPE_DELIVERY_PLAN.md`
- Archive/reclassify: `docs/TCC_PROTOTYPE_SCIENTIFIC_DECISIONS.md`
- Archive/reclassify: `docs/TCC_EXPERIMENTAL_DESIGN.md`
- Archive/reclassify: `docs/TCC_DATA_SOURCE_DECISION.md`
- Archive/reclassify: `docs/TCC_PROFILE_AND_EXPLAINABILITY.md`
- Test: `research/tests/test_tcc_advisor_feedback.py`

**Interfaces:**
- Consumes: decisão de escopo registrada na issue #24.
- Produces: uma única definição ativa do que o TCC entrega e do que é continuidade futura.

- [ ] **Step 1: adicionar teste de regressão de governança**

Adicionar ao `test_tcc_advisor_feedback.py` verificações de que `TCC_REVISION_SCOPE.md` contém as expressões de delimitação e que documentos experimentais ativos não são apontados como requisitos do TCC.

- [ ] **Step 2: executar o teste e confirmar falha no estado atual**

Run:

```bash
cd research
pytest tests/test_tcc_advisor_feedback.py -q
```

Expected: FAIL enquanto documentos/README ainda apresentarem implementação como roadmap ativo.

- [ ] **Step 3: arquivar sem apagar a história científica**

Mover os cinco documentos experimentais para `docs/archive/prototype-experiment/` ou inserir cabeçalho inequívoco de `HISTÓRICO — FORA DO ESCOPO FINAL`. Preferir arquivo quando links internos puderem ser atualizados de forma segura.

- [ ] **Step 4: marcar `prototype/` como artefato exploratório**

No início de `prototype/README.md`, registrar que o código não é requisito, método executado ou resultado científico do TCC final.

- [ ] **Step 5: alinhar README e governança**

Remover linguagem que trate seleção de base, treinamento, inferência e interface como etapas pendentes para concluir o TCC.

- [ ] **Step 6: executar regressão**

Run:

```bash
cd research
pytest tests/test_tcc_advisor_feedback.py -q
```

Expected: PASS.

- [ ] **Step 7: commit**

```bash
git add README.md docs prototype/README.md research/tests/test_tcc_advisor_feedback.py
git commit -m ":memo: docs(tcc): retire experimental roadmap from final scope"
```

---

### Task 2: Desacoplar a CI do TCC do experimento/protótipo

**Files:**
- Modify: `.github/workflows/tcc-quality.yml`
- Modify/Delete from TCC gate: `research/tests/test_experiment_contract.py`
- Preserve: `prototype/tests/`

**Interfaces:**
- Consumes: Task 1.
- Produces: `TCC quality` valida apenas artefatos necessários à entrega acadêmica.

- [ ] **Step 1: registrar contrato de CI esperado**

No teste de regressão textual/governança, verificar que o workflow do TCC não contém `pip install -e "prototype[dev]"`, `tests/test_experiment_contract.py` nem `pytest prototype/tests`.

- [ ] **Step 2: executar teste e confirmar falha**

```bash
cd research
pytest tests/test_tcc_advisor_feedback.py -q
```

Expected: FAIL no workflow atual.

- [ ] **Step 3: simplificar `source-validation`**

Em `.github/workflows/tcc-quality.yml`:

- remover `prototype/pyproject.toml` do `cache-dependency-path`;
- remover instalação de dependências do protótipo;
- remover compilação de `prototype/tcc_prototype`;
- retirar `tests/test_experiment_contract.py` da suíte acadêmica;
- retirar execução de `prototype/tests`;
- manter bibliografia, MMAT, regressões do orientador, pipeline científico relevante e compilação LaTeX.

- [ ] **Step 4: manter protótipo testável separadamente apenas se houver utilidade histórica**

Se for desejável preservar manutenção do código, criar workflow separado e não obrigatório, por exemplo `.github/workflows/prototype-archive.yml`, acionado manualmente. Não conectá-lo à condição de aprovação do TCC.

- [ ] **Step 5: validar**

```bash
cd research
pytest tests/test_bibliography_audit.py tests/test_mmat.py tests/test_mmat_artifacts.py tests/test_tcc_advisor_feedback.py -q
```

Expected: PASS.

- [ ] **Step 6: commit**

```bash
git add .github/workflows/tcc-quality.yml research/tests
git commit -m ":construction_worker: ci(tcc): decouple archived prototype from thesis quality gate"
```

---

### Task 3: Reconstruir o protocolo realmente executado da revisão original

**Files:**
- Inspect: Git history for `research/src/search_terms.py`, `research/src/config.py`, pipeline and exports.
- Create: `research/data/review_protocol_baseline.json`
- Create: `research/exports/analysis/review_protocol_baseline.md`
- Modify: `research/README.md`
- Modify only after evidence: `results/tcc/conteudo/metodologia.tex`
- Test: create `research/tests/test_review_protocol_baseline.py`

**Interfaces:**
- Consumes: banco/exports/logs/commits da revisão original.
- Produces: baseline imutável usado pela atualização de 2026.

- [ ] **Step 1: criar teste para o manifesto**

O teste deve exigir campos mínimos:

```text
schema_version
source_commit
search_started_at/search_completed_at ou justificativa de indisponibilidade
publication_year_min
publication_year_max
query_count
queries_sha256
sources
source_parameters
identified_records
unique_records
eligibility_records
included_studies
```

- [ ] **Step 2: confirmar que o teste falha porque o manifesto ainda não existe**

```bash
cd research
pytest tests/test_review_protocol_baseline.py -q
```

Expected: FAIL por arquivo ausente.

- [ ] **Step 3: investigar 72 versus 108 consultas**

Usar Git history para encontrar a versão de `search_terms.py` e dos logs/exports associada à coleta de 9.431 registros. Não inferir o número apenas pelo README atual.

- [ ] **Step 4: investigar 2015 versus 2016**

Confrontar filtros do código usado, timestamps do banco, distribuição por ano, commits e texto do PTC/TCC. Registrar a evidência que sustenta o recorte realmente aplicado.

- [ ] **Step 5: investigar fontes efetivamente ativas**

Confirmar se Semantic Scholar, OpenAlex, Crossref e CORE contribuíram para a execução canônica ou se alguma fonte estava apenas prevista/configurada.

- [ ] **Step 6: gerar o manifesto baseline e um relatório legível**

`review_protocol_baseline.json` é a fonte de máquina; `review_protocol_baseline.md` explica a reconstrução, incluindo incertezas remanescentes.

- [ ] **Step 7: alinhar documentação e metodologia**

Somente após o manifesto existir, corrigir `research/README.md`, `config.py` quando aplicável e `metodologia.tex` para refletir a execução real.

- [ ] **Step 8: validar**

```bash
cd research
pytest tests/test_review_protocol_baseline.py tests/test_complete_pipeline.py -q
python -m src.validation.bibliography_audit
python -m src.cli stats
```

Expected: manifesto válido e contagens compatíveis com os artefatos canônicos.

- [ ] **Step 9: commit**

```bash
git add research/data/review_protocol_baseline.json research/exports/analysis/review_protocol_baseline.md research/README.md research/src/config.py research/tests/test_review_protocol_baseline.py results/tcc/conteudo/metodologia.tex
git commit -m ":mag: docs(tcc): reconstruct canonical systematic review protocol"
```

---

### Task 4: Criar auditoria científica `afirmação → evidência`

**Files:**
- Extend/Create: `docs/TCC_REFERENCE_AUDIT.md`
- Create: `research/data/tcc_claim_evidence.csv`
- Create: `research/src/validation/claim_evidence_audit.py`
- Test: `research/tests/test_claim_evidence_audit.py`

**Interfaces:**
- Consumes: referências, 17 estudos, capítulos do TCC.
- Produces: inventário auditável de afirmações substantivas.

- [ ] **Step 1: definir colunas do CSV**

```text
claim_id
chapter
section
claim_summary
claim_type
source_key
source_locator
evidence_type
support_level
author_inference
status
notes
```

`support_level` deve usar vocabulário fechado: `direct`, `indirect`, `mixed`, `insufficient`, `not_applicable`.

- [ ] **Step 2: criar teste de schema e cobertura**

O teste deve exigir `claim_id` único, capítulo válido, fonte existente quando `claim_type` exigir referência e justificativa para `indirect/mixed/insufficient`.

- [ ] **Step 3: executar e confirmar falha antes de criar o artefato**

```bash
cd research
pytest tests/test_claim_evidence_audit.py -q
```

- [ ] **Step 4: auditar por capítulo**

Prioridade: metodologia, síntese dos 17 estudos, discussão e conclusão. Cada afirmação quantitativa, causal, comparativa ou generalizante deve ser registrada.

- [ ] **Step 5: revisar inferências autorais**

Marcar explicitamente quando uma “lacuna” ou recomendação é inferência derivada do conjunto e não frase diretamente demonstrada por um estudo.

- [ ] **Step 6: validar cobertura**

```bash
cd research
python -m src.validation.claim_evidence_audit
pytest tests/test_claim_evidence_audit.py tests/test_bibliography_audit.py -q
```

- [ ] **Step 7: commit**

```bash
git add docs/TCC_REFERENCE_AUDIT.md research/data/tcc_claim_evidence.csv research/src/validation/claim_evidence_audit.py research/tests/test_claim_evidence_audit.py
git commit -m ":white_check_mark: test(tcc): add claim to evidence scientific audit"
```

---

### Task 5: Corrigir o texto a partir da auditoria científica

**Files:**
- Modify: `results/tcc/conteudo/introducao.tex`
- Modify: `results/tcc/conteudo/fundamentacao.tex`
- Modify: `results/tcc/conteudo/metodologia.tex`
- Modify: `results/tcc/conteudo/resultadosesperados.tex`
- Modify: `results/tcc/conteudo/prototipo.tex`
- Modify: `results/tcc/conteudo/resultados.tex`
- Modify: `results/tcc/conteudo/conclusao.tex`
- Test: `research/tests/test_tcc_advisor_feedback.py`

**Interfaces:**
- Consumes: Task 4.
- Produces: versão cientificamente calibrada do texto antes da atualização 2026.

- [ ] **Step 1: adicionar regressões para overclaiming identificado**

Cada problema recorrente deve ganhar teste apenas quando puder ser expresso de forma robusta (por exemplo, proibição de declarar implementação/eficácia ou números divergentes), evitando testes frágeis de estilo palavra por palavra.

- [ ] **Step 2: corrigir introdução e objetivos**

Todos os objetivos precisam ser satisfeitos por revisão, avaliação metodológica, síntese e especificação conceitual.

- [ ] **Step 3: corrigir fundamentação**

Substituir afirmações amplas por formulações com fonte específica; preservar distinções conceituais.

- [ ] **Step 4: corrigir metodologia**

Usar exclusivamente o protocolo reconstruído; diferenciar automação de busca/triagem e decisão científica.

- [ ] **Step 5: corrigir síntese dos estudos**

Não converter frequência de uso, maior acurácia isolada ou presença na literatura em “melhor técnica”.

- [ ] **Step 6: corrigir especificação**

Apresentar Random Forest, SHAP, bases e arquiteturas como alternativas condicionais quando não houver comparação própria.

- [ ] **Step 7: fortalecer discussão**

Organizar discussão por padrões convergentes, conflitos, heterogeneidade, qualidade metodológica e validade externa.

- [ ] **Step 8: calibrar conclusão**

Separar `o trabalho encontrou`, `o autor interpreta` e `trabalhos futuros poderão testar`.

- [ ] **Step 9: compilar e testar**

```bash
cd research
pytest tests/test_tcc_advisor_feedback.py tests/test_bibliography_audit.py tests/test_mmat.py tests/test_mmat_artifacts.py -q
cd ../results/tcc
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

- [ ] **Step 10: commit**

```bash
git add results/tcc/conteudo research/tests/test_tcc_advisor_feedback.py
git commit -m ":books: docs(tcc): calibrate claims to scientific evidence"
```

---

### Task 6: Executar atualização incremental da literatura de 2026

**Tracking:** issue #26.

**Files:**
- Modify: `research/src/config.py` only to support explicit runtime update window, without destroying baseline.
- Modify: `research/src/cli.py` / `research/src/pipeline/run.py` as necessary for isolated update mode.
- Reuse: `research/src/search_terms.py` from frozen baseline.
- Reuse: `research/src/processing/dedup.py`.
- Create: `research/data/review_update_2026_manifest.json`
- Create: `research/exports/analysis/review_update_2026_summary.json`
- Test: `research/tests/test_review_update_2026.py`

**Interfaces:**
- Consumes: Task 3 baseline.
- Produces: lote 2026 rastreável, antes/depois da deduplicação, e impacto sobre corpus.

- [ ] **Step 1: criar testes de isolamento do lote**

Exigir que o modo de atualização não sobrescreva o corpus original e que o manifesto inclua `baseline_protocol_sha256`, data de busca, janela, queries e fontes.

- [ ] **Step 2: confirmar falha antes da implementação**

```bash
cd research
pytest tests/test_review_update_2026.py -q
```

- [ ] **Step 3: implementar janela explícita**

Adicionar parâmetros de CLI/configuração para a atualização; não substituir os valores históricos do baseline.

- [ ] **Step 4: executar busca no harness/máquina dedicada**

Registrar stdout/stderr, versões e data. Usar credenciais configuradas sem commit de secrets.

- [ ] **Step 5: deduplicar contra baseline**

Gerar classes `new`, `duplicate_baseline`, `duplicate_update`.

- [ ] **Step 6: triagem automática assistiva + gate humano**

O pipeline pode calcular relevância e priorizar; a decisão final de estudos novos potencialmente incluídos deve ser revisada manualmente.

- [ ] **Step 7: aplicar MMAT aos novos incluídos**

Registrar Q1–Q5 com justificativa e revisão humana.

- [ ] **Step 8: integrar somente depois das decisões**

Atualizar corpus canônico, PRISMA, tabelas e referências após o lote 2026 estar fechado.

- [ ] **Step 9: validar**

```bash
cd research
pytest tests/test_review_update_2026.py tests/test_dedup_logic.py tests/test_mmat.py tests/test_mmat_artifacts.py -q
python -m src.cli stats
```

- [ ] **Step 10: commit em unidades separadas**

Um commit para suporte técnico do update; outro para artefatos/resultados após gate humano.

---

### Task 7: Revalidar PRISMA 2020, PRISMA-S e MMAT após a atualização

**Files:**
- Modify: `results/tcc/postextuais/apendice.tex`
- Modify: `results/tcc/pretextuais/resumo.tex`
- Modify: `results/tcc/conteudo/metodologia.tex`
- Modify: `results/tcc/conteudo/resultadosesperados.tex`
- Modify: `research/data/mmat_assessments.csv` if new studies exist.
- Regenerate: `research/exports/analysis/mmat_assessment.csv`
- Test: `research/tests/test_mmat_artifacts.py`, `research/tests/test_tcc_advisor_feedback.py`

- [ ] **Step 1: auditar PRISMA 2020 item por item**

Usar checklist oficial e registrar `atendido`, `parcial`, `não realizado` ou `não aplicável`.

- [ ] **Step 2: auditar resumo com PRISMA for Abstracts**

Não marcar o item 2 como pleno sem verificar o checklist específico.

- [ ] **Step 3: aplicar PRISMA-S ao relato das buscas**

Documentar consultas completas, fontes, interfaces, datas, limites e deduplicação em artefato acessível, sem inflar o corpo do TCC desnecessariamente.

- [ ] **Step 4: revalidar MMAT**

Manter política por critério; não converter para escore global.

- [ ] **Step 5: validar**

```bash
cd research
python -m src.analysis.mmat_tcc_table --check
cmp data/mmat_assessments.csv exports/analysis/mmat_assessment.csv
pytest tests/test_mmat.py tests/test_mmat_artifacts.py tests/test_tcc_advisor_feedback.py -q
```

---

### Task 8: Fortalecer a síntese sem treinamento de modelos

**Files:**
- Create: `research/exports/analysis/technique_evidence_matrix.csv`
- Create: `research/exports/analysis/problem_data_technique_matrix.csv`
- Modify: `results/tcc/conteudo/resultadosesperados.tex`
- Modify: `results/tcc/conteudo/prototipo.tex`
- Modify: `results/tcc/conteudo/resultados.tex`

**Interfaces:**
- Consumes: corpus final e claim-evidence audit.
- Produces: contribuição analítica que substitui a necessidade artificial de um experimento apressado.

- [ ] **Step 1: criar esquema da matriz de técnicas**

Colunas mínimas:

```text
technique_family
purpose
data_granularity
studies
reported_metrics
interpretability
reported_limitations
math_specific_evidence
methodological_cautions
```

- [ ] **Step 2: criar matriz problema × dados × técnica**

Colunas mínimas:

```text
pedagogical_problem
required_observations
candidate_techniques
evidence_available
evidence_limitations
validation_needed
ethical_risks
```

- [ ] **Step 3: preencher apenas a partir de estudos/fundamentação auditados**

Nenhuma célula deve ser recomendação implícita sem fonte ou inferência declarada.

- [ ] **Step 4: usar as matrizes para reescrever a especificação conceitual**

A arquitetura deve ser apresentada como uma proposta condicionada pelos requisitos, não como tecnologia escolhida por popularidade.

- [ ] **Step 5: validar consistência entre matrizes e texto**

Criar teste simples que confirme que estudos citados nas matrizes existem no corpus final.

---

### Task 9: Revisar voz acadêmica e integridade do uso de LLM

**Files:**
- Modify: capítulos conforme achados.
- Create: `docs/TCC_WRITING_REVIEW.md` com critérios e decisões, sem registrar prompts sensíveis/desnecessários.
- Test: preferir verificações semânticas/estruturais robustas; evitar detector de IA como teste.

- [ ] **Step 1: executar revisores independentes em paralelo**

Agente A: linguagem genérica e metadiscurso.

Agente B: repetição semântica entre capítulos.

Agente C: afirmações fortes sem evidência explícita.

Agente D: consistência terminológica português/inglês.

Cada agente deve retornar `arquivo + trecho + problema + motivo + proposta`, sem editar diretamente nesta etapa.

- [ ] **Step 2: consolidar divergências**

Aceitar alterações somente quando melhorarem clareza, precisão ou rastreabilidade. Não introduzir variação estilística artificial para “parecer humano”.

- [ ] **Step 3: remover vícios recorrentes**

Priorizar:

- frases que apenas anunciam o que o parágrafo fará;
- conclusões tautológicas;
- sequências repetitivas de três/quatro itens sem necessidade;
- adjetivos vagos (`robusto`, `significativo`, `promissor`) sem critério;
- afirmações de importância sem fonte ou consequência concreta;
- transições padronizadas em excesso;
- repetição da mesma conclusão na introdução, discussão e conclusão.

- [ ] **Step 4: verificar política institucional de IA**

Antes da submissão, consultar regra vigente do IFC/curso/orientação sobre declaração de uso de IA generativa. Cumprir a política; não ocultar uso quando houver obrigação de declaração.

- [ ] **Step 5: leitura humana final**

O autor deve conseguir explicar oralmente toda afirmação substantiva, método, limitação e conclusão que permanecer no texto.

---

### Task 10: Decidir o título somente após congelar a contribuição final

**Tracking:** issue #25.

**Files:**
- Modify após aprovação: `results/tcc/pretextuais/capa.tex`
- Modify se necessário: `results/tcc/pretextuais/resumo.tex`
- Modify: `results/tcc/postextuais/apendice.tex` item 1 PRISMA.

- [ ] **Step 1: revisar as opções da issue #25 após Tasks 5–8**

- [ ] **Step 2: apresentar ao orientador a recomendação e alternativas**

- [ ] **Step 3: registrar a decisão na issue #25**

- [ ] **Step 4: aplicar o título aprovado**

- [ ] **Step 5: verificar coerência entre título, problema, objetivo geral, resumo e conclusão**

- [ ] **Step 6: compilar PDF e inspecionar capa/folha de rosto**

---

### Task 11: Gate final de submissão

**Files:** todo o conjunto acadêmico e CI.

- [ ] **Step 1: executar suíte científica completa**

```bash
cd research
python -m compileall -q src
python -m src.validation.bibliography_audit
python -m src.analysis.mmat_tcc_table --check
pytest -q
```

Se testes históricos não relacionados ao escopo final permanecerem no diretório, a suíte deve ser reorganizada antes deste gate para não reintroduzir dependência experimental.

- [ ] **Step 2: compilar LaTeX**

```bash
cd results/tcc
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Expected: exit 0.

- [ ] **Step 3: verificar consistência automática**

- citações existentes;
- referências usadas;
- números PRISMA derivados do corpus;
- tabela MMAT canônica;
- título/resumo/conclusão coerentes;
- ausência de promessa de implementação.

- [ ] **Step 4: inspeção visual integral do PDF**

Revisar todas as páginas, com atenção especial a capa, resumo, sumário, figuras, tabelas longas, referências e apêndice PRISMA.

- [ ] **Step 5: revisão científica humana**

Checklist mínimo:

- consigo defender oralmente por que cada estudo foi incluído?
- consigo explicar a diferença entre relevância temática e qualidade metodológica?
- consigo justificar o recorte temporal real?
- consigo explicar de onde vieram as 72/108 consultas e qual valor é o executado?
- consigo distinguir resultados da literatura de inferências próprias?
- consigo explicar por que não foi implementado/treinado um modelo sem tratar isso como falha metodológica?
- consigo explicar quais conclusões mudaram ou não após eventual atualização 2026?

- [ ] **Step 6: gate do orientador**

Exigir aprovação explícita para escopo, título e conclusões antes de marcar a versão como candidata à entrega.

---

## Agent Execution Topology

### Pode executar em paralelo após Task 3

- auditoria dos 17 estudos;
- auditoria de citações pedagógicas;
- análise de repetição/voz acadêmica;
- análise das matrizes técnica/dados;
- comparação do checklist PRISMA com o texto.

### Deve ser sequencial

1. congelar escopo;
2. reconstruir protocolo original;
3. decidir/rodar atualização 2026;
4. integrar novos estudos;
5. fechar síntese/conclusões;
6. decidir título;
7. gate final.

### Human-only gates

- confirmar protocolo original quando houver evidência conflitante;
- inclusão/exclusão final de estudos;
- MMAT final;
- alteração de critérios de elegibilidade;
- interpretação de achados conflitantes;
- título;
- conclusão científica final.

---

## Review Cadence

Cada PR deve conter uma unidade rejeitável independentemente:

1. governança/CI;
2. protocolo baseline;
3. auditoria de evidências;
4. atualização 2026;
5. síntese e redação científica;
6. título/normalização final.

Depois de cada PR:

- revisar diff;
- executar testes completos aplicáveis;
- inspecionar artefatos gerados;
- registrar limitações descobertas;
- somente então iniciar a próxima dependência.

---

## Scientific References for Execution

- PRISMA 2020 checklist e materiais oficiais: https://www.prisma-statement.org/prisma-2020
- PRISMA-S: Rethlefsen et al. (2021), DOI `10.1186/s13643-020-01542-z`.
- Cochrane Handbook, Chapter IV — Updating a review: https://training.cochrane.org/handbook/current/chapter-iv
- Cochrane Handbook, Chapter 4 — Searching and selecting studies: https://training.cochrane.org/handbook/current/chapter-04
- MMAT 2018 user guide: manter a referência canônica já auditada no TCC.

## Completion Definition

O plano termina quando o TCC possui um único escopo ativo, o protocolo original está reconstruído por evidência, eventual atualização 2026 está integrada de forma reproduzível, as principais afirmações possuem rastreabilidade, a síntese é crítica sem experimento artificial, o texto possui voz acadêmica específica ao estudo, PRISMA/MMAT estão relatados sem overclaiming, e título/objetivos/resumo/conclusão descrevem a mesma contribuição aprovada pela orientação.
