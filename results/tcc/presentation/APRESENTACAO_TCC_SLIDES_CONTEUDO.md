# Apresentação do TCC — conteúdo dos slides

## Identidade

- **Título:** Ensino Personalizado de Matemática: Oportunidades e Técnicas Computacionais
- **Formato:** PowerPoint editável, 16:9
- **Autor:** Thales Ferreira Batista
- **Orientação:** Prof. Dr. Rafael Zanin; Prof. Dr. Manassés Ribeiro
- **Instituição:** IFC — Campus Videira
- **Snapshot:** 03/09/2026
- **Recorte temporal:** 2015–2026, com data de corte em 31/08/2026

O roteiro segue a progressão usada na apresentação do PTC — problema, método,
resultados, implicações e encerramento —, mas o conteúdo abaixo é derivado do
TCC e do snapshot atual. O deck não reproduz números históricos nem transforma
o protótipo conceitual em aplicação implementada.

## Sequência dos slides

### 1. Ensino Personalizado de Matemática

Subtítulo: oportunidades e técnicas computacionais. Apresenta a revisão
sistemática e a especificação conceitual de protótipo, com autor, orientação,
instituição, data do snapshot e recorte temporal.

### 2. O desafio fundamental: diagnóstico personalizado com evidências

Apresenta o problema em duas colunas: a heterogeneidade das turmas, o tempo
docente, o risco de ensino genérico e a fragmentação da literatura. O TCC
organiza evidências para apoiar a interpretação, sem substituir a decisão
pedagógica.

### 3. Objetivo geral

Apresenta ação central, finalidade e escopo. O objetivo é mapear e analisar
aplicações computacionais em educação matemática e identificar tendências,
lacunas e oportunidades para uma especificação conceitual, sem apresentá-la
como protótipo funcional ou avaliação de eficácia.

### 4. Quatro perguntas fundamentam a busca por clareza

Apresenta quatro perguntas orientadoras sobre técnicas, avaliação, lacunas e
direcionamentos para ferramentas de apoio. Elas organizam a análise dos
achados do TCC.

### 5. Missão: mapear o terreno com rigor e transparência

Relaciona o propósito da revisão à diretriz PRISMA 2020, explicitando que o
protocolo organiza identificação, seleção e relato. A lâmina também registra
o limite interpretativo: desempenho observado não equivale automaticamente a
aprendizagem.

### 6. A base conceitual: níveis de interpretação

Distingue o indicador de desempenho observado, a probabilidade preditiva
condicionada ao modelo e aos dados, a proficiência estimada, a competência e a
aprendizagem. A mensagem central é que uma probabilidade preditiva é uma saída
para um alvo definido, não uma medida direta de proficiência, competência,
aprendizagem ou eficácia; a revisão apoia inferências sobre registros, mas não
observa diretamente todos os processos da aprendizagem.

### 7. Objetivos específicos

Apresenta o percurso OE1–OE7 em fluxo visual: revisão, identificação,
classificação, análise, mapeamento de lacunas, auditoria e derivação de
requisitos, avaliação e arquitetura conceitual.

### 8. Estratégia de busca: três camadas

Mostra as camadas matemática, técnicas e educação e as 72 consultas canônicas
versionadas — 48 em inglês e 24 em português —. A composição não é contagem
retrospectiva de chamadas HTTP.

### 9. Quatro fontes de indexação complementares

Apresenta a distribuição do snapshot após a remoção determinística: Semantic
Scholar (1.931 registros), OpenAlex (3.057), Crossref (5.049) e CORE (1.840).
Os valores somam 11.877 registros na triagem, não são contagens independentes
de estudos retidos e não devem ser somados ao total identificado de 11.904.
Teses e dissertações permanecem elegíveis quando atendem aos mesmos critérios
do protocolo.

### 10. O funil da descoberta

Mostra as contagens do snapshot: 11.904 identificados; 27 remoções
determinísticas por DOI/URL; 11.877 na triagem; 9.391 excluídos na triagem;
2.486 na elegibilidade; 2.468 excluídos na elegibilidade; 18 retidos
operacionalmente.

### 11. Fluxo PRISMA do snapshot

Incorpora `research/exports/visualizations/prisma_flow.png`, que é a figura
canônica sincronizada com os artefatos públicos.

### 12. Deduplicação: o que foi confirmado

Explica a diferença entre identidade bibliográfica e semelhança de título. As
27 remoções confirmadas são 25 por DOI normalizado e 2 por URL exata. Os 232
excedentes observados apenas por título permanecem candidatos à auditoria
semântica e não foram tratados automaticamente como duplicatas.

