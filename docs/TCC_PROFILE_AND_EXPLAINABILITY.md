# Perfil de evidências por habilidade e explicabilidade

## Finalidade

O perfil por habilidade organiza evidências técnicas produzidas pelo protocolo
preditivo para permitir inspeção auditável posterior. Ele resume desempenho
observado e probabilidades contextuais de acerto em interações retidas para
teste. Não mede diretamente aprendizagem, domínio, competência latente ou
causalidade, não constitui diagnóstico e não demonstra eficácia pedagógica.

O lote de perfil é uma camada derivada do experimento consolidado. Ele não cria
uma segunda avaliação: não escolhe novos splits, não seleciona seeds, não ajusta
hiperparâmetros e não substitui os artefatos produzidos pela avaliação.

## Dependência do experimento congelado

A execução consome um diretório imutável produzido pelo protocolo experimental,
contendo pelo menos:

- `metrics.json`;
- `predictions.parquet`;
- `splits.parquet`;
- `input-provenance.json`.

Antes de ler o conjunto canônico, a CLI recalcula seu SHA-256 e exige igualdade
com `processed_input_sha256` registrado em `input-provenance.json`. As previsões
e os splits também têm seus hashes recalculados e comparados aos valores
registrados em `metrics.json`.

Assim, o perfil permanece ligado ao mesmo artefato processado, à mesma fonte, à
mesma configuração experimental e às mesmas partições que originaram as
previsões analisadas.

## Fonte probabilística

`probability_source` identifica qual coluna de probabilidade do experimento
alimenta o perfil. Essa escolha não pode ser realizada examinando o perfil ou o
resultado do teste. Ela deve ser justificada a partir da validação e congelada
antes da geração do perfil de teste.

Por esse motivo, `prototype/config/profile.json` mantém
`probability_source: null` até que exista uma decisão registrada. A execução é
interrompida enquanto essa decisão não for congelada.

O perfil usa o modelo selecionado apenas como fonte das probabilidades
contextuais já registradas. A explicação matemática da regressão logística é um
artefato independente de rastreabilidade e não implica que a regressão logística
seja automaticamente escolhida como fonte do perfil.

## Evidência estudante-habilidade

Cada interação continua sendo uma única unidade estudante-item. Para o relatório
por habilidade, a mesma interação pode contribuir para cada habilidade mapeada em
`skill_ids`. Não existe seleção de `primary_skill_id` e não há explosão da linha
canônica de treinamento.

Para cada combinação estudante-habilidade, são registrados:

- `evidence_count`: número de interações únicas disponíveis;
- `mean_predicted_correct_probability`: média das probabilidades contextuais de
  resposta correta nas interações incluídas;
- `predicted_probability_dispersion`: desvio-padrão dessas probabilidades
  contextuais;
- `observed_accuracy`: proporção observada de respostas corretas;
- `observed_accuracy_lower` e `observed_accuracy_upper`: intervalo de Wilson da
  proporção observada;
- `evidence_status`: `reported` ou `insufficient_evidence`;
- fonte probabilística e aviso obrigatório de interpretação.

`mean_predicted_correct_probability` não é probabilidade de domínio da
habilidade. Por exemplo, uma média de 0,60 significa que, nas interações daquela
habilidade incluídas no perfil, o modelo atribuiu em média 60% de probabilidade
de resposta correta. Não significa que o estudante “domina 60%” da habilidade.

`predicted_probability_dispersion` mede variação entre probabilidades
contextuais. Ela não é intervalo de confiança, erro-padrão ou incerteza completa
do modelo.

O intervalo de Wilson se refere exclusivamente à proporção observada de acertos.
Ele não é um intervalo de confiança da probabilidade produzida pelo modelo.

## Evidência insuficiente

`minimum_student_skill_interactions` também permanece nulo no contrato padrão.
O valor deve ser justificado após a caracterização da base e congelado antes da
geração do perfil no teste.

