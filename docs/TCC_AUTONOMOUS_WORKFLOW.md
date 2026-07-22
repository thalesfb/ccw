# Execução autônoma do protótipo

## Objetivo

O fluxo completo do protótipo pode ser executado por um único comando depois que a base foi adquirida com aceite dos termos e seu manifesto foi gerado.

A automação não remove as decisões científicas. Ela garante que as mesmas decisões sejam aplicadas de forma determinística, rastreável e repetível.

## Etapas encadeadas

```text
manifesto e arquivo bruto autorizado
      ↓
validação de tamanho e SHA-256
      ↓
normalização para o contrato canônico
      ↓
relatório de qualidade e Parquet
      ↓
atributos baseados somente no histórico
      ↓
partições cold-start e temporal
      ↓
baselines + regressão logística
      ↓
Random Forest candidata
      ↓
métricas globais e por habilidade
      ↓
explicações e perfil contínuo
      ↓
relatório docente pseudonimizado
      ↓
manifesto final com hashes de todos os artefatos
```

## Comando recomendado

```bash
export TCC_PSEUDONYM_SALT='segredo-local-nao-versionado'

COMMIT=$(git rev-parse HEAD)

tcc-prototype run-all \
  --source-manifest data/manifests/assistments_2009_2010_skill_builder_corrected.json \
  --raw-dir data/raw \
  --output-root data/runs \
  --run-id assistments-v1-primary \
  --git-commit "$COMMIT" \
  --seeds 2026 1701 31415 \
  --split-strategies cold_start temporal \
  --dataset-label 'ASSISTments Skill Builder 2009–2010 corrigido' \
  --model-version '0.3.0' \
  --n-estimators 300 \
  --min-samples-leaf 5 \
  --minimum-profile-evidence 5 \
  --minimum-skill-rows 100 \
  --preferred-report-split temporal \
  --preferred-report-seed 2026
```

## Estrutura de uma execução

```text
data/runs/<run-id>/
├── provenance/
│   └── source_manifest.json
├── prepared/
│   ├── <dataset>.parquet
│   └── <dataset>.quality.json
├── experiments/
│   ├── cold_start/
│   │   └── seed-*/
│   │       ├── baseline/
│   │       └── candidate/
│   └── temporal/
│       └── seed-*/
│           ├── baseline/
│           └── candidate/
├── report/
│   └── teacher-report.html
└── run.manifest.json
```

## Manifesto final

O manifesto registra:

- identificador da execução;
- data e commit Git;
- versões de Python e bibliotecas;
- versão, tamanho e SHA-256 da fonte;
- SHA-256 dos dados processados;
- configuração integral dos experimentos;
- hash da configuração;
- partições e seeds executados;
- localização das métricas;
- relatório docente selecionado;
- tamanho e SHA-256 de cada artefato;
- limites científicos obrigatórios.

Os dados brutos nunca são copiados para a pasta da execução e não aparecem na lista de artefatos.

## Imutabilidade operacional

Uma pasta de execução existente não é sobrescrita. Para repetir o fluxo, deve-se usar outro `run-id` ou remover conscientemente uma execução descartada.

Essa regra evita que novos resultados substituam artefatos já utilizados em análise ou redação.

## Múltiplas sementes

As sementes `2026`, `1701` e `31415` foram registradas previamente no contrato experimental. A comparação entre sementes permite observar estabilidade do modelo e das conclusões.

O relatório docente utiliza uma execução preferencial apenas para visualização. A análise científica deve considerar todas as sementes e as duas estratégias de divisão.

## Falhas

O fluxo interrompe quando:

- commit, `run-id`, seeds ou estratégias são inválidos;
- a pasta de execução já existe;
- a fonte não corresponde ao manifesto;
- o esquema bruto não pode ser adaptado;
- treino ou teste ficam vazios;
- a regressão não possui as duas classes no treino;
- uma etapa não consegue gerar seus artefatos.

Uma execução incompleta não deve ser usada na redação. O erro deve ser corrigido em código ou configuração e uma nova execução deve receber outro identificador.

## Relação com o texto acadêmico

A metodologia e os resultados somente serão atualizados após:

1. revisão e merge dos PRs técnicos;
2. execução autorizada na base real;
3. validação do manifesto da execução;
4. análise de qualidade dos dados;
5. comparação das sementes e partições;
6. revisão dos erros e limitações;
7. seleção justificada dos artefatos para tabelas e figuras.

O comando automatiza o processamento, mas não automatiza a interpretação científica nem a decisão de publicar uma conclusão.