### 13. A distribuição anual concentra registros nos anos recentes

Incorpora a distribuição anual e contextualiza a concentração de registros nos
anos mais recentes do recorte 2015–2026. A leitura é descritiva e não infere
representatividade, causalidade ou qualidade.

### 14. Técnicas observadas no conjunto pós-deduplicação

Destaque, no conjunto pós-deduplicação (n=11.877), para 6.399 registros com
técnica não especificada, 1.073 com assessment,
863 com IA/inteligência artificial, 771 com machine learning e 345 com análise
preditiva. As categorias podem se sobrepor e não medem qualidade, eficácia ou
predominância entre os estudos retidos.

### 15. Um filtro operacional antes da leitura em profundidade

Mostra a distribuição do score e o limiar operacional de 4,0. O score organiza
o processamento, mas não é medida de qualidade metodológica, não produz ranking
e não substitui a leitura das fontes primárias.

### 16. População retida: dois estratos de leitura

Dos 18 registros retidos, 17 são candidatos empíricos provisórios e 1 é um
protocolo ou proposta contextual. A síntese empírica considera os 17; o registro
contextual permanece para rastreabilidade e não sustenta resultado empírico.
A síntese empírica preliminar aponta recorrência de tarefas de predição de
desempenho e estimativa de proficiência, com uso recorrente de modelos
supervisionados.

### 17. Nosso filtro de qualidade: critérios, não uma nota global

O MMAT é apresentado por critério, conforme o desenho de cada estudo, usando
Sim, Não ou Não é possível determinar. A apreciação é preliminar e feita por um
único revisor: nove registros tiveram texto primário revisado e oito foram
apreciados com resumo/metadados. Não há média, ranking ou categoria geral de
qualidade; recuperação de fontes, localizadores e adjudicação ainda precisam ser
consolidados.

### 18. O que emerge entre os candidatos empíricos

Organiza as recorrências em torno de predição de desempenho e estimativa de
proficiência, com uso de RF, SVM e redes neurais. A heterogeneidade de
populações, instrumentos, variáveis e métricas limita a comparabilidade entre
estudos.

### 19. O que podemos concluir — e o que permanece aberto

O snapshot oferece um mapa auditável. A heterogeneidade de populações,
instrumentos, variáveis e métricas impede comparar todos os resultados
diretamente. Acurácia de um artigo não demonstra superioridade geral nem
eficácia pedagógica transferível.

### 20. As lacunas que orientam a especificação

Explicabilidade, integração curricular, participação docente, equidade,
reprodutibilidade e validação em contextos diversos aparecem como lacunas. Elas
são convertidas em requisitos de projeto, não apresentadas como evidência de
que uma solução futura será eficaz.

### 21. Da evidência à especificação — sem saltar para a implementação

Mostra a derivação visual: evidências da revisão e da fundamentação → lacunas →
requisitos. A entrega é uma especificação técnica e pedagógica auditável, com
protocolo e arquitetura de referência; não é aplicação funcional nem validação
com participantes.

### 22. Arquitetura de referência: da fonte à decisão docente

Resume a arquitetura de referência em ingestão, preparação, modelagem,
avaliação/explicabilidade e apresentação. A separação favorece testabilidade,
rastreabilidade e substituição controlada de técnicas.

### 23. Ciência aberta como trilha de auditoria

Apresenta CSV/JSON, BibTeX, manifesto com hashes e relatórios PNG/HTML como
artefatos públicos de reprodução. A bibliografia derivada do pipeline permanece
separada das referências teóricas, pedagógicas, metodológicas e técnicas da
fundamentação.

### 24. Próximos passos científicos

Indica a consolidação da recuperação das fontes e da adjudicação do MMAT, a
revisão das lacunas e da especificação conceitual e a necessidade de novo
protocolo e autorização para qualquer validação experimental. A revisão
sistematizada fundamenta decisões futuras, mas não substitui esse protocolo.

### 25. Obrigado

Encerramento para perguntas e discussão, mantendo título, autor, instituição,
snapshot e recorte temporal.

## Regra de referência

O deck não usa IDs operacionais de artigos como se fossem citações para o
leitor. Quando uma fonte é necessária na exposição, ela deve ser identificada
por autor e ano ou pela referência bibliográfica correspondente no TCC. As
referências teóricas e pedagógicas permanecem externas ao conjunto derivado do
pipeline e não são removidas por uma atualização do snapshot.
