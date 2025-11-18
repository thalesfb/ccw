# 📰 Fundamentação Teórica: Técnicas Computacionais na Educação Matemática

> **Nota**: Esta fundamentação teórica serve como base para a **Fase 1** do Projeto de TCC (PTCC) - Revisão Sistemática da Literatura. As bases teóricas para as Fases 2 e 3 serão expandidas conforme o desenvolvimento do protótipo e validação experimental.

## 🌟 Contexto e Relevância

A transformação digital tem impactado significativamente diversas áreas, inclusive a educação. No ensino da matemática, técnicas computacionais emergem como ferramentas poderosas para personalizar o ensino, diagnosticar o desempenho dos alunos e identificar, de forma automatizada, seus pontos fortes e fracos. 

Abordagens como **Machine Learning**, **Learning Analytics** e **Sistemas Tutores Inteligentes** têm demonstrado grande potencial ao proporcionar intervenções pedagógicas precisas, contribuindo para uma gestão mais eficaz da aprendizagem.

## 🎯 Objetivos da Pesquisa

### Objetivo Geral
Mapear as técnicas e abordagens computacionais aplicadas à educação matemática, com ênfase em Machine Learning, Learning Analytics e Sistemas Tutores Inteligentes, visando compreender como essas tecnologias têm sido utilizadas para diagnosticar o desempenho dos alunos e melhorar seus processos de aprendizagem.

### Objetivos Específicos

1. **Revisão Sistemática**: Realizar uma revisão sistemática da literatura para identificar estudos que apliquem técnicas computacionais no ensino da matemática.

2. **Análise de Métodos**: Analisar a aplicação de métodos como Machine Learning e Learning Analytics na personalização e avaliação do processo educacional.

3. **Identificação de Avanços**: Identificar os principais avanços, desafios e lacunas na utilização de sistemas tutores inteligentes e tecnologias correlatas.

4. **Subsídios para Desenvolvimento**: Fornecer subsídios para o desenvolvimento de um protótipo que integre essas abordagens com o objetivo de otimizar os planos de ensino e a gestão do desempenho dos alunos.

## 🧠 Questões de Pesquisa

A presente investigação busca responder às seguintes questões fundamentais:

1. **Personalização Tecnológica**: Quais tecnologias computacionais estão sendo aplicadas para personalizar o ensino de matemática?

2. **Identificação de Competências**: Como técnicas de machine learning e inteligência artificial têm sido utilizadas para identificar competências individuais de alunos?

3. **Metodologias Adaptativas**: Quais são as metodologias mais eficazes para adaptar planos de ensino com base em dados de desempenho dos alunos?

4. **Métricas de Avaliação**: Que tipos de métricas e indicadores são usados para avaliar competências matemáticas em ambientes educacionais?

5. **Evolução dos Sistemas Tutores**: Como sistemas tutores inteligentes têm evoluído para oferecer recomendações pedagógicas personalizadas?

## 📋 Metodologia de Pesquisa

### Estratégia de Busca Automatizada

A busca é realizada de forma **automatizada utilizando as APIs** das seguintes bases de dados científicas:

#### 🗃️ Bases de Dados Selecionadas

1. **Semantic Scholar**: Ampla cobertura em ciência da computação e áreas relacionadas
   - Endpoint: `https://api.semanticscholar.org/graph/v1/paper/search`
   - Vantagens: Métricas de influência, foco em impacto científico
   - Taxa de consulta: 1 requisição a cada 4 segundos

2. **OpenAlex**: Base de dados aberta e abrangente, sucessora do Microsoft Academic Graph
   - Endpoint: `https://api.openalex.org/works`
   - Vantagens: Dados sobre afiliações institucionais, ampla cobertura
   - Taxa de consulta: 1 requisição a cada 6 segundos (polite pool)

3. **Crossref**: Foco em metadados de publicações e DOIs
   - Endpoint: `https://api.crossref.org/works`
   - Vantagens: Precisão bibliográfica, periódicos tradicionais
   - Taxa de consulta: 1 requisição a cada 4 segundos

4. **CORE**: Agregador de artigos de pesquisa de acesso aberto
   - Endpoint: `https://api.core.ac.uk/v3/search/works`
   - Vantagens: Conteúdos de acesso aberto, diversidade de fontes
   - Taxa de consulta: 1 requisição a cada 6 segundos

### 🔎 Estratégia de Termos de Busca

#### Termos Primários (Domínio de Aplicação)
- "mathematics education" / "educação matemática"
- "math learning" / "aprendizagem matemática" 
- "mathematics teaching" / "ensino de matemática"

