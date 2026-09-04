# Plano de consolidação científica do TCC

**Data de origem:** 30/08/2026
**Última atualização:** 03/09/2026
**Estado:** plano de decisão; não é cronograma vigente e não autoriza execução
automática de um cenário científico.

## Objetivo

Consolidar as evidências da revisão sistemática, do manuscrito, do protótipo e
da apresentação para que a próxima decisão com a orientação seja tomada sobre
uma base rastreável. Este plano não transforma o PR #23 em decisão de escopo e
não substitui a orientação acadêmica.

## Estado que fundamenta a decisão

- O snapshot versionado atual contém 11.904 registros, 27 remoções
  determinísticas por DOI/URL, 11.877 registros na triagem, 2.486 na
  elegibilidade e 18 registros retidos.
- A composição atual é 17 candidatos provisoriamente empíricos e o protocolo
  contextual 6921. O registro 6918 foi corrigido para 2014 e excluído por
  estar fora do recorte 2015--2026.
- A rodada operacional preservou 23 candidatos e registrou sete overrides
  manuais. Oito decisões de escopo foram aprovadas e aplicadas no PR #55:
  três recuperações, uma exclusão temporal e quatro exclusões por escopo ou
  tipo documental.
- A reaplicação documental do MMAT está registrada por critério, mas é
  preliminar: fontes primárias, localizadores e adjudicação pelo supervisor
  ainda não estão completos. O protocolo 6921 não recebe MMAT empírico.
- As referências metodológicas, pedagógicas e teóricas permanecem na
  bibliografia completa do TCC. A bibliografia derivada do pipeline é um
  conjunto separado e contém os 18 registros retidos para rastreabilidade.

## Gatilhos antes da execução

1. Confirmar com a orientação se o trabalho seguirá como revisão/síntese e
   especificação, demonstração/prototipação baseada em artefatos existentes ou
   experimento/implementação própria.
2. Consolidar a interpretação científica dos 17 candidatos empíricos e manter
   o registro 6918 fora da síntese por estar fora do recorte temporal.
3. Completar a verificação das fontes primárias, localizadores e adjudicação do
   MMAT antes de produzir qualquer score, ranking ou conclusão comparativa de
   qualidade.
4. Manter a distinção entre o protocolo histórico de 2025, o snapshot atual e
   qualquer nova coleta. Uma nova execução de APIs gera um novo snapshot e não
   altera retrospectivamente os números atuais.
5. Avaliar checks, conversa, reviews e comentários inline — inclusive Copilot —
   antes de cada push ou merge. Cada apontamento deve ser corrigido no PR,
   justificado com evidência ou explicitamente registrado como pendência.

## Entregas por PR

Os próximos PRs devem ser atômicos e independentes quanto ao tema:

- reconciliação de dados, deduplicação e artefatos do pipeline;
- manuscrito, MMAT e referências derivadas;
- apresentação Slidev e publicação compilada;
- documentação, governança e integração dos PRs anteriores.

Cada PR deve declarar sua base, não versionar o SQLite e incluir os comandos de
validação local. Antes do envio, a branch deve ser comparada com `origin/main`
e o estado remoto deve ser revisado novamente, pois checks e comentários são
eventos mutáveis.

## Relação com PRs anteriores

- **PR #20:** contexto de governança documental; só pode ser aproveitado por
  partes genéricas que não congelem o denominador histórico nem removam a
  infraestrutura do protótipo.
- **PR #23:** contexto editorial/normativo; não decide o cenário científico e
  não deve ser mesclado integralmente por causa da sobreposição e do conflito.
- **PR #34:** contexto de reconciliação; seus arquivos devem ser comparados com
  a fonte atual e não absorvidos como fonte de verdade automática.
- **PR #35:** rollback isolado do commit direto na `main`; deve ser mesclado
  antes dos PRs científicos derivados.

## Critério de encerramento

O plano só pode ser encerrado quando a orientação aprovar um cenário, o
supervisor científico não apontar bloqueios metodológicos in-scope, os checks
locais e remotos estiverem verdes e todas as revisões automatizadas aplicáveis
forem avaliadas. Até lá, o estado correto é **gate científico pendente**.
