# Reconciliação Atualizada do Baseline da Revisão Sistemática

**Snapshot:** 2026-08-31
**Última atualização documental:** 2026-09-01
**Fonte operacional local:** `research/systematic_review.sqlite` (não versionada)
**Representação versionada do snapshot:** `research/exports/analysis/papers.csv` e `research/exports/analysis/papers.json`
**Relatório derivado:** `research/exports/reports/summary.json`
**Manifesto de reprodutibilidade:** `research/exports/reports/reproducibility_manifest.json`
**Status:** baseline local validado; reavaliação preliminar do MMAT registrada; avaliação final pendente

## 1. Estado atual do banco

O banco operacional consolidado contém **11.904 registros**. A coluna persistida
`is_duplicate` está zerada, mas isso não equivale a uma base sem duplicidade:
foram encontrados **25 excedentes por DOI normalizado** e **2 excedentes por URL
exata**. Um dos grupos de URL é misto quanto à presença de DOI: a URL confirma
a identidade mesmo quando apenas um dos registros traz DOI. Esses **27 registros de identidade determinística** são
deduplicados na reconstrução do fluxo PRISMA e não dependem da flag persistida.
O export analítico, portanto, parte de 11.904 registros identificados e leva
**11.877 registros** à triagem. A auditoria bruta encontrou **257 excedentes em
grupos de título normalizado**; depois de retirar as identidades DOI/URL, restam
**232 excedentes apenas por título** para disposição semântica. Nenhum deles é
removido automaticamente, pois igualdade textual pode representar obras,
versões ou registros distintos.

### Auditoria de identidade do snapshot

| Chave de identidade | Grupos repetidos | Linhas nos grupos | Linhas excedentes | Interpretação |
|---|---:|---:|---:|---|
| DOI normalizado | 25 | 50 | 25 | Identidade determinística; um registro por DOI é mantido no fluxo PRISMA |
| URL exata | 2 | 4 | 2 | Identidade determinística independente; um grupo é misto quanto à presença de DOI |
| Título normalizado | 177 | 434 | 257 | Candidatos fracos; títulos iguais podem ser obras diferentes |
| Título-only após DOI/URL | 154 | 386 | 232 | Candidatos restantes depois da remoção determinística; exigem disposição semântica |

O banco possui **0 flags persistidas de duplicidade**, mas o fluxo reconstruído
registra **27 remoções determinísticas por DOI/URL**. As 177 repetições de título
(257 excedentes brutos; 232 excedentes depois da deduplicação por identidade)
continuam sem remoção automática e **0 duplicatas foram confirmadas apenas por
título**. A decisão determinística é de identidade de registro, não uma
avaliação de qualidade metodológica; versões, erratas e relações bibliográficas
especiais devem continuar sendo verificadas quando surgirem nos grupos. O caso dos registros
com DOI `10.1184/r1/6715271` e `10.1184/r1/6715271.v1` é mantido sob revisão
como possível relação de versão.

O arquivo `research/exports/analysis/deduplication_identity_audit.csv` registra,
para cada linha removida, o `duplicate_id`, o `retained_id` usado como fonte de
metadados e, quando diferem, o `retained_stage_source_id` que forneceu a etapa
PRISMA mais avançada. Dessa forma, a reconstrução não confunde metadado mais
completo com origem do estado de seleção.

As contagens verificadas diretamente no banco são:

| Estado final do registro | Total |
|---|---:|
| Triagem | 9.413 |
| Elegibilidade | 2.475 |
| Incluído | **16** |
| **Total de registros no banco consolidado** | **11.904** |

Esses estados são mutuamente exclusivos e somam 11.904 registros.

### Motivos persistidos na triagem (banco bruto)

As 9.413 exclusões da triagem não são uma categoria única. O snapshot atual
registra a seguinte distribuição de motivos operacionais:

| Motivo persistido | Registros |
|---|---:|
| `abstract_too_short` | 4.325 |
| `inclusion_criteria_not_met` | 2.862 |
| `no_methodology` | 2.081 |
| `non_research` | 103 |
| `off_topic` | 42 |
| **Total** | **9.413** |

Esses motivos descrevem a regra aplicada na triagem e não constituem uma
apreciação de qualidade metodológica. A razão `manual_exclusion_after_audit`,
por sua vez, pertence aos sete overrides registrados na elegibilidade e não
deve ser somada novamente às exclusões da triagem.

