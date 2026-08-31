# RESUMO DO CONTEXTO ATUAL

> **Atualização de 31/08/2026:** o baseline local da revisão foi atualizado e validado com 11.904 registros consolidados e 16 estudos incluídos (IDs 1--10, 6916, 6917, 6918, 6920, 6921 e 6923). Este documento preserva abaixo o planejamento histórico; para as contagens vigentes, use `docs/RECONCILIACAO-BASELINE-2026-08-31.md`.

## Baseline vigente (31/08/2026)

O banco consolidado contém **11.904 registros**. Na triagem, **9.413** foram excluídos e **2.491** avançaram à elegibilidade; nessa etapa, **2.475** foram excluídos, resultando em **16 estudos incluídos**. A lista atual é composta pelos IDs 1--10, 6916, 6917, 6918, 6920, 6921 e 6923.

A execução histórica tinha 17 estudos incluídos. Em uma nova rodada, foram encontrados 23 candidatos e removidos 7 falsos positivos, chegando aos 16 atuais. A mudança não é uma simples troca numérica: também envolve nova contagem de ingestão e correção do scoring. A reaplicação do MMAT aos 16 estudos ainda está pendente; portanto, conclusões comparativas sobre qualidade metodológica ou certeza da evidência não devem ser tratadas como consolidadas.

