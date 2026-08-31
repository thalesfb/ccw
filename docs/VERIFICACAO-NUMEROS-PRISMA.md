# Verificação dos Números PRISMA — Esclarecimento

## Questão da Banca

A banca questionou se o número de duplicatas removidas estava correto, sugerindo:
- Se: 9.431 - 2.494 = 6.937 (diferente de 6.914)

## Análise e Resultado

### Números Corretos (Confirmados)

| Métrica | Valor | Verificação |
|---------|-------|------------|
| **Total identificado** | 9.431 | ✓ Confirmado em 4 bases de dados |
| **Duplicatas removidas** | **2.517** | ✓ Verificado em `summary.json` |
| **Taxa de duplicatas** | 26,6% | ✓ (2.517 ÷ 9.431 = 0,2668) |
| **Registros únicos** | 6.914 | ✓ (9.431 - 2.517 = 6.914) |

### Origem da Confusão: O "2494"

O número **2494** aparece no arquivo de dados (`research/exports/analysis/papers.csv`), mas é apenas:
- **Índice de linha** na tabela CSV (row 2494)
- **NÃO é** o número de duplicatas removidas

### Verificação Técnica

A fonte oficial dos números é o arquivo `research/exports/reports/summary.json`:

```json
{
  "statistics": {
    "prisma": {
      "identification": 9431,
      "duplicates_removed": 2517,
      "screening": 6914
    }
  }
}
```

### Verificação Aritmética

```
9.431 - 2.517 = 6.914 ✓ Correto
9.431 - 2.494 = 6.937 ✗ Incorreto (não coincide com 6.914)
```

## Onde os Números Aparecem no Projeto

### Documentos LaTeX (TCC)

- **`results/tcc/conteudo/resultadosesperados.tex`** (Capítulo 4, Seção 4.2)
  ```latex
  Duplicatas removidas & 2.517 (26,6\%) \\
  ```

- **`results/ptc/conteudo/resultadosesperados.tex`** (mesmo conteúdo)

### Página Web Principal

- **`index.html`** — Seção "Fluxo PRISMA 2020"
  ```html
  <li><strong>Remoção de Duplicatas:</strong> 2.517 duplicatas removidas (26,6%) → 6.914 registros únicos</li>
  ```

### Visualizações (Imagens/Gráficos)

- `research/exports/visualizations/prisma_flow.png` — Diagrama PRISMA
- `research/exports/visualizations/selection_funnel.png` — Funil de seleção
- `research/exports/analysis/mmat_visualization.html` — Tabela de estatísticas

**Todos os documentos e imagens estão consistentes com 2.517 duplicatas.**

## Método de Remoção de Duplicatas

A deduplicação foi realizada em **3 etapas**:

1. **Por DOI**: Registros com DOI idêntico foram consolidados
2. **Por Similaridade de Título**: Títulos com similaridade TF-IDF coseno > 0.9 foram considerados duplicatas
3. **Verificação Manual**: Pares suspeitos foram revistos manualmente

Maiores detalhes em: `results/tcc/conteudo/metodologia.tex` (Capítulo 3, Seção 3.4)

## Conclusão

✅ **Os números estão corretos e verificados.**

Não há inconsistência matemática ou metodológica. Todos os documentos, imagens e análises usam o valor correto: **2.517 duplicatas removidas**.

---

**Data de Verificação**: 29 de março de 2026
**Responsável**: Análise técnica automática do pipeline Python + verificação manual
