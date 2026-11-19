# Estado atual e limites da versão do TCC

**Atualização documental:** 14 de novembro de 2026

Este registro público descreve o estado verificável da versão atual do
Trabalho de Conclusão de Curso e separa resultados produzidos, validações
técnicas e decisões metodológicas ainda pendentes. Ele é uma nota de
transparência do repositório; não substitui o texto do TCC, o protocolo da
revisão, a supervisão acadêmica ou qualquer aprovação necessária para uma
execução experimental.

Os critérios gerais para separar relato acadêmico, proveniência técnica e
fluxo de desenvolvimento estão em
[`PUBLICATION_GOVERNANCE.md`](PUBLICATION_GOVERNANCE.md).

## Revisão sistemática e MMAT

<!-- ccw-sync:start snapshot -->
Corte da busca: 31/08/2026; adjudicação inicial: 03/09/2026; reconciliação do escopo: 20/10/2026; reconciliação de identidade e ano: 31/10/2026; cobertura documental registrada: 20/10/2026; PDFs locais conferidos por hash: 29/10/2026.

O snapshot registra 11.904 registros identificados e 29 duplicatas removidas: 27 por identidade DOI/URL e 2 relatórios confirmados manualmente como repetidos. Foram 11.875 registros únicos na triagem, dos quais 9.393 foram excluídos (79,10%). 2.482 avançaram à priorização histórica (20,90% da triagem); 2.464 não avançaram sob a regra histórica (99,27%). O corte 4,0 permanece inalterado e o relato descreve o conjunto adotado nesta versão. A priorização histórica encaminhou 18 registros à lista preliminar (0,73%), não a inclusões finais: 15 estudos empíricos mantidos na seleção histórica, dos quais 14 têm relatório recuperado; Sokkhey permanece sem cópia verificável, como inclusão histórica. Houve 1 exclusão após resumo. Dos 17 relatórios procurados, 2 não foram recuperados (Sokkhey (2020) e Zeng (2025)); 15 foram avaliados em texto completo, incluindo 1 protocolo excluído. Nas 14 avaliações MMAT dos estudos com texto recuperado, S1 recebeu 14 Y e S2 recebeu 13 Y e 1 CT; o autor conferiu essas respostas. Sokkhey mantém respostas históricas não revalidadas por falta de cópia verificável. Nos três estudos de métodos mistos, o autor não conferiu separadamente as respostas dos componentes qualitativo e quantitativo; elas permanecem identificadas como assistidas por IA. Não há escore agregado.
<!-- ccw-sync:end snapshot -->

<!-- ccw-sync:start coverage -->
Na conferência de 29/10/2026, havia **16 PDFs locais para 18 registros candidatos**, identificados por hash. Esse total inclui os 14 textos empíricos recuperados entre os 15 estudos da seleção histórica, 1 registro mantido apenas para contexto após a triagem do resumo e 1 protocolo excluído na avaliação de texto integral. Sokkhey (2020), registro 3, permanece na seleção histórica sem cópia verificável; Zeng (2025), registro 6923, também não foi recuperado e está fora da seleção. Assim, os 16 PDFs locais não correspondem a 16 estudos incluídos nem alteram o fluxo PRISMA. A disponibilidade não comprova que todos os elementos visuais e apêndices foram examinados integralmente. O replay textual congelado de 14/10/2026 abrange **12 fontes e 484 trechos**, não os 16 PDFs registrados na conferência de 29/10/2026. As fontes suplementares não foram incorporadas a esse replay. A tabela delimita as páginas com texto e os elementos visuais registrados para cada fonte.
<!-- ccw-sync:end coverage -->

