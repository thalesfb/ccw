# Apresentação Slidev do TCC

> **Rascunho fora de uso na defesa:** o Slidev, o storyboard e o PPTX ainda
> descrevem a seleção de 15 estudos anterior à emenda. O fluxo histórico foi
> reconciliado em 31/10/2026, mas a regra aprovada ainda aguarda reaplicação
> uniforme; não use estes materiais na defesa antes da atualização do corpus.

## Arquivo da defesa

`slides.md` é o deck canônico da defesa: contém 25 slides, incluindo a capa, e
é a fonte usada para compilar a apresentação pública. `results/tcc/presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md`
é o storyboard de 25 slides que documenta sua progressão; não é a fonte de
renderização.

O arquivo `results/tcc/presentation/ensino_personalizado_de_matematica_tcc.pptx`
é um export editável paralelo de 19 slides, gerado por outro script. Ele não é
o arquivo da defesa, não é exportado de `slides.md` e não permanece sincronizado
automaticamente. Isso não autoriza divergências científicas: mudanças no TCC
exigem conferir os resumos do Slidev, do storyboard e do export paralelo, conforme
[`DOCUMENTATION_SYNC.md`](../docs/tcc/DOCUMENTATION_SYNC.md). Para apresentar o
TCC, use o deck Slidev.

A fala não integra esta revisão semifinal. Sua preparação ocorrerá somente
após a revisão dos PRs e a validação da orientação, com base no conteúdo
aprovado. O roteiro histórico do export paralelo não é fonte do deck vigente
nem evidência de sua atualização.

O material em `results/ptc/presentation/` é uma terceira apresentação,
histórica, referente ao PTC. Serve apenas como referência narrativa e visual,
nunca como fonte dos números atuais do TCC.

Os gráficos versionados, as contagens do fluxo histórico e as legendas da
reconciliação de 31/10/2026 estão atualizados. A síntese dos 15 estudos e outras
partes da narrativa ainda descrevem a seleção pré-emenda; devem ser revistas
depois da reaplicação uniforme do protocolo. Até lá, o conjunto não é corpus
final e os materiais continuam fora de uso na defesa.

## Objetivos de referência do manuscrito

Os slides resumem os objetivos para leitura em apresentação, sem mudar seu
sentido. A transcrição abaixo é gerada do TCC, não do roteiro de fala.

<!-- ccw-sync:start goals -->
### Objetivo geral

Propor uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática, fundamentada no mapeamento e na análise da literatura científica.

### Objetivos específicos

**OE1:** categorizar as abordagens e técnicas computacionais e as finalidades pedagógicas descritas na literatura mapeada.

**OE2:** identificar limitações e lacunas técnicas, pedagógicas, metodológicas e éticas no material examinado.

**OE3:** formular a especificação técnica e pedagógica do protótipo, incluindo requisitos, critérios para seleção de fontes de dados e modelos e uma arquitetura de referência.

**OE4:** propor um protocolo para avaliar a viabilidade e a coerência da especificação conceitual, considerando sua fundamentação, a consistência dos requisitos e as condições técnicas e pedagógicas de uma eventual execução.
<!-- ccw-sync:end goals -->

## Execução local

```bash
npm ci
npm test
npm run validate
npm run build -- --base /ccw/presentation/
```

Execute esses comandos dentro de `presentation/`. Use npm com o
`package-lock.json` versionado; não misture instalações npm e pnpm no mesmo
`node_modules`. O comando [`npm ci`](https://docs.npmjs.com/cli/v11/commands/npm-ci/)
reinstala as versões do arquivo de dependências sem reescrevê-lo.

Se o navegador registrar `Failed to patch FloatingVue` ao iniciar o deck,
reinstale com `npm ci` e repita os testes e a compilação antes de alterar
dependências. Uma instalação local com versões divergentes da CLI, do cliente
e da integração de tooltips reproduziu essa falha; a instalação limpa do
arquivo de dependências e a recompilação eliminaram o erro observado.
`test/tooltip-runtime.test.mjs` exercita a inicialização real da integração
desktop usada pelo cliente Slidev e rejeita erros capturados no console.
Esse teste não monta o deck nem substitui a verificação no navegador: após
recompilar, recarregue a página e confira console, navegação, imagens e QR.
Se o erro persistir com a instalação limpa, preserve a mensagem e investigue
a compatibilidade das dependências, sem ocultar o erro nem desativar tooltips.

## Verificação visual em janelas menores

O Slidev usa um [canvas de largura fixa e proporção definida](https://sli.dev/custom/#slides-deck-configs),
redimensionado para caber na janela. A composição dos slides não deve mudar
para uma coluna por causa da largura externa do navegador; essa mudança faz
o conteúdo ultrapassar o palco, inclusive nas miniaturas do apresentador.

Após alterar os estilos, confira o build em janelas de 1280 × 720 e
860 × 1004 pixels. No slide MMAT, S1/S2 e a legenda Y/N/CT devem ficar
inteiramente acima do rodapé de estado preliminar e dentro do slide.
Confira também as demais rotas, os gráficos, o menu e o encerramento com QR.
O tamanho da janela deve alterar a escala, não a ordem ou o número de colunas
da composição. Esses critérios exigem inspeção no navegador; os testes Node
não verificam posicionamento visual.

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

Os títulos usam o peso negrito 700, espaçamento natural entre letras e
entrelinha mínima de 1,12. Não reutilize o espaçamento negativo da composição
sans-serif anterior com Times: essa combinação comprime e sobrepõe glifos.
No funil da seleção, o recorte dos trapézios se aplica apenas ao fundo
decorativo, nunca ao texto. Confira as legendas completas, inclusive a etapa
com 18 registros, no navegador e no PDF exportado.

O rodapé do fluxo é conciso e seu painel central pode encolher dentro do palco,
sem reduzir o corpo da fonte. A retenção explicita os quatro destinos dos 18
registros: 15 + 1 + 1 + 1. Ressalvas científicas após o título não recebem a
opacidade reduzida do tema padrão; sua leitura integra a revisão visual do PDF.

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

- na seleção histórica anterior à emenda, dos 18 registros do MMAT, 15 estudos
  empíricos foram selecionados, um relatório não foi recuperado, um registro foi
  excluído após o resumo e um protocolo sem resultados concluídos após o texto
  completo; essa seleção não é o corpus final;
- o MMAT desse recorte histórico é preliminar: a busca tem data de corte em
  31/08/2026 e o recorte foi reconciliado em 20/10/2026; 15 estudos têm
  triagem S1/S2 e apreciação dos critérios por categoria; o estudo 8 ainda
  aguarda adjudicação humana. Não há nota média ou ranking, e a reaplicação da
  elegibilidade após a emenda continua pendente;
- as frequências técnicas descrevem o snapshot histórico após deduplicação,
  não uma síntese de eficácia nem o corpus após a emenda;
- referências teóricas, pedagógicas, metodológicas e técnicas do TCC permanecem
  separadas das referências derivadas do pipeline.
