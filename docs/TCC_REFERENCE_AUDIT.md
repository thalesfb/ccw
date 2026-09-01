# Auditoria das referências do TCC

## Finalidade

Este documento registra a validação bibliográfica e a adequação de uso das referências empregadas no TCC. A auditoria separa quatro perguntas que não devem ser confundidas:

1. a publicação existe e pode ser identificada por uma fonte canônica?
2. os metadados bibliográficos estão completos e corretos?
3. o desenho e a qualidade editorial permitem usar a publicação para a finalidade pretendida?
4. a afirmação do TCC é efetivamente sustentada pelo escopo da fonte?

A planilha canônica está em `research/data/reference_audit.csv`. Ela deve ser atualizada sempre que uma referência, citação ou afirmação for alterada.

## Critérios de decisão

- `verified`: existência, metadados e uso considerados adequados para o escopo registrado;
- `metadata_fix`: publicação real, mas ainda existe metadado bibliográfico que requer confirmação ou correção;
- `update_version`: a versão historicamente registrada foi identificada, porém existe edição posterior que não deve substituir silenciosamente a fonte efetivamente consultada;
- `scope_limited`: publicação real, porém sustenta apenas uma parte da afirmação ou deve ser usada como evidência específica;
- `editorial_caution`: publicação localizada, mas com qualidade editorial, transparência metodológica ou relevância insuficiente para ser fonte central;
- `unused`: publicação real que não deve ser usada na redação atual;
- `replace`: a citação deve ser substituída por uma fonte mais canônica para a afirmação.

## Resultado consolidado

### Diretrizes metodológicas

PRISMA 2020 e PRISMA-P 2015 permanecem fontes distintas: a primeira fundamenta o relato da revisão e a segunda os princípios de protocolo. O MMAT passou a ser citado bibliograficamente pelo artigo revisado por pares de Hong et al., DOI `10.3233/EFI-180221`; o manual continua sendo um documento operacional complementar.

O Cochrane Handbook permanece explicitamente versionado como 6.4 no arquivo bibliográfico porque essa é a versão historicamente registrada no trabalho. A existência de edições posteriores constitui drift de versão e exige avaliação metodológica deliberada; não é corrigida pela simples troca do número da versão.

### Fundamentação pedagógica

BNCC, National Research Council, OCDE/PISA, Piaget, Vygotsky, Ausubel, Wood, Bruner e Ross, Black e Wiliam e Hattie e Timperley permanecem na fundamentação com as seguintes restrições:

- Piaget fundamenta construção ativa do conhecimento, mas não deve receber sozinho todas as implicações didáticas específicas da educação matemática;
- Vygotsky fundamenta a Zona de Desenvolvimento Proximal;
- `scaffolding` deve ser atribuído a Wood, Bruner e Ross;
- o framework do PISA fundamenta construtos e desenho da avaliação; os descritores dos níveis devem usar também o relatório de resultados;
- desempenho observado, proficiência estimada, competência e aprendizagem permanecem conceitos relacionados, porém não intercambiáveis.

A entrada legada `Piaget1972` permanece marcada para substituição e não é usada pelo texto atual, que cita `Piaget1972EN`. A entrada de Vygotsky ainda requer conferência da edição citada antes de qualquer enriquecimento de metadados. A citação do SAEB deve distinguir documentação de resultados e eventual uso de microdados quando o projeto chegar à governança de dados.

### Estudos incluídos na revisão

O baseline atualizado contém 16 registros retidos. Dez estudos permanecem do conjunto anterior e seis registros foram incorporados após a correção do pipeline de scoring; os sete registros removidos não devem permanecer como referências de estudos incluídos. Entre os 16 registros atuais, 15 são classificados provisoriamente como empíricos, com o ID 6918 em hold por conflito temporal, e o ID 6921 é um protocolo/proposta retido apenas para contexto e rastreabilidade, fora da síntese empírica. A normalização bibliográfica segue separada das decisões de seleção, e não deve ser usada para inferir qualidade científica ou substituir a reaplicação do MMAT ao conjunto atualizado.

