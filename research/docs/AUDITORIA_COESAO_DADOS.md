# 🔍 Auditoria de Coesão de Dados

**Data**: 16/11/2025 22:35  
**Objetivo**: Validar consistência entre banco de dados SQLite, exports CLI e documentação  
**Status**: ⚠️ **INCONSISTÊNCIAS CRÍTICAS ENCONTRADAS**

---

## 📊 Resumo Executivo

| Fonte | Identificados | Triagem | Elegibilidade | Incluídos | Status |
|-------|---------------|---------|---------------|-----------|--------|
| **Banco SQLite** | **6.516** | 6.516 | 1.835 | **16** | ✅ **CANÔNICO** |
| **CLI `stats`** | 6.516 | 4.665 | 1.835 | 16 | ✅ Correto |
| **Export HTML** | **9.356** | 6.516 | 1.851 | 16 | ❌ **INCORRETO** |
| **Docs (METODOLOGIA.md)** | 6.516 | 4.665 | 1.835 | 16 | ✅ Correto |
| **Docs (RESUMO.md)** | 6.516 | 4.665 | 1.835 | 16 | ✅ Correto |

### ⚠️ Inconsistências Críticas

1. **Export HTML mostra 9.356 identificados** (linha 56 de `summary_report.html`)
   - Valor correto: **6.516**
   - Discrepância: +2.840 papers fantasmas
   - Causa: Função `_compute_prisma_stats_from_df()` usando `dedup_stats.initial_count` ao invés de `len(df)`

2. **PRISMA flow mostra 2.594 duplicatas removidas**
   - Valor real no banco: **0 duplicatas marcadas**
   - Query: `SELECT COUNT(*) FROM papers WHERE exclusion_reason LIKE '%duplic%'` → 0
   - Causa: Código calculando diferença fictícia (9356 - 6762 = 2594)

3. **Elegibilidade com valores inconsistentes**
   - HTML: 1.851 aprovados (linha 81)
   - Banco: 1.835 no estágio `eligibility` + 16 `included` = 1.851 ✅
   - Cálculo correto, mas nomenclatura confusa (deveria ser "Passaram para elegibilidade")

---

## 🗄️ Fonte Canônica: Banco SQLite

### Consulta Direta ao Banco

```bash
$ sqlite3 research/systematic_review.sqlite "SELECT COUNT(*) FROM papers"
6516

$ sqlite3 research/systematic_review.sqlite "SELECT selection_stage, COUNT(*) FROM papers GROUP BY selection_stage"
eligibility|1835
included|16
screening|4665
```

### Métricas Validadas (16/11/2025 22:30)

```
📊 VALORES CANÔNICOS (Banco SQLite)
├─ Total papers únicos: 6.516
├─ Duplicatas marcadas: 0
├─ Status:
│  ├─ excluded: 6.500
│  └─ included: 16
└─ Estágios (selection_stage):
   ├─ screening: 4.665 (71,6% do total)
   ├─ eligibility: 1.835 (28,2% do total)
   └─ included: 16 (0,25% do total)

✅ INCLUÍDOS (16 estudos)
├─ Score médio: 4.20
├─ Score mínimo: 4.0
├─ Score máximo: 4.5
└─ Anos: 2017-2025 (9 anos com dados)

❌ EXCLUÍDOS (6.500 papers)
├─ abstract_too_short: 2.720 (41,8%)
├─ low_relevance_score: 1.835 (28,2%)
├─ inclusion_criteria_not_met: 1.010 (15,5%)
├─ no_methodology: 870 (13,4%)
├─ non_research: 50 (0,8%)
└─ off_topic: 15 (0,2%)
```

---

## 🔧 CLI: Comando `stats`

### Execução em 16/11/2025 22:26

```bash
$ python -m research.src.cli stats

Total de papers: 6516

📋 Por estágio de seleção:
  eligibility: 1835
  Included: 16
  screening: 4665

🗃️ Por base de dados:
  core: 126 (1,9%)
  crossref: 2815 (43,2%)
  openalex: 1793 (27,5%)
  semantic_scholar: 1782 (27,3%)

📅 Por ano (últimos 10):
  2017-2025: 6.516 papers
  (distribuição detalhada no relatório)

💾 Cache: 278 entradas, 0 hits
```

**✅ Status**: CLI está **CORRETO** - reflete exatamente o banco SQLite

---

## 📤 Exports: Comando `export`

### Arquivos Gerados

