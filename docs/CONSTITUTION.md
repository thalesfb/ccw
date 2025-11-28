# Constituição do Projeto — ccw

> Ensino Personalizado de Matemática: Diagnóstico de competências em matemática para adaptação do aprendizado; foco atual na revisão sistemática automatizada e infraestrutura de coleta/análise para fundamentar o produto final.

## 1) Propósito e Escopo

- Objetivo geral: apoiar professores de matemática no ensino personalizado através do diagnóstico de competências com base em evidências.
- Escopo atual: módulo research com pipeline modular para revisão sistemática (coleta, cache, deduplicação, scoring, seleção PRISMA, exports e logs).
- Produto final: ainda em concepção; expansão futura no diretório `src/` para protótipo/aplicação principal que consumirá a base de evidências para avaliação do que a comunidade já fez.

## 2) Arquitetura e Módulos

- Clientes de APIs: Semantic Scholar, OpenAlex, Crossref, CORE (CORE pode ser instável).
- Gerenciador de dados: SQLite (`research/systematic_review.sqlite`)
- Processamento: deduplicação (DOI/URL + similaridade de títulos), scoring multi-critério, seleção por critérios PRISMA.
- Exports: planilhas (CSV/XLSX), relatórios HTML e visualizações em `research/exports/`.
- Logs: auditoria e execução em `research/logs/`.

Estrutura operacional consolidada:

- Banco: `research/systematic_review.sqlite` (criado automaticamente pela CLI/pipeline).
- Exports: `research/exports/…` (planilhas, relatórios, gráficos).
- Logs de auditoria: `research/logs/…` (sem dados sensíveis).

## 3) Scripts e Pontos de Entrada

- Pipeline: `research/src/pipeline/run.py` (pipeline canônico com `SystematicReviewPipeline`).
- CLI: `research/src/cli.py` com comandos como `init-db`, `run-pipeline`, `stats`, `export`.
- Testes: `research/tests/` com variações quick/full/benchmark.

Exemplos de uso (terminal):

- Inicialização do banco: `python -m research.src.cli init-db`
- Execução do pipeline: `python -m research.src.cli run-pipeline`
- Estatísticas rápidas: `python -m research.src.cli stats`

Uso programático (Python):

- `from research.src.pipeline.run import SystematicReviewPipeline, run_systematic_review`

## 4) Configuração por Ambiente (.env)

Variáveis típicas (sem expor segredos):

- APIs: `SEMANTIC_SCHOLAR_API_KEY` (opcional), `CORE_API_KEY` (opcional), `USER_EMAIL` (para identificação em APIs que exigem contato).
- Rate limits (segundos): `SEMANTIC_SCHOLAR_RATE_DELAY`, `OPENALEX_RATE_DELAY`, `CROSSREF_RATE_DELAY`.
- Critérios PRISMA: `REVIEW_YEAR_MIN`, `REVIEW_YEAR_MAX`, `REVIEW_LANGUAGES` (ex.: `en,pt`), `REVIEW_RELEVANCE_THRESHOLD` (limiar de relevância).

Atenção: não versionar `.env` no repositório; usar `.env.example` como referência.

## 5) Estado Atual

- Pipeline cobre a fase inicial do TCC (revisão sistemática automatizada) e gera base de evidências reprodutível.
- Produto principal (diagnóstico e recomendações) seguirá em `src/` na próxima fase.

## 6) Roadmap de Evolução (alto nível)

- Melhorias na classificação/scoring (ML supervisionado, NLP para abstracts).
- Processamento paralelo/assíncrono para coleta e processamento.
- Integrações adicionais (ex.: PubMed, DBLP; export para Zotero/Mendeley).
- Dashboard e automações (monitoramento, agendamento, relatórios contínuos).
- Expansão do produto principal em `src/` (modelagem de competências e recomendações).

## 7) Diretrizes de Engenharia

- SOLID/DRY/KISS/YAGNI.
- Manter logs sem segredos (mas com rastreabilidade completa de execução).
- Registrar TODOs diretamente no código quando aplicável.
- Executar `pytest` a cada alteração relevante no pipeline (tests quick → full → benchmark conforme necessidade).
- Documentar avanços e decisões arquiteturais.

## 8) Critérios de Qualidade e Sucesso

- Reprodutibilidade: execução determinística com versão de termos de busca e parâmetros.
- Cobertura de fontes: múltiplas APIs com fallback; deduplicação robusta; metadados normalizados.
- Qualidade dos dados: preenchimento adequado de campos críticos; scoring consistente; rastreio PRISMA.
- Observabilidade: logs de auditoria, métricas básicas e relatórios exportados.

## 9) Governança de Mudanças

- Novas integrações: respeitar limites das APIs, adicionar config no `.env.example` e cobertura de testes.
- Segurança: garantir que chaves/credenciais nunca apareçam em logs, exports ou versionamento.

## 10) Referências e Links

- README (raiz) — visão geral do TCC e estrutura do repositório.
- `research/README.md` — documentação técnica detalhada do pipeline.
- PRISMA: [http://www.prisma-statement.org/](http://www.prisma-statement.org/)

---

Última atualização: Novembro/2025
