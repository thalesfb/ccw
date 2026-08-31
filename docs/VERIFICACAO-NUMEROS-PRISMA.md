# Verificação dos Números PRISMA — Esclarecimento

> **Aviso de versão:** esta verificação cobre o baseline histórico de 9.431 registros e 17 incluídos. A fonte atual, validada em 31/08/2026, é `docs/RECONCILIACAO-BASELINE-2026-08-31.md` e registra 11.904 registros consolidados e 16 incluídos.

## Estado vigente (31/08/2026)

O banco atual contém **11.904 registros**. O fluxo verificado é: **9.413** excluídos na triagem, **2.491** avançando à elegibilidade, **2.475** excluídos na elegibilidade e **16** incluídos. Os IDs incluídos são 1--10, 6916, 6917, 6918, 6920, 6921 e 6923.

A execução histórica tinha 17 incluídos. Em uma nova rodada, foram encontrados 23 candidatos e removidos 7 falsos positivos, chegando aos 16 atuais. A diferença também envolve atualização da ingestão e correção do scoring; não é uma simples substituição numérica. A reaplicação do MMAT aos 16 estudos atuais permanece pendente, assim como conclusões comparativas sobre qualidade metodológica ou certeza da evidência.

## Questão da Banca (baseline histórico)

A banca questionou se o número de duplicatas removidas estava correto, sugerindo:
- Se: 9.431 - 2.494 = 6.937 (diferente de 6.914)

## Análise e Resultado do baseline histórico

### Números do snapshot histórico (confirmados)

| Métrica | Valor | Verificação |
|---------|-------|------------|
| **Total identificado** | 9.431 | ✓ Confirmado em 4 bases de dados |
| **Duplicatas removidas** | **2.517** | ✓ Verificado em `summary.json` |
| **Taxa de duplicatas** | 26,6% | ✓ (2.517 ÷ 9.431 = 0,2668) |
| **Registros únicos** | 6.914 | ✓ (9.431 - 2.517 = 6.914) |

### Origem da Confusão: O "2494"

O número **2494** aparece no arquivo de dados (`research/exports/analysis/papers.csv`), mas é apenas:
- **Índice de linha** na tabela CSV (row 2494)
- **e também** consta como `total_removed` no registro histórico de `searches` do SQLite

Logo, ele não pode ser descartado apenas como índice de linha.

### Verificação Técnica

O trecho abaixo é o registro do snapshot histórico de `research/exports/reports/summary.json`; o arquivo atual foi regenerado e não deve ser usado para atribuir estes valores ao baseline vigente:

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

## Onde os Números Apareciam no snapshot histórico

### Documentos LaTeX (TCC, versão histórica)

- **`results/tcc/conteudo/resultadosesperados.tex`** (Capítulo 4, Seção 4.2)
  ```latex
  Duplicatas removidas & 2.517 (26,6\%) \\
  ```

- **`results/ptc/conteudo/resultadosesperados.tex`** (mesmo conteúdo)

### Página Web Principal (versão histórica)

- **`index.html`** — Seção "Fluxo PRISMA 2020"
  ```html
  <li><strong>Remoção de Duplicatas:</strong> 2.517 duplicatas removidas (26,6%) → 6.914 registros únicos</li>
  ```

### Visualizações (imagens/gráficos históricos)

- `research/exports/visualizations/prisma_flow.png` — Diagrama PRISMA
- `research/exports/visualizations/selection_funnel.png` — Funil de seleção
- `research/exports/analysis/mmat_visualization.html` — Tabela de estatísticas

Os documentos legados estão consistentes entre si com 2.517 duplicatas, mas esse valor não é reproduzido pelo único registro histórico atualmente disponível na tabela `searches` do SQLite, que registra `total_removed=2494`. A divergência histórica requer o artefato arquivado da execução original.

## Método de Remoção de Duplicatas (snapshot histórico)

A deduplicação foi realizada em **3 etapas**:

1. **Por DOI**: Registros com DOI idêntico foram consolidados
2. **Por Similaridade de Título**: Títulos com similaridade TF-IDF coseno > 0.9 foram considerados duplicatas
3. **Verificação Manual**: Pares suspeitos foram revistos manualmente

Maiores detalhes em: `results/tcc/conteudo/metodologia.tex` (Capítulo 3, Seção 3.4)

## Conclusão sobre o snapshot histórico

✅ **Os números do snapshot histórico estão corretos e verificados.**

Não há inconsistência matemática no snapshot histórico: aqueles documentos, imagens e análises usavam **2.517 duplicatas removidas**. Essa conclusão não se aplica às contagens vigentes; para o estado atual, deve-se usar a reconciliação de 31/08/2026.

---

**Data de Verificação**: 29 de março de 2026
**Responsável**: Análise técnica automática do pipeline Python + verificação manual
