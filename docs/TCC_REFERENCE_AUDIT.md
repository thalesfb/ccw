# Auditoria das referências do TCC

## Finalidade

Este documento registra a validação bibliográfica e a adequação de uso das referências empregadas no TCC. A auditoria separa quatro perguntas que não devem ser confundidas:

1. a publicação existe e pode ser identificada por uma fonte canônica?
2. os metadados bibliográficos estão completos e corretos?
3. o desenho e a qualidade editorial permitem usar a publicação para a finalidade pretendida?
4. a afirmação do TCC é efetivamente sustentada pelo escopo da fonte?

A planilha canônica está em `research/data/reference_audit.csv`. Ela deve ser atualizada sempre que uma referência, citação ou afirmação for alterada.

## Critérios de decisão

- `verified`: existência, metadados e uso considerados adequados;
- `metadata_fix`: publicação real, mas a entrada BibTeX requer correção;
- `scope_limited`: publicação real, porém sustenta apenas uma parte da afirmação ou deve ser usada como evidência específica;
- `editorial_caution`: publicação localizada, mas com qualidade editorial, transparência metodológica ou relevância insuficiente para ser fonte central;
- `unused`: publicação real que não deve ser usada na redação atual;
- `replace`: a citação deve ser substituída por uma fonte mais canônica para a afirmação.

## Resultado consolidado

### Diretrizes metodológicas

PRISMA 2020, PRISMA-P 2015 e o Cochrane Handbook foram confirmados como fontes reais e adequadas, desde que o texto preserve a diferença entre diretriz de relato, protocolo e método de condução. O MMAT também é real, mas a citação deve priorizar o artigo revisado por pares de Hong et al. com DOI `10.3233/EFI-180221`, mantendo o manual apenas como documento operacional complementar.

### Fundamentação pedagógica

BNCC, National Research Council, OCDE/PISA, Piaget, Vygotsky, Ausubel, Wood, Bruner e Ross, Black e Wiliam e Hattie e Timperley foram confirmados. A auditoria preserva as seguintes restrições:

- Piaget fundamenta construção ativa do conhecimento, mas não deve receber sozinho todas as implicações didáticas específicas da educação matemática;
- Vygotsky fundamenta a Zona de Desenvolvimento Proximal;
- `scaffolding` deve ser atribuído a Wood, Bruner e Ross;
- o framework do PISA fundamenta construtos e desenho da avaliação; os descritores dos níveis devem usar também o relatório de resultados;
- desempenho observado, proficiência estimada, competência e aprendizagem permanecem conceitos relacionados, porém não intercambiáveis.

### Estudos incluídos na revisão

Os 17 registros incluídos foram localizados bibliograficamente. Isso não significa que todos possuam o mesmo peso de evidência. A matriz registra separadamente existência, correções de metadados e restrições de uso.

Correções prioritárias:

- `Implementation2025_000`: incluir Hendra Tjahyadi e Krismon N. L. Tude e substituir URL de indexador pelo DOI;
- `Machine2019_007`: preencher o nome dos anais da IEEE EDUCON 2019;
- `Computational2017_008`: classificar como tese de doutorado, não artigo;
- `Data2020_011`: classificar como capítulo de livro, não artigo;
- URLs de Semantic Scholar e OpenAlex devem ser tratadas como proveniência da coleta, não como endereço bibliográfico canônico;
- `Assessing2024_015` permanece na rastreabilidade da revisão, mas não deve ser fonte central para alegações de eficácia de aprendizagem adaptativa sem avaliação adicional do texto completo e do veículo.

## Política de fontes

1. DOI ou página oficial da editora é a URL bibliográfica preferencial.
2. OpenAlex, Semantic Scholar, Crossref e CORE registram a proveniência da descoberta, não substituem a fonte de publicação.
3. Definições centrais devem priorizar obras canônicas, documentos normativos ou revisões robustas.
4. Estudos empíricos recentes devem apoiar resultados específicos, não substituir fundamentos teóricos.
5. Uma referência incluída na revisão pode permanecer na síntese mesmo com limitações, desde que essas limitações sejam registradas e consideradas na interpretação.
6. Nenhuma referência será removida silenciosamente da trilha da revisão sistemática.

## Matriz de afirmações prioritárias

| Afirmação no TCC | Fonte principal | Escopo aceito |
|---|---|---|
| PRISMA orienta o relato transparente da revisão | Page et al., 2021 | relato da revisão, não garantia de qualidade |
| PRISMA-P orienta protocolos | Moher et al., 2015 | protocolo; conformidade parcial deve ser declarada |
| MMAT permite avaliar desenhos heterogêneos | Hong et al., 2018 | avaliação por critérios, sem escore agregado |
| avaliação produz inferências a partir de evidências | NRC, 2001 | distinção entre observação e construto |
| competência matemática envolve mobilização integrada | BNCC, 2018 | definição curricular brasileira |
| proficiência é estimada em escala | OECD, 2023 | interpretação dependente do modelo de mensuração |
| ZDP descreve atuação autônoma e mediada | Vygotsky, 1978 | mediação e desenvolvimento proximal |
| scaffolding é suporte temporário | Wood, Bruner e Ross, 1976 | suporte ajustado e retirada gradual |
| avaliação formativa orienta os próximos passos | Black e Wiliam, 1998 | uso de evidências para ajustar ensino e estudo |
| feedback deve esclarecer objetivo, estado e próximos passos | Hattie e Timperley, 2007 | estrutura e efetividade do feedback |
| EDM e Learning Analytics apoiam análise educacional | Romero e Ventura, 2020 | conceitos, técnicas e limitações |
| ITS possuem modelos de estudante e mecanismos adaptativos | Mousavinasab et al., 2021 | características e métodos de avaliação |

## Reexecução futura da revisão sistemática

O conjunto atual deve ser preservado como `baseline` fechado, com data, consultas, critérios, resultados e artefatos. Uma atualização futura será executada como revisão de atualização, não como substituição silenciosa:

1. congelar o estado atual e gerar manifesto com hashes;
2. versionar APIs, consultas, datas e parâmetros;
3. executar busca apenas para o intervalo posterior à busca original, com sobreposição de segurança;
4. deduplicar contra o corpus congelado;
5. produzir relatório de estudos novos, removidos e alterados;
6. avaliar se as novas evidências modificam decisões do protótipo;
7. atualizar o TCC somente quando a comparação estiver documentada.

A rerrodada não é requisito para iniciar o protótipo. Ela deve ocorrer após a consolidação dos dados e do desenho experimental, evitando que uma busca mutável comprometa o prazo e a rastreabilidade da etapa já concluída.
