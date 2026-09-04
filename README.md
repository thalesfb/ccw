# Ensino Personalizado de Matemática: Oportunidades e Técnicas Computacionais

**Trabalho de Conclusão de Curso - Ciência da Computação - IFC Videira**

> **População vigente (03/09/2026):** o snapshot versionado contém 11.904 registros identificados, 27 remoções determinísticas por DOI/URL, 11.877 registros na triagem e 18 registros retidos após a adjudicação de escopo. São 17 candidatos empíricos provisórios e o protocolo contextual 6921. O ID 6918 foi corrigido para 2014 e excluído do recorte 2015--2026. Os números históricos de 9.431 registros e 17 incluídos permanecem apenas como contexto; a reconciliação vigente está em [`docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md`](docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md).

## Sobre o Projeto

Este repositório contém o desenvolvimento de uma ferramenta tecnológica para auxiliar professores de matemática no ensino personalizado, através da identificação automatizada das competências individuais dos alunos.

![Raio-X da Inteligência Artificial na Educação Matemática](results/ptc/presentation/ensino_personalizado_de_matematica.jpeg)

### Tema

Ensino personalizado de matemática através da identificação automatizada das competências individuais dos alunos usando técnicas computacionais.

## Orientação

- **Orientador:** Prof. Dr. Rafael Zanin (IFC)
- **Coorientador:** Prof. Dr. Manassés Ribeiro (IFC)

## Objetivos

### Objetivo Geral

Mapear e analisar sistematicamente as aplicações de técnicas computacionais — especialmente **machine learning**, **learning analytics** e **sistemas de tutoria inteligente** — no contexto da educação matemática, identificando tendências, lacunas de pesquisa e oportunidades para o desenvolvimento de um modelo computacional (MVP) que auxilie professores na personalização do ensino e no diagnóstico de competências.

### Objetivos Específicos

1. **OE1:** Realizar revisão sistemática da literatura com relato orientado pelo PRISMA 2020 para identificar estudos que apliquem técnicas computacionais na educação matemática (2015-2026).
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
│   ├── exports/        # Analysis results (CSV, JSON, HTML)
│   └── logs/           # Execution logs [gitignored]
├── src/                # Phase 2: Main product (competency diagnosis tool - future)
├── results/            # Phase 1 e 2: PTC e TCC artifacts (LaTeX, validation reports)
├── presentation/       # Fonte e build da apresentação Slidev
├── .gitignore          # Git exclusion patterns
└── README.md           # Project documentation
```

## Apresentação

A fonte está em [`presentation/slides.md`](presentation/slides.md). O workflow
compila a versão hospedável e a publica em [Abrir apresentação Slidev](https://thalesfb.github.io/ccw/presentation/), sem exigir comandos locais.

## Uso do Módulo Research

O módulo `research/` implementa a revisão sistemática automatizada seguindo PRISMA 2020.

### Configuração Inicial

#### Instalar dependências

```bash
cd research
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Inicializar banco de dados:

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
- `research/exports/reports/reproducibility_manifest.json` - Manifesto versionado do snapshot, decisões de auditoria e hashes
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

- `research/exports/references/included_papers.bib` - Registros bibliográficos derivados do snapshot vigente (18; 17 candidatos empíricos provisórios + 1 protocolo contextual)
- `research/exports/references/high_relevance.bib` - Score ≥ 7.0
- `research/exports/references/technique_*.bib` - Por técnica computacional

O arquivo `included_papers.bib` contém somente os 18 registros derivados do
pipeline. O protocolo 6921 é mantido para rastreabilidade, mas não sustenta
afirmações empíricas. As referências de fundamentação pedagógica, avaliação,
metodologia e técnica são mantidas separadamente na bibliografia completa do
TCC e não alteram a contagem de estudos incluídos.

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

---

## 🛠️ Scripts do Repositório

### Scripts Ativos (Uso Recomendado)

- **`research/src/cli.py`**: Interface CLI oficial para todas operações do pipeline
  - Uso: `python -m research.src.cli [comando] [opções]`
  - Comandos principais: `init-db`, `run-pipeline`, `stats`, `export`, `export-bibtex`, `generate-manifest`, `normalize-prisma`, `validate-exports`, `check-exports`
  - `audit` é legado e depende de um módulo ausente; sua correção deve ser tratada em PR atômico separado
- **`research/src/pipeline/`**: Módulos do pipeline de revisão sistemática
- **`research/src/database/`**: Gerenciamento de banco SQLite
- **`research/tests/`**: Testes automatizados (pytest)

---

## Status do Projeto

### Fase 1: Revisão Sistemática — baseline reconciliado; MMAT preliminar registrado

**População vigente após adjudicação (03/09/2026):**

| Etapa | Quantidade | Interpretação |
|-------|------------|---------------|
| Identificação | 11.904 | Registros identificados no snapshot versionado |
| Deduplicação | 27 removidos | 25 excedentes por DOI + 2 por URL exata (um grupo misto quanto ao DOI) |
| Triagem | 11.877 → 2.486 | 9.391 excluídos na triagem |
| Elegibilidade | 2.486 → 18 | 2.468 excluídos na elegibilidade |
| Auditoria de candidatos | 23 → 18 | 8 decisões de escopo aprovadas; 3 recuperados, 1 excluído por período e 4 mantidos fora |
| Retidos | **18** | 17 candidatos empíricos provisórios + 1 protocolo contextual |

