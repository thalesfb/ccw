# 📋 Análise de Estrutura da Documentação - Preparação para PTC

**Data**: 16/11/2025  
**Objetivo**: Identificar arquivos depreciados/duplicados e organizar documentação para preenchimento do PTC

---

## 🔍 Situação Atual

### Estrutura de Diretórios

```
research/docs/
├── METODOLOGIA.md              ✅ CANÔNICO (6.516 / 16 estudos)
├── RESUMO.md                   ✅ CANÔNICO (6.516 / 16 estudos)
├── RESULTADOS_PRELIMINARES.md  ✅ CANÔNICO (6.516 / 16 estudos)
├── GAPS_E_OPORTUNIDADES.md     ✅ ATUALIZADO (nota histórica)
├── FUNDAMENTACAO_TEORICA.md    ✅ ESTÁTICO (teoria de base)
├── INTRODUCAO.md               ✅ ATUALIZADO (20 → 16 estudos)
├── CONCLUSOES.md               ⚠️  VERIFICAR (pode ter refs antigas)
├── GLOSSARIO.md                ✅ ESTÁTICO (terminologia)
├── CRONOGRAMA.md               ⚠️  VERIFICAR (refs antigas)
│
├── METODOLOGIA_OLD.md          ❌ DEPRECIADO (dataset intermediário 9.090 / 20)
├── METODOLOGIA_UPDATED.md      ❌ DEPRECIADO (duplicata intermediária)
├── RESUMO_OLD.md               ❌ DEPRECIADO (dataset exploratório 12.533 / 43)
├── RESULTADOS_PRELIMINARES_OLD.md ❌ DEPRECIADO (dataset exploratório)
│
├── ANALISE_ARQUIVOS.md         ⚠️  META-DOC (sobre exports, manter para referência)
├── REFACTORING_EXPORTS.md      ⚠️  META-DOC (sobre refatoração, manter para referência)
├── RELATORIO_ATUALIZACAO_DOCS.md ⚠️ META-DOC (sobre atualização 14/11, manter para referência)
│
├── archive/                    ✅ CRIADO para histórico
   ├── METODOLOGIA_UPDATED.md  (stub criado)
   ├── RESUMO_OLD.md           (stub criado)
   └── RESULTADOS_PRELIMINARES_OLD.md (stub criado)
```

---

## 📊 Análise de Arquivos

### ✅ Arquivos CANÔNICOS (Usar no PTC)

Estes são os documentos finais com métricas canônicas (6.516 identificados / 16 incluídos):

| Arquivo | Status | Conteúdo | Uso no PTC |
|---------|--------|----------|-----------|
| **METODOLOGIA.md** | ✅ Atualizado | Protocolo PRISMA, 108 queries, deduplicação | **Capítulo 3: Metodologia** |
| **RESUMO.md** | ✅ Atualizado | Resumo PT/EN, métricas canônicas | **Resumo/Abstract** |
| **RESULTADOS_PRELIMINARES.md** | ✅ Atualizado | PRISMA flow, distribuição, análise | **Capítulo 4: Resultados** |
| **FUNDAMENTACAO_TEORICA.md** | ✅ Estático | IA, ML, educação matemática | **Capítulo 2: Fundamentação** |
| **INTRODUCAO.md** | ✅ Atualizado | Contextualização, problema, justificativa | **Capítulo 1: Introdução** |
| **GAPS_E_OPORTUNIDADES.md** | ✅ Atualizado | Análise qualitativa (nota histórica) | **Capítulo 4.3: Discussão** |
| **GLOSSARIO.md** | ✅ Estático | Terminologia técnica | **Apêndice A: Glossário** |

### ❌ Arquivos DEPRECIADOS (Mover para archive/)

Estes arquivos contêm datasets históricos desatualizados:

