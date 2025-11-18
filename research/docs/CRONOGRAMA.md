# 📅 Cronograma de Execução do Projeto

> Este cronograma detalha as atividades planejadas para o desenvolvimento completo do Trabalho de Conclusão de Curso, organizado em três fases principais.

---

## 🎯 Visão Geral do Projeto

### Estrutura em Fases

| Fase | Descrição | Duração | Status | Período |
|------|-----------|---------|--------|---------|
| **Fase 1** | Revisão Sistemática da Literatura | 12 semanas | ✅ CONCLUÍDA | Ago-Out/2025 |
| **Fase 2** | Desenvolvimento do Protótipo | 8 semanas | 📋 PLANEJADA | Mar-Abr/2026 |
| **Fase 3** | Validação Experimental | 6 semanas | 📋 PLANEJADA | Mai-Jun/2026 |

**Duração total estimada**: 26 semanas (~6,5 meses)

---

## ✅ Fase 1: Revisão Sistemática da Literatura (CONCLUÍDA)

**Período**: Agosto - Outubro/2025 (12 semanas)  
**Status**: ✅ **CONCLUÍDA**

### Atividades Realizadas

| Semana | Atividade | Entregas | Status |
|--------|-----------|----------|--------|
| 1-2 | Definição do protocolo PRISMA | Protocolo de revisão, critérios de elegibilidade | ✅ |
| 3-4 | Definição de termos de busca | 108 queries bilíngues (3×6×6 EN + 3×6×2 PT) | ✅ |
| 5-6 | Coleta de dados (APIs) | 6.516 papers identificados | ✅ |
| 7-8 | Triagem e elegibilidade | 16 papers selecionados | ✅ |
| 9-10 | Análise temática | Categorização por abordagem e finalidade | ✅ |
| 11-12 | Síntese e documentação | Relatórios, visualizações, documentação | ✅ |

### Entregas Concluídas

- ✅ Base de dados estruturada (SQLite): `research/systematic_review.db`
- ✅ Pipeline automatizado e reproduzível: `research/src/pipeline/`
- ✅ Documentação acadêmica completa:
  - `RESUMO.md` (PT/EN)
  - `INTRODUCAO.md`
  - `FUNDAMENTACAO_TEORICA.md`
  - `METODOLOGIA.md`
  - `RESULTADOS_PRELIMINARES.md`
  - `CONCLUSOES.md` (Fase 1)
  - `GLOSSARIO.md`
- ✅ Bibliografia formal: `references/referencias_metodologia.bib` (11 refs)
- ✅ Relatórios PRISMA: `exports/reports/`
- ✅ Análises quantitativas: `exports/analysis/`

### Produtos Gerados

1. **Base de Conhecimento**: 16 estudos de alta relevância (score ≥4.0)
2. **Framework Conceitual**: Categorização de aplicações de IA em educação matemática
3. **Infraestrutura Técnica**: Pipeline reproduzível para revisões sistemáticas
4. **Publicações Potenciais**: Material suficiente para artigo científico sobre revisão sistemática

---

## 📋 Fase 2: Desenvolvimento do Protótipo (PLANEJADA)

**Período**: Março - Abril/2026 (8 semanas)  
**Status**: 📋 **PLANEJADA**  
**Disciplina**: TCC (Trabalho de Conclusão de Curso)

### Objetivos da Fase 2

Desenvolver um protótipo funcional de sistema de diagnóstico de competências matemáticas baseado em IA, fundamentado nos achados da revisão sistemática (Fase 1).

### Atividades Planejadas

#### Semanas 1-2: Especificação e Design do Sistema

| Atividade | Descrição | Entregas Esperadas |
|-----------|-----------|-------------------|
| **Requisitos Funcionais** | Definir funcionalidades do sistema baseadas na revisão sistemática | Documento de requisitos |
| **Arquitetura do Sistema** | Projetar arquitetura técnica (backend, frontend, ML pipeline) | Diagrama de arquitetura |
| **Seleção de Tecnologias** | Escolher stack tecnológico (Python, frameworks ML, banco de dados) | Justificativa técnica |
| **Design de Interface** | Prototipar interface de usuário (professores e estudantes) | Wireframes, mockups |

**Entregas**: Documento de especificação técnica (20-30 páginas)

---

#### Semanas 3-4: Desenvolvimento do Backend

