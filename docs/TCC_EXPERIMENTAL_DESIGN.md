# Desenho experimental do protótipo

## Finalidade

Este documento fixa, antes da execução empírica, as decisões que determinam como o protótipo será avaliado. O objetivo é reduzir graus de liberdade analíticos, prevenir vazamento de informação e separar desempenho preditivo de inferências pedagógicas que o experimento não é capaz de sustentar.

As decisões dependentes da base de dados, como limiares mínimos de suporte por habilidade, serão congeladas após a seleção e caracterização da base no lote de governança de dados e antes de qualquer avaliação no conjunto de teste.

## Pergunta de pesquisa operacional

Em que medida modelos computacionais probabilísticos e interpretáveis conseguem estimar a probabilidade de acerto na próxima interação elegível de um estudante, condicionada ao histórico anterior e ao item e às habilidades conhecidos antes da resposta, e transformar essas estimativas em um perfil de evidências por habilidade útil ao apoio da decisão docente?

A pergunta foi formulada para permitir avaliação técnica reproduzível sem afirmar, por extensão indevida, que uma boa previsão comprova aprendizagem, competência latente, causalidade ou eficácia pedagógica.

## Unidade de análise

A unidade mínima é uma interação entre estudante e item:

- estudante anonimizado;
- item ou questão;
- uma ou mais habilidades associadas;
- posição temporal ou timestamp;
- resposta observada;
- indicador de correção;
- tentativas, dicas e tempo, quando disponíveis;
- proveniência do conjunto de dados.

Interações sem possibilidade de ordenação estável não serão usadas no protocolo principal de previsão da próxima resposta.

## Âncora e horizonte de previsão

### Horizonte primário

O horizonte primário é de **uma interação elegível à frente**. A previsão é produzida imediatamente antes de a resposta da interação-alvo ser observada.

Para uma interação-alvo `t`, o modelo pode utilizar somente:

- eventos com ordem estritamente anterior a `t`;
- o identificador do item-alvo, quando conhecido antes da resposta;
- as habilidades associadas ao item-alvo, quando conhecidas antes da resposta;
- contexto disponível antes da resposta e explicitamente permitido pelo contrato do experimento.

O desfecho da interação-alvo e qualquer campo produzido durante ou após sua resolução não podem participar dos atributos do protocolo primário.

### Semântica da linha canônica

A linha canônica representa a própria interação que será prevista. O campo `correct` dessa linha é desconhecido no instante da inferência e somente se torna disponível depois da resposta, quando passa a ser o rótulo observado para avaliação.

O nome `correct_next` é usado no nível de modelagem porque `correct` pertence ao próximo evento em relação ao histórico disponível. Não existe deslocamento implícito que permita usar o resultado da interação-alvo como atributo.

Se o item ou a habilidade da próxima interação não forem conhecidos antes da resposta, essa interação não é elegível para o protocolo primário condicionado a item e habilidade. Um protocolo de previsão sem conhecimento do próximo item constituiria uma tarefa diferente e exigiria especificação própria.

## Variável-alvo

### Alvo primário

`correct_next ∈ {0, 1}` indica se a interação-alvo, que é a próxima interação elegível em relação ao histórico disponível, foi respondida corretamente.

A transformação de escalas parciais, escores contínuos ou códigos específicos de uma base para o desfecho binário deverá ser documentada no lote de governança e preparação dos dados. Casos ambíguos não serão convertidos silenciosamente.

### Saída contínua

O modelo produzirá `P(correct_next = 1 | history, item, skill)`, interpretada como probabilidade estimada de acerto sob as condições representadas pelos dados.

Essa probabilidade não será chamada automaticamente de aprendizagem, competência, proficiência ou domínio verdadeiro. Trata-se de uma estimativa operacional de desempenho futuro condicionada às informações disponíveis.

### Resultado pedagógico derivado

