# 📚 Revisão Sistemática da Literatura - CCW Research

> **Baseline vigente (31/08/2026):** o banco consolidado contém 11.904 registros e 16 estudos incluídos. As seções de resultados históricos abaixo preservam os números de 9.431 registros e 17 incluídos como contexto; a fonte atual e a auditoria de DOI estão em [`docs/RECONCILIACAO-BASELINE-2026-08-31.md`](../docs/RECONCILIACAO-BASELINE-2026-08-31.md).

## 🎯 Visão Geral

Sistema modular para revisão sistemática da literatura em educação matemática com técnicas computacionais, com relato orientado pelo PRISMA 2020.

**Status atual**: ✅ Snapshot vigente reconciliado | 🧪 Testes-alvo da reconciliação validados | 📊 Visualizações PRISMA corretas

---

## ⚡ Quick Start

```bash
# 1. Instalar dependências
cd c:\dev\ccw
pip install -r research/requirements.txt

# 2. Configurar ambiente (opcional)
cp research/.env.example research/.env
# Editar .env com credenciais de APIs se necessário

# 3. Executar pipeline completo
python -m research.src.cli run-pipeline
python -m research.src.cli export

# 4. Ver resultados
# Os arquivos são gerados em research/exports/
```

---

## 🏗️ Arquitetura do Sistema

```text
research/
├── src/                          # Código fonte modular
│   ├── config.py                 # Configuração centralizada
│   ├── cli.py                    # CLI principal
│   ├── database/                 # Gerenciamento SQLite
│   │   ├── manager.py            # Interface do banco
│   │   └── schema.py             # Schema + migrations
│   ├── ingestion/                # Coleta de dados
│   │   ├── semantic_scholar.py  # Semantic Scholar API
│   │   ├── openalex.py           # OpenAlex API
│   │   ├── crossref.py           # Crossref API
│   │   └── core.py               # CORE API (instável)
│   ├── processing/               # Processamento de dados
│   │   ├── dedup.py              # Deduplicação DOI+TF-IDF
│   │   ├── scoring.py            # Score de relevância
│   │   ├── selection.py          # Seleção PRISMA
│   │   └── language_utils.py     # Detecção de idioma
│   ├── analysis/                 # Análise e visualização
│   │   ├── visualizations.py     # Gráficos PRISMA
│   │   └── reports.py            # Relatórios HTML
│   ├── exports/                  # Exportação de dados
│   │   └── excel.py              # Excel + CSV + JSON
│   └── pipeline/                 # Orquestração
│       └── run.py                # Pipeline completo
├── tests/                        # Testes automatizados
│   ├── test_prisma_stages.py     # ✅ Validação PRISMA
│   ├── test_complete_pipeline.py # Suite completa
│   └── test_performance_benchmark.py
├── exports/                      # Saídas geradas
│   ├── summary_report.html       # Relatório resumido
│   ├── papers_report.html        # Papers incluídos
│   ├── gap_analysis.html         # Análise de lacunas
│   ├── analysis/                 # Dados estruturados
│   ├── visualizations/           # Gráficos PNG
│   └── reports/                  # Relatórios completos
├── cache/                        # Cache de APIs
├── logs/                         # Logs de execução
└── systematic_review.sqlite      # Banco SQLite principal (fonte local não versionada)
```

---

## 🔍 Metodologia PRISMA

### Bases de Dados Integradas

| API | Cobertura | Status | Taxa de Sucesso |
|-----|-----------|--------|-----------------|
| **Semantic Scholar** | CS + multidisciplinar | ✅ Estável | >95% |
| **OpenAlex** | 250M+ works abertos | ✅ Estável | >95% |
| **Crossref** | Metadados DOI | ✅ Estável | >95% |
| **CORE** | Open access | ⚠️ Instável | ~70% |

### Estratégia de Busca

**72 queries bilíngues estruturadas** (48 inglês + 24 português) combinando:

**Termos Primários** (6 termos - domínio educacional):

- "mathematics education", "math learning", "mathematics teaching"
- "educação matemática", "aprendizagem matemática", "ensino de matemática"

**Termos Secundários** (22 termos - técnicas computacionais):

