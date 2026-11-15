# Imagens do TCC

O infográfico de visão geral usado pelo README é
[`project_overview_2026-11-15.png`](project_overview_2026-11-15.png), gerado por
[`scripts/generate_project_overview.py`](../../../scripts/generate_project_overview.py)
a partir do fluxo versionado, da matriz MMAT vigente, do registro público de
estado e dos 26 grupos de requisitos. Ele distingue a seleção histórica de 15
estudos dos 14 relatórios empíricos recuperados e das 14 apreciações atuais por
critério; não atribui respostas MMAT atuais a Sokkhey nem inclui Zeng na seleção.
O quadro não apresenta escore agregado e não certifica eficácia educacional.

Os arquivos `project_overview_2026-10-20.png`,
`project_overview_2026-11-03.png` e `project_overview_current.png` foram
preservados como registros históricos e não devem ser reutilizados como visão
vigente.

As seis visualizações canônicas da revisão são copiadas de
`research/exports/visualizations/` pelo sincronizador de ativos derivados.
O infográfico é gerado separadamente e sua atualização deve passar pela checagem
`python scripts/generate_project_overview.py --check`. Alterações no TCC e nos
dados exigem conferência textual e visual conforme o
[contrato de sincronização](../../../docs/tcc/DOCUMENTATION_SYNC.md).
