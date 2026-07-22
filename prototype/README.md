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
- métricas preditivas não são tratadas como prova de aprendizagem.

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

Exemplo:

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

As métricas incluem log-loss, Brier Score, ROC-AUC, precisão média, acurácia, precisão, revocação, F1 e erro esperado de calibração. As saídas incluem:

- métricas globais e por habilidade em JSON;
- previsões do conjunto de teste em Parquet;
- atribuição de todas as linhas às partições em Parquet.

O modelo de regressão usa apenas contagens e taxas anteriores à resposta atual. Para itens ou habilidades inéditos, o pré-processamento ignora categorias desconhecidas sem consultar o conjunto de teste durante o ajuste.

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

No primeiro experimento, interações com múltiplas habilidades recebem uma habilidade primária determinística apenas para os baselines. O conjunto original de habilidades permanece preservado para modelos e análises posteriores.

## Testes

```bash
python -m pytest tests
```

Os testes usam arquivos temporários sintéticos e verificam:

- integridade do manifesto;
- rejeição de hash divergente;
- mapeamento do ASSISTments para o contrato canônico;
- remoção de duplicatas exatas;
- ordenação determinística;
- geração do Parquet e do relatório de qualidade;
- atributos baseados exclusivamente no histórico anterior;
- separação de estudantes e ordem temporal;
- suavização e fallback dos baselines;
- métricas probabilísticas e calibração;
- geração de artefatos do experimento.

## Extensões planejadas

Novas fontes serão integradas por adaptadores independentes. Cada adaptador deverá produzir o mesmo contrato canônico e seus próprios testes, evitando que regras específicas de uma base contaminem o restante do pipeline.

Modelos não lineares, explicabilidade e perfil pedagógico serão adicionados somente depois que os baselines forem executados na base real e seus resultados forem congelados para comparação.