- Machine learning, artificial intelligence, deep learning, neural networks
- Adaptive learning, personalized learning, intelligent tutoring systems
- Learning analytics, educational data mining, predictive analytics
- Student modeling, competency identification, automated assessment
- E mais 10 termos relacionados

### Critérios de Seleção

**✅ Inclusão**:

- Artigos peer-reviewed (2015-2026, como critério planejado)
- Foco em técnicas computacionais + educação matemática
- Metodologia e evidências empíricas claras
- Idiomas: inglês ou português

**❌ Exclusão**:

- Metodologia insuficiente (abstract <50 palavras)
- Foco não-educacional (biologia, física sem contexto educacional)
- Conteúdo não-científico (editoriais, comentários)
- Baixa relevância (score <4.0)

### Fluxo PRISMA

O pipeline segue as fases padrão: Identificação → Deduplicação → Triagem →
Elegibilidade → Inclusão.

**Baseline vigente (31/08/2026)**:

- **Identificação**: 11.904 registros no snapshot consolidado
- **Triagem**: 11.904 avaliados; 9.413 excluídos; 2.491 avançaram
- **Elegibilidade**: 2.491 avaliados; 2.475 excluídos; 16 incluídos
- **Auditoria de candidatos**: 23 candidatos operacionais; 7 falsos positivos removidos manualmente
- **Incluídos**: 16 estudos no conjunto usado pela síntese

Os sete falsos positivos já estão contabilizados nas exclusões de elegibilidade.
O resultado atual decorre de nova ingestão, correção do scoring e auditoria de
pertinência; não é uma simples troca de 17 por 16. O SQLite permanece como
fonte operacional local, ignorada pelo Git. Para reconstituir o snapshot sem
distribuir o banco, use os exports versionados e
`research/exports/reports/reproducibility_manifest.json`.

**Baseline histórico (25/11/2025; não vigente)**:

- **Identificação**: 9.431 registros coletados
- **Duplicatas Removidas**: 2.517 (26,6%)
- **Screening**: 6.914 estudos únicos avaliados
- **Elegibilidade**: 1.883 avaliados em profundidade (excluídos na elegibilidade: 1.866 / 99,1%)
- **Incluídos**: 17 estudos (pontuação de relevância ≥ 4,0)

Os contadores acima pertencem ao snapshot histórico. O baseline vigente é
derivado do banco canônico `research/systematic_review.sqlite` e está
reconciliado em `docs/RECONCILIACAO-BASELINE-2026-08-31.md`.

Para obter os números atualizados execute:

```bash
# Mostrar contagens PRISMA diretamente do banco
python -m research.src.cli stats

# Ou consultar via SQL:
sqlite3 research/systematic_review.sqlite "SELECT COUNT(*) FROM papers;"
sqlite3 research/systematic_review.sqlite "SELECT COUNT(*) FROM papers WHERE selection_stage='included';"
```

Arquivos de exportação e relatórios em `research/exports/` contêm as versões
renderizadas (CSV/HTML/PNG) usadas para publicações e para o README. Sempre
consulte esses artefatos para números fixos gerados em uma execução específica.

---

## 🚀 Como Usar

### CLI Completo

```bash
# Executar pipeline completo
python -m research.src.cli run-pipeline
  --apis semantic_scholar openalex crossref core  # APIs específicas
  --min-score 4.5                            # Score mínimo customizado
  --limit-per-query 100                      # Limite por query

# Ver estatísticas
python -m research.src.cli stats

# Mostrar amostra de papers
python -m research.src.cli show

# Importar dados externos
python -m research.src.cli import-csv dados.csv

# Exportar com relatórios e visualizações
python -m research.src.cli export -o research/exports/

# Exportar incluindo extração de texto completo dos PDFs
python -m research.src.cli export --fetch-fulltext

# Extrair apenas artigos sem full_text no banco
python -m research.src.cli export --fetch-fulltext --only-missing

# Normalizar estágios PRISMA (se necessário)
python -m research.src.cli normalize-prisma
```

### Utilitários de Auditoria (Centralizados no CLI)

