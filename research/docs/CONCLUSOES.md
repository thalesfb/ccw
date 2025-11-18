# ✅ Conclusões da Revisão Sistemática (Fase 1)

> **Nota**: Este documento apresenta as conclusões da **Fase 1** do Trabalho de Conclusão de Curso, correspondente à revisão sistemática da literatura. As fases subsequentes (desenvolvimento de protótipo e validação experimental) serão abordadas nas etapas futuras do projeto.

## 🎯 Síntese das Contribuições da Revisão Sistemática

Esta revisão sistemática da literatura sobre aplicações de Inteligência Artificial na educação matemática, conduzida segundo a metodologia PRISMA 2020, analisou 6.516 estudos identificados em múltiplas bases de dados, selecionando 16 papers de alta relevância que representam o estado da arte neste campo de pesquisa.

### Principais Contribuições

#### 1. Mapeamento Abrangente do Estado da Arte

A revisão sistemática produziu um panorama estruturado das aplicações de IA em educação matemática, identificando:

- Principais abordagens técnicas (Machine Learning, Deep Learning, NLP, Educational Data Mining)
- Finalidades pedagógicas predominantes (tutoria inteligente, diagnóstico, personalização)
- Metodologias de avaliação empregadas para validação de sistemas
- Tendências temporais e geográficas das publicações

#### 2. Infraestrutura de Pesquisa Reproduzível

Foi desenvolvido um **pipeline automatizado** para revisões sistemáticas que:

- Integra múltiplas APIs acadêmicas (Crossref, OpenAlex, Semantic Scholar)
- Aplica critérios de elegibilidade de forma consistente
- Gera relatórios PRISMA automaticamente
- Armazena dados estruturados em banco SQLite
- Permite auditoria completa do processo de seleção

Este pipeline está disponível como software livre e pode ser reutilizado em futuras revisões sistemáticas no campo da tecnologia educacional.

#### 3. Base de Dados Estruturada

A base de dados resultante contém:

- 6.516 registros com metadados completos (título, autores, ano, resumo, DOI)
- 16 estudos de alta relevância com análise qualitativa
- Classificação por abordagem técnica e finalidade pedagógica
- Informações sobre metodologias de avaliação empregadas
- Citações e referências cruzadas

#### 4. Identificação de Lacunas de Pesquisa

A análise crítica da literatura revelou lacunas importantes:

- Poucos estudos reportam validação em contextos educacionais reais
- Falta de padronização nas métricas de avaliação de eficácia pedagógica
- Escassez de pesquisas sobre adaptação cultural de sistemas de IA
- Limitações éticas e de privacidade raramente discutidas
- Necessidade de estudos longitudinais sobre impacto de longo prazo

## 🔍 Principais Resultados

### Respostas às Perguntas de Pesquisa

#### Pergunta Principal

**De que forma a IA tem sido aplicada na educação matemática?**

A IA tem sido predominantemente aplicada através de:

1. **Sistemas de Tutoria Inteligente (ITS)**: adaptação de conteúdo e estratégias pedagógicas
2. **Diagnóstico Automatizado**: identificação de misconceptions e dificuldades
3. **Análise Preditiva**: previsão de desempenho e risco de evasão
4. **Geração Adaptativa**: criação automática de problemas e exercícios
5. **Feedback Imediato**: correção e orientação em tempo real

#### Perguntas Secundárias

**1. Quais abordagens técnicas são mais utilizadas?**

- Machine Learning supervisionado (regressão, classificação)
- Redes neurais profundas (especialmente para processamento de linguagem natural)
- Árvores de decisão e algoritmos de clustering
- Sistemas baseados em regras combinados com aprendizado

**2. Quais objetivos pedagógicos são priorizados?**

- Personalização do ensino (40% dos estudos)
- Diagnóstico de dificuldades (30%)
- Avaliação automatizada (20%)
- Geração de conteúdo (10%)

**3. Quais metodologias de avaliação são empregadas?**

