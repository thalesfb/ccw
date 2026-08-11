# Decisões científicas para implementação do protótipo

## 1. Finalidade do documento

Este documento registra as decisões científicas aprovadas para orientar a implementação do protótipo associado ao Trabalho de Conclusão de Curso. Sua função é reduzir ambiguidades entre o problema educacional, a tarefa estatística, a saída computacional e a interpretação pedagógica.

As decisões aqui registradas constituem uma linha de base de pesquisa. Alterações posteriores deverão ser justificadas por evidências provenientes da literatura, das características da base de dados ou dos resultados experimentais reproduzíveis.

## 2. Problema de pesquisa operacional

O protótipo investigará em que medida modelos computacionais interpretáveis podem estimar a probabilidade de desempenho do estudante em habilidades matemáticas específicas a partir de seu histórico de interações e transformar essas estimativas em um perfil de domínio e fragilidade útil ao apoio da decisão docente.

A implementação não será tratada como mecanismo autônomo de diagnóstico, classificação permanente ou prescrição pedagógica. O professor permanecerá responsável pela interpretação contextual das evidências e pela decisão sobre intervenções.

## 3. Unidade de análise

A unidade de análise primária será uma interação entre estudante e item matemático.

Cada interação deverá estar associada, quando a base permitir, aos seguintes elementos:

- identificador anonimizado do estudante;
- identificador do item ou atividade;
- habilidade, competência ou descritor relacionado ao item;
- ordem temporal da interação;
- resultado observado da resposta;
- quantidade de tentativas;
- uso de dicas ou suporte;
- tempo de resposta;
- atributos contextuais cuja utilização seja metodologicamente e eticamente justificável.

A unidade de análise não será a pessoa como categoria fixa. O sistema analisará evidências produzidas em interações específicas e temporalmente delimitadas.

## 4. Variável-alvo primária

A variável-alvo primária será o resultado da próxima interação do estudante em uma habilidade matemática específica:

- `1`: resposta correta;
- `0`: resposta incorreta.

O horizonte de previsão será explicitamente temporal: apenas informações disponíveis antes da interação prevista poderão ser utilizadas como atributos.

Essa formulação permite avaliar o modelo em uma tarefa observável e reproduzível, sem afirmar que acerto e aprendizagem são conceitos equivalentes.

## 5. Saída probabilística

O modelo deverá produzir uma probabilidade estimada de acerto:

```text
P(acerto na próxima interação | estudante, habilidade, item e histórico disponível)
```

A probabilidade será tratada como uma estimativa condicionada aos dados e ao modelo. Não será interpretada como medida direta e completa de aprendizagem, competência ou capacidade do estudante.

A avaliação deverá incluir discriminação e calibração. Um modelo não será considerado adequado apenas porque ordena corretamente casos de maior ou menor risco; suas probabilidades também deverão apresentar correspondência aceitável com as frequências observadas.

## 6. Resultado pedagógico principal

O resultado pedagógico principal será um perfil de domínio e fragilidade por habilidade.

Esse perfil será construído por meio da agregação controlada das probabilidades e evidências associadas a cada habilidade. A saída deverá preservar:

- habilidade analisada;
- quantidade e recência das evidências;
- probabilidade estimada;
- intervalo ou indicador de incerteza, quando aplicável;
- nível ordinal derivado;
- limitações de interpretação;
- versão do conjunto de dados e do modelo.

O perfil deverá indicar onde existem evidências de maior ou menor dificuldade, sem rotular o estudante de forma permanente.

## 7. Resultados derivados

### 7.1 Nível ordinal

Um nível ordinal poderá ser derivado da probabilidade contínua para facilitar a interpretação, desde que:

- os limites sejam definidos antes da avaliação final;
- a justificativa seja registrada;
- seja realizada análise de sensibilidade aos pontos de corte;
- a probabilidade original continue disponível;
- os níveis não sejam apresentados como categorias naturais ou definitivas.

Exemplos provisórios de linguagem incluem:

- evidência insuficiente;
- fragilidade elevada;
- habilidade em desenvolvimento;
- domínio provável.

Os nomes e limites definitivos dependerão da base, da literatura e da calibração observada.

### 7.2 Alerta binário