Use estes comandos em vez dos scripts avulsos em `tools/` e `research/scripts/`:

```bash
# Auditoria cruzada DB → Exports → PTC (gera JSON/MD em research/logs)
python -m research.src.cli audit

# Valida DB ↔ CSV ↔ summary.json (salva JSON em research/logs)
python -m research.src.cli validate-exports

# Checagem ampla de exports, incluindo parsing dos relatórios HTML
python -m research.src.cli check-exports

# Verificação de duplicatas/ausências/irrelevância no CSV (gera CSV de relatório)
python -m research.src.cli verify-papers --csv research/exports/analysis/papers.csv

# Regenera summary.json a partir do DB canônico
python -m research.src.cli regenerate-summary

# Gera o manifesto versionado do snapshot sem copiar o SQLite para o Git
python -m research.src.cli generate-manifest

# Diagnostica por que um paper foi incluído (busca por título)
python -m research.src.cli diagnose-included --title "parte do título"
```

O manifesto e os exports representam o snapshot sem distribuir o SQLite. O
arquivo de referências derivadas do pipeline é
`research/exports/references/included_papers.bib` e contém somente os 16
estudos atuais. Referências pedagógicas, metodológicas, de avaliação e
técnicas usadas na fundamentação permanecem na bibliografia completa do TCC;
são externas ao conjunto da revisão e não entram na contagem PRISMA.

Observação: os scripts antigos `tools/*.py` e `research/scripts/*.py` estão
obsoletos e serão removidos em breve. Todos os fluxos foram centralizados no CLI.

### Uso Programático

```python
from research.src.pipeline.run import SystematicReviewPipeline
from research.src.config import load_config

config = load_config()
pipeline = SystematicReviewPipeline(config)

# Pipeline completo
results = pipeline.run_full_pipeline(
    export=True,
    min_relevance_score=4.0
)

# Ou por etapas
pipeline.generate_search_queries()
pipeline.collect_data(apis=["semantic_scholar", "openalex"])
pipeline.process_data()
pipeline.apply_selection_criteria(min_relevance_score=4.5)
files = pipeline.export_results()
```

---

## 📊 Outputs Gerados

### Arquivos de Exportação

**Em `research/exports/`** (arquivos fixos, data no conteúdo):

1. **summary_report.html**: Relatório resumido com estatísticas gerais
2. **papers_report_included.html**: Lista de papers incluídos com detalhes
3. **gap_analysis.html**: Análise de lacunas de pesquisa
4. **index.html**: Índice navegável de todos os relatórios

**Em `research/exports/analysis/`**:

- `papers.xlsx`: Dados completos em Excel
- `papers.csv`: Dados em CSV
- `papers.json`: Dados em JSON

**Em `research/exports/visualizations/`**:

- `prisma_flow.png`: Diagrama de fluxo PRISMA
- `selection_funnel.png`: Funil de seleção
- `papers_by_year.png`: Distribuição temporal
- `techniques_distribution.png`: Técnicas computacionais
- `database_coverage.png`: Cobertura por API
- `relevance_distribution.png`: Distribuição de relevância

### Dados nos Papers Incluídos

Cada paper incluído registra:

- **Critérios atendidos**: year_range, language, math_focus, computational_techniques
- **Pontuação de relevância**: 0–10 (incluídos ≥ 4,0)
- **Motivo de inclusão**: Lista de critérios que qualificaram o paper
- **Fonte**: API de origem (semantic_scholar, openalex, crossref, core)
- **Metadados completos**: título, abstract, autores, ano, DOI, etc.

---

## 📄 Extração de Texto Completo

### Funcionalidade Integrada

A partir da versão atual, a extração de texto completo dos PDFs foi **integrada ao comando `export`**, eliminando a necessidade de executar comandos separados. O sistema agora oferece:

**Uso**:

```bash
# Exportar + extrair texto completo de todos os papers
python -m research.src.cli export --fetch-fulltext

# Processar apenas papers sem texto já extraído (incremental)
python -m research.src.cli export --fetch-fulltext --only-missing
```

### Estratégias de Extração

O sistema utiliza múltiplas estratégias para maximizar a taxa de sucesso:

