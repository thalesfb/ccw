# Protótipo do TCC

Este módulo implementa o pipeline reproduzível que transforma conjuntos educacionais autorizados em interações canônicas e executa o protocolo técnico de avaliação do TCC.

## Princípios

- o arquivo bruto nunca é modificado;
- a execução exige manifesto com proveniência e SHA-256;
- versões ou hashes desconhecidos interrompem o fluxo;
- os dados brutos e processados ficam fora do Git;
- relatórios registram contagens, exclusões, parâmetros, versões e hashes;
- dados sintéticos são utilizados no CI, não como evidência educacional;
- atributos de uma resposta usam somente informações disponíveis antes da resposta-alvo;
- o conjunto de teste não seleciona suavização, hiperparâmetros, limiares ou regras de calibração;
- métricas preditivas não são tratadas como prova de aprendizagem ou eficácia pedagógica.

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

A execução produz nomes versionados pelo SHA-256 completo da fonte, como
`<dataset_id>-<sha256>.parquet` e `<dataset_id>-<sha256>.quality.json`. Assim,
uma republicação do arquivo bruto não sobrescreve silenciosamente os artefatos
de uma versão anterior.

## Semântica do ASSISTments corrigido

O comando aceita somente o identificador aprovado
`assistments_2009_2010_skill_builder_corrected`. O adaptador assume a versão
corrigida do Skill Builder 2009–2010, na qual uma interação estudante-problema
ocupa uma única linha. Se detectar a codificação legada em várias linhas, a
execução é interrompida.

Quando `skill_id` representa várias habilidades no formato `skill1_skill2`, o
adaptador preserva essas tags separadamente em `skill_ids`, sem criar linhas
artificiais adicionais. Essa codificação é fixa para a fonte aprovada e não é
um parâmetro ajustável do experimento.

O campo `order_id` é usado como ordem cronológica da interação. O campo
`correct` é preservado como o rótulo observado da interação e significa acerto
na primeira tentativa; uma primeira resposta incorreta ou um pedido de ajuda é
registrado como incorreto. Tentativas, dicas e tempo da própria interação são
preservados somente como campos observados e continuam proibidos como atributos
da mesma interação no protocolo preditivo definido no TCC.

## Avaliar modelos de referência

O comando de avaliação implementa os cenários `student_holdout` e
`personalized_temporal` definidos no contrato experimental. A seleção de
hiperparâmetros usa o `log_loss` da validação a partir de modelos ajustados
somente no treino; o teste não participa da escolha. Todas as seeds registradas
em `config/experiment.json` são executadas, e a CLI não oferece uma opção para
selecionar retrospectivamente apenas uma seed.

Modelos implementados:

- probabilidade global;
- probabilidade histórica suavizada por item;
- probabilidade histórica suavizada pelas habilidades mapeadas;
- probabilidade suavizada pelo histórico anterior do estudante;
- regressão logística regularizada;
- `HistGradientBoostingClassifier` como candidato não linear exploratório.

A regressão logística usa o item e a representação determinística do conjunto
completo de habilidades, sem escolher uma habilidade primária. O modelo não
linear usa atributos históricos numéricos e hashing determinístico do item e de
todas as habilidades. O hashing não usa o alvo, possui largura fixa e aceita
categorias inéditas sem ajuste no teste. O `early_stopping` é desativado para
não criar uma partição implícita fora do protocolo versionado.

As taxas históricas começam com os pseudocontadores versionados em
`evaluation_execution.history_rate_prior`. O código expõe os mesmos valores
como defaults explícitos e os testes de contrato impedem que configuração e
runtime divirjam silenciosamente.

Antes da primeira execução com dados reais, os limiares ainda nulos de
eligibilidade e suporte por habilidade em `config/experiment.json` precisam ser
justificados e congelados após a caracterização da base. Enquanto isso não
ocorrer, a CLI interrompe a avaliação em vez de inventar valores padrão.

A avaliação também exige o relatório `.quality.json` gerado pelo pipeline de
preparação. Antes de ler o Parquet, a CLI recalcula seu SHA-256 e exige igualdade
com `processed_sha256` do relatório. O hash bruto original permanece separado em
`source_sha256`, preservando a cadeia arquivo bruto -> artefato processado ->
execução experimental.

Exemplo após o congelamento desses critérios:

```bash
tcc-prototype evaluate-baselines \
  --input data/processed/<dataset>-<sha256>.parquet \
  --preparation-report data/processed/<dataset>-<sha256>.quality.json \
  --output-dir data/reports \
  --experiment-config config/experiment.json \
  --split-strategy student_holdout
```

Cada seed gera um diretório imutável identificado pelo hash do input processado,
pelo SHA-256 bruto da fonte, pelo hash da configuração, pela estratégia de split
e pela seed. Os artefatos incluem `metrics.json`, `predictions.parquet`,
`splits.parquet` e `input-provenance.json`. Este último registra separadamente o
hash da fonte bruta, do Parquet processado, do relatório de preparação e da
configuração experimental.

As comparações principais usam bootstrap pareado por estudante. O relatório por
habilidade associa uma interação a todas as habilidades mapeadas e conta
interações únicas e estudantes únicos. Como o contrato canônico atual não
contém colunas de subgrupo aprovadas para auditoria, o artefato registra essa
análise como não aplicável em vez de fabricar grupos.

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

## Testes

```bash
python -m pytest tests
```

Os testes usam arquivos temporários sintéticos e verificam o pipeline de dados,
a construção de atributos apenas com histórico anterior, as duas divisões
experimentais, os baselines, a regressão logística, o candidato não linear, as
métricas probabilísticas e de calibração, o bootstrap pareado por estudante, o
suporte multihabilidade, o bloqueio de critérios não congelados, a cadeia de
proveniência do Parquet e a geração de artefatos imutáveis.

## Limites

A implementação torna o protocolo executável, mas não produz por si só
evidência educacional. Resultados sintéticos do CI servem somente para regressão
técnica. Métricas em dados reais poderão sustentar conclusões sobre desempenho
preditivo e calibração no conjunto analisado, não sobre aprendizagem,
competência latente, causalidade ou eficácia pedagógica.

Modelos de explicabilidade e o perfil pedagógico são tratados nos lotes
seguintes, depois da consolidação dos baselines e da avaliação técnica real.
