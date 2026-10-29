# Estado atual e limites da versão do TCC

**Atualização documental:** 20 de outubro de 2026

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
Corte da busca: 31/08/2026; adjudicação inicial: 03/09/2026; reconciliação do escopo: 20/10/2026; cobertura documental: 20/10/2026.

O snapshot registra 11.904 registros identificados, 27 remoções determinísticas por DOI/URL e 11.877 registros na triagem. Foram 2.486 submetidos à priorização operacional; 2.468 não avançaram dessa etapa. A priorização encaminhou 18 candidatos, não 18 inclusões finais: 15 estudos empíricos mantidos provisoriamente, 1 exclusão após resumo, 1 relatório não recuperado no fluxo histórico e 1 protocolo excluído após texto completo. No MMAT preliminar, há 15 triagens S1/S2 e 15 apreciações por categoria; não há escore agregado nem aprovação científica final.
<!-- ccw-sync:end snapshot -->

<!-- ccw-sync:start coverage -->
Em 29/10/2026, há **16 de 18 PDFs locais** identificados por hash; faltam os registros **3 e 6923**. Essa disponibilidade não altera retroativamente as etapas PRISMA nem comprova leitura humana integral. O replay textual congelado de 14/10/2026 abrange **12 fontes e 484 trechos**, não os 16 PDFs atuais. As fontes suplementares não foram incorporadas a esse replay. A leitura documental assistida e a revisão científica humana são estados distintos.
<!-- ccw-sync:end coverage -->

O relatório não recuperado no fluxo histórico é a dissertação de
[Zeng (2025), registro 6923](https://doi.org/10.7916/2q6y-bm58). Consulta ao
Columbia Academic Commons registrada no manifesto de fontes em 13 de outubro de
2026 informou que os arquivos estarão disponíveis a partir de 16 de maio de
2027. O resumo público não substitui o texto primário: a elegibilidade e a
apreciação MMAT desse registro permanecem pendentes, sem alteração das contagens
PRISMA. O registro 3, [Multimodels2020_002](https://doi.org/10.5573/IEIESPC.2020.9.3.217),
também está sem cópia integral local: o acesso disponível levou à compra do
artigo, sem recuperação por via autorizada. Seus julgamentos históricos não
foram revalidados nesta rodada. Não se infere, da ausência local atual, que
nenhuma consulta histórica tenha ocorrido.

O manifesto distingue as datas de referência: a busca tem corte em 31 de agosto
de 2026, a adjudicação inicial do escopo ocorreu em 3 de setembro e a
reconciliação do escopo foi atualizada em 14 de outubro de 2026. O arquivo foi
regenerado para esta revisão e preserva verificadores de integridade dos
artefatos versionados; a atualização não representa nova consulta às APIs nem
altera o corte temporal da busca.

O registro de avaliação MMAT 2018 preserva S1 e S2 como perguntas de triagem e Q1--Q5 como
critérios específicos do delineamento. Dos 15 registros empíricos mantidos
provisoriamente, 15 têm triagem S1/S2 e apreciação dos critérios. As categorias 3 dos estudos 5 e 7 são rotas operacionais com alocação desconhecida; a categoria 2 do 14 segue o sorteio declarado, mas contraditório; e a categoria 4 do 8 é adaptação à modelagem computacional. A unidade do 8 é uma tese/um relatório com componentes matemáticos, sem duplicar frações reutilizadas. O registro 6923 sem texto integral também não recebeu apreciação; suas
células permanecem sem resposta, não como CT. O registro
excluído após resumo e o protocolo sem resultados concluídos estão fora do
denominador MMAT. Como a avaliação foi conduzida por um único revisor e a
adjudicação humana independente permanece pendente, o MMAT é preliminar e por
critério. Não há escore agregado, ranking ou conclusão de eficácia.

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

## Decisões metodológicas pendentes

O escopo desta entrega foi confirmado como revisão crítica da literatura e
especificação conceitual, sem exigir treinamento ou validação educacional do
protótipo. Permanecem a conferência dos julgamentos e das rotas operacionais, sem tratá-las como delineamentos confirmados; a eventual
recuperação dos registros 3 e 6923 por via legítima; e a avaliação do
impacto dos filtros automatizados sobre a cobertura da revisão. Uma execução
computacional futura dependerá de decisão e protocolo próprios, incluindo
fonte, termos de uso, desfecho, limiares e divisão dos dados.

A apresentação de defesa canônica é `presentation/slides.md`, compilada com
Slidev em 25 slides. O PPTX editável em
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
sintéticos verdes, entrega documental, experimento futuro fora do escopo e MMAT preliminar**. A
apresentação e o manuscrito devem comunicar esse limite sem transformar
resultados operacionais em evidência de eficácia educacional.
