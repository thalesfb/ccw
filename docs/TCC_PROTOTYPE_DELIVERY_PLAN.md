# Plano de entrega do protótipo científico

## 1. Objetivo

Este documento define como a implementação do protótipo será entregue para revisão. O trabalho será dividido em lotes pequenos, verificáveis e semanticamente coesos, evitando que decisões bibliográficas, metodológicas, técnicas e de interface sejam misturadas no mesmo conjunto de alterações.

O plano está associado à issue #7 e utiliza o PR nº 6 como linha de base acadêmica inicial.

## 2. Estratégia de branches e pull requests

A implementação utilizará PRs empilhados enquanto o lote anterior ainda não estiver incorporado à branch principal.

Exemplo:

```text
main
  └── agent/revise-tcc-methodology             PR #6
        └── agent/tcc-prototype-governance     lote 1
              └── agent/tcc-reference-audit    lote 2
                    └── agent/tcc-experiment-design
```

Cada PR deverá declarar:

- branch-base;
- dependências;
- arquivos alterados;
- decisões incluídas;
- decisões deliberadamente excluídas;
- testes executados;
- riscos e limitações;
- próximo lote previsto.

Depois que uma dependência for incorporada, o PR subsequente poderá ser redirecionado para a nova base apropriada.

## 3. Convenção de commits

Cada commit deverá representar uma unidade de revisão independente.

Categorias previstas:

- `docs(tcc)`: redação acadêmica e documentos de decisão;
- `docs(data)`: proveniência, licença, dicionário e contrato dos dados;
- `test(data)`: testes de esquema e qualidade;
- `feat(data)`: ingestão, transformação e armazenamento;
- `test(model)`: testes de baselines, métricas e determinismo;
- `feat(model)`: treinamento e inferência;
- `feat(report)`: geração de tabelas, figuras e relatórios;
- `feat(prototype)`: camada de apresentação ao professor;
- `ci(tcc)`: validações automatizadas acadêmicas e técnicas;
- `fix(bib)`: correções bibliográficas verificadas.

Um commit não deverá combinar, por exemplo, correções de DOI com implementação de modelo ou alterações de interface.

## 4. Sequência de lotes

### Lote 1 — governança científica

**Objetivo:** registrar as decisões aprovadas antes de alterar o desenho experimental ou o código.

**Entregas:**

- decisões científicas do protótipo;
- plano de PRs e commits;
- limites explícitos das conclusões;
- regra de rastreabilidade entre experimento e redação.

**Critério de aceitação:** os documentos distinguem claramente alvo estatístico, saída probabilística, resultado pedagógico e conclusões permitidas.

### Lote 2 — auditoria bibliográfica

**Objetivo:** transformar a validação das referências em artefato auditável e corrigir a bibliografia.

**Commits previstos:**

1. adicionar matriz de auditoria bibliográfica;
2. corrigir referências canônicas e pedagógicas;
3. corrigir metadados dos estudos empíricos;
4. alinhar afirmações do texto às fontes;
5. adicionar testes de integridade das citações.

**Arquivos esperados:**

- `results/tcc/referencias.bib`;
- `results/tcc/referencias_pedagogicas.bib`;
- capítulos `.tex` afetados;
- matriz de evidências em `research/data/` ou `docs/`;
- testes de chaves citadas, DOI e campos obrigatórios.

**Exclusões:** nenhuma implementação de dados ou modelagem.

### Lote 3 — desenho experimental

**Objetivo:** formalizar o experimento antes da seleção definitiva da implementação.

**Commits previstos:**

1. formalizar pergunta e hipóteses;
2. definir unidade de análise e alvo;
3. definir estratégia de divisão de dados;
4. definir baselines, métricas e critérios de comparação;
5. atualizar a metodologia prospectiva da implementação.

**Critério de aceitação:** todas as decisões necessárias para evitar seleção oportunista de métricas ou modelos estão registradas antes da avaliação final.

### Lote 4 — seleção e governança dos dados

**Objetivo:** selecionar a base principal mediante critérios científicos e técnicos.

**Commits previstos:**

1. adicionar matriz comparativa das bases candidatas;
2. registrar decisão da base principal e possíveis bases de apoio;
3. documentar licença, proveniência e limitações;
4. criar dicionário de dados;
5. criar contrato de esquema e testes iniciais.

**Critério de aceitação:** a base escolhida possui granularidade compatível com estudante, item, habilidade e tempo, ou as limitações dessa compatibilidade estão formalmente registradas.

### Lote 5 — ingestão e qualidade dos dados

**Objetivo:** implementar pipeline determinístico desde a fonte até uma camada analítica normalizada.

**Commits previstos:**

1. criar configuração e manifestos de origem;
2. implementar download ou importação local controlada;
3. implementar validação de arquivos brutos;
4. normalizar interações;
5. persistir Parquet e catálogo DuckDB;
6. adicionar relatório de qualidade;
7. adicionar testes de determinismo e esquema.

**Critério de aceitação:** uma execução limpa produz o mesmo esquema e artefatos equivalentes a partir da mesma versão dos dados.

### Lote 6 — baselines e protocolo de avaliação

**Objetivo:** estabelecer referências mínimas antes de modelos complexos.

