# Correções normativas aplicadas ao TCC

**Estado:** adequação institucional parcial.

Este registro documenta somente correções verificáveis na camada de apresentação do
TCC. Ele não declara conformidade integral com a ABNT nem substitui a conferência
final do modelo e das instruções da Coordenação de TCC do IFC.

## Linha de base

- ABNT NBR 10520:2023, para citações;
- ABNT NBR 6023:2025, para referências;
- ABNT NBR 14724:2024, versão corrigida de 01.04.2025, para apresentação de
  trabalhos acadêmicos. A correção incorpora a Errata 1; não constitui uma norma
  denominada NBR 14724:2025.
- ABNT NBR 6028:2021, para resumos;
- ABNT NBR 6024:2012, para numeração progressiva das seções;
- ABNT NBR 6027:2012, para o sumário.

As versões e a aplicabilidade institucional devem ser confirmadas pelo canal do
Sistema Integrado de Bibliotecas do IFC e pela orientação. O regulamento do IFC
permite a adoção das normas ABNT ou de critérios definidos pela Coordenação de TCC.

## Correções aplicadas

- citações autor-data entre parênteses agora usam capitalização convencional, como
  `(Piaget, 1972)`;
- referências cujo endereço é DOI agora identificam o DOI separadamente, sem o
  rótulo `Disponível em`;
- URLs sem DOI recebem data de acesso registrada no BibTeX;
- título, autor e assunto foram declarados nos metadados do PDF;
- testes estáticos e compilação do TCC verificam essas propriedades.

## Capitalização de citações e títulos nas referências

São regras distintas e devem ser verificadas separadamente:

- nas citações autor-data entre parênteses, a NBR 10520:2023 usa a forma
  convencional do nome, como (Silva, 2023), em vez de colocar todo o sobrenome
  em caixa alta;
- na lista de referências, a NBR 6023:2025, seção 8.2, determina que título e
  subtítulo sejam reproduzidos como aparecem no documento consultado, separados
  por dois-pontos.

Por isso, não se deve converter em bloco os títulos das referências para Title
Case ou caixa alta. Cada título precisa ser conferido na fonte citada; a
capitalização de uma chamada autor-data não serve como evidência para alterar o
título bibliográfico. A [NBR 6023:2025](https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/149/2025/05/Referencias-NBR-6023-2025.pdf),
seção 8.2, é a fonte consultada para essa distinção.

## Conferência das versões em 8 de outubro de 2026

A identificação da NBR 14724 foi conferida no frontispício e no prefácio da
versão corrigida de 01.04.2025 (páginas físicas 1 e 4). A NBR 6023:2025 foi
conferida no frontispício e no prefácio (páginas físicas 1 e 5); corresponde à
edição de 2018 acrescida da Emenda 1 de 21.05.2025. Não foi encontrada nessa
consulta evidência de uma edição denominada NBR 14724:2026.