O relatório não recuperado no fluxo histórico é a dissertação de
[Zeng (2025), registro 6923](https://doi.org/10.7916/2q6y-bm58). Consulta ao
Columbia Academic Commons registrada no manifesto de fontes em 13 de outubro de
2026 informou que os arquivos estarão disponíveis a partir de 16 de maio de
2027. O resumo público não substitui o texto primário: Zeng está fora da seleção
histórica de 15 estudos e não recebeu apreciação MMAT, sem alteração das
contagens PRISMA. O registro 3, [Multimodels2020_002](https://doi.org/10.5573/IEIESPC.2020.9.3.217),
também está sem cópia integral local: o acesso disponível levou à compra do
artigo, sem recuperação por via autorizada. Seus julgamentos históricos não
foram revalidados nesta rodada. Não se infere, da ausência local atual, que
nenhuma consulta histórica tenha ocorrido.

O manifesto distingue as datas de referência: a busca tem corte em 31 de agosto
de 2026, a adjudicação inicial do escopo ocorreu em 3 de setembro e a
reconciliação do escopo foi atualizada em 20 de outubro de 2026. O arquivo foi
regenerado para esta revisão e preserva verificadores de integridade dos
artefatos versionados; a atualização não representa nova consulta às APIs nem
altera o corte temporal da busca.

O registro MMAT 2018 apresenta S1/S2 e os critérios Q1–Q5 por estudo, sem
escore agregado. Dos 15 estudos empíricos da seleção histórica, 14 têm texto
recuperado e respostas atuais; Sokkhey permanece sem cópia verificável e suas
respostas históricas não foram revalidadas. O estudo 14 usa a categoria 3
quantitativa não randomizada: o artigo se declara quase-experimental sem
atribuição aleatória (§2.2 e §2.7), embora mencione sorteio das escolas em §2.4.
Os estudos 5 e 7 usam uma rota operacional da categoria 3; o estudo 8 usa uma
adaptação da categoria 4 à modelagem computacional. A unidade do estudo 8 é uma
tese/um relatório com componentes matemáticos, sem duplicar frações reutilizadas.
O registro 6923 não recebeu apreciação MMAT, e o protocolo 6921 está fora do
denominador. Em 13/11/2026, o autor conferiu as respostas dos 14 estudos com
texto recuperado contra as evidências localizadas; os componentes dos estudos
mistos não integraram essa conferência e permanecem identificados como assistidos
por IA. A apreciação não gera escore agregado, ranking ou conclusão de eficácia.

## Implementação e escopo experimental

O diretório `prototype/` contém um pipeline implementado para ingestão
manifestada, normalização do ASSISTments, construção de atributos sem
vazamento, separação temporal e por estudante, modelos candidatos, métricas e
bootstrap agrupado por estudante. A suíte local passa com 44 testes, o que
valida o comportamento do código e dos guardrails sintéticos. Isso não
constitui treinamento com dados reais, avaliação de eficácia pedagógica,
participação de estudantes ou validação em escola.

Os limiares mínimos de tamanho da fonte e do conjunto de teste ainda não
foram congelados. Qualquer execução com dados reais depende de uma decisão
metodológica explícita sobre fonte, licença, unidade de análise, desfecho,
divisão dos dados e critérios de avaliação.

## Seleção adotada e limites metodológicos

Esta versão relata a seleção realizada sob o corte de relevância 4,0,
os critérios aplicados e o conjunto histórico de 15 estudos. Não houve
alteração da regra, nova seleção ou incorporação de estudos adicionais. Ver
[`REVISAO-LIMIAR-SELECAO-2026-10-31.md`](REVISAO-LIMIAR-SELECAO-2026-10-31.md),
que documenta o estado da seleção e as limitações do escore utilizado.

O corte 4,0 e a seleção histórica são mantidos nesta versão; não houve nova
seleção.
O valor 4,0 é um corte
da soma ponderada aplicada aos metadados e resumos: a escala nominal é 0–10,
enquanto os valores preservados vão de 0–4,5. O protocolo e o código registram
o limiar, mas não uma calibração empírica ou justificativa para a escolha
exata desse número. O valor não é percentual de aderência ou nota de qualidade.

O escopo desta entrega foi confirmado como revisão crítica da literatura e
especificação conceitual, sem exigir treinamento ou validação educacional do
protótipo. A conferência das respostas MMAT para 14 fontes recuperadas e das rotas
operacionais está registrada com seus limites; Sokkhey permanece sem fonte
verificável, e Zeng está fora da seleção. A cobertura dos filtros automatizados
continua sendo uma limitação do levantamento. Uma execução
computacional futura dependerá de decisão e protocolo próprios, incluindo
fonte, termos de uso, desfecho, limiares e divisão dos dados.

A apresentação de defesa canônica é `presentation/slides.md`, compilada com
Slidev em 24 slides. O PPTX editável em
`results/tcc/presentation/ensino_personalizado_de_matematica_tcc.pptx` contém
19 slides e é uma exportação paralela, gerada por outro script; não é o deck
Slidev nem é exportado automaticamente dele. Seus resumos devem ser conferidos
quando o conteúdo canônico mudar, conforme o
[contrato de sincronização](DOCUMENTATION_SYNC.md). O material em
`results/ptc/presentation/` corresponde à apresentação histórica do PTC, não à
defesa do TCC.

O capítulo da especificação passou a incluir um quadro de rastreabilidade
com 26 grupos de requisitos, distinguindo observações dos estudos, fundamentos
teóricos ou normativos e decisões autorais. Os vínculos e limites declarados
não equivalem a validação do artefato nem a conferência independente integral
das referências. Os filtros de resumo curto/ausente e termos metodológicos
também passaram a ser descritos com contagens e limitações no manuscrito;
reproduzir essas contagens não comprova recuperação exaustiva da literatura.

## Execução experimental e computação externa

A execução experimental do protótipo permanece condicionada à decisão da
orientação e à definição de um protocolo próprio. O Google Colab foi registrado
somente como alternativa tecnológica futura; não foi utilizado nesta versão e
nenhum benefício de conta ou disponibilidade de acelerador foi presumido. Esta
versão não relata treinamento em dados reais, validação experimental nem efeito
pedagógico do protótipo. Qualquer estudo futuro requer aprovação metodológica,
governança dos dados e registro reprodutível de procedimentos e resultados.

## Limite interpretativo da versão

O estado atual pode ser resumido como **código implementado, testes
sintéticos verdes, entrega documental, experimento futuro fora do escopo e
apreciação MMAT por critério, sem escore agregado**. A
apresentação e o manuscrito devem comunicar esse limite sem transformar
resultados operacionais em evidência de eficácia educacional.
