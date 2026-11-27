# Roteiro de falas — defesa do TCC

Roteiro do deck canônico Slidev (`presentation/slides.md`, 24 slides). As mesmas falas estão nas notas do apresentador de cada slide (tecla `P` no Slidev abre o modo apresentador). Ao alterar uma fala, altere os dois lugares; o teste `research/tests/test_presentation_script.py` confere a correspondência.

Tempo total estimado: 23 min 15 s, sem perguntas. Para encurtar, resuma em uma frase os slides 9 (Fontes) e 19 (Exemplos).

Cada bloco indica o que mostrar na tela e a fala sugerida. Os números e as formulações seguem o TCC compilado (`results/tcc/main.pdf`); a fala não acrescenta resultados que o texto não sustenta.

| Slide | Tema | Tempo |
|---:|---|---:|
| 1 | Capa | 0:30 |
| 2 | Contexto — O problema: ler a aprendizagem em turmas heterogêneas | 1:00 |
| 3 | Objetivo geral — O que o trabalho propõe | 0:45 |
| 4 | Problema de pesquisa — Pergunta de pesquisa | 0:30 |
| 5 | Base conceitual — Cinco distinções interpretativas | 1:15 |
| 6 | Didática da matemática — Acertar ou errar não revela o tipo de erro | 1:00 |
| 7 | Objetivos específicos — Quatro objetivos, quatro produtos | 1:00 |
| 8 | Método — Revisão sistemática: busca em três camadas | 1:00 |
| 9 | Fontes — Quatro bases de indexação complementares | 0:40 |
| 10 | Fluxo prisma — Fluxograma de seleção | 1:15 |
| 11 | Seleção original — 15 estudos na seleção; 14 textos recuperados | 0:45 |
| 12 | Corte de relevância — O corte 4,0 é heurístico: havia elegíveis abaixo dele | 1:00 |
| 13 | Qualidade metodológica — MMAT conferido: critério a critério, sem nota global | 1:00 |
| 14 | Resultado — oe1 — Para que as técnicas são usadas nos 15 estudos | 1:15 |
| 15 | Resultado — oe2 — O que falta nos relatos: a resposta mais comum é “não é possível concluir” | 1:15 |
| 16 | Resultado — oe2 — Três eixos de risco viraram requisitos | 1:00 |
| 17 | Síntese — O que a evidência permite especificar | 1:00 |
| 18 | Alcance — O que o TCC entrega, e o que não entrega | 0:50 |
| 19 | Evidências e limites — Exemplos de limitações nos estudos consultados | 1:00 |
| 20 | Resultado — oe3 — Da evidência aos requisitos: uma cadeia rastreável | 1:15 |
| 21 | Arquitetura e saída — O professor vê indícios e incerteza, não um veredito | 1:15 |
| 22 | Oe3 e oe4 — Regras do protocolo proposto | 1:15 |
| 23 | Conclusão — Resposta: uma especificação verificável antes dos dados | 1:15 |
| 24 | Encerramento | 0:15 |

## 1. Capa — 0:30

**Mostrar:** título e a faixa inferior (revisão, 15 estudos, especificação conceitual).

**Fala:** Boa tarde. Apresento o TCC Ensino Personalizado de Matemática. O trabalho tem duas entregas ligadas entre si: uma revisão sistemática de técnicas computacionais aplicadas ao ensino de matemática e, a partir dela, a especificação de um protótipo para apoiar a interpretação do professor. É uma entrega documental: não há sistema validado em escola.

## 2. Contexto — O problema: ler a aprendizagem em turmas heterogêneas — 1:00

**Mostrar:** frase em destaque à esquerda; depois os quatro cartões, de cima para baixo.

**Fala:** Em turmas heterogêneas, a média da turma não mostra onde cada estudante está nem quanta evidência sustenta essa leitura. O professor tem pouco tempo para analisar registros, e a mesma intervenção não atende necessidades distintas. Há literatura sobre técnicas computacionais, mas ela está dispersa em técnicas, alvos e contextos. A premissa do trabalho: a técnica pode organizar evidências, e a interpretação continua com o professor.

## 3. Objetivo geral — O que o trabalho propõe — 0:45

**Mostrar:** caixa central com o objetivo geral; depois PARA QUÊ e ESCOPO.

