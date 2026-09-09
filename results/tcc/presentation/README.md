# Apresentação PowerPoint do TCC

Este diretório contém a apresentação editável do Trabalho de Conclusão de
Curso **Ensino Personalizado de Matemática: Oportunidades e Técnicas
Computacionais**.

## Fonte, exportação e material histórico

Os arquivos têm papéis diferentes e são mantidos em locais separados:

- [`presentation/slides.md`](../../../presentation/slides.md) é a fonte
  independente do deck público Slidev. O build gerado fica em
  `presentation/dist/`.
- O deck vigente do TCC tem 25 slides: essa contagem vale para `presentation/slides.md`
  e para o storyboard `APRESENTACAO_TCC_SLIDES_CONTEUDO.md`.
- [`ensino_personalizado_de_matematica_tcc.pptx`](ensino_personalizado_de_matematica_tcc.pptx)
  é um export editável paralelo, atualmente com 19 slides. Ele não é a fonte do
  deck Slidev e não deve ser usado para inferir a contagem do deck vigente.
- [`APRESENTACAO_TCC_SLIDES_CONTEUDO.md`](APRESENTACAO_TCC_SLIDES_CONTEUDO.md)
  é o storyboard textual de apoio do export PPTX; [`ROTEIRO_FALAS_TCC.md`](ROTEIRO_FALAS_TCC.md)
  contém as falas sugeridas. O gerador não lê esses arquivos automaticamente.
- [`material de apresentação do PTC histórico`](../../../results/ptc/presentation/APRESENTACAO_SLIDES_CONTEUDO.md)
  registra trabalho anterior. Serve para contexto narrativo e visual, não para
  números ou afirmações do TCC vigente.
- [`generate_tcc_presentation.py`](../../../scripts/generate_tcc_presentation.py)
  define conteúdo e layout do PPTX no próprio código, incorpora imagens
  versionadas e valida o arquivo. Não lê o storyboard nem arquivos TeX
  automaticamente.

Slidev e o gerador PPTX são fontes paralelas, sem sincronização automática.
Uma alteração em uma fonte pode deixar a outra desatualizada; a contagem de 19
slides do export editável é uma divergência conhecida que precisa ser resolvida
antes de tratá-lo como export equivalente ao deck vigente de 25 slides.

Após merge e deploy bem-sucedido, os endereços públicos são:

- [apresentação Slidev](https://thalesfb.github.io/ccw/presentation/);
- [PPTX do TCC](https://thalesfb.github.io/ccw/results/tcc/presentation/ensino_personalizado_de_matematica_tcc.pptx);
- [PPTX histórico do PTC](https://thalesfb.github.io/ccw/results/ptc/presentation/ensino_personalizado_de_matematica.pptx).

Esses URLs descrevem o destino do artefato publicado; não confirmam que o
deploy já ocorreu.

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
