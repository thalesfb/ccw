# 📊 Exports - Saídas da Revisão Sistemática

Este diretório reúne saídas da revisão sistemática. Os arquivos tabulares e relatórios do pipeline são regeneráveis via CLI e não devem ser editados manualmente; páginas metodológicas versionadas devem permanecer coerentes com seus ledgers de origem.

> **Snapshot reconciliado em 31/10/2026**: 11.904 registros identificados;
> 29 duplicatas removidas (27 por DOI/URL e 2 relatórios iguais confirmados
> manualmente); 11.875 registros únicos na triagem; 9.393 excluídos; 2.482
> avançaram à priorização histórica e 2.464 não avançaram sob a regra anterior.
> A emenda que retira o escore como critério de exclusão ainda não foi reaplicada.
> A seleção histórica contém 18 registros na shortlist, 17 relatórios procurados,
> 1 não recuperado, 16 avaliados em texto completo, 1 protocolo excluído e 15
> estudos empíricos. O histórico de 31/08 foi corrigido: ID 6952 é repetido do
> artigo 155 (2016), ID 6977 é a mesma tese de ID 8 (2017), e os anos de 361 e
> 7001 foram corrigidos para 2005 e 1997. Fontes e decisões estão em
> `research/data/adjudicated_record_corrections.csv`.

**Fonte vigente para MMAT:** a apreciação atual, por critério e sem score agregado,
está no [ledger atual](../data/mmat_reassessment_current.csv) e na página
[MMAT atual](analysis/mmat_current.html). Os exports gerais `analysis/papers.csv`,
`analysis/papers.json` e planilhas não são fonte de apreciação MMAT. A tabela
[legada](../data/mmat_assessments.csv) e a página [MMAT histórico](analysis/mmat_visualization.html)
foram preservadas para rastreabilidade; seus julgamentos e scores não representam
a avaliação vigente. A seleção de 15 estudos e os 18 registros da shortlist ainda são históricos até a reaplicação da emenda.

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

`included_papers.bib` contém os 18 registros shortlistados derivados do
pipeline, não 18 estudos incluídos. O núcleo empírico tem 15 estudos
provisórios; um relatório não foi recuperado, um registro foi excluído após
resumo e um protocolo foi excluído após texto completo. O
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
| Duplicatas removidas (27 DOI/URL + 2 relatórios iguais confirmados manualmente) | 29 |
| Registros avaliados na triagem | 11.875 |
| Registros na shortlist histórica | 18 (15 estudos empíricos na seleção histórica, 1 não recuperado, 1 excluído após resumo e 1 protocolo excluído) |
| Taxa de inclusão empírica provisória | 0,13% (15/11.904) |
| Período analítico configurado | 2015--2026 |
| Excluídos na triagem | 9.393 (78,91% da identificação; 79,10% dos triados) |
| Avançaram à priorização histórica | 2.482 (20,85% da identificação; 20,90% dos triados) |
| Não avançaram sob a priorização histórica | 2.464 (99,27% de 2.482) |
| Registros encaminhados à leitura de resumo | 18 (0,73% de 2.482) |
| Bases de dados | Consulte `summary.json` e `papers.csv` |

As frequências temáticas devem ser lidas do `summary.json` do mesmo snapshot;
não reutilize percentuais de rodadas históricas sem o respectivo manifesto.

---

## 🚀 Próximos Passos

### Fase 1 (Revisão Sistemática) - 🟡 RECONCILIAÇÃO DE DADOS FEITA; REAPLICAÇÃO PENDENTE
- [x] Snapshot de busca reconciliado (11.904 identificados; 29 duplicatas removidas; 11.875 únicos na triagem; 18 na seleção histórica; 15 estudos empíricos antes da reaplicação)
- [x] Fluxo histórico de triagem e texto completo reconciliado
- [ ] Reaplicar os critérios uniformes à população após a emenda aprovada de 31/10
- [x] Auditoria de títulos candidatos separada da deduplicação determinística
- [x] Exportação BibTeX dos 18 registros shortlistados do pipeline; status de elegibilidade e inclusão são mantidos separadamente no ledger
- [ ] Adjudicação dos 232 candidatos restantes apenas por título (a auditoria bruta registrou 257 excedentes, com sobreposição de identidades)
- [x] Triagem S1/S2 do MMAT em 14 e apreciação dos critérios da categoria em 11 dos 15 registros empíricos mantidos provisoriamente; estudo 8 sem respostas até adjudicação de escopo/unidade
- [ ] Obter o texto integral do registro 6923 quando houver acesso legítimo; sem aplicar MMAT a resumo ou metadados
- [ ] Adjudicar independentemente as 14 triagens, os 11 conjuntos de critérios e as três categorias pendentes do MMAT do núcleo empírico

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
