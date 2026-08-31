# Material para Reunião de Decisão Científica — #27

**Data de referência:** 2026-08-30
**Reunião:** Gate de decisão com orientação (Prof. Dr. Rafael Zanin / Prof. Dr. Manassés Ribeiro)
**Objetivo:** Comparar cenários A/B/C e registrar decisão sobre continuidade do TCC

> **Nota de atualização (31/08/2026):** este material contém uma matriz de decisão construída antes da reconciliação bibliográfica final. A baseline vigente é 11.904 registros e 16 estudos incluídos, após auditoria de 23 candidatos e remoção de 7 falsos positivos. As linhas da matriz que citam estudos removidos e as conclusões baseadas em 17 estudos precisam ser reavaliadas; a reaplicação do MMAT aos 16 estudos atuais ainda está pendente. A fonte atual é `docs/RECONCILIACAO-BASELINE-2026-08-31.md`.

---

## 1. Inventário: Implementado vs. Especificado

### O que EXISTE como código funcional (com testes)

| Componente | Local | Testes | Status |
|---|---|---|---|
| Adaptador ASSISTments | `prototype/tcc_prototype/adapters/assistments.py` | `test_assistments_adapter.py` | ✅ Pronto |
| Pipeline de preparação | `prototype/tcc_prototype/pipeline.py` | `test_pipeline.py` | ✅ Pronto |
| Manifesto/proveniência | `prototype/tcc_prototype/manifest.py` | `test_manifest.py` | ✅ Pronto |
| Engenharia de features | `prototype/tcc_prototype/modeling/features.py` | `test_model_features.py` | ✅ Pronto |
| Baselines (4 variantes) | `prototype/tcc_prototype/modeling/baselines.py` | `test_baselines.py` | ✅ Pronto |
| Regressão logística | `prototype/tcc_prototype/modeling/models.py` | `test_baselines.py` | ✅ Pronto |
| HistGradientBoosting | `prototype/tcc_prototype/modeling/models.py` | `test_baselines.py` | ✅ Pronto |
| Splits (2 estratégias) | `prototype/tcc_prototype/modeling/splits.py` | `test_model_splits.py` | ✅ Pronto |
| Métricas de avaliação | `prototype/tcc_prototype/modeling/evaluation.py` | `test_evaluation.py` | ✅ Pronto |
| Experimento completo | `prototype/tcc_prototype/modeling/experiment.py` | `test_baseline_experiment.py` | ✅ Pronto |
| Perfil de evidências | `prototype/tcc_prototype/profiles.py` | `test_profile_explainability.py` | ✅ Pronto |
| Explicabilidade (LR exata + permutation) | `prototype/tcc_prototype/modeling/explanabilities.py` | `test_profile_explainability.py` | ✅ Pronto |
| CLI (`tcc-prototype`) | `prototype/tcc_prototype/cli.py` | (integração) | ✅ Pronto |
| Config contracts | `prototype/config/*.json` | `test_experiment_contract.py` | ✅ Pronto |

**O que falta para RODAR com dados reais:**
- Baixar ASSISTments Skill Builder 2009-2010 (documento oficial)
- Criar manifesto JSON com SHA-256 do arquivo baixado
- Executar `tcc-prototype prepare-assistments`
- Executar `tcc-prototype evaluate`
- Executar `tcc-prototype profile`

### O que é ESPECIFICAÇÃO (código ou documento, sem evidência experimental)

| Componente | Documento | Status |
|---|---|---|
| Relatório docente (HTML standalone) | `docs/superpowers/specs/2026-08-25-teacher-report-design.md` | 📋 Especificação apenas |
| BNCC crosswalk | Handoff §7 | 📋 Conceitual |
| Arquitetura híbrida (ASSISTments + SAEB) | Handoff §6 | 📋 A ser avaliada |
| Ordinal levels (mastery/fragility) | `config/profile.json` (disabled) | 📋 Congelado até justificativa |
| Binary alerts | `config/profile.json` (disabled) | 📋 Congelado até justificativa |
| SHAP | — | ❌ Não implementado |
| Random Forest | — | ❌ Não implementado (removido como obrigatório) |

### O que NÃO existe

- Nenhum dado real foi baixado ou processado
- Nenhum modelo foi treinado em dados reais
- Nenhuma métrica real foi produzida
- Nenhum resultado foi escrito no TCC como evidência experimental
- O relatório docente não é funcional (é só uma spec)
- BNCC não foi mapeada para skills do ASSISTments

---

## 2. Matriz Científica

### Referência → Problema → Dados → Modelo → Explicabilidade → BNCC → Custo → Limitações

