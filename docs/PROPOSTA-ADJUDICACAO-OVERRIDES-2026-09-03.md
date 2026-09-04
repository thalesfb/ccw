# Adjudicação dos overrides da revisão sistemática

**Data da proposta:** 03/09/2026
**Status:** decisões aprovadas e implementadas no PR #55

> Este documento preserva a justificativa que foi submetida à revisão. A fonte
> normativa da população vigente é o ledger
> `research/data/adjudicated_population_decisions.csv`; os artefatos derivados
> foram regenerados após a aprovação.

## Objetivo

Esta proposta aplica as regras versionadas em
`research/data/current_eligibility_protocol.csv` aos sete registros excluídos
manualmente no snapshot de 31/08/2026. A análise separa elegibilidade,
classificação documental e avaliação metodológica. Uma recomendação de
inclusão não equivale a uma aprovação de qualidade pelo MMAT; uma recomendação
de exclusão não deve ser justificada pelo score do pipeline.

As fontes indicadas são as páginas publicadoras ou institucionais dos próprios
registros. Quando o texto completo não foi recuperado, a limitação permanece
registrada e impede qualquer afirmação metodológica além do que a fonte
permite verificar.

## Decisões aplicadas

| Registro | Disposição aplicada | Fundamento de elegibilidade | Evidência verificável | Efeito no snapshot |
| --- | --- | --- | --- | --- |
| 14 | `include` | Matemática é o domínio central; a animação computacional é uma intervenção educacional ativa e avaliada, ainda que não seja ML. | O registro publicador descreve estudo quase experimental sobre teoremas de círculo, grupos experimental e controle, pré/pós-teste e análise de Mann–Whitney. [Fonte publicadora](https://journals.eduped.org/index.php/IJMME/article/view/1299) | Adicionar à população empírica, com a técnica classificada como tecnologia educacional computacional. |
| 15 | `exclude` | Não há técnica computacional aplicada e avaliada; referências a comunicação digital não satisfazem `computational_centrality`. | O PDF relata entrevistas semiestruturadas e vídeos de sala com professores de matemática e ciências, sem intervenção computacional avaliada. [PDF publicador](https://pdf.ejmse.com/EJMSE_5_2_93.pdf) | Permanecer fora da síntese empírica por escopo, não por score. |
| 6915 | `include` | Matemática é o domínio central e a fonte relata modelos preditivos de IA, resultados concluídos e validação em sala de aula. | O artigo publicador informa nove modelos, análise de 423 publicações e experimento controlado em escola. [Fonte Springer](https://link.springer.com/article/10.1186/s40561-025-00415-z) | Adicionar como estudo publicado com síntese secundária e validação própria; as 423 publicações subjacentes não devem ser contadas como 423 estudos adicionais sem extração independente. |
| 6918 | `exclude_temporal` | A fonte institucional identifica a tese como publicação de 2014, fora do recorte 2015–2026. | O registro oficial da ETH deve prevalecer sobre o ano 2025 armazenado no snapshot operacional. [Registro institucional](https://www.research-collection.ethz.ch/handle/20.500.11850/154763) | Remover da população elegível; preservar a ocorrência na auditoria de metadados e corrigir o ano bibliográfico para 2014. |
| 6919 | `include` | Matemática universitária é parte substantiva do estudo; a proposta pedagógica integra técnicas computacionais avaliadas e apresenta resultados educacionais comparativos. | A página publicadora descreve ensino universitário de matemática, integração de Transformada de Fourier, desenho comparativo, questionários assistidos por IA e medidas multimodais. [Fonte publicadora](https://www.mdpi.com/2071-1050/18/4/1900) | Adicionar à população empírica; a recuperação do texto completo permanece necessária para a adjudicação detalhada do MMAT. |
| 6922 | `exclude_document_type` | O registro é relatório final de projeto. Pela regra de tipo documental, ele só poderia entrar na síntese se fossem verificadas uma publicação elegível e evidências empíricas concluídas e analisáveis. | O repositório institucional identifica o documento como relatório final do projeto Testbed Math, com atividades, casos e disseminação. [Repositório institucional](https://oa.tib.eu/renate/handle/123456789/32087) | Permanecer como registro contextual/auditável, sem MMAT empírico. |
| 6925 | `exclude_outcome_specificity` | O modelo é computacionalmente central, mas o desfecho dependente é uma competência STEM composta; a matemática não é apresentada como desfecho separável para a síntese atual. | O artigo define `STEM competencies` como a média das proficiências em matemática e ciências. [Fonte Springer](https://link.springer.com/article/10.1186/s40594-025-00590-y) | Excluir da síntese matemática específica; preservar como evidência contextual de ML em STEM, se necessário. |
| 6926 | `exclude_domain` | O domínio e o desfecho são educação moral; matemática aparece como variável preditora, não como intervenção, população ou resultado central. | O registro publicador descreve avaliação de ML para educação moral e usa matemática, leitura e escrita como preditores. [Identificador da publicação](https://doi.org/10.1016/j.aej.2025.03.095) | Permanecer fora da síntese matemática por centralidade de domínio. |

## Coerência com a população

As decisões foram aprovadas e o efeito aritmético observado sobre o snapshot
operacional anterior é:

```text
16 registros retidos
- 1 registro fora do recorte temporal (6918)
+ 3 registros elegíveis recuperados dos overrides (14, 6915, 6919)
= 18 registros retidos após a regeneração
```

O resultado é provisoriamente composto por 17 registros empíricos e um registro
contextual (6921). O `papers.csv`, o `summary.json`, o MMAT, as referências e as
figuras foram regenerados no PR #55. O TCC e a apresentação permanecem em
unidades posteriores e não são alterados por este documento.

## Limites da proposta

- A inclusão não implica que os estudos já tenham MMAT final ou que seus
  resultados sejam diretamente combináveis.
- O artigo 6915 exige uma regra explícita de unidade de síntese para evitar
  dupla contagem entre a meta-análise e os estudos que ela agregou.
- O artigo 6919 tem evidência suficiente para a decisão de escopo nesta
  proposta, mas seus detalhes metodológicos devem continuar pendentes no
  registro MMAT até que o texto completo seja arquivado ou revisado com
  localizadores adequados.
- Nenhum título bibliográfico é traduzido, reescrito ou usado como justificativa
  de elegibilidade.
