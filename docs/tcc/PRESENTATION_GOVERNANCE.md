# Governança da apresentação do TCC

Este documento define os critérios de produção e verificação da apresentação
em `presentation/`. Ele separa a referência visual fornecida, os requisitos
institucionais e os critérios científicos verificáveis, sem transformar
decisões de implementação em afirmações acadêmicas.

## Escopo aprovado

- A fonte de verdade do deck é `presentation/slides.md`, em Slidev.
- Os números devem continuar reconciliados com
  `research/exports/reports/summary.json`.
- O estado científico apresentado é o snapshot atual: 18 registros retidos,
  sendo 17 candidatos empíricos provisórios e um protocolo contextual.
- A apresentação não deve prometer eficácia, validação experimental ou um
  protótipo executado quando a evidência correspondente ainda não existe.
- O encerramento deve oferecer o repositório por QR code, com destino
  canônico `https://github.com/thalesfb/ccw`, texto alternativo e uma área
  visual legível para leitura em projeção.

## Template fornecido: instrução versus requisito

O arquivo de template fornecido externamente foi inspecionado como referência
visual e tipográfica. Ele contém 55 slides,
incluindo exemplos, slides de instrução do fornecedor, referências de fonte e
slides descartáveis.

As seguintes propriedades foram aproveitadas como direção visual:

- proporção 16:9;
- composição tipográfica e editorial do material de referência, sem tratá-la
  como a fonte do manuscrito;
- composição editorial com cartões, divisões claras e espaço negativo;
- paleta de referência registrada no slide “Fonts & colors used”.

As instruções “Instructions for use”, a exigência condicional de manter um
slide de créditos e a recomendação de atribuição dependente do tipo de conta
Slidesgo são instruções de licenciamento/uso do fornecedor. Elas não são
normas do IFC, requisitos científicos do TCC nem autorização para publicar o
arquivo original. Por isso, o PPTX não é fonte dos números atuais, não é
versionado no repositório e qualquer crédito deve ser decidido conforme a
licença efetivamente obtida.

O deck do TCC preserva a composição editorial e a proporção 16:9, mas usa a
família Times New Roman/Nimbus Roman/Times para manter continuidade com o
manuscrito. As classes do código usam o prefixo `tcc-`; o material do PTC é
apenas referência histórica e não é a identidade semântica do deck atual.

## Identidade institucional

O deck usa localmente a marca horizontal oficial do IFC Campus Videira,
baixada da página institucional de logotipos e armazenada em
`presentation/public/branding/ifc-campus-videira-horizontal.png`. A marca não
deve ser recriada com CSS, redesenhada ou substituída por um símbolo genérico.

Fontes institucionais consultadas:

- [Logotipos do IFC](https://cecom.ifc.edu.br/logotipos-do-ifc/)
- [Manual de Identidade Visual do IFC](https://cecom.ifc.edu.br/wp-content/uploads/sites/10/2022/10/Manual-de-Identidade-Visual-do-IFC-ATUALIZADO.pdf)
- [Modelos de TCC do SIBI/IFC](https://biblioteca.ifc.edu.br/tcc/)
- [Regulamento de Trabalho de Curso do IFC Videira](https://videira.ifc.edu.br/ciencia-da-computacao/wp-content/uploads/sites/11/2024/06/regulamento-TC-2023.pdf)

Essas fontes orientam a revisão humana; o build não declara conformidade
integral com ABNT, com o manual do IFC ou com a aprovação da banca.

## Legibilidade e acessibilidade

O contrato automatizado em `presentation/deck-standards.mjs` verifica:

- presença da marca institucional e do QR;
- destino e texto alternativo do QR;
- uso da família Times New Roman/Nimbus Roman/Times, compatível com o TCC;
- remoção visual de uma marca IFC desenhada manualmente;
- contraste mínimo WCAG AA de 4,5:1 para texto normal e 3:1 para texto
  grande, conforme [WCAG 2.2, critério 1.4.3](https://www.w3.org/TR/WCAG22/#contrast-minimum).

O QR é gerado por `npm run generate:qr`, a partir da URL registrada no
script, e o SVG gerado é um artefato local reproduzível.

## Limites de publicação

A apresentação publica somente o estado científico e técnico que possui
evidência versionada. O rastreador de issues e o histórico de pull requests
servem à proveniência da engenharia, mas não são fontes de resultados,
aprovação acadêmica ou validação experimental. Reuniões, decisões pendentes,
hipóteses de continuidade e tarefas de desenvolvimento devem aparecer no
deck apenas quando forem necessárias para explicar o escopo e sempre com a
distinção explícita entre realizado, demonstrado e proposto.

Não devem ser publicados em documentos acadêmicos: caminhos locais,
credenciais, logs brutos, transcrições de assistência, instruções internas de
agentes ou conjecturas apresentadas como decisões. Quando uma pendência for
relevante para a interpretação, ela deve ser descrita de forma neutra, com
seu efeito sobre o alcance das conclusões.