Probabilidades e evidências observadas associadas a uma mesma habilidade poderão ser agregadas em um perfil de evidências de domínio e fragilidade. A regra de agregação, a janela histórica, o suporte mínimo e os intervalos de interpretação serão definidos e versionados antes da análise final.

Níveis ordinais e alertas binários serão produtos derivados. Eles não substituirão a probabilidade original e não serão apresentados como diagnósticos definitivos.

## Hipóteses e análises exploratórias

### Hipóteses confirmatórias

- **H1:** baselines históricos que usam informação anterior de estudante, item ou habilidade apresentarão melhor qualidade probabilística que a probabilidade global de acerto.
- **H2:** a regressão logística regularizada apresentará melhor qualidade probabilística que o melhor baseline histórico simples.

A métrica de seleção para essas comparações será o log-loss. O Brier Score e as medidas de calibração funcionarão como evidências co-primárias de consistência. Uma hipótese somente será descrita como sustentada quando a direção do contraste for estável nas partições predefinidas e a incerteza do contraste, estimada de forma agrupada por estudante, não contradizer a conclusão principal.

Os resultados nulos ou contrários às hipóteses serão preservados e reportados. Nenhuma configuração será escolhida retrospectivamente para produzir suporte às hipóteses.

### Análises exploratórias

- **E1:** avaliar se pelo menos um modelo não linear melhora a qualidade preditiva em relação à regressão logística sem produzir perda relevante de calibração ou interpretabilidade;
- **E2:** descrever heterogeneidade de desempenho e calibração entre habilidades com suporte amostral suficiente;
- **E3:** avaliar a utilidade descritiva de um perfil por habilidade em comparação com um único alerta binário.

A análise E3 não constitui evidência de utilidade pedagógica para professores. Uma conclusão sobre compreensão, usabilidade ou efeito em decisões docentes exigiria estudo específico com participantes, fora do experimento preditivo atual.

## Protocolos de divisão

Serão utilizados dois cenários complementares.

### Generalização com estudantes retidos (`student_holdout`)

Os identificadores de estudante serão separados integralmente entre treino, validação e teste. Nenhum estudante do conjunto de validação ou teste poderá contribuir para o ajuste dos parâmetros do modelo.

Durante a avaliação de um estudante retido, atributos históricos desse próprio estudante poderão ser atualizados apenas com interações anteriores à interação-alvo. Essas observações servem como contexto online e não atualizam parâmetros treináveis do modelo.

Esse cenário avalia generalização para estudantes não utilizados no ajuste, mas não equivale necessariamente a `cold start` com histórico zero. A primeira interação elegível de cada estudante retido será reportada separadamente como análise de `cold start` verdadeiro quando a base permitir.

### Previsão temporal personalizada (`personalized_temporal`)

Para estudantes com histórico suficiente, as interações serão ordenadas. A parte inicial formará o período de treino, seguida por validação e teste futuros. A construção dos atributos de cada interação-alvo usará apenas eventos anteriores a ela.

Agregações globais, dificuldades de itens, parâmetros de suavização e transformações aprendidas deverão ser estimados exclusivamente com a porção de treino correspondente. O conjunto de teste não será usado para ajustar hiperparâmetros, limiares ou regras de pré-processamento.

A regra de arredondamento das frações e o tratamento de empates temporais serão determinísticos e versionados.

### Divisões proibidas

A divisão aleatória por linha é proibida no protocolo principal porque ignora a dependência entre interações do mesmo estudante e pode misturar temporalmente observações relacionadas.

Qualquer análise adicional que use outra estratégia de divisão deverá ser identificada como análise de sensibilidade e não poderá substituir silenciosamente o protocolo predefinido.

## Critérios mínimos de inclusão

A configuração inicial exige:

- identificador anônimo de estudante;
- identificador de item;
- indicador de correção ou regra documentada para obtê-lo;
- ordem temporal estável;
- pelo menos uma habilidade ou conceito por item;
- número mínimo configurável de interações por estudante;
- documentação da origem, licença e condições de uso.

Registros duplicados, impossíveis ou sem ordenação confiável serão tratados por regras explícitas e contabilizados no relatório de qualidade.

