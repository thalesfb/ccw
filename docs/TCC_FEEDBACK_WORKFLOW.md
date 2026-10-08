# Incorporação rastreável de feedback ao manuscrito

A revisão distingue observações editoriais, correções factuais, sugestões de
reformulação e decisões metodológicas. Comentários recebidos não substituem
fontes científicas nem autorizam, por si só, mudar o corpus, os critérios de
seleção ou a força das conclusões.

## Ingestão local

O módulo `research.src.validation.pdf_feedback` utiliza a dependência `pypdf`
já prevista no projeto. Ele preserva páginas físicas, texto extraído, hashes,
conteúdo e coordenadas das anotações. Links e janelas auxiliares não são
contados como comentários. PDFs sem texto extraível são identificados; não
se presume que tenham sido submetidos a reconhecimento óptico de caracteres.

```powershell
python -m research.src.validation.pdf_feedback `
  --pdf "caminho/do/manuscrito-anotado.pdf" `
  --transcript "caminho/da/transcricao.txt"
```

O destino padrão é `feedback/private/`, excluído do versionamento. Os arquivos
contêm comentários pessoais e transcrição integral: não devem ser copiados
para issues, commits ou pull requests sem revisão e autorização de publicação.
O código e os testes usam apenas exemplos sintéticos.

Uma nota adesiva identifica uma posição, mas não delimita necessariamente
uma passagem. A extração deixa o trecho associado vazio em vez de inventar
uma citação. O vínculo com o manuscrito deve ser conferido posteriormente.
A transcrição preserva o conteúdo original e os intervalos de caracteres;
isso não equivale a verificar sua fidelidade contra a gravação.

## Verificação e limites

As correções editoriais preservam os critérios, as contagens e a distinção
entre retenção operacional e confirmação em texto completo. Alterações da
pergunta, dos objetivos ou do eixo teórico exigem avaliar os efeitos sobre
resultados, discussão, conclusão e apresentação antes de serem consolidadas.

A conferência de quadros exige examinar o PDF e as listas efetivamente
geradas, não somente os comandos presentes no fonte. O pacote `ltcaption`
fornece suporte a `LTcaptype` para versões antigas de `longtable`, preservando
os tipos já declarados no manuscrito. A [documentação do pacote](https://mirrors.ctan.org/macros/latex/contrib/caption/ltcaption.pdf)
descreve esse mecanismo e a integração com `memoir`.

Os testes de extração são executáveis sem rede:

```powershell
cd research
python -m unittest discover -s tests -p test_pdf_feedback.py
python -m unittest discover -s tests -p test_tcc_editorial_feedback.py
```

Esses testes verificam rastreabilidade e regressões específicas. Não
certificam completude científica, conformidade normativa integral ou
validação empírica do protótipo.

## Compilação e verificação do artefato

O comando abaixo compila em uma árvore temporária nova, incluindo as tabelas
geradas da revisão. Arquivos auxiliares antigos do checkout, inclusive os
de capítulos carregados com `include`, não entram nessa árvore. O diretório
legado `abnetx2` é a origem da cópia `abntex2`; uma cópia local antiga não é
usada como fonte. O PDF só substitui o destino após convergência dos auxiliares
e ausência de citações/referências indefinidas ou pedidos de recompilação.

```powershell
python scripts/compile_tcc.py --output results/tcc/main.pdf --diagnostics .tcc-build/aux
python scripts/validate_tcc_pdf.py --pdf results/tcc/main.pdf --aux .tcc-build/aux
```

A segunda verificação confere o sumário e as listas pelos destinos efetivos
do PDF e pelos números de página impressos. Exige os cinco quadros atuais:
camadas de busca, PICOS, síntese empírica, MMAT e checklist PRISMA. Também
rejeita entradas obsoletas detectadas na revisão editorial. Os auxiliares
devem pertencer à mesma compilação que produziu o PDF. A inspeção visual
continua necessária para legibilidade, quebras e espaçamento.

O estilo de citação legado preserva a definição de `bibcite` do `hyperref`.
Uma redefinição diferente daquela restaurada pelo Babel gerava comparações
incompatíveis e pedidos permanentes de recompilação. A correção preserva os
links das citações e a detecção de mudanças reais; não suprime os avisos.

## Comparação institucional delimitada

Foram consultados, em 7 de outubro de 2026, a [página de templates da biblioteca
do IFC](https://biblioteca.ifc.edu.br/tcc/) e o [template completo nela indicado](https://biblioteca.ifc.edu.br/wp-content/uploads/sites/53/2022/11/template-TC-2022-novembro-docx-.docx).
O estilo `Legenda` desse DOCX define alinhamento centralizado e aparece nos
exemplos de ilustrações. Essa é a base institucional da centralização aplicada;
não se atribui à ABNT uma obrigação universal de centralizar legendas.

A [página do curso em Videira](https://videira.ifc.edu.br/ciencia-da-computacao/defesas-de-tc/)
também disponibiliza um modelo TC tradicional identificado como 2026. Seu
`config_inicial.tex` conserva a configuração antiga `raggedright`. A diferença
foi tratada explicitamente, adotando para as legendas o template apresentado
pela biblioteca como obrigatório, sem trocar silenciosamente toda a classe
institucional. Essa comparação não certifica todos os elementos do template
nem dispensa a conferência das demais normas vigentes.

Na organização editorial, a justificativa concentra relevância e contribuição;
os procedimentos permanecem na metodologia. A delimitação permanece na
introdução para explicitar o escopo antes dos resultados, e a explicação sobre
literatura cinzenta foi integrada aos critérios. Essas escolhas preservam a
transparência metodológica e são submetidas à revisão acadêmica, sem pressupor
aprovação institucional ou do orientador.