**Fala:** O objetivo geral é propor uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática, fundamentada na literatura. O apoio se limita a mostrar ao professor indícios de desempenho e de incerteza por estudante e habilidade, sem substituir seu julgamento. O escopo é revisão e especificação; protótipo validado e avaliação de eficácia ficam fora.

## 4. Problema de pesquisa — Pergunta de pesquisa — 0:30

**Mostrar:** ler a pergunta inteira, sem paráfrase.

**Fala:** A pergunta de pesquisa é esta. A palavra que orienta a resposta é estruturar: o resultado esperado é uma forma rastreável de organizar a especificação a partir da evidência, e não a escolha de um modelo vencedor.

## 5. Base conceitual — Cinco distinções interpretativas — 1:15

**Mostrar:** a escada de 01 a 05, em ordem; ao final, a regra de leitura.

**Fala:** Antes da revisão, separo cinco termos que a literatura às vezes mistura. Desempenho observado é o que foi registrado na tarefa. Probabilidade preditiva é a saída de um modelo para um alvo definido e com os dados usados; não é proficiência. Proficiência estimada exige modelo de mensuração e evidência de validade. Competência, no sentido da BNCC, é mobilizar conhecimentos, habilidades, atitudes e valores. Aprendizagem, neste trabalho, é mudança ao longo do tempo. A regra que sai daqui: a saída computacional organiza evidência e produz estimativas, mas sozinha não observa a aprendizagem nem demonstra eficácia.

## 6. Didática da matemática — Acertar ou errar não revela o tipo de erro — 1:00

**Mostrar:** o exemplo do 7º ano; depois o cartão 0/1 ≠ diagnóstico.

**Fala:** Dois referenciais da didática da matemática delimitam o que essa saída não capta. Para Duval, compreender exige coordenar ao menos dois registros de representação. Para Brousseau, um erro pode manifestar um obstáculo. No exemplo, errar a conversão do enunciado para 2x + 5 = 15 é diferente de errar ao isolar x, mas os dois viram o mesmo zero num registro binário. Por isso a especificação organiza indícios por habilidade, com incerteza, e deixa o tipo de erro para o professor, na revisão docente da função F06. Codificar itens por registro de representação fica como trabalho futuro.

## 7. Objetivos específicos — Quatro objetivos, quatro produtos — 1:00

**Mostrar:** os quatro passos e, em cada um, o produto indicado pela seta.

**Fala:** Os quatro objetivos específicos geram quatro produtos. OE1 categoriza técnicas e finalidades: resulta na tipologia dos 15 estudos. OE2 codifica limitações metodológicas e de relato com o MMAT e discute os eixos técnico, pedagógico e ético. OE3 formula a especificação: 26 grupos de requisitos, critérios de dados e modelos e a arquitetura. OE4 propõe o protocolo para avaliar a viabilidade e a coerência da especificação. O protocolo está proposto e não foi aplicado.

## 8. Método — Revisão sistemática: busca em três camadas — 1:00

**Mostrar:** os hexágonos (três camadas); o cartão de 72 consultas; a faixa PRISMA/MMAT.

**Fala:** A busca combina três camadas: um termo matemático, um termo de técnica computacional e um termo de educação. Foram 72 consultas canônicas, 48 em inglês e 24 em português, em quatro bases, para 2015 a 2026, com busca encerrada em 31 de agosto de 2026. O PRISMA 2020 orienta o relato, e o MMAT 2018 orienta a apreciação metodológica.

## 9. Fontes — Quatro bases de indexação complementares — 0:40

**Mostrar:** os quatro cartões com as contagens; a legenda.

**Fala:** As quatro bases são complementares: Semantic Scholar, OpenAlex, Crossref e CORE. Depois da remoção de 29 duplicatas ficaram 11.875 registros. A base indicada em cada cartão é a origem da versão mantida, não a cobertura exclusiva daquela base. Se faltar tempo, este slide pode ser dito em uma frase.

## 10. Fluxo prisma — Fluxograma de seleção — 1:15

**Mostrar:** percorrer o fluxograma de cima para baixo, apontando cada caixa.