Na reconstrução do fluxo, 22 desses registros foram retirados antes da
triagem por identidade DOI/URL, preservando o estágio mais avançado quando os
registros redundantes estavam em etapas diferentes. Assim, as exclusões de
triagem efetivamente contadas no PRISMA são **9.391**, distribuídas em 4.313
por `abstract_too_short`, 2.856 por `inclusion_criteria_not_met`, 2.075 por
`no_methodology`, 103 por `non_research` e 42 por `off_topic`. Na elegibilidade,
cinco registros `low_relevance_score` são excedentes de identidade; por isso,
o fluxo conta **2.470** exclusões nessa etapa, mantendo os sete
`manual_exclusion_after_audit` dentro das exclusões já persistidas.

## 2. Fluxo PRISMA a relatar

Para evitar ambiguidade entre registros que entram em uma etapa e registros excluídos nessa etapa, o fluxo deve ser apresentado com entradas, exclusões e remanescentes:

| Etapa | Entraram | Excluídos | Avançaram |
|---|---:|---:|---:|
| Identificação | 11.904 | 27 por DOI/URL | 11.877 |
| Triagem | 11.877 | 9.391 | 2.486 |
| Elegibilidade | 2.486 | 2.470 | **16** |
| Inclusão | 16 | — | **16** |

As verificações aritméticas são:

```text
11.904 - 27 = 11.877
11.877 - 9.391 = 2.486
2.486 - 2.470 = 16
16 / 11.904 = aproximadamente 0,13%
```

O comando `check-exports` pode apresentar grupos repetidos ao inspecionar o
banco bruto, porque essa checagem lista o DOI armazenado literalmente. A
auditoria do fluxo normaliza caixa, prefixos, resolutores e pontuação terminal
do DOI; também considera URL exata como chave independente e remove a união das identidades.
Assim, a diferença entre a listagem literal do banco e os 25 grupos DOI da
auditoria não é uma segunda contagem de remoções: o número que entra no PRISMA
é a auditoria normalizada, com 27 linhas removidas no total, e o CSV analítico
fica sem identidades DOI repetidas.

### Percentuais do fluxo

| Relação | Percentual |
|---|---:|
| Excluídos na triagem / identificação | 78,89% |
| Avançaram da triagem / identificação | 20,88% |
| Excluídos na elegibilidade / elegibilidade | 99,36% |
| Incluídos / elegibilidade | 0,64% |
| Incluídos / identificação | 0,13% |

Esses percentuais usam o denominador indicado em cada linha. Não se deve
calcular a taxa de duplicatas atual como `0/11.904`: zero é apenas a quantidade
de flags persistidas; a reconstrução determinística remove 27 registros por
identidade DOI/URL e conserva a auditoria separada dos títulos repetidos.

O valor `9.413` é a quantidade excluída na triagem, e `2.475` é a quantidade excluída na elegibilidade. Eles não devem ser apresentados isoladamente como se fossem o total que entrou em cada etapa.

## 3. Estudos incluídos

O conjunto atual confirmado pelo banco é:

```text
1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
6916, 6917, 6918, 6920, 6921, 6923
```

Os dez primeiros registros pertencem ao conjunto bibliográfico já consolidado. Os seis registros com IDs 6916, 6917, 6918, 6920, 6921 e 6923 foram incorporados no snapshot atualizado.

O número 16 é o total de registros retidos operacionalmente. Para a interpretação científica, o arquivo `research/data/current_synthesis_scope.csv` separa 15 registros classificados provisoriamente como empíricos, candidatos à síntese de evidências e ao MMAT, do ID 6921, um protocolo/proposta retido apenas para mapeamento contextual e rastreabilidade. O protocolo não sustenta afirmações empíricas nem uma apreciação MMAT empírica. O registro 6918 permanece dentro desse total operacional, mas está retido em *hold*: a fonte oficial da ETH confirma o título e o DOI e informa publicação em 2014, em conflito com o ano 2025 armazenado no snapshot. Até a adjudicação dessa discrepância, 6918 não sustenta uma conclusão empírica final dependente do período 2015--2026.

## 4. Diferença em relação ao baseline histórico

O baseline histórico usado nos documentos anteriores era:

| Métrica | Baseline histórico | Baseline atual |
|---|---:|---:|
| Registros identificados | 9.431 | 11.904 |
| Duplicatas removidas na etapa histórica | 2.517 | 27 por DOI/URL no fluxo reconstruído |
| Registros no snapshot após a etapa de consolidação | 6.914 | 11.877 |
| Registros que avançaram à elegibilidade | 1.883 | 2.486 |
| Registros incluídos no snapshot operacional | 17 | **16** |
| Estudos empíricos provisórios na síntese de evidências | 17 | **15** |
| Protocolo/proposta retido para contexto | 0 | **1** |

