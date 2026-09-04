# Integração da engenharia documental ao plano do TCC

## 1. Objetivo

Este documento posiciona a governança de engenharia documental em relação ao plano científico e técnico do TCC. Seu propósito é evitar que melhorias de compilação, normalização, rastreabilidade e manutenção do LaTeX sejam confundidas com novos objetivos científicos ou com lotes funcionais do protótipo.

A engenharia documental é tratada como uma **camada transversal de governança**. Ela protege a produção e a revisão dos artefatos acadêmicos, mas não constitui um novo lote da implementação científica.

## 2. Marco de consolidação acadêmica

Em **2026-08-11**, o PR #6 foi incorporado à `main`. Esse merge consolida na linha principal do repositório a revisão textual e metodológica que apresenta o trabalho como concluído dentro do escopo efetivamente executado: revisão sistemática, avaliação metodológica e especificação técnica e pedagógica do protótipo.

Esse marco não transforma implementações experimentais ainda não revisadas em resultados acadêmicos. Os PRs do protótipo permanecem sujeitos à revisão individual, às dependências declaradas e às restrições científicas da issue #7.

## 3. Posição da padronização documental

As decisões registradas em `NORMATIVE_GOVERNANCE.md`, `DOCUMENT_ENGINEERING_ROADMAP.md` e no ADR de preservação institucional não criam um "Lote 10" e não alteram a sequência dos lotes 2–9 da issue #7.

A relação é transversal:

| Área do plano científico | Relação com a engenharia documental |
|---|---|
| Lote 2 — auditoria bibliográfica | fornece integridade de citações e referências, mas não substitui a avaliação da qualidade ou adequação das fontes. |
| Lote 3 — desenho experimental | preserva rastreabilidade entre decisões metodológicas, texto e artefatos, sem definir hipóteses ou métricas. |
| Lotes 4–8 — dados, modelos e protótipo | não interfere na implementação científica; apenas poderá validar artefatos que alimentem o documento. |
| Lote 9 — integração acadêmica final | é o principal ponto de contato: previews, proveniência, compilação e verificações objetivas podem reduzir o risco de divergência entre resultados reproduzidos e redação. |
| Entrega institucional | a governança normativa orienta a revisão de formatação e requisitos do IFC sem substituir automaticamente particularidades institucionais. |

## 4. Regra de não interferência

Enquanto os lotes científicos em aberto forem revisados, a documentação de engenharia documental pode ser consolidada, mas sua implementação operacional deve permanecer separada.

Em particular:

1. a revisão dos PRs #9–#19 não deve ser bloqueada pela implementação futura de `tcc-preview.yml`, `tcc-compliance.yml` ou `normative-watch.yml`;
2. nenhuma atualização normativa deve alterar automaticamente a classe `abntex2-IFC`;
3. nenhuma melhoria de CI deve ser interpretada como evidência científica;
4. nenhuma mudança de formatação deve antecipar alteração de conteúdo acadêmico;
5. conflitos entre ABNT, orientação institucional e implementação devem ser registrados como drift e encaminhados para revisão humana.

## 5. Ordem de trabalho após o merge do PR #6

A sequência científica permanece a já definida na issue #7 e nos PRs empilhados.

### Pré-requisito técnico — normalizar a pilha de PRs

O PR #6 foi incorporado por squash merge. Portanto, o commit consolidado na `main` não preserva como ancestral o histórico da branch `agent/revise-tcc-methodology`, sobre a qual a pilha #9–#19 foi originalmente construída.

Antes de revisar o mérito do lote 2, deve-se:

1. reconstruir ou rebasear `agent/tcc-reference-audit` sobre a `main` atual, preservando somente as mudanças próprias do PR #9;
2. confirmar que o diff do #9 não reapresenta as alterações do PR #6;
3. executar novamente os checks do CI;
4. reconstruir os PRs descendentes sequencialmente sobre os novos heads de seus pais.

