# ADR-0001 — Preservar particularidades institucionais do IFC em atualizações normativas

- **Status:** aceito
- **Data:** 2026-08-07
- **Escopo de implementação:** adiado
- **Decisão relacionada:** governança de engenharia documental do TCC

## Contexto

O TCC utiliza uma customização institucional baseada em `abntex2` que contém comportamentos específicos do IFC, como composição de capa, folha de rosto e outras decisões de apresentação. Parte dessa implementação é legada e pode ter sido escrita sob versões anteriores de normas técnicas e dependências LaTeX.

Ao mesmo tempo, normas técnicas, orientações institucionais, templates do Sistema Integrado de Bibliotecas e instruções da Coordenação de TCC podem evoluir em ritmos diferentes.

Tratar uma atualização de ABNT como autorização para substituir integralmente a classe institucional cria risco de regressão: uma implementação tecnicamente mais nova pode remover particularidades que continuam obrigatórias para o IFC. O problema inverso também existe: tratar a classe legada como autoridade absoluta pode perpetuar comportamentos que já não correspondem à baseline vigente.

O regulamento de PTCC/TCC do Bacharelado em Ciência da Computação do IFC Campus Videira prevê observância dos padrões nacionais adotados pela ABNT ou de critérios definidos pelo Coordenador de TCC, além de permitir instruções complementares. Portanto, a governança precisa representar múltiplas fontes de autoridade e sua aplicabilidade por domínio.

## Decisão

Adotar as seguintes regras:

1. **Particularidades institucionais do IFC serão preservadas por padrão.**
2. **Atualizações normativas não modificarão automaticamente componentes institucionais.**
3. **A precedência será resolvida por domínio, não por uma hierarquia global `ABNT > IFC`.**
4. **Componentes como capa, folha de rosto, folha de aprovação, identidade visual e textos institucionais serão classificados como `institutional-strict` quando sua origem institucional for confirmada.**
5. **Quando uma mudança normativa aparentemente alcançar um componente `institutional-strict`, o sistema deverá registrar `NORMATIVE_INSTITUTIONAL_CONFLICT` e exigir revisão humana.**
6. **A classe LaTeX e os pacotes usados pelo projeto serão tratados como implementação, não como fonte normativa.**
7. **Uma futura modernização deverá decompor o código em comportamento institucional, comportamento normativo e escolha técnica antes de alterar a classe.**
8. **Mudanças de apresentação com impacto observável deverão possuir evidência de regressão visual e estrutural.**
9. **Nenhum workflow futuro poderá editar automaticamente componentes institucionais com preservação estrita.**
10. **Contribuições ao modelo institucional serão tratadas como trabalho pós-TCC e submetidas ao processo e aos mantenedores apropriados.**

## Consequências positivas

- reduz o risco de descaracterização do modelo institucional;
- torna conflitos entre fontes explícitos e auditáveis;
- permite modernização técnica sem confundir pacote novo com regra nova;
- preserva rastreabilidade entre fonte, decisão e implementação;
- facilita futuras contribuições upstream com mudanças menores e justificadas;
- evita que o CI produza uma falsa declaração de conformidade integral.

## Consequências negativas e custos

- algumas mudanças não poderão ser resolvidas automaticamente;
- será necessário manter metadados das fontes e datas de verificação;
- conflitos reais podem exigir consulta à Coordenação, orientação ou biblioteca;
- testes de regressão visual e fixtures aumentam a infraestrutura futura;
- a classe legada não poderá ser simplesmente substituída por uma alternativa moderna sem auditoria prévia.

Esses custos são aceitos porque a correção institucional e a rastreabilidade são mais importantes que a simplificação da manutenção.

## Alternativas consideradas

### A. Substituir a classe institucional sempre que houver implementação ABNT mais recente

**Rejeitada.** Idade do pacote não determina fidelidade ao modelo institucional. A substituição pode alterar elementos específicos do IFC sem autorização.

### B. Considerar a classe atual como fonte definitiva de verdade

**Rejeitada.** Código legado pode conter decisões técnicas obsoletas, referências normativas antigas ou divergência em relação a orientações institucionais posteriores.

### C. Aplicar uma precedência global em que ABNT sempre prevalece

**Rejeitada.** A aplicabilidade depende do domínio e o próprio regulamento admite critérios definidos pela Coordenação de TCC. Conflitos exigem interpretação, não substituição mecânica.

### D. Manter a decisão apenas como conhecimento informal

**Rejeitada.** Decisões implícitas não são reproduzíveis e aumentam o risco de regressões futuras, especialmente em um repositório público com múltiplos PRs e automações.

## Critérios que reabrem esta decisão

Este ADR deve ser revisado se ocorrer qualquer uma das situações abaixo:

- publicação de novo regulamento institucional que defina precedência diferente;
- orientação formal da Coordenação ou Colegiado sobre conflitos entre template e norma;
- substituição oficial do modelo LaTeX por uma fonte canônica com nova política de manutenção;
- alteração institucional explícita de elementos hoje classificados como `institutional-strict`;
- mudança no processo de depósito da biblioteca que exija comportamento incompatível com esta decisão.

Reabrir o ADR não significa revogá-lo automaticamente. A nova evidência deve ser registrada e comparada com o contexto original.

## Rastreabilidade

A política operacional associada está documentada em:

- `docs/tcc/NORMATIVE_GOVERNANCE.md`;
- `docs/tcc/DOCUMENT_ENGINEERING_ROADMAP.md`.

Este ADR registra a decisão. Os documentos operacionais podem detalhar sua implementação futura sem alterar o princípio aqui estabelecido.
