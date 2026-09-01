# Recomendações para PRs Abertas — 2026-09-01

> **Atualização após a auditoria do PR #34:** estas recomendações foram
> recalibradas com base no estado remoto dos PRs e no baseline científico
> vigente. O PR #34 é contexto de reconciliação, não fonte de verdade para
> absorção automática de alterações. O PR #23 não deve ser mesclado por
> inteiro: suas mudanças precisam ser revisadas e, quando compatíveis,
> reaplicadas em lotes atômicos sobre a base atual. O PR #20 pode ser avaliado
> separadamente por tratar de governança documental e não sobrepor o baseline.

## Decisão atual para os PRs sob auditoria

| PR | Estado/contexto avaliado | Decisão nesta iteração |
|----|--------------------------|------------------------|
| #34 | Baseline operacional, correções de pipeline, exports e manuscrito; diff amplo | Não mesclar como unidade única sem revisão final; usar como contexto da reconciliação |
| #23 | Revisão editorial com sobreposição e conflito no estado remoto | Não mesclar integralmente; extrair somente mudanças compatíveis em PR atômico |
| #20 | Governança documental, sem sobreposição material com o baseline, mas com pelo menos uma salvaguarda ainda escrita para os 17 estudos | Pode seguir em revisão independente após generalizar essa salvaguarda para o registro vigente; não deve alterar resultados ou referências derivadas |

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
> consultado novamente em 01/09/2026.

## Checks e revisão automatizada verificados

O estado remoto consultado para esta reconciliação também inclui os checks de
CI, a conversa geral, as revisões e os comentários inline. O registro abaixo é
uma fotografia de 01/09/2026 e deve ser repetido antes de qualquer push ou
merge:

| PR | Checks observados | Revisões/comentários relevantes |
|---|---|---|
| #20 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE` | Sem review técnica ou comentário acionável; a salvaguarda dos 17 estudos foi generalizada no commit `a0512df` |
| #23 | `source-validation` falhou; `latex-build` e `canonical-pdf-sync` passaram; `UNSTABLE/MERGEABLE` | Sem review técnica ou comentário acionável; manter como contexto e extrair mudanças seletivamente |
| #34 | `source-validation` falhou; `latex-build` e `canonical-pdf-sync` passaram; `UNSTABLE/MERGEABLE` | Copilot não conseguiu revisar por limite de quota; não há comentário acionável dele |
| #35 | Fechada após a reescrita da `main`; rollback não é uma PR ativa | Os três apontamentos do Copilot foram transformados em correções/tests nas PRs científicas seguintes |
| #36 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE` | Copilot indisponível por quota; nenhum comentário técnico acionável |
| #37 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE` após rebase | Copilot indisponível por quota; nenhum comentário técnico acionável |
| #38 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE` | Copilot indisponível por quota; nenhum comentário técnico acionável |
| #39 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE`; head atual `f5b8221` | Copilot indisponível por quota; nenhum comentário técnico acionável; follow-up esclarece a proveniência das 72 consultas |
| #40 | Todos os checks, incluindo `manuscript-validation` e `presentation-build`, passaram; `CLEAN/MERGEABLE` | Copilot indisponível por quota; nenhum comentário técnico acionável |
| #41 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE` após rebase | Copilot indisponível por quota; nenhum comentário técnico acionável |
| #42 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE` após rebase | Copilot indisponível por quota; nenhum comentário técnico acionável |
| #43 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE`; head atual `6543a74` | Copilot indisponível por quota; nenhum comentário técnico acionável; follow-up sincroniza o hash do dedup e a escrita LF do manifesto |
| #44 | `source-validation` e `latex-build` passaram; `MERGEABLE` | Copilot indisponível por quota; nenhum comentário técnico acionável |
| #45 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE` | Copilot indisponível por quota; registro de auditoria e ordem de revisão |
| #46 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE`; head atual `9c83e1c` | Copilot indisponível por quota; matriz de evidência dos sete overrides, ainda sem adjudicação final; proveniência de 6922/6918 refinada |
| #47 | `source-validation`, `latex-build` e `canonical-pdf-sync` passaram; `CLEAN/MERGEABLE` | Copilot indisponível por quota; testes das expectativas do protocolo vigente |

Após esses follow-ups, uma integração descartável dos heads atuais de #36--#47
passou em **87/87 testes**. O deck integrado também passou em `npm run validate`
e no build do Slidev, produzindo `index.html` e os assets `prisma_flow` e
`selection_funnel`. Essa validação é evidência de compatibilidade técnica; não
substitui a adjudicação científica dos estudos e overrides pendentes.