**Fala:** Este é o fluxo de seleção. Foram 11.904 registros identificados e 29 duplicatas removidas; 11.875 foram triados, e as regras automáticas excluíram 9.393, em boa parte por resumo ausente ou curto. Dos 2.482 priorizados por escore de relevância, o corte 4,0 deixou 18 na lista preliminar. Um saiu após a leitura do resumo; 17 relatórios foram procurados e dois não foram recuperados, Sokkhey e Zeng. Quinze foram avaliados em texto completo, e um protocolo sem resultados foi excluído. A seleção original fica com 15 estudos, e o próximo slide explica por quê.

## 11. Seleção original — 15 estudos na seleção; 14 textos recuperados — 0:45

**Mostrar:** o número 15 e a divisão 14 + 1.

**Fala:** São 15 estudos na seleção original, 14 com texto recuperado e conferido. Sokkhey permanece na seleção, mas sem apreciação MMAT, e sua linha na síntese se baseia só no resumo publicado. Zeng não foi recuperado e não integra os 15.

## 12. Corte de relevância — O corte 4,0 é heurístico: havia elegíveis abaixo dele — 1:00

**Mostrar:** as três barras; o número 4,0; o aviso de limitação.

**Fala:** O corte 4,0 serviu para priorizar a leitura e foi mantido. Explorei o que ficou abaixo dele: 13 de 45 registros elegíveis no censo entre 3,75 e 3,95; 29 de 54 na seleção dirigida entre 3,50 e 3,74; e 5 de 30 na amostra estratificada entre 3,00 e 3,49. Os desenhos são diferentes, então não somo as frações nem estimo a perda total. É uma limitação declarada: o recorte não é um censo da literatura, e o escore mede relevância, não qualidade.

## 13. Qualidade metodológica — MMAT conferido: critério a critério, sem nota global — 1:00

**Mostrar:** S1 e S2; a legenda Y/N/CT; a faixa de estado embaixo.

**Fala:** O MMAT funciona em duas etapas: duas perguntas de triagem e depois cinco critérios próprios da categoria do estudo. Cada resposta é Sim, Não ou Não é possível concluir. Nos 14 textos recuperados, S1 teve 14 Sim e S2 teve 13 Sim e 1 Não é possível concluir. A leitura é critério a critério, sem nota global. Nos três estudos de métodos mistos, as respostas dos componentes qualitativo e quantitativo seguem identificadas como assistidas por IA.

## 14. Resultado — oe1 — Para que as técnicas são usadas nos 15 estudos — 1:15

**Mostrar:** as cinco barras; depois o aviso de categorias não homogêneas.

**Fala:** Este é o resultado do OE1. Cada estudo recebeu uma finalidade principal: predição ou classificação em 8, personalização ou sistemas tutores em 3, intervenção didática em 2, modelagem cognitiva em 1 e integração curricular em 1. Nos estudos de predição, a finalidade pedagógica aparece apenas pelo alvo previsto, como nota ou desempenho posterior. Há um limite na própria tipologia: predição é uma tarefa computacional, e as outras quatro são finalidades de uso. As frequências descrevem este recorte, não a literatura toda.

## 15. Resultado — oe2 — O que falta nos relatos: a resposta mais comum é “não é possível concluir” — 1:15

**Mostrar:** a grade; destacar a linha quantitativo descritivo (Q2 a Q4 com 7 de 7).

**Fala:** Este é o resultado do OE2. A grade conta quantas vezes cada critério ficou como Não é possível concluir. Nos sete estudos quantitativos descritivos, Q2, Q3 e Q4 ficaram assim em todos. A leitura é que falta informação nos relatos, mais do que falha demonstrada. A consequência para o projeto é exigir que se declarem alvo, população, transformações dos dados e forma de avaliação.

## 16. Resultado — oe2 — Três eixos de risco viraram requisitos — 1:00

**Mostrar:** as três colunas e os códigos R e F de cada uma; o rodapé de equidade.

**Fala:** Os três eixos de risco discutidos no OE2 viraram requisitos. No eixo técnico, validar sem vazar informação: R20 registra quando o desfecho é definido e quais atributos existem nesse momento, e F03 bloqueia a saída que viole isso. No pedagógico, não chamar previsão de proficiência e manter o professor na interpretação. No ético, finalidade, minimização e pseudonimização, com atenção ao art. 14 da LGPD para crianças e adolescentes. A análise de equidade, R23, não foi operacionalizada porque os dados não têm colunas de subgrupo aprovadas.

