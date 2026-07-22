# Protótipo do TCC

Este módulo implementa o pipeline reproduzível que transforma conjuntos educacionais autorizados em interações canônicas e executa experimentos probabilísticos para o TCC.

## Princípios

- o arquivo bruto nunca é modificado;
- a execução exige manifesto com proveniência e SHA-256;
- versões ou hashes desconhecidos interrompem o fluxo;
- os dados brutos e processados ficam fora do Git;
- relatórios registram contagens, exclusões e hashes;
- dados sintéticos são utilizados no CI, não como evidência educacional;
- atributos de uma resposta usam somente eventos anteriores;
- estudantes ou períodos futuros não podem contaminar o treinamento;
- métricas preditivas não são tratadas como prova de aprendizagem;
- explicações descrevem o modelo e não estabelecem causalidade.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Preparar ASSISTments

1. obtenha a versão corrigida do Skill Builder 2009–2010 pela página oficial;
2. salve o arquivo em `data/raw/`;
3. crie um manifesto em `data/manifests/` conforme `contracts/dataset_manifest.schema.json`;
4. registre o SHA-256 do arquivo efetivamente obtido;
5. execute:

```bash
tcc-prototype prepare-assistments \
  --manifest data/manifests/assistments.json \
  --raw-dir data/raw \
  --output-dir data/processed
```

A execução produz:

- `*.parquet`: tabela normalizada de interações;
- `*.quality.json`: relatório de qualidade, contagens e hashes.

## Executar os baselines

O protocolo compara duas formas de divisão:

- `cold_start`: estudantes inteiros ficam restritos a uma partição;
- `temporal`: o passado de cada estudante antecede validação e teste.

```bash
tcc-prototype evaluate-baselines \
  --input data/processed/assistments_2009_2010_skill_builder_corrected.parquet \
  --output-dir data/reports \
  --split-strategy temporal \
  --seed 2026 \
  --minimum-skill-rows 100
```

São avaliados:

- probabilidade global;
- probabilidade suavizada por item;
- probabilidade suavizada por habilidade;
- probabilidade suavizada pelo histórico do estudante;
- regressão logística regularizada com atributos históricos e variáveis categóricas.

As métricas incluem log-loss, Brier Score, ROC-AUC, precisão média, acurácia, precisão, revocação, F1 e erro esperado de calibração. As saídas incluem métricas, previsões e atribuições das partições.

## Avaliar o candidato não linear

A Random Forest é executada nas mesmas partições dos baselines:

```bash
tcc-prototype evaluate-candidate \
  --input data/processed/assistments_2009_2010_skill_builder_corrected.parquet \
  --output-dir data/reports \
  --split-strategy temporal \
  --seed 2026 \
  --n-estimators 300 \
  --min-samples-leaf 5 \
  --minimum-profile-evidence 5
```

O comando produz:

- métricas dos baselines e da Random Forest;
- previsões do teste;
- importância por permutação das variáveis originais;
- explicações locais exatas da regressão logística em log-odds;
- perfil por estudante e habilidade;
- avisos obrigatórios de interpretação.

A Random Forest é apenas um modelo candidato. A preferência por ela exige ganho consistente em relação aos baselines, calibração adequada, estabilidade e custo interpretativo aceitável.

## Perfil por habilidade

O perfil contínuo contém:

- probabilidade média estimada;
- dispersão das previsões;
- quantidade de evidências;
- acurácia observada;
- intervalo de Wilson da proporção observada;
- estado de suficiência das evidências.

Os níveis ordinais e o alerta binário permanecem desabilitados em `config/profile.json`. O código somente gera níveis quando recebe limiares explícitos e versionados. Esse mecanismo permite testar uma futura regra sem transformar limites arbitrários em resultado científico.

## Contrato canônico

Cada interação contém, no mínimo:

- estudante anonimizado;
- item;
- habilidade ou conjunto de habilidades;
- ordem da interação;
- correção da resposta;
- conjunto de origem;
- identificador rastreável da linha original.

Campos como timestamp, tentativas, dicas e tempo são preservados quando disponíveis.

No primeiro experimento, interações com múltiplas habilidades recebem uma habilidade primária determinística para comparação dos modelos iniciais. O conjunto original de habilidades permanece preservado para modelos e análises posteriores.

## Testes

```bash
python -m pytest tests
```

Os testes usam arquivos temporários sintéticos e verificam:

- integridade do manifesto e rejeição de hash divergente;
- normalização do ASSISTments e remoção de duplicatas;
- atributos baseados exclusivamente no histórico anterior;
- separação de estudantes e ordem temporal;
- suavização e fallback dos baselines;
- métricas probabilísticas e calibração;
- determinismo do candidato não linear;
- reconstrução exata das predições logísticas por contribuições;
- suficiência de evidências e ativação explícita de limiares;
- geração dos artefatos de cada experimento.

## Extensões

Novas fontes serão integradas por adaptadores independentes. Cada adaptador deverá produzir o mesmo contrato canônico e seus próprios testes, evitando que regras específicas de uma base contaminem o restante do pipeline.

SHAP poderá ser acrescentado após a execução real caso apresente estabilidade e valor comunicacional superior às explicações já implementadas. Nenhuma extensão será incorporada à redação dos resultados antes da geração reproduzível dos artefatos.