1. **Resolvedores de PDF**:
   - IEEE Stamp URLs (papers do IEEE Xplore)
   - Unpaywall API (open access papers)
   - Crossref metadata links
   - CORE API (repositórios acadêmicos)
   - HTML scraping para publishers open access

2. **Fallbacks Inteligentes**:
   - Tentativa de múltiplos protocolos (HTTPS → HTTP)
   - Rotação de User-Agents
   - Cache de resultados para evitar reprocessamento

3. **Validação Robusta**:
   - Verificação HEAD antes do download completo
   - Detecção de content-type (PDF vs HTML)
   - Extração de texto com PyPDF2 + pdfplumber

### Informações nos Relatórios

Os relatórios HTML gerados agora incluem:

**Em `summary_report.html`**:
- Card de cobertura com percentual de extração
- Total de papers extraídos vs falhas
- Top 5 causas de falha mais frequentes

**Em `papers_report_included.html`**:
- Badge de status (✅ Extraído / ❌ Não extraído)
- Tamanho do texto extraído (em KB)
- Palavras-chave detectadas automaticamente
- Motivos de falha quando aplicável

### Taxa de Sucesso Atual

**Cobertura**: 0/16 textos completos no snapshot atual; a extração não foi concluída

**Principais Causas de Falha**:
- `connection_exhausted`: Timeout após múltiplas tentativas
- `head_error`: Erro na verificação HEAD do URL
- `ieee_no_fallback_link`: IEEE sem link de fallback disponível
- `html_no_pdf_link`: Página HTML sem link direto para PDF

### Cache e Persistência

- **Cache JSON**: `research/exports/full_texts_cache.json`
- **Banco de dados**: Campo `full_text` na tabela `papers`
- **Incremental**: Flag `--only-missing` processa apenas novos papers

---

## 🧪 Testes Automatizados

### Executar Testes

```bash
# Todos os testes
cd research && pytest

# Testes PRISMA específicos
pytest research/tests/test_prisma_stages.py -v

# Com cobertura
pytest --cov=research.src --cov-report=html
```

### Suite de Testes

**✅ test_prisma_stages.py** (9 testes da validação PRISMA):

- Critérios de inclusão/exclusão
- Fases PRISMA (screening, eligibility, inclusion)
- Consistência de estatísticas
- Registro de motivos de exclusão/inclusão

**✅ test_complete_pipeline.py**:

- Integração completa do pipeline
- Validação de APIs e coleta
- Processamento e deduplicação
- Seleção PRISMA e exportação

**✅ test_performance_benchmark.py**:

- Métricas de performance
- Cache hit rate
- Tempo de execução por fase

---

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# APIs (opcionais - funcionam sem chaves)
SEMANTIC_SCHOLAR_API_KEY=your_key
CORE_API_KEY=your_key
USER_EMAIL=your_email@domain.com

# Rate limits (segundos entre requests)
SEMANTIC_SCHOLAR_RATE_DELAY=4.0
OPENALEX_RATE_DELAY=6.0
CROSSREF_RATE_DELAY=4.0

# Critérios de revisão
REVIEW_YEAR_MIN=2015
REVIEW_YEAR_MAX=2025
REVIEW_LANGUAGES=en,pt
REVIEW_RELEVANCE_THRESHOLD=4.0  # limiar de relevância
```

### Personalizar Termos de Busca

Edite `research/src/config/search_terms.py`:

```python
# Adicionar novos termos
COMPUTATIONAL_TECHNIQUES_EN.append("new_technique")
EDUCATIONAL_CONTEXTS_PT.append("novo_contexto")

