# Relatório de Reconciliação: Recorte Temporal 2015 vs 2016

**Data:** 2026-08-30
**Autor:** Thales Ferreira Batista
**Status:** Histórico superseded pela reconciliação do baseline de 31/08/2026

> **Nota:** as tabelas e recomendações abaixo preservam a análise temporal anterior, baseada em 9.431 registros e 17 incluídos. Elas não representam o fluxo vigente. A nova execução consolidou 11.904 registros, avaliou 23 candidatos e registrou 7 overrides manuais, mantendo 16 registros retidos operacionalmente; quatro overrides ainda aguardam adjudicação de escopo. Consulte `docs/RECONCILIACAO-BASELINE-2026-08-31.md` antes de reutilizar qualquer número ou recomendação.

---

## 1. Aquisição Realmente Executada

O pipeline histórico coletou registros de **2015 a 2025**:

| Ano | Total Coletados |
|-----|----------------|
| 2015 | 312 |
| 2016 | 369 |
| 2017 | 441 |
| 2018 | 405 |
| 2019 | 533 |
| 2020 | 761 |
| 2021 | 696 |
| 2022 | 707 |
| 2023 | 801 |
| 2024 | 970 |
| 2025 | 714 |
| 2026 | 2 |
| **Total** | **6.914** |

**Nota:** 2026 aparece com 2 registros, mas o ano ainda não está encerrado.

---

## 2. Seleção Realmente Executada

| Fase | Entraram | Saíram | Restaram |
|------|----------|--------|----------|
| Identificação | 9.431 | - | 9.431 |
| Remoção duplicatas | 9.431 | 2.517 | 6.914 |
| Triagem | 6.914 | 5.031 | 1.883 |
| Elegibilidade | 1.883 | 1.866 | 17 |
| Inclusão | 17 | - | 17 |

**Total incluídos:** 17 estudos

---

## 3. Intenção Metodológica do Autor

O autor informou que o recorte pretendido é **2016–2025** (dez anos inclusivos).

**Porém:** A execução histórica coletou registros de 2015.

---

## 4. Impacto de Excluir Formalmente 2015

### 4.1 Nos 17 estudos incluídos

| Ano | Incluídos |
|-----|-----------|
| 2015 | **0** |
| 2016 | 0 |
| 2017 | 2 |
| 2019 | 1 |
| 2020 | 2 |
| 2021 | 2 |
| 2022 | 2 |
| 2023 | 2 |
| 2024 | 3 |
| 2025 | 3 |
| **Total** | **17** |

**Conclusão:** Excluir 2015 **NÃO altera** os 17 estudos incluídos. Nenhum estudo de 2015 foi incluído.

### 4.2 Nos números PRISMA

| Cenário | Identification | Screening | Eligibility | Included |
|---------|---------------|-----------|-------------|----------|
| Atual (2015-2025) | 9.431 | 6.914 | 1.883 | 17 |
| Sem 2015 (2016-2025) | 9.119 | 6.602 | 1.883* | 17 |
| Sem 2015+2016 (2017-2025) | 8.750 | 6.233 | 1.883* | 17 |

*Nota: O número de papers que entram na elegibilidade depende de quantos passam a triagem, não apenas do recorte inicial.

### 4.3 Impacto na identificação

- Remover 2015: **-312 registros** (9.431 → 9.119)
- Remover 2015+2016: **-681 registros** (9.431 → 8.750)

---

## 5. Impacto nos Números PRISMA

### 5.1 Se mantivermos 2015 no relato

O relato atual está correto: "a aquisição histórica abrangeu 2015–2025".

### 5.2 Se mudarmos para 2016-2025

Precisaríamos atualizar:
- Identification: 9.119 (ou recalculado after dedup)
- Todos os números downstream

### 5.3 Recomendação

Como nenhum estudo de 2015 foi incluído, a mudança 2015→2016 é **principalmente documental**. Os 17 estudos incluídos permanecem os mesmos.

Uma formulação possível:

> "A aquisição histórica abrangeu 2015–2025, mas o recorte analítico definido foi 2016–2025 (dez anos inclusivos). Registros de 2015 foram coletados mas nenhum atendeu aos critérios de inclusão."

---

## 6. Correção do Bug AI/assessment

### 6.1 Bug identificado