Quando um grupo estudante-habilidade não atinge esse suporte, ele recebe
`insufficient_evidence`. Ausência ou escassez de observações não é convertida em
fragilidade, dificuldade ou baixa competência.

## Níveis ordinais e alertas

Níveis ordinais e alerta binário permanecem desabilitados. Este lote não
implementa classificações como “domínio provável”, “fragilidade” ou equivalentes.

Uma futura ativação exigiria, em estudo separado:

1. limiares definidos antes da avaliação no teste;
2. análise dos custos de erros de classificação;
3. evidência de calibração e estabilidade;
4. análise da população e período de validade;
5. revisão pedagógica da semântica e do uso humano;
6. documentação versionada da decisão.

## Reconstrução verificável da regressão logística

Para explicar a regressão logística, o protótipo reconstrói somente a
especificação já congelada no experimento:

1. recupera do artefato os mesmos `source_row_id` de treino e teste;
2. reconstrói os atributos históricos a partir das interações canônicas;
3. recupera `C`, `max_iter` e a seed já registrados;
4. ajusta a regressão apenas no treino registrado;
5. recalcula as probabilidades do teste;
6. exige que elas coincidam com `logistic_regression_probability` armazenada em
   `predictions.parquet` dentro da tolerância numérica definida.

Se a reprodução falhar, nenhuma explicação é aceita. Esse ajuste não constitui
novo tuning nem novo experimento; ele é uma verificação determinística da
execução registrada.

### Contribuições locais

Para cada linha explicada, a saída registra intercepto, valor transformado,
coeficiente e produto entre valor e coeficiente. A soma das contribuições com o
intercepto reconstrói exatamente o log-odds da regressão logística.

Essas contribuições descrevem o cálculo do modelo. Frases causais como “esta
variável causou a dificuldade” não são autorizadas.

### Importância por permutação

A importância global é calculada sobre as variáveis de entrada da regressão
reconstruída usando log-loss no conjunto de teste registrado. O resultado mede a
alteração do desempenho preditivo quando uma variável é permutada.

Importância por permutação não estabelece causalidade e pode ser redistribuída
entre atributos correlacionados. O uso do teste é exclusivamente descritivo e
não retorna ao ciclo de seleção, tuning ou definição da fonte probabilística.

## Proveniência e imutabilidade

Uma execução de perfil é identificada pelo hash de `metrics.json` do experimento
e pelo hash da configuração de perfil. O diretório não pode ser sobrescrito.

`profile-manifest.json` registra, entre outros elementos:

- hashes da fonte, configuração experimental, métricas, previsões e splits;
- hash da configuração do perfil;
- fonte probabilística e suporte mínimo congelados;
- quantidade de linhas de explicação e repetições da permutação;
- erro máximo da reprodução das probabilidades logísticas;
- hashes dos artefatos derivados;
- salvaguarda de interpretação.

## Linguagem autorizada

Exemplos compatíveis com o protocolo:

- “A probabilidade média estimada de acerto nas interações analisadas foi 0,60.”
- “O histórico possui evidência insuficiente para relatar este perfil com o
  suporte configurado.”
- “A variável apresentou maior dependência preditiva no modelo analisado.”
- “Esta contribuição aumenta o log-odds calculado pela regressão logística.”

Exemplos incompatíveis:

- “O estudante domina a habilidade em 60%.”
- “O estudante não aprendeu frações.”
- “A variável causou a dificuldade.”
- “O sistema diagnosticou deficiência.”
- “A recomendação melhora a aprendizagem.”

## Participação docente

Um produto educacional futuro poderá apresentar essas evidências ao professor
como apoio à inspeção, preservando contexto, possibilidade de rejeição e decisão
profissional independente. Essa possibilidade de uso não foi validada neste
lote e não deve ser apresentada como evidência de utilidade docente ou impacto
pedagógico.
