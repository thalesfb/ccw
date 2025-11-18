# 📚 Documentação do Projeto - Guia de Uso

**Atualizado**: 16/11/2025  
**Dataset Canônico**: 6.516 identificados / 16 incluídos  
**Status**: Pronto para conversão LaTeX (PTC/TCC)

---

## 📋 Arquivos Principais (Usar no PTC)

### Documentação Acadêmica Canônica

| Arquivo | Finalidade | Uso no PTC | Status |
|---------|-----------|-----------|--------|
| **RESUMO.md** | Resumo PT/EN + métricas | Resumo/Abstract | ✅ Canônico |
| **INTRODUCAO.md** | Contexto, problema, objetivos | Capítulo 1: Introdução | ✅ Canônico |
| **FUNDAMENTACAO_TEORICA.md** | IA, ML, educação matemática | Capítulo 2: Fundamentação | ✅ Canônico |
| **METODOLOGIA.md** | Protocolo PRISMA, 108 queries | Capítulo 3: Metodologia | ✅ Canônico |
| **RESULTADOS_PRELIMINARES.md** | PRISMA flow, distribuições, **Tabela 1: síntese completa dos 16 estudos incluídos** | Capítulo 4: Resultados | ✅ Canônico |
| **GAPS_E_OPORTUNIDADES.md** | Análise qualitativa de gaps | Capítulo 5: Discussão | ✅ Canônico |
| **CONCLUSOES.md** | Síntese e contribuições | Capítulo 6: Conclusões | ✅ Canônico |
| **GLOSSARIO.md** | Terminologia técnica | Apêndice A: Glossário | ✅ Canônico |

### Documentação de Suporte

| Arquivo | Finalidade | Observações |
|---------|-----------|-------------|
| **CRONOGRAMA.md** | Planejamento temporal | Referência para cronograma do TCC |
| **ANALISE_ARQUIVOS.md** | Explica estrutura de exports | Reprodutibilidade e auditoria |

---

## 🗂️ Estrutura de Diretórios

```
research/docs/
├── 📄 RESUMO.md                       ✅ Resumo PT/EN (canônico 6.516/16)
├── 📄 INTRODUCAO.md                   ✅ Introdução (canônico)
├── 📄 FUNDAMENTACAO_TEORICA.md        ✅ Teoria (estático)
├── 📄 METODOLOGIA.md                  ✅ Metodologia PRISMA (canônico)
├── 📄 RESULTADOS_PRELIMINARES.md      ✅ Resultados (canônico)
├── 📄 GAPS_E_OPORTUNIDADES.md         ✅ Análise de gaps (nota histórica)
├── 📄 CONCLUSOES.md                   ✅ Conclusões Fase 1 (canônico)
├── 📄 GLOSSARIO.md                    ✅ Terminologia (estático)
├── 📄 CRONOGRAMA.md                   ✅ Planejamento (canônico)
├── 📄 ANALISE_ARQUIVOS.md             ✅ Sobre exports (referência)
├── 📄 ANALISE_ESTRUTURA_DOCS.md       ✅ Este relatório de análise
├── 📄 README_DOCS.md                  📌 Este guia
│
├── 📁 archive/                        🗃️ Documentação histórica
│   ├── METODOLOGIA_OLD.md             (dataset não especificado)
│   ├── METODOLOGIA_UPDATED_original.md (9.090 / 20)
│   ├── RESUMO_OLD_original.md         (12.533 / 43)
│   ├── RESULTADOS_PRELIMINARES_OLD_original.md (12.533 / 43)
│   ├── REFACTORING_EXPORTS.md         (histórico técnico 05/10)
│   └── RELATORIO_ATUALIZACAO_DOCS.md  (auditoria 14/11)
│
└── (sem diretório deep_analysis/ em docs)
```

---

## 📊 Valores Canônicos (Dataset Atual)

### Métricas PRISMA 2020