## 17. Síntese — O que a evidência permite especificar — 1:00

**Mostrar:** a frase de título do bloco e os três pontos numerados.

**Fala:** Como os estudos usam populações, alvos e métricas diferentes, não faz sentido ranquear modelos. O que a evidência permite é fixar condições de projeto: alvo explícito, modelo simples como referência, com a regressão logística, e incerteza visível, porque poucas respostas não sustentam conclusão sobre o estudante.

## 18. Alcance — O que o TCC entrega, e o que não entrega — 0:50

**Mostrar:** as duas colunas; o rodapé de limitações.

**Fala:** O TCC entrega um mapa auditável da literatura e uma especificação com requisitos rastreáveis e regras de avaliação definidas antes dos dados. Não entrega evidência de eficácia: não compara modelos em dados reais, não valida protótipo em escola e não mede efeito na aprendizagem. As limitações principais são o revisor único, a triagem em texto completo e a extração produzidas por modelos de IA, com o MMAT conferido pelo autor, 14 de 15 textos recuperados, a sensibilidade abaixo do corte e a ausência de aplicação com participantes.

## 19. Evidências e limites — Exemplos de limitações nos estudos consultados — 1:00

**Mostrar:** os dois cartões: relato e implicação de cada um.

**Fala:** Dois exemplos mostram o tipo de limite encontrado, sem indicar frequência. Em He e colaboradores, há oito turmas de 45 estudantes e uma amostra de 90 por comparação, sem que o texto explicite essa relação, e um único professor responde pelas duas turmas de controle; por isso a especificação exige declarar denominadores e unidade de análise. Em Nyantah e colaboradores, a alocação aparece como aleatória e depois como quase-experimental, os grupos já diferiam no pré-teste e a intervenção combina animação e jigsaw; não se pode atribuir o resultado à animação isoladamente.

## 20. Resultado — oe3 — Da evidência aos requisitos: uma cadeia rastreável — 1:15

**Mostrar:** a cadeia da esquerda para a direita; depois o exemplo R04 e o quadro das duas matrizes.

**Fala:** O OE3 se organiza como uma cadeia rastreável, que é a Figura 3 do TCC: revisão, 26 grupos de requisitos, sete funções, critérios de aceitação e o protocolo do OE4. No exemplo de proteção de dados, R04 exige finalidade, minimização e controle de acesso; F04 limita a consulta individual e F07 registra e exporta versões; o critério de aceitação pede perfil autorizado e identificadores pseudonimizados. Há duas matrizes: os 15 estudos se relacionam a 18 grupos de requisitos, e seis estudos são citados diretamente em sete grupos. Esses vínculos motivam decisões de projeto; não validam os requisitos.

## 21. Arquitetura e saída — O professor vê indícios e incerteza, não um veredito — 1:15

**Mostrar:** o fluxo F01 a F06 à esquerda; no cartão, apontar o intervalo 0,30–0,90 na régua.

**Fala:** A arquitetura vai da ingestão com fonte, licença e dicionário, F01, à preparação com vínculo curricular, F02, à modelagem, F03, à avaliação com métricas e explicações, F05, e à apresentação com revisão docente, F04 e F06. F07 registra e exporta tudo. À direita, uma saída fictícia: o estudante A acertou 4 de 6 itens de comparação de frações, taxa de 0,67, mas o intervalo de Wilson de 95% vai de 0,30 a 0,90. Com tão poucas respostas, não há conclusão sobre o estudante. A média das probabilidades previstas aparece sem intervalo próprio, a calibração não foi examinada e o alerta de risco fica desabilitado. Quem decide o próximo passo é a professora.

## 22. Oe3 e oe4 — Regras do protocolo proposto — 1:15

**Mostrar:** painel esquerdo, condições i a iii; painel direito, regra docente e conferência técnica.