**Data do planejamento histórico:** 07/03/2026
**Status no planejamento histórico:** ✅ PTC defendido e aprovado | 🟢 TCC Fase 1 em andamento
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
🟢 Mar 2026: TCC iniciado - Fase 1 (desenvolvimento do protótipo)
⏳ Abr-Mai 2026: Completar TCC - Fases 2-3 (validação experimental)
🎯 Jun 2026: DEFESA FINAL DO TCC
```

### Estrutura do Projeto (3 Fases)

| Fase | Nome | Status | Período | Entrega |
|------|------|--------|---------|---------|
| **Fase 1** | Revisão Sistemática | ✅ **CONCLUÍDA** | Jan-Mar 2026 | PTC defendido |
| **Fase 2** | Desenvolvimento Protótipo | 🟢 **EM ANDAMENTO** | Mar-Abr 2026 | MVP funcional |
| **Fase 3** | Validação Experimental | ⏳ Pendente | Mai 2026 | Resultados validação |

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

## 📋 O QUE PRECISAMOS FAZER AGORA (TCC)

### Estratégia

As correções serão incorporadas **na versão final do TCC** (não precisamos refazer o PTC, que já foi aprovado).

### Etapa 1: Correções Terminológicas (Semanas 1-2 do TCC)

**Tempo:** 5-7 horas  
**Prioridade:** ALTA

- [ ] Substituir "seguindo o protocolo PRISMA 2020" → "com relato estruturado conforme PRISMA 2020"
- [ ] Adicionar parágrafo explicativo sobre Cochrane (condução) vs. PRISMA (relato)
- [ ] Criar apêndice com checklist PRISMA 2020 completo (27 itens)
- [ ] Marcar itens atendidos no checklist

**Arquivos afetados:**
- `introducao.tex` (2 correções)
- `metodologia.tex` (3 modificações)
- `apendice-prisma-checklist.tex` (novo arquivo, ~200 linhas)
- `main.tex` (1 inclusão)

### Etapa 2: Complementos Metodológicos (planejamento histórico; Semanas 2-4 do TCC)

**Tempo:** 10-12 horas  
**Prioridade:** MÉDIA (pode ser feito em paralelo ao desenvolvimento do protótipo)

- [ ] Aplicar MMAT 2018 aos 16 estudos do baseline vigente (o planejamento histórico mencionava 17; ~30 min cada)
- [ ] Criar tabela de qualidade metodológica
- [ ] Adicionar seção "Avaliação da Qualidade Metodológica" em metodologia.tex
- [ ] Adicionar seção "Limitações da Revisão" em conclusao.tex
- [ ] Atualizar checklist PRISMA (itens 9, 14, 20, 21 passam de ⚠️ para ✅)

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
| **Versão Final TCC** | 27/27 | 0/27 | 100% ✅ |

**Meta:** Versão final do TCC com aderência total ao PRISMA 2020.

---

## 🎯 CRONOGRAMA SUGERIDO

### Semana 1 do TCC (Esta semana)

**Foco:** Correções terminológicas + início do protótipo

- [ ] Segunda-feira: Revisar plano com orientador
- [ ] Terça-feira: Copiar arquivos PTC → estrutura TCC
- [ ] Quarta-quinta: Executar correções 1.1.A, 1.1.B, 1.2.A, 1.2.B (3h)
- [ ] Sexta-feira: Criar apêndice PRISMA checklist (3h)
- [ ] Paralelo: Iniciar design do protótipo

### Semana 2 do TCC

**Foco:** Compilar versão corrigida + continuar protótipo

- [ ] Segunda: Compilar LaTeX, verificar erros
- [ ] Terça: Enviar versão corrigida ao orientador
- [ ] Quarta-sexta: Iniciar avaliação MMAT (primeiros 5-6 estudos)
- [ ] Paralelo: Desenvolvimento do protótipo

### Semanas 3-4 do TCC (planejamento histórico)

**Foco:** Completar MMAT + seção de limitações

- [ ] Completar MMAT dos 16 estudos atuais (o plano histórico mencionava 17)
- [ ] Criar tabela de qualidade
- [ ] Escrever seção de limitações
- [ ] Atualizar checklist PRISMA
- [ ] Paralelo: Desenvolvimento do protótipo

### Semana 5+ do TCC

**Foco:** Validação experimental (Fase 3) + integração final

- [ ] Versão final da dissertação com todas as correções
- [ ] Preparar defesa final

---

## 💡 BENEFÍCIOS DA OBSERVAÇÃO DA BANCA

**Não foi uma crítica negativa, foi uma contribuição pedagógica valiosa:**

1. ✅ **Aprofundou compreensão metodológica** - Agora entendemos claramente a distinção entre condução (Cochrane) e relato (PRISMA)

2. ✅ **Fortaleceu fundamentação do protótipo** - A aplicação planejada do MMAT poderá identificar quais estudos têm maior qualidade metodológica, permitindo decisões de design baseadas em evidências robustas após a reaplicação ao conjunto atual

3. ✅ **Melhorou transparência** - O checklist completo PRISMA 2020 tornará a dissertação mais transparente e reproduzível

4. ✅ **Preparou para publicação** - A versão final do TCC terá padrão de qualidade suficiente para publicação em periódico científico

5. 🎯 **Objetivo de transparência** - aderência integral ao PRISMA 2020 e avaliação MMAT só poderão ser reivindicadas após a consolidação da reaplicação no conjunto atual

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

- ✅ Revisão sistemática: baseline histórico preservado (9.431 → 6.914 → 17 estudos) e baseline vigente validado (11.904 → 9.413 excluídos na triagem → 2.491 → 2.475 excluídos na elegibilidade → 16 estudos)
- ✅ Pipeline automatizado e reproduzível (GitHub)
- ✅ Diagrama PRISMA flow
- ✅ Síntese narrativa dos achados
- ✅ PTC defendido e aprovado
- ✅ Base sólida para desenvolvimento do protótipo

### O Que Está EM ANDAMENTO 🟢

- 🟢 TCC Fase 1: Desenvolvimento do protótipo
- 🟢 Incorporação das correções PRISMA na versão final

### O Que Está PENDENTE ⏳

- ⏳ Correções terminológicas (Etapa 1) - 5-7h
- ⏳ Reaplicação da avaliação MMAT aos 16 estudos atuais e consolidação da tabela - 10-12h
- ⏳ Auditoria da integridade dos identificadores (DOIs repetidos e registros sem DOI), conforme reconciliação do baseline
- ⏳ Seção de limitações (Etapa 2) - 2h
- ⏳ Validação experimental do protótipo (Fase 3)
- ⏳ Defesa final do TCC

---

## 🎯 PRÓXIMA AÇÃO IMEDIATA (STATUS ATUAL)

**O que fazer AGORA:**

1. Reaplicar o MMAT aos 16 estudos atuais e registrar os julgamentos por critério
2. Consolidar a decisão sobre os DOIs repetidos e os registros sem DOI
3. Atualizar o relato final somente após essas verificações

**Minha recomendação:**

Fazer **Etapa 1 AGORA** (5-7 horas) porque:
- É rápido (1-2 sessões de trabalho)
- Remove pressão mental de "dívida técnica pendente"
- Permite focar 100% no protótipo depois sem interrupções
- Base da dissertação fica pronta desde já

**Etapa 2** pode ser feita em paralelo ao protótipo nas semanas 2-4 (fragmentado: 1-2h por dia).

---

**Precisa de alguma clarificação ou quer que eu execute as correções da Etapa 1 agora?**
