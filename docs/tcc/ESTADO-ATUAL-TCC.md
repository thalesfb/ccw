# Estado atual e limites da versão do TCC

**Atualização:** 14 de setembro de 2026

Este registro público descreve o estado verificável da versão atual do
Trabalho de Conclusão de Curso e separa resultados produzidos, validações
técnicas e decisões metodológicas ainda pendentes. Ele é uma nota de
transparência do repositório; não substitui o texto do TCC, o protocolo da
revisão, a supervisão acadêmica ou qualquer aprovação necessária para uma
execução experimental.

Os critérios gerais para separar relato acadêmico, proveniência técnica e
fluxo de desenvolvimento estão em
[`PUBLICATION_GOVERNANCE.md`](PUBLICATION_GOVERNANCE.md).

## Revisão sistemática e MMAT

O snapshot vigente da revisão tem data de corte em 31 de agosto de 2026. O
fluxo PRISMA registra 11.904 registros identificados, 11.877 após remoções
determinísticas, 2.486 submetidos à elegibilidade e 18 retidos
operacionalmente. A população retida está separada em 17 candidatos empíricos
provisórios e um protocolo ou proposta contextual, que não integra a síntese
de evidências.

O manifesto de reprodutibilidade registra a geração do snapshot em
4 de setembro de 2026, às 02:45:33 UTC, e preserva os hashes dos exports e
dos ledgers que sustentam essa contagem. A data do snapshot e a data de geração
dos artefatos são informações de proveniência; não representam, por si só,
uma nova rodada de coleta nas APIs.

O ledger do MMAT 2018 preserva as duas perguntas de triagem, S1 e S2, e os
critérios Q1--Q5 correspondentes ao delineamento de cada estudo. As respostas
usam a legenda Y (sim), N (não) e CT (não é possível concluir com a evidência
disponível). Nove registros tiveram o texto primário revisado externamente e
oito foram apreciados com base em resumo ou metadados. Como a leitura foi
realizada por um único revisor e a recuperação de fontes, os localizadores e
a adjudicação ainda não estão completos, o MMAT permanece uma apreciação
documental preliminar por critério. Não há escore agregado, ranking ou
conclusão de eficácia.

## Implementação e escopo experimental

O diretório `prototype/` contém um pipeline implementado para ingestão
manifestada, normalização do ASSISTments, construção de atributos sem
vazamento, separação temporal e por estudante, modelos candidatos, métricas e
bootstrap agrupado por estudante. A suíte local passa com 44 testes, o que
valida o comportamento do código e dos guardrails sintéticos. Isso não
constitui treinamento com dados reais, avaliação de eficácia pedagógica,
participação de estudantes ou validação em escola.

Os limiares mínimos de tamanho da fonte e do conjunto de teste ainda não
foram congelados. Qualquer execução com dados reais depende de uma decisão
metodológica explícita sobre fonte, licença, unidade de análise, desfecho,
divisão dos dados e critérios de avaliação.

## Decisões metodológicas pendentes

As próximas decisões relevantes são: confirmar se o trabalho permanecerá como
revisão sistemática acompanhada de especificação conceitual ou se incluirá um
estudo computacional exploratório separado; aprovar, caso aplicável, a fonte
de dados, seus termos de uso, o desfecho `correct_next`, os limiares mínimos e
o protocolo de divisão; consolidar o deck canônico de 25 slides e distinguir
qualquer exportação histórica de 19 slides; e concluir a recuperação das
fontes primárias e a adjudicação do MMAT.

Também permanece pendente uma matriz de rastreabilidade que associe cada
requisito da especificação aos estudos e artefatos que o fundamentam. Até que
essa matriz seja concluída, a ligação entre literatura e requisitos deve ser
apresentada como derivação temática documentada, não como cobertura exaustiva
de cada requisito por uma fonte individual.

## Possível execução futura com Google Colab

O Google Colab é um ambiente de notebooks Python executados no navegador.
Benefícios, unidades de computação, GPUs, TPUs e execução em segundo plano
dependem do plano e da conta efetivamente associados ao serviço; não devem
ser inferidos apenas pelo nome de um produto. O repositório, portanto, não
assume que um “Colab CLI” ou MCP de terceiros seja uma interface oficial do
benefício para consumidores.

Depois de aprovada a execução, as alternativas podem ser comparadas entre o
Colab web, um runtime local compatível com Jupyter e, se houver governança
própria de projeto, orçamento e identidade, o Colab Enterprise/Vertex AI.
Qualquer notebook futuro deverá registrar versão da fonte, data de acesso,
hashes dos artefatos, configuração, divisão, métricas, avisos e relatório.
Dados brutos restritos não devem ser commitados nem publicados, e métricas
preditivas não devem ser apresentadas como aprendizagem ou eficácia
pedagógica.

Fontes oficiais sobre o serviço:

- [Google One — benefícios do Google AI Pro e Colab](https://support.google.com/googleone/answer/14534406?hl=en)
- [Google Colab — perguntas frequentes e limites dos planos](https://research.google.com/colaboratory/faq.html)
- [Google Colab — runtimes locais](https://research.google.com/colaboratory/local-runtimes.html)
- [Google Cloud — runtimes do Colab Enterprise](https://docs.cloud.google.com/vertex-ai/docs/colab/create-runtime)

## Limite interpretativo da versão

O estado atual pode ser resumido como **código implementado, testes
sintéticos verdes, experimento real pendente e MMAT preliminar**. A
apresentação e o manuscrito devem comunicar esse limite sem transformar
resultados operacionais em evidência de eficácia educacional.
