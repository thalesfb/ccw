# Revisão dirigida de afirmações pedagógicas

## Alcance

Esta revisão registra as decisões de redação relativas ao foco da especificação e à distinção entre desempenho e aprendizagem. Não certifica todas as afirmações do TCC, não conclui a apreciação MMAT e não modifica o corpus empírico. A existência de uma referência e a adequação de uma afirmação ao texto dessa referência são verificações diferentes.

## Fontes consultadas e limites

| Afirmação ou decisão | Fonte e localizador | Resultado e limite de uso |
|---|---|---|
| Letramento matemático inclui raciocinar, representar, comunicar, argumentar e resolver problemas. | BNCC, seção Matemática do Ensino Fundamental, p. 266 impressa (página física 268 do PDF); [documento oficial do MEC](https://basenacionalcomum.mec.gov.br/images/BNCC_EI_EF_110518_versaofinal_site.pdf). Texto e página renderizada conferidos em 7 de outubro de 2026. | Sustenta a descrição curricular. Não demonstra que uma ferramenta computacional desenvolve essas capacidades. |
| Competência envolve mobilização de conhecimentos, habilidades, atitudes e valores. | BNCC, Introdução, p. 8 impressa (página física 10 do mesmo PDF), definição de competência; texto e página conferidos. | Sustenta a definição adotada. A decisão de não reduzir competência a um resultado isolado é apresentada como cuidado interpretativo deste trabalho. |
| Conhecimento do estudante e observação de sua atuação não são equivalentes; avaliação exige inferência e envolve incerteza. | NRC (2001), capítulo 2, *Precision and Imprecision in Assessment* e *Assessment as a Process of Reasoning from Evidence*, pp. 42–44; [texto integral na editora](https://www.nationalacademies.org/read/10019/chapter/4). Consulta em 7 de outubro de 2026. | Sustenta o limite entre observação e inferência. Não fornece resultado experimental do protótipo nem prova eficácia de uma intervenção. |
| Aprendizagem é delimitada operacionalmente como mudanças no que o estudante sabe e consegue fazer ao longo do tempo. | Definição operacional explicitada no TCC; NRC fundamenta o limite inferencial, não é apresentado como autor dessa formulação literal. | Escolha de delimitação, não tese transferida de Piaget a outro autor. A exigência de acompanhamento é uma condição proposta para avaliação futura, ainda não executada. |
| ZDP, aprendizagem significativa, scaffolding, avaliação formativa e feedback orientam aspectos diferentes dos requisitos. | Vygotsky (1978), Ausubel (1968), Wood, Bruner e Ross (1976), Black e Wiliam (1998), Hattie e Timperley (2007), conforme o ledger bibliográfico. | Atribuições preservadas, sem novos localizadores inventados. Esta etapa não incluiu nova conferência integral de todas essas obras. A edição de Vygotsky e a rastreabilidade das demais passagens continuam sujeitas à auditoria. |

## Consequências para a redação

O PDF da BNCC consultado possui 600 páginas e SHA-256 `ad623d7b33986a4e87e1441a4e675064cd30db3650b86a75caefa476e802272b`. A numeração impressa foi distinguida da posição física no arquivo. O texto do NRC foi conferido no leitor integral da editora, sem atribuir a essa consulta um hash de PDF não obtido.

A pergunta e o objetivo geral foram centrados na proposição de uma especificação técnica e pedagógica para apoiar a interpretação docente de evidências de desempenho. Os quatro objetivos específicos distinguem categorização da literatura, identificação de limitações e lacunas, formulação da especificação e proposição do protocolo. A revisão sistemática e o pipeline permanecem meios metodológicos e contribuições documentais.

O atendimento ao objetivo de propor o protocolo corresponde à definição de procedimentos, não à realização de experimentos. A conclusão preserva a ausência de validação empírica educacional própria e a condição preliminar da síntese e do MMAT.

Piaget foi retirado da redação ativa por delimitação editorial. Sua proveniência bibliográfica foi preservada como não utilizada; a decisão não declara incompatibilidade universal entre teorias. As contribuições pedagógicas remanescentes foram organizadas em prosa, distinguindo conceitos atribuídos aos autores de requisitos propostos neste trabalho.

## Esclarecimentos técnicos delimitados

A revisão editorial explica termos no contexto em que são usados, sem transformar
uma definição de algoritmo ou métrica em evidência de eficácia educacional.
As definições de famílias de modelos se apoiam em James et al. (2021), capítulos
4 e 8--10. A distinção entre discriminação ROC e calibração preserva as fontes
metodológicas Fawcett (2006) e Niculescu-Mizil e Caruana (2005).

Foram conferidos, em 7 de outubro de 2026, a [documentação oficial de métricas
do scikit-learn 1.6](https://scikit-learn.org/1.6/modules/model_evaluation.html),
seções 3.4.4.5, 3.4.4.6 e 3.4.4.9; a [documentação oficial do JRip no Weka](https://weka.sourceforge.io/doc.dev/weka/classifiers/rules/JRip.html);
o resumo e a seção 3 do [artigo primário de Lafferty, McCallum e Pereira](https://www.cis.upenn.edu/~danroth/Teaching/CS598-05/Papers/crf.pdf);
e as etapas 3--8 do [procedimento oficial Jigsaw Classroom](https://www.jigsaw.org/).
As páginas de documentação e procedimento são identificadas em notas no
manuscrito. Elas esclarecem termos, não certificam a implementação ou a
fidelidade metodológica de cada artigo retido. O artigo sobre CRF foi acrescentado
somente como fundamento técnico, sem alterar o corpus da revisão.

## Verificação ainda necessária

A revisão global deve conferir cada afirmação central contra o texto primário, registrar localizadores e restrições de uso e verificar a derivação de cada requisito. Testes de estrutura documental e uma compilação bem-sucedida não substituem essa verificação científica.
