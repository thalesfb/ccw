# Artefatos de Análise e Relatórios

Este projeto mantém, por padrão, os arquivos de análise produzidos na exportação para facilitar auditoria, reprodutibilidade e exploração adicional.

## Onde ficam os arquivos
- Base: `research/exports`
- Análises (tabelas para exploração): `research/exports/analysis/`
- Visualizações (gráficos): `research/exports/visualizations/`
- Relatórios (HTML): `research/exports/reports/`

## Arquivos principais em `analysis/`
- `papers.xlsx`, `papers.csv`, `papers.json`: conjunto de artigos utilizado para gerar visualizações e relatórios (já deduplicado para evitar artefatos inconsistentes nas planilhas).
- `revisao_sistematica.xlsx`: versão com abas filtradas, útil para navegação por critérios.
- `deduplicated_rows.csv`: relatório de linhas removidas na deduplicação local feita apenas para os artefatos de análise.

### Sobre `deduplicated_rows.csv`
- O objetivo é transparência: mostra quais registros foram eliminados durante a deduplicação aplicada aos arquivos de análise.
- A ordem de preferência preserva o registro com maior completude (prioriza presença de DOI, resumo e ano) e remove os demais equivalentes por DOI ou por título normalizado.
- Este relatório não altera a contagem “canônica” de identificação do PRISMA. A contagem “Identificados” no PRISMA é derivada do total antes da deduplicação (pré-dedup), registrado durante o processamento.

## PRISMA – Semântica das contagens
- **Identificados (Identification):** total coletado antes da deduplicação (pré-dedup). É extraído dos `dedup_stats` do pipeline e propagado para os relatórios.
- **Duplicatas removidas:** quantidade removida pela deduplicação inicial do pipeline (não a deduplicação de conveniência aplicada aos arquivos de análise).
- **Triagem (Screening):** total encaminhado para triagem; no fluxo atual, todos os identificados pós-dedup são triados.
- **Elegibilidade (Eligibility):** artigos que passam da triagem com score mínimo.
- **Incluídos (Included):** artigos finais após elegibilidade e limite máximo opcional.

## Limpeza opcional
- Por padrão, os artefatos de análise são mantidos.
- Para remover arquivos `analysis/*` após a exportação, use o parâmetro de CLI `--cleanup-analysis`.