Um alerta binário de acompanhamento prioritário poderá ser produzido como saída secundária. Ele deverá ser derivado do perfil por habilidade e nunca substituir a informação probabilística e contextual.

O alerta não será denominado diagnóstico, reprovação provável ou incapacidade. Sua finalidade será apenas apoiar triagem docente sujeita a revisão humana.

## 8. Hipóteses de pesquisa iniciais

As hipóteses iniciais serão testadas e poderão ser refinadas após a seleção definitiva da base:

- **H1:** modelos que incorporam histórico por habilidade apresentam melhor desempenho preditivo do que referências baseadas apenas na frequência global de acertos;
- **H2:** pelo menos um modelo não linear apresenta ganho mensurável sobre a regressão logística, sem perda desproporcional de calibração ou interpretabilidade;
- **H3:** a agregação por habilidade produz perfis mais informativos para análise de erros do que uma única pontuação global;
- **H4:** o desempenho e a calibração variam entre habilidades e subgrupos disponíveis na base, exigindo análise estratificada;
- **H5:** explicações baseadas em atributos históricos podem ser apresentadas de forma rastreável, mas não autorizam inferências causais sobre o estudante.

## 9. Modelos de referência

Todo modelo candidato deverá ser comparado a referências simples. O conjunto inicial incluirá, conforme compatibilidade com a base:

1. frequência global de acertos;
2. frequência histórica de acertos por estudante;
3. frequência histórica de acertos por habilidade;
4. regressão logística regularizada;
5. pelo menos um modelo não linear baseado em árvores.

Modelos mais complexos, incluindo técnicas de rastreamento de conhecimento ou modelos sequenciais, somente serão incorporados após a existência de baselines reproduzíveis e de uma justificativa baseada na literatura e na estrutura temporal dos dados.

## 10. Avaliação técnica

A avaliação principal deverá considerar:

- ROC-AUC;
- PR-AUC;
- log-loss;
- Brier Score;
- curvas e erro de calibração;
- precisão, revocação e F1 em limites previamente definidos;
- desempenho por habilidade;
- desempenho por subgrupos disponíveis e eticamente utilizáveis;
- estabilidade entre diferentes sementes e divisões de dados.

A divisão entre treino, validação e teste deverá impedir vazamento temporal e vazamento entre registros relacionados. A estratégia definitiva dependerá da estrutura da base e será registrada antes da avaliação final.

## 11. Interpretabilidade

A interpretação deverá ocorrer em dois níveis:

- **global:** identificação de padrões gerais associados às estimativas do modelo;
- **local:** apresentação dos fatores que contribuíram para uma estimativa específica.

As explicações deverão ser acompanhadas de alertas explícitos de que associação estatística não representa causalidade. Variáveis sensíveis ou contextuais não poderão ser utilizadas para justificar expectativas deterministas sobre estudantes.

## 12. Limites das conclusões

O experimento poderá sustentar conclusões sobre:

- desempenho preditivo na base selecionada;
- calibração das probabilidades;
- diferenças de desempenho entre habilidades;
- estabilidade e rastreabilidade das explicações;
- viabilidade técnica do pipeline e do perfil pedagógico proposto.

O experimento não poderá, sem estudo adicional apropriado, sustentar conclusões sobre:

- melhoria efetiva da aprendizagem;
- eficácia em sala de aula;
- causalidade entre atributos e dificuldades;
- diagnóstico psicológico, cognitivo ou clínico;
- generalização automática para estudantes brasileiros quando a base não representar esse contexto;
- substituição do julgamento docente.

## 13. Reprodutibilidade e rastreabilidade

Cada experimento deverá registrar:

- origem e versão dos dados;
- transformação aplicada a cada variável;
- critérios de inclusão e exclusão;
- divisão dos conjuntos;
- sementes aleatórias;
- versão das dependências;
- configuração do modelo;
- métricas e artefatos gerados;
- commit de origem;
- limitações conhecidas.

Resultados somente poderão ser incorporados ao texto do TCC depois de reproduzidos por código versionado e validados pelos testes correspondentes.

## 14. Estado da decisão

**Status:** aprovado para implementação.

**Dependência:** PR nº 6, que estabelece a fundamentação teórica, a revisão sistemática e a especificação conceitual inicial.

**Issue de acompanhamento:** #7.