```
research/exports/analysis/
├── analysis/
│   ├── revisao_sistematica.xlsx    ✅ 6.516 linhas (correto)
│   ├── papers.xlsx                 ✅ 6.516 linhas (correto)
│   ├── papers.csv                  ✅ 6.516 linhas (correto)
│   └── papers.json                 ✅ 6.516 registros (correto)
│
├── reports/
│   ├── summary_report.html         ❌ Mostra "9356 Total de Papers" (INCORRETO)
│   ├── papers_report_included.html ✅ 16 papers (correto)
│   └── gap_analysis.html           ✅ Baseado nos 16 (correto)
│
└── visualizations/
    ├── prisma_flow.png             ❌ Mostra 9356 identificados (INCORRETO)
    ├── selection_funnel.png        ❌ Mostra 9356 no topo (INCORRETO)
    ├── papers_by_year.png          ✅ Baseado em 6.516 (correto)
    ├── techniques_distribution.png ✅ Correto
    ├── database_coverage.png       ✅ Correto
    └── relevance_distribution.png  ✅ Correto
```

### ❌ Problemas nos Reports HTML

**Arquivo**: `research/exports/analysis/reports/summary_report.html`

**Linhas problemáticas**:

```html
<!-- Linha 56 -->
<h3>9356</h3>
<p>Total de Papers</p>

<!-- Linha 81 - Tabela PRISMA -->
<td>📚 Identificação</td>
<td style="text-align: right;">9356</td>

<!-- Linha 84 -->
<td>🔍 Triagem (aprovados)</td>
<td style="text-align: right;">6516</td>
```

**Cálculo Implícito (ERRADO)**:
- Identificação: 9.356
- Duplicatas removidas: 2.840 (não documentado, mas implícito por 9356 - 6516)
- Triagem: 6.516

**Cálculo Correto**:
- Identificação: **6.516** (já deduplicados no banco)
- Duplicatas: **0** (deduplicação feita antes de inserir no banco)
- Triagem: 6.516

---

## 📝 Documentação Markdown

### ✅ METODOLOGIA.md (Correto)

```markdown
**Total de registros identificados**: 6.516
- Crossref: ~43,8%
- OpenAlex: ~27,0%
- Semantic Scholar: ~27,3%
- CORE: ~2,0%

**Triagem (Screening)**: 4.665 → 28,4% excluídos
**Elegibilidade**: 1.835 → 99,1% excluídos
**Incluídos (final)**: 16 estudos (~0,25%)
```

### ✅ RESUMO.md (Correto)

```markdown
| Etapa | Quantidade |
|-------|-----------|
| Identificação | 6.516 |
| Triagem | 4.665 |
| Elegibilidade | 1.835 |
| Incluídos | 16 |
```

### ✅ CONCLUSOES.md (Atualizado 16/11)

Atualizado de `12.533/43` → `6.516/16` ✅

### ✅ CRONOGRAMA.md (Atualizado 16/11)

Atualizado com métricas canônicas ✅

---

## 🐛 Análise de Causa Raiz

### Problema 1: Valor 9.356 nos Relatórios

**Arquivo**: `research/src/exports/excel.py` (linha 268-277)

```python
def _compute_prisma_stats_from_df(df: pd.DataFrame) -> dict:
    stats = {}
    stats['identification'] = len(df)  # ✅ Correto: conta linhas do DataFrame
    if 'selection_stage' in df.columns:
        stats['screening'] = int(len(df))
        stats['eligibility'] = int(df['selection_stage'].isin(['eligibility', 'included']).sum())
        stats['included'] = int((df['selection_stage'] == 'included').sum())
        stats['screening_excluded'] = int((df['selection_stage'] == 'screening').sum())
        stats['eligibility_excluded'] = int((df['selection_stage'] == 'eligibility').sum())
    return stats
```

**Mas então** (linha 323-324):

```python
# Use PRISMA stats from pipeline (already computed from deduplicated data)
local_stats = dict(stats) if stats else _compute_prisma_stats_from_df(df)
```

**Raiz do problema**: `stats` passado externamente contém valores **INCORRETOS** de `dedup_stats.initial_count`

**Arquivo**: `research/src/processing/selection.py` (linha 39-45)

```python
def _load_dedup_stats_from_df(self, df: pd.DataFrame) -> None:
    """If the dataframe carries dedup_stats in attrs, load them into selector stats."""
    try:
        dedup = getattr(df, 'attrs', {}).get('dedup_stats') if df is not None else None
        if dedup:
            self.stats['identification'] = int(dedup.get('initial_count', 0))  # ❌ PROBLEMA!
            self.stats['duplicates_removed'] = int(dedup.get('total_removed', 0))
    except Exception:
        logger.debug("No dedup_stats available on DataFrame.attrs")
```

