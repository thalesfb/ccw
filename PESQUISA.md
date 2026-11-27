# PESQUISA.md — Contexto e Workflow de Pesquisa Cientifica

> Caderno de trabalho do pesquisador, com contexto, tarefas e procedimentos auxiliares.
> O TCC e os dados versionados permanecem como fontes do estado acadêmico publicado.
>
> **Ultima atualizacao:** 2026-11-18

> **Fluxo vigente:** as contagens atuais estão no TCC (`results/tcc/main.pdf`) e nos dados versionados em `research/data/`, que são as fontes vigentes; este documento não as substitui. Em resumo: 11.904 registros identificados; 29 duplicatas removidas (27 por DOI/URL e 2 relatórios iguais, manual); 11.875 triados; 9.393 excluídos na triagem; 2.482 na priorização histórica; 2.464 não avançaram; 18 na lista preliminar. O ID 6918 foi corrigido para 2014 e excluído do recorte 2015--2026. A transição entre o conjunto operacional anterior e a população adjudicada está em `docs/RECONCILIACAO-POPULACAO-ADJUDICADA-2026-09-03.md`.

---

## 1. Identidade do Projeto

| Campo | Valor |
|-------|-------|
| **Titulo** | Ensino Personalizado de Matemática: revisão sistemática de técnicas computacionais e especificação de um protótipo de apoio à interpretação docente |
| **Aluno** | Thales Ferreira Batista |
| **Orientador** | Prof. Dr. Rafael Zanin (IFC) |
| **Coorientador** | Prof. Dr. Manasses Ribeiro (IFC) |
| **Instituicao** | Instituto Federal Catarinense — Campus Videira |
| **Curso** | Ciencia da Computacao (Bacharelado) |

| Fase | Descricao | Periodo | Status |
|------|-----------|---------|--------|
| Fase 1 | Revisao sistematica e reconciliacao da população | Mar-Nov 2025; adjudicação em 03/09/2026 | Seleção original preservada; apreciação por critério conferida nas 14 fontes recuperadas |
| Fase 2 | Desenvolvimento do prototipo (TCC) | Sem prazo vigente | Aguardando decisão da orientação |
| Fase 3 | Validacao experimental (TCC) | Sem prazo vigente | Não iniciada |

**Revisao Sistematica vigente:** 11.904 registros identificados; 29 duplicatas removidas; 11.875 triados; 9.393 excluídos na triagem; 2.482 na priorização histórica; 2.464 não avançaram; **18 na lista preliminar**. Dessa lista, 1 foi excluído após o resumo e 17 foram procurados para texto integral; 2 não foram recuperados (Sokkhey 2020 e Zeng 2025); 15 foram avaliados em texto integral, 1 protocolo foi excluído e 14 relatórios empíricos foram recuperados. A seleção original sob o corte 4,0 mantém 15 estudos, dos quais 14 têm texto recuperado; Sokkhey permanece na seleção original sem apreciação MMAT, por falta de cópia verificável do texto completo. O 6918 foi corrigido para 2014 e excluído por estar fora do recorte. As etiquetas do pipeline têm categorias sobrepostas e descrevem o conteúdo bibliográfico, não qualidade metodológica.

---

## 2. Observacoes da Banca e estado de atendimento

| ID | Observacao | Severidade |
|----|-----------|------------|
| BANCA-001 | PRISMA 2020 e guideline de relato, nao protocolo | MEDIA |
| BANCA-002 | Tempo verbal deve ser passado | MEDIA |
| BANCA-003 | Falta fundamentacao sobre ensino de matematica | ALTA |
| BANCA-004 | Definir escopo tecnico do prototipo | ALTA |
| BANCA-005 | Termos estrangeiros em italico | MEDIA |
| BANCA-006 | Distinguir "ensino de matematica" de "educacao matematica" | ALTA |
| BANCA-007 | Publico-alvo e o professor, nao formuladores de politicas | MEDIA |
| BANCA-008 | Recorte temporal: 2015-2026 (12 anos) | MEDIA |
| BANCA-009 | Numeros do fluxo PRISMA consistentes em todo documento | ALTA |
| BANCA-010 | "Resultados Esperados" renomeado | BAIXA |
| BANCA-011 | Figuras/tabelas ABNT: caption + fonte | MEDIA |
| BANCA-012 | Tabela 2: colunas ajustadas | MEDIA |
| BANCA-013 | Tabela 3: soma > 100% explicada | BAIXA |
| BANCA-014 | Trecho "lacunas de revisoes anteriores" reformulado | MEDIA |
| BANCA-015 | Problema de pesquisa sem negrito | BAIXA |
| BANCA-016 | Referencias adicionadas: STI, adaptativa, avaliacao, metricas | MEDIA |
| BANCA-017 | Citacao Cochrane no trecho de APIs | BAIXA |
| BANCA-018 | Cap. Resultados renomeado para Revisao Sistematica | MEDIA |
| BANCA-019 | Procedimento MMAT definido; respostas conferidas pelo autor em 14 estudos com texto recuperado | ALTA |