## Modelos de referência

A comparação começará por modelos simples:

1. probabilidade global de acerto;
2. probabilidade histórica suavizada por item;
3. probabilidade histórica suavizada por habilidade;
4. média histórica suavizada do estudante;
5. regressão logística regularizada.

Parâmetros de suavização e hiperparâmetros serão definidos com treino e validação e congelados antes da avaliação do teste. O conjunto de teste não participará da escolha da intensidade de suavização.

Um modelo não linear baseado em árvores será adicionado somente depois que os baselines estiverem validados. Modelos sequenciais profundos e `knowledge tracing` avançado serão extensões, não requisitos do primeiro experimento.

## Atributos candidatos

Somente atributos disponíveis antes da resposta-alvo poderão ser usados:

- quantidade de interações anteriores;
- taxa histórica de acerto do estudante;
- taxa histórica do estudante na habilidade;
- dificuldade histórica do item calculada apenas no treino;
- número histórico de tentativas;
- uso histórico de dicas;
- tempo histórico mediano ou transformado;
- intervalo desde a interação anterior;
- posição da interação na sessão;
- habilidade e item codificados de forma apropriada.

No protocolo primário, `correct`, `answer`, número de tentativas, número de dicas e tempo decorrido **da própria interação-alvo** são desfechos ou informações posteriores à âncora e não podem ser usados como atributos. Suas versões históricas, derivadas exclusivamente de interações anteriores, podem ser utilizadas.

Atributos demográficos não serão utilizados no modelo principal para gerar classificações individuais. Quando disponíveis e permitidos, poderão ser usados apenas para auditoria de desempenho e calibração entre subgrupos.

## Itens associados a múltiplas habilidades

A interação canônica preservará `skill_ids` como conjunto de habilidades do item. O protocolo principal não duplicará linhas de treinamento apenas para transformar uma interação multihabilidade em várias observações artificialmente independentes.

Relatórios por habilidade poderão associar a mesma interação a mais de uma habilidade, mas deverão:

- contar separadamente interações únicas e estudantes únicos;
- preservar a dependência entre observações na estimação de incerteza;
- explicitar que as categorias de habilidade podem se sobrepor;
- versionar qualquer estratégia alternativa de atribuição ou ponderação.

## Métricas

### Métrica de seleção

O **log-loss** será a métrica utilizada para seleção de modelos probabilísticos, por avaliar diretamente a qualidade das probabilidades previstas e penalizar previsões incorretas excessivamente confiantes.

### Evidência co-primária

O **Brier Score** será reportado em todas as comparações principais. Divergência relevante entre log-loss, Brier Score e calibração será tratada como `trade-off` e impedirá uma afirmação simples de superioridade sem discussão explícita.

### Calibração

A calibração será avaliada por:

- intercepto de calibração;
- inclinação de calibração;
- curva de confiabilidade/calibração;
- erro esperado de calibração, apenas como medida complementar e com regra de binning registrada.

Nenhuma única medida de calibração será usada isoladamente para declarar um modelo calibrado.

### Métricas secundárias

- ROC-AUC;
- PR-AUC / average precision;
- acurácia em limiar previamente definido, quando aplicável;
- precisão, revocação e F1, quando houver decisão binária derivada.

As métricas serão apresentadas globalmente e por habilidade apenas quando houver suporte suficiente.

## Suporte amostral para análises por habilidade

O suporte mínimo não será escolhido após observar o desempenho no teste. Após a seleção da base no lote de governança de dados serão congelados, antes da avaliação final:

- número mínimo de interações de teste por habilidade;
- número mínimo de estudantes distintos por habilidade;
- política para habilidades raras e categorias sobrepostas.

Habilidades abaixo do suporte predefinido serão reportadas como evidência insuficiente em vez de receberem estimativas fortes.

## Comparação e incerteza

