# Auditoria dos estudos retidos na síntese do TCC

Este registro documenta o papel que cada estudo pode sustentar no TCC. Ele foi elaborado a partir de `research/data/current_synthesis_scope.csv` e `research/data/reference_audit.csv`, cujo snapshot vigente é de 3 de setembro de 2026. Não substitui a leitura dos textos primários, o MMAT ou a decisão de escopo do orientador.

A classificação abaixo separa quatro funções: **central**, quando o estudo sustenta diretamente uma afirmação da síntese; **específica**, quando sustenta apenas o resultado ou contexto que relata; **contextual**, quando informa uma decisão de projeto ou uma lacuna, sem sustentar eficácia; e **tangencial**, quando sua relação com o problema é indireta e não deve fundamentar conclusões centrais.

| Estudo | Papel atual e contribuição que pode sustentar | Limite de interpretação e ação necessária |
| --- | --- | --- |
| `Math2021_001` | Evidência específica sobre predição/classificação em dados educacionais de matemática. | A apreciação é limitada ao resumo/metadados; não usar métricas ou generalizações como evidência central antes da recuperação do texto primário. |
| `Implementation2025_000` | Estudo empírico diretamente relacionado a mineração de dados educacionais e predição de desempenho em matemática. | Pode ocupar posição central, mas a acurácia deve ser apresentada como resultado reportado pelo estudo, não como eficácia transferível. MMAT ainda é preliminar. |
| `Multimodels2020_002` | Comparação de modelos para desempenho em matemática; contribui para justificar comparação entre modelos candidatos. | A comparação não estabelece superioridade universal nem validade em outra população. Manter a dependência do contexto e do desenho. |
| `Analysis2022_003` | Contribui para discutir seleção de atributos e mineração de dados aplicada ao domínio matemático. | Usar como evidência específica do procedimento relatado; não converter seleção de atributos em explicação causal da aprendizagem. |
| `Design2025_004` | Contribui como contexto para trajetórias personalizadas e representação do estado do estudante. | Metadados e cautela editorial limitam afirmações de eficácia; não usar como prova isolada de que personalização melhora aprendizagem. |
| `Identifying2017_006` | Estudo específico de classificação com dados educacionais, útil para discutir identificação de padrões de desempenho. | A contribuição deve permanecer situada na população, instrumento e desfecho do artigo. Não extrapolar para diagnóstico geral. |
| `Innovative2023_005` | Contribui para o contexto de aplicação de IA no ensino superior de matemática. | Metadados e ano/edição ainda exigem confirmação na fonte publicadora antes de uso central. |
| `Computational2017_008` | Modelos de aprendizagem interativa para autoria de tutores e ajuste a dados humanos. O capítulo 5 aborda aritmética de frações, ligando a tese diretamente ao domínio matemático. | O trabalho reutiliza dados humanos e avalia simulações; não demonstra eficácia própria do protótipo do TCC. Comparações entre componentes exigem preservar tarefa e desenho, sem inferir equivalência com uma nova intervenção educacional prospectiva. |
| `Machine2019_007` | Trabalho em anais de congresso sobre análise preditiva em educação STEM. | O tipo documental não confirma, sozinho, o desenho empírico nem a contribuição específica para matemática. O texto completo continua necessário; não citar métricas ou resultados experimentais sem fonte primária. |
| `Machine2024_009` | Contribui com evidência específica sobre uso de aprendizado de máquina como apoio ao ensino de matemática. | O texto disponível é limitado; evitar generalização e registrar a necessidade de recuperação do texto completo. |
| `Enhancing2025_012` | Oferece contexto específico sobre recurso computacional e aprendizagem cooperativa em geometria. | O vínculo com o núcleo de modelagem computacional é indireto; tratar como evidência pedagógica contextual, não como prova de desempenho de ML. |
| `He2025_6915` | Contribui como estudo publicado sobre modelos preditivos e decisões em tecnologia educacional matemática. | As 423 publicações analisadas pelo artigo não são 423 estudos adicionais desta síntese. Usar o artigo como uma unidade e explicitar sua função secundária/meta-analítica. |
| `Villegas2025_6916` | Estudo diretamente relacionado a tutoria inteligente, adaptação e feedback personalizado. | Pode sustentar uma discussão central do desenho, condicionada à leitura metodológica e ao MMAT; a referência foi normalizada para *Smart Learning Environments*. |
| `Ozseven2026_6917` | Contribui com evidência específica sobre modelagem híbrida/neuro-fuzzy em educação matemática. | A confirmação editorial e a apreciação metodológica ainda são preliminares; não apresentar o modelo como alternativa validada para o protótipo. |
| `UniversityMathematics2026_6919` | Contribui para contexto de aplicação de matemática universitária e sustentabilidade. | A relação com personalização e diagnóstico computacional é tangencial; reavaliar sua permanência na síntese central após decisão do orientador. |
| `Echeveria2025_6920` | Contribui com um caso específico de classificação relacionado a mentalidade matemática e intervenção precoce. | Manter cautela editorial e metodológica; não transformar o resultado de classificação em medida geral de aprendizagem. |
| `Imperatrice2025_6921` | Protocolo/proposta contextual útil para rastreabilidade do mapeamento. | Não é evidência empírica, não integra a síntese de eficácia e não recebe MMAT empírico. Deve permanecer explicitamente separado dos 17 candidatos empíricos. |
| `Zeng2025_6923` | Contribui para discutir sinais multimodais, carga cognitiva e requisitos de dados/interação. | A relação com ensino personalizado é indireta e a apreciação é limitada; usar somente como contexto de instrumentação e lacuna. |