| Atividade | Descrição | Entregas Esperadas |
|-----------|-----------|-------------------|
| **Modelagem de Dados** | Definir schema de banco de dados (competências, avaliações, perfis) | Diagrama ER, scripts SQL |
| **API REST** | Implementar endpoints (autenticação, CRUD de avaliações, diagnóstico) | API documentada (Swagger/OpenAPI) |
| **Integração ML** | Implementar pipeline de diagnóstico (classificação, predição) | Módulo ML funcional |
| **Testes Unitários** | Cobertura de testes ≥80% | Suite de testes (pytest) |

**Entregas**: Backend funcional com API REST documentada

---

#### Semanas 5-6: Desenvolvimento do Frontend e Integração

| Atividade | Descrição | Entregas Esperadas |
|-----------|-----------|-------------------|
| **Interface Professor** | Dashboard para visualização de diagnósticos, recomendações | Aplicação web (React/Vue/Angular) |
| **Interface Estudante** | Sistema de avaliação adaptativa | Aplicação web responsiva |
| **Integração Backend-Frontend** | Conectar frontend com API REST | Sistema integrado |
| **Testes de Integração** | Validar fluxos completos (E2E testing) | Suite de testes (Cypress/Selenium) |

**Entregas**: Sistema completo funcional (MVP - Minimum Viable Product)

---

#### Semanas 7-8: Refinamento e Documentação

| Atividade | Descrição | Entregas Esperadas |
|-----------|-----------|-------------------|
| **Refinamento UX** | Melhorias de usabilidade baseadas em testes internos | Sistema refinado |
| **Documentação Técnica** | Manual de instalação, uso e manutenção | Documentação completa |
| **Documentação Acadêmica** | Capítulo "Desenvolvimento" da monografia | Texto acadêmico (15-20 páginas) |
| **Preparação Fase 3** | Planejamento da validação experimental | Protocolo de validação |

**Entregas**: Sistema pronto para validação experimental

---

### Recursos Necessários (Fase 2)

#### Infraestrutura Técnica

- **Servidor de Desenvolvimento**: VPS ou instância cloud (AWS/Azure/DigitalOcean)
- **Banco de Dados**: PostgreSQL ou MySQL
- **Ambiente ML**: GPU (opcional, para treinamento de modelos)
- **Repositório**: GitHub para controle de versão

#### Software e Ferramentas

- **Linguagens**: Python 3.10+, JavaScript/TypeScript
- **Frameworks Backend**: FastAPI ou Django REST Framework
- **Frameworks Frontend**: React ou Vue.js
- **ML/AI**: scikit-learn, TensorFlow/PyTorch (se necessário)
- **Testes**: pytest, Cypress, coverage.py
- **Documentação**: Sphinx (Python), Swagger (API)

#### Recursos Humanos

- **Desenvolvedor Principal**: Aluno (Thales Ferreira)
- **Orientador**: Prof. Dr. Rafael Zanin (orientação técnica e acadêmica)
- **Coorientador**: Prof. Dr. Manassés Ribeiro (expertise em educação matemática)
- **Consultoria Opcional**: Docentes de Engenharia de Software (para revisão de arquitetura)

---

### Entregas Finais da Fase 2

1. **Sistema Funcional (MVP)**
   - Backend com API REST documentada
   - Frontend com interfaces professor/estudante
   - Pipeline ML para diagnóstico de competências
   - Testes automatizados (cobertura ≥80%)

2. **Documentação Técnica**
   - Manual de instalação e configuração
   - Documentação de API (Swagger/OpenAPI)
   - Guia de uso para professores

3. **Documentação Acadêmica**
   - Capítulo "Desenvolvimento" (15-20 páginas)
   - Decisões de design justificadas pela revisão sistemática
   - Análise de trade-offs técnicos

4. **Repositório GitHub**
   - Código-fonte completo
   - README com instruções claras
   - Licença open-source (MIT ou GPL)

---

## 📋 Fase 3: Validação Experimental (PLANEJADA)

**Período**: Maio - Junho/2026 (6 semanas)  
**Status**: 📋 **PLANEJADA**  
**Disciplina**: TCC (Trabalho de Conclusão de Curso)

### Objetivos da Fase 3

Validar a eficácia do protótipo desenvolvido em contexto educacional real, coletando evidências empíricas sobre sua usabilidade, acurácia diagnóstica e impacto pedagógico.

### Atividades Planejadas

#### Semanas 1-2: Preparação do Experimento

