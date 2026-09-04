# Verificação dos Números PRISMA — Esclarecimento

> **Aviso de versão:** esta verificação preserva o baseline histórico de 9.431
> registros e 17 incluídos e a baseline operacional anterior de 31/08/2026.
> A fonte vigente, após o PR #55, é
> `docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md`, com 18 registros
> retidos e o ID 6918 corrigido para 2014 e excluído do recorte.

## Estado do baseline operacional anterior (31/08/2026)

O snapshot operacional anterior continha **11.904 registros brutos**. O fluxo verificado remove 27
registros redundantes por DOI/URL antes da triagem: **11.877** avaliados,
**9.391** excluídos na triagem, **2.486** avançando à elegibilidade, **2.470**
excluídos na elegibilidade e **16** registros retidos operacionalmente. Desses,
15 registros são provisoriamente classificados como empíricos; o 6918 permanece em hold temporal e o ID 6921 é um protocolo contextual fora da síntese empírica.
Os IDs retidos são 1--10,
6916, 6917, 6918, 6920, 6921 e 6923.

A execução histórica tinha 17 incluídos. Em uma nova rodada, foram identificados 23 candidatos e aplicados 7 overrides manuais, chegando aos 16 registros retidos operacionais. A diferença também envolve atualização da ingestão e correção do scoring; não é uma simples substituição numérica. A reavaliação documental do MMAT aos registros empíricos aplicáveis foi registrada com decisões e evidências por critério; nove textos primários foram revisados externamente, enquanto a confirmação das fontes, a adjudicação e a conclusão final permanecem pendentes. Quatro overrides ainda exigem adjudicação de fonte primária/escopo.

![Fluxo PRISMA do snapshot operacional atual](../research/exports/visualizations/prisma_flow.png)

![Funil de seleção do snapshot operacional atual](../research/exports/visualizations/selection_funnel.png)

### Auditoria de identidade do snapshot atual

O snapshot possui **0 remoções pela flag persistida**, mas a reconstrução do
fluxo identifica **27 registros redundantes por identidade determinística**:
25 excedentes em 25 grupos de DOI e 2 excedentes em 2 grupos de URL exata; um
dos grupos de URL é misto quanto à presença de DOI, por isso a URL é tratada
como evidência independente de identidade e não como uma classe “sem DOI”.
Também foram encontrados **177 grupos de título normalizado** (434 linhas; 257
excedentes brutos). Após retirar as 27 identidades DOI/URL, permanecem **154
grupos** (386 linhas; 232 excedentes) apenas por título. Esses títulos são
candidatos fracos e não são removidos automaticamente; a decisão por DOI/URL
não é uma avaliação de qualidade metodológica.

## Questão da Banca (baseline histórico)

A banca questionou se o número de duplicatas removidas estava correto, sugerindo:
- Se: 9.431 - 2.494 = 6.937 (diferente de 6.914)

## Análise e Resultado do baseline histórico

### Números do snapshot histórico (documentados, não confirmados pela execução preservada)

| Métrica | Valor | Verificação |
|---------|-------|------------|
| **Total identificado** | 9.431 | Documentado no histórico |
| **Duplicatas removidas** | **2.517** | Documentado, mas conflita com `total_removed=2494` no único registro preservado |
| **Taxa de duplicatas** | 26,6% | Derivada de 2.517 ÷ 9.431; não é validação independente |
| **Registros únicos** | 6.914 | Aritmética interna do histórico; não é baseline vigente |

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
9.431 - 2.517 = 6.914 (aritmética interna do documento histórico)
9.431 - 2.494 = 6.937 (valor implicado pelo registro histórico preservado)

As duas contas são matematicamente corretas para as respectivas entradas; o
repositório não preserva a execução que permita decidir qual entrada representa
a coleta histórica.
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
- `research/exports/analysis/mmat_visualization.html` — Visualização histórica do MMAT (17 estudos; não é o resultado atual)

Os documentos legados estão consistentes entre si com 2.517 duplicatas, mas esse valor não é reproduzido pelo único registro histórico atualmente disponível na tabela `searches` do SQLite, que registra `total_removed=2494`. A divergência histórica requer o artefato arquivado da execução original.

## Método de Remoção de Duplicatas (snapshot histórico)

A deduplicação foi realizada em **3 etapas**:

1. **Por DOI**: Registros com DOI idêntico foram consolidados
2. **Por Similaridade de Título**: Títulos com similaridade TF-IDF coseno > 0.9 foram considerados duplicatas
3. **Verificação Manual**: Pares suspeitos foram revistos manualmente

Maiores detalhes em: `results/tcc/conteudo/metodologia.tex` (Capítulo 3, Seção 3.4)

## Conclusão sobre o snapshot histórico

Os documentos do snapshot histórico são internamente consistentes quando usam
**2.517 duplicatas removidas**, mas essa contagem não está reproduzida pelo
artefato histórico preservado. Portanto, ela não deve ser chamada de verificada
nem usada para recalcular o baseline atual. Para o estado vigente, use a
reconciliação de 31/08/2026 e a auditoria de candidatos de duplicidade.

---

**Registro histórico**: 29 de março de 2026
**Atualização do baseline vigente**: 31 de agosto de 2026
**Responsável**: Análise técnica automática do pipeline Python + verificação manual