- todos os modelos usarão exatamente as mesmas partições em cada cenário;
- seeds, parâmetros, versões e hashes das partições serão registrados;
- todas as seeds predefinidas serão reportadas; não será escolhida a seed com melhor resultado;
- contrastes entre modelos serão calculados de forma pareada nas mesmas observações de teste;
- quando utilizado bootstrap para intervalos, o reamostramento será feito por estudante, preservando conjuntamente suas interações;
- o bootstrap das previsões retidas quantificará incerteza associada à amostra de avaliação; variação causada pelo treinamento será analisada separadamente pelas seeds e partições predefinidas;
- diferenças pequenas serão apresentadas com sua incerteza e não apenas pelo valor pontual;
- modelos mais complexos somente serão preferidos quando o ganho for consistente e compatível com os requisitos de calibração e interpretação.

## Interpretabilidade

A regressão logística fornecerá coeficientes e efeitos direcionais. Para modelos de árvore, poderão ser avaliadas explicações globais e locais com SHAP ou método equivalente.

A interpretação deverá distinguir:

- associação estatística;
- importância para o modelo;
- explicação da previsão;
- causa da dificuldade;
- recomendação pedagógica.

Somente as três primeiras podem ser obtidas diretamente do experimento preditivo. Importância de variável ou explicação local não será descrita como causa.

## Perfil por habilidade

O perfil será calculado a partir de previsões e evidências observadas, contendo:

- habilidade;
- probabilidade estimada;
- quantidade de interações e estudantes que sustentam a estimativa;
- intervalo ou medida de incerteza;
- período considerado;
- versão do modelo;
- limitações de interpretação.

Habilidades com poucas evidências serão marcadas como insuficientes em vez de receberem classificação forte.

## Auditoria de equidade

Quando os dados, a licença e a base legal permitirem, poderão ser comparados:

- log-loss e Brier Score por subgrupo;
- calibração por subgrupo;
- taxas de falso positivo e falso negativo para alertas derivados;
- cobertura de habilidades e quantidade de interações.

Os limiares mínimos de suporte por subgrupo serão definidos antes da avaliação do teste. Diferenças observadas serão descritas como propriedades do modelo no conjunto analisado, não como características naturais dos grupos.

## Conclusões permitidas e proibidas

### O experimento poderá sustentar

- comparação de qualidade preditiva entre modelos no conjunto analisado;
- avaliação de calibração nas partições predefinidas;
- descrição de heterogeneidade por habilidade com suporte suficiente;
- análise de associações e de importância para o modelo;
- identificação de limitações de cobertura e generalização.

### O experimento não poderá, isoladamente, sustentar

- melhoria de aprendizagem;
- eficácia de uma intervenção pedagógica;
- causalidade entre atributo e dificuldade do estudante;
- diagnóstico psicológico, clínico ou educacional definitivo;
- equivalência entre probabilidade de acerto e competência latente;
- generalização para populações, instituições ou contextos não representados pelos dados;
- substituição da interpretação profissional do professor.

## Critérios de execução do experimento

O experimento será considerado executado quando:

1. todas as partições forem reproduzíveis e versionadas;
2. os baselines e pelo menos um modelo não linear forem comparados;
3. log-loss, Brier Score e calibração forem avaliados;
4. resultados por habilidade respeitarem suporte previamente congelado;
5. os artefatos forem gerados por código;
6. limitações de generalização forem registradas;
7. análise de incerteza for produzida segundo o protocolo;
8. nenhuma métrica for descrita como prova de aprendizagem ou eficácia pedagógica.

## Prática de ciência aberta

O repositório deverá conter:

- manifesto do conjunto de dados sem redistribuir arquivos proibidos;
- script de download ou instruções verificáveis;
- hashes dos arquivos brutos;
- contrato de esquema;
- configuração do experimento;
- código de preparação, treino e avaliação;
- ambiente versionado;
- hashes das partições de treino, validação e teste;
- tabelas e figuras geradas automaticamente;
- registro de exclusões e transformações;
- registro de qualquer desvio do protocolo com justificativa e data.