Há uma pendência específica na coluna histórica: os documentos legados usam 2.517 duplicatas removidas, enquanto o único registro histórico preservado em `searches.results_summary` no SQLite registra `total_removed=2494` (e implicaria 6.937 registros após a consolidação). O baseline atual não depende desse valor histórico; a divergência deve ser resolvida a partir do artefato arquivado da execução original antes de qualquer afirmação definitiva sobre a deduplicação histórica.

Há uma evidência adicional importante nessa comparação: o `papers.csv` legado
preservado no Git contém **6.914 linhas**, não 9.431. Nesse arquivo, os DOIs
não se repetem e as etapas persistidas somam 6.914 (5.031 em triagem, 1.866
em elegibilidade e 17 incluídos). Isso mostra que ele representa uma saída já
consolidada, mas não preserva o ledger dos pares removidos nem a execução que
produziu a consolidação. Portanto, `9.431 - 6.914 = 2.517` é uma diferença
aritmética compatível com o relato histórico, não uma confirmação independente
de 2.517 decisões de deduplicação. O `2494` do resumo histórico do SQLite
também não pode ser usado para reconstruir esses pares. Para o snapshot atual,
somente as 27 remoções por identidade DOI/URL possuem auditoria linha a linha;
os 232 excedentes apenas por título continuam pendentes de disposição semântica.

A execução histórica tinha 17 estudos incluídos. Em uma nova rodada, foram identificados 23 candidatos e registrados 7 overrides manuais, chegando aos 16 registros retidos atualmente, dos quais 15 são classificados provisoriamente como empíricos — incluindo o 6918, que permanece em hold por conflito temporal — e um é o protocolo/proposta contextual 6921. Portanto, a diferença não deve ser descrita como uma simples subtração de três registros: o snapshot atual também foi consolidado com nova contagem de ingestão e com o pipeline de scoring corrigido. No snapshot vigente, os sete overrides estão registrados pelos IDs de banco **14, 15, 6915, 6919, 6922, 6925 e 6926**, conforme a tabela abaixo. As chaves bibliográficas históricas do PTC são uma linhagem documental separada e não devem ser mapeadas automaticamente para esses sete overrides.

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

Como a lógica determinística de inclusão pelo score ainda selecionaria esses 23 candidatos sem o override, o manifesto versionado registra os sete overrides e os campos necessários para reencontrar cada linha. O arquivo `research/data/manual_override_adjudication.csv` acrescenta evidência do abstract, fonte consultada, avaliação de escopo e ação necessária para cada caso. Ele não transforma uma hipótese em justificativa final: quatro casos (14, 6915, 6919 e 6925) exigem recuperação/inspeção da fonte primária e adjudicação de escopo, enquanto três permanecem com proposta de razão sujeita ao supervisor. Assim, os 16 registros atuais são a composição auditada do snapshot, e não o resultado de uma regra automática suficiente, isoladamente, para reproduzir os sete descartes.

## 5. Correções do pipeline

As correções preservadas no código são:

- uso de `\bai\b` para evitar falsos positivos por substring, como em `aims` e `training`;
- remoção de `assessment` como termo amplo do grupo de *Learning Analytics*;
- deduplicação determinística por DOI/URL normalizados durante a exportação do fluxo, mesmo quando a flag persistida está zerada; títulos repetidos permanecem candidatos;
- seleção dos estudos incluídos diretamente pelo estado persistido no banco.

## 6. Bibliografia e MMAT

Os arquivos `results/tcc/referencias.bib` e `results/tcc/referencias_pedagogicas.bib`, carregados conjuntamente pelo `main.tex`, mantêm os 16 registros atuais e as referências metodológicas, pedagógicas, de avaliação e técnicas. O export `research/exports/references/included_papers.bib` contém somente os 16 registros derivados do pipeline; o escopo explícito identifica 15 candidatos provisórios à síntese empírica, com o 6918 em hold temporal, e 6921 como contextual.

A atualização do conjunto incluído tornou obsoleta a tabela MMAT histórica de 17 estudos. A reaplicação vigente foi registrada em um ledger independente dos 16 registros: foram registrados julgamentos por critério, justificativas e localizadores para nove textos primários revisados externamente; cinco estudos permanecem em nível de abstract/metadados, um está em hold por conflito de ano e recuperação do texto primário (ID 6918), e o protocolo/proposta 6921 foi marcado como não aplicável ao MMAT empírico nesta etapa. Uma verificação externa também corroborou a existência bibliográfica e o ano de 2025 do ID 6923, embora seu texto integral não tenha sido recuperado. Isso é uma reavaliação documental preliminar, não um score final nem uma conclusão comparativa de qualidade.

