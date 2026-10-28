# Revisão editorial e consistência do MMAT — 28/10/2026

## Escopo

Revisão dos sete capítulos do TCC, resumo em português e inglês, quadro de rastreabilidade, apêndice PRISMA e tabelas MMAT importadas. O anexo de modelo está desativado no documento principal. A revisão é editorial e de consistência entre artefatos; não substitui a apreciação científica das fontes nem encerra as pendências metodológicas.

## Correções

- Retirada da introdução a discussão do registro de Uskov et al. (2019), excluído por escopo. A exclusão permanece documentada na metodologia e no quadro dos 18 registros preliminares; não se alterou o fluxo de seleção.
- Substituição de “coortes” por grupos de estudantes e explicitação dos anos 2021 e 2025 na comparação de Xia et al. (2026). São grupos de períodos distintos, não os mesmos estudantes acompanhados por quatro anos. Mantida a limitação de confundimento temporal.
- Tradução das 30 justificativas dos seis componentes MMAT para português, na fonte CSV que gera o quadro e a página HTML. Preservados IDs, categorias, respostas Y/N/CT, localizadores e estado provisório. Os títulos das seções usadas como localizadores permanecem no idioma do artigo para permitir a localização.
- Categorias metodológicas no HTML apresentadas em português, em vez dos códigos internos. Estados pendentes e não avaliados permanecem explícitos.
- Substituição de anglicismos evitáveis por fluxo automatizado, lista de verificação, retorno pedagógico, modelo de referência, comparação de modelos e caderno computacional interativo. Nomes oficiais de instrumentos, métodos, bases, formatos e consultas de busca foram preservados quando necessários à identificação/reprodução.
- Esclarecimento de seleção de atributos por avaliação de subconjuntos, de modelo que combina redes neurais e lógica difusa e de comparação nos mesmos participantes. Substituição de “basal” por “inicial”.
- Remoção de orientação de diagramação que aparecia indevidamente no capítulo do protótipo. A futura avaliação com dados reais foi distinguida da implementação exploratória já existente e dos seus testes sintéticos.
- Localizadores do apêndice PRISMA atualizados para a seção existente, mediante referência automática. Tempo verbal da abertura do resumo inglês alinhado ao português.

## Situação da classificação MMAT

O HTML atual (`mmat_current.html`) corresponde ao gerador e às fontes versionadas. A página `mmat_visualization.html` é histórica e usa outro conjunto de 17 registros. A navegação principal aponta para a página atual. Não foi confirmada nesta revisão a URL que o leitor consultou nem o estado efetivamente publicado no servidor.

O registro atual reúne 18 itens: 15 estudos empíricos provisórios e três disposições distintas (exclusão após resumo, relatório não recuperado e protocolo excluído). Destes 15 estudos, 14 têm S1/S2 e 11 têm Q1–Q5 apreciados. Por isso, o quadro principal MMAT do TCC tem 14 linhas e não 18; sua cobertura não deve ser confundida com o tamanho do corpus. Não há nota global ou ranking de qualidade.

| Estudo | Pendência documental/metodológica preservada |
|---|---|
| Zhang, Zhu e Feng (2025), registro 5 | Tamanho amostral, seleção e alocação não estabelecidos; a descrição inclui simulação. Categoria pendente. |
| Xiaohui Zhang (2023), registro 7 | Formação/alocação dos grupos não estabelecida; não há decisão entre categoria randomizada e não randomizada. |
| Nyantah et al. (2025), registro 14 | O artigo descreve alocação aleatória em uma passagem e desenho sem atribuição aleatória em outra. Categoria pendente. |
| MacLellan (2017), registro 8 | Unidade de apreciação entre modelos/simulações e estudos com estudantes ainda não definida. Sem S1/S2 ou Q1–Q5; não somar suas bases distintas. |

As justificativas e localizadores estão em `research/data/mmat_reassessment_current.csv`. Categorizar esses estudos exige resolver a ambiguidade metodológica, não preencher lacunas por conveniência editorial. O relatório não recuperado de Zeng (2025) continua sem MMAT; as respostas históricas de Sokkhey et al. (2020) permanecem sem reconferência do original indisponível nesta revisão.

## Limites restantes

O texto mantém repetições de contagens e ressalvas entre metodologia, revisão, discussão e conclusão. Uma redução estrutural dessas repetições pode ser objeto de outra revisão, sem apagar limitações materiais. A exposição matemática da explicação do modelo pode ser simplificada futuramente, preservando os detalhes necessários à reprodução. Nenhuma eficácia educacional própria foi atribuída ao protótipo nesta revisão.