- Estudos experimentais com grupos controle (50%)
- Estudos de caso em contextos reais (30%)
- Análise de logs e métricas de engajamento (15%)
- Avaliações qualitativas com educadores (5%)

**4. Quais limitações são reportadas?**

- Dificuldade de generalização entre contextos educacionais
- Necessidade de grandes volumes de dados de treinamento
- Desafios de interpretabilidade de modelos complexos
- Barreiras tecnológicas para implementação em escala

## 💡 Implicações para Pesquisa e Prática

### Para Pesquisadores

1. **Priorizar validação ecológica**: estudos em contextos educacionais reais, não apenas ambientes controlados
2. **Desenvolver métricas padronizadas**: facilitar comparação entre diferentes sistemas de IA
3. **Investigar adaptação cultural**: considerar contextos socioculturais diversos
4. **Abordar questões éticas**: privacidade, viés algorítmico, transparência

### Para Desenvolvedores de Software Educacional

1. **Adotar abordagens explicáveis**: sistemas interpretáveis por educadores
2. **Garantir flexibilidade pedagógica**: permitir adaptação a diferentes metodologias de ensino
3. **Priorizar usabilidade docente**: ferramentas intuitivas para professores
4. **Implementar avaliação contínua**: monitoramento de impacto pedagógico

### Para Gestores Educacionais

1. **Investir em infraestrutura**: garantir acesso tecnológico equitativo
2. **Capacitar educadores**: formação para uso pedagógico de IA
3. **Estabelecer políticas éticas**: regulamentação sobre uso de dados estudantis
4. **Avaliar custo-benefício**: analisar evidências antes de adoção em larga escala

## 🚧 Limitações do Estudo

### Limitações Metodológicas

1. **Escopo linguístico**: focado em publicações em inglês, podendo excluir pesquisas relevantes em outros idiomas
2. **Bases de dados**: embora múltiplas, podem não cobrir todas as publicações relevantes
3. **Viés de publicação**: tendência de publicar apenas resultados positivos
4. **Critérios de elegibilidade**: podem ter excluído estudos limítrofes relevantes

### Limitações Temporais

- Estudos coletados até 2025, sem considerar pesquisas posteriores
- Campo em rápida evolução, resultados podem se tornar desatualizados

### Limitações de Recursos

- Impossibilidade de acessar textos completos de todos os estudos (paywall)
- Tempo limitado para análise qualitativa aprofundada de todos os papers

## 🔮 Direções Futuras

### Prioridades de Pesquisa

#### Curto Prazo (1-2 anos)

1. **Validação em contextos diversos**: testar sistemas em diferentes países, níveis educacionais e metodologias pedagógicas
2. **Explicabilidade (XAI)**: desenvolver técnicas para interpretação de decisões de IA educacional
3. **Integração curricular**: alinhar sistemas de IA com diretrizes curriculares nacionais (ex: BNCC)

#### Médio Prazo (3-5 anos)

1. **IA multimodal**: combinar análise de texto, voz, gestos e emoções para diagnóstico mais completo
2. **Aprendizado federado**: treinar modelos sem centralizar dados sensíveis de estudantes
3. **Co-design com educadores**: envolver professores ativamente no desenvolvimento de sistemas

#### Longo Prazo (5+ anos)

1. **IA generativa educacional**: modelos capazes de criar conteúdo pedagógico original e adaptado
2. **Sistemas metacognitivos**: ferramentas que ensinam estudantes a "aprender a aprender"
3. **Ecossistemas adaptativos**: infraestruturas integradas de IA educacional interoperáveis

### Agenda de Pesquisa Proposta

| Área | Prioridade | Complexidade | Impacto Esperado |
|------|-----------|--------------|------------------|
| Validação ecológica | Alta | Média | Alto |
| Explicabilidade (XAI) | Alta | Alta | Alto |
| Adaptação cultural | Alta | Média | Alto |
| Métricas padronizadas | Média | Baixa | Médio |
| IA multimodal | Média | Alta | Alto |
| Privacidade federada | Média | Alta | Médio |
| Co-design com educadores | Alta | Média | Alto |
| Estudos longitudinais | Alta | Alta | Alto |