A [relação atualizada de normas da Biblioteca da UFES](https://biblioteca.ufes.br/normalizacao)
corrobora as versões de resumos, numeração e sumário acima e registra também a
NBR 15287:2025, específica para projetos de pesquisa. Esta última não substitui
automaticamente a NBR 14724 na apresentação do TCC concluído; o projeto
preparatório e o trabalho final são documentos distintos. Guias institucionais
anteriores às revisões de 2023–2025 devem ser lidos considerando essa diferença
de atualização, sem presumir que toda regra legada esteja vigente.

As seções 5.8 e 5.9 da NBR 14724 corrigida distinguem ilustrações, entre elas
quadros, e tabelas; exigem identificação e fonte, com remissão ao IBGE para
apresentação tabular. A conferência automatizada do projeto verifica a
classificação das listas e as propriedades declaradas de citações e referências.
Esses testes não certificam integralmente margens, espaçamentos, conteúdo ou
conformidade institucional. A conferência visual do PDF e a validação pelo canal
da biblioteca continuam necessárias, especialmente quanto aos elementos de
aprovação e catalogação.

Quanto ao alinhamento, a seção 5.8 exige que identificação, título, fonte,
legenda e notas acompanhem as margens da ilustração; não prescreve, por si só,
centralização nem alinhamento à esquerda. O template específico do curso para
TC tradicional (2026) configura as legendas com `\captionstyle[\raggedright]{}`;
essa configuração foi adotada no TCC como escolha do modelo institucional, não
como exigência atribuída à ABNT.

A NBR 10520:2023, seção 6.1.6, exige letras minúsculas após o ano para distinguir
documentos da mesma autoria publicados no mesmo ano. Como o TCC cita duas obras
de Brasil de 2018 — a BNCC e a LGPD —, a chamada `Brasil (2018a)` não deve ser
reduzida a `Brasil (2018)`; o sufixo evita ambiguidade e segue a ordem das
referências.

Foram consultadas as cópias institucionais da
[NBR 14724 corrigida](https://vigilanciasanitaria.prefeitura.rio/wp-content/uploads/sites/84/2025/10/ABNT-NBR-14724-2025-informacao-e-documentacao-trabalho-academico.pdf)
e da [NBR 6023:2025](https://www.fho.edu.br/assets/documentos/FHO_Biblioteca_Referencia_ABNT_6023_2025.pdf).
Os textos integrais das normas não são reproduzidos nem distribuídos no
repositório; o acesso institucional do IFC deve ser usado para a conferência
final. Esta é uma linha de base documentada, não uma certificação de vigência
obtida diretamente de todo o catálogo ABNT.

## Comparação com o template institucional

Em 14 de outubro de 2026, foram reconsultadas as páginas do [Sistema Integrado de
Bibliotecas do IFC](https://biblioteca.ifc.edu.br/tcc/), da [Biblioteca do Campus
Videira](https://videira.ifc.edu.br/biblioteca/trabalhos-de-conclusao-de-curso-tccs/)
e do [curso de Ciência da Computação](https://videira.ifc.edu.br/ciencia-da-computacao/defesas-de-tc/).
A orientação geral do SIBI, vinculada à Portaria Normativa nº 6/2022, pede a
logomarca institucional na capa e na folha de rosto. A página da Biblioteca do
Campus Videira ainda lista modelos de monografia de novembro de 2022. Já a página
do curso lista pacotes LaTeX de 2026 para TC tradicional e desenvolvimento de
software.

O item do curso identifica o primeiro pacote como ``TC – Trabalho de Conclusão
de Curso – TRADICIONAL'' e aponta para ``modelo-latex-ifc-TCC-Tradicional-2026.zip''.
O pacote tradicional foi comparado localmente em 14 de outubro de 2026. Seu
`config_inicial.tex` usa `\hangcaption` e `\captionstyle[\raggedright]{}`; o TCC
foi alinhado nesse ponto, sem substituir em bloco as adaptações e revisões já
incorporadas. A cópia local não foi comparada criptograficamente com o arquivo
remoto do Drive, cuja visualização solicita login. O pacote de desenvolvimento
também aponta para o Drive e não foi inspecionado. No pacote tradicional, a classe
usa o brasão da República na capa e não insere imagem na folha de rosto; a classe
local também mantém comentário relativo à NBR 6027:2012. Esses fatos descrevem os
arquivos examinados, mas não certificam conformidade integral.

Permanece uma divergência entre a orientação geral publicada pelo SIBI — logo do
IFC na capa e na folha de rosto — e o pacote específico do curso, que apresenta
brasão na capa e não inclui imagem na folha de rosto. A inspeção do pacote não
determina, por si só, se ele substitui ou atualiza a instrução geral para o
depósito. Conforme decisão pendente, a capa e a folha de rosto não foram alteradas;
a Coordenação, a Biblioteca ou a orientação deve confirmar qual instrução
prevalece. As listas de ilustrações, quadros e tabelas permanecem separadas. A
classe LaTeX local continua sendo uma adaptação; esta comparação não certifica
conformidade institucional ou normativa integral.

A folha de aprovação deste PDF é um modelo sem assinaturas e não comprova a
aprovação do trabalho. Para o depósito final, ela deverá ser substituída ou
complementada conforme o procedimento vigente do IFC, incluindo as assinaturas
eletrônicas requeridas. O termo de autorização para publicação também não integra
esta versão de orientação. Os formulários finais, a ficha catalográfica quando
aplicável e eventuais particularidades do curso devem ser confirmados com a
Coordenação e a Biblioteca. A classe LaTeX local contém comentários relativos a
edições anteriores de normas; a inspeção do pacote tradicional de 2026 não valida
automaticamente todos os seus usos nem os requisitos do pacote de desenvolvimento
de software, que não foi inspecionado. As decisões de capa e folha de rosto
permanecem pendentes de confirmação institucional.

## Fontes públicas de conferência

- [Normalização do Sistema de Bibliotecas da UFES](https://sib.ufes.br/normalizacao)
- [ABNT NBR 14724:2024 — cópia institucional](https://www.ufpi.br/images/Picos/Biblioteca/Atualizao%20do%20site/NBR%2014724%20de%202024%20para%20Trabalhos%20Acadmicos.pdf)
- [ABNT NBR 6023:2025 — cópia pública](https://vigilanciasanitaria.prefeitura.rio/wp-content/uploads/sites/84/2025/10/ABNT-NBR-6023-2025-Normatizacao-de-referencias.pdf)
- [ABNT NBR 10520:2023 — cópia acadêmica](https://ppgletras.furg.br/images/ABNT/2023_abnt-10520-citacoes.pdf)
