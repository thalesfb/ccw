# Ciclo de vida dos dados do protótipo

Este diretório define a organização local dos dados. Arquivos brutos e processados não devem ser commitados, salvo amostras sintéticas explicitamente identificadas.

## Estrutura

- `manifests/`: proveniência, versão, licença, tamanho e SHA-256;
- `raw/`: arquivo original sem alterações;
- `interim/`: extração e normalização intermediária;
- `processed/`: tabelas analíticas em Parquet ou DuckDB;
- `reports/`: relatórios de qualidade, contagens e exclusões.

## Fluxo pretendido

```text
registro da fonte
      ↓
aquisição autorizada
      ↓
validação do hash
      ↓
inspeção do esquema bruto
      ↓
normalização para interação canônica
      ↓
validação de qualidade e temporalidade
      ↓
partições reproduzíveis
      ↓
Parquet/DuckDB + relatório
```

## Automação segura

O pipeline deverá automatizar tudo o que puder ser reproduzido sem violar termos de acesso:

- download direto apenas quando autorizado;
- retomada e cache de arquivos grandes;
- cálculo de SHA-256;
- extração idempotente;
- detecção de encoding e delimitador;
- mapeamento de colunas por adaptador versionado;
- validação do contrato canônico;
- geração de relatórios;
- interrupção em caso de versão, hash ou esquema desconhecido.

Quando a fonte exigir download manual ou aceite de termos, o pipeline deverá explicar o arquivo esperado e validar o arquivo fornecido. Não deverá contornar autenticação, aceite ou limites do provedor.

## Política de reprodutibilidade

Cada execução deve registrar:

- commit do código;
- manifesto e hash da fonte;
- adaptador e versão;
- configuração utilizada;
- data e duração;
- contagens de entrada e saída;
- exclusões por regra;
- hashes dos artefatos processados.

## Dados sintéticos

Dados sintéticos poderão ser versionados apenas para:

- testes unitários;
- validação de contratos;
- demonstração da interface;
- execução do CI.

Eles nunca serão utilizados como evidência de desempenho educacional.