Para manter essa reaplicação separada do histórico, o repositório agora
mantém quatro artefatos separados: `research/data/mmat_current_study_registry.csv`
contém exatamente os 16 registros atuais; `research/data/mmat_primary_sources_manifest.csv`
registra a fonte primária, o estado de acesso e as pendências de verificação;
`research/data/mmat_reassessment_current.csv` registra S1, S2 e Q1--Q5 por
estudo, além de uma nota de evidência para cada critério; e
`research/data/current_synthesis_scope.csv` explicita a separação entre evidência
empírica e o protocolo contextual. O ledger atual possui
9 estudos com texto primário revisado externamente, 5 com abstract/metadados,
1 em hold por conflito de fonte e 1 protocolo/proposta sem resultado empírico,
marcado como não aplicável ao MMAT empírico. Enquanto não houver texto
primário verificável para todos, localizadores suficientes e adjudicação pelo
supervisor, as respostas preliminares — inclusive as que já são `Y` ou `N` —
não são uma avaliação MMAT final, não geram score e não sustentam ranking de
qualidade.

## 7. Artefatos e próxima consolidação

Os artefatos derivados do banco foram regenerados a partir do mesmo snapshot, incluindo `summary.json`, `summary_report.html`, `papers_report_included.html`, `included_papers.bib` e as visualizações. O manuscrito canônico é `results/tcc/main.tex`, que inclui os arquivos em `results/tcc/conteudo/`. O histórico `9.431/2.494` foi mantido apenas como contexto e é ignorado pelo cálculo atual quando não fecha com as 11.904 linhas brutas e as 11.877 linhas após a deduplicação determinística.

## 8. Reprodutibilidade sem versionar o SQLite

O SQLite é necessário como fonte operacional local para consultas, estados e
contagens, mas não é distribuído no repositório por ser um artefato grande e
mutável. A representação versionada do snapshot é composta por:

- `papers.csv` e `papers.json`, com os registros e estados usados na auditoria;
- `summary.json`, com o fluxo PRISMA e as estatísticas derivadas;
- `included_papers.bib`, com somente os 16 registros retidos pelo pipeline
  (15 empíricos e o protocolo contextual 6921);
- `reference_audit.csv` e os dois arquivos bibliográficos carregados pelo TCC,
  `results/tcc/referencias.bib` e `results/tcc/referencias_pedagogicas.bib`, que
  mantêm separadas as decisões bibliográficas dos estudos e as referências
  teóricas/metodológicas;
- `mmat_current_study_registry.csv`, `mmat_primary_sources_manifest.csv` e
  `mmat_reassessment_current.csv`, que separam a reavaliação vigente da tabela
  MMAT histórica de 17 estudos;
- `manual_override_adjudication.csv`, que registra a evidência disponível e a
  ação necessária para cada uma das sete exclusões manuais;
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

## Relação com a apresentação histórica do PTC

O arquivo `results/ptc/presentation/ensino_personalizado_de_matematica.pptx`
foi mantido como material histórico de comunicação e foi auditado por suas
imagens incorporadas (26 slides e 28 mídias). Ele continua útil para a
narrativa do problema, do diagnóstico personalizado e das lacunas de
personalização, mas não é fonte de contagens vigentes. Em particular, os
percentuais calculados sobre os 17 estudos e as alegações agregadas de
acurácia, ganhos de 10--20% ou viés de publicação não foram transpostos para
o TCC ou para o Slidev atual: o corpus mudou, as métricas são heterogêneas e
essas afirmações não são reproduzidas pelo snapshot versionado. O Slidev
reconciliado usa as imagens atuais do pipeline e apresenta somente métricas
que podem ser ligadas ao `summary.json`, preservando as limitações e o estado
preliminar do MMAT.

Antes do commit final, devem ser verificados:

1. ausência dos números históricos no texto atual do TCC, salvo quando explicitamente marcados como histórico;
2. presença exclusiva das 16 chaves atuais entre os estudos incluídos;
3. correspondência entre o banco, os exports e a bibliografia, incluindo a decisão documentada sobre os DOIs repetidos;
4. confirmação das fontes, dos localizadores e da adjudicação final do MMAT preliminar já registrado;
5. compilação do TCC e inspeção do PDF atualizado.
