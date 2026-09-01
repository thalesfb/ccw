# Reconciliação Atualizada do Baseline da Revisão Sistemática

**Data:** 2026-08-31
**Fonte operacional local:** `research/systematic_review.sqlite` (não versionada)
**Representação versionada do snapshot:** `research/exports/analysis/papers.csv` e `research/exports/analysis/papers.json`
**Relatório derivado:** `research/exports/reports/summary.json`
**Manifesto de reprodutibilidade:** `research/exports/reports/reproducibility_manifest.json`
**Status:** baseline local validado; sincronização textual concluída; reaplicação do MMAT pendente

## 1. Estado atual do banco

O banco consolidado contém **11.904 registros**. Todos estão marcados com `is_duplicate = 0`; portanto, o export registra zero remoções adicionais baseadas nessa flag. Isso não equivale, por si só, a unicidade por DOI: a auditoria do export encontrou **10.658 DOIs normalizados distintos**, **1.222 registros sem DOI** e **24 grupos de DOI repetido** (48 linhas). Essa diferença é uma pendência de integridade dos dados e não deve ser ocultada pelo rótulo genérico “único”.

As contagens verificadas diretamente no banco são:

| Estado final do registro | Total |
|---|---:|
| Triagem | 9.413 |
| Elegibilidade | 2.475 |
| Incluído | **16** |
| **Total de registros no banco consolidado** | **11.904** |

Esses estados são mutuamente exclusivos e somam 11.904 registros.

## 2. Fluxo PRISMA a relatar

Para evitar ambiguidade entre registros que entram em uma etapa e registros excluídos nessa etapa, o fluxo deve ser apresentado com entradas, exclusões e remanescentes:

| Etapa | Entraram | Excluídos | Avançaram |
|---|---:|---:|---:|
| Identificação | 11.904 | — | 11.904 |
| Triagem | 11.904 | 9.413 | 2.491 |
| Elegibilidade | 2.491 | 2.475 | **16** |
| Inclusão | 16 | — | **16** |

As verificações aritméticas são:

```text
11.904 - 9.413 = 2.491
2.491 - 2.475 = 16
16 / 11.904 = aproximadamente 0,13%
```

O valor `9.413` é a quantidade excluída na triagem, e `2.475` é a quantidade excluída na elegibilidade. Eles não devem ser apresentados isoladamente como se fossem o total que entrou em cada etapa.

## 3. Estudos incluídos

O conjunto atual confirmado pelo banco é:

```text
1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
6916, 6917, 6918, 6920, 6921, 6923
```

Os dez primeiros registros pertencem ao conjunto bibliográfico já consolidado. Os seis registros com IDs 6916, 6917, 6918, 6920, 6921 e 6923 foram incorporados no snapshot atualizado.

## 4. Diferença em relação ao baseline histórico

O baseline histórico usado nos documentos anteriores era:

| Métrica | Baseline histórico | Baseline atual |
|---|---:|---:|
| Registros identificados | 9.431 | 11.904 |
| Duplicatas removidas na etapa histórica | 2.517 | 0 adicionais no banco consolidado |
| Registros no snapshot após a etapa de consolidação | 6.914 | 11.904 |
| Registros que avançaram à elegibilidade | 1.883 | 2.491 |
| Estudos incluídos | 17 | **16** |

Há uma pendência específica na coluna histórica: os documentos legados usam 2.517 duplicatas removidas, enquanto o único registro histórico preservado em `searches.results_summary` no SQLite registra `total_removed=2494` (e implicaria 6.937 registros após a consolidação). O baseline atual não depende desse valor histórico; a divergência deve ser resolvida a partir do artefato arquivado da execução original antes de qualquer afirmação definitiva sobre a deduplicação histórica.

A execução histórica tinha 17 estudos incluídos. Em uma nova rodada, foram encontrados 23 candidatos e removidos 7 falsos positivos, chegando aos 16 atuais. Portanto, a diferença não deve ser descrita como uma simples subtração de três registros: o snapshot atual também foi consolidado com nova contagem de ingestão e com o pipeline de scoring corrigido. Os sete registros que não pertencem mais ao conjunto incluído são os estudos associados às chaves históricas `Machine2022_010`, `Data2020_011`, `Enhancing2025_012`, `Authentic2024_013`, `Performance2023_014`, `Assessing2024_015` e `Analysis2021_016`.

### Registro dos sete overrides da auditoria

O banco atual permite reproduzir quais linhas foram retiradas do conjunto candidato: as sete estão na etapa `eligibility`, com `status=excluded`, `exclusion_reason=manual_exclusion_after_audit` e scores no limiar operacional. Este registro é um manifesto de rastreabilidade da decisão persistida; ainda não substitui a justificativa individual de pertinência que deverá ser arquivada para cada exclusão.