**Fala:** As regras foram fixadas antes de qualquer dado real. Para o modelo, a referência é a regressão logística regularizada. Um candidato mais complexo só é adotado se cumprir três condições: melhorar a perda logarítmica, com intervalo de 95% por reamostragem pareada por estudante; não piorar o Brier nem aumentar o erro de calibração esperado; e oferecer explicação local conferível. Se falhar, mantém-se a referência. Para o OE4, um painel de cinco docentes avalia cada grupo de requisitos em duas rodadas; o grupo é coerente se ao menos quatro dos cinco derem 3 ou 4 em cada dimensão, sem problema crítico. A conferência técnica é separada. As fichas estão no Apêndice C. Nada disso foi aplicado, e a aplicação depende de parecer ético.

## 23. Conclusão — Resposta: uma especificação verificável antes dos dados — 1:15

**Mostrar:** as quatro contribuições; depois os próximos passos.

**Fala:** Respondendo à pergunta: a especificação se estrutura ligando alvo e população à evidência disponível, convertendo os achados em requisitos e definindo como o professor examina as saídas. O OE1 mostrou que a literatura se concentra em predição, com finalidade pedagógica indireta. O OE2 mostrou que o desempenho reportado não se transfere para a sala de aula sem alvo, população, validação e incerteza. O OE3 converteu essas lacunas em exigências verificáveis. O OE4 fixou os critérios de avaliação antes da aplicação. Os próximos passos são aplicar o protocolo com docentes após parecer ético, testar a regra de modelo em dados reais documentados, construir a correspondência com as habilidades da BNCC e codificar itens por registro de representação.

## 24. Encerramento — 0:15

**Mostrar:** o QR do repositório.

**Fala:** Obrigado. O texto, os dados derivados e o código estão no repositório público, acessível pelo QR. Fico à disposição para as perguntas.

## Perguntas prováveis da banca

- **Por que o corte 4,0 e não outro?** O corte priorizou a leitura e foi mantido. A exploração abaixo dele (13 de 45, 29 de 54 e 5 de 30) mostrou elegíveis de fora; isso é limitação declarada, sem estimativa de perda, e o recorte não é censo da literatura.
- **Por que manter Sokkhey sem texto completo?** A seleção original não foi refeita depois das conferências. Sokkhey permanece nela, sem apreciação MMAT, e sua linha na síntese se baseia no resumo publicado. Zeng não foi recuperado e está fora dos 15.
- **Qual foi o papel da IA?** A triagem em texto completo, a extração de dados e as respostas MMAT foram conduzidas com apoio de ferramentas de IA generativa (Apêndice E). O autor conferiu as respostas MMAT dos 14 estudos com texto recuperado, critério a critério; nos três mistos, os componentes separados não foram conferidos e seguem identificados como assistidos por IA. A síntese depende da fidedignidade dessas etapas.
- **Por que não há protótipo validado?** O escopo é documental. A implementação exploratória serviu só como verificação técnica do fluxo, com dados sintéticos. Validação em escola e avaliação de eficácia são trabalhos futuros.
- **Por que a regressão logística como referência?** É simples, produz probabilidades e é interpretável. Um candidato mais complexo só é adotado se melhorar a perda logarítmica com intervalo de 95% abaixo de zero, sem piorar Brier nem calibração, e com explicação local conferível.
- **De onde vem a regra de quatro em cinco docentes?** É uma escolha de projeto (80%) para o painel, não validação estatística do instrumento nem estimativa para uma população docente. Há duas rodadas individuais e uma reunião para discutir divergências sem forçar consenso.
- **Como ficam os dados de crianças e adolescentes?** A aplicação depende de parecer ético e de base legal; o art. 14 da LGPD exige o melhor interesse do titular. A especificação prevê finalidade, minimização e pseudonimização, que não equivale a anonimização.
- **O protótipo usa a BNCC?** O adaptador atual aceita só o ASSISTments, com habilidades de um currículo estrangeiro. A correspondência com as habilidades da BNCC não foi construída nem validada e precede qualquer uso no Brasil.
- **Por que o MMAT sem nota global?** A apreciação é apresentada por critério, sem escore agregado. CT indica informação insuficiente na evidência disponível ao revisor, não falha demonstrada do estudo.
- **Duval e Brousseau foram operacionalizados?** Não. Eles delimitam o que uma saída binária não capta. O diagnóstico do tipo de erro fica com o professor (F06), e a codificação por registro de representação é trabalho futuro.