```
┌─────────────────────────────────────────┐
│   IDENTIFICAÇÃO: 6.548 registros       │
│   ├─ Crossref: ~43,8%                   │
│   ├─ OpenAlex: ~27,0%                   │
│   ├─ Semantic Scholar: ~27,3%          │
│   └─ CORE: ~2,0%                        │
│                                         │
│   Período: 2017-2026 (10 anos)         │
│   Queries: 108 bilíngues (72 EN + 36 PT)│
└─────────────────────────────────────────┘
           ↓ (Remoção de duplicatas)
┌─────────────────────────────────────────┐
│   DUPLICATAS REMOVIDAS: 32              │
└─────────────────────────────────────────┘
           ↓ (Registros únicos)
┌─────────────────────────────────────────┐
│   TRIAGEM (título/resumo): 6.516        │
│   Excluídos na triagem: 1.851 (28,4%)   │
└─────────────────────────────────────────┘
           ↓ (Score ≥4.0)
┌─────────────────────────────────────────┐
│   ELEGIBILIDADE: 1.835 registros        │
│   Excluídos na elegibilidade: 1.819 (99,1%)│
└─────────────────────────────────────────┘
           ↓ (Critérios finais)
┌─────────────────────────────────────────┐
│   INCLUÍDOS: 16 estudos                 │
│   Taxa de inclusão: ~0,25%              │
│   Score médio: 4.2 (range: 4.0-4.5)    │
└─────────────────────────────────────────┘
```

### Estratégia de Busca (3 Camadas)

```
Camada 1: Base (Matemática)
├─ EN: mathematics, math, mathematical
└─ PT: matemática, mat, matemático

Camada 2: Tecnológica (IA)
├─ EN: AI, ML, DL, NN, NLP, EDM (6 termos)
└─ PT: IA, aprendizado de máquina, rede neural, etc. (6 termos)

Camada 3: Educacional
├─ EN: education, learning, teaching, instruction, pedagogy, curriculum (6)
└─ PT: educação, aprendizagem (2)

TOTAL: 3×6×6 (EN) + 3×6×2 (PT) = 72 + 36 = 108 queries
```

---

## 🎯 Mapeamento para Estrutura PTC/TCC

Manter simples (KISS): usar diretamente os `.tex` em `results/ptc/conteudo/` e preencher a partir dos `.md` canônicos conforme necessário. Sem automatizações de conversão neste momento.

---

## ✅ Checklist de Preparação Completa

### ✅ Fase 1: Limpeza (CONCLUÍDA)

- [x] Mover arquivos `*_OLD.md` para `archive/`
- [x] Mover arquivos `*_UPDATED.md` para `archive/`
- [x] Mover meta-documentação técnica para `archive/`
- [x] Atualizar `CONCLUSOES.md` com valores canônicos
- [x] Atualizar `CRONOGRAMA.md` com valores canônicos

### 🔄 Fase 2: Validação (PENDENTE)

- [ ] Buscar globalmente por valores antigos (`12.533`, `43`, `9.090`, `20`)
- [ ] Verificar narrativas referem-se a 16 estudos (não 43 ou 20)
- [ ] Confirmar database filename é `systematic_review.sqlite` (não `.db`)
- [ ] Validar todos os percentuais derivados (28,4%, 99,1%, ~0,25%)

### 📝 Fase 3: Preparação LaTeX (REMOVIDA - KISS)

Sem automações neste momento. Usar diretamente `results/ptc/`.

### 📚 Fase 4: Referências BibTeX (PENDENTE)

- [ ] Gerar BibTeX atualizado: `python -m research.src.cli export-bibtex --included-only`
- [ ] Copiar para `results/ptc/referencias.bib`
- [ ] Combinar com referências metodológicas manuais (`research/references/references.bib`)
- [ ] Validar formato BibTeX (chaves únicas, campos obrigatórios)

---

## 🚀 Comandos Úteis

### Verificação de Consistência