#### Termos Secundários (22 Técnicas Computacionais)
1. "machine learning" / "aprendizado de máquina"
2. "artificial intelligence" / "inteligência artificial"
3. "deep learning" / "aprendizado profundo"
4. "neural networks" / "redes neurais"
5. "natural language processing" / "processamento de linguagem natural"
6. "educational data mining" / "mineração de dados educacionais"
7. "learning analytics" / "análise de aprendizagem"
8. "adaptive learning" / "aprendizagem adaptativa"
9. "personalized learning" / "aprendizagem personalizada"
10. "intelligent tutoring systems" / "sistemas de tutoria inteligente"
11. "automated assessment" / "avaliação automatizada"
12. "predictive analytics" / "análise preditiva"
13. "student modeling" / "modelagem de estudantes"
14. "competency identification" / "identificação de competências"
15. "recommendation systems" / "sistemas de recomendação"
16. "reinforcement learning" / "aprendizado por reforço"
17. "knowledge tracing" / "rastreamento de conhecimento"
18. "cognitive modeling" / "modelagem cognitiva"
19. "learning design" / "design de aprendizagem"
20. "educational technology" / "tecnologia educacional"
21. "computer-aided instruction" / "instrução assistida por computador"
22. "e-learning systems" / "sistemas de e-learning"

#### Geração de Combinações
A combinação dos termos primários e secundários utiliza o operador booleano `AND`, gerando **132 combinações** únicas para busca:

```python
# Fonte: research/src/search_terms.py
FIRST_TERMS = 6   # Termos educacionais (PT + EN)
SECOND_TERMS = 22 # Técnicas computacionais
TOTAL_QUERIES = 6 × 22 = 132 queries ✅ VERIFICADO
```

Cada query segue o formato: `"termo_primário" AND "termo_secundário"`

Exemplos práticos:
- "mathematics education" AND "machine learning"
- "educação matemática" AND "aprendizado de máquina"
- "math learning" AND "intelligent tutoring systems"

### 🚩 Critérios de Seleção

#### ✔️ Critérios de Inclusão

1. **Qualidade Científica**: Artigos completos revisados por pares (peer-reviewed)
2. **Recorte Temporal**: Estudos publicados nos últimos 10 anos (2015-2025)
3. **Relevância Temática**: Foco explícito na aplicação de técnicas computacionais no contexto do ensino e aprendizagem da matemática
4. **Evidência Empírica**: Estudos que apresentem dados empíricos, descrições detalhadas de metodologias ou evidências de desenvolvimento/avaliação de sistemas
5. **Replicabilidade**: Fontes que permitam a replicabilidade dos resultados
6. **Idiomas**: Inglês ou Português

#### ❌ Critérios de Exclusão

1. **Metodologia Insuficiente**: Estudos com metodologia insuficiente ou incoerente, cuja descrição dos métodos seja vaga
2. **Foco Descontextualizado**: Trabalhos com foco indireto ou descontextualizado da matemática
3. **Falta de Suporte Empírico**: Publicações predominantemente sem suporte empírico (dados, testes, validação)
4. **Impacto Não Mensurável**: Estudos com impacto não mensurável ou irrelevante
5. **Falta de Validação**: Documentos não validados cientificamente (preprints, relatórios internos)
6. **Falhas Conceituais**: Estudos com falhas conceituais ou contradições metodológicas
7. **Limitações Linguísticas**: Publicações em idiomas não compatíveis

### 🗯️ Processo de Seleção (PRISMA)

O processo de seleção dos estudos segue as diretrizes **PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)**:

1. **Identificação**: Coleta inicial de artigos das bases de dados usando as strings de busca definidas
2. **Triagem**: Leitura de títulos e resumos dos artigos únicos, aplicação dos critérios de inclusão/exclusão
3. **Elegibilidade**: Leitura completa dos artigos pré-selecionados, verificação detalhada dos critérios
4. **Inclusão**: Artigos que passaram por todas as etapas são incluídos na síntese qualitativa

## 🔑 Justificativas Metodológicas

### Escolha das APIs
A integração de múltiplas APIs proporciona:
- **Cobertura Complementar**: Cada base tem forças específicas (Semantic Scholar para impacto, OpenAlex para amplitude, Crossref para precisão, CORE para acesso aberto)
- **Redução de Viés**: Minimiza vieses de seleção de uma única fonte
- **Reprodutibilidade**: Automação permite replicação exata do processo
- **Eficiência**: Coleta sistemática de grandes volumes de dados

