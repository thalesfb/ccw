# Apresentação Slidev do TCC

> **Versão para a defesa:** `slides.md` é o arquivo que será usado na defesa
> (banca prevista para 03/12/2026). A capa indica que a apreciação MMAT é
> preliminar enquanto a conferência pelo autor não terminar. O Slidev, o
> storyboard e o PPTX ainda descrevem a seleção histórica de 15 estudos sob o
> corte 4,0. O fluxo foi reconciliado em 31/10/2026; esta correção registra
> somente o conjunto atual.

## Arquivo da defesa

`slides.md` é o deck canônico da defesa, em revisão até a atualização final: contém 25 slides, incluindo a capa, e
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
reconciliação de 31/10/2026 estão atualizados. A síntese descreve os 15 estudos
selecionados historicamente sob o corte 4,0. Não houve mudança do corte,
nova seleção ou incorporação de estudos adicionais. Os materiais deixam de
ser identificados como rascunho; a apreciação MMAT segue indicada como
preliminar até a conferência pelo autor.

## Sequência da defesa (11/2026)

A sequência atual dá mais peso aos resultados de cada objetivo e às regras
propostas: problema de pesquisa desdobrado por objetivo, base didática (Duval
e Brousseau), corte 4,0 com a exploração abaixo dele, tipologia do OE1, lacunas
de relato e eixos de risco do OE2, cadeia de rastreabilidade, saída fictícia
com intervalo de Wilson, regras do OE3 e do OE4 e conclusão com as
contribuições. O gráfico de etiquetas de técnicas de todos os registros e o
histograma de relevância saíram do deck porque não descreviam os 15 estudos;
os slides de resultado são desenhados em HTML a partir das tabelas do TCC.

## Objetivos de referência do manuscrito

Os slides resumem os objetivos para leitura em apresentação, sem mudar seu
sentido. A transcrição abaixo é gerada do TCC, não do roteiro de fala.

<!-- ccw-sync:start goals -->
### Objetivo geral

Propor uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática, fundamentada no mapeamento e na análise da literatura científica. Neste trabalho, o apoio à interpretação docente delimita-se à apresentação, ao professor, de indicadores pontuais de evidência e de incerteza produzidos pelo protótipo a partir de tarefas específicas, incluindo a média das probabilidades previstas, sem intervalo próprio, e a taxa de acertos observada com intervalo de Wilson, por estudante e habilidade; não abrange o acompanhamento longitudinal de trajetórias de aprendizagem nem dispensa o julgamento pedagógico do professor.

### Objetivos específicos

**OE1:** categorizar as abordagens e técnicas computacionais e as finalidades pedagógicas descritas na literatura mapeada.

**OE2:** identificar, por codificação sistemática, limitações metodológicas e de relato e discutir conceitualmente dimensões técnicas, pedagógicas e éticas no material examinado.

**OE3:** formular a especificação técnica e pedagógica do protótipo, incluindo requisitos, critérios para seleção de fontes de dados e modelos e uma arquitetura de referência.

**OE4:** propor um protocolo para avaliar a viabilidade e a coerência da especificação conceitual, considerando sua fundamentação, a consistência dos requisitos e as condições técnicas e pedagógicas de execução.
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

- na seleção histórica sob o corte 4,0, dos 18 registros do MMAT, 15 estudos
  empíricos foram mantidos; um registro foi excluído após o resumo, dois dos 17
  relatórios procurados não foram recuperados, 15 foram avaliados em texto
  completo, um protocolo foi excluído e 14 relatórios empíricos foram recuperados;
  Sokkhey permanece entre os 15 apenas como inclusão histórica sem cópia verificável;
- o MMAT desse recorte histórico é preliminar: a busca tem data de corte em
  31/08/2026 e o recorte foi reconciliado em 20/10/2026; 15 estudos têm
  triagem S1/S2 e apreciação preliminar dos critérios por categoria, incluindo
  as rotas operacionais dos estudos 5, 7, 8 e 14. Não há nota média ou ranking;
- as frequências técnicas descrevem a seleção histórica após deduplicação,
  não uma síntese de eficácia nem um corpus final;
- referências teóricas, pedagógicas, metodológicas e técnicas do TCC permanecem
  separadas das referências derivadas do pipeline.
