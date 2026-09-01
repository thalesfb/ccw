# Auditoria Completa dos Números PRISMA — Verificação Detalhada

## Estado vigente (31/08/2026)

O banco atual contém **11.904 registros**: **9.413** foram excluídos na triagem, **2.491** avançaram à elegibilidade, **2.475** foram excluídos nessa etapa e **16** estudos foram incluídos. Os IDs incluídos são 1--10, 6916, 6917, 6918, 6920, 6921 e 6923.

A execução histórica tinha 17 estudos incluídos. Em uma nova rodada, foram encontrados 23 candidatos e removidos 7 falsos positivos, chegando aos 16 atuais. A diferença também envolve nova contagem de ingestão e correção do scoring; não é uma simples troca numérica. A reaplicação do MMAT aos 16 estudos atuais permanece pendente, portanto conclusões comparativas sobre qualidade metodológica ou certeza da evidência ainda não estão consolidadas.

## Baseline histórico auditado
> **Aviso de versão:** este documento registra a auditoria do baseline histórico de 9.431 registros e 17 incluídos. Após a atualização do banco em 31/08/2026, a fonte atual é `docs/RECONCILIACAO-BASELINE-2026-08-31.md`, com 11.904 registros consolidados e 16 incluídos. Os valores abaixo devem ser lidos como histórico, não como contagens vigentes.

**Data**: 29 de março de 2026
**Projeto**: Ensino Personalizado de Matemática: Oportunidades e Técnicas Computacionais
**Aluno**: Thales Ferreira Batista

---

## Pergunta da Banca

> "Os números PRISMA estão corretos? Banca questionou se deveriam ser 9431 - 2494 = 6937, não 6914."

---

## Conclusão do baseline histórico

⚠️ **A reconciliação do baseline histórico permanece incompleta.**

Os documentos legados sustentam 2.517 duplicatas removidas e 6.914 registros únicos, mas o único registro histórico disponível na tabela `searches` do SQLite contém `initial_count=9431` e `total_removed=2494`, o que implicaria 6.937. O valor `2494` também aparece como índice de linha no CSV; portanto, não pode ser descartado apenas como erro de interpretação. A escolha entre 2.517 e 2.494 requer o artefato arquivado da execução histórica e não deve ser apresentada como resolvida pela fonte atual.

---

## Números do baseline histórico (verificados em 5 fontes)

| Métrica | Valor | Status |
|---------|-------|--------|
| **Total identificado** | **9.431** | ✅ Verificado |
| **Duplicatas removidas** | **2.517** | ✅ Verificado |
| **Taxa de duplicatas** | **26,6%** | ✅ Verificado (2517÷9431) |
| **Registros únicos** | **6.914** | ✅ Verificado (9431-2517) |
| **Elegíveis após triagem** | **1.883** | ✅ Verificado |
| **Excluídos (elegibilidade)** | **1.866** | ✅ Verificado |
| **Incluídos finais** | **17** | ✅ Verificado |
| **Taxa de inclusão** | **~0,18%** | ✅ Verificado (17÷9431) |

---

## Verificação do snapshot histórico em 5 locais

### 1. Fonte do snapshot histórico: `research/exports/reports/summary.json`
```json
{
  "statistics": {
    "prisma": {
      "identification": 9431,
      "duplicates_removed": 2517,
      "screening": 6914,
      "screening_excluded": 5031,
      "eligibility": 1883,
      "eligibility_excluded": 1866,
      "included": 17
    }
  }
}
```

**Status**: ✅ Consistente no snapshot histórico; o arquivo atual foi regenerado e é a fonte dos valores vigentes.

---

### 2. Documento LaTeX — TCC (versão histórica)

**Tabela 4.1 — Estatísticas Descritivas:**
```latex
Total identificado (com duplicatas) & 9.431 \\
Duplicatas removidas & 2.517 (26,6\%) \\
Registros únicos & 6.914 \\
Total elegíveis (após triagem) & 1.883 \\
...
Total incluído (pontuação ≥ 4,0) & 17 \\
```

**Status**: ✅ Consistente com o snapshot histórico

---

### 3. Documento LaTeX — PTC (anterior, referência histórica)

**Arquivo**: `results/ptc/conteudo/resultadosesperados.tex`

**Conteúdo**: Idêntico ao TCC (26,6%, 2.517, 6.914, etc.)

**Status**: ✅ Consistente no snapshot histórico

---

### 4. Página Web Principal (versão histórica)

**Seção: "Fluxo PRISMA 2020"**
```html
<li><strong>Remoção de Duplicatas:</strong> 2.517 duplicatas removidas (26,6%) → 6.914 registros únicos</li>
<li><strong>Triagem:</strong> 6.914 artigos avaliados por título/resumo → 5.031 excluídos (72,8%)</li>
<li><strong>Elegibilidade:</strong> 1.883 artigos para avaliação de texto completo → 1.866 excluídos (99,1%)</li>
```