| Arquivo | Problema | Dataset | Ação Recomendada |
|---------|----------|---------|------------------|
| **METODOLOGIA_OLD.md** | Metodologia antiga | Não especificado | **MOVER para archive/** |
| **METODOLOGIA_UPDATED.md** | Intermediário | 9.090 / 20 estudos | **MOVER para archive/** |
| **RESUMO_OLD.md** | Exploratório | 12.533 / 43 estudos | **MOVER para archive/** |
| **RESULTADOS_PRELIMINARES_OLD.md** | Exploratório | 12.533 / 43 estudos | **MOVER para archive/** |

**Observação**: Stubs já foram criados em `archive/`, mas os arquivos originais ainda estão em `docs/`.

### ⚠️ Arquivos META-DOCUMENTAÇÃO (Avaliar Necessidade)

Documentos sobre o processo de desenvolvimento (não são conteúdo acadêmico):

| Arquivo | Propósito | Decisão Recomendada |
|---------|-----------|---------------------|
| **ANALISE_ARQUIVOS.md** | Explica estrutura de exports | **MANTER** (útil para reprodutibilidade) |
| **REFACTORING_EXPORTS.md** | Histórico de refatoração (05/10/2025) | **MOVER para archive/** (histórico técnico) |
| **RELATORIO_ATUALIZACAO_DOCS.md** | Auditoria de atualização (14/11/2024) | **MOVER para archive/** (auditoria interna) |
| **CRONOGRAMA.md** | Cronograma do projeto | **VERIFICAR e ATUALIZAR** (pode ter refs antigas) |
| **CONCLUSOES.md** | Conclusões da Fase 1 | **VERIFICAR e ATUALIZAR** (pode ter refs antigas) |

### ✅ Diretório deep_analysis/

Removido do `docs/` (obsoleto). Caso necessário, gere análises profundas via CLI para `research/exports/`.

---

## 🎯 Mapeamento para Estrutura do PTC

### Estrutura Típica de PTC/TCC

```
results/ptc/conteudo/
├── 01-introducao.tex          ← INTRODUCAO.md
├── 02-fundamentacao.tex       ← FUNDAMENTACAO_TEORICA.md + refs
├── 03-metodologia.tex         ← METODOLOGIA.md
├── 04-resultados.tex          ← RESULTADOS_PRELIMINARES.md
├── 05-discussao.tex           ← GAPS_E_OPORTUNIDADES.md
└── 06-conclusoes.tex          ← CONCLUSOES.md (após verificação)

results/ptc/postextuais/
└── apendices.tex
    ├── Apêndice A: Glossário  ← GLOSSARIO.md
    ├── Apêndice B: Queries    ← METODOLOGIA.md (seção específica)
    └── Apêndice C: Protocolo  ← METODOLOGIA.md (critérios PRISMA)

results/ptc/pretextuais/
├── resumo.tex                 ← RESUMO.md (seção PT)
└── abstract.tex               ← RESUMO.md (seção EN)

results/ptc/referencias.bib    ← research/exports/references/included_papers.bib
```

---

## 📝 Checklist de Preparação para PTC

### Fase 1: Limpeza de Arquivos Depreciados

- [ ] **Mover para archive/:**
  - [ ] `METODOLOGIA_OLD.md`
  - [ ] `METODOLOGIA_UPDATED.md`
  - [ ] `RESUMO_OLD.md`
  - [ ] `RESULTADOS_PRELIMINARES_OLD.md`
  - [ ] `REFACTORING_EXPORTS.md` (histórico técnico)
  - [ ] `RELATORIO_ATUALIZACAO_DOCS.md` (auditoria interna)

- [ ] **Atualizar `.gitignore`:**
  ```gitignore
  # Arquivos depreciados (apenas archive/)
  research/docs/*_OLD.md
  research/docs/*_UPDATED.md
  ```

### Fase 2: Verificação de Consistência

- [ ] **CRONOGRAMA.md**: Verificar se contém referências a datasets antigos (12.533 / 43 ou 9.090 / 20)
- [ ] **CONCLUSOES.md**: Verificar se métricas estão alinhadas com canônico (6.516 / 16)
- [ ] **INTRODUCAO.md**: Confirmar atualização de "20 estudos" → "16 estudos" (já feito?)
- [ ] **Todos os arquivos**: Buscar por `12.533`, `43`, `9.090`, `20` (valores antigos)

**Comando de busca global:**
```bash
cd research/docs
grep -rn "12.533\|9.090" --include="*.md" --exclude-dir=archive
grep -rn " 43 \| 20 " --include="*.md" --exclude-dir=archive | grep -v "2023\|2024\|2025"
```

### Fase 3 e 4: Conversão LaTeX (REMOVIDAS - KISS)

Sem automação de conversão. Usar diretamente `results/ptc/`.

### Fase 5: Integração de Referências BibTeX

- [ ] **Gerar BibTeX atualizado:**
  ```bash
  python -m research.src.cli export-bibtex --included-only \
    -o research/exports/references
  ```

- [ ] **Copiar para PTC:**
  ```bash
  cp research/exports/references/included_papers.bib \
     results/ptc/referencias.bib
  ```

- [ ] **Adicionar referências metodológicas:**
  ```bash
  # Combinar com referências manuais (PRISMA, BNCC, etc.)
  cat research/references/references.bib >> results/ptc/referencias.bib
  ```

---

## 🚨 Valores Canônicos para Verificação

### Dataset CANÔNICO Atual (Pipeline Consolidado)

```
Identificação (pré-dedup):    6.548
Duplicatas removidas:            32
Triagem (únicos):             6.516
Excluídos na triagem:        1.851 (28,4%)
Elegibilidade (texto completo): 1.835
Excluídos na elegibilidade:  1.819 (99,1%)
Incluídos:                      16

Período:                      2017-2026
Queries:                      108 bilíngues (72 EN + 36 PT)
Bases de dados:               4 (Crossref, OpenAlex, Semantic Scholar, CORE)
```

### Datasets HISTÓRICOS (Apenas para Referência)

| Dataset | Identificados | Incluídos | Queries | Status |
|---------|---------------|-----------|---------|--------|
| **Exploratório** | 12.533 | 43 | 132 | ❌ OBSOLETO |
| **Intermediário** | 9.090 | 20 | 108 | ❌ OBSOLETO |
| **CANÔNICO** | 6.516 | 16 | 108 | ✅ ATUAL |

---

## 📚 Arquivos de Referência para o PTC

### Documentos Acadêmicos (Conteúdo Principal)

```
✅ USAR DIRETAMENTE:
├── INTRODUCAO.md               → Capítulo 1
├── FUNDAMENTACAO_TEORICA.md    → Capítulo 2
├── METODOLOGIA.md              → Capítulo 3
├── RESULTADOS_PRELIMINARES.md  → Capítulo 4.1
├── deep_analysis/DEEP_ANALYSIS_REPORT.md → Capítulo 4.2
├── GAPS_E_OPORTUNIDADES.md     → Capítulo 5 (Discussão)
├── CONCLUSOES.md               → Capítulo 6 (após verificação)
├── RESUMO.md                   → Resumo/Abstract
└── GLOSSARIO.md                → Apêndice A
```

### Documentos Técnicos (Reprodutibilidade)

```
⚠️ MANTER COMO REFERÊNCIA (não incluir no PTC):
├── ANALISE_ARQUIVOS.md         → Documenta estrutura de exports
└── CRONOGRAMA.md               → Planejamento temporal (após verificação)
```

### Documentos de Auditoria (Mover para archive/)

```
❌ ARQUIVAR (histórico técnico, não acadêmico):
├── REFACTORING_EXPORTS.md
├── RELATORIO_ATUALIZACAO_DOCS.md
├── METODOLOGIA_OLD.md
├── METODOLOGIA_UPDATED.md
├── RESUMO_OLD.md
└── RESULTADOS_PRELIMINARES_OLD.md
```

---

## 🔧 Comandos de Execução

### 1. Mover Arquivos Depreciados

```bash
# Criar backup completo antes
cd c:/dev/ccw/research/docs

# Mover arquivos OLD/UPDATED
mv METODOLOGIA_OLD.md archive/
mv RESUMO_OLD.md archive/
mv RESULTADOS_PRELIMINARES_OLD.md archive/

# Mover meta-documentação técnica
mv REFACTORING_EXPORTS.md archive/
mv RELATORIO_ATUALIZACAO_DOCS.md archive/

# Nota: METODOLOGIA_UPDATED.md já tem stub em archive/, mover original
mv METODOLOGIA_UPDATED.md archive/METODOLOGIA_UPDATED_original.md
```

### 2. Verificar Consistência de Valores

```bash
# Buscar valores antigos (exploratório: 12.533 / 43)
grep -rn "12.533\|12533" *.md --color=auto
grep -rn " 43 " *.md | grep -v "2023\|2024\|2025" --color=auto

# Buscar valores antigos (intermediário: 9.090 / 20)
grep -rn "9.090\|9090" *.md --color=auto
grep -rn " 20 " *.md | grep -v "2020\|2023\|2024" --color=auto

# Valores canônicos esperados
grep -rn "6.516\|6516" *.md --color=auto  # Deve aparecer
grep -rn " 16 " *.md --color=auto          # Deve aparecer (incluídos)
```

### 3. Gerar Estrutura PTC

```bash
# Criar diretório de preparação
mkdir -p research/docs/ptc_source
mkdir -p research/docs/ptc_source/apendices

# Copiar arquivos canônicos com nomenclatura sequencial
cp INTRODUCAO.md ptc_source/01-introducao.md
cp FUNDAMENTACAO_TEORICA.md ptc_source/02-fundamentacao.md
cp METODOLOGIA.md ptc_source/03-metodologia.md
cp RESULTADOS_PRELIMINARES.md ptc_source/04-resultados.md
cp GAPS_E_OPORTUNIDADES.md ptc_source/05-discussao.md
cp CONCLUSOES.md ptc_source/06-conclusoes.md
cp RESUMO.md ptc_source/00-resumo.md
cp GLOSSARIO.md ptc_source/apendices/apendice-a-glossario.md
```

### 4. Conversão Markdown → LaTeX (Exemplo)

```bash
cd research/docs/ptc_source

# Converter cada capítulo (ajustar caminhos conforme necessário)
for file in *.md; do
  basename="${file%.md}"
  pandoc "$file" \
    -o "../../../results/ptc/conteudo/${basename}.tex" \
    --from=markdown \
    --to=latex \
    --standalone=false \
    --wrap=preserve
done
```

---

## 🎯 Próximos Passos Imediatos

### Prioridade ALTA

1. **Mover arquivos depreciados para archive/**
   - `METODOLOGIA_OLD.md`
   - `METODOLOGIA_UPDATED.md` (substituir stub)
   - `RESUMO_OLD.md` (substituir stub)
   - `RESULTADOS_PRELIMINARES_OLD.md` (substituir stub)

2. **Verificar CONCLUSOES.md e CRONOGRAMA.md**
   - Buscar por valores antigos (12.533, 43, 9.090, 20)
   - Atualizar para canônico (6.516, 16) se necessário

3. **Busca global de valores antigos**
   - Executar comandos grep acima
   - Corrigir ocorrências encontradas

### Prioridade MÉDIA

4. **Criar estrutura ptc_source/**
   - Copiar arquivos canônicos renomeados
   - Preparar para conversão LaTeX

5. **Gerar BibTeX atualizado**
   - `python -m research.src.cli export-bibtex --included-only`
   - Copiar para `results/ptc/referencias.bib`

### Prioridade BAIXA

6. **Conversão Markdown → LaTeX**
   - Instalar Pandoc se necessário
   - Converter arquivos preparados
   - Ajustes manuais (emojis, tabelas, citações)

---

## ✅ Critérios de Sucesso

### Documentação Limpa

- [ ] Nenhum arquivo `*_OLD.md` ou `*_UPDATED.md` em `research/docs/`
- [ ] Todos os depreciados movidos para `archive/`
- [ ] Meta-documentação técnica arquivada

### Consistência de Valores

- [ ] Nenhuma ocorrência de `12.533` ou `43` (exceto em `archive/` e notas históricas explícitas)
- [ ] Nenhuma ocorrência de `9.090` ou `20` (exceto em `archive/`)
- [ ] Valores canônicos `6.516` e `16` presentes em todos os documentos principais

### Estrutura Pronta para PTC

- [ ] Diretório `ptc_source/` criado com arquivos renomeados
- [ ] Ordem sequencial clara (01-, 02-, 03-, etc.)
- [ ] BibTeX atualizado em `results/ptc/referencias.bib`

---

## 📖 Referências Internas

- **Pipeline consolidado**: `research/src/pipeline/`
- **Banco canônico**: `research/systematic_review.sqlite`
- **Exports atuais**: `research/exports/`
- **Análise profunda (opcional via CLI)**: `research/exports/deep_analysis/`
- **Template PTC**: `results/ptc/`

---

**Data do Relatório**: 16/11/2025  
**Próxima Ação**: Executar Fase 1 (Limpeza de Depreciados)
