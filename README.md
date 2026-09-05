# Ensino Personalizado de Matemática: Oportunidades e Técnicas Computacionais

**Trabalho de Conclusão de Curso - Ciência da Computação - IFC Videira**

> **População vigente (03/09/2026):** o snapshot versionado contém 11.904 registros identificados, 27 remoções determinísticas por DOI/URL, 11.877 registros na triagem e 18 registros retidos após a adjudicação de escopo. São 17 candidatos empíricos provisórios e o protocolo contextual 6921. O ID 6918 foi corrigido para 2014 e excluído do recorte 2015--2026. Os números históricos de 9.431 registros e 17 incluídos permanecem apenas como contexto; a reconciliação vigente está em [`docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md`](docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md).

## Sobre o Projeto

Este repositório documenta uma revisão sistemática da literatura e a elaboração de uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente de evidências sobre competências matemáticas. A especificação não corresponde a uma aplicação funcional nem a uma validação experimental realizada neste trabalho.

![Fluxo PRISMA do snapshot adjudicado](research/exports/visualizations/prisma_flow.png)

### Tema

Aplicações de técnicas computacionais no ensino de matemática e elaboração de uma especificação conceitual de apoio à interpretação docente.

## Orientação

- **Orientador:** Prof. Dr. Rafael Zanin (IFC)
- **Coorientador:** Prof. Dr. Manassés Ribeiro (IFC)

## Objetivos

### Objetivo Geral

Mapear e analisar sistematicamente as aplicações de técnicas computacionais no ensino de matemática e, a partir das evidências encontradas, elaborar uma especificação técnica e pedagógica de protótipo para apoio à interpretação de evidências sobre competências.

### Objetivos Específicos

1. **OE1:** Realizar uma revisão sistemática da literatura, com relato apoiado pelo PRISMA 2020, sobre estudos publicados entre 2015 e 2026.
2. **OE2:** Identificar e categorizar as principais abordagens computacionais aplicadas ao ensino de matemática.
3. **OE3:** Classificar as finalidades pedagógicas atribuídas às aplicações encontradas.
4. **OE4:** Analisar criticamente as metodologias e limitações dos estudos incluídos.
5. **OE5:** Mapear lacunas técnicas, pedagógicas, metodológicas e éticas.
6. **OE6:** Manter um pipeline automatizado e auditável para coleta, processamento e exportação da revisão.
7. **OE7:** Derivar requisitos funcionais e não funcionais, critérios de seleção de dados e modelos, um protocolo de avaliação e uma arquitetura de referência para o protótipo.

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
├── src/                # Protótipo futuro; não implementado no TCC vigente
├── results/            # Artefatos do PTC histórico e do TCC vigente
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

### Fase 1: Revisão Sistemática — snapshot adjudicado; MMAT preliminar registrado

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

### Fase 2: Especificação conceitual do protótipo — concluída no escopo do TCC

O TCC vigente produziu uma especificação conceitual baseada na revisão e na
fundamentação pedagógica. Foram consolidados requisitos, critérios para dados
e modelos, um protocolo de avaliação e uma arquitetura de referência. Não foi
desenvolvida uma aplicação funcional nem treinado um modelo definitivo.

### Fase 3: Validação experimental — fora do escopo atual

Esta versão do trabalho não realiza validação experimental. Não foram coletados
dados com participantes, conduzidos testes em ambiente escolar ou produzidas
métricas próprias de eficácia, usabilidade ou aceitação.

### Próximos Passos Imediatos

- [x] Completar protocolo de revisão sistemática
- [x] Definir bases de dados, termos de busca e critérios de inclusão/exclusão
- [x] Definir e versionar a estratégia canônica de busca (72 consultas bilíngues × 4 APIs)
- [x] Consolidar o snapshot versionado da busca (11.904 registros identificados)
- [x] Analisar e categorizar os artigos encontrados (18 registros retidos no snapshot vigente; 17 candidatos empíricos provisórios e 1 protocolo contextual)
- [x] Gerar relatórios e visualizações PRISMA
- [x] Finalizar documentação acadêmica do PTC (LaTeX)
- [ ] Concluir a recuperação de fontes, os localizadores e a adjudicação metodológica do MMAT
- [ ] Realizar a revisão final do TCC com a orientação
- [ ] Registrar eventuais trabalhos futuros separadamente, sem tratá-los como resultados do TCC vigente

## Autor

Thales Ferreira - Graduando em Ciência da Computação - IFC Videira
