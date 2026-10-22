# Auditoria das divergências entre especificação e código

**Base:** `origin/main` em `2a05171`, conferida em 22/10/2026.
**Origem:** seção 1.2 de `docs/tcc/REUNIAO-DECISAO-ESCOPO.md` (PR #113).
**Escopo registrado:** revisão crítica e especificação conceitual; o protocolo
do OE4 foi proposto, não aplicado (`docs/tcc/ESTADO-ATUAL-TCC.md`). Esta
auditoria **não decide o escopo** (#24, #27). Ela corrige erros factuais e
torna explícito o que a especificação propõe, o que o código em `prototype/`
implementa e o que não foi executado.

Os números de linha se referem a `origin/main` antes desta alteração.

## Decisões

Legenda: **corrigir** = erro factual, corrigido na fonte e propagado;
**esclarecer** = diferença legítima de desenho, agora explícita nos dois lados;
**manter** = afirmação conferida e preservada.

| # | Divergência | Onde aparece | O que a fonte diz | Decisão | Alteração |
| --- | --- | --- | --- | --- | --- |
| 1 | Fonte de dados: manuscrito cita SAEB/PISA como possibilidades; código adota ASSISTments | `prototipo.tex:31`; `rastreabilidade-requisitos.tex:56` (R13); `docs/TCC_DATA_SOURCE_DECISION.md:5`; `prototype/config/data_sources.json:3` | Página do conjunto: versão corrigida com "one row per student-problem", habilidades múltiplas reunidas em um campo, pedido de citar a URL exata e Feng et al. (2009), artigo que não usa este conjunto. Página 2009–2010: `order_id` cronológico, `skill_id`, "free to use". Página de termos: proíbe repasse e reidentificação, exige reconhecimento e publicação de dados e algoritmos | **esclarecer** | O manuscrito declara que o código usa ASSISTments como teste de viabilidade, não como seleção da base, e que nenhum arquivo foi processado (`prototipo.tex`, R13). O documento de decisão ganhou nota de alcance e o registro dos termos. Nova entrada bib: `Feng2009`. A URL do conjunto foi para nota de rodapé, como já se faz no manuscrito para páginas sem data de publicação, para não inventar um ano |
| 2 | Edição do SAEB: bib `SAEB2021`; config `saeb_2023` | `referencias.bib:305`; `rastreabilidade-requisitos.tex:56`; `data_sources.json:49` | O relatório existe em 4 volumes. A catalogação do vol. 1 informa título, "Brasília, DF : Inep, 2024", 261 p. e ISBN 978-65-5801-078-4. A bib registrava ano 2022, título inexistente e URL genérica. A página de 2023 oferece microdados e 3 volumes de resultados; a de 2025 só oferece planilha | **corrigir** (metadados) + **esclarecer** (edições) | `SAEB2021` corrigida (título, ano 2024, ISBN, URL do PDF). Os papéis de cada edição ficaram explícitos: relatório 2021 como contexto no manuscrito, microdados 2023 como candidata no código (`TCC_DATA_SOURCE_DECISION.md`, `TCC_REFERENCE_AUDIT.md`, `reference_audit.csv`). A edição da config não mudou: é a mais recente com microdados |
| 3 | Modelos: RF/SVM especificados; código com regressão logística (RL) e gradient boosting (GB) | `prototipo.tex:37-39`; `prototype/README.md:90-97`; `experiment.json:53-55`; `models.py:26,82` | Friedman (2001), via Crossref: "Greedy function approximation: A gradient boosting machine". Documentação do scikit-learn 1.9.1: `HistGradientBoostingClassifier` é "Histogram-based Gradient Boosting". Pedregosa et al. (2011), JMLR 12(85). Breiman (2001) e Cortes e Vapnik (1995) já constavam da bib | **esclarecer** | O manuscrito afirma que o código não implementa RF nem SVM, que RL e GB são uma escolha de teste do fluxo, sem comparação e sem treino real. Novas entradas bib: `Friedman2001` e `Pedregosa2011` (RL já citada por `James2021`). O README do protótipo ganhou um quadro de relação com a especificação |
| 4 | Explicabilidade: SHAP/LIME especificados; código com decomposição exata da RL e permutação | `prototipo.tex:62`; R26 (`rastreabilidade-requisitos.tex:82`); `TCC_EXPERIMENTAL_DESIGN.md:229`; `explanations.py:26,187` | `explanations.py` decompõe o log-odds em intercepto + coeficiente × valor transformado e usa `permutation_importance` no teste. Breiman (2001, relatório técnico de jan. 2001, seção 10) descreve a permutação dos valores de uma variável nos dados *out-of-bag*. A documentação do scikit-learn cita Breiman (2001) e avisa que a importância é relativa ao modelo. A decomposição usada não é apresentada como SHAP | **esclarecer** | O manuscrito, R26 e o desenho experimental agora dizem que não há SHAP nem LIME, que o GB não tem explicação e que essas saídas não indicam causas. Nenhuma equivalência com SHAP é afirmada |
| 5 | H2 com redações diferentes | `TCC_EXPERIMENTAL_DESIGN.md:78`; `TCC_PROTOTYPE_SCIENTIFIC_DECISIONS.md:104`; `experiment.json:59` | O contrato executável (`experiment.json`) e o desenho experimental coincidem: RL regularizada supera o melhor baseline. O documento de decisões se declara "formulação histórica" (§1, §14). Seu contraste não linear × RL é a E1 do desenho | **corrigir** | No documento histórico, H2 foi marcada como substituída, com nota que aponta a formulação vigente e a E1. Também foi incluída uma nota com a hierarquia vigente das métricas (log-loss, Brier, calibração; ROC-AUC secundária) |
| 6 | Plano de entrega marcado "ativo" | `TCC_PROTOTYPE_DELIVERY_PLAN.md:288` | Corpo da #7, em 22/10/2026: "decisão pendente com a orientação"; etapas não realizadas "ficam em espera, não canceladas" | **corrigir** | Status alterado para "em espera", com referência à #7, à #24 e à #27 |
| 7 | Sem bib para ASSISTments, TIMSS e gradient boosting | `referencias.bib` | TIMSS 2023 só aparece em config e docs. O DOI `10.58150/IEA_TIMSS_2023_G8_data_edition_1` resolve na DataCite para "TIMSS 2023 International Database [...] Grade 8" (IEA, 2024). O manuscrito não menciona TIMSS 2023; TIMSS 2011 entra apenas via `Identifying2017_006` | **corrigir** (ASSISTments, GB) + **manter** (TIMSS) | Bib nova apenas para o que o manuscrito passou a citar: `Feng2009`, `Friedman2001` e `Pedregosa2011`. TIMSS 2023 continua fora da bib, porque não é citado; a entrada deverá ser criada se o texto vier a usá-lo |

Ajustes conexos: o README do protótipo dizia executar "o protocolo técnico de
avaliação do TCC". O protocolo executável é o de
`docs/TCC_EXPERIMENTAL_DESIGN.md`, distinto do protocolo do OE4, e a redação
foi corrigida. O campo `license_or_terms` de `data_sources.json` passou a
citar a página de termos. Nenhuma lógica de código foi alterada.

## Fontes consultadas (acesso em 22/10/2026)

- ASSISTments, página do conjunto: <https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data/skill-builder-data-2009-2010>
- ASSISTments, dados 2009–2010 e cabeçalhos de colunas: <https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data>
- ASSISTments, termos de uso: <https://sites.google.com/site/assistmentsdata/termsofuseforusingdata>
- Crossref, `10.1007/s11257-009-9063-7` (Feng, Heffernan e Koedinger, 2009) e `10.1214/aos/1013203451` (Friedman, 2001): <https://api.crossref.org/works/>
- JMLR, Pedregosa et al. (2011): <https://jmlr.org/papers/v12/pedregosa11a.html>
- scikit-learn 1.9.1, `HistGradientBoostingClassifier`: <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html>. O código fixa a versão 1.6.1 (`prototype/pyproject.toml`)
- scikit-learn 1.9.1, importância por permutação: <https://scikit-learn.org/stable/modules/permutation_importance.html>
- Breiman (2001), relatório técnico, seção 10: <https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf>
- Inep, Saeb 2021 (página e PDF do vol. 1, com a catalogação na p. 4): <https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/resultados/2021>; <https://download.inep.gov.br/educacao_basica/saeb/2021/resultados/relatorio_de_resultados_do_saeb_2021_volume_1.pdf>
- Inep, Saeb 2023 e 2025: <https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/resultados/2023>; <https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/resultados/2025>
- DataCite, TIMSS 2023 Grade 8: <https://doi.org/10.58150/IEA_TIMSS_2023_G8_data_edition_1>
- GitHub, issue #7 (corpo, status de governança): <https://github.com/thalesfb/ccw/issues/7>

## Pendências para a orientação

- Decidir o escopo (A/B/C, #24/#27). Se a execução for aprovada, fixar a base
  com os critérios de `prototipo.tex` e registrar os termos do ASSISTments no
  manifesto.
- Decidir se RF, SVM, SHAP e LIME continuam como alternativas especificadas ou
  se a especificação adota as escolhas do código. Esta auditoria não fez essa
  escolha.
- A revisão humana desta conciliação permanece pendente.