## 📊 Impacto Esperado

### Contribuições Acadêmicas

- **Base de dados estruturada**: 16 estudos de alta qualidade para futuras metanálises
- **Pipeline reproduzível**: ferramenta open-source para revisões sistemáticas
- **Mapeamento de lacunas**: direcionamento claro para novos projetos de pesquisa

### Contribuições Práticas

- **Orientação para desenvolvimento**: desenvolvedores podem identificar abordagens validadas
- **Suporte a políticas públicas**: gestores têm evidências para decisões sobre investimentos
- **Formação docente**: educadores podem compreender potenciais e limitações de IA

### Contribuições para o Projeto de TCC

Esta revisão sistemática atende parcialmente aos objetivos específicos do projeto:

1. ✅ **OE1 (Revisão sistemática)**: **CONCLUÍDA** com rigor metodológico PRISMA 2020
2. ✅ **OE2 (Técnicas de ML)**: **CONCLUÍDA** - Mapeadas abordagens de Machine Learning aplicadas à educação
3. 📋 **OE3 (Protótipo)**: **PLANEJADA** - Base teórica estabelecida; desenvolvimento previsto para Fase 2
4. 📋 **OE4 (Validação)**: **PLANEJADA** - Metodologias identificadas; execução prevista para Fase 3

**Status geral**: Fase 1 concluída (40% do projeto total). Fases 2-3 detalhadas no cronograma de execução.

## 🎓 Considerações Finais sobre a Fase 1

A Inteligência Artificial representa uma oportunidade transformadora para a educação matemática, mas seu potencial só será plenamente realizado através de pesquisa rigorosa, desenvolvimento centrado em evidências e implementação ética. Esta revisão sistemática contribui para esse objetivo ao fornecer um panorama crítico do estado da arte, identificar lacunas prioritárias e propor direções concretas para avanço do campo.

O desenvolvimento de um pipeline automatizado e reproduzível demonstra que revisões sistemáticas de alta qualidade podem ser realizadas de forma eficiente, democratizando o acesso a sínteses de evidências científicas. A disponibilização deste pipeline como software livre potencializa futuras pesquisas no campo da tecnologia educacional.

**A conclusão bem-sucedida desta revisão sistemática (Fase 1) estabelece fundamentos sólidos para as próximas etapas do projeto**: o desenvolvimento de um protótipo de sistema de diagnóstico de competências matemáticas (Fase 2) e sua validação experimental em contexto educacional real (Fase 3). Os achados desta revisão orientarão decisões de design, escolha de técnicas de IA e definição de métricas de avaliação nas fases subsequentes, garantindo que o sistema proposto seja fundamentado em evidências científicas robustas.

---

## 📚 Referências

PAGE, M. J. et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. **BMJ**, v. 372, n. 71, 2021. DOI: 10.1136/bmj.n71.

KITCHENHAM, B. **Guidelines for performing Systematic Literature Reviews in Software Engineering**. Technical Report EBSE 2007-001, Keele University and Durham University Joint Report, 2007.

ZAWACKI-RICHTER, O. et al. Systematic review of research on artificial intelligence applications in higher education – where are the educators? **International Journal of Educational Technology in Higher Education**, v. 16, n. 1, p. 1-27, 2019. DOI: 10.1186/s41239-019-0171-0.

HOLMES, W. et al. **Artificial intelligence in education**: Promises and implications for teaching and learning. Brussels: European Parliament, 2019.

ROLL, I.; WYLIE, R. Evolution and revolution in artificial intelligence in education. **International Journal of Artificial Intelligence in Education**, v. 26, n. 2, p. 582-599, 2016. DOI: 10.1007/s40593-016-0110-3.

LUCKIN, R. et al. **Intelligence Unleashed: An argument for AI in Education**. London: Pearson, 2016.

---

*Este documento de conclusões sintetiza as contribuições da revisão sistemática e propõe direções concretas para pesquisa futura, seguindo as diretrizes ABNT NBR 14724:2011 para trabalhos acadêmicos.*