---

## 3. Estado Atual

### Etapas concluidas

- Etapa 1: Correcoes PRISMA
- Etapa 2: procedimento MMAT definido; respostas MMAT de 14 estudos com texto recuperado conferidas pelo autor em 13/11/2026; componentes dos estudos mistos fora da conferência
- Etapa 2.5: Tempo verbal passado
- Etapa 3: Fundamentacao ensino de matematica
- Etapa 4: Capitulo do prototipo
- Etapa 4.5: Revisao geral (italicos, terminologia, ABNT, numeros, referencias)
- Etapa 5 parcial: Reestruturacao capitulos, pipeline MMAT historico, pretextuais, esqueletos

### Pendente (apos desenvolvimento do prototipo)

- [ ] Conteudo real do Cap. Resultados e Discussao
- [ ] Conteudo real do Cap. Conclusao
- [ ] Textos pessoais (dedicatoria, agradecimentos)
- [ ] Atualizar cronograma com datas reais
- [ ] Revisao final completa

---

## 4. Estrutura do TCC (65 paginas, compilado)

```text
results/tcc/
  main.tex                      -- Documento mestre
  config_inicial.tex            -- Pacotes e configuracoes
  referencias.bib               -- Bibliografia (~33 entradas)
  conteudo/
    introducao.tex              -- Cap 1: Introducao
    fundamentacao.tex           -- Cap 2: Fundamentacao Teorica
    metodologia.tex             -- Cap 3: Metodologia
    resultadosesperados.tex     -- Cap 4: Revisao Sistematica da Literatura
    prototipo.tex               -- Cap 5: Desenvolvimento do Prototipo
    resultados.tex              -- Cap 6: Resultados e Discussao (reconciliado; MMAT provisório)
    conclusao.tex               -- Cap 7: Conclusao (reconciliada; escopo final pendente)
    cronograma.tex              -- Cap 8: Cronograma
  pretextuais/
    capa.tex                    -- Dados do projeto
    resumo.tex                  -- Resumo + Abstract (escritos)
    acronimos.tex               -- Definicoes glossaries
    folhadeaprovacao.tex        -- Dados da banca
    dedicatoria.tex             -- Template
    agradecimentos.tex          -- Template
    epigrafe.tex                -- Template
  postextuais/
    apendice.tex                -- Checklist PRISMA 2020 (27/27)
  images/                       -- 6 PNGs da revisao sistematica
```

---

## 5. Pipeline MMAT (snapshot vigente e histórico)

O módulo MMAT possui um ledger por critério para os estudos da seleção original. A conferência documental abrangeu os 14 estudos com texto recuperado; Sokkhey permanece na seleção original sem apreciação MMAT, por falta de cópia verificável do texto completo. O ledger não produz escore agregado nem afirma certeza da evidência.

### Validar o snapshot vigente

```bash
cd c:/dev/ccw
python -m research.src.analysis.mmat_current_tcc_table --check
python -m pytest research/tests/test_mmat_current.py -q
```

O módulo `research.src.analysis.mmat_assessment` e os artefatos
`mmat_assessments.csv`, `mmat_assessment.csv` e `mmat_tcc_table.tex` preservam a
execução histórica de 17 estudos. Eles não devem ser usados para validar o
denominador vigente.

### Saídas vigentes

