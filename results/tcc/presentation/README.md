# Export PowerPoint editável paralelo do TCC

> **Desatualizado para a defesa.** Este export e suas visualizações incorporadas
> refletem a seleção anterior à emenda aprovada em 31/10/2026. A elegibilidade
> ainda precisa ser reaplicada; não use estes números como corpus final nem
> apresente o arquivo até a atualização posterior à reaplicação.

Este diretório contém um artefato editável auxiliar, não a apresentação que
será usada na defesa do TCC **Ensino Personalizado de Matemática:
Oportunidades e Técnicas Computacionais**.

## Papéis dos artefatos

- [`presentation/slides.md`](../../../presentation/slides.md) é a fonte do deck
  canônico Slidev da defesa, com 25 slides. O build público fica em
  `presentation/dist/`.
- [`APRESENTACAO_TCC_SLIDES_CONTEUDO.md`](APRESENTACAO_TCC_SLIDES_CONTEUDO.md)
  é o storyboard de conteúdo de 25 slides associado ao deck Slidev; não é lido
  automaticamente pelo compilador.
- [`ensino_personalizado_de_matematica_tcc.pptx`](ensino_personalizado_de_matematica_tcc.pptx)
  é um export editável paralelo, com 19 slides, gerado independentemente. Não
  é o arquivo da defesa, não é derivado de `slides.md` e não é sincronizado com
  o deck canônico. A diferença de contagem é intencional entre artefatos com
  papéis distintos, não uma paridade de exportação pendente.
- [`ROTEIRO_FALAS_TCC.md`](ROTEIRO_FALAS_TCC.md) é um roteiro histórico do
  export paralelo, fora do escopo e da validação da versão semifinal atual;
  não deve ser usado como fonte do deck Slidev vigente.
- [`material de apresentação do PTC histórico`](../../../results/ptc/presentation/APRESENTACAO_SLIDES_CONTEUDO.md)
  é uma terceira apresentação, de uma etapa anterior. Serve como contexto
  narrativo e visual, nunca como fonte dos números do TCC vigente.
- [`generate_tcc_presentation.py`](../../../scripts/generate_tcc_presentation.py)
  define o conteúdo e o layout do PPTX paralelo. Não lê o storyboard, o roteiro
  de falas nem os arquivos TeX.

A fala não integra esta revisão semifinal. Sua preparação ocorrerá somente
após a revisão dos PRs e a validação da orientação, com base no conteúdo
aprovado.

Após merge e deploy bem-sucedido, os endereços públicos são:

- [apresentação Slidev](https://thalesfb.github.io/ccw/presentation/);
- [PPTX do TCC](https://thalesfb.github.io/ccw/results/tcc/presentation/ensino_personalizado_de_matematica_tcc.pptx);
- [PPTX histórico do PTC](https://thalesfb.github.io/ccw/results/ptc/presentation/ensino_personalizado_de_matematica.pptx).

Esses URLs descrevem o destino do artefato publicado; não confirmam que o
deploy já ocorreu.

## Regeneração e validação do export paralelo

Executados a partir da raiz do repositório:

```bash
python scripts/generate_tcc_presentation.py
python scripts/generate_tcc_presentation.py --check
```

O validador verifica os 19 slides do export, seus títulos, marcadores do
recorte versionado atual, exemplos de limitações vinculados a estudos, ausência de
números históricos do PTC e incorporação das visualizações canônicas. O
workflow `tcc-quality` também executa essa validação em pull requests.

## Proveniência do conteúdo

O conteúdo do TCC usa o texto atual em [`results/tcc/`](../) e os artefatos
versionados em [`research/exports/`](../../../research/exports/). As figuras
canônicas são incorporadas de
[`research/exports/visualizations/`](../../../research/exports/visualizations/).
O PTC histórico não é fonte desses dados. Referências teóricas, pedagógicas,
metodológicas e técnicas pertencem à bibliografia própria do TCC e permanecem
separadas das referências derivadas do pipeline.

O deck apresenta uma especificação conceitual, não uma aplicação funcional.
Não afirma treinamento com base definitiva, eficácia pedagógica ou validação
com participantes.
