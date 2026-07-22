# Protótipo do TCC

Este módulo implementa o pipeline reproduzível que adquire conjuntos educacionais autorizados, transforma-os em interações canônicas, executa experimentos probabilísticos e gera um relatório docente autônomo.

## Princípios

- o uso da base exige leitura e aceite dos termos aplicáveis;
- o arquivo bruto nunca é modificado nem redistribuído;
- a execução exige manifesto com proveniência e SHA-256;
- versões ou hashes desconhecidos interrompem o fluxo;
- os dados brutos e processados ficam fora do Git;
- relatórios registram contagens, exclusões e hashes;
- dados sintéticos são utilizados no CI, não como evidência educacional;
- atributos de uma resposta usam somente eventos anteriores;
- estudantes ou períodos futuros não podem contaminar o treinamento;
- métricas preditivas não são tratadas como prova de aprendizagem;
- explicações descrevem o modelo e não estabelecem causalidade;
- identificadores estudantis não são inseridos diretamente no relatório HTML.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Adquirir a base ASSISTments

Antes da aquisição, leia:

- a página canônica do conjunto corrigido;
- os termos oficiais de uso de dados anonimizados.

O comando exige aceite explícito e uma finalidade científica concreta:

```bash
tcc-prototype acquire-assistments \
  --raw-dir data/raw \
  --manifest-dir data/manifests \
  --purpose "Experimento reproduzível do TCC sobre perfis de habilidades matemáticas" \
  --accept-terms
```

A execução:

- baixa a versão corrigida e colapsada para `data/raw/`;
- calcula SHA-256 e tamanho;
- registra data, finalidade, URL dos termos e evidência do aceite;
- marca a redistribuição como proibida;
- não adiciona o arquivo bruto ao Git.

O aceite implica não tentar reidentificação, não redistribuir dados estudantis, comunicar informação identificável encontrada, reconhecer o ASSISTments e manter público o código científico associado à publicação.

## Preparar ASSISTments

Use o manifesto gerado pela aquisição:

```bash
tcc-prototype prepare-assistments \
  --manifest data/manifests/assistments_2009_2010_skill_builder_corrected.json \
  --raw-dir data/raw \
  --output-dir data/processed
```

A execução valida tamanho e hash, então produz uma tabela Parquet normalizada e um relatório JSON de qualidade, contagens e hashes.

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

São avaliados probabilidade global, probabilidades suavizadas por item, habilidade e estudante, além de regressão logística. As métricas incluem log-loss, Brier Score, ROC-AUC, precisão média, métricas de classificação e erro esperado de calibração.

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

O comando produz métricas, previsões, importância por permutação, explicações logísticas, perfis por habilidade e avisos de interpretação. A Random Forest é apenas um candidato; sua preferência exige ganho consistente, calibração, estabilidade e custo interpretativo aceitável.

## Perfil por habilidade

O perfil contínuo contém probabilidade média, dispersão, quantidade de evidências, acurácia observada, intervalo de Wilson e estado de suficiência das evidências.

Os níveis ordinais e o alerta binário permanecem desabilitados em `config/profile.json`. O código somente gera níveis quando recebe limiares explícitos e versionados.

## Gerar o relatório docente

O relatório é um HTML único, sem bibliotecas ou chamadas externas. Os estudantes recebem pseudônimos derivados por SHA-256 com um sal local.

```bash
export TCC_PSEUDONYM_SALT='valor-secreto-local'

tcc-prototype build-teacher-report \
  --profiles data/reports/candidate_temporal_seed_2026.skill_profiles.parquet \
  --metrics data/reports/candidate_temporal_seed_2026.metrics.json \
  --importance data/reports/candidate_temporal_seed_2026.permutation_importance.csv \
  --output data/reports/teacher-report.html \
  --dataset-label 'ASSISTments Skill Builder 2009–2010 corrigido' \
  --model-version '0.3.0'
```

A interface permite selecionar um estudante pseudonimizado, revisar habilidades, comparar modelos, consultar dependência preditiva, registrar notas locais, exportar CSV e imprimir. O relatório não persiste notas nem envia dados.

## Contrato canônico

Cada interação contém estudante anonimizado, item, habilidade ou conjunto de habilidades, ordem, correção, conjunto de origem e identificador rastreável da linha original. Tentativas, dicas, timestamp e tempo são preservados quando disponíveis.

No primeiro experimento, interações com múltiplas habilidades recebem uma habilidade primária determinística para comparação dos modelos iniciais. O conjunto original permanece preservado.

## Testes

```bash
python -m pytest tests
```

Os testes sintéticos verificam:

- bloqueio da aquisição sem aceite ou finalidade;
- manifesto não redistribuível com hash e evidência de aceite;
- integridade do manifesto e rejeição de hash divergente;
- normalização e remoção de duplicatas;
- atributos sem vazamento;
- partições por estudante e tempo;
- baselines, calibração e artefatos;
- determinismo do candidato não linear;
- reconstrução das predições logísticas;
- suficiência de evidências e limiares explícitos;
- pseudonimização e escape dos dados incorporados ao HTML;
- presença de avisos e elementos básicos de acessibilidade.

## Extensões

Novas fontes serão integradas por adaptadores independentes que produzam o mesmo contrato canônico. SHAP poderá ser acrescentado após a execução real caso apresente estabilidade e valor comunicacional superior às explicações existentes.

Nenhuma extensão ou resultado será incorporado à redação acadêmica antes da geração reproduzível e da revisão dos artefatos.
