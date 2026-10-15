# Estado atual e limites da versão do TCC

**Atualização:** 14 de outubro de 2026

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

O recorte da busca tem data de corte em 31 de agosto de 2026. O fluxo registra
11.904 registros identificados, 11.877 após remoções determinísticas e 2.486
submetidos à priorização operacional; 2.468 não avançaram dessa etapa e 18
registros formaram a lista preliminar. Um registro foi excluído após resumo; dos 17
relatórios procurados, um não foi recuperado e 16 foram avaliados em texto
completo. Um foi excluído após essa avaliação por ser protocolo sem resultados
concluídos. Os 15 restantes formam provisoriamente o núcleo empírico, sujeitos
à adjudicação pendente do estudo 8. Os textos integrais dos estudos 1, 5 e 10
foram consultados e seus papéis foram delimitados como predição/avaliação
matemática (1 e 10) e proposta de personalização (5). A priorização operacional
não equivale à elegibilidade.

O único texto integral ainda não recuperado é a dissertação de
[Zeng (2025), registro 6923](https://doi.org/10.7916/2q6y-bm58). Consulta ao
Columbia Academic Commons registrada no manifesto de fontes em 13 de outubro de
2026 informou que os arquivos estarão disponíveis a partir de 16 de maio de
2027. O resumo público não substitui o texto primário: a elegibilidade e a
apreciação MMAT desse registro permanecem pendentes, sem alteração das contagens
PRISMA.

O manifesto distingue as datas de referência: a busca tem corte em 31 de agosto
de 2026, a adjudicação inicial do escopo ocorreu em 3 de setembro e a
reconciliação do escopo foi atualizada em 14 de outubro de 2026. O arquivo foi
gerado novamente nessa última data e preserva verificadores de integridade dos
artefatos versionados; a atualização não representa nova consulta às APIs nem
altera o corte temporal da busca.

O registro de avaliação MMAT 2018 preserva S1 e S2 como perguntas de triagem e Q1--Q5 como
critérios específicos do delineamento. Dos 15 registros empíricos mantidos
provisoriamente, 14 têm apreciação MMAT preliminar. O estudo 8 permanece no
fluxo PRISMA e no núcleo provisório, sem respostas MMAT até adjudicar sua
elegibilidade e unidade de apreciação; suas bases distintas não devem ser
somadas. O registro 6923 sem texto integral também não recebeu apreciação; suas
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

As próximas decisões relevantes são: confirmar se o trabalho permanecerá como
revisão sistemática acompanhada de especificação conceitual ou se incluirá um
estudo computacional exploratório separado; aprovar, caso aplicável, a fonte
de dados, seus termos de uso, o desfecho `correct_next`, os limiares mínimos e
o protocolo de divisão; concluir a recuperação das fontes primárias e a
adjudicação humana do MMAT; e decidir se haverá execução experimental própria.

A apresentação de defesa canônica é `presentation/slides.md`, compilada com
Slidev em 25 slides. O PPTX editável em
`results/tcc/presentation/ensino_personalizado_de_matematica_tcc.pptx` contém
19 slides e é uma exportação paralela, gerada por outro script; não é o deck
Slidev nem permanece sincronizada com ele. O material em
`results/ptc/presentation/` corresponde à apresentação histórica do PTC, não à
defesa do TCC.

Também permanece pendente uma matriz de rastreabilidade que associe cada
requisito da especificação aos estudos e artefatos que o fundamentam. Até que
essa matriz seja concluída, a ligação entre literatura e requisitos deve ser
apresentada como derivação temática documentada, não como cobertura exaustiva
de cada requisito por uma fonte individual.

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
sintéticos verdes, experimento real pendente e MMAT preliminar**. A
apresentação e o manuscrito devem comunicar esse limite sem transformar
resultados operacionais em evidência de eficácia educacional.
