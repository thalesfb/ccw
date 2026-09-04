# Recomendações para PRs Abertas — 2026-09-03

> **Atualização após o merge do PR #55:** estas recomendações foram
> recalibradas com base no estado remoto dos PRs e no baseline científico
> vigente. O PR #55 congelou a população adjudicada de 18 registros. O PR #34 é contexto de reconciliação, não fonte de verdade para
> absorção automática de alterações. O PR #23 não deve ser mesclado por
> inteiro: suas mudanças precisam ser revisadas e, quando compatíveis,
> reaplicadas em lotes atômicos sobre a base atual. O PR #20 já foi mesclado;
> seus princípios genéricos não alteram a fonte científica do snapshot.

## Decisão atual para os PRs sob auditoria

| PR | Estado/contexto avaliado | Decisão nesta iteração |
|----|--------------------------|------------------------|
| #34 | Baseline operacional, correções de pipeline, exports e manuscrito; diff amplo | Não mesclar como unidade única sem revisão final; usar como contexto da reconciliação |
| #23 | Revisão editorial com sobreposição e conflito no estado remoto | Não mesclar integralmente; extrair somente mudanças compatíveis em PR atômico |
| #20 | Governança documental; já incorporado à `main` | Princípios genéricos podem ser reutilizados; não altera resultados ou referências derivadas |
| #55 | População adjudicada e artefatos de pesquisa; incorporado à `main` | Fonte vigente para 18 registros, 27 remoções determinísticas e ledger de escopo |

Essa decisão preserva a separação entre três tipos de mudança: resultados
derivados do pipeline, redação/metodologia e governança. Qualquer alteração
que mude contagens, corpus incluído, avaliação MMAT ou interpretação científica
deve retornar ao gate de reconciliação antes de ser incorporada.

## Contexto histórico

O diagnóstico de 30/08/2026 dizia que as seis PRs abertas tinham CI verde e
nenhuma review. Essa frase não é mais um estado remoto vigente: #23 e #34 têm
falhas de `source-validation`, e #35 recebeu revisão automatizada do Copilot.

> O contexto acima e as recomendações para os demais PRs abaixo preservam o
> diagnóstico histórico de 30/08/2026. Para os PRs #20, #23 e #34, prevalece
> a decisão atual registrada na seção anterior, baseada no estado remoto
> consultado novamente após o merge do PR #55. O estado de checks e comentários
> deve ser consultado novamente antes de qualquer merge.

## Checks e revisão automatizada verificados

O estado remoto consultado para esta reconciliação também inclui os checks de
CI, a conversa geral, as revisões e os comentários inline. O registro abaixo é
uma fotografia de 01/09/2026 e deve ser repetido antes de qualquer push ou
merge:

| PR | Checks observados | Revisões/comentários relevantes |
|---|---|---|
| #34 | `source-validation` falhou no check de whitespace; `latex-build` e `canonical-pdf-sync` passaram | Copilot não conseguiu revisar por limite de quota; não há comentário acionável dele |
| #23 | `source-validation` falha em dois testes antigos; `latex-build` e `canonical-pdf-sync` passaram; branch conflitante | Nenhuma revisão submetida |
| #20 | `source-validation` e `latex-build` passaram | Nenhuma revisão submetida |
| #35 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram | Copilot apontou três problemas reais no baseline revertido; foram respondidos no PR e reservados para PRs científicos atômicos, pois #35 é exclusivamente o rollback |

Os três apontamentos do Copilot no PR #35 foram: correspondência de `AI` por
substring em `selection.py`, o mesmo risco no `scoring.py`, e a divergência
entre o recorte temporal documentado e a configuração. Eles não foram
introduzidos no rollback puro; serão tratados no lote científico que suceder a
reversão. Nenhum check verde substitui a revisão do conteúdo científico.

---

## PR #23 — `docs/tcc-editorial-normative-revision`
**Título:** docs(tcc): refine academic form and terminology
**Branch:** `docs/tcc-editorial-normative-revision`
**Recomendação atual:** ⚠️ **Não mesclar integralmente; reaplicar seletivamente**

**Por quê:**
- Edição editorial pode ser útil, mas o estado remoto atual é conflitante e
  sobrepõe arquivos do PR #34.
- O conteúdo precisa ser comparado com o manuscrito reconciliado: não pode
  reintroduzir 17 estudos, contagens históricas, referências indevidas ou
  afirmações de MMAT concluído.
- Mudanças aprovadas devem ser reaplicadas em um lote pequeno e revisável,
  com compilação LaTeX e testes de citações.

**Ação:** Não mesclar a branch inteira. Selecionar mudanças editoriais
compatíveis, reaplicá-las sobre a base atual e abrir/atualizar um PR atômico.

