# Governança de publicação do projeto

Este documento define como o repositório público deve separar o relato
acadêmico do TCC, a proveniência técnica dos artefatos e o fluxo de
desenvolvimento. A publicidade do repositório favorece revisão, reprodução e
histórico, mas não torna todo detalhe de desenvolvimento apropriado para o
texto científico.

## Camadas de publicação

O conteúdo deve ser classificado antes de ser incorporado ao manuscrito, à
apresentação ou a uma página pública:

- **Relato acadêmico:** problema, objetivos, fundamentação, método, resultados,
  limitações e conclusões sustentados por fontes e artefatos verificáveis.
- **Proveniência técnica:** código, manifests, testes, versões, hashes,
  workflows e decisões de engenharia necessárias para reproduzir ou auditar
  um artefato.
- **Fluxo de desenvolvimento:** issues, pull requests, planos e tarefas ainda
  não concluídas. Essa camada pode permanecer pública para transparência, mas
  não constitui evidência científica nem aprovação metodológica.

Uma informação pode ser necessária na proveniência técnica sem pertencer ao
relato acadêmico. A apresentação e o TCC devem usar a camada acadêmica e
referenciar a proveniência somente quando isso esclarecer a reprodução ou o
limite de uma conclusão.

## Estados permitidos

Todo resultado relevante deve usar uma categoria precisa:

- **Realizado:** procedimento executado e documentado;
- **Validado:** procedimento realizado e verificado por teste, auditoria ou
  revisão identificável;
- **Demonstrado:** comportamento observado em demonstração, sem extrapolação
  para eficácia educacional;
- **Especificado:** requisito ou arquitetura proposta, ainda não executada;
- **Pendente:** decisão ou evidência necessária antes de uma conclusão;
- **Fora do escopo:** atividade não realizada nesta versão.

Termos como “concluído”, “validado” e “eficaz” não devem ser usados como
sinônimos. Em particular, testes sintéticos validam código e guardrails, mas
não demonstram eficácia pedagógica.

## Conteúdo que não deve migrar para o relato acadêmico

Não devem ser incorporados ao TCC ou à apresentação: caminhos locais de
computador, credenciais, logs brutos, transcrições de assistência, instruções
internas de agentes, detalhes de autenticação, conjecturas de escopo ou
decisões ainda não aprovadas apresentadas como resultados. Quando uma
pendência afetar a interpretação, deve-se publicar apenas a descrição neutra
da pendência, sua evidência e seu efeito sobre o alcance das conclusões.

## Rastreabilidade e revisão humana

Issues e pull requests podem registrar a evolução do trabalho, mas a inclusão
de uma tarefa, a aprovação de um workflow ou o sucesso de um teste não
substituem revisão científica. Cada afirmação quantitativa ou metodológica do
TCC deve apontar para a fonte, o artefato ou o procedimento que a sustenta.
Julgamentos de elegibilidade, MMAT, escopo, interpretação pedagógica e
conclusão científica permanecem sujeitos à revisão humana.

Antes de publicar uma nova versão, verificar: linguagem formal; ausência de
dados sensíveis ou caminhos locais; distinção entre TCC e PTC histórico;
coerência entre texto, apresentação e artefatos; e correspondência entre o
estado declarado e a evidência realmente disponível.