A correspondência fechada entre os IDs incluídos no banco e as chaves citadas pelo manuscrito é: `1 → Math2021_001`, `2 → Implementation2025_000`, `3 → Multimodels2020_002`, `4 → Analysis2022_003`, `5 → Design2025_004`, `6 → Identifying2017_006`, `7 → Innovative2023_005`, `8 → Computational2017_008`, `9 → Machine2019_007`, `10 → Machine2024_009`, `6916 → Villegas2025_6916`, `6917 → Ozseven2026_6917`, `6918 → Kaser2025_6918`, `6920 → Echeveria2025_6920`, `6921 → Imperatrice2025_6921` e `6923 → Zeng2025_6923`. O conjunto citado na tabela de registros do manuscrito e o export `included_papers.bib` devem usar exatamente essas 16 chaves; a tabela de síntese empírica e as conclusões de evidência devem excluir o protocolo contextual 6921, conforme `research/data/current_synthesis_scope.csv`.

As sete chaves históricas removidas — `Machine2022_010`, `Data2020_011`, `Enhancing2025_012`, `Authentic2024_013`, `Performance2023_014`, `Assessing2024_015` e `Analysis2021_016` — não fazem parte das bibliografias de estudos incluídos atuais. Elas só podem aparecer em documentação histórica de reconciliação, acompanhadas da indicação explícita de que foram removidas. Essa lista é a linhagem bibliográfica do PTC histórico; ela não deve ser tratada como mapeamento automático dos sete overrides do snapshot vigente, que são os IDs 14, 15, 6915, 6919, 6922, 6925 e 6926.

As seguintes correções prioritárias foram aplicadas ao arquivo bibliográfico usado pelo TCC:

- `Implementation2025_000`: segundo autor, volume, número, páginas e URL DOI;
- `Math2021_001`: nome completo dos anais, páginas e URL DOI;
- `Multimodels2020_002`: volume, número, páginas e URL DOI;
- `Analysis2022_003`: páginas e URL DOI;
- `Design2025_004`: nome dos anais, páginas e URL DOI, mantendo cautela editorial;
- `Identifying2017_006`: volume, número, páginas e URL DOI;
- `Machine2019_007`: anais IEEE EDUCON 2019, páginas e URL DOI;
- `Computational2017_008`: classificação como tese de doutorado da Carnegie Mellon University;
- `Villegas2025_6916`, `Ozseven2026_6917` e `Echeveria2025_6920`: registros adicionados ao baseline a partir do banco atualizado e revisados em fonte primária externa para o ledger MMAT preliminar;
- `Kaser2025_6918`: registro adicionado ao baseline com identificador persistente preservado; o repositório oficial da ETH confirma a identidade e o DOI e data a tese de 2014, enquanto o snapshot operacional registra 2025. O texto integral não foi recuperado localmente, portanto a elegibilidade temporal e o MMAT permanecem em hold;
- `Imperatrice2025_6921`: registro adicionado ao baseline sem venue ou identificador persistente no metadado local; o PDF externo foi revisado e descreve protocolo/proposta sem resultados empíricos concluídos, portanto não sustenta uma apreciação MMAT empírica nesta etapa;
- `Zeng2025_6923`: registro adicionado ao baseline com identificador persistente preservado; o repositório e o programa oficial de dissertações do Teachers College corroboram título, autoria e ano de 2025, mas a fonte primária integral ainda não foi recuperada;
- todas as URLs de Semantic Scholar e OpenAlex foram removidas dos dois artefatos bibliográficos de estudos incluídos; a proveniência de descoberta permanece no pipeline de pesquisa, não na citação final.

As cautelas atuais permanecem explícitas:

- `Innovative2023_005`: o DOI é canônico, mas ano/volume/número devem ser confirmados em fonte editorial antes de sustentar afirmação central;
- os seis novos registros permanecem sob cautela editorial para afirmações centrais de eficácia, mesmo quando a fonte primária foi consultada: o ledger MMAT atual separa 6916, 6917 e 6920 como revisados externamente, 6918 como hold de fonte/período, 6921 como protocolo/proposta não aplicável ao MMAT empírico e 6923 como fonte integral ainda não recuperada. O CSV mantém `metadata_status=metadata_fix`, `use_status=editorial_caution` e `decision=retain_with_caution` para todos os seis; os dois registros com fonte externa corroborada agora estão marcados com `existence=verified`, mas isso não elimina a pendência de metadados, texto integral ou escopo. As mesmas cautelas foram registradas nas entradas BibTeX. Em particular, `Imperatrice2025_6921` não possui DOI ou venue no metadado local.

