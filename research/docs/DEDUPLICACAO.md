# Estratégia de Deduplicação Não-Destrutiva

## Visão Geral

O pipeline implementa uma estratégia de **deduplicação não-destrutiva**, onde todos os registros coletados são preservados no banco de dados e duplicatas são apenas marcadas com flags, nunca deletadas.

## Implementação

### Campos do Banco de Dados

- **`is_duplicate`** (BOOLEAN): Flag indicando se o registro é uma duplicata (1) ou original (0)
- **`duplicate_of`** (TEXT): Referência ao registro original (DOI ou URL do primeiro registro encontrado)

### Lógica de Detecção

A função `find_duplicates()` em `research/src/processing/dedup.py` identifica duplicatas por:

1. **DOI normalizado**: Remove pontuação, converte para lowercase
2. **URL**: Se DOI não disponível, compara URLs normalizadas
3. **Marcação**: Todas as ocorrências exceto a primeira são marcadas como duplicatas

### Semântica PRISMA 2020

A estratégia respeita a semântica PRISMA 2020:

- **identification**: Total de registros coletados (incluindo duplicatas)
  - Exemplo: 9513 papers
- **duplicates_removed**: Contagem de registros marcados como `is_duplicate=1`
  - Exemplo: 2505 duplicatas identificadas
- **screening**: Conjunto único de registros para triagem (identification - duplicates_removed)
  - Exemplo: 7008 papers únicos

## Artefatos Gerados

### Banco de Dados
- **Localização**: `research/systematic_review.sqlite`
- **Tabela**: `papers` com todos os 9513 registros
- **Schema**: Sem constraint UNIQUE no DOI (permite múltiplos registros)

### Arquivo de Auditoria
- **Localização**: `research/exports/analysis/deduplicated_rows.csv`
- **Conteúdo**: Todos os registros marcados como `is_duplicate=True` com referências `duplicate_of`
- **Propósito**: Trail de auditoria completo; permite reconstruir lógica de deduplicação

## Benefícios

1. **Preservação de dados**: Nenhum registro é perdido; possível recuperar dados se necessário
2. **Auditoria completa**: Rastreabilidade total da lógica de deduplicação via CSV
3. **Flexibilidade**: Possível ajustar critérios de deduplicação retroativamente
4. **PRISMA compliance**: Contagens corretas para identification (pré-dedup) vs screening (pós-dedup)
5. **Compatibilidade reversa**: Exporter suporta DBs legados (sem flags) via fallback para CSV

## Queries Úteis

### Verificar totais
```sql
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN is_duplicate = 1 THEN 1 ELSE 0 END) as duplicates,
  COUNT(*) - SUM(CASE WHEN is_duplicate = 1 THEN 1 ELSE 0 END) as unique_papers
FROM papers;
```

### Listar duplicatas de um DOI específico
```sql
SELECT title, doi, duplicate_of 
FROM papers 
WHERE is_duplicate = 1 AND duplicate_of = 'DOI:10.1234/example'
ORDER BY retrieved_at;
```

### Exportar registros únicos
```sql
SELECT * FROM papers WHERE is_duplicate = 0 OR is_duplicate IS NULL;
```

## Migração Automática

O `DatabaseManager` detecta automaticamente bancos legados (com UNIQUE constraint no DOI) e executa migração:

1. Desabilita foreign keys temporariamente
2. Cria nova tabela sem UNIQUE constraint
3. Copia todos os dados preservando histórico
4. Adiciona colunas `is_duplicate` e `duplicate_of`
5. Reabilita foreign keys

**Importante**: A migração é segura e preserva todos os dados existentes.

## Referências

- **Schema**: `research/src/database/schema.py`
- **Manager**: `research/src/database/manager.py` (método `_migrate_schema_if_needed()`)
- **Dedup Logic**: `research/src/processing/dedup.py` (função `find_duplicates()`)
- **Pipeline**: `research/src/pipeline/run.py` (método `process_data()`)
- **Exporter**: `research/src/exports/excel.py` (método `_compute_prisma_stats_from_df()`)
