# Exports da Revisão Sistemática

Este diretório preserva saídas geradas pelo fluxo de revisão sistemática. Os arquivos de dados e relatórios devem ser tratados como **snapshots de uma execução**, e não como documentação manual do protocolo.

## Snapshot utilizado pelo TCC

O arquivo `reports/summary.json` preserva as contagens consolidadas usadas na versão atual do TCC:

| Etapa | Contagem |
| --- | ---: |
| Registros identificados | 9.431 |
| Duplicatas removidas | 2.517 |
| Registros únicos / triagem | 6.914 |
| Elegibilidade | 1.883 |
| Excluídos na elegibilidade | 1.866 |
| Estudos incluídos | 17 |

O mesmo export registra contribuição de Crossref, OpenAlex, Semantic Scholar e CORE e distribuição temporal entre 2015 e 2025 para os registros dentro da janela reportada.

A reconstrução do protocolo e suas limitações está documentada em `../protocol_execution_2025.json`. Esse manifesto deve ser consultado quando for necessário distinguir:

- configuração versionada;
- números preservados nos exports;
- informações que não podem ser reconstruídas retrospectivamente, como um log completo de todas as requisições HTTP da coleta histórica.

## Estrutura atual

```text
exports/
├── analysis/        # dados e tabelas de análise preservados
├── references/      # referências e tabela MMAT gerada
├── reports/         # relatórios HTML/JSON
└── visualizations/  # figuras utilizadas na análise/TCC
```

Entre os artefatos diretamente relevantes para o documento estão:

- `reports/summary.json` — contagens e estatísticas consolidadas;
- `reports/papers_report_included.html` — relatório dos estudos incluídos;
- `reports/gap_analysis.html` — relatório de lacunas;
- `references/mmat_tcc_table.tex` — tabela MMAT consumida pelo LaTeX;
- `analysis/mmat_assessment.csv` — export da avaliação metodológica;
- `visualizations/prisma_flow.png` — fluxo de seleção;
- `visualizations/selection_funnel.png` — funil de seleção;
- `visualizations/database_coverage.png` — contribuição das fontes.

## Regeneração

Os exports são produzidos pelo código de `research/src/`. Em uma execução local com o banco correspondente, os comandos principais são:

```bash
python -m research.src.cli stats
python -m research.src.cli export
```

O banco histórico de 2025 não é distribuído nesta branch. Consequentemente, executar novamente o pipeline contra APIs atuais constitui uma **nova coleta**, que deve produzir seus próprios artefatos e não substituir silenciosamente os snapshots utilizados no TCC.

## Regras de consistência

- não editar números do TCC sem confrontá-los com os artefatos versionados;
- não substituir exports históricos por uma nova execução sem registrar data e protocolo;
- não interpretar a pontuação de relevância como qualidade metodológica;
- manter as avaliações MMAT por critério, sem escore agregado;
- uma eventual atualização para 2026 deve permanecer separada do corpus histórico até a deduplicação e triagem, conforme a issue #26.

Números históricos antigos que não correspondem ao corpus atual do TCC não devem ser mantidos neste README como se fossem o estado vigente.
