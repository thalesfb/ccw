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

Mapear e analisar sistematicamente as aplicações de técnicas computacionais — especialmente **machine learning**, **learning analytics** e **sistemas de tutoria inteligente** — no contexto da educação matemática, identificando tendências, lacunas de pesquisa e oportunidades para o desenvolvimento de um modelo computacional (MVP) que auxilie professores na personalização do ensino e no diagnóstico de competências.

### Objetivos Específicos

1. **OE1:** Realizar revisão sistemática da literatura seguindo o protocolo PRISMA 2020 para identificar estudos que apliquem técnicas computacionais na educação matemática (2015-2025).
2. **OE2:** Identificar e categorizar as principais abordagens de IA (Machine Learning, Deep Learning, NLP, Educational Data Mining) aplicadas à educação matemática.
3. **OE3:** Classificar as aplicações segundo suas finalidades pedagógicas: tutoria inteligente, diagnóstico, avaliação automatizada, personalização, predição e feedback adaptativo.
4. **OE4:** Analisar criticamente as metodologias de avaliação utilizadas para validar a eficácia de sistemas computacionais em contextos educacionais.
5. **OE5:** Mapear sistematicamente as lacunas de pesquisa, limitações técnicas e desafios reportados nos estudos incluídos.
6. **OE6:** Criar um pipeline automatizado e reproduzível para coleta, processamento e análise de literatura científica.

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

**Resultados PRISMA (atualizado em 27/11/2025)**:

| Etapa | Quantidade | Observação |
|-------|------------|------------|
| 📚 **Identificação** | 9.431 | 72 consultas bilíngues × 4 APIs |
| 🔄 **Duplicatas Removidas** | 2.494 | 26,4% do total |
| 🔍 **Triagem (Screening)** | 6.937 | Registros únicos avaliados |
| 📖 **Elegibilidade** | 1.883 | Taxa de exclusão: 72,8% |
| ❌ **Excluídos (Elegibilidade)** | 1.866 | Taxa de exclusão: 99,1% |
| ✅ **Incluídos** | 17 | Pontuação ≥ 4.0 |
| 📊 **Taxa de Inclusão Final** | ~0,18% | Do total identificado |

**Métricas Adicionais:**
- 🎯 **Pontuação média de relevância:** 4.2 (escala 0-5)
- ⚡ **Cache hit rate:** ~92%
- 📅 **Período coberto:** 2017–2026 (10 anos)

**Síntese Temática dos Estudos Incluídos:**
- **Abordagens Técnicas:** ML Supervisionado (76,5%), Deep Learning (11,8%), Sistemas Híbridos (5,9%), Redes Bayesianas (5,9%)
- **Finalidades Pedagógicas:** Predição (52,9%), Personalização (17,6%), Diagnóstico (11,8%), Recomendação (11,8%), Modelagem (5,9%)
- **Termos Frequentes:** Machine Learning (58,8%), Assessment (52,9%), Predictive Analytics (47,1%), Adaptive Learning (35,3%)
- **Desempenho dos Modelos:** Acurácias reportadas de 75% a 96,89%

### Fase 2: Desenvolvimento do Protótipo 🚧 EM PLANEJAMENTO

**Período:** Fevereiro–Julho 2026

- [ ] Levantamento de requisitos funcionais e não-funcionais baseado na literatura
- [ ] Definição de arquitetura de software e escolha de tecnologias
- [ ] Implementação de algoritmos de ML para diagnóstico automatizado
- [ ] Desenvolvimento de interface para professores e alunos
- [ ] Integração com bases de dados educacionais

### Fase 3: Validação Experimental 📋 PLANEJADO

**Período:** Julho–Novembro 2026

- [ ] Planejamento de estudo experimental (design, amostra, instrumentos)
- [ ] Coleta de dados em ambiente escolar controlado
- [ ] Análise quantitativa e qualitativa dos resultados
- [ ] Avaliação de eficácia, usabilidade e aceitação
- [ ] Refinamento do protótipo com base nos resultados

### Próximos Passos Imediatos

- [x] Completar protocolo de revisão sistemática
- [x] Definir bases de dados, termos de busca e critérios de inclusão/exclusão
- [x] Realizar busca nas bases de dados (72 queries bilíngues × 4 APIs)
- [x] Analisar e categorizar os artigos encontrados (17 incluídos)
- [x] Gerar relatórios e visualizações PRISMA
- [x] Finalizar documentação acadêmica do PTC (LaTeX)
- [ ] Desenvolver cronograma detalhado da Fase 2 (protótipo)
- [ ] Iniciar levantamento de requisitos para MVP

## Autor

Thales Ferreira - Graduando em Ciência da Computação - IFC Videira
