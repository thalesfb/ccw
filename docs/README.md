# Documentação do projeto

Este diretório reúne governança, decisões e auditorias. Os relatórios da revisão
estão em [`research/exports/`](../research/exports/), não em `docs/`.

## Referências atuais

- [Texto e PDF do TCC](../results/tcc/README.md): fonte do relato científico.
- [Estado, escopo e pendências](tcc/ESTADO-ATUAL-TCC.md): entrega documental e
  limites da apreciação MMAT preliminar.
- [Cobertura e contribuições das fontes](tcc/SOURCE-COVERAGE-AND-CONTRIBUTIONS.md):
  disponibilidade atual, cobertura de leitura e contribuições delimitadas.
- [Reconciliação da população](RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md):
  estágios distintos da seleção e proveniência das contagens.
- [Governança documental e normativa](tcc/README.md): documentos implementados,
  propostas futuras e limites de conformidade institucional.
- [Sincronização dos materiais](tcc/DOCUMENTATION_SYNC.md): geração dos trechos
  repetidos e revisão das páginas, apresentações e imagens.
- [Operação do módulo de pesquisa](../research/README.md): comandos e distinção
  entre verificar o snapshot e executar uma nova coleta.

Notas e propostas históricas conservam sua data e seu escopo; não substituem
essas referências para descrever o estado atual.

## Relatórios e publicação

Os arquivos versionados incluem
[`summary_report.html`](../research/exports/reports/summary_report.html),
[`papers_report_included.html`](../research/exports/reports/papers_report_included.html),
[`gap_analysis.html`](../research/exports/reports/gap_analysis.html), a
[página MMAT](../research/exports/analysis/mmat_current.html) e as
[visualizações](../research/exports/visualizations/).

O [site público](https://thalesfb.github.io/ccw/) é publicado pelo
[workflow de Pages](../.github/workflows/publish-reports.yml), após a conclusão
com sucesso de `TCC quality` na `main`, ou por acionamento manual. O workflow
utiliza os artefatos versionados e o PDF validado; não executa uma nova busca.
Um PR aprovado nos testes ainda não significa que essa versão esteja publicada.

## Conferência local sem nova busca

Na raiz do checkout, com as dependências de pesquisa instaladas:

```bash
python -m research.src.validation.versioned_snapshot
python -m research.src.processing.adjudicated_snapshot --check
python scripts/sync_project_docs.py --check
```

Esses comandos verificam contratos e rastreabilidade. Não certificam revisão
científica completa, leitura humana das fontes ou aprovação da orientação.