| ID no banco | DOI | Score | Estado atual |
|---:|---|---:|---|
| 14 | `10.56855/ijmme.v3i2.1299` | 4,05 | excluído manualmente após auditoria |
| 15 | `10.12973/ejmse.5.2.93` | 4,05 | excluído manualmente após auditoria |
| 6915 | `10.1186/s40561-025-00415-z` | 4,40 | excluído manualmente após auditoria |
| 6919 | `10.3390/su18041900` | 4,15 | excluído manualmente após auditoria |
| 6922 | `10.34657/31156` | 4,05 | excluído manualmente após auditoria |
| 6925 | `10.1186/s40594-025-00590-y` | 4,00 | excluído manualmente após auditoria |
| 6926 | `10.1016/j.aej.2025.03.095` | 4,00 | excluído manualmente após auditoria |

Como a lógica determinística de inclusão pelo score ainda selecionaria esses 23 candidatos sem o override, o manifesto versionado registra os sete overrides e os campos necessários para reencontrar cada linha. Ele ainda não inventa uma justificativa substantiva que não esteja documentada na auditoria: o campo de justificativa individual permanece pendente. Assim, os 16 estudos atuais são a composição auditada do snapshot, e não o resultado de uma regra automática suficiente, isoladamente, para reproduzir os sete descartes.

## 5. Correções do pipeline

As correções preservadas no código são:

- uso de `\bai\b` para evitar falsos positivos por substring, como em `aims` e `training`;
- remoção de `assessment` como termo amplo do grupo de *Learning Analytics*;
- uso explícito da flag `is_duplicate` para os estados PRISMA, com a ressalva de que a repetição de DOI ainda requer auditoria própria;
- seleção dos estudos incluídos diretamente pelo estado persistido no banco.

## 6. Bibliografia e MMAT

Os arquivos `results/tcc/referencias.bib` e `results/tcc/referencias_pedagogicas.bib`, carregados conjuntamente pelo `main.tex`, mantêm os 16 estudos atuais e as referências metodológicas, pedagógicas, de avaliação e técnicas. O export `research/exports/references/included_papers.bib` contém somente os 16 estudos derivados do pipeline.

A atualização do conjunto incluído tornou obsoleta a tabela MMAT histórica de 17 estudos. Não há julgamentos MMAT persistidos para os seis estudos novos no snapshot atual; por isso, a reaplicação do instrumento aos 16 estudos é uma pendência metodológica explícita. Até essa reaplicação, conclusões comparativas sobre qualidade metodológica ou certeza da evidência permanecem pendentes. Nenhum julgamento novo deve ser inferido apenas a partir dos metadados do banco.

## 7. Artefatos e próxima consolidação

Os artefatos derivados do banco foram regenerados a partir do mesmo snapshot, incluindo `summary.json`, `summary_report.html`, `papers_report_included.html`, `included_papers.bib` e as visualizações. O manuscrito canônico é `results/tcc/main.tex`, que inclui os arquivos em `results/tcc/conteudo/`. O histórico `9.431/2.494` foi mantido apenas como contexto e é ignorado pelo cálculo atual quando não fecha com as 11.904 linhas exportadas.

## 8. Reprodutibilidade sem versionar o SQLite

O SQLite é necessário como fonte operacional local para consultas, estados e
contagens, mas não é distribuído no repositório por ser um artefato grande e
mutável. A representação versionada do snapshot é composta por:

- `papers.csv` e `papers.json`, com os registros e estados usados na auditoria;
- `summary.json`, com o fluxo PRISMA e as estatísticas derivadas;
- `included_papers.bib`, com somente os 16 estudos do pipeline;
- `reference_audit.csv` e os dois arquivos bibliográficos carregados pelo TCC,
  `results/tcc/referencias.bib` e `results/tcc/referencias_pedagogicas.bib`, que
  mantêm separadas as decisões bibliográficas dos estudos e as referências
  teóricas/metodológicas;
- o manifesto JSON, que registra os IDs incluídos, os sete overrides, os hashes
  dos artefatos e as limitações da reexecução.

Para verificar o snapshot publicado, use os arquivos versionados e execute:

```text
python -m research.src.cli --db /caminho/para/systematic_review.sqlite generate-manifest
python -m research.src.cli --db /caminho/para/systematic_review.sqlite stats
python -m research.src.cli --db /caminho/para/systematic_review.sqlite export
```

O primeiro comando atualiza o manifesto a partir de uma cópia local do banco;
ele não adiciona o SQLite ao Git. Uma nova coleta com `run-pipeline` é uma
reexecução metodológica, não uma garantia de obter exatamente o mesmo snapshot,
porque APIs, cache e metadados externos podem mudar.

Antes do commit final, devem ser verificados:

1. ausência dos números históricos no texto atual do TCC, salvo quando explicitamente marcados como histórico;
2. presença exclusiva das 16 chaves atuais entre os estudos incluídos;
3. correspondência entre o banco, os exports e a bibliografia, incluindo a decisão documentada sobre os DOIs repetidos;
4. reaplicação ou registro formal da pendência do MMAT;
5. compilação do TCC e inspeção do PDF atualizado.
