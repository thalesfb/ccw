# MEMORANDO TÉCNICO AO ORIENTADOR

**Assunto:** Incorporação de ajustes sobre PRISMA 2020 na versão final do TCC
**Data:** 07 de março de 2026
**De:** Thales Ferreira Batista (aluno de Ciência da Computação - IFC Videira)
**Para:** Prof. Dr. Rafael Zanin (Orientador) e Prof. Dr. Manassés Ribeiro (Coorientador)
**Status:** Documento histórico; PTC defendido e aprovado | estado atual na reconciliação do baseline

> **Nota de atualização (01/09/2026):** este memorando registra o contexto e o plano do baseline histórico. A revisão foi reexecutada posteriormente: o snapshot vigente contém 11.904 registros e 16 retidos operacionalmente (15 classificados provisoriamente como empíricos, com 6918 em hold por conflito temporal, + o protocolo contextual 6921); 23 candidatos foram auditados e 7 overrides manuais foram registrados, dos quais 4 ainda aguardam adjudicação de escopo. A reavaliação documental do MMAT foi registrada para os registros empíricos, com nove textos primários revisados externamente, mas fontes restantes, localizadores, adjudicação e conclusão final permanecem pendentes. Para decisões atuais, prevalece `docs/RECONCILIACAO-BASELINE-2026-08-31.md`.

---

## 1. CONTEXTO

Durante a defesa do PTC (já aprovada), a banca examinou a seção de metodologia e identificou uma imprecisão terminológica no posicionamento do PRISMA 2020. A observação específica foi:

> **"PRISMA 2020 não é metodologia/protocolo de condução da revisão, é guideline de relato"**

**Situação atual:** PTC foi aprovado com esta ressalva. Agora, na fase de construção do TCC, devemos incorporar as correções na versão final da dissertação.

## 2. ANÁLISE TÉCNICA DA OBSERVAÇÃO

### 2.1. A Banca Está Tecnicamente Correta

Consultamos o artigo fonte do PRISMA 2020 (Page et al., 2021, BMJ, DOI: 10.1136/bmj.n71) e confirmamos que o documento explicita claramente:

> *"PRISMA 2020 is **not intended to guide systematic review conduct**, for which comprehensive resources are available [...] PRISMA 2020 **should not be used to assess the conduct or methodological quality** of systematic reviews; other tools exist for this purpose. Furthermore, PRISMA 2020 is **not intended to inform the reporting of systematic review protocols**, for which a separate statement is available (PRISMA-P 2015)"*

**Tradução e interpretação:**
- PRISMA 2020 = **guideline de RELATO** (reporting guideline)
- PRISMA 2020 ≠ **metodologia de CONDUÇÃO** (conduct guidance)
- Para condução: Cochrane Handbook, IOM Standards, COSMOS-E
- Para protocolos: PRISMA-P 2015
- Para avaliação de qualidade: ROBIS, AMSTAR 2

### 2.2. O Problema Identificado no PTC

Em diversos pontos do documento, utilizamos formulações como:

- **introducao.tex, linha 37:** *"revisão sistemática da literatura seguindo o protocolo \cite{PRISMA2020}"*
- **introducao.tex, linha 56:** *"revisão sistemática seguindo o protocolo PRISMA 2020"*
- **metodologia.tex, linha 7:** *"seguindo as diretrizes PRISMA 2020"*

**Problema:** A expressão "seguindo o protocolo PRISMA 2020" implica que PRISMA foi usado como metodologia de **condução**, quando na verdade foi/deve ser usado como checklist de **relato**.

### 2.3. Situação do baseline histórico do PTC

**Importante:** O diagnóstico abaixo descreve o baseline histórico do PTC e
não valida o snapshot vigente. Os números históricos são preservados para
rastreabilidade, mas não devem ser reutilizados como resultado atual:

🗂️ **Busca histórica documentada** - 4 bases de dados, 72 queries bilíngues estruturadas
🗂️ **Contagem histórica** - 9.431 registros identificados → 6.914 linhas preservadas
🗂️ **Deduplicação descrita no histórico** - DOI e similaridade de título >0,9; a execução não possui ledger independente dos pares
🗂️ **Triagem histórica** - scoring de relevância com limiar 4,0/10
🗂️ **Seleção histórica** - 1.883 registros avaliados → 17 incluídos no relato do PTC
🗂️ **Extração e diagrama históricos** - metadados e fluxo PRISMA preservados como contexto
🗂️ **Síntese histórica** - categorização por técnica e aplicação, sem autoridade sobre o snapshot atual

Esses itens são evidência documental do PTC, não uma conclusão de que a
deduplicação histórica foi independentemente reproduzida ou de que o conjunto
histórico ainda seja o corpus vigente.

## 3. IMPACTO E GRAVIDADE

