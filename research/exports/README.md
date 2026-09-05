# 📊 Exports - Saídas da Revisão Sistemática

Este diretório contém as **saídas geradas automaticamente** pelo pipeline de revisão sistemática. Todos os arquivos aqui são **gerados via CLI** e não devem ser editados manualmente.

> **População adjudicada atual (03/09/2026):** 11.904 registros identificados;
> 27 registros redundantes foram removidos deterministicamente por DOI/URL antes
> da triagem. O fluxo analítico conta 11.877 na triagem, 9.391 excluídos, 2.486
> na elegibilidade, 2.468 excluídos nessa etapa e 18 registros retidos (17
> candidatos empíricos provisórios e o protocolo contextual 6921). O registro
> 6918 foi corrigido para 2014 e excluído do recorte 2015--2026. A auditoria
> bruta encontrou 257 excedentes em
> títulos normalizados; após a remoção DOI/URL, 232 excedentes permanecem apenas
> por título como candidatos de auditoria.

---

## 📁 Estrutura de Diretórios

```
research/exports/
├── analysis/              # Análises quantitativas (CSV, JSON)
│   ├── papers_YYYYMMDD_HHMMSS.csv
│   └── papers_YYYYMMDD_HHMMSS.json
├── deep_analysis/         # Análise aprofundada via MCPs e APIs externas
│   ├── DEEP_ANALYSIS_REPORT.md
│   ├── enriched_papers_cache.json
│   └── analyses_summary.json
├── references/            # Referências bibliográficas (BibTeX)
│   ├── all_papers.bib
│   ├── included_papers.bib
│   ├── high_relevance.bib
│   └── technique_*.bib
├── reports/               # Relatórios HTML/JSON
│   ├── summary_YYYYMMDD_HHMMSS.json
│   └── summary_report_YYYYMMDD_HHMMSS.html
└── visualizations/        # Gráficos e visualizações
    ├── prisma_flow.png
    ├── temporal_trends.png
    └── citation_network.html
```

---

## 🔧 Comandos CLI

### 1. Exportação Padrão
Exporta todos os dados com relatórios e visualizações:

```bash
python -m research.src.cli export
```

**Saídas**:
- `analysis/papers_*.csv` - Dados tabulares
- `analysis/papers_*.json` - Dados estruturados
- `analysis/deduplication_identity_audit.csv` - Pares retidos/removidos por identidade DOI/URL
- `reports/summary_report_*.html` - Relatório visual
- `visualizations/*.png` - Gráficos PRISMA e temporais

Para reproduzir a população adjudicada e os relatórios a partir dos artefatos
versionados, sem SQLite, execute:

```bash
python -m research.src.processing.adjudicated_snapshot
```

### 2. Análise Aprofundada
Enriquece papers com APIs externas (Semantic Scholar) e gera análise temática:

```bash
python -m research.src.cli deep-analysis
```

**Saídas**:
- `deep_analysis/DEEP_ANALYSIS_REPORT.md` - Relatório completo
- `deep_analysis/enriched_papers_cache.json` - Cache de APIs
- `deep_analysis/analyses_summary.json` - Análises estruturadas

**Características**:
- ✅ Enriquecimento via Semantic Scholar API (TL;DR, citações, referências)
- ✅ Análise temática (técnicas computacionais, abordagens educacionais)
- ✅ Análise temporal (tendências por ano, evolução de técnicas)
- ✅ Redes de citação (papers mais citados/influentes)
- ✅ Cache JSON para reprodutibilidade

### 3. Exportação BibTeX
Gera referências bibliográficas formatadas para LaTeX:

```bash
# Todos os papers
python -m research.src.cli export-bibtex

# Apenas papers incluídos
python -m research.src.cli export-bibtex --included-only

# Diretório customizado
python -m research.src.cli export-bibtex -o research/references
```

**Saídas**:
- `references/all_papers.bib` - Todos os papers do banco
- `references/included_papers.bib` - Apenas papers incluídos (ver export gerado; contagem obtida dinamicamente do DB)
- `references/high_relevance.bib` - Score ≥ 7.0
- `references/technique_*.bib` - Organizados por técnica computacional

**Formato**:
```bibtex
@article{Machine2024_001,
  author = {Silva, J. and Costa, M.},
  title = {{Machine Learning in Mathematics Education}},
  journal = {IEEE Transactions on Learning Technologies},
  year = {2024},
  doi = {10.1109/TLT.2024.123456},
  keywords = {machine_learning, neural_network, learning_analytics},
  note = {Relevance: 8.5/10; Source: Semantic Scholar},
}
```

---

## 📚 Uso dos Arquivos BibTeX em LaTeX

### 1. Usar no projeto TCC
```bash
# Não sobrescreva a bibliografia completa do TCC.
# Consulte included_papers.bib como a bibliografia derivada do pipeline.
```