**Commits previstos:**

1. implementar divisão temporal e prevenção de vazamento;
2. implementar frequência global;
3. implementar frequências por estudante e habilidade;
4. implementar regressão logística;
5. implementar métricas e calibração;
6. gerar relatório comparativo reproduzível.

**Critério de aceitação:** os baselines são executáveis, testados e geram métricas versionadas.

### Lote 7 — modelo não linear e interpretabilidade

**Objetivo:** testar se maior complexidade oferece ganho justificável.

**Commits previstos:**

1. implementar modelo baseado em árvores;
2. registrar busca limitada de hiperparâmetros;
3. comparar discriminação e calibração;
4. gerar explicações globais;
5. gerar explicações locais;
6. avaliar estabilidade e diferenças entre habilidades.

**Critério de aceitação:** qualquer modelo recomendado demonstra ganho sobre os baselines e mantém condições adequadas de calibração e interpretação.

### Lote 8 — perfil de domínio e fragilidade

**Objetivo:** converter resultados técnicos em uma saída pedagógica conservadora.

**Commits previstos:**

1. implementar agregação por habilidade;
2. calcular quantidade e recência das evidências;
3. definir níveis ordinais versionados;
4. implementar regras de alerta opcional;
5. gerar casos de teste e exemplos auditáveis.

**Critério de aceitação:** toda classificação apresentada pode ser rastreada até interações, probabilidades, versão do modelo e regra de agregação.

### Lote 9 — protótipo de apresentação docente

**Objetivo:** disponibilizar os resultados de forma compreensível sem automatizar decisões pedagógicas.

**Commits previstos:**

1. criar API ou camada de consulta;
2. criar visão individual;
3. criar visão agregada por turma ou conjunto;
4. exibir explicações, incerteza e limitações;
5. permitir exportação;
6. adicionar testes de acessibilidade e contratos.

**Critério de aceitação:** a interface apresenta evidências e limitações, não prescrições automáticas.

### Lote 10 — integração ao texto do TCC

**Objetivo:** atualizar o trabalho acadêmico somente com resultados realmente reproduzidos.

**Commits previstos:**

1. atualizar metodologia executada;
2. atualizar arquitetura implementada;
3. incluir dados e pré-processamento;
4. incluir resultados e baselines;
5. incluir análise de erros, calibração e subgrupos;
6. atualizar discussão e limitações;
7. gerar tabelas e figuras automaticamente;
8. revisar resumo e conclusão.

**Critério de aceitação:** nenhuma afirmação quantitativa depende de edição manual ou de resultado não rastreável.

## 5. Política de testes

Cada lote técnico deverá introduzir ou atualizar testes compatíveis com sua responsabilidade.

### Dados

- schema;
- domínios e tipos;
- chaves e duplicidade;
- ordenação temporal;
- valores ausentes;
- determinismo;
- prevenção de vazamento.

### Modelos

- formato de entrada e saída;
- probabilidades válidas;
- reprodutibilidade por seed;
- comportamento dos baselines;
- cálculo das métricas;
- serialização e carregamento.

### Relatórios

- presença de proveniência;
- correspondência entre métricas e artefatos;
- ausência de edição manual nas tabelas utilizadas pelo TCC;
- estabilidade do formato esperado.

### Texto acadêmico

- chaves de citação existentes;
- referências efetivamente citadas;
- ausência de linguagem que transforme estimativas em diagnósticos;
- consistência entre números do texto e artefatos gerados;
- compilação LaTeX.

## 6. Política de atualização do TCC

A redação acadêmica seguirá três estados:

1. **decisão planejada:** registrada em documentos de desenho, sem ser apresentada como resultado;
2. **implementação executada:** descrita na metodologia após existir código versionado;
3. **resultado validado:** incorporado a resultados e discussão após reprodução automatizada.

O texto não poderá antecipar resultados, métricas ou eficácia.

## 7. Política de revisão em lotes

Cada PR deverá ser pequeno o suficiente para permitir revisão temática. Recomenda-se:

- até um contexto científico principal por PR;
- commits ordenados da documentação para os testes e, depois, para a implementação;
- ausência de mudanças cosméticas não relacionadas;
- comentários claros quando uma decisão permanecer provisória;
- PR em modo rascunho enquanto critérios de aceitação não estiverem completos;
- nenhuma mesclagem automática.

## 8. Dependências iniciais

| Lote | Branch-base prevista | Dependência |
|---|---|---|
| 1 | `agent/revise-tcc-methodology` | PR #6 |
| 2 | `agent/tcc-prototype-governance` | lote 1 |
| 3 | branch do lote 2 | auditoria bibliográfica |
| 4 | branch do lote 3 | desenho experimental |
| 5 | branch do lote 4 | decisão dos dados |
| 6 | branch do lote 5 | pipeline normalizado |
| 7 | branch do lote 6 | baselines |
| 8 | branch do lote 7 | probabilidades avaliadas |
| 9 | branch do lote 8 | perfil por habilidade |
| 10 | branch do lote 9 | implementação e resultados |

## 9. Estado do plano

**Status:** ativo.

**Issue de acompanhamento:** #7.

**Linha de base:** PR #6.

**Primeiro lote:** `agent/tcc-prototype-governance`.
