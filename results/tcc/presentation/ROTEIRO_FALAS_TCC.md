# Roteiro de falas — apresentação do TCC

Tempo sugerido: aproximadamente 18–20 minutos, deixando espaço para perguntas.
O texto é um guia oral; a redação científica completa permanece em
`results/tcc/`.

## 1. Capa — 0:30

Este trabalho investiga o uso de técnicas computacionais no ensino de
matemática. O resultado não é apresentado como uma solução pronta: ele combina
uma revisão sistemática da literatura com uma especificação conceitual de
protótipo para apoiar a interpretação docente.

## 2. O problema — 1:00

O ponto de partida são as turmas heterogêneas. Estudantes chegam com
conhecimentos prévios, ritmos e dificuldades diferentes, e o professor precisa
interpretar muitas evidências em tempo limitado. Técnicas computacionais podem
ajudar a organizar esses registros. Isso não significa que o modelo conheça
sozinho a aprendizagem do estudante ou que possa substituir a decisão
pedagógica.

## 3. Questão e objetivo — 1:00

A pergunta é como identificar e sintetizar as principais técnicas aplicadas ao
ensino de matemática e converter as evidências em uma especificação que apoie o
professor. O objetivo geral une essas duas frentes: mapear a literatura e
derivar uma proposta técnica e pedagógica coerente com seus achados e limites.

## 4. Objetivos específicos — 0:50

Os objetivos percorrem todo o ciclo do trabalho: realizar a revisão, categorizar
técnicas e finalidades, analisar limitações, mapear lacunas, manter o pipeline
auditável e derivar requisitos, critérios de dados e modelos, protocolo de
avaliação e arquitetura. Implementação funcional e validação com participantes
não fazem parte do escopo executado.

## 5. Fundamentação — 1:10

Uma distinção importante organiza a leitura: desempenho observado é o registro
de uma tarefa; proficiência estimada é uma inferência em uma escala; competência
envolve mobilizar conhecimentos e estratégias; aprendizagem é uma transformação
ao longo do tempo. Esses conceitos se relacionam, mas não são equivalentes. Uma
saída computacional deve, portanto, ser interpretada como evidência parcial e
contextualizada pelo professor.

## 6. Método — 1:10

O PRISMA 2020 foi usado como diretriz de relato, e os critérios foram
organizados com apoio do PICOS. A busca utilizou Semantic Scholar, OpenAlex,
Crossref e CORE, com inglês e português no período de 2015 a 2026. A estratégia
canônica contém 72 combinações de termos, 48 em inglês e 24 em português. É
importante dizer com precisão que esse número descreve a composição versionada
da estratégia; não existe um log histórico completo que permita chamá-lo de
contagem de chamadas HTTP concluídas.

## 7. Contagens — 1:10

O snapshot começa com 11.904 registros. Foram removidas 27 linhas por identidade
bibliográfica determinística, chegando a 11.877 na triagem. A triagem excluiu
9.391 registros e encaminhou 2.486 para elegibilidade. Nessa etapa, 2.468 foram
excluídos e 18 foram retidos operacionalmente. Cada número representa uma etapa
distinta, por isso não devemos substituir o fluxo por uma única porcentagem.

## 8. PRISMA — 0:45

Esta figura é a representação visual do mesmo fluxo. Ela está versionada junto
dos artefatos de pesquisa e foi incorporada diretamente à apresentação. O
objetivo é permitir que o leitor acompanhe a transição entre identificação,
deduplicação, triagem, elegibilidade e retenção.

## 9. Deduplicação — 1:05

A deduplicação atual precisa ser lida com cuidado. As 27 remoções confirmadas
foram feitas por DOI normalizado ou URL exata: 25 e 2, respectivamente. Também
foram observados 232 excedentes apenas por título normalizado, mas eles não
foram removidos automaticamente. Títulos iguais podem indicar versões, erratas
ou obras diferentes; por isso esses registros continuam como candidatos a uma
auditoria semântica.

## 10. Panorama — 0:55

