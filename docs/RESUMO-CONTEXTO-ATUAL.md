# RESUMO DO CONTEXTO ATUAL

> **Atualização de 01/09/2026:** o baseline local da revisão foi atualizado e validado com 11.904 registros consolidados e 16 registros retidos operacionalmente (IDs 1--10, 6916, 6917, 6918, 6920, 6921 e 6923). Quinze registros são classificados provisoriamente como empíricos; o 6918 está em hold por conflito entre o ano oficial da fonte (2014) e o ano armazenado no snapshot (2025), e o ID 6921 é um protocolo/proposta mantido apenas para contexto e rastreabilidade. Este documento preserva abaixo o planejamento histórico; para as contagens vigentes, use `docs/RECONCILIACAO-BASELINE-2026-08-31.md`.

## Baseline vigente (31/08/2026)

O banco operacional contém **11.904 registros**. A deduplicação determinística
retirou 27 registros redundantes por DOI/URL; no fluxo PRISMA, **11.877** foram
avaliados na triagem, **9.391** foram excluídos e **2.486** avançaram à
elegibilidade; nessa etapa, **2.470** foram excluídos, resultando em **16
registros retidos operacionalmente**. Desses, 15 são provisoriamente classificados como empíricos, com o 6918 em hold temporal, e o ID 6921 é
um protocolo/proposta contextual fora da síntese empírica. A lista atual é composta pelos IDs 1--10, 6916, 6917,
6918, 6920, 6921 e 6923.

A execução histórica tinha 17 estudos incluídos. Em uma nova rodada, foram identificados 23 candidatos e aplicados 7 overrides manuais, chegando aos 16 registros retidos operacionais. A mudança não é uma simples troca numérica: também envolve nova contagem de ingestão e correção do scoring. Quinze registros empíricos são provisórios; o 6918 permanece fora de conclusões temporais finais até a resolução do conflito de ano, e o ID 6921 é um protocolo/proposta retido apenas para contexto e não é aplicável ao MMAT empírico. A reavaliação documental do MMAT dos registros aplicáveis foi registrada com evidência por critério; nove textos primários foram revisados externamente, mas fontes restantes, localizadores e adjudicação ainda estão pendentes. Quatro overrides exigem recuperação/inspeção de fonte primária e adjudicação de escopo. Portanto, conclusões comparativas sobre qualidade metodológica ou certeza da evidência não devem ser tratadas como consolidadas.

### Plano vigente após a reconciliação

O baseline de 16 está congelado como estado operacional, mas não como resultado
científico final. A auditoria de identidade separa 27 remoções determinísticas
(25 excedentes por DOI e 2 por URL exata, com um grupo misto quanto à presença
de DOI) de 232 candidatos restantes apenas por título normalizado (257 excedentes
brutos, incluindo a sobreposição com identidades), que aguardam disposição semântica. A reavaliação MMAT foi registrada em
`research/data/mmat_reassessment_current.csv`, com S1/S2, Q1--Q5 e evidência
por critério. Nove estudos têm texto primário revisado externamente; o ledger
continua preliminar até haver texto primário para todos os registros empíricos
aplicáveis, localizadores
por critério e adjudicação. Os próximos artefatos devem ser entregues em PRs atômicos, sem
versionar o SQLite e sem misturar as referências teóricas com a bibliografia
derivada do pipeline. A separação entre os 15 registros provisoriamente empíricos (com o 6918 em hold) e o protocolo
contextual 6921 é mantida em `research/data/current_synthesis_scope.csv`.

**Data do planejamento histórico:** 07/03/2026
**Status no planejamento histórico:** preservado como registro; não é cronograma vigente
**Aluno:** Thales Ferreira Batista (Ciência da Computação - IFC Videira)
**Orientador:** Prof. Dr. Rafael Zanin (IFC)
**Coorientador:** Prof. Dr. Manassés Ribeiro (IFC)

---

## 📍 ONDE ESTAMOS

### Linha do Tempo

