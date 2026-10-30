# Base da síntese de conteúdo

Esta síntese usa os 15 estudos já incluídos em `current_synthesis_scope.csv`.
Não executa busca, modifica seleção ou altera respostas MMAT. As tabelas são
geradas por `python -m src.analysis.content_synthesis`, a partir de `research`;
`--check` compara a saída com os arquivos versionados.

`study_synthesis_current.csv` registra a leitura categorial por estudo. As
fontes são identificadas pela chave bibliográfica; a correspondência com DOI,
hash do PDF, cobertura e limites de leitura está em
`evidence_sources_current.json` e `study_contribution_current.json`. Os
localizadores da coluna `source` distinguem páginas físicas e impressas. A
codificação é uma síntese do autor, sujeita à revisão científica humana.

A finalidade principal corresponde ao componente matemático central examinado:
predição/classificação (8), personalização/STI (3), intervenção didática (2),
modelagem cognitiva (1) e integração curricular (1). Atividades secundárias não
criam novas inclusões. He é contado pela aplicação escolar, distinguindo a
predição de efeitos no mesmo relatório. MacLellan é contado uma vez, sem somar
domínios ou duplicar frações reutilizadas. Multimodels conserva a categoria
histórica e os campos não reconferidos; sua linha não deriva requisito técnico.

As métricas são atribuídas aos estudos, sem harmonização de alvos ou ranking.
Em Math, 78,39% preserva a denominação `macro-average` dos autores. Em
Innovative, gl=80 corresponde ao pré-teste (Tabela 2, página física 10);
o pós-teste tem gl=79 sob variâncias iguais (Tabela 6, página física 11).
Nenhum denominador é corrigido por suposição. Em Echeveria, 98,8% corresponde
à SVM; a divergência de totais está na matriz MLP.

As contagens MMAT usam os 15 estudos principais e discriminam categoria e
critério. Os seis componentes dos três mistos são contados separadamente.
Não há escore total ou equivalência entre posições Q/C de desenhos distintos.

As cinco referências de contexto acrescentadas têm verificação registrada em
`reference_audit.csv`: Opesemowo/Adewuyi (2024), Yi et al. (2025), Abdelrahman
et al. (2023), relatório técnico OECD (2024) e Resolução CNS 510/2016. Foram
consultadas as seções necessárias às afirmações utilizadas; para Yi, apenas
o resumo e os metadados publicados pelo editor. Elas não ampliam o corpus.
O ano de Yi segue o fascículo de 2025, embora publicado online em 2024. O
relatório OECD segue a citação oficial de 2024; o PDF atualmente disponibilizado
tem copyright de 2025. A comparação com revisões anteriores é de escopo e
forma de síntese, sem incorporar seus efeitos ou estudos às contagens do TCC.

Critérios funcionais, cenários, cinco docentes e regra de consenso do OE4 são
propostas de projeto. Os exemplos são fictícios. Não houve convite, coleta,
aprovação ética, execução do painel ou validação educacional nesta alteração.