`included_papers.bib` contém somente os 18 registros retidos derivados do
pipeline (17 candidatos empíricos provisórios e o
protocolo contextual 6921). O
TCC mantém separadamente referências metodológicas, pedagógicas, de avaliação
e técnicas em `results/tcc/referencias.bib` e
`results/tcc/referencias_pedagogicas.bib`. Essa separação é deliberada e está
auditada em `research/data/reference_audit.csv`.

### 2. Usar no documento LaTeX
```latex
\documentclass{abntex2}

% No final do documento
\bibliography{referencias}
\bibliographystyle{abntex2-num}  % Ou abntex2-alf para autor-ano

% Citar no texto
De acordo com \cite{Machine2024_001}, ...
```

### 3. Compilar
```bash
cd results/tcc
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 🔄 Reprodutibilidade

### Cache de Análises
O arquivo `deep_analysis/enriched_papers_cache.json` preserva todas as respostas de APIs, permitindo:

1. **Reexecução sem chamadas de API**: Análises rápidas usando cache
2. **Auditoria**: Verificar dados originais recebidos das APIs
3. **Compartilhamento**: Enviar cache para colaboradores (evita rate limits)

### Regenerar Análises (com cache)
```bash
# Se enriched_papers_cache.json existir, será usado automaticamente
python -m research.src.cli deep-analysis
```

### Forçar Recoleta de APIs
```bash
# Remover cache para forçar novas chamadas
rm research/exports/deep_analysis/enriched_papers_cache.json
python -m research.src.cli deep-analysis
```

---

## 📊 Estatísticas Atuais

**Última exportação**: ver timestamp nos arquivos em `research/exports/analysis/`

| Métrica | Valor |
|---------|-------|
| Total de registros brutos no banco | 11.904 |
| Remoções determinísticas por DOI/URL | 27 |
| Registros avaliados na triagem | 11.877 |
| Registros retidos | 18 (17 provisoriamente empíricos + 1 contextual) |
| Taxa de inclusão | 0,15% (18/11.904) |
| Período analítico configurado | 2015--2026 |
| Excluídos na triagem | 9.391 (78,89% da identificação) |
| Avançaram à elegibilidade | 2.486 (20,88% da identificação) |
| Excluídos na elegibilidade | 2.468 (99,28% da elegibilidade) |
| Bases de dados | Consulte `summary.json` e `papers.csv` |

As frequências temáticas devem ser lidas do `summary.json` do mesmo snapshot;
não reutilize percentuais de rodadas históricas sem o respectivo manifesto.

---

## 🚀 Próximos Passos

### Fase 1 (Revisão Sistemática) - 🟡 SNAPSHOT ADJUDICADO
- [x] Snapshot atual exportado (11.904 identificados; 11.877 após deduplicação; 18 registros retidos)
- [x] Fluxo de triagem e elegibilidade reconciliado
- [x] Auditoria de títulos candidatos separada da deduplicação determinística
- [x] Exportação BibTeX dos 18 registros retidos do pipeline (17 candidatos empíricos provisórios + 1 contextual)
- [ ] Adjudicação dos 232 candidatos restantes apenas por título (a auditoria bruta registrou 257 excedentes, com sobreposição de identidades)
- [x] Reavaliação documental preliminar do MMAT aos 17 registros empíricos com evidência por critério
- [ ] Recuperação das fontes restantes e adjudicação final do MMAT aos 17 registros empíricos

### Fase 2 (Especificação conceitual do Protótipo) - ✅ REGISTRADA NO TCC
- [x] Derivar requisitos funcionais e não funcionais
- [x] Definir critérios para fontes de dados e modelos
- [x] Documentar protocolo de avaliação
- [x] Documentar arquitetura de referência
- Implementação funcional: fora do escopo do TCC vigente

### Fase 3 (Validação Experimental) - ⛔ FORA DO ESCOPO ATUAL
Esta versão não realiza validação experimental: não há coleta com participantes,
testes em ambiente escolar ou métricas próprias de eficácia, usabilidade e aceitação.

---

## 📝 Notas Importantes

### ⚠️ Não Editar Manualmente
Arquivos neste diretório são **gerados automaticamente**. Qualquer edição manual será sobrescrita na próxima execução do CLI.

### 🔒 Versionamento
Arquivos com timestamp (`papers_20251005_142319.csv`) preservam histórico de execuções. Útil para:
- Comparar resultados ao longo do tempo
- Rastrear mudanças na base de dados
- Auditoria de processo PRISMA

### 📦 Backup
Recomenda-se fazer backup periódico de:
- `deep_analysis/enriched_papers_cache.json` (≈200KB, contém dados de APIs)
- `references/*.bib` (≈45KB cada, referências formatadas)
- Últimos `analysis/papers_*.csv` (versão mais recente dos dados)

---

**Autor**: Thales Ferreira
**Orientação**: Prof. Dr. Rafael Zanin, Prof. Dr. Manassés Ribeiro
**Projeto**: Revisão Sistemática - Machine Learning em Educação Matemática
**Fase**: PTCC Fase 1 (Revisão Sistemática) ✅ CONCLUÍDA