```
✅ Jan-Fev 2026: Revisão sistemática executada no baseline histórico (9.431 → 17 estudos)
✅ Fev 2026: PTC escrito e documentado
✅ Mar 2026: PTC DEFENDIDO E APROVADO
    ⚠️ Observação da banca: "PRISMA 2020 não é metodologia/protocolo de condução"
✅ 31 Ago 2026: Baseline reexecutado e reconciliado (11.904 → 16 registros; 15 empíricos provisórios, 6918 em hold + 1 protocolo contextual)
🟡 31 Ago--01 Set 2026: reavaliação documental MMAT registrada por critério; fontes restantes, localizadores e adjudicação final pendentes
⏳ Próxima fase: cenário do protótipo e eventual validação aguardam decisão com a orientação
```

### Estrutura do Projeto (3 Fases)

| Fase | Nome | Status | Período | Entrega |
|------|------|--------|---------|---------|
| **Fase 1** | Revisão Sistemática | 🟡 **OPERACIONALMENTE CONCLUÍDA; GATE CIENTÍFICO PENDENTE** | Jan-Mar 2026 + reconciliação em 31/08/2026 | PTC defendido; MMAT preliminar |
| **Fase 2** | Desenvolvimento Protótipo | ⏳ **A DEFINIR** | Sem prazo vigente | Decisão de escopo e MVP |
| **Fase 3** | Validação Experimental | ⏳ **NÃO INICIADA** | Sem prazo vigente | Protocolo e resultados, se autorizados |

---

## 🎓 O QUE ACONTECEU NA DEFESA DO PTC

### Observação da Banca

**Crítica específica:**
> "PRISMA 2020 não é metodologia/protocolo de condução da revisão, é guideline de relato"

**Contexto:**
- ❌ PTC usava expressões como "seguindo o protocolo PRISMA 2020"
- ✅ PRISMA 2020 é guideline de RELATO, não de CONDUÇÃO
- ✅ Metodologia de condução = Cochrane Handbook, IOM Standards
- ✅ PRISMA 2020 = Checklist de transparência (27 itens)

### Decisão da Banca

**Resultado:** ✅ **PTC APROVADO** com recomendação de incorporar correções na versão final do TCC

**Compromisso assumido na defesa:**
1. Corrigir terminologia (relato vs. condução)
2. Incluir checklist PRISMA completo no apêndice
3. Aplicar avaliação de qualidade (MMAT) na fase TCC
4. Adicionar seção de limitações

---

## 📋 PLANO HISTÓRICO DE AJUSTES DO TCC

> Esta seção é preservada para explicar as correções solicitadas na defesa do
> PTC. Ela não é uma lista de tarefas vigente: as correções terminológicas, o
> checklist e a seção de limitações já foram incorporados ao manuscrito. O
> MMAT do snapshot atual já foi reaplicado em nível documental e está
> registrado por critério; falta consolidar fontes, localizadores e
> adjudicação, não iniciar o procedimento do zero.

### Estratégia

As correções foram incorporadas **na versão do TCC em revisão** (não é
necessário refazer o PTC, que já foi aprovado). O que permanece abaixo é o
plano de trabalho originalmente proposto, mantido como histórico.

### Etapa 1: Correções Terminológicas (Semanas 1-2 do TCC)

**Tempo:** 5-7 horas
**Prioridade:** ALTA

- [x] Substituir "seguindo o protocolo PRISMA 2020" → "com relato estruturado conforme PRISMA 2020"
- [x] Adicionar parágrafo explicativo sobre Cochrane (condução) vs. PRISMA (relato)
- [x] Incorporar o checklist PRISMA 2020 no apêndice vigente do TCC
- [x] Marcar no checklist o que está atendido, parcial ou pendente

**Arquivos afetados:**
- `introducao.tex` (2 correções)
- `metodologia.tex` (3 modificações)
- `apendice-prisma-checklist.tex` (novo arquivo, ~200 linhas)
- `main.tex` (1 inclusão)

### Etapa 2: Complementos Metodológicos (planejamento histórico; Semanas 2-4 do TCC)

**Tempo:** 10-12 horas
**Prioridade:** MÉDIA (pode ser feito em paralelo ao desenvolvimento do protótipo)