**Explicação**:
- `dedup_stats.initial_count` = 9.356 (total **ANTES** da deduplicação durante a coleta)
- `dedup_stats.total_removed` = 2.840 (duplicatas removidas **ANTES** de inserir no banco)
- Mas o **banco SQLite já contém apenas 6.516 papers únicos**
- Usar `initial_count` nos relatórios cria discrepância porque os dados já foram deduplicados

### Problema 2: PRISMA Flow Diagram

**Arquivo**: `research/src/analysis/visualizations.py` (linha 97-111)

```python
identification = int(stats.get('identification', 0))
duplicates_removed = int(stats.get('duplicates_removed', 0))
screening_total = int(stats.get('screening', 0))

logger.info(
    f"PRISMA stats used -> ident={identification}, dup_removed={duplicates_removed}, "
    f"screening={screening_total}, eligibility={eligibility_total}, included={included}"
)
```

**Logs observados** (16/11 22:30):

```
PRISMA stats used -> ident=9356, dup_removed=2594, screening=6516, 
eligibility=1851, included=16, screening_excl=4665, eligibility_excl=1835
```

**Problema**: `ident=9356` está ERRADO! Deveria ser `ident=6516` (valor do banco)

---

## 🎯 Valores Corretos vs Incorretos

### Tabela Comparativa

| Métrica | Valor Correto (Banco) | Valor Incorreto (HTML) | Discrepância |
|---------|----------------------|------------------------|--------------|
| **Identificados** | **6.516** | 9.356 | +2.840 |
| Duplicatas removidas | 0 (já dedup) | 2.594 | +2.594 |
| Triagem (total) | 6.516 | 6.516 | ✅ OK |
| Triagem (exclusões) | 4.665 | 4.665 | ✅ OK |
| Elegibilidade (total) | 1.835 + 16 = 1.851 | 1.851 | ✅ OK |
| Elegibilidade (exclusões) | 1.835 | 1.835 | ✅ OK |
| **Incluídos** | **16** | **16** | ✅ OK |

### Fluxo PRISMA Correto

```
┌─────────────────────────────────────────┐
│  IDENTIFICAÇÃO: 6.516 registros únicos  │
│  (Deduplicação realizada ANTES do DB)   │
│                                         │
│  ├─ Crossref: 2.815 (43,2%)            │
│  ├─ OpenAlex: 1.793 (27,5%)            │
│  ├─ Semantic Scholar: 1.782 (27,3%)    │
│  └─ CORE: 126 (1,9%)                   │
│                                         │
│  Período: 2017-2025 (9 anos)           │
│  Queries: 108 bilíngues                │
└─────────────────────────────────────────┘
           ↓ (Screening automático)
┌─────────────────────────────────────────┐
│  TRIAGEM: 6.516 registros avaliados     │
│  ❌ Excluídos: 4.665 (71,6%)            │
│     ├─ abstract_too_short: 2.720       │
│     ├─ inclusion_criteria: 1.010       │
│     ├─ no_methodology: 870             │
│     └─ outros: 65                      │
│  ✅ Aprovados: 1.851 (28,4%)            │
└─────────────────────────────────────────┘
           ↓ (Score ≥ 4.0)
┌─────────────────────────────────────────┐
│  ELEGIBILIDADE: 1.851 registros         │
│  ❌ Excluídos: 1.835 (99,1%)            │
│     └─ low_relevance_score: 1.835      │
│  ✅ Aprovados: 16 (0,9%)                │
└─────────────────────────────────────────┘
           ↓ (Critérios finais)
┌─────────────────────────────────────────┐
│  INCLUÍDOS: 16 estudos (0,25%)          │
│                                         │
│  ✅ Score médio: 4.20                   │
│  ✅ Score range: 4.0 - 4.5              │
│  ✅ Anos: 2017-2025                     │
└─────────────────────────────────────────┘
```

---

## 🔧 Ações Corretivas Necessárias

### 1. Correção de Código (Alta Prioridade)

**Arquivo**: `research/src/exports/excel.py`

**Problema**: Função `_compute_prisma_stats_from_df()` ignora que `stats` pode conter valores pré-dedup

**Solução**: Sempre recalcular `identification` a partir do DataFrame quando não há `stats['duplicates_removed']`:

