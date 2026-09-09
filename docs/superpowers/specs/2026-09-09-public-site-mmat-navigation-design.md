# Especificação — portal público, navegação e MMAT vigente

**Data:** 2026-09-09
**Escopo:** `index.html`, `research/index.html`, páginas públicas de resultados,
artefatos MMAT e publicação GitHub Pages
**Status:** implementada neste PR, com validação pendente de revisão remota

## 1. Problema e objetivo

O portal público reúne a revisão sistemática, os resultados do PTC/TCC e a
apresentação, mas cada área possui uma linguagem visual e uma navegação própria.
O índice principal usa um gradiente genérico, cartões com hierarquia fraca e
links que misturam o estado atual com uma visualização histórica do MMAT. Isso
dificulta a leitura da evidência vigente e a circulação entre as páginas.

O objetivo é transformar o site em um portal acadêmico institucional claro,
rastreável e responsivo, mantendo a precisão científica do snapshot atual e
aproximando a identidade do portal da apresentação revisada.

## 2. Princípios e limites

- **Fonte de verdade científica:** os números do MMAT devem ser derivados de
  `research/data/mmat_reassessment_current.csv`, do registro de estudos e do
  manifesto de reprodutibilidade. A página não terá números digitados sem
  validação.
- **MMAT sem nota global:** a interface deve explicar os critérios S1/S2 e
  Q1–Q5 e os valores Y/N/CT, mas não calcular nota, percentual, ranking ou
  rótulo de qualidade agregado.
- **Estado honesto:** 18 registros no ledger atual, sendo 17 candidatos
  empíricos provisórios e um protocolo contextual; nove textos primários foram
  revisados externamente e oito registros ainda estão em nível de
  abstract/metadados. Recuperação de fontes, localizadores e adjudicação final
  permanecem pendentes.
- **Identidade institucional:** usar a marca oficial do IFC já versionada na
  apresentação e manter Asap/Barlow como referência tipográfica. A página não
  declara aprovação formal do manual de identidade nem conformidade integral
  com ABNT/IFC.
- **Preservação:** a visualização histórica do MMAT permanece acessível como
  proveniência, mas deve ser rotulada claramente como histórica e não vigente.
- **Escopo não incluído:** não alterar o protocolo científico, a seleção de
  estudos, os julgamentos MMAT, os exports de dados ou o conteúdo das issues.

## 3. Direção visual

Adotar uma linguagem editorial institucional, com mais espaço negativo e
hierarquia de informação:

- fundo claro/off-white, texto em azul-marinho quase preto e acentos IFC
  verde/vermelho usados com moderação;
- Asap para títulos e Barlow para corpo, números e navegação;
- cartões com bordas, estados e agrupamentos sem depender de gradientes;
- títulos curtos, labels de status e números grandes para o snapshot;
- emojis deixam de ser a principal linguagem de navegação; ícones decorativos
  podem permanecer quando têm `aria-hidden` e não substituem o texto;
- foco visível, alvos de toque adequados, contraste mínimo WCAG AA para texto
  normal e texto grande;
- comportamento responsivo para leitura em notebook, projetor e celular.

O resultado deve parecer um catálogo de pesquisa/relatório acadêmico, não uma
landing page promocional. O QR code da apresentação continua apontando para o
repositório canônico.

## 4. Arquitetura de navegação

Criar um shell visual compartilhado para as páginas mantidas pelo projeto:

1. **Visão geral** — `index.html`
2. **Revisão sistemática** — `research/index.html`
3. **MMAT atual** — nova página em
   `research/exports/analysis/mmat_current.html`
4. **Apresentação** — `presentation/`
5. **PTC** — `results/ptc/`
6. **TCC** — `results/tcc/`
7. **Repositório** — GitHub

O shell terá marca, navegação primária, estado ativo, breadcrumb ou contexto
da página e um rodapé com snapshot, fonte dos dados e retorno ao repositório.
Links para relatórios derivados e para a visualização histórica ficarão dentro
das páginas de pesquisa, em vez de competir com a navegação primária.

A implementação deve preferir CSS compartilhado e componentes estáticos
simples. Um script de navegação só será usado se reduzir duplicação sem criar
dependência de caminho absoluto específica do GitHub Pages. Todos os links
devem funcionar tanto no caminho publicado `/ccw/` quanto em preview local.

## 5. Página MMAT atual

A nova página terá quatro blocos:

### Cabeçalho de estado

Título “MMAT 2018 — apreciação preliminar por critérios”, data do snapshot,
badge “preliminar” e aviso destacado: “não é uma nota global nem um ranking”.

### Resumo auditável

Cards para 18 registros, 17 candidatos empíricos, 1 protocolo contextual, 9
textos primários revisados e 8 registros de abstract/metadados. Os valores
devem ser checados contra o CSV/manifesto durante o build ou validação.

### Método e tabela

Explicação curta dos critérios, da codificação Y/N/CT e da separação do
protocolo contextual. Tabela legível com identificador, título abreviado,
classificação, critérios e estado da fonte, com busca ou filtro somente se isso
não prejudicar a acessibilidade e a leitura em celular.

### Proveniência e pendências

Links para CSV, manifesto e repositório; seção explícita de pendências; link
separado para `mmat_visualization.html`, identificado como “visualização
histórica — 17 estudos”.

## 6. Alterações no índice e nas páginas existentes

- Substituir o link principal “MMAT histórico (referência)” por “MMAT atual —
  apreciação preliminar”.
- Manter a referência histórica como link secundário e com o rótulo correto.
- Transformar os números do índice em um snapshot com status e data de corte,
  evitando que “MMAT agregado (não calculado)” pareça uma métrica faltante a
  ser preenchida automaticamente.
- Aplicar o shell visual e a folha de estilos compartilhada ao índice de
  pesquisa e às páginas PTC/TCC sem reescrever o conteúdo científico.
- Corrigir problemas de codificação de caracteres nas páginas tocadas.
- Atualizar o workflow de Pages para copiar os novos assets e validar a
  presença da página MMAT atual.

## 7. Verificação e critérios de aceite

Antes de publicar:

- teste estático confirma os links primários, a página MMAT atual e a
  preservação da página histórica;
- teste de dados confirma os números e a ausência de nota/ranking global;
- validação confirma que o protocolo 6921 não entra na síntese empírica;
- build do site e do deck continuam passando;
- auditoria visual em viewport desktop e móvel verifica contraste, foco,
  overflow, leitura da tabela e navegação de retorno;
- workflow de GitHub Pages copia os assets e encontra todos os destinos;
- nenhum resultado científico novo é inferido pelo redesign.

## 8. Entrega incremental

1. adicionar a especificação e obter revisão;
2. implementar tokens, shell e página MMAT atual;
3. migrar índice, pesquisa e resultados para o shell;
4. validar localmente e publicar atualização no PR aberto;
5. revisar o site publicado e registrar eventuais pendências como issues, sem
   encerrar gates científicos ainda abertos.