Enquanto houver PRs empilhados, a política de merge deve ser escolhida conscientemente. Merge commits preservam a ancestralidade das branches e reduzem a necessidade de restacking. Squash merges são compatíveis com a pilha, mas exigem reconstrução do próximo PR após cada integração.

### Etapa imediata — revisar o lote 2

Depois da normalização da branch, o PR #9 é o próximo ponto de revisão porque trata da auditoria bibliográfica completa e está diretamente apoiado sobre a baseline acadêmica agora incorporada à `main`.

A revisão deve confirmar, antes de merge:

- correspondência entre cada entrada bibliográfica e sua decisão de auditoria;
- existência e correção dos identificadores canônicos;
- distinção entre descoberta bibliográfica e fonte canônica;
- adequação das fontes que sustentam decisões técnicas;
- ausência de mudança silenciosa no conjunto retido no snapshot vigente (atualmente 18 registros, com escopo e estado registrados nos artefatos versionados);
- compatibilidade dos validadores com a compilação e os testes existentes.

### Etapa seguinte — revisar o lote 3

Após a consolidação do PR #9, o PR #10 deve ser revisado como desenho experimental. O foco é a validade da pergunta operacional, do alvo, das partições, dos baselines, das métricas e dos limites de inferência.

Essa etapa também absorve refinamentos já identificados após a revisão do PR #6, especialmente terminologia de "diagnóstico", consistência entre a descrição das consultas e a implementação versionada, e força das afirmações metodológicas.

### Etapas posteriores

Na sequência:

1. PR #11 — seleção e governança das fontes de dados;
2. PR #12 — pipeline reproduzível de preparação;
3. PR #13 — baselines e partições sem vazamento;
4. PR #14 — candidato não linear, explicabilidade e perfil por habilidade;
5. PR #15 — relatório docente;
6. PR #16 — aquisição controlada da base primária;
7. PR #17 — congelamento da revisão sistemática como baseline;
8. PR #18 — execução ponta a ponta;
9. PR #19 — gate de integridade e geração de artefatos acadêmicos.

Cada PR deve ser revisado e consolidado antes de o seguinte ser tratado como parte da `main`. A existência de código e testes em uma branch empilhada não equivale a aprovação científica ou técnica.

## 6. Gate para resultados reais

Mesmo após a eventual consolidação dos PRs técnicos, a integração de resultados experimentais ao TCC continua bloqueada até que exista execução real autorizada e auditável.

São condições mínimas:

- fonte de dados autorizada e corretamente versionada;
- manifesto de proveniência íntegro;
- verificação de hashes e esquema;
- execução das partições e sementes previstas;
- análise de estabilidade entre execuções;
- revisão dos erros e limitações;
- confirmação de que os artefatos usados no texto correspondem à execução selecionada;
- manutenção da distinção entre desempenho preditivo e eficácia pedagógica.

## 7. Momento da engenharia documental operacional

A implementação do roadmap documental deve ocorrer em trilha própria e incremental. Ela pode ser iniciada quando não competir com revisões essenciais do TCC e quando houver benefício claro para a próxima etapa de revisão acadêmica.

A prioridade futura permanece:

1. preview integral por PR com proveniência por SHA;
2. diff renderizado quando viável;
3. checks objetivos de integridade e compilação;
4. fixture normativa;
5. baseline versionada de fontes e regras;
6. verificações semiautomáticas;
7. monitoramento de drift;
8. auditoria comportamental da classe institucional;
9. eventual contribuição upstream após a conclusão do TCC.

Essa trilha deve continuar separada da implementação do protótipo e de qualquer futura contribuição ao modelo institucional do IFC.

## 8. Critério de governança

O planejamento passa a considerar duas trilhas coordenadas, mas não acopladas:

- **trilha científica e técnica:** issue #7 e PRs #9–#19;
- **trilha de engenharia documental:** PR #20 e roadmap pós-TCC.

A primeira determina o que pode ser afirmado cientificamente. A segunda determina como o documento e suas regras de apresentação podem ser produzidos, auditados e mantidos com rastreabilidade.

Nenhuma das duas deve substituir a autoridade da outra.