O panorama mostra as categorias observadas no conjunto após a remoção
determinística. Técnica não especificada aparece em 6.399 registros, seguida de
assessment, IA e machine learning. Essas categorias podem se sobrepor e são
descritivas. Elas não são uma contagem dos 18 retidos, não são uma nota de
qualidade e não medem eficácia.

## 11. Tempo e fontes — 0:50

As distribuições por ano e por fonte ajudam a caracterizar o snapshot. Elas
mostram como o conjunto foi recuperado, mas não permitem concluir que uma base
é mais representativa ou que a produção científica esteja distribuída de forma
uniforme. A cobertura está condicionada às fontes, aos idiomas e às condições
de disponibilidade dos metadados.

## 12. População retida — 1:05

Dos 18 registros retidos operacionalmente, 17 são candidatos empíricos
provisórios. Um registro é um protocolo ou proposta contextual e foi preservado
para rastreabilidade, não para sustentar uma conclusão empírica. Entre os
empíricos, o padrão dominante envolve predição de desempenho e estimativa de
proficiência, com uso recorrente de modelos supervisionados. Isso descreve a
literatura encontrada; não escolhe um algoritmo vencedor.

## 13. MMAT — 1:10

O MMAT 2018 foi aplicado por critério, conforme o desenho metodológico. As
respostas são mantidas como Sim, Não ou Não é possível determinar, sem produzir
uma pontuação agregada. A avaliação é preliminar e foi feita por um único
revisor. Nove registros tiveram texto primário revisado e oito dependeram de
resumo e metadados. A recuperação das fontes, os localizadores e a adjudicação
precisam ser consolidados. Portanto, não apresento um ranking de qualidade.

## 14. Interpretação dos achados — 1:00

A revisão sustenta um mapa auditável das aplicações e de suas limitações. Ao
mesmo tempo, os estudos usam populações, instrumentos, variáveis e métricas
diferentes. Isso impede comparar diretamente todas as acurácias e impede
transferir o resultado de um artigo para outra escola. Predição de desempenho
também não é sinônimo de aprendizagem.

## 15. Lacunas — 0:55

As lacunas mais relevantes estão na explicabilidade, no alinhamento curricular,
na participação docente, na análise de equidade, na reprodutibilidade e na
validação em diferentes contextos. Elas orientam decisões da especificação. Uma
lacuna não é uma prova automática de ineficácia; é um sinal de que uma solução
futura precisaria tornar essas condições explícitas e avaliáveis.

## 16. Derivação — 0:55

O trabalho conecta a revisão à fundamentação pedagógica. Das evidências e
limitações são derivadas lacunas; das lacunas são derivados requisitos; e esses
requisitos organizam critérios para dados e modelos, um protocolo de avaliação e
uma arquitetura de referência. Assim, o protótipo não aparece como uma ideia
desconectada do levantamento.

## 17. Protótipo conceitual — 1:05

A arquitetura separa ingestão, preparação, modelagem, avaliação e explicabilidade
e apresentação. Ela prevê rastreabilidade, incerteza, revisão humana,
privacidade e alinhamento curricular. É uma especificação, não uma aplicação
funcional. Não houve treinamento com uma base definitiva, métricas próprias de
acurácia ou validação com participantes.

## 18. Contribuições e limites — 1:05

As contribuições são a síntese estruturada, o pipeline automatizado e
versionado, a distinção entre relevância temática e avaliação metodológica e a
especificação técnica e pedagógica auditável. Os limites incluem a condução por
um único pesquisador, a cobertura desigual das fontes, o MMAT preliminar e a
ausência de eficácia pedagógica própria. Declarar esses limites faz parte da
validade do resultado.

## 19. Encerramento — 0:30

Em síntese, o trabalho respondeu ao escopo ao articular revisão sistemática,
fundamentação pedagógica, apreciação metodológica e especificação conceitual.
Sua tese central é que técnicas computacionais podem apoiar a interpretação de
evidências, desde que seus limites sejam explicitados e o professor permaneça
no centro da decisão pedagógica. Obrigado; fico à disposição para perguntas.