### 3.1. Gravidade: BAIXA (Correção Cirúrgica Viável)

**Importante:** A banca aprovou o PTC reconhecendo a qualidade metodológica do trabalho apesar desta observação.

- ❌ **NÃO** substitui a reconciliação do snapshot vigente
- ❌ **NÃO** permite transferir automaticamente contagens ou julgamentos para os 16 registros atuais
- ✅ **SIM** exige que o baseline histórico permaneça rotulado como histórico e não reproduzível independentemente
- ✅ **SIM** exige correções terminológicas em 5-8 pontos do texto (para versão final TCC)
- ✅ **SIM** exige complementação de alguns itens do checklist PRISMA (para versão final TCC)

### 3.2. Precedentes na Literatura

Este tipo de imprecisão terminológica é comum em trabalhos iniciais com PRISMA:

- Moher et al. (2015) reportaram que ~40% dos autores confundem PRISMA com metodologia
- A própria comunidade PRISMA publicou diversos editoriais esclarecendo o escopo desde 2009
- Revisões sistemáticas publicadas em periódicos de alto impacto já receberam correções similares pós-aceite

## 4. PLANO DE CORREÇÃO PARA VERSÃO FINAL DO TCC

> **Aplicação ao snapshot vigente:** as tarefas de avaliação abaixo devem ser
> executadas sobre os **15 registros empíricos aplicáveis**. O protocolo
> contextual 6921 permanece separado. As menções a 17 estudos nas
> seções que descrevem a execução do PTC são históricas e não representam o
> conjunto vigente.

### 4.1. Correções Terminológicas (Prioridade Alta - 1ª quinzena do TCC)

**A. Correções terminológicas em introducao.tex:**

| Localização | ANTES | DEPOIS |
|-------------|-------|--------|
| Linha 37 (OE1) | "seguindo o protocolo \cite{PRISMA2020}" | "com relato estruturado conforme PRISMA 2020 \cite{PRISMA2020}" |
| Linha 56 | "seguindo o protocolo PRISMA 2020" | "cujo relato segue as diretrizes PRISMA 2020" |

**B. Correções em metodologia.tex:**

| Localização | ANTES | DEPOIS |
|-------------|-------|--------|
| Linha 7 | "seguindo as diretrizes PRISMA 2020" | "com relato estruturado conforme PRISMA 2020" |
| Linha 4 (título) | "Protocolo da Revisão Sistemática" | "Protocolo e Relato da Revisão Sistemática" |

**C. Adição de seção explicativa em metodologia.tex (após linha 9):**

Inserir novo parágrafo esclarecendo:

```latex
A condução desta revisão sistemática fundamentou-se em princípios
metodológicos consolidados (Cochrane Handbook for Systematic Reviews,
Institute of Medicine Standards). O relato dos resultados segue
integralmente as 27 recomendações do PRISMA 2020 (checklist completo
disponível no Apêndice X), garantindo transparência, reprodutibilidade
e completude na comunicação dos achados.
```

**D. Criação de Apêndice com Checklist PRISMA 2020:**

- Criar arquivo: `pretextuais/apendice-prisma-checklist.tex`
- Incluir tabela com os 27 itens do PRISMA 2020
- Marcar com ✓ os itens atendidos e listar localização no documento
- Para itens não aplicáveis, justificar brevemente

### 4.2. Complementos Metodológicos (Durante TCC - paralelo ao desenvolvimento do protótipo)

**E. Avaliação de Qualidade Metodológica:**

Atualmente o item #9 do PRISMA 2020 ("Risk of bias assessment") não está explicitamente atendido. Recomenda-se:

1. Concluir e adjudicar o **MMAT** (Mixed Methods Appraisal Tool) nos 15
   registros empíricos aplicáveis; o protocolo 6921 permanece fora da avaliação
   empírica
   - Justificativa: Cobre múltiplos desenhos de estudo (quantitativos, qualitativos, mistos)
   - Tempo estimado: 6-8 horas (20-30 min por estudo)

2. Criar tabela de qualidade metodológica em `resultados.tex`:
   - Colunas: Registro | Desenho | S1/S2/Q1--Q5 | Base da evidência |
     Localizador | Limitações Principais

3. Adicionar subseção em `metodologia.tex`:
   ```latex
   \subsection{Avaliação da Qualidade Metodológica}

   Os registros empíricos foram avaliados quanto à qualidade metodológica
   utilizando o Mixed Methods Appraisal Tool (MMAT) versão 2018 \cite{MMAT2018}...
   ```

**F. Seção de Limitações:**

Adicionar seção explícita em `conclusao.tex`:

