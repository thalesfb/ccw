# 📰 Fundamentação Teórica: Técnicas Computacionais na Educação Matemática

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

#### Termos Secundários (Técnicas Computacionais)
- "adaptive learning" / "aprendizagem adaptativa"
- "personalized learning" / "aprendizagem personalizada"
- "intelligent tutoring systems" / "sistemas de tutoria inteligente"
- "learning analytics" / "análise de aprendizagem"
- "educational data mining" / "mineração de dados educacionais"
- "machine learning" / "aprendizado de máquina"
- "artificial intelligence" / "inteligência artificial"
- "automated assessment" / "avaliação automatizada"
- "competency identification" / "identificação de competências"
- "student modeling" / "modelagem de estudantes"
- "predictive analytics" / "análise preditiva"

#### Geração de Combinações
A combinação dos termos primários e secundários utiliza o operador booleano `AND`, gerando **132 combinações** únicas para busca (6 termos primários × 22 termos secundários).

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

*Esta fundamentação teórica serve como base científica para o desenvolvimento de sistemas computacionais aplicados à educação matemática, garantindo rigor metodológico e relevância prática dos resultados obtidos.*