- [x] Registrar a reaplicação documental preliminar do MMAT 2018 aos 15 registros empíricos aplicáveis (o planejamento histórico mencionava 17; o protocolo 6921 permanece separado)
- [x] Criar tabela de qualidade metodológica por critério
- [x] Adicionar seção "Avaliação da Qualidade Metodológica" em metodologia.tex
- [x] Adicionar seção "Limitações da Revisão" em conclusao.tex
- [ ] Consolidar fontes primárias, localizadores e adjudicação final; não converter os itens em uma aprovação automática

**Arquivos afetados:**
- `metodologia.tex` (nova seção MMAT)
- `resultados.tex` (tabela de qualidade)
- `conclusao.tex` (seção de limitações)
- `apendice-prisma-checklist.tex` (atualizar status)

---

## 📊 IMPACTO NO CHECKLIST PRISMA 2020 (PLANEJAMENTO HISTÓRICO)

Os percentuais abaixo registram uma projeção do planejamento anterior e não representam o status documental atual.

| Momento | Atendidos | Pendentes | Taxa |
|---------|-----------|-----------|------|
| **PTC Defendido** | 18/27 | 9/27 | 67% |
| **Após Etapa 1** | 21/27 | 6/27 | 78% |
| **Versão final planejada (histórica)** | 27/27 | 0/27 | Meta, não status atual |

**Meta:** Versão final do TCC com aderência total ao PRISMA 2020.

---

## 🎯 CRONOGRAMA SUGERIDO

### Semana 1 do TCC (planejamento histórico; datas não vigentes)

**Foco:** Correções terminológicas + início do protótipo

- [ ] Segunda-feira: Revisar plano com orientador
- [ ] Terça-feira: Copiar arquivos PTC → estrutura TCC
- [ ] Quarta-quinta: Executar correções 1.1.A, 1.1.B, 1.2.A, 1.2.B (3h)
- [ ] Sexta-feira: Criar apêndice PRISMA checklist (3h)
- [ ] Paralelo: Iniciar design do protótipo

### Semana 2 do TCC (planejamento histórico; datas não vigentes)

**Foco:** Compilar versão corrigida + continuar protótipo

- [ ] Segunda: Compilar LaTeX, verificar erros
- [ ] Terça: Enviar versão corrigida ao orientador
- [ ] Quarta-sexta: Iniciar avaliação MMAT (primeiros 5-6 estudos)
- [ ] Paralelo: Desenvolvimento do protótipo

### Semanas 3-4 do TCC (planejamento histórico; datas não vigentes)

**Foco:** Completar MMAT + seção de limitações

- [ ] Completar e adjudicar o MMAT dos 15 registros empíricos aplicáveis (o plano histórico mencionava 17; 6921 é contextual)
- [ ] Criar tabela de qualidade
- [ ] Escrever seção de limitações
- [ ] Atualizar checklist PRISMA
- [ ] Paralelo: Desenvolvimento do protótipo

### Semana 5+ do TCC (planejamento histórico; datas não vigentes)

**Foco:** Validação experimental (Fase 3) + integração final

- [ ] Versão final da dissertação com todas as correções
- [ ] Preparar defesa final

---

## 💡 BENEFÍCIOS DA OBSERVAÇÃO DA BANCA

**Não foi uma crítica negativa, foi uma contribuição pedagógica valiosa:**

1. ✅ **Aprofundou compreensão metodológica** - Agora entendemos claramente a distinção entre condução (Cochrane) e relato (PRISMA)

2. ✅ **Fortaleceu fundamentação do protótipo** - A reaplicação documental do MMAT explicita, por critério, quais limitações podem afetar a interpretação; decisões de design continuam condicionadas à consolidação e não a um ranking de qualidade

3. ✅ **Melhorou transparência** - O checklist completo PRISMA 2020 tornará a dissertação mais transparente e reproduzível

4. ✅ **Preparou para publicação** - A versão final do TCC terá padrão de qualidade suficiente para publicação em periódico científico

5. 🎯 **Objetivo de transparência** - aderência integral ao PRISMA 2020 e avaliação MMAT só poderão ser reivindicadas após a consolidação da reaplicação e adjudicação no conjunto atual

---

## 📚 DOCUMENTOS DE REFERÊNCIA

### Criados Para Este Projeto

1. **[memorando-orientador-prisma.md](./memorando-orientador-prisma.md)**
   Documento técnico formal explicando a observação da banca para o orientador

