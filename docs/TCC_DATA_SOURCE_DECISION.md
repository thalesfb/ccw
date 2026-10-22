# Decisão e governança das fontes de dados

> **Alcance desta decisão.** Este documento fixa a fonte usada pelo código
> exploratório em `prototype/` para verificar a viabilidade técnica do fluxo de
> previsão da próxima resposta. Não é a seleção da base de uma investigação
> empírica do TCC: o manuscrito mantém a escolha da fonte condicionada à
> documentação e ao problema (`results/tcc/conteudo/prototipo.tex`, seção
> "Princípios e Requisitos"), e a decisão de executar ou não o protótipo está
> pendente com a orientação (#7, #24, #27). Nenhum arquivo real foi processado.
> A conciliação está em
> [`tcc/AUDITORIA-DIVERGENCIAS-ESPECIFICACAO-CODIGO.md`](tcc/AUDITORIA-DIVERGENCIAS-ESPECIFICACAO-CODIGO.md).

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

A página dos dados de 2009–2010 (`https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data`) declara que o conjunto é livre para uso, mas nenhuma das duas páginas apresenta uma licença padronizada equivalente a um identificador SPDX. O site também mantém uma página separada de termos (`https://sites.google.com/site/assistmentsdata/termsofuseforusingdata`), que, em 22/10/2026, impunha, entre outras condições, não tentar identificar estudantes, não repassar os dados a terceiros, reconhecer o ASSISTments nas publicações e tornar públicos os dados e algoritmos do trabalho publicado. Por isso, o manifesto da execução deverá registrar a URL canônica, a data de acesso e os termos observados no momento da aquisição, sem inferir permissões adicionais.

A página do conjunto pede que a publicação inclua a URL exata do conjunto (no manuscrito, nota de rodapé no capítulo da especificação, pois a página não informa data de publicação) e que o sistema ASSISTments seja citado por Feng, Heffernan e Koedinger (2009), "Addressing the assessment challenge with an online system that tutors as it assesses", *User Modeling and User-Adapted Interaction*, 19(3), 243–266, DOI `10.1007/s11257-009-9063-7` (bib `Feng2009`; metadados conferidos no Crossref em 22/10/2026). A própria página informa que esse artigo não usa o conjunto de 2009–2010.

## Base secundária

O conjunto **Eedi / Diagnostic Questions – NeurIPS 2020 Education Challenge** será a primeira opção de replicação e teste de escalabilidade.

Justificativas:

- questões diagnósticas de matemática;
- milhões de respostas de estudantes;
- problema oficial de previsão de respostas;
- metadados de questões, estudantes e respostas;
- tarefas de qualidade de questões e recomendação que podem sustentar extensões futuras;
- artigo e materiais públicos descrevendo o desafio.

A página oficial disponibiliza os dados sob licença **CC BY-NC-ND 4.0**. O uso no TCC deverá respeitar as restrições de uso não comercial e de distribuição de material adaptado, bem como as restrições específicas informadas para imagens das questões. Os dados brutos e artefatos que reproduzam ou adaptem material licenciado não serão redistribuídos sem revisão específica dos termos aplicáveis.

A base Eedi não será necessária para concluir o primeiro experimento. Seu uso dependerá da validação do manifesto de acesso, da estrutura das habilidades e da capacidade computacional.

Fontes canônicas:

- `https://www.eedischool.com/projects/neurips-education-challenge`
- `https://proceedings.mlr.press/v133/wang21a.html`

## Fontes de contexto e experimento complementar

### SAEB

O SAEB será a principal referência brasileira para proficiência, contexto educacional e discussão de aplicabilidade nacional. Os microdados de 2023 poderão sustentar um experimento complementar de proficiência, mas não substituem registros sequenciais por habilidade necessários ao alvo de próxima resposta.

A página oficial de resultados de 2023 do Inep é a referência canônica desta edição e disponibiliza o acesso aos Microdados Saeb 2023 e aos três volumes de "Resultados Saeb 2023". Em 22/10/2026, 2023 era a edição mais recente com microdados nessa página; a de 2025 oferecia apenas planilha de resultados.

Duas edições aparecem no repositório com papéis distintos. O manuscrito cita o *Relatório de resultados do Saeb 2021*, volume 1 (Inep, Brasília, 2024, ISBN 978-65-5801-078-4; bib `SAEB2021`), só como documentação contextual (requisito R13). A configuração `saeb_2023` registra uma candidata de dados sem adaptador implementado. Se o SAEB vier a ser usado operacionalmente, o texto deverá citar o relatório e os microdados da mesma edição efetivamente adquirida.

Fonte oficial:

`https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/resultados/2023`

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

O repositório da IEA exige aceite dos termos e condições antes do acesso aos arquivos. O pipeline não deverá automatizar ou contornar esse aceite.

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
3. os métodos de aquisição registrados em configuração deverão usar o mesmo vocabulário aceito pelo contrato de manifesto;
4. downloads automáticos somente serão habilitados quando os termos permitirem acesso direto;
5. fontes que exigem aceite manual terão comando de registro e validação, sem contornar o mecanismo de acesso;
6. o pipeline falhará quando o hash não corresponder ao manifesto;
7. arquivos corrigidos ou republicados receberão nova versão de manifesto;
8. a extração não sobrescreverá versões anteriores silenciosamente.

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
- licenças e termos de uso prevalecerão sobre conveniência técnica.

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