Os sete overrides manuais e a correção temporal do ID 6918 estão registrados
na população adjudicada. Quatro overrides permaneceram excluídos por escopo,
enquanto três foram recuperados; a mudança envolveu também a correção do ano
bibliográfico, a composição do conjunto e a separação entre síntese empírica e
contextual. Não se trata de trocar apenas um número. A fonte de verdade e as
ressalvas sobre DOI e MMAT estão em
[`docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md`](docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md).

O SQLite é um artefato operacional local e permanece ignorado pelo Git. A
reconstituição auditável do snapshot é feita pelos exports versionados, pelo
ledger de decisões, pela bibliografia dos 18 registros retidos e pelo manifesto
de reprodutibilidade; uma nova coleta nas APIs pode produzir metadados
diferentes.

O detalhamento da transição entre a baseline anterior e a população vigente
está em [`docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md`](docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md). O documento
`docs/RECONCILIACAO-BASELINE-2026-08-31.md` permanece como registro histórico
da baseline operacional anterior.

**Baseline histórico (documento de 27/11/2025; não vigente)**:

> O arquivo legado de 6.914 linhas já era uma saída pós-consolidação. Os
> 2.517 registros foram obtidos pela diferença aritmética `9.431 - 6.914`,
> mas o ledger dos pares removidos não foi preservado; o resumo histórico do
> SQLite registra 2.494. Portanto, esses números são contexto histórico não
> reproduzível independentemente, e não devem ser misturados com as 27
> identidades DOI/URL auditadas no snapshot atual.

| Etapa | Quantidade | Observação |
|-------|------------|------------|
| 📚 **Identificação** | 9.431 | 72 consultas bilíngues × 4 APIs |
| 🔄 **Duplicatas Removidas** | 2.517 | 26,6% do total |
| 🔍 **Triagem (Screening)** | 6.914 | Registros únicos avaliados |
| 📖 **Elegibilidade** | 1.883 | Taxa de exclusão: 72,8% |
| ❌ **Excluídos (Elegibilidade)** | 1.866 | Taxa de exclusão: 99,1% |
| ✅ **Incluídos** | 17 | Pontuação ≥ 4.0 |
| 📊 **Taxa de Inclusão Final** | ~0,18% | Do total identificado |

**Métricas Adicionais do baseline histórico:**

- 🎯 **Pontuação média de relevância:** 4,2 (intervalo: 4,0–4,5)
- ⚡ **Cache hit rate:** ~92%
- 📅 **Período coberto:** 2015–2025 (11 anos)

**Síntese Temática do baseline histórico:**

- **Abordagens Técnicas:** ML Supervisionado (76,5%), Deep Learning (11,8%), Sistemas Híbridos (5,9%), Redes Bayesianas (5,9%)
- **Finalidades Pedagógicas:** Predição (52,9%), Personalização (17,6%), Diagnóstico (11,8%), Recomendação (11,8%), Modelagem (5,9%)
- **Termos Frequentes:** Machine Learning (58,8%), Assessment (52,9%), Predictive Analytics (47,1%), Adaptive Learning (35,3%)
- **Desempenho dos Modelos:** Acurácias reportadas de 75% a 96,89%

### Fase 2: Desenvolvimento do Protótipo 📋 AGUARDANDO DEFINIÇÃO

**Período:** não há prazo vigente no snapshot de 31/08/2026; o intervalo
Fevereiro–Julho de 2026 pertence ao planejamento histórico.

- [ ] Levantamento de requisitos funcionais e não-funcionais baseado na literatura
- [ ] Definição de arquitetura de software e escolha de tecnologias
- [ ] Implementação de algoritmos de ML para diagnóstico automatizado
- [ ] Desenvolvimento de interface para professores e alunos
- [ ] Integração com bases de dados educacionais

### Fase 3: Validação Experimental 📋 AGUARDANDO DEFINIÇÃO

**Período:** não há prazo vigente no snapshot de 31/08/2026; o intervalo
Julho–Novembro de 2026 pertence ao planejamento histórico.

- [ ] Planejamento de estudo experimental (design, amostra, instrumentos)
- [ ] Coleta de dados em ambiente escolar controlado
- [ ] Análise quantitativa e qualitativa dos resultados
- [ ] Avaliação de eficácia, usabilidade e aceitação
- [ ] Refinamento do protótipo com base nos resultados

### Próximos Passos Imediatos

- [x] Completar protocolo de revisão sistemática
- [x] Definir bases de dados, termos de busca e critérios de inclusão/exclusão
- [x] Realizar busca nas bases de dados (72 queries bilíngues × 4 APIs)
- [x] Analisar e categorizar os artigos encontrados (18 registros retidos no snapshot vigente; 17 estudos no baseline histórico)
- [x] Gerar relatórios e visualizações PRISMA
- [x] Finalizar documentação acadêmica do PTC (LaTeX)
- [ ] Definir, com a orientação, o cenário científico de continuidade
- [ ] Desenvolver cronograma da Fase 2 somente após essa decisão

## Autor

Thales Ferreira - Graduando em Ciência da Computação - IFC Videira
