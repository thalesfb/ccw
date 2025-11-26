# 📊 Exports - Saídas da Revisão Sistemática

Este diretório contém as **saídas geradas automaticamente** pelo pipeline de revisão sistemática. Todos os arquivos aqui são **gerados via CLI** e não devem ser editados manualmente.

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
- `reports/summary_report_*.html` - Relatório visual
- `visualizations/*.png` - Gráficos PRISMA e temporais

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

### 1. Copiar para o projeto TCC
```bash
cp research/exports/references/included_papers.bib results/tcc/referencias.bib
```

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
| Total de papers no banco | (see `research/systematic_review.db`) |
| Papers incluídos | (see `research/exports/reports/summary_report_*.html`) |
| Taxa de inclusão | (computed at export time) |
| Período | 2015-2025 |
| Média de citações | (see `research/exports/analysis/papers_*.csv`) |
| Bases de dados | (see `research/exports/analysis/papers_*.csv`) |

**Top 3 Técnicas**:
1. Machine Learning + Neural Networks + Learning Analytics (32,6%)
2. ML + LA + Statistical + Tree-based (18,6%)
3. LA + Statistical + Tree + NN + ML (16,3%)

---

## 🚀 Próximos Passos

### Fase 1 (Revisão Sistemática) - ✅ COMPLETA
- [x] Coleta de dados (12.533 papers)
- [x] Screening e eligibility (PRISMA 2020)
- [x] Seleção final (43 papers)
- [x] Análise aprofundada via APIs
- [x] Exportação BibTeX

### Fase 2 (Desenvolvimento do Protótipo) - 📋 PLANEJADA
- [ ] Definir arquitetura (ML + LA + XAI)
- [ ] Selecionar datasets (públicos ou IFC)
- [ ] Implementar modelo preditivo
- [ ] Dashboard para professores
- [ ] Testes de usabilidade

### Fase 3 (Validação Experimental) - 📋 PLANEJADA
- [ ] Protocolo quasi-experimental
- [ ] Coleta de dados (turmas IFC)
- [ ] Análise estatística (pré/pós-teste)
- [ ] Entrevistas qualitativas
- [ ] Relatório final

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
