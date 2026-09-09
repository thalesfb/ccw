# Governança da apresentação do PTC

Este documento registra as decisões para a apresentação em `presentation/` e
separa requisitos do pedido do usuário, instruções encontradas no arquivo
PPTX de referência e critérios científicos ou institucionais verificáveis.

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

O arquivo local
`C:\Users\user\Downloads\Ensino Personalizado de Matemática_ Oportunidades e Técnicas Computacionais_template.pptx`
foi inspecionado como referência visual e tipográfica. Ele contém 55 slides,
incluindo exemplos, slides de instrução do fornecedor, referências de fonte e
slides descartáveis.

As seguintes propriedades foram aproveitadas como direção visual:

- proporção 16:9;
- famílias Asap e Barlow;
- composição editorial com cartões, divisões claras e espaço negativo;
- paleta de referência registrada no slide “Fonts & colors used”.

As instruções “Instructions for use”, a exigência condicional de manter um
slide de créditos e a recomendação de atribuição dependente do tipo de conta
Slidesgo são instruções de licenciamento/uso do fornecedor. Elas não são
normas do IFC, requisitos científicos do PTC nem autorização para publicar o
arquivo original. Por isso, o PPTX não é fonte dos números atuais, não é
versionado no repositório e qualquer crédito deve ser decidido conforme a
licença efetivamente obtida.

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
- permanência das famílias Asap/Barlow;
- remoção visual de uma marca IFC desenhada manualmente;
- contraste mínimo WCAG AA de 4,5:1 para texto normal e 3:1 para texto
  grande, conforme [WCAG 2.2, critério 1.4.3](https://www.w3.org/TR/WCAG22/#contrast-minimum).

O QR é gerado por `npm run generate:qr`, a partir da URL registrada no
script, e o SVG gerado é um artefato local reproduzível.

## Relação com as issues abertas

Esta atualização atende a parte editorial e de rastreabilidade da decisão
registrada nas issues, mas não encerra gates científicos ou de orientação:

- [#27](https://github.com/thalesfb/ccw/issues/27): deck preparado para reunião
  de decisão sobre continuidade; a reunião ainda deve registrar o cenário e
  a justificativa escolhidos.
- [#24](https://github.com/thalesfb/ccw/issues/24): escopo, capítulos,
  linguagem PRISMA e distinção entre realizado, demonstrado e proposto
  continuam sujeitos à revisão científica.
- [#25](https://github.com/thalesfb/ccw/issues/25): o título final depende da
  decisão de escopo e não é resolvido por uma melhoria visual.
- [#26](https://github.com/thalesfb/ccw/issues/26) e
  [#29](https://github.com/thalesfb/ccw/issues/29): atualização de literatura,
  protocolo e adjudicação não devem ser inferidos do deck.
- [#28](https://github.com/thalesfb/ccw/issues/28) e
  [#7](https://github.com/thalesfb/ccw/issues/7): harness e protótipo não são
  declarados executados apenas porque aparecem como próximos passos.

Assim, as issues permanecem abertas até que seus gates próprios tenham
evidência e aprovação. A apresentação documenta a pendência em vez de
transformá-la em resultado.
