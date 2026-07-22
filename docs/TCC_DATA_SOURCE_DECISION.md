# Decisão e governança das fontes de dados

## Decisão principal

A base primária do primeiro experimento será a versão corrigida do conjunto **ASSISTments Skill Builder 2009–2010**.

A escolha decorre da correspondência entre o problema científico e a estrutura dos dados:

- domínio matemático;
- interações estudante-problema;
- indicador de correção;
- questões associadas a habilidades;
- tentativas e dicas em parte dos registros;
- ordenação de interações;
- uso recorrente em pesquisas de student modeling e knowledge tracing;
- tamanho compatível com execução local e reprodução independente.

A página oficial alerta para duplicatas nas versões antigas e disponibiliza uma versão corrigida com uma linha por estudante-problema. O pipeline deverá aceitar apenas uma versão explicitamente registrada no manifesto, calculando hash antes do processamento.

Página canônica do conjunto:

`https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data/skill-builder-data-2009-2010`

A utilização acadêmica também deverá citar o sistema ASSISTments por meio de Feng, Heffernan e Koedinger (2009), DOI `10.1007/s11257-009-9063-7`.

### Termos específicos do ASSISTments

A disponibilização pública do arquivo não elimina as condições de uso. A página oficial de termos exige compromisso com a proteção dos dados estudantis:

- não tentar descobrir informações pessoalmente identificáveis;
- excluir e comunicar imediatamente qualquer informação identificável encontrada;
- não redistribuir os dados estudantis;
- utilizar a base somente para a finalidade informada;
- reconhecer o ASSISTments nas publicações;
- tornar públicos os dados próprios e algoritmos produzidos no trabalho científico, respeitando a proibição de redistribuição da base original.

Termos oficiais:

`https://sites.google.com/site/assistmentsdata/termsofuseforusingdata`

O comando de aquisição exige `--accept-terms` e uma finalidade científica textual. A data do aceite, a finalidade, o endereço dos termos, a versão, o tamanho e o SHA-256 são registrados no manifesto. O arquivo bruto permanece ignorado pelo Git.

## Base secundária

O conjunto **Eedi / Diagnostic Questions – NeurIPS 2020 Education Challenge** será a primeira opção de replicação e teste de escalabilidade.

Justificativas:

- questões diagnósticas de matemática;
- milhões de respostas de estudantes;
- problema oficial de previsão de respostas;
- metadados de questões, estudantes e respostas;
- tarefas de qualidade de questões e recomendação que podem sustentar extensões futuras;
- artigo e materiais públicos descrevendo o desafio.

A base Eedi não será necessária para concluir o primeiro experimento. Seu uso dependerá da validação dos termos de acesso, licença, estrutura das habilidades e capacidade computacional. A licença indicada na página do desafio é CC BY-NC-ND 4.0, o que permite uso não comercial com atribuição, mas restringe redistribuição de material transformado.

Fontes canônicas:

- `https://www.eedischool.com/projects/neurips-education-challenge`
- `https://proceedings.mlr.press/v133/wang21a.html`

## Fontes de contexto e experimento complementar

### SAEB

O SAEB será a principal referência brasileira para proficiência, contexto educacional e discussão de aplicabilidade nacional. Os microdados de 2023 poderão sustentar um experimento complementar de proficiência, mas não substituem registros sequenciais por habilidade necessários ao alvo de próxima resposta.

Fonte oficial:

`https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/saeb`

### PISA 2022

O PISA disponibiliza questionários, estimativas de desempenho, dados escolares e arquivo cognitivo de itens. Será utilizado para fundamentação de proficiência, comparação internacional e possível análise complementar. Pesos amostrais, valores plausíveis e desenho da avaliação deverão ser respeitados.

Fonte oficial:

`https://www.oecd.org/en/data/datasets/pisa-2022-database.html`

### TIMSS 2023