- `research/data/mmat_current_study_registry.csv` — registro dos 18 estudos atuais
- `research/data/mmat_primary_sources_manifest.csv` — fontes e estados de acesso
- `research/data/mmat_reassessment_current.csv` — respostas S1/S2 e Q1--Q5 por estudo
- `research/exports/references/mmat_current_tcc_table.tex` — tabela LaTeX vigente
- Banco SQLite operacional local (coluna `notes` com o histórico do MMAT); ele não é versionado nem necessário para verificar o snapshot publicado. O ledger vigente registra a conferência por critério das respostas para 14 estudos com texto recuperado; as evidências e os limites estão documentados nas fichas e nos localizadores

### Testes

```bash
python -m pytest research/tests/test_mmat_current.py -q
```

Os testes validam o ledger vigente, seus critérios e as respostas Y/N/CT. Isso não deve ser lido como escore de qualidade: as conclusões permanecem limitadas pelas fontes recuperadas e pelas evidências localizadas em cada ficha.

### Estado dos artefatos MMAT

| Snapshot | Estado | Uso permitido |
|-------|-----|---------|
| Histórico | 17 julgamentos por critério | somente auditoria e rastreabilidade histórica |
| Vigente | 15 estudos na seleção original; 14 com texto recuperado e conferência registrada | síntese por critério, sem escore global |

Não há média ou ranking de qualidade reportado para o conjunto vigente.

---

## 6. Regras para Agentes

### Terminologia

- **"ensino de matematica"** = processo didatico (USAR NA MAIORIA)
- **"educacao matematica"** = campo de pesquisa (APENAS ao referir-se a area)
- **PRISMA 2020** = guideline de relato. **Cochrane Handbook** = conducao. **MMAT** = qualidade
- Nunca dizer "protocolo PRISMA" ou "metodologia PRISMA"

### Formatacao

- **Tempo verbal:** passado. Excecao: definicoes atemporais e trabalhos futuros
- **Italico:** todo termo estrangeiro em `\textit{}`. Excecoes: nomes de ferramentas, siglas
- **Figuras/tabelas:** `\caption{}` ACIMA, `\fonte{}` ABAIXO (ABNT)
- **Publico-alvo:** professor. Nao mencionar formuladores de politicas
- **Periodo:** 2015-2026 (12 anos)

### Numeros-chave (remetem ao TCC e aos dados vigentes)

Fonte do relato: `results/tcc/main.pdf`, compilado de `results/tcc/main.tex`. Fonte vigente das contagens: `research/data/`. Este documento não é fonte autônoma: em caso de divergência, prevalecem o TCC e os dados versionados.

Consultas: 72 (48 EN + 24 PT) | Bases: 4 | Período: 2015-2026

### Compilacao

```bash
cd c:/dev/ccw/results/tcc
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Verificar: zero `^!` no log, zero `undefined`.

### Ao Receber Feedback da Banca

1. Registrar na secao 2 com ID [BANCA-NNN]
2. Classificar severidade e arquivos impactados
3. Implementar, compilar, marcar como concluida

---

## 7. Referencias Metodologicas

| Referencia | Funcao | Key BibTeX |
|-----------|--------|------------|
| PRISMA 2020 (Page et al., BMJ 2021) | Guideline de relato | `PRISMA2020` |
| PRISMA-P 2015 (Moher et al., 2015) | Guideline para protocolos | `PRISMAP2015` |
| Cochrane Handbook v6.5 (2024) | Referência complementar para a pergunta e a elegibilidade | `CochraneHandbook` |
| MMAT 2018 (Hong et al.) | Avaliacao de qualidade | `MMAT2018` |
| BNCC (Brasil, 2018) | Curriculo nacional | `BNCC2018` |
| PISA 2022 (OECD, 2023) | Dados internacionais | `PISA2022` |
| SAEB 2021 (Inep, 2024) | Documentação contextual dos resultados | `SAEB2021` |

---

## 8. Uso de IA

O uso de ferramentas de IA generativa para redação e revisão textual, desenvolvimento e revisão do código, apoio à triagem e à apreciação MMAT está descrito na Metodologia e no Apêndice de ferramentas do TCC (`results/tcc/postextuais/ferramentas-ia.tex`). A responsabilidade pela conferência das fontes, do texto e do código e pelas análises permanece com o autor.