```bash
# Buscar valores antigos (exploratório: 12.533 / 43)
cd research/docs
grep -rn "12.533\|12533" *.md --color=auto
grep -rn " 43 " *.md | grep -v "2023\|2024\|2025" --color=auto

# Buscar valores antigos (intermediário: 9.090 / 20)
grep -rn "9.090\|9090" *.md --color=auto
grep -rn " 20 " *.md | grep -v "2020\|2023\|2024" --color=auto

# Confirmar valores canônicos presentes
grep -rn "6.516\|6516" *.md --color=auto
grep -rn " 16 " *.md --color=auto
```

### Estatísticas do Dataset

```bash
# Verificar métricas atuais
python -m research.src.cli stats

# Exportar papers incluídos
python -m research.src.cli export --format csv --stage included -o ../exports/analysis/

# Gerar BibTeX
python -m research.src.cli export-bibtex --included-only -o ../exports/references/
```

### Validação de Integridade

```bash
# Verificar integridade do banco SQLite
sqlite3 research/systematic_review.sqlite "PRAGMA integrity_check;"

# Contar registros por estágio
sqlite3 research/systematic_review.sqlite "SELECT selection_stage, COUNT(*) FROM papers GROUP BY selection_stage;"

# Verificar scores dos incluídos
sqlite3 research/systematic_review.sqlite "SELECT MIN(relevance_score), MAX(relevance_score), AVG(relevance_score) FROM papers WHERE selection_stage='included';"
```

---

## 📖 Referências Internas

### Banco de Dados e Pipeline

- **Banco canônico**: `research/systematic_review.sqlite`
- **Pipeline**: `research/src/pipeline/`
- **CLI**: `research/src/cli.py`

### Exports e Análises

- **Exports gerais**: `research/exports/`
- **BibTeX**: `research/exports/references/`

### Templates e Estrutura TCC

- **Template PTC**: `results/ptc/`
- **Template TCC**: `results/tcc/`
- **Referências manuais**: `research/references/references.bib`

---

## 📝 Notas Importantes

### Datasets Históricos (Arquivados)

| Dataset | Identificados | Incluídos | Queries | Status | Localização |
|---------|---------------|-----------|---------|--------|-------------|
| **Exploratório** | 12.533 | 43 | 132 | ❌ Obsoleto | `archive/*_OLD_original.md` |
| **Intermediário** | 9.090 | 20 | 108 | ❌ Obsoleto | `archive/METODOLOGIA_UPDATED_original.md` |
| **CANÔNICO** | 6.516 | 16 | 108 | ✅ Atual | Todos os `*.md` principais |

> ⚠️ **Importante**: Apenas o dataset CANÔNICO (6.516 / 16) deve ser usado no PTC/TCC. Datasets históricos permanecem em `archive/` para transparência e auditoria.

### Transparência Histórica

Os documentos canônicos contêm notas de transparência explícitas sobre a transição de datasets:

- **RESUMO.md**: Linha 35 (nota sobre histórico)
- **RESULTADOS_PRELIMINARES.md**: Linha 3 (nota sobre snapshot canônico)
- **GAPS_E_OPORTUNIDADES.md**: Linha 3 (nota sobre conjunto exploratório)

Essas notas asseguram rastreabilidade e rigor acadêmico, seguindo boas práticas de reproducibilidade científica.

---

## 🎓 Citação Recomendada (Metadados)

```
Título: Aplicações de Inteligência Artificial na Educação Matemática: 
        Uma Revisão Sistemática

Dataset: 6.516 registros identificados / 16 incluídos
Período: 2017-2026 (10 anos)
Bases: Crossref, OpenAlex, Semantic Scholar, CORE
Metodologia: PRISMA 2020
Queries: 108 bilíngues (EN/PT)
Scoring: Relevância ≥4.0 (escala 0-10)
Taxa inclusão: ~0,25%

Repositório: c:\dev\ccw\research\
Banco: research/systematic_review.sqlite
Pipeline: research/src/pipeline/ (Python 3.11+)
```

---

**Última Atualização**: 16/11/2025  
**Status**: Documentação limpa e pronta para conversão LaTeX  
**Próxima Etapa**: Preparar estrutura `ptc_source/` e converter para LaTeX