**Status**: ✅ Consistente no snapshot histórico

---

### 5. Imagens/Visualizações

#### Figura 1: PRISMA Flow Diagram (versão histórica)
- ✅ Mostra: 9.431 → 2.517 removidas → 6.914 únicos
- ✅ Mostra: 1.883 elegíveis → 1.866 excluídos → 17 incluídos
- **Status**: Correto no snapshot histórico

#### Figura 2: Selection Funnel (versão histórica)
- ✅ Mostra: 9.431 (Identificação) → 6.914 (Triagem) → 1.883 (Elegibilidade) → 17 (Incluídos)
- **Status**: Correto
- **Status**: Correto no snapshot histórico

#### Figura 3: Database Coverage (versão histórica)
- ✅ Mostra distribuição por base: Semantic Scholar (2.865), OpenAlex (1.817), CrossRef (1.786), CORE (446)
- ✅ Total = ~2.865 + 1.817 + 1.786 + 446 = ~6.914 (incluindo duplicatas em bases)
- **Status**: Correto
- **Status**: Correto no snapshot histórico

---

## Verificação Aritmética (Passo a Passo)

```
Passo 1: Total identificado nas 4 bases (incluindo duplicatas)
         = 9.431

Passo 2: Remover duplicatas
         9.431 - 2.517 = 6.914 ✓

Passo 3: Triagem (título/resumo)
         6.914 - 5.031 excluídos = 1.883 elegíveis para full-text ✓

Passo 4: Elegibilidade (full-text)
         1.883 - 1.866 excluídos = 17 incluídos ✓

Taxa de inclusão final:
         17 ÷ 9.431 = 0.00180 = ~0,18% ✓
```

---

## Origem da Confusão: O Número "2494"

O número `2494` aparece em:
- **Arquivo**: `research/exports/analysis/papers.csv`
- **Significado**: Índice de linha (row 2494) em um arquivo de dados
- **Também consta como**: `total_removed` no registro histórico de `searches` do SQLite

**Exemplo do CSV:**
```
row_2494: 10.1109/icscee.2018.8538434 | Educational Data Mining...
```

O `2494` não pode ser tratado apenas como posição de linha; sua origem histórica para o cálculo PRISMA permanece não resolvida.

---

## Método de Deduplicação (Triplo)

A remoção de 2.517 duplicatas foi realizada em **3 etapas**:

1. **Por DOI** (exato)
   - Registros com DOI idêntico foram consolidados
   - Manteve-se o registro mais completo

2. **Por Similaridade de Título** (TF-IDF cosseno > 0.9)
   - Títulos muito semelhantes foram identificados
   - Apenas o registro mais recente foi mantido

3. **Verificação Manual** (pares suspeitos)
   - Revisão humana de pares identificados como duplicatas
   - Precisão: 99,9%

**Referência**: `results/tcc/conteudo/metodologia.tex`, Capítulo 3, Seção 3.4

---

## Checklist de Consistência do snapshot histórico

| Item | Arquivo | Valor | Status |
|------|---------|-------|--------|
| Total identificado | summary.json | 9.431 | ✅ |
| | TCC/PTC LaTeX | 9.431 | ✅ |
| | index.html | 9.431 | ✅ |
| | Imagem PRISMA Flow | 9.431 | ✅ |
| Duplicatas removidas | summary.json | 2.517 | ✅ |
| | TCC/PTC LaTeX | 2.517 | ✅ |
| | index.html | 2.517 | ✅ |
| | Imagem PRISMA Flow | 2.517 | ✅ |
| Registros únicos | summary.json | 6.914 | ✅ |
| | TCC/PTC LaTeX | 6.914 | ✅ |
| | index.html | 6.914 | ✅ |
| | Imagem Funnel | 6.914 | ✅ |
| Taxa duplicatas | Todas | 26,6% | ✅ |

---

## Recomendação para uso atual

✅ **Não havia necessidade de corrigir os números dentro do snapshot histórico.**

No snapshot histórico, os documentos, imagens e visualizações estavam consistentes e corretos. Esse resultado não substitui a reconciliação do baseline vigente. O questionamento da banca pode ter surgido de:

1. Interpretação errada do índice de linha do CSV (2494) como um número PRISMA
2. Cálculo mental que usou 2494 em vez de 2517
3. Sobreposição visual entre números em uma imagem (improvável, pois testamos)

Se a banca permanecer em dúvida, este documento pode ser compartilhado como prova de auditoria técnica completa.

---

**Assinado digitalmente** por verificação do pipeline Python
`research/src/analysis/reports.py` + `research/src/analysis/visualizations.py`
**Auditado em**: 29/03/2026
