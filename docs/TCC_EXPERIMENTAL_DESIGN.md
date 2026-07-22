# Desenho experimental do protótipo

## Pergunta de pesquisa operacional

Em que medida modelos computacionais probabilísticos e interpretáveis conseguem estimar a correção da próxima resposta de um estudante em uma habilidade matemática e transformar essas estimativas em um perfil de domínio e fragilidade útil ao apoio da decisão docente?

A pergunta foi formulada para permitir avaliação técnica reproduzível sem afirmar, por extensão indevida, que uma boa previsão comprova aprendizagem ou eficácia pedagógica.

## Unidade de análise

A unidade mínima será uma interação entre estudante e item:

- estudante anonimizado;
- item ou questão;
- uma ou mais habilidades associadas;
- posição temporal ou timestamp;
- resposta observada;
- indicador de correção;
- tentativas, dicas e tempo, quando disponíveis;
- proveniência do conjunto de dados.

Interações sem possibilidade de ordenação temporal não serão usadas no protocolo principal de previsão da próxima resposta.

## Variável-alvo

### Alvo primário

`correct_next ∈ {0, 1}` indica se a próxima resposta registrada para o estudante foi correta.

O alvo deve ser obtido exclusivamente da interação futura em relação ao conjunto de atributos construído. Nenhuma variável posterior à resposta pode ser utilizada no treinamento ou na inferência.

### Saída contínua

O modelo produzirá `P(correct_next = 1 | history, item, skill)`, interpretada como probabilidade estimada de acerto sob as condições representadas pelos dados.

A probabilidade não será chamada automaticamente de aprendizagem, competência ou domínio verdadeiro. Ela será uma estimativa operacional associada ao histórico disponível.

### Resultado pedagógico derivado

Probabilidades de interações pertencentes a uma mesma habilidade poderão ser agregadas em um perfil de domínio e fragilidade. A regra de agregação, a janela histórica e os intervalos de interpretação serão definidos e versionados antes da análise final.

Níveis ordinais e alertas binários serão produtos derivados. Eles não substituirão a probabilidade original e não serão apresentados como diagnósticos definitivos.

## Hipóteses

- **H1:** atributos históricos simples por estudante, item e habilidade produzirão melhor log-loss e Brier Score que a probabilidade global de acerto.
- **H2:** regressão logística regularizada produzirá um baseline competitivo e mais facilmente interpretável.
- **H3:** pelo menos um modelo não linear poderá melhorar discriminação, mas o ganho deverá ser analisado junto à calibração e ao custo de explicação.
- **H4:** o desempenho e a calibração variarão entre habilidades, exigindo análise desagregada.
- **H5:** um perfil por habilidade preservará mais informação pedagógica que um único rótulo binário de risco.

As hipóteses serão testadas, não presumidas como verdadeiras.

## Protocolos de divisão

Serão utilizados dois cenários complementares.

### Generalização para estudantes não observados

Os identificadores de estudante serão separados entre treino, validação e teste. Nenhum estudante do conjunto de teste poderá aparecer no treino. Esse cenário estima a capacidade de generalização para novos estudantes.

### Previsão temporal personalizada

Para estudantes com histórico suficiente, as interações serão ordenadas. A parte inicial formará o histórico de treino, seguida por validação e teste futuros. A construção dos atributos em cada linha usará apenas eventos anteriores à linha prevista.

A divisão aleatória por linha será proibida no protocolo principal, pois permitiria que eventos futuros ou interações do mesmo estudante contaminassem o treinamento.

## Critérios mínimos de inclusão

A configuração inicial exigirá:

- identificador anônimo de estudante;
- identificador de item;
- indicador de correção;
- ordem temporal estável;
- pelo menos uma habilidade ou conceito por item;
- número mínimo configurável de interações por estudante;
- documentação da origem e licença.

Registros duplicados, impossíveis ou posteriores ao evento previsto serão removidos por regras explícitas e contabilizados no relatório de qualidade.

## Modelos de referência

A comparação começará por modelos simples:

