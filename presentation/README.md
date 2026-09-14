# Apresentação Slidev do TCC

Esta apresentação é uma demonstração pública e resumida do TCC. O conteúdo
quantitativo é validado contra `research/exports/reports/summary.json`; as
visualizações são cópias dos PNGs versionados em `research/exports/visualizations`.
O deck vigente tem 25 slides; esse número é validado por `npm run validate`.

O PPTX/PDF em `results/ptc/presentation/` foi consultado apenas como referência
narrativa e visual. Ele contém uma apresentação histórica rasterizada e não é
fonte dos números atuais. O deck atual não reproduz as contagens históricas
da apresentação do PTC.

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
composição editorial clara, fundo claro e azul institucional. A apresentação
preserva essa gramática e usa a família Times compatível com o TCC
(Times New Roman/Nimbus Roman) para manter continuidade tipográfica com o
manuscrito. Isso não torna o PPTX de 19 slides equivalente ao deck canônico de
25 slides.

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