O TIMSS oferece dados de matemática e ciências para 4º e 8º anos, com respostas, resultados e questionários contextuais. Será fonte de comparação e possível validação externa de métodos de análise de avaliações em larga escala.

Fontes oficiais e DOI dos dados:

- Grade 4: `10.58150/IEA_TIMSS_2023_G4_data_edition_1`
- Grade 8: `10.58150/IEA_TIMSS_2023_G8_data_edition_1`
- Repositório: `https://www.iea.nl/data-tools/repository`

## Fonte metodológica não matemática

O EdNet possui grande volume de interações e licença CC BY-NC 4.0, mas foi coletado em uma plataforma de preparação para TOEIC. Por isso, não será base principal nem evidência sobre aprendizagem matemática.

Ele poderá ser usado somente como teste técnico opcional de escalabilidade ou compatibilidade do esquema, com a limitação de domínio explicitamente registrada.

## Matriz de adequação

| Fonte | Matemática | Sequencial | Habilidades | Alvo próxima resposta | Papel no TCC |
|---|---:|---:|---:|---:|---|
| ASSISTments 2009–2010 Skill Builder | sim | sim | sim | sim | base primária |
| Eedi NeurIPS 2020 | sim | sim | conceitos/metadados | sim | replicação e escala |
| SAEB 2023 | sim | não equivalente | descritores agregados | não | contexto brasileiro e experimento complementar |
| PISA 2022 | sim | avaliação por itens | domínios/processos | não como tutoria | proficiência e comparação internacional |
| TIMSS 2023 | sim | avaliação por itens | domínios curriculares | não como tutoria | validação externa e contexto |
| EdNet | não | sim | tags | sim | teste técnico opcional |

## Regras de aquisição

1. dados brutos não serão commitados;
2. cada fonte terá manifesto com URL, data de acesso, versão, licença ou termos, tamanho e SHA-256;
3. downloads automáticos somente serão habilitados quando os termos permitirem e, quando exigido, após aceite explícito;
4. a finalidade científica e a evidência de aceite serão registradas para fontes controladas;
5. o pipeline não contornará autenticação, aceite ou restrições do provedor;
6. o pipeline falhará quando o hash não corresponder ao manifesto;
7. arquivos corrigidos ou republicados receberão nova versão de manifesto;
8. a extração não sobrescreverá versões anteriores silenciosamente;
9. proibições de redistribuição se aplicam também a anexos, artefatos de CI e relatórios públicos.

## Organização dos dados

```text
prototype/data/
├── manifests/   # metadados, hashes e proveniência versionados
├── raw/         # arquivos originais, ignorados pelo Git
├── interim/     # dados extraídos e normalizados, ignorados pelo Git
├── processed/   # dados analíticos Parquet/DuckDB, ignorados pelo Git
└── reports/     # relatórios de qualidade e proveniência versionáveis
```

## Privacidade e ética

- somente identificadores públicos, anônimos ou pseudonimizados serão processados;
- o projeto não tentará reidentificar estudantes, escolas ou professores;
- combinações de atributos com risco de reidentificação não serão publicadas;
- dados individuais reais não serão exibidos na interface pública;
- exemplos de interface utilizarão registros sintéticos ou agregados;
- variáveis sensíveis não serão usadas no modelo individual principal;
- licenças e termos de uso prevalecerão sobre conveniência técnica;
- se informação identificável for encontrada, o processamento será interrompido e a obrigação específica da fonte será seguida.

## Critério para mudar a base principal

A base primária somente será substituída quando outra fonte demonstrar simultaneamente:

1. melhor aderência ao domínio matemático;
2. granularidade estudante-item-habilidade;
3. ordenação temporal confiável;
4. licença compatível e proveniência estável;
5. documentação suficiente;
6. viabilidade de processamento;
7. benefício científico claro para a pergunta aprovada.

A escolha não será alterada apenas porque outra base produz métricas maiores.
