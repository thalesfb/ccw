# Trabalho de Conclusão de Curso

[`main.tex`](main.tex) inclui os capítulos, os elementos pré e pós-textuais e
a bibliografia do TCC. O PDF compilado é [`main.pdf`](main.pdf). O relato
científico é a referência para os resumos do site, da apresentação e da
documentação; o modelo institucional serve à formatação, não define o escopo
da pesquisa. A versão desta entrega é documental, sem treinamento com dados
reais ou validação educacional própria.

## Objetivos do manuscrito

<!-- ccw-sync:start goals -->
### Objetivo geral

Propor uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática, fundamentada no mapeamento e na análise da literatura científica.

### Objetivos específicos

**OE1:** categorizar as abordagens e técnicas computacionais e as finalidades pedagógicas descritas na literatura mapeada.

**OE2:** identificar limitações e lacunas técnicas, pedagógicas, metodológicas e éticas no material examinado.

**OE3:** formular a especificação técnica e pedagógica do protótipo, incluindo requisitos, critérios para seleção de fontes de dados e modelos e uma arquitetura de referência.

**OE4:** propor um protocolo para avaliar a viabilidade e a coerência da especificação conceitual, considerando sua fundamentação, a consistência dos requisitos e as condições técnicas e pedagógicas de uma eventual execução.
<!-- ccw-sync:end goals -->

As contagens e os limites estão na [nota de estado](../../docs/tcc/ESTADO-ATUAL-TCC.md).
Ao alterar o texto, siga o [contrato de sincronização](../../docs/tcc/DOCUMENTATION_SYNC.md)
e confira também os resumos manuais e as imagens. Elementos opcionais do modelo
continuam disponíveis; não devem ser removidos para atualizar a documentação.

## Elementos opcionais editáveis

Os arquivos `pretextuais/dedicatoria.tex`, `pretextuais/agradecimentos.tex`,
`pretextuais/epigrafe.tex` e `pretextuais/folhadeautorizacao.tex` permanecem
disponíveis para preenchimento pelo autor. O formulário de autorização conserva
a estrutura e o texto histórico do modelo, com os campos pessoais em branco;
não foi substituído por um título vazio. Os exemplos dos outros elementos estão
preservados como comentários editáveis, não como declarações pessoais prontas.
Suas linhas `\include` continuam comentadas em `main.tex`, como já ocorria com
a autorização no modelo anterior, portanto não geram páginas no PDF padrão.

Para utilizar um elemento, preencha seu arquivo e remova o `%` da respectiva
linha `\include` em `main.tex`. Recompile e confira o resultado. Não ative
elementos ainda vazios nem utilize citações sem conferir autoria e fonte.

### Autorização de publicação e proteção dos dados

O autor autoriza a publicação acadêmica deste TCC. Essa manifestação não substitui
o preenchimento e a assinatura do formulário institucional que o IFC exigir para
o depósito. Ela também não representa aceite de cláusulas adicionais do modelo
histórico, como uso de imagem, nem concede permissão para redistribuir textos
integrais de artigos de terceiros.

A folha editável foi mantida para essa formalização futura. Seu texto, sua
exigência e sua posição devem ser confirmados com o IFC antes da inclusão.
A data antiga de 2016 foi substituída por campos em branco. CPF, matrícula e
assinatura devem ser preenchidos somente na cópia privada destinada à instituição,
nunca no repositório público. Não se deve anexar uma digitalização preenchida ou
assinada ao Git; a versão pública deve continuar sem esses identificadores.

Contribuindo com a iniciativa de Lucas Barbosa (https://github.com/lvbarbosa)

Arquivos adaptados por Eliton Tiago (https://github.com/ElitonTiago)

Toda ajuda é bem vinda :D