| # | Referência (estudo) | Problema/técnica | Dataset adequado | Modelo/método | Explicabilidade | Relação BNCC | Custo estimado | Limitação principal | Conclusão permitida |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Pejic et al. 2021 | Predição de desempenho | ASSISTments/EdNet | Classificação binária | Coeficientes LR | Mapeamento curricular | Baixo | Dados EUA | Viabilidade em contexto similar |
| 2 | Depren 2017 | Knowledge tracing | ASSISTments | Bayesian KT | Probabilidades | — | Baixo | Plataforma específica | Comportamento preditivo |
| 3 | MacLellan 2017 | Skills-based analysis | ASSISTments | Análise por skill | — | — | Baixo | Skill tags limitadas | Evidência por habilidade |
| 4 | Appiah-Odame 2024 | Educational data mining | Genérico | ML supervisionado | Feature importance | — | Médio | Diversidade de dados | Padrões preditivos |
| 5 | Mertasari 2023 | Predição de notas | Moodle | Regressão/classificação | LR coefficients | — | Baixo | Dados de avaliação | Evidência de desempenho |
| 6 | Hasib 2022 | Análise de interações | Plataformaeducacional | ML supervisionado | — | — | Médio | Generalização | Padrões de interação |
| 7 | Zhang 2023 | Knowledge tracing | ASSISTments | Deep learning | SHAP (limitado) | — | Alto (GPU) | Complexidade | Comportamento sequencial |
| 8 | Tjahyadi 2025 | Predição acadêmica | Universidade | Ensemble | Feature importance | — | Médio | Contexto superior | Risco de evasão |
| 9 | Zhang et al. 2025 | Assistente inteligente | Plataforma própria | LLM + analytics | — | — | Alto | Validade limitada | Demonstração conceitual |
| 10 | Jose et al. 2024 | Feedback personalizado | Moodle | Classificação | — | Parcial | Médio | Dados limitados | Evidência de feedback |
| 11 | Kumar 2022 | Análise preditiva | Diversos | ML supervisionado | — | — | Médio | Heterogeneidade | Padrões gerais |
| 12 | Salas-Rueda 2021 | Visualização de dados | Sala de aula | Regressão | — | — | Baixo | Amostra pequena | Evidência contextual |
| 13 | Unal 2020 | Gamificação | Plataforma gamificada | Classificação | — | — | Baixo | Contexto específico | Engajamento |
| 14 | Nyantah 2025 | Avaliação formativa | Universidade | ML | — | — | Médio | Contexto superior | Avaliação contínua |
| 15 | Milicevic 2024 | Recomendação de conteúdo | Sistema adaptativo | Filtros colaborativos | — | Parcial | Médio | Dados de preferência | Seleção de conteúdo |
| 16 | Sokkhey 2020 | Predição de notas | Moodle | Regressão/classificação | — | — | Baixo | Amostra limitada | Desempenho acadêmico |
| 17 | Uskov 2019 | Gamificação em ED | Revisão teórica | — | — | — | Baixo | Sem dados empíricos | Revisão conceitual |

### Legenda de dados

| Dataset | Tipo | Adequação |巴西 | Aquisição |
|---|---|---|---|---|
| **ASSISTments** | Interações sequenciais estudante-item | ✅ Ideal para previsão da próxima resposta | ❌ EUA | Download público (termos a revisar) |
| **SAEB** | Proficiência, Larga escala | ⚠️ Não sequencial (teste único) | ✅ Brasil | Download público (INEP) |
| **EdNet** | Interações de tutor | ✅ Similar ao ASSISTments | ❌ Coreia do Sul | Download público |
| **Eedi** | Interações estudante-questão | ✅ Adequado | ❌ Reino Unido | CC BY-NC-ND 4.0 |
| **PISA** | Proficiência, Larga escala | ⚠️ Não sequencial | ✅ Brasil (parcial) | Download público (OECD) |

---

## 3. Matriz de Decisão A/B/C