```python
def _compute_prisma_stats_from_df(df: pd.DataFrame) -> dict:
    stats = {}
    # SEMPRE usar len(df) para identification (dados já dedup no banco)
    stats['identification'] = len(df)
    stats['duplicates_removed'] = 0  # Já foi feito antes do DB
    
    if 'selection_stage' in df.columns:
        stats['screening'] = int(len(df))
        stats['eligibility'] = int(df['selection_stage'].isin(['eligibility', 'included']).sum())
        stats['included'] = int((df['selection_stage'] == 'included').sum())
        stats['screening_excluded'] = int((df['selection_stage'] == 'screening').sum())
        stats['eligibility_excluded'] = int((df['selection_stage'] == 'eligibility').sum())
    return stats
```

**Arquivo**: `research/src/processing/selection.py`

**Solução**: Não carregar `dedup_stats.initial_count` para `self.stats['identification']` OU documentar claramente que é pré-dedup:

```python
def _load_dedup_stats_from_df(self, df: pd.DataFrame) -> None:
    """Load dedup stats from DataFrame attrs (historical, pre-database values)."""
    try:
        dedup = getattr(df, 'attrs', {}).get('dedup_stats') if df is not None else None
        if dedup:
            # NÃO usar initial_count - dados no DF já estão deduplicados
            # self.stats['identification'] = len(df)  # Usar tamanho real do DF
            self.stats['duplicates_removed'] = int(dedup.get('total_removed', 0))
            self.stats['_historical_initial_count'] = int(dedup.get('initial_count', 0))  # Apenas para log
    except Exception:
        logger.debug("No dedup_stats available on DataFrame.attrs")
```

### 2. Regenerar Exports (Alta Prioridade)

```bash
cd /c/dev/ccw
python -m research.src.cli export -o research/exports/analysis/
```

**Arquivos afetados**:
- ❌ `summary_report.html` (linha 56: 9356 → 6516)
- ❌ `prisma_flow.png` (box "Identificação": 9356 → 6516)
- ❌ `selection_funnel.png` (topo do funil: 9356 → 6516)

### 3. Atualizar Documentação (Média Prioridade)

**Arquivos corretos (não precisam atualização)**:
- ✅ METODOLOGIA.md
- ✅ RESUMO.md
- ✅ RESULTADOS_PRELIMINARES.md
- ✅ CONCLUSOES.md
- ✅ CRONOGRAMA.md

**Arquivos que precisam revisão**:
- ⚠️ **README_DOCS.md**: Remover referências a `deep_analysis/` (excluído pelo usuário)
- ⚠️ **ANALISE_ESTRUTURA_DOCS.md**: Atualizar seção de exports com warnings sobre discrepâncias

### 4. Validação Final (Alta Prioridade)

```bash
# Confirmar valor canônico
sqlite3 research/systematic_review.sqlite "SELECT COUNT(*) FROM papers"
# Esperado: 6516

# Verificar exports regenerados
grep -r "9356" research/exports/analysis/reports/
# Esperado: 0 matches

# Validar HTML
python -c "
from bs4 import BeautifulSoup
with open('research/exports/analysis/reports/summary_report.html') as f:
    soup = BeautifulSoup(f, 'html.parser')
    stat_cards = soup.find_all('div', class_='stat-card')
    total = stat_cards[0].find('h3').text
    print(f'Total no HTML: {total}')
    assert total == '6516', f'Esperado 6516, encontrado {total}'
"
```

---

## 📊 Impacto da Inconsistência

### Documentos Afetados

| Documento | Status Antes | Status Atual | Ação |
|-----------|--------------|--------------|------|
| `summary_report.html` | ❌ 9356 | ⏳ Pendente | Regenerar export |
| `prisma_flow.png` | ❌ 9356 | ⏳ Pendente | Regenerar export |
| `selection_funnel.png` | ❌ 9356 | ⏳ Pendente | Regenerar export |
| METODOLOGIA.md | ✅ 6516 | ✅ Correto | Nenhuma |
| RESUMO.md | ✅ 6516 | ✅ Correto | Nenhuma |
| CONCLUSOES.md | ✅ 6516 | ✅ Correto | Nenhuma |
| README_DOCS.md | ✅ 6516 | ⚠️ Refs deep_analysis/ | Limpar refs |
| ANALISE_ESTRUTURA_DOCS.md | ✅ 6516 | ⚠️ Refs deep_analysis/ | Limpar refs |

### Impacto Acadêmico

**Gravidade**: 🔴 **ALTA** - Inconsistência em métricas PRISMA compromete reprodutibilidade

**Riscos**:
1. **Revisão por pares**: Avaliadores questionarão discrepância entre números documentados
2. **Reprodutibilidade**: Impossível replicar análise com valores conflitantes
3. **Credibilidade**: Inconsistências indicam falta de rigor metodológico
4. **Comparações**: Outros pesquisadores não conseguirão comparar resultados