## Fontes primárias para decisões técnicas

A especificação conceitual citava técnicas computacionais sem que todas possuíssem referência metodológica própria. O lote passa a incluir e citar fontes primárias para as decisões técnicas que permanecem no texto:

| Decisão/técnica | Fonte primária | Uso permitido no TCC |
|---|---|---|
| Random Forest | Breiman (2001) | definição metodológica e referência do algoritmo, não evidência de superioridade neste problema |
| SVM | Cortes e Vapnik (1995) | definição metodológica e referência do algoritmo, não escolha definitiva do modelo |
| análise ROC | Fawcett (2006) | fundamentação da métrica/curva de avaliação |
| calibração de probabilidades | Niculescu-Mizil e Caruana (2005) | fundamentação metodológica de calibração, sem antecipar resultado experimental |
| LIME | Ribeiro, Singh e Guestrin (2016) | técnica candidata de explicação local |
| SHAP | Lundberg e Lee (2017) | técnica candidata de atribuição de importância local/global |

Essas referências sustentam a descrição das técnicas. Elas não demonstram que essas técnicas sejam as melhores para a base ainda não executada e não constituem resultados do protótipo.

## Política de fontes

1. DOI ou página oficial da editora é a URL bibliográfica preferencial.
2. OpenAlex, Semantic Scholar, Crossref e CORE registram a proveniência da descoberta, não substituem a fonte de publicação.
3. Definições centrais devem priorizar obras canônicas, documentos normativos ou revisões robustas.
4. Estudos empíricos recentes devem apoiar resultados específicos, não substituir fundamentos teóricos.
5. Uma referência incluída na revisão pode permanecer na síntese mesmo com limitações, desde que essas limitações sejam registradas e consideradas na interpretação.
6. Nenhuma referência será removida silenciosamente da trilha da revisão sistemática.
7. Uma edição mais nova de uma fonte metodológica não substitui automaticamente a edição efetivamente consultada; mudança de versão deve ser registrada e avaliada.

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
| Random Forest é uma alternativa de ensemble supervisionado | Breiman, 2001 | método candidato, sem evidência de superioridade no TCC |
| SVM é uma alternativa de classificação por margem | Cortes e Vapnik, 1995 | método candidato, sem escolha definitiva |
| ROC pode apoiar avaliação de classificadores | Fawcett, 2006 | avaliação técnica, não eficácia pedagógica |
| calibração avalia/ajusta a qualidade probabilística | Niculescu-Mizil e Caruana, 2005 | avaliação probabilística do modelo |
| LIME é técnica candidata de explicação local | Ribeiro, Singh e Guestrin, 2016 | explicação de modelo, não causalidade |
| SHAP é técnica candidata de atribuição de importância | Lundberg e Lee, 2017 | explicação de modelo, não causalidade |

## Pendências explicitamente não resolvidas

A auditoria não declara todos os registros como perfeitos. Permanecem, de forma rastreável:

1. decidir se o Cochrane Handbook historicamente citado deve permanecer em 6.4 ou ser atualizado após comparação metodológica com edições posteriores;
2. confirmar em fonte editorial os metadados ainda ambíguos de `Innovative2023_005`;
3. revisar a edição bibliográfica de Vygotsky antes de enriquecer campos de editores/edição;
4. distinguir, quando a fonte SAEB for usada operacionalmente, a documentação de resultados da referência aos microdados efetivamente adquiridos;
5. concluir a reaplicação e a adjudicação do MMAT aos 15 registros empíricos
   aplicáveis; o protocolo contextual 6921 permanece fora dessa avaliação. O
   ledger vigente já contém decisões e evidências por critério, mas a tabela
   histórica de 17 estudos não pode ser reutilizada.

Essas pendências não autorizam remover os estudos da revisão nem reescrever resultados. Elas limitam o uso bibliográfico correspondente e devem ser reavaliadas quando o texto ou o pipeline dependerem delas.

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
