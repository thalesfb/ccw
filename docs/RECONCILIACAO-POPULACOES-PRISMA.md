# Reconciliação das populações PRISMA

> **Registro histórico — supersedido:** esta auditoria descreve a divergência
> entre o SQLite e o export antes do congelamento da população adjudicada. Use
> `docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md` para o estado vigente.

Status: auditoria de consistência. Este documento não altera a composição da revisão nem autoriza a atualização do TCC.

## Escopo e fontes

Esta auditoria compara a população persistida localmente no SQLite com os artefatos versionados da exportação. O SQLite não é incluído no controle de versão; ele foi consultado apenas como evidência operacional local.

As fontes versionadas são:

- `research/exports/reports/summary.json`;
- `research/exports/analysis/papers.csv`;
- `research/exports/analysis/deduplication_identity_audit.csv`.

O recorte configurado é inclusivo de 2015 a 2026, com data-limite em 2026-08-31. A presença do registro 6918 nesse conjunto ainda depende da adjudicação de conflito de metadados documentada no PR 48.

## População do fluxo exportado

Os números abaixo são os observados no `summary.json` do snapshot de 2026-08-31:

| Ponto de controle | Registros | Definição |
| --- | ---: | --- |
| Identificação bruta | 11.904 | Linhas antes da remoção determinística por identidade |
| Duplicatas determinísticas | 27 | Excedentes de DOI/URL normalizado: 25 por DOI e 2 por URL |
| Entrada na triagem | 11.877 | 11.904 - 27 |
| Excluídos na triagem | 9.391 | Registros que não avançaram para elegibilidade |
| Avançaram para elegibilidade | 2.486 | 11.877 - 9.391 |
| Excluídos na elegibilidade | 2.470 | Registros elegíveis operacionalmente, mas abaixo do critério aplicado |
| Incluídos | 16 | Registros finais do snapshot operacional |

As porcentagens correspondentes, calculadas sobre esses denominadores, são: 78,89% excluídos na triagem sobre a identificação bruta; 20,88% avançados sobre a identificação bruta; 99,36% excluídos na elegibilidade; e 0,64% incluídos entre os que chegaram à elegibilidade.

## Divergência encontrada

A consulta ao SQLite local retornou a seguinte distribuição terminal:

| Estágio terminal no SQLite | Status | Registros |
| --- | --- | ---: |
| screening | excluded | 9.413 |
| eligibility | excluded | 2.475 |
| included | included | 16 |
| **Total** |  | **11.904** |

Comparando essa distribuição com `papers.csv`, que contém 11.877 linhas, a diferença líquida é:

- 22 registros a menos em `screening`;
- 5 registros a menos em `eligibility`;
- nenhuma diferença em `included`.

O arquivo de auditoria de identidade lista 27 IDs ausentes da exportação: 21 originalmente marcados em `screening` e 6 em `eligibility`. Portanto, a distribuição líquida 22/5 não pode ser explicada apenas pela coluna `duplicate_stage`. Há também uma mudança de estágio do registro 8031: `screening` com motivo `inclusion_criteria_not_met` no SQLite e `eligibility` com motivo `low_relevance_score` na exportação. O registro 9357 mantém o estágio, mas muda o motivo de exclusão.

Esse achado não escolhe qual estado é cientificamente correto. Ele demonstra que o banco persistido e a exportação não são a mesma população decisória. Antes de atualizar o manuscrito, é necessário definir um artefato canônico imutável e gerar banco derivado, CSV, JSON, relatórios e figuras a partir dele.

## Implicações para a redação

Até a reconciliação ser aprovada:

1. não se deve declarar que não houve duplicatas;
2. não se deve misturar os números terminais do SQLite com os números do fluxo deduplicado;
3. as contagens de motivos devem ser apresentadas com o mesmo denominador e a mesma população do diagrama PRISMA;
4. os 16 incluídos são uma contagem operacional provisória, não uma decisão final sobre a validade científica de cada estudo;
5. a adjudicação temporal do registro 6918 deve ocorrer antes da síntese e da reavaliação MMAT.

## Próxima decisão técnica

O PR seguinte deve fazer a reconciliação da população, sem modificar o TCC: uma exportação congelada deve conter a identidade do registro, a etapa, o status, o motivo primário, a origem da decisão e o hash do artefato. O SQLite poderá ser reconstruído dessa exportação, mas não será tratado como arquivo publicado.