2. **[plano-ajustes-defesa.md](./plano-ajustes-defesa.md)**
   Guia passo-a-passo detalhado de TODAS as correções com exemplos de código LaTeX

3. **[RESUMO-CONTEXTO-ATUAL.md](./RESUMO-CONTEXTO-ATUAL.md)** (este arquivo)
   Síntese executiva do contexto atual

### Artigos PRISMA (Fontes Primárias)

1. **PRISMA 2020 Main Article**
   Page MJ et al. BMJ 2021;372:n71
   DOI: [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71)

2. **PRISMA-P 2015 (Protocols)**
   Moher D et al. Systematic Reviews 2015;4:1
   DOI: [10.1186/2046-4053-4-1](https://doi.org/10.1186/2046-4053-4-1)

3. **Cochrane Handbook v6.4**
   Higgins JPT et al. 2023
   URL: [www.training.cochrane.org/handbook](https://www.training.cochrane.org/handbook)

4. **MMAT 2018**
   Hong QN et al. 2018
   URL: [http://mixedmethodsappraisaltoolpublic.pbworks.com](http://mixedmethodsappraisaltoolpublic.pbworks.com)

---

## 🚦 STATUS ATUAL DO PROJETO

### O Que Está PRONTO ✅

- ✅ Revisão sistemática: baseline histórico preservado (9.431 → 6.914 → 17 estudos) e baseline vigente validado (11.904 → 27 deduplicados → 11.877 → 9.391 excluídos na triagem → 2.486 → 2.470 excluídos na elegibilidade → 16 registros; 15 empíricos provisórios, com 6918 em hold + 1 contextual)
- ✅ Pipeline automatizado e reproduzível (GitHub)
- ✅ Diagrama PRISMA flow
- ✅ Síntese narrativa dos achados
- ✅ PTC defendido e aprovado
- ✅ Base sólida para desenvolvimento do protótipo

### O Que Está EM ANDAMENTO 🟢

- 🟡 Auditoria científica do baseline: recuperação de fontes, localizadores e adjudicação MMAT
- 🟡 Preparação do próximo PR atômico, mantendo a separação entre snapshot, síntese empírica e referências teóricas

### O Que Está PENDENTE ⏳

- ✅ Correções terminológicas incorporadas no manuscrito; revisão final do relato ainda necessária
- ✅ Reavaliação documental preliminar do MMAT aos registros empíricos provisórios, com evidência por critério; 6918 permanece em hold temporal
- ⏳ Recuperação das fontes restantes e consolidação/adjudicação da tabela MMAT final
- 🟡 Auditoria da integridade dos identificadores: 25 grupos DOI e 2 grupos URL tratados deterministicamente; 154 grupos de título-only (232 excedentes) permanecem candidatos à disposição semântica
- ✅ Seção de limitações presente; revisão final condicionada ao gate científico
- ⏳ Validação experimental do protótipo (Fase 3)
- ⏳ Defesa final do TCC

---

## 🎯 PRÓXIMA AÇÃO IMEDIATA (STATUS ATUAL)

**Próximo ciclo vigente (sem prazo artificial):**

1. Recuperar as fontes primárias restantes e registrar localizadores para cada critério MMAT aplicável;
2. adjudicar os sete overrides e os julgamentos MMAT com o supervisor, mantendo o protocolo 6921 fora da síntese empírica;
3. resolver o conflito temporal do ID 6918 e os grupos de título-only sem alterar o fluxo por inferência;
4. atualizar o manuscrito e a apresentação somente com decisões já documentadas;
5. abrir PRs atômicos, com checks locais e remotos verificados e comentários do Copilot avaliados.

**Minha recomendação:**

O plano histórico recomendava fazer **Etapa 1** em 5--7 horas porque:
- É rápido (1-2 sessões de trabalho)
- Remove pressão mental de "dívida técnica pendente"
- Permite focar 100% no protótipo depois sem interrupções
- Base da dissertação fica pronta desde já

**Etapa 2** foi parcialmente executada no snapshot atual; a consolidação final
continua condicionada às fontes e à adjudicação descritas acima. Não usar esta
seção para inferir prazos atuais.
