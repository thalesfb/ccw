# Reconciliação de metadados: Käser Jacober

**Data do snapshot auditado:** 31/08/2026

**Escopo deste registro:** proveniência do metadado bibliográfico; nenhuma decisão de inclusão é aplicada por este documento.

## Resultado da investigação

O registro operacional 6918 foi inserido pelo fluxo normal da fonte CORE, na consulta `mathematics AND student modeling AND learning`. Não foi encontrada evidência de inserção manual ou de *override* para esse registro.

O payload bruto armazenado pela CORE identificava:

- título: *Modeling and Optimizing Computer-Assisted Mathematics Learning in Children*;
- autora: Käser Jacober, Tanja;
- DOI: `10.3929/ethz-a-010265296`;
- identificador CORE: `339157722`;
- `yearPublished`: `2025`;
- `publishedDate`: ausente;
- tipo documental: tese.

O registro correspondente na [ETH Research Collection](https://www.research-collection.ethz.ch/handle/20.500.11850/154763) confirma o mesmo título, autora e DOI, mas data a tese de **2014**.

## Ponto de divergência

A primeira divergência observável ocorre no metadado fornecido pela CORE, antes da normalização local. O normalizador apenas copia `yearPublished` para o campo `year`; como o valor recebido era 2025, o registro satisfez o filtro operacional de 2015–2026.

Assim, não há evidência de que o filtro temporal tenha sido deliberadamente ignorado. Há, sim, uma limitação de confiabilidade: o filtro tratou o ano de uma fonte agregadora como suficiente, sem uma verificação independente para conflitos bibliográficos.

## Situação científica

O recorte da revisão permanece 2015–2026. Portanto, a confirmação de 2014 impede que este registro seja tratado automaticamente como estudo elegível dentro desse recorte. A decisão final de escopo deve ser registrada antes de atualizar a síntese, o MMAT, os números PRISMA, as referências do TCC ou os artefatos publicados.

Este registro de auditoria não altera o número de estudos, não corrige os exports e não substitui a reexecução/validação do fluxo. Ele apenas preserva a evidência necessária para que a decisão posterior seja reproduzível, já que o SQLite local não é versionado.

## Lacunas e próximos controles

1. O payload original da CORE não está versionado fora do SQLite; o arquivo machine-readable deste PR preserva os campos essenciais da divergência.
2. A causa interna pela qual a CORE atribuiu 2025 não pode ser determinada somente pelo repositório; erro de indexação ou derivação de metadados permanece hipótese.
3. O pipeline deve validar o limite superior do intervalo e definir como tratar conflitos entre fontes antes de publicar uma síntese.
4. Um teste de regressão deve impedir que um conflito temporal conhecido seja apresentado como inclusão final.

## Limite deste PR

Este PR é deliberadamente atômico. Ele não modifica o manuscrito científico, a bibliografia, o MMAT, as contagens PRISMA, o SQLite, os CSV/JSON/HTML exportados ou a apresentação. Essas alterações dependem da reconciliação quantitativa e serão propostas em PRs separados.