## Regra de uso no texto e na apresentação

Nenhum estudo desta lista, isoladamente, sustenta eficácia educacional geral, superioridade de algoritmo ou validade de um protótipo ainda não executado em base real. Afirmações quantitativas devem permanecer atribuídas ao artigo que as reportou e acompanhadas da população, do desfecho e da limitação documental correspondente. A composição de 18 registros é uma retenção operacional: 17 candidatos empíricos provisórios e 1 registro contextual.

Antes de uma versão final, devem ser consolidados a recuperação dos textos primários, os localizadores de evidência, a confirmação dos metadados pendentes e a adjudicação do MMAT. Até lá, o vocabulário correto é “candidato empírico provisório”, “resultado reportado” e “evidência disponível”, e não “estudo validado” ou “eficácia demonstrada”.

## Conferência adicional de fontes primárias

Em 8 de outubro de 2026, a recuperação documental produziu nove PDFs locais:
oito candidatos empíricos e o protocolo contextual. O manifesto
`research/data/evidence_sources_current.json` registra os 18 IDs do escopo,
endereços públicos, êxitos e falhas de recuperação, quantidade de páginas e
hashes dos arquivos obtidos. A correspondência de título ou DOI é uma
verificação de identidade documental, não aprovação metodológica. A conferência
humana final e a adjudicação continuam pendentes. Os PDFs, os textos integrais
e o índice SQLite permanecem em cache operacional não versionado.