# Sistema gera automaticamente todas as combinações
```

---

## 🔧 Funcionalidades Técnicas

### Sistema de Cache Inteligente

- Cache local por query em JSON
- Speedup até 22x em execuções repetidas
- Evita sobrecarga nas APIs
- Armazenamento eficiente por fonte

### Deduplicação Avançada

**Estratégia em 3 níveis**:

1. DOI/URL idênticos (remoção direta)
2. Similaridade TF-IDF de títulos (limiar 0,9)
3. Preservação da melhor fonte (DOI > abstract completo)

### Scoring Multi-Critério

**Score 0-10 baseado em**:

- Técnicas computacionais mencionadas
- Contexto educacional matemático
- Qualidade metodológica
- Métricas de impacto (citações, H-index)

### Detecção Robusta de Idioma

**Estratégia híbrida**:

1. `langdetect` em título + abstract + keywords
2. Fallback regex para português/inglês
3. Cache de resultados para performance

### Logging Estruturado

**Único arquivo de log ativo**:

- `research/logs/ingestion.base.log`: Log consolidado de todas as operações
- Rotação automática quando atinge 10MB
- 3 backups mantidos
- Formato: `timestamp | level | module | message`

---

## 🐛 Troubleshooting

### Problemas Comuns

**Rate Limiting (HTTP 429)**:

```bash
# Aumentar delays no .env
SEMANTIC_SCHOLAR_RATE_DELAY=6.0
OPENALEX_RATE_DELAY=8.0
```

**Logs Detalhados**:

```bash
# Habilitar debug
export DEBUG=1
python -m research.src.cli run-pipeline
```

**Performance Lenta**:

- Usar cache em execuções subsequentes (automático)
- Reduzir número de queries (`--limit-per-query 50`)
- Usar apenas APIs estáveis (`--apis semantic_scholar openalex`)

---

## 📈 Métricas de Qualidade

### Performance Atual

- **Taxa de sucesso das APIs**: >95% (exceto CORE ~70%)
- **Tempo de execução**: variável; depende das APIs, limites e cache
- **Deduplicação operacional**: 0 remoções pela flag no snapshot; a auditoria encontrou 24 grupos de DOI repetido (48 linhas)
- **Taxa de inclusão final**: ~0,13% (16 de 11.904)
- **Cobertura temporal**: 2015-2026 (12 anos)
- **Cache**: contadores acumulados e dependentes do histórico; não são uma métrica fixa de reprodutibilidade

### Qualidade dos Dados

- **Papers com abstract**: 11.885/11.904 (99,8%)
- **Papers com DOI**: 10.682/11.904 (89,7%)
- **Papers com ano válido**: 11.904/11.904 (100%)
- **Reprodutibilidade**: o snapshot é representado por exports e manifesto versionados; nova coleta pode variar e as justificativas substantivas dos 7 overrides ainda requerem registro individual

---

## 🎓 Contribuição para o TCC

### Entregáveis Prontos

1. ✅ Snapshot representado por exports versionados e manifesto de reprodutibilidade (o SQLite é local e não versionado)
2. ✅ Análises estatísticas automatizadas
3. ✅ Visualizações profissionais (PNG)
4. ✅ Relatórios HTML completos
5. ✅ Pipeline reexecutável e auditável

### Metodologia Científica

- ✅ Protocolo PRISMA completo
- ✅ Transparência total (código aberto)
- ✅ Reprodutibilidade do snapshot documentada por exports e manifesto
- ✅ Auditabilidade via logs
- ✅ Rastreabilidade de cada paper

### Insights para o Protótipo

**Técnicas Mais Utilizadas**:

- Machine learning para modelagem
- Learning analytics para personalização
- Sistemas adaptativos baseados em competências
- Avaliação automatizada com feedback

**Lacunas Identificadas**:

- Integração de múltiplas técnicas
- Escalabilidade para grandes turmas
- Adaptação cultural e pedagógica
- Métricas padronizadas de avaliação

---

## 👥 Créditos

**Autor**: Thales Ferreira
**TCC - Ciência da Computação**  
**Instituição**: IFC Videira  
**Período**: 2025-2026

### 📚 Referências

- [PRISMA Guidelines](http://www.prisma-statement.org/)
- [Semantic Scholar API](https://api.semanticscholar.org/)
- [OpenAlex API](https://docs.openalex.org/)
- [Crossref API](https://github.com/CrossRef/rest-api-doc)
- [CORE API](https://core.ac.uk/docs/)

---

*📅 Última atualização: 31 de agosto de 2026*
*✅ Status: Snapshot reconciliado | Validações-alvo aprovadas | MMAT dos 16 estudos ainda pendente*
