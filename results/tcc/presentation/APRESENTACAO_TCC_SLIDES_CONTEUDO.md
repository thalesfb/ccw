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

### 2. O problema de pesquisa

Turmas heterogêneas produzem evidências variadas sobre o desempenho. Técnicas
computacionais podem organizar registros e revelar padrões, mas a interpretação
permanece pedagógica e não pode ser substituída por uma saída algorítmica.

### 3. Questão e objetivo

Apresenta o problema de pesquisa, o objetivo geral e quatro perguntas
orientadoras sobre técnicas, avaliação, lacunas e requisitos para uma ferramenta
de apoio.

### 4. Objetivos específicos

Resume OE1–OE7: revisão relatada com apoio do PRISMA 2020; categorização de
abordagens e finalidades; análise metodológica; lacunas; pipeline auditável; e
derivação da especificação de protótipo.

### 5. A base conceitual: quatro níveis de interpretação

Distingue desempenho observado, proficiência estimada, competência e
aprendizagem. A mensagem central é que a revisão pode apoiar inferências sobre
registros, mas não observa diretamente todos os processos da aprendizagem.

### 6. Desenho metodológico

Apresenta PRISMA 2020 como diretriz de relato, PICOS como apoio aos critérios,
as quatro fontes consultadas, os idiomas e o recorte temporal. Registra que as
72 consultas são a composição canônica versionada — 48 em inglês e 24 em
português —, não uma contagem retrospectiva de chamadas HTTP, pois não há log
histórico completo.

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

### 10. Panorama descritivo do snapshot

Incorpora a distribuição de técnicas. Destaca 6.399 registros com técnica não
especificada, 1.073 com assessment, 863 com IA/inteligência artificial e 771
com machine learning. As categorias podem se sobrepor e não medem qualidade,
eficácia ou apenas os registros retidos.

### 11. Distribuição temporal e fontes

Apresenta a distribuição anual e a cobertura das quatro fontes. As figuras são
descritivas; não sustentam inferências de representatividade, qualidade ou
efeito pedagógico.

### 12. População retida e síntese empírica

Dos 18 registros retidos, 17 são candidatos empíricos provisórios e 1 é um
protocolo ou proposta contextual. A síntese empírica considera os 17; o registro
contextual permanece para rastreabilidade e não sustenta resultado empírico.
Predominam tarefas de predição de desempenho e estimativa de proficiência, com
recorrência de modelos supervisionados.

### 13. Apreciação metodológica pelo MMAT 2018

O MMAT é apresentado por critério, conforme o desenho de cada estudo, usando
Sim, Não ou Não é possível determinar. A apreciação é preliminar e feita por um
único revisor: nove registros tiveram texto primário revisado e oito foram
apreciados com resumo/metadados. Não há média, ranking ou categoria geral de
qualidade; recuperação de fontes, localizadores e adjudicação ainda precisam ser
consolidados.

### 14. O que a síntese sustenta

O snapshot oferece um mapa auditável. A heterogeneidade de populações,
instrumentos, variáveis e métricas impede comparar todos os resultados
diretamente. Acurácia de um artigo não demonstra superioridade geral nem
eficácia pedagógica transferível.

### 15. Lacunas documentadas

Explicabilidade, integração curricular, participação docente, equidade,
reprodutibilidade e validação em contextos diversos aparecem como lacunas. Elas
são convertidas em requisitos de projeto, não apresentadas como evidência de
que uma solução futura será eficaz.

### 16. Da evidência à especificação

Mostra a derivação: evidências da revisão e da fundamentação → lacunas →
requisitos → critérios e protocolo → arquitetura de referência.

### 17. Especificação conceitual do protótipo

Incorpora a arquitetura de referência do TCC e resume ingestão, preparação,
modelagem, avaliação/explicabilidade e apresentação. A especificação não é uma
aplicação funcional, não usa uma base definitiva e não possui métricas próprias
ou validação com participantes.

### 18. Contribuições e limites

Contribuições: síntese estruturada, pipeline versionado, separação entre
relevância e avaliação metodológica e especificação auditável. Limites: um
pesquisador, cobertura desigual das fontes, apreciação MMAT preliminar, ausência
de aplicação funcional e de eficácia pedagógica própria.

### 19. Obrigado

Encerramento para perguntas e discussão, mantendo título, autor, instituição,
snapshot e recorte temporal.

## Regra de referência

O deck não usa IDs operacionais de artigos como se fossem citações para o
leitor. Quando uma fonte é necessária na exposição, ela deve ser identificada
por autor e ano ou pela referência bibliográfica correspondente no TCC. As
referências teóricas e pedagógicas permanecem externas ao conjunto derivado do
pipeline e não são removidas por uma atualização do snapshot.
