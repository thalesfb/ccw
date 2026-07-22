# Perfil por habilidade e explicabilidade

## Finalidade

O perfil por habilidade organiza evidências para apoiar a análise docente. Ele não mede diretamente aprendizagem, não substitui avaliação pedagógica e não autoriza classificação permanente do estudante.

## Componentes do perfil

Para cada combinação estudante–habilidade, o protótipo registra:

- quantidade de interações utilizadas;
- probabilidade média estimada pelo modelo;
- dispersão das probabilidades;
- acurácia observada no período;
- intervalo de Wilson para a acurácia observada;
- estado da evidência;
- versão de eventuais limiares;
- aviso obrigatório de interpretação.

O intervalo de Wilson descreve a incerteza da proporção observada, não um intervalo de confiança completo para a probabilidade do modelo. Essa distinção deve permanecer explícita na redação e na interface.

## Evidência insuficiente

Uma habilidade com menos interações que o mínimo configurado recebe o estado `insufficient_evidence`. O sistema não completa dados ausentes com um rótulo forte e não confunde falta de observação com fragilidade.

## Níveis ordinais

Os níveis ordinais estão desabilitados por padrão. A ativação exige:

1. limiares definidos em uma configuração versionada;
2. análise na validação, sem escolher os limites pelo desempenho do teste;
3. estabilidade entre seeds e partições;
4. avaliação dos custos de classificações incorretas;
5. revisão pedagógica dos nomes e interpretações;
6. documentação da população e do período de validade.

Os rótulos previstos no código são operacionais:

- `high_fragility`;
- `monitoring`;
- `developing`;
- `probable_mastery`.

Mesmo quando ativados, esses rótulos continuarão acompanhados da probabilidade, quantidade de evidências e aviso de limitação.

## Modelo não linear

O candidato não linear inicial é uma Random Forest. Sua escolha decorre de três fatores:

- recorrência em estudos de mineração de dados educacionais incluídos na revisão;
- capacidade de representar relações não lineares e interações;
- possibilidade de comparação direta com baselines simples.

A Random Forest não é considerada superior por definição. Ela somente poderá ser escolhida após comparação em partições idênticas, considerando log-loss, Brier Score, calibração, estabilidade, custo computacional e interpretação.

## Explicações

### Regressão logística

A regressão logística permite decompor cada predição em:

- intercepto;
- valor transformado da variável;
- coeficiente;
- contribuição em log-odds.

A soma das contribuições e do intercepto reconstrói exatamente a saída linear do modelo. Isso fornece rastreabilidade matemática da previsão.

### Random Forest

A importância global inicial é estimada por permutação nas variáveis de entrada originais. A análise mede quanto o desempenho preditivo se altera quando uma variável é embaralhada. Ela não estabelece causalidade e pode distribuir importância entre variáveis correlacionadas.

SHAP permanece uma extensão possível. Sua adoção dependerá da estabilidade das explicações, do custo computacional e da capacidade de comunicar os resultados sem extrapolação causal.

## Linguagem permitida

Exemplos adequados:

- “A variável contribuiu para elevar a probabilidade estimada pelo modelo.”
- “O modelo apresentou maior dependência preditiva desta variável no conjunto analisado.”
- “A habilidade possui poucas evidências e não recebeu classificação ordinal.”

Exemplos inadequados:

- “A variável causou a dificuldade do estudante.”
- “O estudante não aprendeu a habilidade.”
- “A inteligência artificial diagnosticou uma deficiência.”
- “A recomendação melhora a aprendizagem.”

## Participação docente

O professor poderá:

- examinar as evidências associadas ao perfil;
- considerar o contexto da atividade e da turma;
- rejeitar ou revisar interpretações;
- registrar uma decisão independente da estimativa;
- solicitar nova evidência antes de qualquer intervenção.

A interface deverá apresentar o modelo como apoio à decisão e preservar a autonomia profissional docente.
