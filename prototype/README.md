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

A execução produz:

- `*.parquet`: tabela normalizada de interações;
- `*.quality.json`: relatório de qualidade, contagens e hashes.

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

- integridade do manifesto;
- rejeição de hash divergente;
- mapeamento do ASSISTments para o contrato canônico;
- remoção de duplicatas exatas;
- ordenação determinística;
- geração do Parquet e do relatório de qualidade.

## Extensões planejadas

Novas fontes serão integradas por adaptadores independentes. Cada adaptador deverá produzir o mesmo contrato canônico e seus próprios testes, evitando que regras específicas de uma base contaminem o restante do pipeline.
