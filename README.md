# Ensino Personalizado de Matemática: Oportunidades e Técnicas Computacionais

**Trabalho de Conclusão de Curso - Ciência da Computação - IFC Videira**

## Sobre o Projeto

Este repositório contém o desenvolvimento de uma ferramenta tecnológica para auxiliar professores de matemática no ensino personalizado, através da identificação automatizada das competências individuais dos alunos.

### Tema

Ensino personalizado de matemática através da identificação automatizada das competências individuais dos alunos usando técnicas computacionais.

## Orientação

- **Orientador:** Prof. Dr. Rafael Zanin (IFC)
- **Coorientador:** Prof. Dr. Manassés Ribeiro (IFC)

## Objetivos

### Objetivo Geral

Desenvolver uma ferramenta tecnológica que permita ao professor um acompanhamento individualizado dos alunos através de um ensino personalizado.

### Objetivos Específicos

1. Realizar revisão sistemática da literatura sobre tecnologias computacionais aplicadas à educação (learning analytics, personalização do ensino, sistemas tutores inteligentes).
2. Explorar técnicas de machine learning e análise preditiva para avaliação de desempenho em matemática.
3. Projetar e implementar um protótipo de software para uso em ambiente educacional.

## Estrutura do Repositório

```bash
├── .github/            # Copilot workflow guidelines and prompts
├── docs/               # Academic documentation (constitution, regulations)
├── research/           # Phase 1: Systematic literature review module
│   ├── src/            # Pipeline modules (ingestion, processing, analysis)
│   ├── tests/          # Test suite (integration, performance, quality)
│   ├── docs/           # Module documentation (methodology, theory)
│   ├── references/     # BibTeX academic references
│   ├── papers/         # Downloaded PDFs
│   ├── cache/          # API response cache (SQLite)
│   ├── exports/        # Analysis results (CSV, JSON, HTML) [gitignored]
│   └── logs/           # Execution logs [gitignored]
├── src/                # Phase 2: Main product (competency diagnosis tool - future)
├── results/            # Phase 1 e 2: PTC e TCC artifacts (LaTeX, validation reports)
├── .gitignore          # Git exclusion patterns
└── README.md           # Project documentation
```

## Uso do Módulo Research

O módulo `research/` implementa a revisão sistemática automatizada seguindo PRISMA 2020.

### Configuração Inicial

1. Instalar dependências:

```bash
cd research
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Inicializar banco de dados:

```bash
python -m research.src.cli init-db
```

### Comandos Disponíveis

#### 1. Pipeline Completo
Executa revisão sistemática completa (busca → screening → seleção):

```bash
python -m research.src.cli run-pipeline --min-score 4.0
```

#### 2. Estatísticas
Visualiza métricas do banco de dados:

```bash
python -m research.src.cli stats
```

#### 3. Exportação Padrão
Gera relatórios HTML, CSV, JSON e visualizações:

```bash
python -m research.src.cli export
```

**Saídas**:
- `research/exports/analysis/papers.csv` - Dados tabulares
- `research/exports/reports/summary_report.html` - Relatório visual
- `research/exports/visualizations/*.png` - Gráficos PRISMA

#### 4. Exportação BibTeX (✨)

Gera referências bibliográficas formatadas para LaTeX:

```bash
# Apenas papers incluídos
python -m research.src.cli export-bibtex --included-only

# Todos os papers do banco
python -m research.src.cli export-bibtex
```

**Saídas**:

- `research/exports/references/included_papers.bib` - Papers incluídos (16)
- `research/exports/references/high_relevance.bib` - Score ≥ 7.0
- `research/exports/references/technique_*.bib` - Por técnica computacional

**Uso em LaTeX**:

```latex
\bibliography{included_papers}
\bibliographystyle{abntex2-num}
```

### Testes

```bash
# Executar suite completa
pytest research/tests/

# Testes específicos
pytest research/tests/test_complete_pipeline.py
pytest research/tests/test_performance_benchmark.py
```

Para detalhes sobre metodologia PRISMA e arquitetura do pipeline, consulte:

- `research/README.md` - Guia de uso detalhado
- `research/docs/METODOLOGIA.md` - Implementação PRISMA
- `research/docs/FUNDAMENTACAO_TEORICA.md` - Base teórica
- `docs/CONSTITUTION.md` - Governança do projeto

---

## 🛠️ Scripts do Repositório

### Scripts Ativos (Uso Recomendado)

- **`research/src/cli.py`**: Interface CLI oficial para todas operações do pipeline
  - Uso: `python -m research.src.cli [comando] [opções]`
  - Comandos principais: `init-db`, `run-pipeline`, `stats`, `export`, `export-bibtex`, `normalize-prisma`, `audit`, `validate-exports`
- **`research/src/pipeline/`**: Módulos do pipeline de revisão sistemática
- **`research/src/database/`**: Gerenciamento de banco SQLite
- **`research/tests/`**: Testes automatizados (pytest)

---

## Status do Projeto

### Fase 1: Revisão Sistemática ✅ COMPLETA

**Resultados PRISMA (atualizado em 25/11/2025)**:

- 📚 **Identificação**: 9.431 registros coletados (72 queries bilíngües × 4 APIs)
- 🔍 **Triagem (Screening)**: 6.937 estudos únicos avaliados (duplicatas removidas: 2.494 / 26,4%)
- 📖 **Elegibilidade**: 1.883 avaliados em profundidade (excluídos na elegibilidade: 1.866 / 99,1%)
- ✅ **Incluídos**: 17 estudos (relevance_score ≥4.0)
- 📊 **Taxa de inclusão final**: ~0,18% do total identificado

### Próximos Passos

- [x] Completar protocolo de revisão sistemática
- [x] Definir bases de dados, termos de busca e critérios de inclusão/exclusão
- [x] Realizar busca nas bases de dados (72 queries bilíngües × 4 APIs)
- [x] Analisar e categorizar os artigos encontrados (17 incluídos)
- [x] Gerar relatórios e visualizações PRISMA
- [ ] Desenvolver cronograma detalhado da Fase 2 (protótipo)
- [ ] Finalizar documentação acadêmica (LaTeX)

## Autor

Thales Ferreira - Graduando em Ciência da Computação - IFC Videira