### Critérios de Recorte Temporal
O período de 2015-2025 foi escolhido por representar:
- **Era da IA Educacional**: Período de maior evolução nas técnicas computacionais educacionais
- **Maturidade do Machine Learning**: Consolidação de técnicas de ML aplicadas à educação
- **Explosão do Learning Analytics**: Desenvolvimento massivo de ferramentas de análise educacional
- **Relevância Tecnológica**: Tecnologias ainda atuais e aplicáveis

### Abordagem Bilíngue
A inclusão de termos em português e inglês visa:
- **Amplitude Geográfica**: Capturar pesquisas de diferentes regiões
- **Diversidade Cultural**: Incluir abordagens culturalmente específicas
- **Completude**: Evitar perda de estudos relevantes por limitações linguísticas

## 📊 Estrutura de Dados para Análise

### Campos de Classificação
Cada artigo coletado é classificado segundo os seguintes critérios:

- **Bibliográficos**: título, autores, ano, venue, DOI/URL
- **Conteúdo**: abstract, texto completo (quando disponível)
- **Técnicos**: técnicas computacionais aplicadas, métodos de avaliação
- **Educacionais**: tópico matemático específico, tipo de estudo
- **Qualidade**: fonte de dados, acesso aberto, relevância
- **Processo**: estágio PRISMA, motivos de exclusão

### Métricas de Qualidade
- **Relevância**: Pontuação 1-5 baseada na aderência aos critérios
- **Impacto**: Número de citações e métricas de influência
- **Metodologia**: Robustez do design experimental
- **Aplicabilidade**: Potencial de implementação prática

## 🎯 Contribuições Esperadas

Esta fundamentação teórica e metodológica visa:

1. **Mapeamento Sistemático**: Criar um panorama completo e atualizado da área
2. **Identificação de Lacunas**: Encontrar oportunidades de pesquisa e desenvolvimento
3. **Base para Protótipo**: Fornecer subsídios científicos sólidos para desenvolvimento tecnológico
4. **Referencial Teórico**: Estabelecer uma base conceitual robusta para futuras pesquisas
5. **Diretrizes Práticas**: Orientar implementações de tecnologias educacionais baseadas em evidências

---

---

## 📚 Referências

BAKER, R. S.; INVENTADO, P. S. **Educational data mining and learning analytics**. In: LARUSSON, J. A.; WHITE, B. (Ed.). Learning analytics: From research to practice. New York: Springer, 2014. p. 61-75.

CHASSIGNOL, M. et al. Artificial Intelligence trends in education: a narrative overview. **Procedia Computer Science**, v. 136, p. 16-24, 2018. DOI: 10.1016/j.procs.2018.08.233.

HOLMES, W. et al. **Artificial intelligence in education**: Promises and implications for teaching and learning. Brussels: European Parliament, 2019.

LUCKIN, R. et al. **Intelligence Unleashed: An argument for AI in Education**. London: Pearson, 2016.

ROLL, I.; WYLIE, R. Evolution and revolution in artificial intelligence in education. **International Journal of Artificial Intelligence in Education**, v. 26, n. 2, p. 582-599, 2016. DOI: 10.1007/s40593-016-0110-3.

SIEMENS, G.; BAKER, R. S. Learning analytics and educational data mining: towards communication and collaboration. In: **Proceedings of the 2nd International Conference on Learning Analytics and Knowledge**. ACM, 2012. p. 252-254. DOI: 10.1145/2330601.2330661.

VAN LEEUWEN, A. et al. Teacher perspectives on the development of adaptive educational technology. **Educational Technology Research and Development**, v. 67, n. 5, p. 1207-1233, 2019. DOI: 10.1007/s11423-019-09655-2.

ZAWACKI-RICHTER, O. et al. Systematic review of research on artificial intelligence applications in higher education – where are the educators? **International Journal of Educational Technology in Higher Education**, v. 16, n. 1, p. 1-27, 2019. DOI: 10.1186/s41239-019-0171-0.

BAKER, R. S. J. D.; YACEF, K. The state of educational data mining in 2009: A review and future visions. **Journal of Educational Data Mining**, v. 1, n. 1, p. 3-17, 2009.

CONATI, C.; JAQUES, N.; MUIR, M. Understanding attention to adaptive hints in educational games: An eye-tracking study. **International Journal of Artificial Intelligence in Education**, v. 23, n. 1-4, p. 136-161, 2013. DOI: 10.1007/s40593-013-0002-8.

---

*Esta fundamentação teórica serve como base científica para o desenvolvimento de sistemas computacionais aplicados à educação matemática, garantindo rigor metodológico e relevância prática dos resultados obtidos.*
```