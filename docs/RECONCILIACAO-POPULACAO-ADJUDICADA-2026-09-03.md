# Reconciliação da População Adjudicada da Revisão Sistemática

**Snapshot vigente:** 03/09/2026
**Commit de consolidação:** `5d72bf6` (PR #55)
**Fonte versionada:** `research/exports/analysis/papers.csv`, `summary.json` e
`research/data/current_synthesis_scope.csv`
**Ledger de decisões:** `research/data/adjudicated_population_decisions.csv`

## Escopo deste documento

Este documento descreve a população resultante das decisões de escopo aprovadas
no PR #54 e implementadas no PR #55. Ele é a referência pública para o snapshot
vigente. A execução local do SQLite permanece útil para diagnóstico operacional,
mas não contém as decisões adjudicadas e não deve substituir os artefatos
versionados.

O manuscrito do TCC ainda é uma unidade de trabalho separada. Este documento
não autoriza inserir no TCC o histórico de PRs, discussões internas ou detalhes
de implementação que não sejam necessários ao relato científico.

## Fluxo PRISMA vigente

| Etapa | Entraram | Excluídos/removidos | Avançaram/retidos |
| --- | ---: | ---: | ---: |
| Identificação | 11.904 | 27 por identidade DOI/URL | 11.877 |
| Triagem | 11.877 | 9.391 (78,89%) | 2.486 (20,88%) |
| Elegibilidade | 2.486 | 2.468 (99,28%) | 18 (0,72%) |
| Inclusão | 18 | — | 18 |

A taxa de inclusão em relação à identificação é **0,15%**. As porcentagens
usam o denominador indicado em cada etapa; não são porcentagens de qualidade
metodológica.

### Deduplicação

A auditoria atual não é uma contagem zero. As 27 remoções determinísticas são:

- 25 linhas excedentes em 25 grupos de DOI normalizado;
- 2 linhas excedentes em 2 grupos de URL exata;
- 0 linhas removidas apenas pela flag persistida do SQLite.

Há ainda 177 grupos de título normalizado, com 257 excedentes brutos. Depois da
remoção DOI/URL, 232 excedentes permanecem apenas por título. Eles são
candidatos à auditoria semântica e não foram removidos automaticamente, porque
títulos iguais podem representar versões, erratas ou obras distintas.

## Como 16 registros se tornaram 18

A mudança não é uma simples substituição do número 16 por 18. A auditoria
histórica preservou um universo de 23 candidatos: 16 registros retidos no
snapshot operacional anterior e 7 overrides manuais. As oito decisões de
escopo aprovadas no PR #54 foram aplicadas em nível de linha:

| ID | Disposição vigente | Consequência |
| ---: | --- | --- |
| 14 | `include` | recuperado como candidato empírico provisório |
| 15 | `exclude_computational_centrality` | permanece fora por ausência de técnica computacional avaliada |
| 6915 | `include` | recuperado como candidato empírico provisório; publicações agregadas não são contadas novamente sem extração independente |
| 6918 | `exclude_temporal` | ano bibliográfico corrigido para 2014; fora do recorte 2015--2026 |
| 6919 | `include` | recuperado como candidato empírico provisório |
| 6922 | `exclude_document_type` | relatório final de projeto; não é estudo empírico elegível |
| 6925 | `exclude_outcome_specificity` | desfecho STEM composto sem resultado matemático separável |
| 6926 | `exclude_domain` | matemática é apenas variável preditora em estudo de educação moral |

Assim, o efeito líquido foi `16 - 1 + 3 = 18`. O ledger registra as fontes, a
regra aplicada, o estado da decisão e a data de verificação. A decisão de
escopo não é uma nota de qualidade e não substitui a avaliação metodológica.

## População retida e papel na síntese

Os 18 IDs do snapshot são:

```text
1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
14, 6915, 6916, 6917, 6919, 6920, 6921, 6923
```

O arquivo `current_synthesis_scope.csv` distingue 17 candidatos empíricos
provisórios do ID 6921, que permanece como protocolo/proposta contextual. O
6921 não sustenta resultado empírico nem entra em uma síntese quantitativa ou
em uma avaliação MMAT empírica.

O artigo identificado pelo ID 6918 não pertence à população atual: a fonte
institucional confirma o ano 2014, fora do recorte 2015--2026. A ocorrência
permanece auditável no export, mas não deve ser citada como estudo incluído.

## MMAT e referências

O ledger MMAT atual foi alinhado aos 18 registros para impedir que a tabela
histórica de 17 estudos seja usada como denominador atual. Essa etapa é
**preliminar**: os critérios, fontes e localizadores ainda exigem consolidação
e adjudicação pelo supervisor. Não há nota média, ranking ou conclusão de
qualidade metodológica final.

`research/exports/references/included_papers.bib` contém somente as referências
derivadas da população do pipeline. As referências teóricas, pedagógicas,
metodológicas e técnicas usadas na fundamentação do TCC permanecem na
bibliografia completa e não devem ser removidas por não pertencerem ao fluxo de
descoberta.

## Reprodução sem distribuir o SQLite

Os artefatos versionados podem ser verificados e regenerados sem distribuir o
banco local:

```bash
python -m research.src.validation.versioned_snapshot
python -m research.src.processing.adjudicated_snapshot --check
python -m research.src.processing.adjudicated_snapshot
```

O manifesto `research/exports/reports/reproducibility_manifest.json` registra os
hashes, o ledger de decisões, a separação entre o snapshot versionado e o
diagnóstico local do SQLite e a limitação da reavaliação MMAT.

## Histórico preservado

Os valores 9.431 identificados, 2.517 duplicatas e 17 incluídos pertencem à
execução histórica anterior. Eles continuam preservados para rastreabilidade,
mas não são contagens do snapshot vigente. A documentação legada
`docs/RECONCILIACAO-BASELINE-2026-08-31.md` deve ser lida com esse escopo
histórico; ela não substitui este documento.

## Próximas unidades

1. consolidar a recuperação das fontes e a adjudicação final do MMAT;
2. sincronizar o TCC com esta população, sem expor histórico interno de
   desenvolvimento;
3. revisar e reconstruir a apresentação Slidev a partir do TCC e dos artefatos
   vigentes.