| Dimensão | Cenário A | Cenário B | Cenário C |
|---|---|---|---|
| **Descrição** | Revisão/síntese/especificação conceitual | Demonstração de viabilidade com artefatos consolidados | Experimento/implementação própria |
| **O que o TCC apresenta** | Estado da arte + especificação do protótipo | Especificação + execução com ASSISTments (dados públicos) | Especificação + execução completa + análise por habilidade + BNCC crosswalk |
| **Dados necessários** | Nenhum novo obrigatório | ASSISTments (download público) | ASSISTments + possível SAEB para contextualização |
| **Treinamento próprio** | Não | Opcional (reutilizar baselines) | Provável (baselines + LR + HGB) |
| **Protótipo executável** | Não obrigatório | Desejável (demo funcional) | Necessário |
| **BNCC** | Fundamentação/especificação | Crosswalk demonstrativo possível | Crosswalk + discussão curricular |
| **Explicabilidade** | Revisão da literatura | LR exata + permutation importance | LR exata + permutation + possível SHAP (se justificado) |
| **Evidência permitida** | Síntese científica | Viabilidade técnica/metodológica | Desempenho técnico no protocolo executado |
| **Eficácia pedagógica** | Não demonstrada | Não demonstrada | Não demonstrada (sem estudo adicional) |
| **Custo de tempo** | ~2-3 semanas (revisão + escrita) | ~4-6 semanas (execução + escrita) | ~8-12 semanas (execução completa + BNCC + escrita) |
| **Risco** | Baixo | Médio (dados podem falhar) | Médio-alto (execução completa + validação) |
| **Contribuição central** | Revisão sistemática robusta + framework conceitual | Pipeline reproduzível + baselines calibrados | Pipeline + modelo + perfil de evidências + BNCC |
| **Diferencial** | Revisão 11.904→16 + procedimento MMAT pendente + framework | Revisão + execução reproduzível com dados reais | Revisão + execução + contextualização brasileira |
| **Requisito para banca** | TCC defensável | TCC defensável com demo | TCC defensável com resultados |

### Pergunta-chave para cada cenário

**Cenário A:** "O que o TCC contribui sem executar o protótipo?"
- Resposta: Revisão sistemática reconciliada (11.904→16), procedimento MMAT definido mas ainda pendente para o conjunto atual, framework conceitual e especificação do protótipo como artefato reproduzível.

**Cenário B:** "É possível demonstrar viabilidade sem treinar do zero?"
- Resposta: Sim, com baselines calibrados (probabilidade global, suavizada, LR). O ASSISTments permite executar o pipeline completo e produzir métricas reais.

**Cenário C:** "O que se ganha com execução completa?"
- Resposta: Perfil de evidências por habilidade, análise de explicabilidade, contextualização BNCC. Mas: não valida eficácia pedagógica.

---

## 4. O que o orientador precisa decidir

1. **Cenário:** A, B ou C?
2. **Dataset:** ASSISTments (primário), SAEB (contextualização), ou outro?
3. **HBNCC:** Crosswalk demonstrativo (B) ou validação metodológica (C)?
4. **Explicabilidade:** LR exata (já implementada) + permutation (já implementada) + SHAP (a avaliar)?
5. **Título:** Manter, alterar, ou decidir após cenário?
6. **Atualização 2026:** Incluir literatura recente ou manter recorte 2016-2025?
7. **Harmonizável:** Execução em outro ambiente necessário? (Capacidades: Python, GPU, datasets)
8. **Próxima entrega:** Versão do TCC com que nível de completude?

---

## 5. Capacidades deste ambiente vs. necessário

### Capacidades disponíveis (agente/Claude Code)

- ✅ Git + GitHub (PRs, issues, CI)
- ✅ Node.js (Slidev para deck)
- ✅ Leitura/escrita de código e documentos
- ✅ Web search (literatura)
- ✅ Revisão de diffs e código
- ❌ Python (não está no PATH — `.venv/` existe mas não ativado)
- ❌ GPU
- ❌ Datasets reais (não baixados)
- ❌ pdflatex (não verificado)

### Capacidades necessárias para Cenário B ou C

| Capacidade | Cenário B | Cenário C | Disponível? |
|---|---|---|---|
| Python 3.11+ | Sim | Sim | ⚠️ .venv existe, precisa ativar |
| pandas, scikit-learn, pyarrow | Sim | Sim | ⚠️ No pyproject.toml, precisa instalar |
| ASSISTments download | Sim | Sim | ❌ Revisão de termos necessária |
| Execução de notebooks/scripts | Sim | Sim | ⚠️ Depende de Python |
| Slidev (deck) | Não | Não | ⚠️ npx disponível |
| GPU | Não | Não | ❌ Não disponível |
| SAEB download | Opcional | Opcional | ✅ Download público INEP |
| BNCC mapeamento | Manual | Manual | ✅ Revisão humana |

---

## 6. Recomendação para a reunião

### Antes da reunião (pode ser feito agora)

1. **Preparar deck Slidev** com:
   - Estado do TCC (revisão, MMAT, especificação)
   - Inventário implementado vs. especificado
   - Matriz científica
   - Matriz de decisão A/B/C
   - Perguntas para o orientador

2. **Verificar se Python funciona** no .venv local

3. **Revisar PRs abertas** (#16 aquisição, #18 workflow, #19 artefatos, #20 governança, #23 editorial) — nenhuma deve ser mesclada antes da decisão

### Na reunião

- Apresentar material como **apresentação de decisão**, não de banca
- Deixar claro o que é código vs. evidência real
- Registrar decisão no template da issue #27

### Após a reunião

- Atualizar issue #27 com registro da decisão
- Classificar lotes como necessário/opcional/demonstrativo/fora do escopo
- Iniciar execução conforme cenário escolhido