**selection.py (linha 117-118):**
```python
# ANTES (bug):
if re.search(r"(machine learning|artificial intelligence|AI|data mining|analytics|tutor|adaptive|personalized)", ...)

# DEPOIS (corrigido):
if re.search(r"(machine learning|artificial intelligence|\bai\b|data mining|learning analytics|tutor|adaptive|personalized)", ...)
```

**scoring.py (linha 14-15):**
```python
# ANTES (bug):
ML_TERMS = r"(machine learning|deep learning|data mining|neural network|svm|random forest|bayes|lstm|artificial intelligence|AI|predictive|classification|clustering)"
LA_TERMS = r"(learning analytics|educational data mining|intelligent tutor|adaptive learning|personalized learning|student modeling|competenc|skill|assessment)"

# DEPOIS (corrigido):
ML_TERMS = r"(machine learning|deep learning|data mining|neural network|svm|random forest|bayes|lstm|artificial intelligence|\bai\b|predictive|classification|clustering)"
LA_TERMS = r"(learning analytics|educational data mining|intelligent tutor|adaptive learning|personalized learning|student modeling|competenc)"
```

### 6.2 Causa raiz

- `AI` sem `\b` causava falsos positivos em palavras como "aims", "training", "Ghanaian"
- `assessment` em LA_TERMS era amplo demais — pegava estudos educacionais sem analytics/ML

### 6.3 Impacto nos 3 estudos suspeitos

| Estudo | Técnicas (ANTES) | Técnicas (DEPOIS) | Ação |
|--------|------------------|-------------------|------|
| Enhancing Student Achievement in Circle Theorems | Não especificado | N/A (sem técnica) | **EXCLUIR** |
| Authentic Assessment for Motivating Student Learning | Machine Learning, Assessment | N/A (sem técnica) | **EXCLUIR** |
| Performance assessment: Improving metacognitive ability | Assessment | N/A (sem técnica) | **EXCLUIR** |

### 6.4 Recomendação

Após correção do bug, os 3 estudos **não deveriam ter sido incluídos**. Recomendação:

1. Aplicar correção no código
2. Re-executar seleção (ou marcar manualmente para exclusão)
3. Atualizar PRISMA: 17 → **14** estudos incluídos
4. Reauditar os 14 restantes

---

## 7. Lista de Quaisquer Outras Falhas Descobertas

1. **Bug AI substring** — corrigido
2. **Bug assessment em LA_TERMS** — corrigido
3. **Números obsoletos em documentação antiga** — já corrigidos na branch
4. **Metodologia antiga dizia "peer-reviewed" mas pipeline não exigia** — branch já começou a corrigir

---

## 8. Recomendação sobre Representação do Protocolo

### Opção A: Manter 2015-2025 no relato

> "A busca abrangeu 2015–2025, totalizando 6.914 registros únicos após deduplicação, dos quais 17 atenderam aos critérios de inclusão."

**Prós:** Transparência total, reflete o que foi executado
**Contras:** Pode causar confusão se o autor pretende 2016-2025

### Opção B: Relatar 2015 como pré-coleta

> "A aquisição histórica abrangeu 2015–2025, mas o recorte analítico definido foi 2016–2025. Registros de 2015 foram coletados mas nenhum atendeu aos critérios de inclusão."

**Prós:** Honra tanto a execução quanto a intenção
**Contras:** Mais complexo de relatar

### Opção C: Recalcular sem 2015

Remover 2015 do banco e recalcular todos os números.

**Prós:** Números consistentes com 2016-2025
**Contras:** Perde rastreabilidade histórica

### Recomendação: **Opção B**

É a mais honesta e completa. Mantém rastreabilidade enquanto honra a intenção do autor.

---

## 9. Próximos Passos (para o orientador decidir)

1. **Confirmar recorte:** 2016-2025 ou manter 2015-2025?
2. **Decidir sobre os 3 estudos:** Excluir após correção do bug?
3. **Atualizar PRISMA:** 17 → 14 incluídos (se excluir os 3)?
4. **Re-executar pipeline:** After correções, re-validar números
5. **Decidir sobre atualização 2026:** Incluir ou não?

---

## 10. Proposta de Arquitetura para Agente Local

(Esta seção será preenchida conforme solicitado no handoff)

---

**Status:** Aguardando decisão do orientador sobre pontos 1-5.
