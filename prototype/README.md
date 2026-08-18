# Protótipo do TCC

Este módulo implementa o pipeline reproduzível que transforma conjuntos educacionais autorizados em interações canônicas para os experimentos do TCC.

## Princípios

- o arquivo bruto nunca é modificado;
- a execução exige manifesto com proveniência e SHA-256;
- versões ou hashes desconhecidos interrompem o fluxo;
- os dados brutos e processados ficam fora do Git;
- relatórios registram contagens, exclusões e hashes;
- dados sintéticos são utilizados no CI, não como evidência educacional.

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

A execução produz nomes versionados pelo hash da fonte, como
`<dataset_id>-<sha256-prefix>.parquet` e
`<dataset_id>-<sha256-prefix>.quality.json`. Assim, uma republicação do
arquivo bruto não sobrescreve silenciosamente os artefatos de uma versão
anterior.

## Semântica do ASSISTments corrigido

O adaptador assume a versão corrigida do Skill Builder 2009–2010. Nessa
versão, uma interação estudante-problema ocupa uma única linha. Quando
`skill_id` representa várias habilidades no formato `skill1_skill2`, o
adaptador preserva essas tags separadamente em `skill_ids`, sem criar linhas
artificiais adicionais.

O campo `order_id` é usado como ordem cronológica da interação. O campo
`correct` é preservado como o rótulo observado da interação e significa acerto
na primeira tentativa; uma primeira resposta incorreta ou um pedido de ajuda é
registrado como incorreto. Tentativas, dicas e tempo da própria interação são
preservados somente como campos observados e continuam proibidos como atributos
da mesma interação no protocolo preditivo definido no TCC.

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

Os testes usam arquivos temporários sintéticos e verificam:

- integridade e contenção do manifesto;
- rejeição de hash, tipos e métodos de aquisição fora do contrato;
- mapeamento do ASSISTments para o contrato canônico;
- preservação de múltiplas habilidades na versão corrigida;
- remoção de duplicatas exatas;
- ordenação determinística;
- versionamento dos nomes de artefato pelo hash da fonte;
- geração do Parquet e do relatório de qualidade.

## Extensões planejadas

Novas fontes serão integradas por adaptadores independentes. Cada adaptador deverá produzir o mesmo contrato canônico e seus próprios testes, evitando que regras específicas de uma base contaminem o restante do pipeline.
