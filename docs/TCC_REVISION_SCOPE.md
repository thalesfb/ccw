# Registro da revisão do TCC

A revisão metodológica consolidada foi realizada pela issue #5 e pelo PR #6. A revisão editorial e normativa subsequente é acompanhada pelo PR #23. Este documento distingue **estado executado** de **decisão futura** para evitar que uma conversa exploratória seja convertida em mudança definitiva de escopo sem validação da orientação.

## Estado acadêmico já executado

Até o momento, o TCC possui como entregas efetivamente documentadas:

- revisão sistemática da literatura;
- avaliação metodológica dos estudos incluídos;
- síntese e discussão dos achados;
- especificação conceitual do protótipo;
- artefatos e planejamento experimental já existentes no repositório, que não devem ser confundidos com validação pedagógica concluída.

A implementação funcional completa, o treinamento definitivo de modelos e a validação empírica com participantes **não podem ser descritos como resultados já realizados**. Isso não significa, contudo, que estejam definitivamente excluídos da continuidade do TCC.

## Decisão científica futura — pendente de orientação

A estratégia de continuidade deve ser discutida com o orientador. Três cenários permanecem abertos:

1. **revisão/síntese/especificação:** consolidar a contribuição principalmente documental e científica;
2. **demonstração de viabilidade com recursos consolidados:** reutilizar modelos, métodos, pesos, notebooks, bibliotecas ou outros artefatos científicos já documentados, quando isso permitir demonstrar a proposta sem treinamento desnecessário do zero;
3. **experimento próprio:** prosseguir com parte ou todo o desenho experimental e a implementação planejados na issue #7.

Nenhum desses cenários é considerado aprovado apenas por constar neste documento. A issue #24 organiza as evidências para a decisão, a issue #7 preserva a linha experimental e a issue #25 acompanha o título.

Até o gate com a orientação:

- não remover ou arquivar o diretório `prototype/` por mudança presumida de escopo;
- não desativar os testes experimentais existentes;
- não reclassificar os documentos experimentais como trabalho descartado;
- não escrever resultados experimentais ainda não produzidos;
- não pressupor que todo modelo precise ser treinado do zero;
- não tratar reutilização de um modelo consolidado como evidência automática de eficácia pedagógica.

## Decisões metodológicas preservadas

- O PRISMA 2020 é apresentado como diretriz de relato.
- O PRISMA-P é apresentado como orientação para protocolos; não se declara conformidade integral porque não houve registro prospectivo.
- O limiar usado na elegibilidade representa relevância temática e não qualidade metodológica.
- O MMAT é reportado por Q1--Q5, sem nota geral, média, ranking ou categoria de qualidade e sem ser reclassificado como medida global de certeza da evidência.
- A reutilização do cache é explicada como métrica dependente da execução; valores conflitantes não são transformados em indicador estável sem artefato versionado correspondente.
- Desempenho observado, proficiência estimada, competência e aprendizagem são tratados como conceitos relacionados, mas distintos.
- Nenhuma métrica técnica isolada deve ser interpretada como evidência de aprendizagem ou eficácia pedagógica.
- Frequência de uso de uma técnica na literatura não equivale a superioridade científica.

## Decisões editoriais da revisão atual

- A Seção 1.5 descreve a estrutura do trabalho em prosa contínua, sem lista de capítulos.
- O capítulo de cronologia da execução foi removido da versão textual atual; o TCC está organizado em sete capítulos.
- Títulos de figuras são apresentados acima das ilustrações e as fontes permanecem abaixo, conforme o padrão institucional adotado.
- O Capítulo 5 mantém suas seções temáticas, mas apresenta princípios, requisitos, critérios de dados, avaliação e arquitetura em prosa acadêmica.
- Listas são preservadas quando cumprem função metodológica de precisão e reprodutibilidade; listas meramente expositivas são preferencialmente convertidas em prosa.
- O Capítulo 6 prioriza interpretação e discussão integrada dos achados.
- A conclusão delimita o alcance dos resultados sem alegações de eficácia não demonstrada.
- O apêndice PRISMA 2020 registra itens atendidos, parciais, não realizados e não aplicáveis e não declara conformidade integral artificial.
- Termos técnicos em português são priorizados quando existe equivalente consagrado e natural no contexto científico.
- Quando um termo estrangeiro é mantido por utilidade técnica ou identificação terminológica, preserva-se a convenção de destaque adotada no documento e no contexto institucional.
- O título atual permanece no fonte até decisão com a orientação; a issue #25 reúne alternativas condicionadas ao escopo final.

## Divergência do protocolo da revisão a resolver

Antes de uma eventual atualização de literatura até 2026, deve ser reconstruído o protocolo realmente executado. Hoje há divergência entre registros de 72/108 consultas e recortes iniciados em 2015/2016.

A correção deve partir de evidência versionada — histórico Git, banco, logs, exports e parâmetros — e não de escolha retrospectiva do valor mais conveniente. A issue #24 acompanha essa auditoria e a issue #26 registra a atualização de 2026 como possibilidade condicionada à orientação.

## Referência institucional e normativa

A normalização deve observar, em conjunto:

1. os modelos do curso de Ciência da Computação do IFC Campus Videira;
2. o template institucional aplicável;
3. as edições vigentes das normas de trabalhos acadêmicos, citações, referências, resumos e sumário;
4. as orientações específicas do orientador e da banca quando compatíveis com o regulamento e o template.

O repositório contém uma customização LaTeX institucional criada em 2017. Ela deve ser comparada de forma controlada com o modelo vigente antes da entrega definitiva, sem substituição silenciosa que altere elementos institucionais.

## Contrato de validação

Pull requests que alteram o TCC devem, conforme o escopo da mudança:

1. verificar whitespace no diff;
2. compilar fontes Python relevantes;
3. executar auditoria bibliográfica e controles MMAT;
4. executar testes editoriais/metodológicos;
5. **preservar e executar os testes experimentais existentes enquanto a orientação não decidir reclassificá-los**;
6. compilar o documento LaTeX;
7. publicar/validar o PDF e logs;
8. inspecionar visualmente as páginas afetadas;
9. não mesclar automaticamente.

## Uso de LLMs e agentes

Ferramentas de IA podem apoiar busca, auditoria, comparação de fontes, detecção de inconsistências, execução de testes e elaboração de alternativas. Elas não substituem a decisão científica do autor/orientador sobre:

- escopo do TCC;
- inclusão ou exclusão de estudos;
- julgamento MMAT;
- interpretação dos resultados;
- escolha do título;
- aceitação de redação substantiva.

A revisão de estilo busca clareza, precisão e voz acadêmica responsável; não deve ser orientada por tentativa de enganar detectores de IA.

## Próximo gate

A próxima decisão estrutural é acadêmica, não técnica: apresentar à orientação os cenários A/B/C, a possibilidade de reutilização de recursos científicos consolidados, o custo de treinamento próprio, a situação da atualização bibliográfica e as limitações atuais. Somente após essa decisão a governança do repositório deverá marcar atividades como obrigatórias, opcionais, demonstrativas ou fora do escopo.