| Atividade | Descrição | Entregas Esperadas |
|-----------|-----------|-------------------|
| **Aprovação Ética** | Submeter protocolo ao Comitê de Ética em Pesquisa (CEP) | Aprovação CEP |
| **Seleção de Participantes** | Recrutar professores e estudantes (escola parceira) | Termos de consentimento assinados |
| **Preparação de Material** | Criar avaliações diagnósticas, questionários de usabilidade | Material de coleta de dados |
| **Treinamento** | Capacitar professores no uso do sistema | Professores treinados |

**Entregas**: Protocolo experimental aprovado, participantes recrutados

---

#### Semanas 3-4: Execução do Experimento

| Atividade | Descrição | Entregas Esperadas |
|-----------|-----------|-------------------|
| **Aplicação Pré-teste** | Avaliar conhecimentos prévios dos estudantes | Dados de baseline |
| **Uso do Sistema** | Estudantes utilizam o sistema (2 semanas, 3-4 sessões) | Logs de interação, diagnósticos gerados |
| **Observação** | Acompanhar uso em sala de aula | Notas de campo |
| **Coleta de Feedback** | Aplicar questionários de usabilidade (professores e estudantes) | Dados de percepção |

**Entregas**: Dados brutos coletados (interações, diagnósticos, questionários)

---

#### Semanas 5-6: Análise e Documentação

| Atividade | Descrição | Entregas Esperadas |
|-----------|-----------|-------------------|
| **Análise Quantitativa** | Estatísticas descritivas, testes de hipóteses | Resultados estatísticos |
| **Análise Qualitativa** | Análise temática de feedback aberto | Categorias temáticas |
| **Interpretação** | Discutir resultados à luz da revisão sistemática | Discussão fundamentada |
| **Documentação Acadêmica** | Capítulos "Resultados" e "Discussão" da monografia | Texto acadêmico (20-30 páginas) |

**Entregas**: Análise completa dos resultados experimentais

---

### Metodologia de Validação

#### Design Experimental

**Tipo**: Estudo de caso único com medidas pré/pós  
**Participantes**: 30-50 estudantes + 2-3 professores (amostra de conveniência)  
**Contexto**: Turmas de Ensino Fundamental II ou Médio (matemática)  
**Duração**: 2 semanas de intervenção

#### Variáveis de Interesse

**Variáveis Dependentes**:
1. **Acurácia Diagnóstica**: Concordância entre diagnóstico do sistema e avaliação de professores
2. **Usabilidade**: Escores SUS (System Usability Scale)
3. **Satisfação**: Questionário Likert (1-5)
4. **Engajamento**: Tempo de uso, taxa de conclusão de atividades

**Variáveis Independentes**:
- Uso do sistema (presença/ausência)
- Perfil do estudante (desempenho prévio em matemática)

#### Instrumentos de Coleta

1. **Testes de Conhecimento**: Pré-teste e pós-teste (mesmas competências)
2. **Questionário SUS**: 10 itens para avaliar usabilidade
3. **Questionário de Satisfação**: 15 itens Likert (escala 1-5)
4. **Entrevistas Semiestruturadas**: Professores (30-45 min cada)
5. **Logs do Sistema**: Interações, tempo de uso, diagnósticos gerados

#### Análise de Dados

**Quantitativa**:
- Estatísticas descritivas (média, desvio-padrão, frequências)
- Testes t pareados (pré-teste vs. pós-teste)
- Correlação de Pearson (acurácia diagnóstico vs. avaliação professor)
- Análise de usabilidade (SUS score ≥68 = aceitável)

**Qualitativa**:
- Análise temática de entrevistas (Braun & Clarke, 2006)
- Categorização de feedback aberto
- Triangulação com dados quantitativos

---

### Recursos Necessários (Fase 3)

#### Parcerias Institucionais

- **Escola Parceira**: Ensino Fundamental II ou Médio (IFC ou rede pública/privada de Videira)
- **Comitê de Ética**: Submissão ao CEP do IFC ou plataforma Brasil

#### Recursos Materiais

- **Computadores/Tablets**: Para acesso dos estudantes ao sistema (laboratório de informática)
- **Internet**: Conexão estável durante sessões de uso
- **Material Impresso**: Termos de consentimento, questionários

#### Recursos Humanos

- **Pesquisador**: Aluno (coleta de dados, análise)
- **Orientadores**: Apoio metodológico e pedagógico
- **Professores Participantes**: Aplicação em sala de aula (remuneração simbólica ou certificação)

---

### Entregas Finais da Fase 3

1. **Relatório de Validação Experimental**
   - Descrição do protocolo experimental
   - Resultados quantitativos (estatísticas, gráficos)
   - Resultados qualitativos (temas identificados)
   - Discussão fundamentada na revisão sistemática

