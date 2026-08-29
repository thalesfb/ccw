# Registro da revisão do TCC

A revisão metodológica consolidada foi realizada pela issue #5 e pelo PR #6. A revisão editorial e normativa subsequente é acompanhada pelo PR #23, que preserva as decisões metodológicas já validadas e ajusta a forma acadêmica do texto final.

## Decisões metodológicas preservadas

- A revisão sistemática da literatura, a avaliação metodológica dos estudos incluídos e a especificação conceitual do protótipo constituem as entregas concluídas do TCC.
- A implementação funcional, o treinamento em uma base definitiva e a validação empírica com participantes permanecem fora do escopo executado e são tratados como continuidade da pesquisa.
- Alegações sem artefatos reproduzíveis sobre protótipo funcional, experimentos, validação escolar e defesa não devem ser introduzidas.
- O PRISMA 2020 é apresentado como diretriz de relato.
- O PRISMA-P é apresentado como orientação para protocolos; não se declara conformidade integral porque não houve registro prospectivo.
- O limiar usado na elegibilidade representa relevância temática e não qualidade metodológica.
- O MMAT é reportado por Q1--Q5, sem nota geral, média, ranking ou categoria de qualidade e sem ser reclassificado como medida global de certeza da evidência.
- A reutilização do cache é explicada como métrica dependente da execução; os valores conflitantes de 63% e 92% permanecem excluídos por não constituírem uma medida estável e versionada da mesma execução.
- Desempenho observado, proficiência estimada, competência e aprendizagem são tratados como conceitos relacionados, mas distintos.

## Decisões editoriais da revisão atual

- A Seção 1.5 descreve a estrutura do trabalho em prosa contínua, sem lista de capítulos.
- O capítulo de cronologia da execução foi removido da versão final; o TCC textual passa a ser organizado em sete capítulos.
- Títulos de figuras são apresentados acima das ilustrações e as fontes permanecem abaixo, conforme o padrão institucional adotado para o documento.
- O Capítulo 5 mantém suas seções temáticas, mas apresenta princípios, requisitos, critérios de dados, avaliação e arquitetura em prosa acadêmica, sem estrutura de checklist.
- Listas são preservadas quando cumprem função metodológica de precisão e reprodutibilidade, como critérios de inclusão e exclusão, deduplicação, avaliação MMAT e etapas de derivação da especificação. Listas meramente expositivas são preferencialmente convertidas em prosa.
- O Capítulo 6 prioriza interpretação e discussão integrada dos achados, reduzindo a repetição descritiva dos capítulos anteriores.
- A conclusão apresenta contribuições e limitações em prosa e delimita o alcance dos resultados sem alegações defensivas de eficácia não demonstrada.
- O apêndice PRISMA 2020 utiliza a estrutura atual do checklist, incluindo seus subitens, e registra explicitamente itens atendidos, parciais, não realizados e não aplicáveis. Ele não declara conformidade integral.
- Termos técnicos em português são priorizados quando existe equivalente consagrado e natural no contexto científico, como `aprendizado de máquina`, `analítica da aprendizagem`, `mineração de dados educacionais`, `floresta aleatória`, `devolutiva pedagógica` e `fluxo automatizado`.
- Quando um termo estrangeiro é mantido por utilidade técnica, identificação terminológica ou ausência de tradução adequada, preserva-se a convenção de destaque adotada no documento e pelo contexto institucional, sem promover uma substituição visual automática.
- O título atual permanece no fonte até discussão com a orientação. A revisão registra propostas mais aderentes ao escopo final, mas não altera o título silenciosamente.

## Referência institucional e normativa

A normalização deve observar, em conjunto:

1. a página do curso de Ciência da Computação do IFC Campus Videira, que publica modelos LaTeX para PTC, TC tradicional e TC de desenvolvimento;
2. o modelo institucional divulgado pelo Sistema Integrado de Bibliotecas do IFC, cuja página informa que os trabalhos de conclusão devem observar o template institucional conforme a Portaria Normativa nº 6/2022 do CONSEPE;
3. as edições vigentes das normas de apresentação de trabalhos acadêmicos, citações, referências, resumos e sumário disponibilizadas pelos serviços institucionais de normalização;
4. as orientações específicas da orientação e da banca quando definirem escolhas editoriais compatíveis com as normas e o template do curso.

O repositório contém uma customização LaTeX institucional criada em 2017. Ela foi mantida para evitar uma troca silenciosa que alterasse capa, folha de rosto, paginação e demais elementos institucionais sem uma comparação controlada. O documento compila automaticamente e o PDF é disponibilizado como artefato do CI. Antes da entrega definitiva, o resultado renderizado deve ser comparado com o modelo LaTeX de TC aplicável ao enquadramento definido pelo curso e com os elementos institucionais obrigatórios.

## Contrato de validação

Pull requests que alteram o TCC devem:

1. verificar erros de whitespace no diff contra a `main`;
2. compilar os fontes Python;
3. executar os testes do MMAT e dos artefatos acadêmicos;
4. executar os testes específicos dos pontos do retorno do orientador e da revisão editorial;
5. compilar o documento LaTeX em modo de interrupção no primeiro erro;
6. publicar o PDF e o log de compilação como artefatos;
7. registrar a inspeção visual das páginas afetadas antes de considerar a revisão concluída.

Os testes de regressão verificam, entre outros pontos:

- ausência de comandos LaTeX de ênfase duplicados;
- ausência das taxas conflitantes de cache no texto do TCC;
- diferenciação entre PRISMA-P e PRISMA 2020;
- explicação de TF-IDF e similaridade do cosseno;
- análise textual antes da tabela longa da síntese;
- ausência de identificadores técnicos longos em forma não quebrável;
- ausência de alegações de etapas ainda não realizadas;
- distinção entre aprendizagem, competência, proficiência e desempenho;
- MMAT sem agregação numérica e com origem dos julgamentos registrada;
- padronização das fontes elaboradas pelo autor;
- retirada do capítulo de cronologia da versão final;
- estrutura da Seção 1.5 em prosa;
- Capítulo 5 sem listas de especificação;
- legendas das figuras do Capítulo 4 acima das ilustrações;
- checklist PRISMA atual, sem resíduos do PTC nem declaração de conformidade integral;
- preferência por equivalentes técnicos em português;
- preservação da convenção de destaque quando termos estrangeiros permanecem necessários.

## Continuidade após o TCC documental

Uma etapa posterior poderá comparar fontes de dados candidatas, definir o problema computacional, estabelecer modelos de referência, selecionar a arquitetura mínima e implementar um protótipo reproduzível. Nenhuma tecnologia ou modelo deve ser considerado escolhido apenas por ter aparecido com maior frequência na literatura, e qualquer alegação de eficácia pedagógica dependerá de desenho empírico próprio e validação adequada.