1. probabilidade global de acerto;
2. probabilidade histórica por item;
3. probabilidade histórica por habilidade;
4. média histórica do estudante com suavização;
5. regressão logística regularizada.

Um modelo não linear baseado em árvores será adicionado somente depois que os baselines estiverem validados. Modelos sequenciais profundos e knowledge tracing avançado serão extensões, não requisitos do primeiro experimento.

## Atributos candidatos

Somente atributos disponíveis antes da resposta prevista poderão ser usados:

- quantidade de interações anteriores;
- taxa histórica de acerto do estudante;
- taxa histórica do estudante na habilidade;
- dificuldade histórica do item calculada apenas no treino;
- número de tentativas anteriores;
- uso histórico de dicas;
- tempo histórico mediano ou transformado;
- intervalo desde a interação anterior;
- posição da interação na sessão;
- habilidade e item codificados de forma apropriada.

Atributos demográficos não serão utilizados no modelo principal para gerar classificações individuais. Quando disponíveis e permitidos, poderão ser usados apenas para auditoria de desempenho e calibração entre subgrupos.

## Métricas

### Métricas primárias

- log-loss;
- Brier Score.

Essas métricas avaliam a qualidade das probabilidades e penalizam previsões excessivamente confiantes e incorretas.

### Métricas secundárias

- ROC-AUC;
- PR-AUC;
- acurácia em limiar previamente definido;
- precisão, revocação e F1;
- erro esperado de calibração;
- curvas de confiabilidade.

As métricas serão apresentadas globalmente e por habilidade quando houver suporte amostral mínimo.

## Comparação e incerteza

- todos os modelos usarão as mesmas partições;
- seeds, parâmetros e versões serão registrados;
- intervalos de confiança serão estimados por bootstrap agrupado por estudante quando computacionalmente viável;
- diferenças pequenas não serão interpretadas apenas pelo valor pontual;
- modelos mais complexos somente serão preferidos quando o ganho for consistente e relevante.

## Interpretabilidade

A regressão logística fornecerá coeficientes e efeitos direcionais. Para modelos de árvore, serão avaliadas explicações globais e locais com SHAP ou método equivalente.

A interpretação deverá distinguir:

- associação estatística;
- importância para o modelo;
- explicação da previsão;
- causa da dificuldade;
- recomendação pedagógica.

Somente as três primeiras podem ser obtidas diretamente do experimento preditivo.

## Perfil por habilidade

O perfil será calculado a partir de previsões e evidências observadas, contendo:

- habilidade;
- probabilidade estimada;
- quantidade de evidências;
- intervalo ou medida de incerteza;
- período considerado;
- versão do modelo;
- limitações de interpretação.

Habilidades com poucas evidências serão marcadas como insuficientes em vez de receberem classificação forte.

## Auditoria de equidade

Quando os dados e a licença permitirem, serão comparados:

- log-loss e Brier Score por subgrupo;
- calibração por subgrupo;
- taxas de falso positivo e falso negativo para alertas derivados;
- cobertura de habilidades e quantidade de interações.

Diferenças observadas serão descritas como propriedades do modelo no conjunto analisado, não como características naturais dos grupos.

## Critérios de conclusão

O lote experimental será considerado executado quando:

1. todas as partições forem reproduzíveis;
2. os baselines e pelo menos um modelo não linear forem comparados;
3. a calibração for avaliada;
4. os resultados forem desagregados por habilidade;
5. os artefatos forem gerados por código;
6. limitações de generalização forem registradas;
7. nenhuma métrica for descrita como prova de melhoria da aprendizagem.

## Prática de ciência aberta

O repositório deverá conter:

- manifesto do conjunto de dados sem redistribuir arquivos proibidos;
- script de download ou instruções verificáveis;
- hashes dos arquivos brutos;
- contrato de esquema;
- configuração do experimento;
- código de preparação, treino e avaliação;
- ambiente versionado;
- tabelas e figuras geradas automaticamente;
- registro de exclusões e transformações.