Os três apontamentos do Copilot no PR #35 foram: correspondência de `AI` por
substring em `selection.py`, o mesmo risco no `scoring.py`, e a divergência
entre o recorte temporal documentado e a configuração. Eles foram tratados nas
correções do snapshot e nas regressões automatizadas das PRs #36 e #43. Os
avisos de quota nas PRs posteriores significam que não houve revisão automática;
não significam aprovação. Nenhum check verde substitui a revisão do conteúdo
científico. Nos PRs #46 e #47, a mensagem do Copilot continua sendo apenas
indisponibilidade por limite de quota; portanto, não há aprovação automatizada
nem comentário técnico a incorporar.

## Auditoria técnica de encoding, whitespace e finais de linha (01/09/2026)

A comparação foi feita no diff de cada PR contra sua base efetiva, usando
`git diff --check` e decodificação UTF-8 estrita em memória. Isso verifica a
saúde do patch sem converter o worktree do operador nem tratar o SQLite como
artefato versionável.

| PR | Resultado técnico | Interpretação |
|---|---|---|
| #16--#19 | `diff-check` limpo; arquivos textuais válidos em UTF-8; sem BOM e sem finais mistos | Nenhum bloqueio de encoding/line ending identificado |
| #20 | `diff-check` limpo; 5 arquivos textuais válidos em UTF-8; sem BOM e sem finais mistos | Não há bloqueio de encoding/line ending identificado |
| #23 | `diff-check` limpo; 18 arquivos textuais válidos em UTF-8; sem BOM e sem finais mistos | O bloqueio é funcional: dois testes do protocolo falham, não é um problema de codificação |
| #34 | 238.628 diagnósticos de trailing whitespace e 1 de espaço antes de tabulação em 14 arquivos; UTF-8 válido; 5 arquivos com finais CRLF/LF/CR misturados e BOM em `papers.csv` | `source-validation` para antes dos testes. Os principais arquivos são exports `.bib/.csv`, `.gitignore`, dois HTML e código/LaTeX; o patch precisa de normalização isolada e revisão semântica |
| #35 (fechada) | Não é PR ativa após a reescrita de `main`; não é candidata a merge | Seus problemas funcionais foram reavaliados nas PRs científicas posteriores |
| #36--#47 | `diff-check` limpo; todos os arquivos textuais alterados válidos em UTF-8; sem BOM e sem finais mistos | Nenhum bloqueio técnico dessa classe foi encontrado |

No #23, os erros concretos do check são `computational_techniques` sendo
acionado por uma correspondência de `AI` dentro de palavras comuns e a
auditoria não encontrar os três registros preservados que o teste exige. O
correto é extrair a correção já validada no #36, não mesclar a branch inteira.

No #34, a saída inclui espaços finais intencionais de hard break Markdown,
mas também conversões de linha e exports gerados em escala. Uma eventual
recuperação deve: (1) preservar o conteúdo científico e as quebras semânticas;
(2) normalizar os arquivos textuais para LF; (3) remover trailing whitespace
não intencional; (4) reexecutar `git diff --check` e todos os testes; e (5)
continuar excluindo o commit `a91b439`, que já foi removido de `main`.

## Ordem de revisão para concluir o objetivo

1. **Histórico:** manter `main` em `627a105`, confirmar que `a91b439` não é ancestral e preservar apenas a branch de recuperação.
2. **Fonte científica:** revisar #36 (snapshot, deduplicação DOI/URL, scoring, 23 candidatos, 7 overrides, 16 retidos, exports e reprodutibilidade sem SQLite).
3. **Contrato documental:** revisar #37 (baseline atual versus histórico, duplicatas, percentuais, protocolo, planos e datas).
4. **Evidência e protocolo:** revisar #43 (identidade canônica), #46 (evidência dos sete overrides/MMAT) e #47 (testes das expectativas do protocolo vigente). Nenhum desses PRs muda o corpus por si só.
5. **Manuscrito:** revisar #38 (texto parte a parte, referências empíricas versus teóricas/manuais, citações e imagens preservadas).
6. **Validação e apresentação:** revisar #40, depois #39 e #42 (workflow, build reproduzível, publicação clicável, narrativa e proveniência do Slidev/PTC).
7. **Proveniência e governança:** revisar #44, #41 e #45, verificando que o estado dos PRs e os artefatos legados continuam descritos como contexto, não como fonte de verdade.
8. **PRs anteriores:** revisar #20 separadamente; usar #23 apenas para extração editorial após a base científica; manter #34 por último como fonte de contexto/salvamento seletivo, nunca como unidade de merge.
9. **Gate científico final:** antes de qualquer conclusão, recuperar fontes primárias, adjudicar os sete overrides e fechar o MMAT dos 15 estudos empíricos aplicáveis; checks verdes não substituem essa decisão.

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
- O follow-up `a0512df` generalizou a verificação textual de “17 estudos
  incluídos” para o conjunto retido no snapshot vigente, sem congelar o
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
