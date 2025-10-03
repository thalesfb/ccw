# Otimização de Planos de Ensino de Matemática

**Trabalho de Conclusão de Curso - Ciência da Computação - IFC Videira**

## Sobre o Projeto

Este repositório contém o desenvolvimento de uma ferramenta tecnológica para auxiliar professores de matemática na otimização de seus planos de ensino, através da identificação automatizada das competências individuais dos alunos.

### Tema

"Apoio à Otimização dos Planos de Ensino de Matemática por meio da identificação automatizada das competências individuais dos alunos usando técnicas computacionais."

## Orientação

- **Orientador:** Prof. Me. Rafael Zanin (IFC)
- **Coorientador:** Prof. Dr. Manassés Ribeiro (IFC)

## Objetivos

### Objetivo Geral

Desenvolver uma ferramenta tecnológica que permita ao professor diagnosticar competências individuais dos alunos e sugerindo planos de ensino adaptativos.

### Objetivos Específicos

1. Realizar revisão sistemática da literatura sobre tecnologias computacionais aplicadas à educação (learning analytics, personalização do ensino, sistemas tutores inteligentes).
2. Explorar técnicas de machine learning e análise preditiva para avaliação de desempenho em matemática.
3. Projetar e implementar um protótipo de software capaz de analisar dados de avaliação e gerar recomendações pedagógicas.
4. Validar o protótipo em ambiente experimental usando dados reais de turmas de matemática.

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
├── results/            # Phase 3: TCC artifacts (LaTeX, validation reports)
├── .gitignore          # Git exclusion patterns
├── requirements.txt    # Python dependencies
├── pytest.ini          # Test configuration
└── README.md           # Project documentation
```

## Uso do Módulo Research

O módulo `research/` implementa a revisão sistemática automatizada (Fase 1 do TCC):

### Configuração

1. Instalar dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Configurar APIs (copiar `.env.example` para `.env` e adicionar chaves):
   - Semantic Scholar API
   - OpenAlex
   - Crossref
   - CORE

### Execução

```bash
# Coletar artigos das APIs
python -m research.src.cli collect

# Ver resultados em research/exports/
ls research/exports/analysis/        # papers_*.csv, papers_*.json
ls research/exports/reports/         # summary_*.html
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

## Status do Projeto

🚧 Em desenvolvimento 🚧

## Próximos Passos

- [x] Completar protocolo de revisão sistemática
- [x] Definir bases de dados, termos de busca e critérios de inclusão/exclusão
- [x] Realizar busca nas bases de dados
- [x] Analisar e categorizar os artigos encontrados
- [ ] Investigar ferramentas semelhantes (ex: Edmodo, Google Classroom, Moodle, Khan Academy, etc.)
- [ ] Desenvolver cronograma detalhado do projeto
- [ ] Modelo de projeto em LaTeX


## Autor

Thales Ferreira - Graduando em Ciência da Computação - IFC Videira
