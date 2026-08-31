# PESQUISA.md — Contexto e Workflow de Pesquisa Cientifica

> Documento vivo para agentes e pesquisador. Funciona como CLAUDE.md do projeto,
> rastreador de melhorias baseado em feedback da banca, e guia de workflow.
>
> **Ultima atualizacao:** 2026-08-31

> **Baseline vigente (31/08/2026):** a base consolidada contém 11.904 registros. Destes, 9.413 foram excluídos na triagem, 2.491 avançaram à elegibilidade, 2.475 foram excluídos nessa etapa e 16 estudos permanecem incluídos. A reexecução partiu de 23 candidatos, removeu 7 falsos positivos e alterou a composição do conjunto; os números atuais não são uma simples substituição de 17 por 16. A reconciliação completa está em `docs/RECONCILIACAO-BASELINE-2026-08-31.md`.

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

**Revisao Sistematica vigente:** 11.904 registros no snapshot; 9.413 excluídos na triagem; 2.491 avaliados na elegibilidade; 2.475 excluídos nessa etapa; **16 incluídos**. Entre os estudos atuais, as etiquetas do pipeline registram Machine Learning em 11/16 (68,8%) e Predictive Analytics em 9/16 (56,3%), com categorias sobrepostas; essas etiquetas descrevem o conteúdo bibliográfico e não qualidade metodológica.

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
| BANCA-019 | Procedimento MMAT definido; reaplicacao aos 16 estudos atuais ainda pendente | ALTA |

---

## 3. Estado Atual

### Etapas concluidas

- Etapa 1: Correcoes PRISMA
- Etapa 2: procedimento MMAT definido; reaplicacao aos 16 estudos atuais pendente
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

## 5. Pipeline MMAT (snapshot historico)

O modulo MMAT e standalone e o arquivo atualmente versionado contém julgamentos do conjunto histórico de 17 estudos. Ele não representa a avaliação final do snapshot vigente de 16 estudos. A reaplicação por critério aos 16 estudos atuais deve ocorrer antes de qualquer síntese de qualidade metodológica ou afirmação de certeza da evidência.

### Executar

```bash
cd c:/dev/ccw
python -m research.src.analysis.mmat_assessment
```

### Saidas

- `research/exports/analysis/mmat_assessment.csv` — tabela CSV
- `research/exports/references/mmat_table.tex` — tabela LaTeX
- SQLite histórico atualizado (coluna `notes` com JSON do MMAT); a base canônica atual permanece sem julgamentos MMAT finais para os seis estudos novos

### Testes

```bash
python -m pytest research/tests/test_mmat.py -v
```

Os testes validam o artefato histórico de 17 estudos, os cinco critérios por estudo e as respostas Y/N/CT. Isso não deve ser lido como confirmação de que os 16 estudos atuais já foram avaliados.

### Estado dos artefatos MMAT

| Snapshot | Estado | Uso permitido |
|-------|-----|---------|
| Histórico | 17 julgamentos por critério | somente auditoria e rastreabilidade histórica |
| Vigente | 16 estudos incluídos; reaplicação pendente | não emitir síntese MMAT final |

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

### Numeros-chave (fonte unica de verdade)

Total: 11.904 | Excluidos na triagem: 9.413 | Avancaram a elegibilidade: 2.491 | Excluidos na elegibilidade: 2.475 | Incluidos: 16 | Taxa: ~0,13% | Consultas: 72 (48 EN + 24 PT) | Bases: 4 | Periodo: 2015-2026

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