---

## PR #20 — `agent/tcc-document-governance`
**Título:** docs(tcc): formalize document engineering governance
**Branch:** `agent/tcc-document-governance`
**Recomendação atual:** ✅ **Revisar e, se genérico, mesclar separadamente**

**Por quê:**
- Formaliza governança documental e não sobrepõe materialmente o baseline
  reconciliado do PR #34.
- A branch ainda contém uma verificação textual de “17 estudos incluídos”; isso
  deve virar uma regra sobre o registro versionado atual, sem congelar o
  denominador histórico.
- A documentação herdada também descreve a deduplicação como DOI/URL mais
  similaridade de títulos; isso precisa ser generalizado para a regra vigente,
  na qual somente identidades determinísticas DOI/URL alteram o fluxo PRISMA e
  candidatos apenas por título permanecem em auditoria.
- Ainda deve ser verificado para garantir que não trate o SQLite como artefato
  obrigatório, não substitua as bibliografias teóricas e empíricas e não
  congele números históricos como atuais.

**Ação:** Fazer revisão independente. Se permanecer genérico e passar nos
testes/documentação, mesclar em unidade própria, sem empilhá-lo no PR #34.

---

## PR #19 — `agent/tcc-academic-artifacts`
**Título:** feat(tcc): gate and generate academic result artifacts
**Branch:** `agent/tcc-academic-artifacts`
**Recomendação:** ⛔ **NÃO mesclar antes da decisão**

**Por quê:**
- Gera artefatos acadêmicos a partir de execução
- Só faz sentido após execução real (Cenário B ou C)
- Dados sintéticos servem para testar software, não para evidência científica
- Issue #7 define: "Dados sintéticos NÃO servem para produzir resultados científicos do TCC"

**Ação:** Manter pendente até execução real ser autorizada e concluída.

---

## PR #18 — `agent/tcc-autonomous-workflow`
**Título:** feat(prototype): orchestrate reproducible end-to-end runs
**Branch:** `agent/tcc-autonomous-workflow`
**Recomendação:** ⛔ **Revisar antes de mesclar**

**Por quê:**
- Contém decisões obsoletas identificadas no handoff:
  - `cold_start` como conceito
  - `temporal` como split único
  - Random Forest obrigatória
  - seed preferencial
- Pode conflitar com a arquitetura atual do protótipo
- Issue #7: "Não reaplicar literalmente. Se reconstruído, usar contratos científicos atuais."

**Ação:** Revisar código, verificar se contém decisões obsoletas. Se sim, reconstruir com contratos atuais antes de mesclar. Alternativa: fechar e recriar quando necessário.

---

## PR #17 — `agent/tcc-review-baseline`
**Título:** feat(research): freeze review baseline for future updates
**Branch:** `agent/tcc-review-baseline`
**Recomendação:** ⏳ **Aguardar decisão #27**

**Por quê:**
- Congela baseline da revisão para atualizações futuras
- Pode ser útil independentemente do cenário
- Mas: se a decisão for não atualizar literatura 2026, perde utilidade

**Ação:** Revisar conteúdo. Se for apenas snapshot da revisão atual, pode ser mesclado. Se contiver decisões de escopo, aguardar.

---

## PR #16 — `agent/tcc-controlled-acquisition`
**Título:** feat(prototype): enforce controlled dataset acquisition
**Branch:** `agent/tcc-controlled-acquisition`
**Recomendação:** ⛔ **NÃO mesclar antes da decisão**

**Por quê:**
- Implementa aquisição controlada de dados
- Bloqueado conceitualmente pelo gate #24/#27
- O desenho antigo de `--accept-terms` precisa ser revisado
- "NÃO baixar automaticamente dados reais apenas porque existe código antigo no PR #16"
- A revisão dos termos de uso do ASSISTments é uma decisão humana, não automatizável

**Ação:** Manter pendente. Após decisão do cenário, revisar e reconstruir se necessário.

---

## Resumo de ação

| PR | Antes da reunião | Após reunião (se A) | Após reunião (se B/C) |
|----|-----------------|---------------------|----------------------|
| #23 editorial | ⚠️ Extrair seletivamente | PR atômico após reconciliação | PR atômico após reconciliação |
| #20 governança | Revisar separadamente | Mesclar se genérico | Mesclar se genérico |
| #19 artefatos | ⛔ Manter pendente | Fechar | Aguardar execução real |
| #18 workflow | Revisar (obsoleto?) | Fechar ou reconstruir | Reconstruir com contratos atuais |
| #17 baseline | Revisar | Mesclar se snapshot | Mesclar se útil |
| #16 aquisição | ⛔ Manter pendente | Fechar | Reconstruir com termos revisados |