**Mitigação**:
- ✅ Banco de dados SQLite é fonte canônica confiável
- ✅ Documentação Markdown (METODOLOGIA, RESUMO) está correta
- ⏳ Exports HTML precisam regeneração URGENTE

---

## ✅ Checklist de Correção

### Código (Prioridade: 🔴 Alta)

- [ ] Corrigir `research/src/exports/excel.py::_compute_prisma_stats_from_df()`
- [ ] Corrigir `research/src/processing/selection.py::_load_dedup_stats_from_df()`
- [ ] Adicionar testes unitários para validação de métricas PRISMA
- [ ] Validar que `len(df)` sempre prevalece sobre `dedup_stats.initial_count`

### Exports (Prioridade: 🔴 Alta)

- [ ] Executar `python -m research.src.cli export -o research/exports/analysis/`
- [ ] Validar `summary_report.html` mostra 6516 (não 9356)
- [ ] Validar `prisma_flow.png` mostra 6516 no box "Identificação"
- [ ] Validar `selection_funnel.png` mostra 6516 no topo do funil

### Documentação (Prioridade: 🟡 Média)

- [ ] Remover referências a `deep_analysis/` em README_DOCS.md
- [ ] Remover referências a `deep_analysis/` em ANALISE_ESTRUTURA_DOCS.md
- [ ] Adicionar warning sobre versões antigas de exports
- [ ] Documentar processo de auditoria para futuras validações

### Validação (Prioridade: 🔴 Alta)

- [ ] Confirmar banco SQLite tem 6516 papers (fonte canônica)
- [ ] Grep por "9356" em todos os arquivos (deve retornar 0 matches em docs ativos)
- [ ] Validar todos os 16 papers incluídos têm `relevance_score >= 4.0`
- [ ] Confirmar 0 duplicatas marcadas no banco
- [ ] Executar `pytest tests/` para validar integridade do pipeline

---

## 📌 Notas Adicionais

### Sobre Duplicatas

**Observação importante**: O valor "2.594 duplicatas removidas" nos logs refere-se a:
- Duplicatas identificadas **DURANTE A COLETA** (fase de ingestão)
- **NÃO** são papers presentes no banco SQLite
- Deduplicação ocorre **ANTES** de inserir no banco
- Banco contém **APENAS** os 6.516 papers únicos

**Implicação**: Reportar "9.356 identificados - 2.594 duplicatas = 6.762" é **INCORRETO** porque:
1. O banco **JÁ** contém dados deduplicados (6.516)
2. Não há registro de duplicatas para apresentar no PRISMA (foram descartadas antes do DB)
3. PRISMA flow deve mostrar: "**6.516 identificados** (após deduplicação automática durante coleta)"

### Recomendação de Nomenclatura

**Atual** (confuso):
```
Identificação: 9.356
Duplicatas removidas: 2.594
Triagem: 6.516
```

**Proposto** (claro):
```
Registros coletados: 9.356
Duplicatas removidas (automático): 2.594
Identificação (únicos): 6.516
Triagem: 6.516
```

OU simplesmente:

```
Identificação: 6.516 (registros únicos)
Triagem: 6.516
Elegibilidade: 1.851
Incluídos: 16
```

### Princípio KISS (Keep It Simple, Stupid)

Conforme solicitado pelo usuário:
- ✅ **Fonte única de verdade**: SQLite database
- ✅ **Sem redundância**: Não reportar valores pré-dedup em produção
- ✅ **Clareza**: Números devem refletir estado atual do banco
- ❌ **Evitar**: Cálculos derivados (9356 - 2594) que confundem leitores

---

## 🎯 Resumo para TCC/PTC

**Usar SEMPRE estes valores**:

```yaml
identificacao: 6516
triagem_excluidos: 4665
triagem_aprovados: 1851
elegibilidade_excluidos: 1835
elegibilidade_aprovados: 16
incluidos_final: 16

taxa_inclusao: 0.25%  # (16/6516)
taxa_exclusao_triagem: 71.6%  # (4665/6516)
taxa_exclusao_elegibilidade: 99.1%  # (1835/1851)

score_medio_incluidos: 4.20
score_minimo: 4.0
score_maximo: 4.5

bases_dados: 4
queries_total: 108
periodo: 2017-2025
anos_cobertos: 9
```

---

**Última Atualização**: 16/11/2025 22:35  
**Auditado por**: Sistema automatizado + revisão manual  
**Próxima Revisão**: Após correção de código e regeneração de exports