2. **Capítulos da Monografia**
   - "Resultados" (15-20 páginas)
   - "Discussão" (10-15 páginas)
   - "Conclusões e Trabalhos Futuros" (5-10 páginas)

3. **Dataset Anonimizado**
   - Dados brutos (sem identificação de participantes)
   - Disponibilização em repositório público (OSF, Zenodo)

4. **Artigo Científico (opcional)**
   - Submissão a conferência ou periódico da área
   - Divulgação dos resultados para comunidade acadêmica

---

## 📊 Resumo de Entregas por Fase

| Fase | Entregas Principais | Formato | Status |
|------|---------------------|---------|--------|
| **Fase 1** | Revisão sistemática, pipeline, documentação | Markdown, SQLite, Python | ✅ CONCLUÍDA |
| **Fase 2** | Protótipo funcional, documentação técnica | Software (GitHub), LaTeX | 📋 PLANEJADA |
| **Fase 3** | Validação experimental, análise de dados | LaTeX, dataset | 📋 PLANEJADA |

---

## 🎓 Integração com Disciplinas do Curso

### PTCC (Projeto de TCC)

**Semestre**: 2025/2  
**Status**: 🔄 EM ANDAMENTO  
**Entrega**: Projeto de pesquisa completo (Fases 1-3 planejadas)

**Componentes**:
- ✅ Revisão sistemática (Fase 1 - concluída)
- 📋 Proposta de protótipo (Fase 2 - especificação)
- 📋 Protocolo de validação (Fase 3 - metodologia)
- 📋 Cronograma detalhado (este documento)
- 📋 Orçamento estimado

**Banca de Qualificação**: Novembro/2025  
**Critérios de Avaliação** (Regulamento IFC):
- Relevância e atualidade do tema
- Articulação tema-problema-questões
- Profundidade do referencial teórico
- Clareza/adequação da metodologia
- Exequibilidade e cronograma

---

### TCC (Trabalho Final)

**Semestre**: 2026/1  
**Status**: ⏳ FUTURO  
**Entrega**: Monografia completa + Sistema funcional

**Componentes**:
- Execução Fase 2 (desenvolvimento do protótipo)
- Execução Fase 3 (validação experimental)
- Redação da monografia completa (ABNT)
- Defesa pública perante banca examinadora

**Banca de Defesa**: Junho/2026  
**Peso da banca**: ≥80% da nota final

---

## 💰 Orçamento Estimado

### Recursos Computacionais

| Item | Especificação | Custo Mensal | Duração | Total |
|------|---------------|--------------|---------|-------|
| **Servidor Cloud** | VPS 2 vCPU, 4GB RAM | R$ 50 | 4 meses | R$ 200 |
| **Banco de Dados** | PostgreSQL gerenciado | R$ 30 | 4 meses | R$ 120 |
| **Domínio** | .com.br para sistema | R$ 40 | 1 ano | R$ 40 |

**Subtotal Infraestrutura**: R$ 360

---

### Recursos Materiais

| Item | Especificação | Quantidade | Custo Unit. | Total |
|------|---------------|-----------|-------------|-------|
| **Impressões** | Material para validação | 200 páginas | R$ 0,20 | R$ 40 |
| **Encadernação** | Monografia (banca) | 5 cópias | R$ 15 | R$ 75 |

**Subtotal Materiais**: R$ 115

---

### Total Estimado: R$ 475

> **Observação**: Custos podem ser reduzidos utilizando créditos educacionais (GitHub Student Pack, AWS Educate, Google Cloud for Education).

---

## 📚 Referências

BRAUN, V.; CLARKE, V. Using thematic analysis in psychology. **Qualitative Research in Psychology**, v. 3, n. 2, p. 77-101, 2006. DOI: 10.1191/1478088706qp063oa.

BROOKE, J. SUS: A "quick and dirty" usability scale. In: JORDAN, P. W. et al. (Ed.). **Usability evaluation in industry**. London: Taylor & Francis, 1996. p. 189-194.

PAGE, M. J. et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. **BMJ**, v. 372, n. 71, 2021. DOI: 10.1136/bmj.n71.

YIN, R. K. **Case study research: Design and methods**. 5th ed. Thousand Oaks: SAGE, 2014.

---

*Este cronograma está sujeito a ajustes conforme necessidades identificadas durante execução do projeto, sempre com aprovação dos orientadores e do Colegiado do Curso.*
