# Apresentação PowerPoint do TCC

Este diretório contém a apresentação editável do Trabalho de Conclusão de
Curso **Ensino Personalizado de Matemática: Oportunidades e Técnicas
Computacionais**.

## Artefatos

- [`ensino_personalizado_de_matematica_tcc.pptx`](ensino_personalizado_de_matematica_tcc.pptx): apresentação pronta para abrir no PowerPoint, LibreOffice Impress ou equivalente;
- [`APRESENTACAO_TCC_SLIDES_CONTEUDO.md`](APRESENTACAO_TCC_SLIDES_CONTEUDO.md): storyboard e fonte textual revisável;
- [`ROTEIRO_FALAS_TCC.md`](ROTEIRO_FALAS_TCC.md): roteiro de exposição, com tempo sugerido;
- [`../../../../scripts/generate_tcc_presentation.py`](../../../../scripts/generate_tcc_presentation.py): gerador e validador determinístico do deck.

## Regeneração e validação

Executados a partir da raiz do repositório:

```bash
python scripts/generate_tcc_presentation.py
python scripts/generate_tcc_presentation.py --check
```

O validador verifica o número e os títulos dos slides, os marcadores do
snapshot atual, a ausência de números históricos do PTC e a incorporação das
visualizações canônicas. O workflow `tcc-quality` também executa essa
validação em pull requests.

## Proveniência do conteúdo

O deck usa como fonte científica o texto atual em `results/tcc/` e os artefatos
versionados em `research/exports/`. As figuras de seleção e panorama são
incorporadas diretamente de `research/exports/visualizations/`; a arquitetura
é a figura conceitual já usada pelo TCC.

A apresentação existente em `results/ptc/presentation/` foi consultada apenas
como referência de narrativa e organização visual. Seus números e afirmações
históricas não são reutilizados. Referências teóricas, pedagógicas,
metodológicas e técnicas continuam pertencendo à bibliografia própria do TCC,
separada das referências derivadas do pipeline.

O deck apresenta uma especificação conceitual, não uma aplicação funcional.
Não afirma treinamento com base definitiva, eficácia pedagógica ou validação
com participantes.
