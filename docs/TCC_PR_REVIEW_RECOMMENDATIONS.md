# Recomendações para PRs Abertas — 2026-08-30

## Contexto

Todas as 6 PRs abertas têm CI verde mas **nenhuma review**. Antes da reunião de decisão (#27), nenhuma deve ser mesclada porque dependem da definição de escopo.

---

## PR #23 — `docs/tcc-editorial-normative-revision`
**Título:** docs(tcc): refine academic form and terminology
**Branch:** `docs/tcc-editorial-normative-revision`
**Recomendação:** ✅ **Mesclar após review**

**Por quê:**
- Edição editorial (terminologia, tempo verbal, formatação)
- CI verde, sem dependência de decisão científica
- Melhora qualidade do texto independentemente do cenário
- Baixo risco

**Ação:** Revisar diff, confirmar que não quebra compilação LaTeX, mesclar.

---

## PR #20 — `agent/tcc-document-governance`
**Título:** docs(tcc): formalize document engineering governance
**Branch:** `agent/tcc-document-governance`
**Recomendação:** ⏳ **Aguardar decisão #27**

**Por quê:**
- Formaliza governança documental
- Pode conter referências a decisões de escopo ainda não tomadas
- Não bloqueia trabalho imediato

**Ação:** Revisar após decisão do cenário. Se o conteúdo for genérico (não depende de A/B/C), pode ser mesclado antes.

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
| #23 editorial | ✅ Mesclar | — | — |
| #20 governança | Revisar | Mesclar se genérico | Revisar e mesclar |
| #19 artefatos | ⛔ Manter pendente | Fechar | Aguardar execução real |
| #18 workflow | Revisar (obsoleto?) | Fechar ou reconstruir | Reconstruir com contratos atuais |
| #17 baseline | Revisar | Mesclar se snapshot | Mesclar se útil |
| #16 aquisição | ⛔ Manter pendente | Fechar | Reconstruir com termos revisados |
