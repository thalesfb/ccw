# Apresentação Slidev do TCC

## Arquivo da defesa

`slides.md` é o deck canônico da defesa: contém 25 slides, incluindo a capa, e
é a fonte usada para compilar a apresentação pública. `results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md`
é o storyboard de 25 slides que documenta sua progressão; não é a fonte de
renderização.

O arquivo `results/tcc/presentation/ensino_personalizado_de_matematica_tcc.pptx`
é um export editável paralelo de 19 slides, gerado por outro script. Ele não é
o arquivo da defesa, não é exportado de `slides.md` e não permanece sincronizado
automaticamente. Para apresentar o TCC, use o deck Slidev.

O material em `results/ptc/presentation/` é uma terceira apresentação,
histórica, referente ao PTC. Serve apenas como referência narrativa e visual,
nunca como fonte dos números atuais do TCC.

O conteúdo quantitativo do deck canônico é validado contra
`research/exports/reports/summary.json`; as visualizações são cópias dos PNGs
versionados em `research/exports/visualizations`.

## Execução local

```bash
npm ci
npm run validate
npm run build -- --base /ccw/presentation/
```

O deck segue a direção visual do template fornecido, mas o arquivo PPTX
original é apenas referência local: a fonte de verdade continua sendo
`slides.md`. A marca institucional vem do ativo oficial do IFC Campus Videira
em `public/branding/`, e o QR do encerramento é regenerável com:

```bash
npm run generate:qr
```

O template fornecido foi auditado como referência visual: formato widescreen,
composição editorial clara, fundo claro e azul institucional. O deck Slidev
preserva essa gramática e usa a família Times compatível com o TCC
(Times New Roman/Nimbus Roman) para manter continuidade tipográfica com o
manuscrito.

A tipografia usa fontes locais, com `fonts.provider: none`, para não solicitar
Times New Roman a um provedor de fontes web. A configuração segue a
[documentação de fontes do Slidev](https://sli.dev/custom/config-fonts#providers).
Os fallbacks Times/Nimbus Roman continuam definidos no CSS; disponibilidade
tipográfica e legibilidade devem ser verificadas no ambiente de exportação.

O slide MMAT exibe agora as perguntas de triagem S1 e S2 e a legenda vigente
Y/N/CT, em vez de esconder essas perguntas sob uma abreviação. A fonte
científica continua sendo o ledger versionado; a apresentação não cria um
escore agregado.

As verificações editoriais, de identidade, QR, tipografia e contraste ficam em
`deck-standards.mjs` e são executadas por:

```bash
npm test
npm run validate
```

Após o merge, o workflow de publicação compila o deck e o disponibiliza em
`/ccw/presentation/`, sem exigir que o leitor execute comandos.

## Limites científicos

- os 18 registros retidos incluem 17 candidatos empíricos provisórios e um
  protocolo contextual;
- o MMAT atual é preliminar e não produz nota média ou ranking;
- as frequências técnicas são descritivas sobre o snapshot após deduplicação,
  não uma síntese de eficácia;
- referências teóricas, pedagógicas, metodológicas e técnicas do TCC permanecem
  separadas das referências derivadas do pipeline.