| Registro | Fonte disponível nesta execução e contribuição delimitada |
| --- | --- |
| `Math2021_001` | Texto integral não recuperado. Mantém-se o limite de resumo/metadados; não acrescentar métricas ou procedimentos não verificados. |
| `Implementation2025_000` | PDF, 10 páginas. Páginas físicas 2–3: nota escolar, 280 estudantes e divisão 70/30. Página 7: 75% de acurácia de teste e revocação de 43% para a classe baixa. Sustenta resultado preditivo situado, não eficácia de intervenção. |
| `Multimodels2020_002` | PDF não recuperado; houve falha no espelho registrado e timeout na conexão local à editora. O [registro oficial](https://ieiespc.org/ieiespc/ArticleDetail/RD_R/397270) confirma título, autores, DOI e páginas 217–229; o resumo descreve classificação de desempenho em escolas cambojanas. Métricas e procedimento completo continuam sem nova confirmação por página. |
| `Analysis2022_003` | Texto integral não recuperado; falha de acesso ao endereço registrado. Não confirmar prevenção de vazamento ou validade dos atributos apenas pelos metadados. |
| `Design2025_004` | Texto integral não recuperado. Otimização de trajetórias é finalidade reportada, não ganho de aprendizagem confirmado. |
| `Identifying2017_006` | PDF, 20 páginas. Estudo de classificação com TIMSS 2011 na Turquia. O resultado depende do alvo, da população e da métrica; não equivale à validação de diagnóstico longitudinal. A classificação reportada não torna confiança do estudante uma causa demonstrada do desempenho. |
| `Innovative2023_005` | Texto integral não recuperado. Mantêm-se as pendências de metadados editoriais e de pertinência já registradas. |
| `Computational2017_008` | PDF, 108 páginas. Páginas físicas 60 e 64 (impressas 44 e 48): simulações em tarefas de frações com registros preexistentes do DataShop para 79 estudantes; os efeitos instrucionais são previstos qualitativamente, não como escores absolutos. Na p. 48, a tese reporta, para dois modelos mistos binomiais, AIC 9.512,8/9.521,3, BIC 9.566,7/9.575,2 e teste de razão de verossimilhança χ²(0) = 8,49, p < 0,01. A auditoria não reavaliou a inferência porque não dispõe das especificações completas dos modelos nem do código original; registra o resultado como reportado, sem tratá-lo como evidência estatística validada ou declará-lo inválido. Página física 72 (impressa 56): análise distinta de equações com 71 estudantes e 10.052 passos disponíveis; 4.568 passos em que os estudantes executaram as próprias ações formaram o subconjunto analisado, enquanto tarefas de estratégia em que o tutor realizava as transformações ficaram fora desse recorte. A tese contribui como referência conceitual e metodológica situada, não como evidência de eficácia universal de tutoria. A revisão integral de todos os componentes continua pendente. |
| `Machine2019_007` | Texto integral não recuperado. A entrada bibliográfica e os metadados identificam um trabalho nos anais do EDUCON 2019, não uma comprovação do delineamento. A natureza da investigação e os resultados continuam exigindo conferência; não usar como resultado experimental independente. |
| `Machine2024_009` | Texto integral não recuperado; falha de acesso ao endereço registrado. Não conferir precisão, desenho ou transferibilidade somente por título e resumo. |
| `Enhancing2025_012` | PDF, 22 páginas. Página física 15 (impressa 105): diferença entre grupos já no pré-teste. Sustenta discussão de animação com aprendizagem cooperativa, não seleção de algoritmo ML nem efeito isolado da animação. |
| `He2025_6915` | PDF, 42 páginas. Páginas físicas 1, 16 e 31–35 distinguem meta-análise, predição de efeitos e comparação escolar. As 423 publicações são dados do artigo, não novas inclusões no TCC. A distribuição de professores entre braços limita a inferência causal; categoria MMAT e unidade de apreciação requerem adjudicação. |
| `Villegas2025_6916` | PDF, 31 páginas. Páginas físicas 14 e 22 descrevem seis semanas e resultados até a oitava semana, sem conciliação no relato examinado. Pode informar requisitos de feedback e adaptação, mas não sustenta um cronograma único ou eficácia transferível ao protótipo. |
| `Ozseven2026_6917` | PDF, 17 páginas. Modelagem de dados ASSISTments com regras neuro-fuzzy e classificadores; contribuição é uma alternativa reportada, não um algoritmo já escolhido ou validado neste projeto. A auditoria de atributos históricos e particionamento permanece necessária antes de aproveitar o protocolo experimental. |
| `UniversityMathematics2026_6919` | Texto integral não recuperado; falha de acesso ao endereço registrado. Relação tangencial ao problema principal e permanência na síntese central continuam sujeitas à decisão de escopo. |
| `Echeveria2025_6920` | PDF, 13 páginas. Página física 7 (impressa 69): 633 recrutados e 428 com dados completos; construção de categorias e seleção de oito itens da escala de mentalidade. A sobreposição entre indicadores do alvo e preditores limita a leitura como diagnóstico independente. Não demonstra efeito de intervenção precoce. |
| `Imperatrice2025_6921` | PDF, 8 páginas. Página física 1 apresenta um piloto futuro; permanece protocolo contextual, fora da síntese empírica e da apreciação MMAT empírica. |
| `Zeng2025_6923` | Texto integral não recuperado. Permanece contexto de instrumentação multimodal; não confirmar reconhecimento de carga cognitiva como diagnóstico geral de aprendizagem. |

Uma reexecução de integridade dos nove PDFs recuperados conferiu 434 trechos
com `pypdf` 6.19.0 e `fontTools` 4.66.1, sem divergências entre conteúdo,
página física e hashes. A versão histórica de `fontTools` não havia sido
registrada no manifesto original; portanto, essa combinação é identificada
como ambiente de reprodução verificado, não como confirmação retrospectiva da
instalação usada na extração inicial. O resultado comprova a rastreabilidade
técnica nesta configuração, mas não resolve a confirmação editorial das fontes
nem substitui a apreciação científica humana.

Os oito registros de afirmação–evidência em
`research/data/claim_evidence_current.json` cobrem somente as afirmações
explicitamente confrontadas nesta rodada. O estado `SUPPORTED` documenta o
suporte ao relato atribuído, não certifica a validade do artigo. Não representa
conclusão da revisão profunda de todo o manuscrito, apreciação independente
humana ou encerramento das pendências do MMAT.
