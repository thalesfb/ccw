# Material para a reunião de decisão de escopo científico

**Base:** `origin/main` em `2a05171` (após #110–#112), conferida em 22/10/2026.
**Acompanha:** #27 (reunião), #24 (gate científico), #25 (título), #7, #26, #28 e #29.

Este material compara os cenários A, B e C definidos na #24. Não recomenda
nenhum deles e não registra uma decisão. Cada afirmação aponta para um arquivo
do repositório ou para uma entrada de `results/tcc/referencias.bib` ou
`results/tcc/referencias_pedagogicas.bib`. O que não está documentado aparece
como **a confirmar com a orientação**. A reunião não exige protótipo em execução
(#27, "Regra para esta reunião").

> **Registro anterior.** `docs/tcc/ESTADO-ATUAL-TCC.md:78` e o comentário de
> 15/10/2026 na #27 registram que o escopo desta entrega foi confirmado como
> revisão crítica e especificação conceitual, sem treinamento nem validação
> educacional. A ficha de decisão da #27 (seção 7 deste documento) ainda não
> foi preenchida em material versionado. Cabe à reunião ratificar esse registro,
> revisá-lo ou adiar a decisão, e registrar a justificativa.

## 1. Estado atual do TCC

| Componente | Estado verificável | Evidência |
| --- | --- | --- |
| Revisão sistemática | 11.904 identificados; 27 remoções DOI/URL; 11.877 na triagem; 2.486 na priorização; **18 selecionados preliminarmente**. Desses, 15 estudos empíricos mantidos provisoriamente, 1 excluído após o resumo, 1 texto integral não recuperado e 1 protocolo excluído após texto completo. Corte da busca em 31/08/2026. | `docs/tcc/ESTADO-ATUAL-TCC.md` (bloco `snapshot`); `results/tcc/conteudo/resultados.tex:8` |
| MMAT 2018 | **14 triagens S1/S2 e 11 apreciações por categoria**, todas preliminares, feitas por um único revisor e sem escore agregado. Os estudos 5, 7 e 14 aguardam a definição do delineamento, o estudo 8 aguarda adjudicação de elegibilidade e unidade, e o 6923 não foi apreciado. | `resultados.tex:10,20`; `research/data/mmat_reassessment_current.csv` |
| Cobertura das fontes | 16 de 18 PDFs locais (faltam 3 e 6923). A leitura foi assistida, e a leitura humana integral continua pendente. | `research/data/study_contribution_current.json` (`reading_basis`) |
| Especificação conceitual | Requisitos, critérios para dados e modelos, arquitetura de referência e um quadro com 26 grupos de requisitos rastreáveis. O protocolo do OE4 foi **proposto, não aplicado**. | `results/tcc/conteudo/prototipo.tex:43-48`; `resultados.tex:44`; `rastreabilidade-requisitos.tex` |
| Objetivos | Objetivo geral propositivo e 4 objetivos específicos (OE1–OE4). O OE4 não exige desenvolver o protótipo. | `results/tcc/conteudo/introducao.tex:24,28` |
| Título vigente | "Ensino Personalizado de Matemática: Oportunidades e Técnicas Computacionais" | `results/tcc/pretextuais/capa.tex:5` |
| Apresentação | Deck canônico em Slidev, com 25 slides; o PPTX de 19 slides é um export paralelo. | `docs/tcc/ESTADO-ATUAL-TCC.md` (seção de decisões pendentes) |

### 1.1 Implementado versus especificado (`prototype/`)

Escala usada: **E** = especificado no texto ou em docs; **I** = implementado em
código; **T** = coberto por testes sintéticos; **R** = executado em dados reais;
**V** = validado (técnica ou pedagogicamente).

| Componente | E | I | T | R | V | Evidência |
| --- | --- | --- | --- | --- | --- | --- |
| Ingestão com manifesto e SHA-256 (ASSISTments 2009–2010 corrigido) | sim | sim | sim | não | não | `prototype/tcc_prototype/adapters/assistments.py`; `prototype/README.md` |
| Adaptadores Eedi, SAEB, PISA, TIMSS, EdNet | sim (só em config) | não | não | não | não | `prototype/config/data_sources.json`; só existe o adaptador ASSISTments |
| Splits `student_holdout` e `personalized_temporal`, atributos sem vazamento | sim | sim | sim | não | não | `prototype/tcc_prototype/modeling/splits.py`, `features.py` |
| Baselines (global, item, habilidade, estudante), regressão logística regularizada, `HistGradientBoostingClassifier` | sim | sim | sim | não | não | `modeling/baselines.py`, `models.py:26,82` |
| Random Forest e SVM | sim (alternativas) | não | não | não | não | `prototipo.tex:37-39` |
| Log-loss, Brier, calibração, bootstrap pareado por estudante | sim | sim | sim | não | não | `modeling/evaluation.py`; `docs/TCC_EXPERIMENTAL_DESIGN.md:176-195` |
| Perfil contínuo por estudante e habilidade (Wilson, dispersão) | sim | sim | sim | não | não | `tcc_prototype/profiles.py`; `docs/TCC_PROFILE_AND_EXPLAINABILITY.md` |
| Níveis ordinais e alerta binário | sim (condicionado) | desabilitado | — | não | não | `prototype/README.md` ("permanecem desabilitados") |
| Explicação exata da regressão logística e importância por permutação | sim | sim | sim | não | não | `modeling/explanations.py:10,187` |
| SHAP e LIME | sim | não | não | não | não | `prototipo.tex:62`; requisito R26 (`rastreabilidade-requisitos.tex:82`) |
| Harness `doctor`/`demo`/`run` | sim (#28) | não | não | não | não | `tcc_prototype/cli.py:68-92` tem apenas `prepare-assistments`, `evaluate-baselines` e `build-evidence-profile` |
| Interface docente (Lote 9) | sim | não | não | não | não | `docs/TCC_PROTOTYPE_DELIVERY_PLAN.md:180` |
| Limiares de elegibilidade e suporte; fonte probabilística do perfil | exigidos | `null` (a CLI bloqueia) | sim | — | — | `prototype/config/experiment.json:20,97-98,105-106`; `config/profile.json:3,5` |

Na preparação deste material, a suíte do protótipo foi executada localmente:
**44 testes passaram**, todos com dados sintéticos. Não há base real no
repositório (`prototype/data/` contém apenas o README), e o Google Colab não foi
usado (`prototype/README.md:7-14`; `ESTADO-ATUAL-TCC.md`).

### 1.2 Divergências documentais

Pesam pouco no cenário A e passam a pesar nos cenários B e C, porque a execução
herdaria escolhas que o manuscrito não sustenta.

1. **Fonte de dados.** O manuscrito menciona SAEB, PISA e dados sintéticos como
   possibilidades, sem fixar uma base (`prototipo.tex:31`). O código e os docs
   fixam ASSISTments como base primária (`docs/TCC_DATA_SOURCE_DECISION.md`).
   ASSISTments e TIMSS não constam de `referencias.bib`; a citação de Feng,
   Heffernan e Koedinger (2009) aparece apenas em
   `TCC_DATA_SOURCE_DECISION.md:26`.
2. **Edição do SAEB.** A bibliografia cita o relatório SAEB 2021 (`SAEB2021`),
   mas a configuração usa os microdados de 2023 (`saeb_2023`).
3. **Modelos.** O manuscrito registra RF e SVM como alternativas
   (`prototipo.tex:37-39`). O código implementa regressão logística e gradient
   boosting. Nenhuma referência metodológica de gradient boosting consta da
   bibliografia.
4. **Explicabilidade.** O manuscrito prevê SHAP e LIME (`prototipo.tex:62`). O
   código implementa contribuições exatas da regressão logística e importância
   por permutação.
5. **Hipótese H2.** Em `TCC_EXPERIMENTAL_DESIGN.md:78`, a regressão logística
   supera o melhor baseline. Em `TCC_PROTOTYPE_SCIENTIFIC_DECISIONS.md:104`, um
   modelo não linear supera a regressão logística, o que no desenho
   experimental aparece apenas como a análise exploratória E1. As métricas
   principais também diferem (`SCIENTIFIC_DECISIONS.md` §10 contra
   `EXPERIMENTAL_DESIGN.md` §Métricas).
6. **Status do plano.** `TCC_PROTOTYPE_DELIVERY_PLAN.md` §9 marca "Status:
   ativo", enquanto a governança da #7 marca a decisão como pendente.

## 2. Matriz dos estudos retidos

A matriz segue a forma `referência → problema/técnica → dados → modelo/método →
explicabilidade → contribuição possível`. Foi extraída de
`research/data/study_contribution_current.json`,
`research/data/claim_evidence_current.json` (C-RSL-01 a 09) e
`docs/tcc/AUDITORIA-ESTUDOS-SINTESE.md`. A coluna de explicabilidade **não foi
codificada** no repositório para o corpus, por isso "n.c." significa "não
codificado; a confirmar na fonte primária". Os números de cada linha são os que
o próprio estudo reporta, não desempenho validado.

| Referência | Problema/técnica | Dados | Modelo/método | Explicabilidade | Contribuição possível ao TCC |
| --- | --- | --- | --- | --- | --- |
| `Math2021_001` | Classificação em categorias operacionais de desempenho | PISA 2012 em computador (271.323 → 58.753 registros) | Rede neural e RF; kappa, recall, ROC-AUC | n.c. | Cautela com seleção analítica e independência do teste |
| `Implementation2025_000` | Predição de notas de Matemática (escola privada, ensino fundamental) | Registros escolares | SMOTE+RUSBoost; 70/30; acurácia de 75% e recall de 43% na classe Low (C-RSL-01/02) | n.c. | Desbalanceamento e métricas por classe |
| `Multimodels2020_002` | Predição de desempenho em Matemática (Camboja) | Não revalidado (sem PDF) | Múltiplos modelos de EDM (rótulo histórico) | n.c. | Não revalidada nesta rodada |
| `Analysis2022_003` | Classificação de notas de Matemática e Português | Dados escolares (amostragem pouco relatada) | Seleção wrapper; DT e RF (Tabelas 6 e 8) | Seleção de atributos, que não é explicação causal | Explicitar desfecho, atributos e validação |
| `Design2025_004` | Trajetórias personalizadas | Matemática, Chinês e Inglês; amostra não informada | Grafo de conhecimento, aprendizagem por reforço, análise de sentimento | n.c. | Exemplo de relato insuficiente (amostra e alocação) |
| `Identifying2017_006` | Classificação de desempenho | TIMSS 2011 (Turquia) | Classificadores de EDM; 10 dobras (descrição invertida, p. 1613) | n.c. | Definição do alvo e relato da validação |
| `Innovative2023_005` | Modelo de ensino inteligente com perfil e trajetórias | 2 turmas (120; 50 e 52 válidos) | Comparação pré/pós entre grupos | n.c. | Inconsistência de denominadores; alocação não relatada |
| `Computational2017_008` | Modelos computacionais de aprendizes para autoria de tutores | DataShop: frações (79 estudantes) e equações (71 estudantes; 4.568 ações) | Simulação comparada a registros humanos (C-RSL-07/08) | n.c. | Modelagem em nível de passo; bases distintas, que não se somam |
| `Machine2024_009` | Predição de aprovação, reprovação ou resultado condicional em Matemática | 50 estudantes de Engenharia Industrial, 2017–2021 | Árvore de decisão; acurácia de 72% sem validação descrita | Modelo intrinsecamente legível; relato das regras a confirmar | Cautela com amostra local e temporalidade |
| `Enhancing2025_012` | Intervenção: animação computacional e jigsaw (teoremas de círculo) | Grupos com diferença já no pré-teste (C-RSL-05) | Quase-experimento ou ensaio, com alocação contraditória | não se aplica | Intervenção combinada que não isola o efeito |
| `He2025_6915` | Síntese, predição de tamanho de efeito e aplicação escolar | 423 publicações (dados do artigo) e turmas | Modelo preditivo de tamanho de efeito (C-RSL-03) | n.c. | Separar estimandos e unidades |
| `Villegas2025_6916` | Tutoria inteligente e feedback | 450 estudantes de STEM, mais entrevistas | Métodos mistos (C-RSL-04) | n.c. | Distinguir feedback, resultado e janela temporal |
| `Ozseven2026_6917` | Predição de acerto em matemática on-line | Interações em matemática on-line | Híbrido neuro-fuzzy e ML; partição por estudante (C-RSL-09) | n.c. (regras fuzzy a confirmar) | Rótulo, métricas e partição por estudante |
| `UniversityMathematics2026_6919` | Matemática universitária integrada à metrologia de SiC com recursos de IA | Coortes de 2021 e 2025; 12 entrevistas | Métodos mistos | não se aplica | Integração curricular; não isola o efeito da IA |
| `Echeveria2025_6920` | Classificação de mentalidade matemática (construto afetivo) | 633 recrutados, 428 casos completos | Classificadores, incluindo MLP | n.c. | Itens que definem o alvo também entram como preditores (C-RSL-06) |

Fora da matriz ficam `Machine2019_007` (excluído após o resumo, usado como
contexto), `Imperatrice2025_6921` (protocolo) e `Zeng2025_6923` (texto integral
não recuperado; embargo informado até 16/05/2027).

**Leitura da matriz.** O que segue vem dos registros acima e não deve ser
extrapolado para a área como um todo:

- predominam registros escolares tabulares e avaliações em larga escala (PISA
  2012, TIMSS 2011);
- só `Computational2017_008` e `Ozseven2026_6917` descrevem dados por passo ou
  interação;
- nenhum registro está documentado como uso de SAEB ou de dados brasileiros
  sequenciais;
- o uso de SHAP, LIME ou permutação no corpus não foi codificado.

## 3. Fontes de dados

| Fonte | Unidade e estrutura | Sequencial por habilidade? | Acesso e termos (registrados) | Pode sustentar | Não pode sustentar |
| --- | --- | --- | --- | --- | --- |
| ASSISTments 2009–2010 Skill Builder (corrigido) | Interação estudante-problema, `order_id`, `correct`, `skill_id` (com multihabilidade) | sim | Download público; a página declara uso livre, sem licença SPDX; registrar os termos no manifesto | Viabilidade técnica e desempenho preditivo e calibração no conjunto analisado | Aprendizagem, competência, contexto brasileiro atual (`data_sources.json`, `known_risks`) |
| Eedi NeurIPS 2020 | Respostas a questões diagnósticas de matemática | sim (conceitos e metadados) | CC BY-NC-ND 4.0; restrições sobre imagens | Replicação e escala (não necessária ao 1º experimento) | Idem; redistribuição de material adaptado |
| SAEB 2023 (Inep) | Proficiência e questionários contextuais | não equivalente | Download oficial; revisões de privacidade podem alterar variáveis | Contexto brasileiro de proficiência; análise complementar | Alvo de próxima resposta; sequência de tutoria |
| PISA 2022 (OCDE; bib `PISA2022`, `OECDPISA2022Framework`) | Itens, valores plausíveis, pesos amostrais | não (avaliação por itens) | Download oficial | Proficiência e comparação internacional, com pesos e valores plausíveis | Sequência de tutoria |
| TIMSS 2023 (IEA) | Itens e questionários, 4º e 8º anos | não | **Exige aceite dos termos**, que não deve ser automatizado | Contexto e validação externa de métodos de avaliação | Sequência de tutoria; não está na bib |
| EdNet KT1 | Interações em preparação para o TOEIC | sim | CC BY-NC 4.0 | Apenas teste técnico de escala e esquema | Qualquer conclusão sobre matemática |

Fonte: `docs/TCC_DATA_SOURCE_DECISION.md:88-97` e `prototype/config/data_sources.json`.
Os termos precisam ser reconferidos na data de aquisição.

**Duas naturezas de dado, que não se misturam.**

- *Dados sequenciais por interação e habilidade* (ASSISTments, Eedi) sustentam
  probabilidades de acerto na próxima interação.
- *Dados brasileiros de proficiência e contexto* (SAEB) sustentam a descrição
  de proficiência estimada em escala oficial e de fatores contextuais.

Nenhum dos dois converte o outro: uma probabilidade de acerto não é
proficiência SAEB, e uma proficiência SAEB não gera uma sequência de interações
(`fundamentacao.tex:12`; `NRC2001`).

**Arquitetura híbrida possível (cenários B e C).** O método seria demonstrado em
ASSISTments, e a contextualização curricular viria de um crosswalk documentado
de habilidade para habilidade da BNCC, com o SAEB servindo apenas como
referência descritiva do contexto brasileiro. Essa arquitetura pode afirmar
viabilidade técnica e coerência do mapeamento. Não pode afirmar validação
nacional, nem transferência do desempenho para escolas brasileiras, nem
equivalência entre habilidades do ASSISTments e da BNCC. O custo do crosswalk
(número de habilidades, revisão docente) está **a confirmar com a orientação**.

## 4. Modelos, explicabilidade e BNCC

**Papel de cada modelo, quando a pergunta o justifica.** As fontes estão em
`TCC_EXPERIMENTAL_DESIGN.md:132-145` e `James2021`.

- *Baselines históricos*: são a referência mínima obrigatória. Sem eles, um
  ganho do modelo não é interpretável. Relevantes em B e C.
- *Regressão logística regularizada*: modelo probabilístico interpretável, cujos
  coeficientes têm leitura direta (`James2021`). Candidato natural de B.
- *Gradient boosting e RF*: só se justificam se a pergunta for "um modelo não
  linear melhora o resultado sem perder calibração?" (análise E1). No corpus,
  RF aparece em `Math2021_001` e `Analysis2022_003` (`Breiman2001`). Não há
  referência de gradient boosting na bibliografia, o que exigiria acréscimo.
- *Calibração e ROC* (`NiculescuMizilCaruana2005`, `Fawcett2006`): aplicam-se
  apenas a saídas probabilísticas compatíveis com a tarefa.

**Explicabilidade: o que cada técnica permite e o que não estabelece.**

| Técnica | Faz sentido quando | Não estabelece |
| --- | --- | --- |
| Contribuições exatas da regressão logística | O modelo é a própria regressão; as contribuições são aditivas na escala log-odds (`James2021`), e a reconstrução é verificada contra as previsões (`TCC_PROFILE_AND_EXPLAINABILITY.md`) | Causa da dificuldade; recomendação pedagógica |
| Importância por permutação | Dependência preditiva global no teste, como descrição (`explanations.py:187`) | Causalidade; não retorna à seleção de modelos (`prototype/README.md`) |
| SHAP (`LundbergLee2017`) e LIME (`RibeiroSinghGuestrin2016`) | Modelos não lineares (árvores), com a estabilidade e o custo avaliados (R26) | Causa; competência; validade curricular |

A distinção entre associação, importância para o modelo, explicação da
previsão, causa e recomendação está em `TCC_EXPERIMENTAL_DESIGN.md:229-240`.
Só as três primeiras vêm de um experimento preditivo.

**Estratégia de alinhamento com a BNCC.** As fontes são `BNCC2018`, `NRC2001` e
os requisitos R08 e R25.

1. Montar uma tabela de correspondência versionada no formato
   `skill_id → código de habilidade BNCC`. Cada linha recebe um tipo de
   relação (equivalente, parcial ou relacionada), a justificativa e o revisor.
2. Submeter a tabela à revisão de um docente de Matemática (R25); essa revisão
   ainda não foi executada.
3. Relatar o desempenho observado e a probabilidade *associados* a habilidades
   da BNCC, nunca como medida de competência BNCC. A BNCC define competência
   como mobilização de conhecimentos, habilidades, atitudes e valores
   (`fundamentacao.tex:8`).

No cenário A, essa estratégia fica no nível de especificação. Em B, cabe um
crosswalk demonstrativo. Em C, o crosswalk ou a sua validação metodológica
dependem do escopo aprovado.

## 5. Hipóteses de diferencial científico

| Hipótese | Sustentação atual | Busca adicional antes de reivindicar? |
| --- | --- | --- |
| D1. Articular RSL, MMAT por critério (sem escore) e especificação com 26 grupos de requisitos rastreáveis | Artefatos versionados (`resultados.tex:54`) | **Sim**, para afirmar que é inédito; para descrevê-la como contribuição do TCC, não |
| D2. A separação operacional entre desempenho, predição, proficiência, competência e aprendizagem orienta os requisitos | `fundamentacao.tex:12`; `NRC2001` | Sim, se for apresentada como diferencial frente a outras especificações |
| D3. A explicabilidade está ausente ou é pouco relatada nos estudos de matemática do recorte | **Não codificada** no corpus (seção 2) | Sim: codificar os 15 estudos antes de qualquer afirmação |
| D4. Faltam dados brasileiros públicos sequenciais por habilidade em matemática | Nenhuma evidência no repositório | Sim, uma busca específica |
| D5. Crosswalk de ASSISTments para a BNCC | Nenhum trabalho prévio buscado | Sim |
| D6. Pipeline com proveniência por hash e bloqueio de limiares não congelados | Código e testes | Não como ciência; é uma propriedade de engenharia |

## 6. Cenários A, B e C

Todos os cenários compartilham pendências: adjudicar o estudo 8 e o
delineamento dos estudos 5, 7 e 14; obter segundo revisor do MMAT; avaliar a
sensibilidade dos filtros; e resolver a proveniência das buscas (#24 e #29). A
**eficácia pedagógica não é demonstrada em nenhum cenário** sem um estudo
próprio com participantes.

| Dimensão | A: revisão, síntese e especificação | B: demonstração de viabilidade | C: experimento próprio |
| --- | --- | --- | --- |
| Contribuição central | Síntese crítica e especificação rastreável | Execução reproduzível de um método consolidado sobre dados públicos | Teste de hipóteses (H1 e H2) sob protocolo congelado |
| Entregáveis | Manuscrito atual consolidado; OE4 como protocolo proposto | A + 1 run documentado (manifesto, hashes, métricas descritivas) + capítulo de demonstração | A + runs com todas as seeds e splits, comparação de modelos, perfil, explicações e capítulo de resultados |
| Alternativa concreta | — | **B1:** pipeline atual (baselines + regressão logística) sobre ASSISTments, sem modelo novo. **B2:** reusar artefato pré-treinado; nenhum candidato identificado no repositório (a confirmar) | Plano das #7 e #28 |
| Dados | Nenhum dado novo | ASSISTments, com termos registrados | ASSISTments; Eedi opcional; SAEB só como contexto |
| Treinamento próprio | não | Ajuste de baselines e da regressão logística (hardware e tempo a confirmar) | sim |
| Protótipo executável | não obrigatório | desejável (harness mínimo, #28) | necessário (#28 completo) |
| BNCC | Fundamentação e especificação | Crosswalk demonstrativo | Crosswalk com revisão docente, conforme o escopo |
| Evidência permitida | Síntese científica | Viabilidade técnica e metodológica no conjunto analisado | Desempenho preditivo e calibração no protocolo executado |
| Trabalho específico | Resolver as divergências da seção 1.2 no texto; aplicar ou não o protocolo do OE4 (a decidir) | Congelar os limiares nulos; decidir `probability_source`; manifesto; harness mínimo; resolver as divergências 1–4 e 6; reescrever OE4 e o capítulo de resultados | Tudo de B, mais: resolver a divergência 5 (H2), as métricas, Eedi, análise por habilidade, explicações para os modelos avaliados e revisão dos resultados |
| Riscos | Contribuição percebida como só documental; diferencial a confirmar (seção 5) | Demonstração lida como evidência educacional; base de 2009–2010 distante do contexto brasileiro; mudança de termos | Prazo; resultados nulos (precisam ser relatados); desvio de escopo dos objetivos já escritos |
| Custo (tempo) | Menor dos três | Intermediário | Maior |
| Título (#25) | Opções A–D da #25 | Família "Revisão Sistemática e Demonstração de Viabilidade" | Só depois de o experimento existir (#25) |
| #7 | Preservada como linha futura | Lotes 5–8 com execução limitada; Lote 9 fora | Lotes 5–10 viram requisito |
| #28 | Não necessária | `doctor` e `demo`; `run` para um único run | Completa |
| #26 (atualização 2026) | Possível, por prioridade | Concorre por tempo | Pouco compatível sem prazo adicional |

Os custos de tempo estão em escala relativa. A estimativa em semanas depende do
prazo de entrega e da disponibilidade de hardware, que não estão registrados no
repositório: **a confirmar com a orientação**. Os objetivos atuais (OE4 sem
execução, `introducao.tex:28`) correspondem ao cenário A. B e C exigem revisar
os objetivos, o resumo e a conclusão.

## 7. Decisões a registrar literalmente

Campos da #27, mais itens que este material tornou explícitos:

```text
cenário escolhido: A | B | C | decisão adiada
ratifica o registro de 15/10/2026 (ESTADO-ATUAL-TCC.md:78)? sim/não
papel do protótipo (código atual): documentação técnica | demonstração | experimento
dataset(s) aprovados para uso/demonstração:
modelos/métodos aprovados para avaliação:
estratégia de explicabilidade (LR exata | permutação | SHAP/LIME | só especificação):
tratamento das divergências 1.2 (fonte, modelos, explicabilidade, H2, status do plano):
papel da BNCC (fundamentação | crosswalk demonstrativo | crosswalk revisado):
aplicar o protocolo do OE4 nesta versão? sim/não
necessidade de harness executável: sim/não
atualização da revisão até 2026: sim/não/a decidir
segundo revisor MMAT e adjudicação dos estudos 5, 7, 8, 14: quem/quando
título: manter/alterar/a decidir (qual opção da #25)
deck a apresentar (Slidev de 25 slides | PPTX de 19 slides):
justificativa da orientação:
próxima entrega:
```

## 8. Estado das issues relacionadas

| Issue | Estado | Observação |
| --- | --- | --- |
| #24 | aberta | O gate de decisão está pendente; frentes MMAT e protocolo em andamento |
| #25 | aberta | O título depende do cenário; nenhuma opção foi escolhida |
| #7 | aberta | Linha experimental preservada; nada executado em dados reais |
| #28 | aberta | Harness não implementado; não é necessário para esta reunião |
| #26 | aberta | Nenhuma busca de 2026 executada; depende de prioridade |
| #29 | aberta | **O texto da issue está desatualizado** ("Estado conferido em 06/09/2026": "17 candidatos empíricos provisórios e 1 protocolo contextual"). Precisa ser atualizado para os números reconciliados após #110–#112: 18 → 15 empíricos provisórios, 1 excluído após o resumo, 1 não recuperado, 1 protocolo excluído |
| #27 | aberta | O comentário de 06/09 cita `docs/TCC_DECISION_MEETING_MATERIAL.md`, que nunca foi versionado. Este documento cumpre esse papel com outro nome. O deck Slidev da reunião continua opcional e está a confirmar |
