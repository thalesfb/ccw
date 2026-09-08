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

### 2. Por que esta revisão?

Turmas heterogêneas produzem evidências variadas sobre o desempenho. Técnicas
computacionais podem organizar registros e revelar padrões, mas a interpretação
permanece pedagógica e não pode ser substituída por uma saída algorítmica.

### 3. Perguntas e objetivo

Apresenta quatro perguntas orientadoras sobre técnicas, avaliação, lacunas e
direcionamentos para ferramentas de apoio, além do objetivo geral de mapear
aplicações e derivar uma especificação conceitual.

### 4. O que este trabalho entrega

Resume OE1–OE7: revisão relatada com apoio do PRISMA 2020; categorização de
abordagens e finalidades; análise metodológica; lacunas; pipeline auditável; e
derivação da especificação de protótipo.

### 5. A base conceitual: quatro níveis de interpretação

Distingue desempenho observado, proficiência estimada, competência e
aprendizagem. A mensagem central é que a revisão pode apoiar inferências sobre
registros, mas não observa diretamente todos os processos da aprendizagem.

### 6. Protocolo e escopo

Apresenta PRISMA 2020 como diretriz de relato, PICOS como apoio aos critérios,
as quatro fontes consultadas, os idiomas e o recorte temporal. Registra que as
72 consultas são a composição canônica versionada — 48 em inglês e 24 em
português —, não uma contagem retrospectiva de chamadas HTTP, pois não há log
histórico completo. Também explicita a aceitação de teses e dissertações sob os
mesmos critérios e o uso do score como filtro operacional.

### 7. Do registro bruto à população retida

Mostra as contagens do snapshot: 11.904 identificados; 27 remoções
determinísticas por DOI/URL; 11.877 na triagem; 9.391 excluídos na triagem;
2.486 na elegibilidade; 2.468 excluídos na elegibilidade; 18 retidos
operacionalmente.

### 8. Fluxo PRISMA do snapshot

Incorpora `research/exports/visualizations/prisma_flow.png`, que é a figura
canônica sincronizada com os artefatos públicos.

### 9. Deduplicação: o que foi confirmado

Explica a diferença entre identidade bibliográfica e semelhança de título. As
27 remoções confirmadas são 25 por DOI normalizado e 2 por URL exata. Os 232
excedentes observados apenas por título permanecem candidatos à auditoria
semântica e não foram tratados automaticamente como duplicatas.

### 10. Panorama descritivo dos dados da revisão

Incorpora a distribuição de técnicas. Destaca 6.399 registros com técnica não
especificada, 1.073 com assessment, 863 com IA/inteligência artificial e 771
com machine learning. As categorias podem se sobrepor e não medem qualidade,
eficácia ou apenas os registros retidos.

### 11. Distribuição temporal e fontes

Apresenta a distribuição anual e a cobertura das quatro fontes. As figuras são
descritivas; não sustentam inferências de representatividade, qualidade ou
efeito pedagógico.

### 12. Score de relevância: filtro operacional

Mostra a distribuição do score e o limiar operacional de 4,0. O score organiza
o processamento, mas não é medida de qualidade metodológica, não produz ranking
e não substitui a leitura das fontes primárias.

### 13. População retida e síntese

Dos 18 registros retidos, 17 são candidatos empíricos provisórios e 1 é um
protocolo ou proposta contextual. A síntese empírica considera os 17; o registro
contextual permanece para rastreabilidade e não sustenta resultado empírico.
Predominam tarefas de predição de desempenho e estimativa de proficiência, com
recorrência de modelos supervisionados.

### 14. Apreciação metodológica sem nota global

O MMAT é apresentado por critério, conforme o desenho de cada estudo, usando
Sim, Não ou Não é possível determinar. A apreciação é preliminar e feita por um
único revisor: nove registros tiveram texto primário revisado e oito foram
apreciados com resumo/metadados. Não há média, ranking ou categoria geral de
qualidade; recuperação de fontes, localizadores e adjudicação ainda precisam ser
consolidados.

### 15. O que emerge nos 17 candidatos empíricos

Organiza o padrão dominante em torno de predição de desempenho e estimativa de
proficiência, com recorrência de RF, SVM e redes neurais. A heterogeneidade de
populações, instrumentos, variáveis e métricas limita a comparabilidade entre
estudos.

### 16. O que podemos concluir — e o que não podemos

O snapshot oferece um mapa auditável. A heterogeneidade de populações,
instrumentos, variáveis e métricas impede comparar todos os resultados
diretamente. Acurácia de um artigo não demonstra superioridade geral nem
eficácia pedagógica transferível.

### 17. Lacunas documentadas

Explicabilidade, integração curricular, participação docente, equidade,
reprodutibilidade e validação em contextos diversos aparecem como lacunas. Elas
são convertidas em requisitos de projeto, não apresentadas como evidência de
que uma solução futura será eficaz.

### 18. Da evidência à especificação

Mostra a derivação: evidências da revisão e da fundamentação → lacunas →
requisitos → critérios e protocolo → arquitetura de referência.

### 19. Arquitetura de referência em cinco componentes

Resume a arquitetura de referência em ingestão, preparação, modelagem,
avaliação/explicabilidade e apresentação. A separação favorece testabilidade,
rastreabilidade e substituição controlada de técnicas.

### 20. Reprodutibilidade sem distribuir o SQLite

Apresenta CSV/JSON, BibTeX, manifesto com hashes e relatórios PNG/HTML como
artefatos públicos de reprodução. A bibliografia derivada do pipeline permanece
separada das referências teóricas, pedagógicas, metodológicas e técnicas da
fundamentação.

### 21. Próximos passos científicos

Indica a consolidação da recuperação das fontes e da adjudicação do MMAT, a
revisão das lacunas e da especificação conceitual e a necessidade de novo
protocolo e autorização para qualquer validação experimental. A revisão
sistematizada fundamenta decisões futuras, mas não substitui esse protocolo.

### 22. Obrigado

Encerramento para perguntas e discussão, mantendo título, autor, instituição,
snapshot e recorte temporal.

## Regra de referência

O deck não usa IDs operacionais de artigos como se fossem citações para o
leitor. Quando uma fonte é necessária na exposição, ela deve ser identificada
por autor e ano ou pela referência bibliográfica correspondente no TCC. As
referências teóricas e pedagógicas permanecem externas ao conjunto derivado do
pipeline e não são removidas por uma atualização do snapshot.
