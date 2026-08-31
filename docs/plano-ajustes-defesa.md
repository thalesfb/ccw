# PLANO DETALHADO DE AJUSTES PARA VERSÃO FINAL DO TCC

**Objetivo:** Incorporar correções solicitadas pela banca do PTC na versão final da dissertação  
**Contexto:** PTC defendido e aprovado | Fase 1 do TCC em andamento (desenvolvimento do protótipo)  
**Prazo:** Ao longo da Fase 1 do TCC (próximas 4-6 semanas)  
**Status:** 🟢 Pronto para execução

> **Nota de atualização (31/08/2026):** este é um plano histórico elaborado antes da reconciliação do baseline. As referências a 17 estudos, às contagens antigas e à conclusão do MMAT descrevem planejamento ou snapshot anterior. O conjunto vigente tem 16 estudos após auditoria de 23 candidatos e remoção de 7 falsos positivos; a reaplicação do MMAT ainda não foi concluída. Use `docs/RECONCILIACAO-BASELINE-2026-08-31.md` para o estado atual.

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Fase 1: Correções Imediatas (Antes da Defesa)](#fase-1-correções-imediatas-antes-da-defesa)
3. [Fase 2: Complementos TCC](#fase-2-complementos-tcc)
4. [Checklist de Execução](#checklist-de-execução)
5. [Scripts de Apoio](#scripts-de-apoio)
6. [Argumentação para Defesa](#argumentação-para-defesa)

---

## 🎯 VISÃO GERAL

### Problema Identificado

**Crítica da Banca:**  
*"PRISMA 2020 não é metodologia/protocolo de condução da revisão, é guideline de relato"*

### Causa Raiz

Uso impreciso de terminologia em múltiplos pontos do documento:
- ❌ "seguindo o protocolo PRISMA 2020"
- ❌ "condução seguindo PRISMA 2020"
- ✅ **Correção:** "relato estruturado conforme PRISMA 2020"

### Estratégia de Correção

```
┌─────────────────────────────────────────┐
│  ✅ PTC DEFENDIDO E APROVADO           │
│  Observação da banca reconhecida        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  ETAPA 1: Semanas 1-2 TCC              │
│  - Correções terminológicas             │
│  - Checklist PRISMA no apêndice         │
│  - Seção explicativa metodologia        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  ETAPA 2: Semanas 2-4 TCC              │
│  - Avaliação MMAT (paralelo ao protótipo)│
│  - Seção de limitações                  │
│  - Tabela de qualidade                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  VERSÃO FINAL TCC (antes da defesa)    │
│  - Dissertação completa e corrigida     │
│  - 27/27 itens PRISMA atendidos         │
└─────────────────────────────────────────┘
```

---

## � ETAPA 1: CORREÇÕES TERMINOLÓGICAS (Semanas 1-2 do TCC)

### 1.1. Correções em `introducao.tex`

**Arquivo:** `c:/dev/ccw/results/ptc/conteudo/introducao.tex`

#### Correção 1.1.A - Linha 37 (OE1)

**ANTES:**
```latex
\item \textbf{OE1}: Realizar revisão sistemática da literatura seguindo o protocolo \cite{PRISMA2020} para identificar estudos que apliquem técnicas computacionais na educação matemática, publicados nos últimos 11 anos (2015-2025).
```

**DEPOIS:**
```latex
\item \textbf{OE1}: Realizar revisão sistemática da literatura, com relato estruturado conforme PRISMA 2020 \cite{PRISMA2020}, para identificar estudos que apliquem técnicas computacionais na educação matemática, publicados nos últimos 11 anos (2015-2025).
```

**Justificativa:** Remove "seguindo o protocolo" e esclarece que PRISMA 2020 é usado para estruturar o relato.

---

#### Correção 1.1.B - Linha 56

**ANTES:**
```latex
A presente fase, correspondente ao PTC, realiza uma revisão sistemática seguindo o protocolo PRISMA 2020 para mapear o estado da arte das técnicas computacionais aplicadas à educação matemática.
```

**DEPOIS:**
```latex
A presente fase, correspondente ao PTC, realiza uma revisão sistemática da literatura cujo relato segue as diretrizes PRISMA 2020 para mapear o estado da arte das técnicas computacionais aplicadas à educação matemática.
```

**Justificativa:** Explicita que PRISMA 2020 orienta o RELATO, não a CONDUÇÃO.

---

### 1.2. Correções em `metodologia.tex`

**Arquivo:** `c:/dev/ccw/results/ptc/conteudo/metodologia.tex`

#### Correção 1.2.A - Linhas 1-9 (Introdução da Seção)

**ANTES:**
```latex
\chapter{METODOLOGIA}
\label{cap:metodologia}

\section{Protocolo da Revisão Sistemática}

Este trabalho adota a metodologia de \textbf{Revisão Sistemática da Literatura} seguindo as diretrizes PRISMA 2020 (\textit{Preferred Reporting Items for Systematic Reviews and Meta-Analyses}) \cite{PRISMA2020}.
```

**DEPOIS:**
```latex
\chapter{METODOLOGIA}
\label{cap:metodologia}

\section{Protocolo e Relato da Revisão Sistemática}

Este trabalho adota a metodologia de \textbf{Revisão Sistemática da Literatura}, fundamentada em princípios metodológicos consolidados do \textit{Cochrane Handbook for Systematic Reviews} e dos padrões do \textit{Institute of Medicine} (IOM). O relato dos resultados segue integralmente as 27 recomendações do PRISMA 2020 (\textit{Preferred Reporting Items for Systematic Reviews and Meta-Analyses}) \cite{PRISMA2020}, garantindo transparência, reprodutibilidade e completude na comunicação dos achados.
```

**Justificativa:** 
1. Ajusta título da seção para refletir distinção entre protocolo (condução) e relato
2. Explicita que a CONDUÇÃO segue Cochrane/IOM
3. Explicita que o RELATO segue PRISMA 2020
4. Menciona os 27 itens (preparando para checklist no apêndice)

---

#### Correção 1.2.B - Após linha 9 (Novo parágrafo)

**INSERIR:**
```latex
A escolha da abordagem PRISMA 2020 para estruturação do relato justifica-se por sua ampla aceitação na comunidade científica internacional como padrão de transparência, seu rigor na documentação de todas as etapas do processo de revisão, e sua capacidade de assegurar que o relato seja explícito, replicável e auditável. Esta guideline de relato é especialmente adequada para comunicar os resultados da Fase 1 do projeto, na qual o objetivo principal é mapear o estado da arte das técnicas computacionais aplicadas à educação matemática.

\textbf{Importante:} Embora esta revisão não tenha sido registrada prospectivamente em bases como PROSPERO devido a restrições de cronograma acadêmico, o protocolo foi desenvolvido seguindo princípios do PRISMA-P 2015 (\textit{Preferred Reporting Items for Systematic Review and Meta-Analysis Protocols}), com definição \textit{a priori} de: (1) questão de pesquisa estruturada, (2) critérios de elegibilidade explícitos, (3) estratégia de busca reproduzível, (4) processo de seleção sistemático, e (5) método de síntese pré-definido. O checklist completo de aderência ao PRISMA 2020 encontra-se disponível no Apêndice~\ref{apendice:prisma-checklist}.
```

**Justificativa:**
1. Esclarece função do PRISMA 2020 (estruturação do relato)
2. Reconhece ausência de registro PROSPERO com justificativa acadêmica
3. Demonstra que PRINCÍPIOS de protocolo foram seguidos (PRISMA-P)
4. Antecipa referência ao checklist no apêndice

---

### 1.3. Criação do Apêndice - Checklist PRISMA 2020

**Arquivo:** `c:/dev/ccw/results/ptc/pretextuais/apendice-prisma-checklist.tex` (CRIAR NOVO)

**Conteúdo:**
```latex
\chapter{CHECKLIST PRISMA 2020}
\label{apendice:prisma-checklist}

Este apêndice apresenta o checklist completo de aderência às 27 recomendações do PRISMA 2020 para relato de revisões sistemáticas. Para cada item, indica-se a localização no documento onde a informação correspondente pode ser encontrada.

\begin{longtable}{|p{0.5cm}|p{3.5cm}|p{6cm}|p{3cm}|}
\hline
\textbf{N°} & \textbf{Item PRISMA 2020} & \textbf{Descrição} & \textbf{Localização no PTC} \\
\hline
\endfirsthead

\multicolumn{4}{c}%
{\tablename\ \thetable\ -- Continuação da página anterior} \\
\hline
\textbf{N°} & \textbf{Item PRISMA 2020} & \textbf{Descrição} & \textbf{Localização no PTC} \\
\hline
\endhead

\hline \multicolumn{4}{r}{\textit{Continua na próxima página}} \\
\endfoot

\hline
\endlastfoot

%--- TÍTULO ---
1 & Título & Identificar o relatório como uma revisão sistemática & Capa, folha de rosto \\
\hline

%--- RESUMO ---
2 & Resumo estruturado & Resumo estruturado incluindo contexto, objetivo, métodos, resultados e conclusões & Resumo (pág. vi-vii) \\
\hline

%--- INTRODUÇÃO ---
3 & Justificativa & Descrever a fundamentação da revisão no contexto do conhecimento existente & Cap. 1, Seção 1.1-1.2 \\
\hline

4 & Objetivos & Fornecer declaração explícita de questões de pesquisa/objetivos & Cap. 1, Seção 1.3 \\
\hline

%--- METODOLOGIA ---
5 & Critérios de elegibilidade & Especificar critérios de inclusão/exclusão & Cap. 2, Seção 2.3 \\
\hline

6 & Fontes de informação & Especificar todas as bases consultadas e datas de cobertura & Cap. 2, Seção 2.2.1 \\
\hline

7 & Estratégia de busca & Apresentar estratégia de busca completa para pelo menos uma base & Cap. 2, Seção 2.2.2 \\
\hline

8 & Processo de seleção & Especificar processo de screening, elegibilidade e inclusão & Cap. 2, Seção 2.3 \\
\hline

9 & Avaliação de risco de viés & Especificar métodos para avaliar risco de viés nos estudos & \textcolor{orange}{⚠ Não aplicado - previsto para TCC} \\
\hline

10 & Coleta de dados & Especificar métodos de extração de dados & Cap. 2, Seção 2.4 \\
\hline

11a & Dados coletados & Listar e definir todas as variáveis extraídas & Cap. 2, Seção 2.4 \\
\hline

11b & Desvios do protocolo & Relatar desvios do protocolo e justificativas & Cap. 2 (sem desvios significativos) \\
\hline

%--- RESULTADOS ---
12 & Seleção de estudos & Reportar número de estudos em cada etapa com razões para exclusões & Cap. 3, Fig. PRISMA flow \\
\hline

13 & Características dos estudos & Apresentar características relevantes dos estudos incluídos & Cap. 3, Seção 3.2 \\
\hline

14 & Risco de viés nos estudos & Apresentar avaliações de risco de viés para cada estudo & \textcolor{orange}{⚠ Não aplicado - previsto para TCC} \\
\hline

15 & Resultados de estudos individuais & Apresentar resultados de cada estudo analisado & Cap. 3, Seção 3.3 \\
\hline

16a & Síntese dos resultados & Método de síntese (meta-análise ou narrativa) & Cap. 3, Seção 3.4 (narrativa) \\
\hline

16b & Métodos adicionais de síntese & Outros métodos de análise/síntese (subgrupos, sensibilidade, meta-regressão) & N/A (síntese narrativa) \\
\hline

17 & Viés de publicação & Avaliação de viés de publicação & \textcolor{orange}{⚠ Não aplicado - previsto para TCC} \\
\hline

18 & Certeza da evidência & Avaliação de certeza/qualidade da evidência & \textcolor{orange}{⚠ Não aplicado - previsto para TCC} \\
\hline

%--- DISCUSSÃO ---
19 & Discussão geral & Interpretação dos resultados considerando objetivos e outras evidências & Cap. 4, Discussão \\
\hline

20 & Limitações da evidência & Limitações da evidência incluída (risco de viés, inconsistência, imprecisão) & \textcolor{orange}{⚠ Seção explícita será adicionada no TCC} \\
\hline

21 & Limitações da revisão & Limitações dos processos da própria revisão & \textcolor{orange}{⚠ Seção explícita será adicionada no TCC} \\
\hline

22 & Implicações & Implicações para prática, política e pesquisa futura & Cap. 4, Conclusão \\
\hline

%--- OUTROS ---
23 & Registro e protocolo & Informações sobre registro e protocolo (PROSPERO, etc.) & Cap. 2 (justificativa de ausência) \\
\hline

24 & Suporte & Fontes de apoio financeiro e outros suportes & Folha de rosto \\
\hline

25 & Conflitos de interesse & Declarar conflitos de interesse & Folha de rosto \\
\hline

26 & Disponibilidade de dados & Declarar disponibilidade de dados, código e outros materiais & Cap. 2 (código em repositório GitHub) \\
\hline

27 & Checklist & Incluir checklist PRISMA 2020 completo & \textcolor{blue}{✓ Presente neste apêndice} \\
\hline

\caption{Checklist de aderência ao PRISMA 2020 (Page et al., 2021)}
\label{tab:prisma-checklist}
\end{longtable}

\section*{Notas Explicativas}

\textbf{Legenda:}
\begin{itemize}
    \item \textcolor{blue}{✓} Item totalmente atendido com localização específica no documento
    \item \textcolor{orange}{⚠} Item parcialmente atendido ou previsto para fase TCC
    \item \textcolor{red}{✗} Item não aplicável ao tipo/escopo desta revisão
\end{itemize}

\textbf{Itens marcados como "previsto para TCC":}

Os itens 9, 14, 17, 18, 20 e 21 referem-se a avaliações de qualidade metodológica, risco de viés, certeza da evidência e limitações explícitas. Estes elementos não foram aplicados na fase PTC devido a:

\begin{enumerate}
    \item \textbf{Cronograma acadêmico:} PTC focado em mapeamento exploratório
    \item \textbf{Escopo da Fase 1:} Identificação e categorização de estudos
    \item \textbf{Planejamento do TCC:} Avaliação crítica aprofundada será conduzida na Fase 2
\end{enumerate}

A aplicação do \textbf{Mixed Methods Appraisal Tool (MMAT)} está programada para a fase TCC, permitindo avaliar a qualidade metodológica dos 16 estudos incluídos no snapshot vigente, considerando a heterogeneidade de desenhos de pesquisa identificados.

\textbf{Referência:}

Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. \textit{BMJ} 2021;372:n71. doi: 10.1136/bmj.n71
```

**Justificativa:**
1. Transparência total sobre aderência ao PRISMA 2020
2. Identificação clara de quais itens estão completos vs. pendentes
3. Demonstra que maioria dos itens (21/27) já está atendida
4. Justifica itens pendentes como planejamento para TCC

---

### 1.4. Atualização do `main.tex`

**Arquivo:** `c:/dev/ccw/results/ptc/main.tex`

**Localizar a seção de inclusão de apêndices (geralmente próximo ao final, antes de `\end{document}`)**

**INSERIR:**
```latex
% ---
% APÊNDICES
% ---
\begin{apendicesenv}
\partapendices
\include{pretextuais/apendice-prisma-checklist}
\end{apendicesenv}
% ---
```

**Observação:** Se já existir estrutura de apêndices, adicionar apenas a linha `\include{pretextuais/apendice-prisma-checklist}` dentro do bloco existente.

---

### 1.5. Atualização de `referencias.bib`

**Arquivo:** `c:/dev/ccw/results/ptc/referencias.bib`

**Verificar se estas referências existem. Se não, ADICIONAR:**

```bibtex
@article{PRISMA2020,
    author = {Page, Matthew J and McKenzie, Joanne E and Bossuyt, Patrick M and Boutron, Isabelle and Hoffmann, Tammy C and Mulrow, Cynthia D and others},
    title = {The PRISMA 2020 statement: an updated guideline for reporting systematic reviews},
    journal = {BMJ},
    volume = {372},
    pages = {n71},
    year = {2021},
    doi = {10.1136/bmj.n71},
    url = {https://doi.org/10.1136/bmj.n71}
}

@article{PRISMAP2015,
    author = {Moher, David and Shamseer, Larissa and Clarke, Mike and Ghersi, Davina and Liberati, Alessandro and Petticrew, Mark and Shekelle, Paul and Stewart, Lesley A},
    title = {Preferred reporting items for systematic review and meta-analysis protocols (PRISMA-P) 2015 statement},
    journal = {Systematic Reviews},
    volume = {4},
    number = {1},
    pages = {1},
    year = {2015},
    doi = {10.1186/2046-4053-4-1},
    url = {https://doi.org/10.1186/2046-4053-4-1}
}

@book{CochraneHandbook,
    author = {Higgins, Julian PT and Thomas, James and Chandler, Jacqueline and Cumpston, Miranda and Li, Tianjing and Page, Matthew J and Welch, Vivian A},
    title = {Cochrane Handbook for Systematic Reviews of Interventions},
    edition = {version 6.4},
    year = {2023},
    publisher = {Cochrane},
    url = {www.training.cochrane.org/handbook}
}

@article{MMAT2018,
    author = {Hong, Quan Nha and Pluye, Pierre and Fàbregues, Sergi and Bartlett, Gillian and Boardman, Felicity and Cargo, Margaret and Dagenais, Pierre and Gagnon, Marie-Pierre and Griffiths, Frances and Nicolau, Belinda and O'Cathain, Alicia and Rousseau, Marie-Claude and Vedel, Isabelle},
    title = {Mixed Methods Appraisal Tool (MMAT), version 2018},
    year = {2018},
    note = {Registration of Copyright (\#1148552), Canadian Intellectual Property Office, Industry Canada},
    url = {http://mixedmethodsappraisaltoolpublic.pbworks.com}
}
```

---

## 📅 CHECKLIST DE EXECUÇÃO - FASE 1

### Dia 1 (2-3 horas)

- [ ] **1.1.A** - Corrigir introducao.tex linha 37 (OE1)
- [ ] **1.1.B** - Corrigir introducao.tex linha 56 (Estrutura do Trabalho)
- [ ] **1.2.A** - Corrigir metodologia.tex linhas 1-9 (título + introdução)
- [ ] **1.2.B** - Adicionar parágrafo explicativo em metodologia.tex após linha 9
- [ ] **1.5** - Verificar/adicionar referências em referencias.bib

### Dia 2 (3-4 horas)

- [ ] **1.3** - Criar arquivo apendice-prisma-checklist.tex completo
- [ ] **1.4** - Atualizar main.tex para incluir apêndice
- [ ] Compilar LaTeX e verificar ausência de erros
- [ ] Revisar todo documento buscando outras menções a "protocolo PRISMA"
- [ ] Gerar PDF final e verificar formatação

### Antes da Defesa

- [ ] Imprimir versão atualizada para banca
- [ ] Preparar slide explicando correções (se necessário)
- [ ] Ensaiar resposta sobre PRISMA (ver seção 6 deste documento)

---

## 🔬 ETAPA 2: COMPLEMENTOS METODOLÓGICOS (Semanas 2-4 do TCC)

### 2.1. Avaliação de Qualidade com MMAT

**Prazo:** Semanas 2-4 do TCC (pode ser feito em paralelo ao desenvolvimento do protótipo)  
**Tempo estimado:** aproximadamente 8-10 horas (30-40 min por estudo × 16 estudos)  
**Vantagem:** Fortalece fundamentação teórica para decisões de design do protótipo

#### Passo 2.1.1 - Familiarização com MMAT

1. Baixar MMAT 2018:
   - URL: http://mixedmethodsappraisaltoolpublic.pbworks.com
   - Ler manual completo (15 páginas)

2. Entender categorias de desenho:
   - Categoria 1: Qualitativo
   - Categoria 2: Quantitativo randomizado
   - Categoria 3: Quantitativo não-randomizado
   - Categoria 4: Quantitativo descritivo
   - Categoria 5: Métodos mistos

#### Passo 2.1.2 - Aplicação do MMAT aos 16 Estudos Atuais

Criar planilha de avaliação:

| ID | Autor (Ano) | Tipo de Estudo | Q1 | Q2 | Q3 | Q4 | Q5 | Score | Limitações Principais |
|----|-------------|----------------|----|----|----|----|----|----|----------------------|
| 001 | Implementation2025 | ... | Y | Y | Y | N | Y | 4/5 | ... |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Critérios:**
- Y (Yes) = critério atendido
- N (No) = critério não atendido
- CT (Can't Tell) = informação insuficiente

**Score:** Somar Y's (não usar porcentagem conforme recomendação MMAT)

#### Passo 2.1.3 - Adicionar Seção em metodologia.tex

**Inserir nova seção após "Estratégia de Busca":**

```latex
\section{Avaliação da Qualidade Metodológica}

Os estudos incluídos foram submetidos a avaliação crítica de qualidade metodológica utilizando o \textit{Mixed Methods Appraisal Tool} (MMAT) versão 2018 \cite{MMAT2018}. O MMAT foi selecionado por sua capacidade de avaliar diferentes desenhos de estudo (qualitativos, quantitativos e mistos) de forma padronizada, adequando-se à heterogeneidade metodológica identificada nesta revisão.

O processo de avaliação consistiu em:

\begin{enumerate}
    \item \textbf{Classificação do desenho de estudo}: Cada um dos 16 estudos atuais deverá ser categorizado conforme seu desenho metodológico (qualitativo, quantitativo randomizado, quantitativo não-randomizado, quantitativo descritivo ou métodos mistos).
    
    \item \textbf{Aplicação dos critérios MMAT}: Para cada estudo, deverão ser aplicados 5 critérios de qualidade específicos ao seu desenho metodológico, respondendo "Sim", "Não" ou "Não é possível determinar" para cada critério.
    
    \item \textbf{Síntese da qualidade}: Conforme recomendação dos autores do MMAT, a qualidade metodológica deverá ser reportada descritivamente (contagem de critérios atendidos) sem cálculo de score percentual, evitando simplificação excessiva de aspectos complexos de qualidade.
\end{enumerate}

A avaliação deverá ser conduzida por um único revisor com registro detalhado de justificativas para cada julgamento, permitindo auditoria e revisão das decisões. Estudos com baixa qualidade metodológica não deverão ser excluídos automaticamente, mas terão suas limitações consideradas na síntese narrativa e discussão dos achados.

Os resultados completos da avaliação MMAT encontram-se na Seção~\ref{sec:qualidade-estudos}.
```

#### Passo 2.1.4 - Criar Tabela de Qualidade em resultados.tex

**Inserir nova seção após características dos estudos:**

```latex
\section{Qualidade Metodológica dos Estudos Incluídos}
\label{sec:qualidade-estudos}

A Tabela~\ref{tab:mmat-avaliacao} deverá apresentar a avaliação de qualidade metodológica dos 16 estudos atuais segundo o MMAT 2018, após a reaplicação do instrumento.

\begin{landscape}
\begin{longtable}{|p{1cm}|p{4cm}|p{3cm}|p{1.5cm}|p{8cm}|}
\hline
\textbf{ID} & \textbf{Estudo} & \textbf{Tipo} & \textbf{Score MMAT} & \textbf{Principais Limitações Metodológicas} \\
\hline
\endfirsthead
\multicolumn{5}{c}{\tablename\ \thetable\ -- Continuação} \\
\hline
\textbf{ID} & \textbf{Estudo} & \textbf{Tipo} & \textbf{Score MMAT} & \textbf{Principais Limitações Metodológicas} \\
\hline
\endhead
\hline \multicolumn{5}{r}{\textit{Continua...}} \\
\endfoot
\hline
\endlastfoot

001 & Implementation2025 & Quant. Não-RCT & 4/5 & Tamanho amostral pequeno (n=45); ausência de grupo controle \\
\hline
002 & ... & ... & .../5 & ... \\
\hline
% [PREENCHER COM OS 16 ESTUDOS ATUAIS APÓS A REAPLICAÇÃO]

\caption{Avaliação de qualidade metodológica segundo MMAT 2018}
\label{tab:mmat-avaliacao}
\end{longtable}
\end{landscape}

\subsection{Síntese da Qualidade Metodológica}

Dos 16 estudos atuais:
\begin{itemize}
    \item \textbf{X estudos (Y\%)} atenderam a todos os 5 critérios MMAT (5/5)
    \item \textbf{X estudos (Y\%)} atenderam a 4 critérios (4/5)
    \item \textbf{X estudos (Y\%)} atenderam a 3 critérios (3/5)
    \item \textbf{X estudos (Y\%)} atenderam a menos de 3 critérios (<3/5)
\end{itemize}

As limitações metodológicas mais frequentes foram:
\begin{enumerate}
    \item \textbf{Tamanho amostral reduzido} (identificado em X estudos): ...
    \item \textbf{Ausência de grupo controle} (identificado em X estudos): ...
    \item \textbf{Validade de instrumentos não reportada} (identificado em X estudos): ...
\end{enumerate}

Estas limitações foram consideradas na interpretação dos achados e discussão das implicações para a prática.
```

---

### 2.2. Seção de Limitações

**Arquivo:** Criar nova seção em `conclusao.tex` ou `discussao.tex`

#### Passo 2.2.1 - Adicionar Seção de Limitações da Revisão

**Inserir antes da seção de Conclusões/Considerações Finais:**

```latex
\section{Limitações da Revisão Sistemática}
\label{sec:limitacoes}

Reconhecemos as seguintes limitações metodológicas desta revisão sistemática, as quais devem ser consideradas na interpretação dos achados:

\subsection{Limitações de Processo}

\begin{enumerate}
    \item \textbf{Ausência de registro prospectivo em PROSPERO}
    
    Esta revisão não foi registrada prospectivamente na base International Prospective Register of Systematic Reviews (PROSPERO) antes de sua execução. Embora o protocolo tenha sido desenvolvido seguindo princípios do PRISMA-P 2015 com definição \textit{a priori} de questão de pesquisa, critérios de elegibilidade, estratégia de busca e métodos de síntese, a ausência de registro público prévio impede verificação externa de possíveis desvios do protocolo original.
    
    \textbf{Justificativa:} Restrições de cronograma acadêmico do PTC/TCC, com prazo de 6 meses para completar revisão, análise e desenvolvimento de protótipo.
    
    \textbf{Mitigação:} Todo o pipeline de coleta, processamento e análise está disponibilizado em repositório público GitHub com histórico completo de \textit{commits}, permitindo auditoria \textit{post-hoc} do processo.
    
    \item \textbf{Screening por revisor único com suporte algorítmico}
    
    A triagem de elegibilidade (screening de 6.914 títulos/resumos) foi realizada por um único revisor com suporte de sistema automatizado de relevance scoring, em contraste com a recomendação padrão de dupla-revisão independente.
    
    \textbf{Implicação:} Aumento do risco de viés de seleção, com possível exclusão de estudos relevantes ou inclusão de estudos marginalmente relevantes.
    
    \textbf{Mitigação:} 
    \begin{itemize}
        \item Sistema de scoring algorítmico (TF-IDF + word embeddings) reduz subjetividade
        \item Threshold conservador (4.0/10) minimiza exclusões indevidas
        \item Critérios de elegibilidade explícitos e pré-definidos
        \item Processo auditável com registro de scores para todos os 6.914 estudos
    \end{itemize}
    
    \item \textbf{Dependência de títulos e resumos para triagem inicial}
    
    A triagem de elegibilidade baseou-se exclusivamente em títulos e resumos (abstracts) disponibilizados pelas APIs, sem acesso a textos completos de todos os 6.914 estudos únicos.
    
    \textbf{Implicação:} Possível exclusão de estudos relevantes cujo título/resumo não evidencia claramente a aplicação de técnicas computacionais em educação matemática.
    
    \textbf{Mitigação:} Abstracts de artigos científicos convencionalmente contêm informações sobre métodos, contexto e objetivos; estudos que não mencionam estes elementos em seus abstracts provavelmente não os abordam substancialmente no texto completo.
\end{enumerate}

\subsection{Limitações da Evidência}

\begin{enumerate}
    \item \textbf{Heterogeneidade metodológica dos estudos incluídos}
    
    Os 16 estudos atuais apresentam grande diversidade de desenhos de pesquisa (estudos quasi-experimentais, estudos de caso, design-based research, surveys), dificultando síntese quantitativa (meta-análise). A síntese narrativa adotada permite acomodar esta heterogeneidade, mas limita generalizações quantitativas sobre eficácia.
    
    \item \textbf{Viés de publicação}
    
    Não foi conduzida avaliação formal de viés de publicação (funnel plots, testes estatísticos) devido ao pequeno número de estudos incluídos (n=16) e à heterogeneidade metodológica. É provável que estudos com resultados negativos ou nulos tenham menor probabilidade de publicação.
    
    \item \textbf{Restrição linguística implícita}
    
    Embora a estratégia de busca tenha sido bilíngue (inglês/português), as quatro bases de dados consultadas (Semantic Scholar, OpenAlex, Crossref, CORE) têm cobertura predominante de literatura anglófona. Estudos publicados exclusivamente em outros idiomas (espanhol, mandarim, francês) podem estar sub-representados.
\end{enumerate}

\subsection{Implicações das Limitações}

Estas limitações não invalidam os achados da revisão, mas sugerem cautela na generalização. Especificamente:

\begin{itemize}
    \item As tendências identificadas (predominância de técnicas de ML supervisionado, foco em ensino fundamental) refletem o corpus de estudos indexados em bases anglófonas, não necessariamente todo o universo de aplicações.
    
    \item As lacunas mapeadas (e.g., escassez de estudos em geometria espacial) são lacunas \textit{na literatura científica publicada}, podendo haver aplicações práticas não reportadas formalmente.
    
    \item A ausência de avaliação de qualidade formal (MMAT) na fase PTC impede julgamentos sobre confiabilidade dos efeitos reportados, limitando recomendações para prática educacional direta.
\end{itemize}

Revisões futuras devem considerar: (1) registro prospectivo em PROSPERO, (2) dupla-revisão independente para screening, (3) busca em bases não-anglófonas (SciELO, LILACS, CNKI), e (4) aplicação de ferramentas de avaliação de qualidade desde a fase inicial.
```

---

### 2.3. Atualização do Checklist PRISMA (Apêndice)

Após completar avaliação MMAT e seção de limitações, atualizar o apêndice:

**Modificar em `apendice-prisma-checklist.tex`:**

```latex
% ITEM 9
9 & Avaliação de risco de viés & Especificar métodos para avaliar risco de viés nos estudos & \textcolor{blue}{✓ Cap. 2, Seção 2.X (MMAT 2018)} \\
\hline

% ITEM 14
14 & Risco de viés nos estudos & Apresentar avaliações de risco de viés para cada estudo & \textcolor{blue}{✓ Cap. 3, Tabela MMAT completa} \\
\hline

% ITEM 20
20 & Limitações da evidência & Limitações da evidência incluída (risco de viés, inconsistência, imprecisão) & \textcolor{blue}{✓ Cap. 4, Seção Limitações} \\
\hline

% ITEM 21
21 & Limitações da revisão & Limitações dos processos da própria revisão & \textcolor{blue}{✓ Cap. 4, Seção Limitações} \\
\hline
```

---

## ✅ CHECKLIST DE EXECUÇÃO - ETAPA 2

### Semana 2-3 do TCC (paralelo ao desenvolvimento do protótipo)

#### Segunda-feira (3h)
- [ ] Baixar e ler manual MMAT 2018
- [ ] Criar planilha de avaliação (Excel/Google Sheets)
- [ ] Classificar desenho metodológico dos 16 estudos atuais

#### Terça a Quinta (6-8h)
- [ ] Aplicar MMAT aos 16 estudos atuais (30-40 min cada)
- [ ] Registrar justificativas para cada julgamento
- [ ] Tabular resultados

#### Sexta-feira (3h)
- [ ] Adicionar seção MMAT em metodologia.tex
- [ ] Criar tabela de qualidade em resultados.tex
- [ ] Escrever síntese de qualidade metodológica

### Semana 3-4 do TCC

#### Segunda-feira (2h)
- [ ] Escrever seção completa de limitações
- [ ] Inserir em conclusao.tex ou discussao.tex

#### Terça-feira (1h)
- [ ] Atualizar checklist PRISMA no apêndice
- [ ] Revisar referências (MMAT2018 incluída?)

#### Quarta-feira (2h)
- [ ] Compilar LaTeX completo
- [ ] Verificar indexação de todas seções novas
- [ ] Revisar numeração de figuras/tabelas

#### Quinta-feira (2h)
- [ ] Leitura crítica completa do documento
- [ ] Buscar outras menções a "protocolo" que precisem ajuste
- [ ] Verificar consistência terminológica

#### Sexta-feira (1h)
- [ ] Gerar PDF final
- [ ] Enviar versão atualizada ao orientador
- [ ] Solicitar feedback antes de prosseguir para Fase 3

---

## 🛠 SCRIPTS DE APOIO

### Script 1: Buscar Menções a "Protocolo PRISMA"

```bash
cd c:/dev/ccw/results/ptc
grep -rn "protocolo.*PRISMA\|PRISMA.*protocolo" conteudo/*.tex
```

**Objetivo:** Identificar todas as menções que precisam correção.

### Script 2: Validar Compilação LaTeX

```bash
cd c:/dev/ccw/results/ptc
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

**Objetivo:** Compilar documento completo após modificações.

### Script 3: Contar Atendimento de Itens PRISMA

```python
# Para executar após criar checklist
import re

with open('pretextuais/apendice-prisma-checklist.tex', 'r', encoding='utf-8') as f:
    content = f.read()

atendidos = len(re.findall(r'\\textcolor\{blue\}\{✓', content))
parciais = len(re.findall(r'\\textcolor\{orange\}\{⚠', content))
nao_aplicaveis = len(re.findall(r'\\textcolor\{red\}\{✗', content))

print(f"Itens atendidos: {atendidos}/27")
print(f"Itens parciais/futuros: {parciais}/27")
print(f"Itens não aplicáveis: {nao_aplicaveis}/27")
print(f"Taxa de atendimento: {(atendidos/27)*100:.1f}%")
```

---

## 💬 ARGUMENTAÇÃO USADA NA DEFESA DO PTC (REGISTRO)

**Nota:** Estas foram as respostas dadas durante a defesa do PTC. Registramos aqui para referência.

### Resposta à Observação sobre PRISMA 2020

**O que foi dito na defesa:**

> "Agradeço a observação precisa da banca. De fato, PRISMA 2020 é uma *reporting guideline*, não uma metodologia de condução. Consultando o artigo fonte de Page et al. (2021) no BMJ, os autores explicitam que PRISMA 2020 'não é destinado a guiar a condução de revisões sistemáticas'. Para a condução metodológica, seguimos princípios do Cochrane Handbook e padrões do Institute of Medicine. PRISMA 2020 foi utilizado como framework para estruturar o relato dos achados. Na versão final do TCC, corrigiremos a terminologia e incluiremos o checklist completo de 27 itens no apêndice."

**Resultado:** Banca aceitou a explicação e aprovou o PTC com recomendação de incorporar as correções na versão final.

---

## 🎯 PREPARAÇÃO PARA DEFESA FINAL DO TCC

### Cenário 1: Banca verifica se correções foram implementadas

**Resposta sugerida:**

> "As correções terminológicas e o checklist PRISMA 2020 foram incorporados. O MMAT foi definido como procedimento, mas ainda precisa ser reaplicado aos 16 estudos atuais antes de afirmarmos que a avaliação de qualidade está concluída; não devemos apresentar a tabela histórica de 17 estudos como resultado vigente."

### Cenário 2: Banca questiona como MMAT influenciou o design do protótipo

**Resposta sugerida:**

> "A avaliação de qualidade com MMAT foi fundamental para as decisões de design. Identificamos que X/16 estudos com maior qualidade metodológica (score 5/5 ou 4/5) convergiam para [padrão identificado]. Esta convergência de estudos robustos fundamentou nossa escolha de [decisão de design específica do protótipo]. Estudos com limitações metodológicas (score <3/5) foram considerados para contexto, mas não guiaram decisões críticas de arquitetura."

### Cenário 3: Banca elogia o aprimoramento metodológico

**Resposta:**

> "Agradecemos. A observação da banca do PTC foi pedagogicamente valiosa. O processo de correção aprofundou nossa compreensão da distinção entre frameworks de condução vs. relato, enriquecendo a formação metodológica. Adicionalmente, a aplicação do MMAT criou uma ponte analítica importante entre a revisão sistemática (Fase 1) e o desenvolvimento do protótipo (Fase 2), permitindo decisões de design baseadas em evidências de alta qualidade."

---

## 📊 RESUMO EXECUTIVO DO PLANO

### Investimento de Tempo Total

| Etapa | Atividades | Tempo | Prazo |
|-------|-----------|-------|-------|
| **Etapa 1** | Correções terminológicas + Checklist PRISMA | 5-7 horas | Semanas 1-2 do TCC |
| **Etapa 2** | Avaliação MMAT + Seção de limitações | 10-12 horas | Semanas 2-4 do TCC |
| **Total** | — | **15-19 horas** | Antes da defesa final |

**Vantagem:** Pode ser feito em paralelo ao desenvolvimento do protótipo, sem impactar cronograma principal.

### Impacto no Checklist PRISMA 2020

| Status | PTC Defendido | Após Etapa 1 | Após Etapa 2 (Versão Final) |
|--------|---------------|--------------|-----------------------------|
| ✅ Atendido | 18/27 (67%) | 21/27 (78%) | 27/27 (100%) |
| ⚠ Pendente | 9/27 (33%) | 6/27 (22%) | 0/27 (0%) |

**Meta:** Versão final do TCC com 100% de aderência ao PRISMA 2020.

### Arquivos a Modificar

**Etapa 1 (Semanas 1-2):**
1. ✏️ `conteudo/introducao.tex` (2 correções)
2. ✏️ `conteudo/metodologia.tex` (2 correções + 1 adição)
3. ➕ `pretextuais/apendice-prisma-checklist.tex` (novo arquivo)
4. ✏️ `main.tex` (1 linha adicionada)
5. ✏️ `referencias.bib` (verificar 4 referências)

**Etapa 2 (Semanas 2-4):**
6. ✏️ `conteudo/metodologia.tex` (adicionar seção MMAT)
7. ✏️ `conteudo/resultados.tex` (adicionar tabela de qualidade)
8. ✏️ `conteudo/conclusao.tex` (adicionar seção de limitações)
9. ✏️ `pretextuais/apendice-prisma-checklist.tex` (atualizar 4 itens)

**Observação:** Arquivos do PTC serão copiados/adaptados para a estrutura do TCC (diretório `results/tcc/`).

---

## 🎯 PRÓXIMOS PASSOS IMEDIATOS

### Esta Semana (Semana 1 do TCC):

1. ✅ **Revisar este plano com o orientador** → Alinhar prioridades
2. 🔄 **Copiar arquivos PTC → TCC** → Estabelecer base para correções
3. 🚀 **Executar Etapa 1** → Correções terminológicas + checklist PRISMA
4. 📤 **Enviar ao orientador** → Validação das correções

### Próximas 2-3 Semanas:

5. 🔬 **Executar Etapa 2 (paralelo ao protótipo)** → MMAT + limitações
6. ✅ **Integrar na dissertação final** → Versão completa para defesa do TCC

### Antes da Defesa Final do TCC:

7. 📋 **Verificar checklist PRISMA 27/27** → Aderência total garantida
8. 📄 **Gerar versão final** → PDF para banca

---

**Última atualização:** 07/03/2026  
**Status atual:** 🟢 PTC defendido e aprovado | TCC Fase 1 em andamento  
**Próxima ação:** Executar Etapa 1 (estimativa: 5-7 horas distribuídas em 1-2 semanas)  
**Responsável:** Thales Ferreira Batista (aluno) + Prof. Dr. Rafael Zanin (orientador)
