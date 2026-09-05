# Apresentação Slidev do TCC

Esta apresentação é uma demonstração pública e resumida do TCC. O conteúdo
quantitativo é validado contra `research/exports/reports/summary.json`; as
visualizações são cópias dos PNGs versionados em `research/exports/visualizations`.

O PPTX/PDF em `results/ptc/presentation/` foi consultado apenas como referência
narrativa e visual. Ele contém uma apresentação histórica rasterizada e não é
fonte dos números atuais. O deck atual não reproduz afirmações históricas sobre
9.431 registros, 2.517 duplicatas ou 17 incluídos.

## Execução local

```bash
npm ci
npm run validate
npm run build -- --base /ccw/presentation/
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