```latex
\section{Limitações da Revisão}

Reconhecemos as seguintes limitações metodológicas:

1. **Ausência de registro prospectivo**: Esta revisão não foi registrada
   no PROSPERO antes da execução devido a restrições de cronograma acadêmico.

2. **Screening por revisor único**: A triagem de elegibilidade foi realizada
   por um único revisor com suporte de sistema algorítmico de scoring,
   aumentando risco de viés de seleção em comparação com dupla-revisão
   independente.

3. **Dependência de abstracts**: A triagem inicial baseou-se em títulos
   e resumos devido à inviabilidade de obter textos completos de 6.914 estudos.
```

## 5. IMPACTO NO CRONOGRAMA DO TCC

### Distribuição ao longo da Fase 1 do TCC:

| Período | Atividade | Tempo | Prioridade |
|---------|-----------|-------|------------|
| 1ª-2ª semana | Correções terminológicas (A-C) | 2-3 horas | Alta |
| 1ª-2ª semana | Criação do checklist PRISMA (D) | 3-4 horas | Alta |
| 2ª-3ª semana | Avaliação MMAT (E) | 8-10 horas | Média |
| 3ª-4ª semana | Seção de limitações (F) | 2 horas | Média |

**Total estimado:** 15-19 horas de trabalho adicional
**Vantagem:** Estas atividades podem ser feitas em paralelo ao desenvolvimento do protótipo, sem impactar cronograma principal

## 6. POSICIONAMENTO ADOTADO NA DEFESA DO PTC (REGISTRADO)

### 6.1. Reconhecimento da Observação

> "Agradecemos a observação precisa da banca. De fato, PRISMA 2020 é uma
> guideline de relato (reporting guideline), não uma metodologia de condução.
> A confusão terminológica identificada será corrigida na versão final do TCC."

### 6.2. Reafirmação da Metodologia (mantida na defesa)

> "A revisão sistemática foi conduzida seguindo princípios do Cochrane Handbook
> e do Institute of Medicine. O PRISMA 2020 foi utilizado como framework de
> relato para garantir transparência e completude na comunicação dos achados,
> função para a qual foi expressamente projetado."

### 6.3. Compromisso de Completude

> "Na transição para o TCC, completaremos o checklist de 27 itens do PRISMA 2020,
> adicionaremos avaliação de qualidade metodológica com MMAT, e incluiremos seção
> explícita de limitações da evidência."

## 7. RECOMENDAÇÃO PARA VERSÃO FINAL DO TCC

**Posicionamento adotado:**

A observação da banca foi aceita e será incorporada integralmente na versão final. Ações:

1. ✅ **Executar** as correções terminológicas nas primeiras 2 semanas do TCC
2. ✅ **Incorporar** o checklist PRISMA completo no apêndice da dissertação final
3. 🟡 **Consolidar** a avaliação de qualidade (MMAT) dos 15 registros empíricos, após a reavaliação preliminar
4. ✅ **Adicionar** seção robusta de limitações na discussão final

**Benefício adicional:** A aplicação do MMAT aos 15 registros empíricos, mantendo o protocolo 6921 separado, poderá fortalecer a fundamentação das decisões de design do protótipo, criando ponte metodológica entre as Fases 1 e 2 do projeto. Isso ainda não é uma conclusão disponível, pois a adjudicação está pendente.

Este ajuste não representa retrabalho, mas aprimoramento natural da articulação entre condução metodológica (Cochrane) e relato transparente (PRISMA), agregando rigor à dissertação final.

---

## 8. REFERÊNCIAS CONSULTADAS

1. Page MJ, McKenzie JE, Bossuyt PM, et al. **The PRISMA 2020 statement: an updated guideline for reporting systematic reviews.** BMJ 2021;372:n71. doi: 10.1136/bmj.n71

2. Moher D, Shamseer L, Clarke M, et al. **Preferred reporting items for systematic review and meta-analysis protocols (PRISMA-P) 2015 statement.** Syst Rev. 2015;4(1):1. doi: 10.1186/2046-4053-4-1

3. Higgins JPT, Thomas J, Chandler J, et al. **Cochrane Handbook for Systematic Reviews of Interventions** version 6.4 (updated August 2023). Cochrane, 2023.

4. Hong QN, Pluye P, Fàbregues S, et al. **Mixed Methods Appraisal Tool (MMAT), version 2018.** Registration of Copyright (#1148552), Canadian Intellectual Property Office, Industry Canada.

---

**Contexto atual (01/09/2026):** o plano acima permanece histórico. O baseline vigente e as próximas decisões científicas estão em `docs/RECONCILIACAO-BASELINE-2026-08-31.md`; não há cronograma vigente inferido deste memorando.

**Aguardo orientações sobre como proceder.**

Atenciosamente,
Thales Ferreira Batista
Aluno de Ciência da Computação
Instituto Federal Catarinense - Campus Videira
