# PESQUISA.md — Contexto e Workflow de Pesquisa Cientifica

> Documento vivo para agentes e pesquisador. Funciona como CLAUDE.md do projeto,
> rastreador de melhorias baseado em feedback da banca, e guia de workflow.
>
> **Ultima atualizacao:** 2026-03-28

---

## 1. Identidade do Projeto

| Campo | Valor |
|-------|-------|
| **Titulo** | Ensino Personalizado de Matematica: Oportunidades e Tecnicas Computacionais |
| **Aluno** | Thales Ferreira Batista |
| **Orientador** | Prof. Dr. Rafael Zanin (IFC) |
| **Coorientador** | Prof. Dr. Manasses Ribeiro (IFC) |
| **Instituicao** | Instituto Federal Catarinense — Campus Videira |
| **Curso** | Ciencia da Computacao (Bacharelado) |

| Fase | Descricao | Periodo | Status |
|------|-----------|---------|--------|
| Fase 1 | Revisao Sistematica da Literatura (PTC) | Mar-Nov 2025 | Concluida |
| Fase 2 | Desenvolvimento do Prototipo (TCC) | Fev-Jun 2026 | Em andamento |
| Fase 3 | Validacao Experimental (TCC) | Jul-Nov 2026 | Planejada |

**Revisao Sistematica:** 9.431 identificados, 6.914 unicos, **17 incluidos** (score >= 4.0). ML supervisionado 76.5%, predicao 52.9%.

---

## 2. Observacoes da Banca (todas CONCLUIDAS)

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
| BANCA-019 | MMAT integrado ao pipeline com dados reais | ALTA |

---

## 3. Estado Atual

### Etapas concluidas

- Etapa 1: Correcoes PRISMA
- Etapa 2: MMAT + Limitacoes
- Etapa 2.5: Tempo verbal passado
- Etapa 3: Fundamentacao ensino de matematica
- Etapa 4: Capitulo do prototipo
- Etapa 4.5: Revisao geral (italicos, terminologia, ABNT, numeros, referencias)
- Etapa 5 parcial: Reestruturacao capitulos, MMAT pipeline, pretextuais, esqueletos

### Pendente (apos desenvolvimento do prototipo)

- [ ] Conteudo real do Cap. Resultados e Discussao
- [ ] Conteudo real do Cap. Conclusao
- [ ] Textos pessoais (dedicatoria, agradecimentos)
- [ ] Atualizar cronograma com datas reais
- [ ] Revisao final completa

---

## 4. Estrutura do TCC (74 paginas, compilado)

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
    resultados.tex              -- Cap 6: Resultados e Discussao (esqueleto)
    conclusao.tex               -- Cap 7: Conclusao (esqueleto)
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

## 5. Pipeline MMAT

O modulo MMAT e standalone, nao integrado ao pipeline principal de revisao.

### Executar

```bash
cd c:/dev/ccw
python -m research.src.analysis.mmat_assessment
```

### Saidas

- `research/exports/analysis/mmat_assessment.csv` — tabela CSV
- `research/exports/references/mmat_table.tex` — tabela LaTeX
- SQLite atualizado (coluna `notes` com JSON do MMAT)

### Testes

```bash
python -m pytest research/tests/test_mmat.py -v
```

22 testes, todos passando. Valida: 17 estudos, scores 1-5, 5 criterios por estudo, Y/N/CT validos.

### Resultados MMAT

| Score | Qtd | Estudos |
|-------|-----|---------|
| 5/5 | 3 | Pejic 2021, Depren 2017, MacLellan 2017 |
| 4/5 | 3 | Appiah-Odame 2024, Mertasari 2023, Hasib 2022 |
| 3/5 | 6 | Tjahyadi 2025, Nyantah 2025, Milicevic 2024, Zhang 2023, Sokkhey 2020, Uskov 2019 |
| 2/5 | 3 | Zhang et al. 2025, Jose et al. 2024, Kumar 2022 |
| 1/5 | 2 | Salas-Rueda 2021, Unal 2020 |

Media: 3.12/5

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

### Numeros-chave (fonte unica de verdade)

Total: 9.431 | Duplicatas: 2.517 (26,6%) | Unicos: 6.914 | Elegiveis: 1.883 | Excluidos: 1.866 | Incluidos: 17 | Taxa: ~0,18% | Consultas: 72 (48 EN + 24 PT) | Bases: 4 | Periodo: 2015-2026

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
| Cochrane Handbook v6.4 (2023) | Conducao da revisao | `CochraneHandbook` |
| MMAT 2018 (Hong et al.) | Avaliacao de qualidade | `MMAT2018` |
| BNCC (Brasil, 2018) | Curriculo nacional | `BNCC2018` |
| PISA 2022 (OECD, 2023) | Dados internacionais | `PISA2022` |
| SAEB 2021 (INEP, 2022) | Dados nacionais | `SAEB2021` |
