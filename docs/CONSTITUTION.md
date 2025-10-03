# Constituição do Projeto — ccw

> Apoio ao TCC: Diagnóstico de competências em matemática; foco atual na revisão sistemática automatizada e infraestrutura de coleta/análise.

## 1) Propósito e Escopo

- Objetivo geral: apoiar professores de matemática no diagnóstico de competências e na otimização de planos de ensino com base em evidências.
- Escopo atual: módulo research com pipeline modular para revisão sistemática (coleta, cache, deduplicação, scoring, seleção PRISMA, exports e logs).
- Produto final: ainda em concepção; expansão futura no diretório `src/` para protótipo/aplicação principal que consumirá a base de evidências.

## 2) Arquitetura e Módulos

- Clientes de APIs: Semantic Scholar, OpenAlex, Crossref, CORE (CORE pode ser instável).
- Gerenciador de dados: SQLite (`research/systematic_review.db`), com cache local por API (JSON) em `research/cache/`.
- Processamento: deduplicação (DOI/URL + similaridade de títulos), scoring multi-critério, seleção por critérios PRISMA.
- Exports: planilhas (CSV/XLSX), relatórios HTML e visualizações em `research/exports/`.
- Logs: auditoria e execução em `research/logs/`.

Estrutura operacional consolidada:

- Cache por API: `research/cache/{semantic_scholar|openalex|crossref|core}/`.
- Banco: `research/systematic_review.db` (criado automaticamente pela CLI/pipeline).
- Exports: `research/exports/…` (planilhas, relatórios, gráficos).
- Logs de auditoria: `research/logs/…` (sem dados sensíveis).

## 3) Scripts e Pontos de Entrada

- Pipeline: `research/src/pipeline/improved_pipeline.py` (ou equivalente em `research/src/pipeline/`).
- CLI: `research/src/cli.py` com comandos como `init-db`, `run-pipeline`, `stats`, `export`.
- Testes: `research/tests/` com variações quick/full/benchmark.

Exemplos de uso (terminal):

- Inicialização do banco: `python -m research.src.cli init-db`
- Execução do pipeline: `python -m research.src.cli run-pipeline`
- Estatísticas rápidas: `python -m research.src.cli stats`

Uso programático (Python):

- `from research.src.pipeline.improved_pipeline import ImprovedSystematicReviewPipeline`

## 4) Configuração por Ambiente (.env)

Variáveis típicas (sem expor segredos):

- APIs: `SEMANTIC_SCHOLAR_API_KEY` (opcional), `CORE_API_KEY` (opcional), `USER_EMAIL` (para identificação em APIs que exigem contato).
- Rate limits (segundos): `SEMANTIC_SCHOLAR_RATE_DELAY`, `OPENALEX_RATE_DELAY`, `CROSSREF_RATE_DELAY`.
- Critérios PRISMA: `REVIEW_YEAR_MIN`, `REVIEW_YEAR_MAX`, `REVIEW_LANGUAGES` (ex.: `en,pt`), `REVIEW_RELEVANCE_THRESHOLD`.

Atenção: não versionar `.env` no repositório; usar `.env.example` como referência.

## 5) Estado Atual

- Refatoração do módulo research concluída e validada (pipeline modular, testes de validação, cache e logs).
- Pipeline cobre a fase inicial do TCC (revisão sistemática automatizada) e gera base de evidências reprodutível.
- Produto principal (diagnóstico e recomendações) seguirá em `src/` na próxima fase.

## 6) Roadmap de Evolução (alto nível)

- Processamento paralelo/assíncrono para coleta e processamento.
- Integrações adicionais (ex.: PubMed, DBLP; export para Zotero/Mendeley).
- Dashboard e automações (monitoramento, agendamento, relatórios contínuos).
- Expansão do produto principal em `src/` (modelagem de competências e recomendações).

## 7) Diretrizes de Engenharia

- SOLID/DRY/KISS/YAGNI.
- Manter logs sem segredos (mas com rastreabilidade completa de execução).
- Registrar TODOs diretamente no código quando aplicável e no `research/refactoring_plan.md`.
- Executar `pytest` a cada alteração relevante no pipeline (tests quick → full → benchmark conforme necessidade).
- Documentar avanços e decisões arquiteturais no `research/refactoring_plan.md`.

## 8) Critérios de Qualidade e Sucesso

- Reprodutibilidade: execução determinística com versão de termos de busca e parâmetros.
- Cobertura de fontes: múltiplas APIs com fallback; deduplicação robusta; metadados normalizados.
- Qualidade dos dados: preenchimento adequado de campos críticos; scoring consistente; rastreio PRISMA.
- Observabilidade: logs de auditoria, métricas básicas e relatórios exportados.

## 9) Governança de Mudanças

- Mudanças no pipeline: abrir PR com descrição, checklist de testes (quick/full) e atualização de docs.
- Novas integrações: respeitar limites das APIs, adicionar config no `.env.example` e cobertura de testes.
- Segurança: garantir que chaves/credenciais nunca apareçam em logs, exports ou versionamento.

## 10) Referências e Links

- README (raiz) — visão geral do TCC e estrutura do repositório.
- `research/README.md` — documentação técnica detalhada do pipeline.
- `research/refactoring_plan.md` — histórico e plano com TODOs.
- PRISMA: [http://www.prisma-statement.org/](http://www.prisma-statement.org/)

---

Última atualização: Outubro/2025
