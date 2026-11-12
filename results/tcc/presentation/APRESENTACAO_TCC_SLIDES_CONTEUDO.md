# Apresentação do TCC — conteúdo dos slides

> **Rascunho histórico — não usar na defesa.** Os números deste storyboard
> antecedem a reconciliação de 31/10/2026. O corte 4,0 e a seleção histórica
> de 15 estudos permanecem inalterados. A revisão da apresentação para a
> defesa permanece suspensa; esta atualização não modifica o conjunto de estudos.

## Identidade

- **Título:** Ensino Personalizado de Matemática: Oportunidades e Técnicas Computacionais
- **Papel:** storyboard de conteúdo para o deck canônico Slidev de 25 slides; não é o export PPTX editável paralelo de 19 slides
- **Autor:** Thales Ferreira Batista
- **Orientação:** Prof. Dr. Rafael Zanin; Prof. Dr. Manassés Ribeiro
- **Instituição:** IFC — Campus Videira
- **Atualização da sequência:** 12/11/2026
- **Recorte temporal:** 2015–2026, com data de corte em 31/08/2026

O roteiro organiza a exposição do TCC em problema, método, resultados,
implicações e encerramento. O conteúdo abaixo é derivado do manuscrito e do
recorte versionado atual. O deck não reproduz números históricos nem transforma o
protótipo conceitual em aplicação implementada.

## Sequência dos slides

A sequência de 11/2026 dá mais peso aos resultados de cada objetivo e às
regras propostas, e menos ao pipeline de coleta. Gráficos de etiquetas de
técnicas de todos os registros e o histograma de relevância saíram do deck,
porque não descreviam os 15 estudos.

### 1. Ensino Personalizado de Matemática

Capa com título, autor, orientação, instituição, data de corte da busca e
estado do material.

### 2. O problema: ler a aprendizagem em turmas heterogêneas

A média da turma não mostra onde cada estudante está nem quanta evidência
sustenta essa leitura. Técnicas computacionais podem organizar evidências,
com o professor responsável pela interpretação.

### 3. O que o trabalho propõe

Objetivo geral do TCC, com objeto (técnicas aplicadas à educação matemática,
2015–2026), finalidade (indícios de desempenho e de incerteza por habilidade)
e escopo (revisão e especificação documental, sem protótipo validado).

### 4. Problema de pesquisa

Como estruturar a especificação a partir da literatura, desdobrado em quatro
perguntas, cada uma ligada a um objetivo específico (OE1–OE4).

### 5. Cinco níveis que uma saída não deve confundir

Desempenho observado, probabilidade preditiva, proficiência estimada,
competência e aprendizagem, com base em National Research Council (2001),
OECD (2023) e BNCC (2018).

### 6. Acertar ou errar não revela o tipo de erro

Duval (2009) e Brousseau (2008), com o exemplo de 2x + 5 = 15. A
especificação organiza indícios por habilidade; o tipo de erro e o obstáculo
ficam com o professor (F06).

### 7. Quatro objetivos, quatro produtos

OE1 a OE4 e o produto de cada um: tipologia, lacunas de relato, 26 grupos de
requisitos com regra de modelo, e protocolo de avaliação.

### 8. Revisão sistemática: busca em três camadas

72 consultas (48 em inglês e 24 em português), quatro bases, relato com o
PRISMA 2020 e apreciação com o MMAT 2018.

### 9. Quatro bases de indexação complementares

Semantic Scholar, OpenAlex, Crossref e CORE, com 11.875 registros após a
remoção de 29 duplicatas.

### 10. Fluxo da seleção

De 11.904 registros a 18 na lista de leitura. Após uma exclusão no resumo,
17 relatórios foram procurados, dois não foram recuperados (Sokkhey e Zeng) e 15 foram avaliados
em texto completo; um protocolo foi excluído. A seleção histórica permanece com 15 estudos.

### 11. Fluxograma PRISMA

Fluxograma 1 do TCC, com a distinção entre priorização por relevância e
avaliação de elegibilidade.

### 12. O corte 4,0 é heurístico

A exploração abaixo do corte encontrou registros classificados como elegíveis
(13 de 45, 29 de 54 e 5 de 30). O corpus é um recorte, não um censo; a
limitação é declarada sem estimativa de perda.

### 13. O destino dos 18 registros

15 estudos empíricos (Sokkhey sem cópia verificável), Zeng não recuperado,
uma exclusão após resumo e um protocolo excluído.

### 14. MMAT preliminar

Perguntas S1 e S2, legenda Y/N/CT e estado preliminar: estudos 5 e 7 em
categoria 3 operacional, estudo 8 em categoria 4 adaptada, sem escore
agregado; respostas produzidas por IA e em conferência pelo autor.

### 15. Resultado do OE1: para que as técnicas são usadas

Predição/classificação (8), personalização ou STI (3), intervenção didática
(2), modelagem cognitiva (1) e integração curricular (1), com exemplos de
técnicas. As categorias não são homogêneas.

### 16. Resultado do OE2: o que falta nos relatos

Respostas CT por categoria e critério do MMAT. CT predomina em
representatividade, medidas, completude, controle e análise; a especificação
passa a exigir alvo, população, transformações e avaliação descritos.

### 17. Resultado do OE2: três eixos de risco viraram requisitos

Técnico (R20), pedagógico (R02) e ético (R04). A análise por subgrupos (R23)
não foi operacionalizada.

### 18. O que a evidência permite especificar

Síntese dos 15 estudos provisórios: alvo explícito, modelo simples como
referência e incerteza visível.

### 19. O que o TCC entrega, e o que não entrega

Entrega um mapa auditável e uma especificação; não entrega evidência de
eficácia. Limitações: revisor único com apoio de IA, 14 de 15 textos
recuperados, sensibilidade abaixo do corte e ausência de participantes.

### 20. Exemplos de limitações nos estudos consultados

Quatro exemplos localizados nos textos primários (He, Villegas-Ch, Nyantah e
Echeveria), sem estimativa de prevalência.

### 21. Resultado do OE3: da evidência aos requisitos

Cadeia revisão → requisitos (26 grupos) → funções F01–F07 → aceitação →
protocolo, com os exemplos R02 e R20.

### 22. Arquitetura e saída para o professor

Arquitetura de referência e tela fictícia: 4 de 6 acertos, intervalo de
Wilson de 0,30 a 0,90, média das probabilidades 0,65 sem intervalo próprio.

### 23. Regras fixadas antes de qualquer dado real

Regra de escolha de modelo (OE3) e regras de avaliação da especificação
(OE4), que verificam rastreabilidade, consistência arquitetural,
correspondência conceitual e condições de viabilidade. Nenhuma foi aplicada.

### 24. Conclusão e próximos passos

Quatro contribuições ligadas aos objetivos e próximos passos: conferir o
MMAT, aplicar o protocolo após parecer ético, testar a regra de modelo em
dados reais e codificar itens por registro de representação.

### 25. Obrigado

Encerramento para perguntas, com QR do repositório e link do TCC.

## Regra de referência

O deck não usa IDs operacionais de artigos como se fossem citações para o
leitor. Quando uma fonte é necessária na exposição, ela deve ser identificada
por autor e ano ou pela referência bibliográfica correspondente no TCC. As
referências teóricas e pedagógicas permanecem externas ao conjunto derivado do
fluxo automatizado e não são removidas por uma atualização do recorte versionado.
