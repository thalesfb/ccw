# Protocolo para atualização futura da revisão sistemática

## Princípio

A revisão já documentada no TCC constitui uma etapa concluída e será preservada como baseline. Uma nova execução não poderá sobrescrever silenciosamente o banco, os 17 estudos incluídos, o fluxo PRISMA, a avaliação MMAT ou os artefatos utilizados na redação.

A atualização será tratada como uma **revisão sistemática de atualização**. O objetivo será determinar se publicações posteriores ou registros anteriormente não recuperados modificam a síntese, as lacunas ou as decisões do protótipo.

## Congelamento do estado atual

O arquivo `research/config/review_baseline.json` declara:

- commit de origem;
- corpus dos 17 estudos;
- artefatos metodológicos e analíticos;
- contagens relatadas;
- fontes consultadas;
- limiar de relevância;
- política de atualização;
- divergências que precisam ser resolvidas antes da nova busca.

O manifesto de conteúdo é produzido por:

```bash
cd research
python -m src.validation.review_baseline freeze \
  --config config/review_baseline.json \
  --repository-root .. \
  --output baselines/systematic-review-2025-11-25.manifest.json
```

O manifesto registra SHA-256, tamanho e contagens de cada artefato, além da identidade bibliográfica dos estudos. Depois de gerado no commit declarado, deve ser revisado e versionado em um PR próprio.

## Divergência temporal conhecida

Há uma divergência histórica que não será ocultada:

- a metodologia consolidada informa período de 2016 a 2025;
- o README histórico informa 2015 a 2025.

Antes da atualização, uma única janela deverá ser escolhida e justificada. A execução futura não poderá deduzir automaticamente o limite inferior a partir de documentação conflitante.

## Etapas da atualização

### 1. Validar o baseline

```bash
python -m src.validation.review_baseline verify \
  --manifest baselines/systematic-review-2025-11-25.manifest.json \
  --repository-root ..
```

Qualquer divergência interrompe a atualização até que se determine se houve alteração autorizada ou perda de artefato.

### 2. Criar uma execução independente

A nova busca deverá usar:

- banco ou namespace próprio;
- cache separado ou versionado;
- diretório de exportação específico;
- data e commit registrados;
- configurações explícitas;
- sobreposição temporal mínima para reduzir perda na fronteira;
- mesmas fontes originais quando ainda disponíveis;
- relatório de indisponibilidade ou mudança de API.

A atualização não deve reutilizar contadores mutáveis do banco atual como se fossem resultados do baseline.

### 3. Deduplicar em duas camadas

A deduplicação ocorrerá:

1. dentro da nova execução;
2. entre o novo corpus e o baseline congelado.

A identidade principal será DOI normalizado. Na ausência de DOI, será utilizada combinação auditável de título normalizado e ano, seguida de revisão manual dos casos incertos.

### 4. Comparar os corpora

Depois da triagem e exportação do corpus candidato:

```bash
python -m src.validation.review_baseline compare \
  --baseline baselines/systematic-review-2025-11-25.manifest.json \
  --candidate-bib updates/2026/included_papers.bib \
  --output updates/2026/corpus_comparison.json
```

O relatório separa:

- estudos adicionados;
- estudos removidos;
- registros bibliograficamente alterados;
- estudos inalterados.

Um estudo não será removido do histórico apenas porque deixou de aparecer na nova API. Remoções precisam de justificativa explícita, como correção de duplicidade, retração ou erro de elegibilidade.

### 5. Avaliar qualidade e impacto

Cada estudo novo deverá passar pelos mesmos critérios de elegibilidade e por avaliação metodológica compatível com o MMAT.

A atualização também deverá responder:

- surgiram métodos ou bases de dados não contemplados?
- as evidências alteram a escolha da variável-alvo?
- alteram a base principal ou os modelos de referência?
- modificam requisitos éticos, de explicabilidade ou avaliação?
- contradizem conclusões anteriores?
- justificam modificar o protótipo já implementado?

A existência de publicações novas não implica automaticamente mudança de decisão.

### 6. Produzir uma nota de atualização

A nota de atualização deverá conter:

- data da busca;
- janela temporal;
- alterações nas fontes e APIs;
- consultas executadas;
- fluxo PRISMA exclusivo da atualização;
- estudos novos e suas avaliações;
- comparação com o baseline;
- impacto ou ausência de impacto sobre o TCC.

## Momento adequado

A rerrodada será realizada somente depois de:

1. consolidar e revisar os PRs da etapa atual;
2. adquirir e validar a base do protótipo;
3. executar os baselines e o modelo candidato;
4. congelar os primeiros resultados técnicos;
5. avaliar se o prazo permite uma atualização completa e metodologicamente consistente.

Essa ordem evita que uma busca externa e mutável paralise o desenvolvimento principal ou faça o texto perder rastreabilidade.

## Proibições

- sobrescrever o baseline;
- alterar silenciosamente critérios ou limiares;
- misturar registros da atualização com contagens originais;
- apresentar estudos apenas recuperados como estudos incluídos;
- atualizar automaticamente capítulos do TCC;
- interpretar crescimento do número de publicações como melhora de qualidade;
- excluir estudo histórico somente porque uma API deixou de retorná-lo.
