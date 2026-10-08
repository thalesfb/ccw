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
o antigo parágrafo metodológico foi retirado. A delimitação detalhada foi
deslocada para a metodologia, preservando na introdução somente uma remissão
ao escopo documental. A explicação sobre literatura cinzenta foi reduzida a
uma frase nos critérios, sem mudar os tipos documentais elegíveis. A imagem
do PRISMA é identificada como Figura na lista de ilustrações, e a cobertura
por fonte é apresentada em uma única pizza com quantidades e percentuais.
Essas mudanças de apresentação não alteram as decisões de seleção nem os
julgamentos MMAT.

A síntese empírica é um quadro em retrato, com continuação automática e fonte
de dez pontos. Tema e finalidade compartilham uma coluna, sem retirar as
informações anteriormente apresentadas. A identificação do estudo, a
abordagem, a avaliação e o resultado reportado permanecem explícitos. Essa
organização evita a quebra de página obrigatória causada pelo ambiente de
paisagem; a compilação ainda pode quebrar o quadro entre páginas quando o
espaço disponível se esgota.

A abertura do quadro MMAT reserva espaço para a identificação, o cabeçalho
e as primeiras linhas antes de criar seu destino no PDF. A reserva é
condicional: não impõe uma página nova quando há espaço suficiente. Isso
evita que o texto do quadro avance enquanto a âncora da lista permanece
na página anterior, divergência detectada pelo verificador no TeX Live.

Uma observação interrogativa exige uma resposta, não uma marcação automática
de conclusão. A devolutiva individual deve indicar o que mudou, onde a mudança
pode ser verificada e, quando houver adaptação, sua justificativa e o limite
da confirmação. Pergunta, objetivos e interpretações científicas não são
considerados aprovados somente porque o artefato compilou ou os testes
passaram. Comentários e respostas pessoais permanecem nos arquivos privados,
separados desta descrição pública do processo de revisão.

## Recuperação local de evidências científicas

O módulo `research.src.validation.evidence_retrieval` oferece recuperação lexical
por SQLite FTS5, reutilizando o extrator de páginas do projeto. Não chama modelos,
serviços de embeddings ou APIs. O índice operacional deve permanecer no cache
ignorado, separado do banco da coleta e das decisões versionadas do corpus.
Cada trecho conserva ID do estudo, papel documental, página física, posição no
texto e hashes do PDF, da página e do trecho. A indexação rejeita passagens que
não correspondam à página original; a consulta verifica alteração da fonte.

A lista permitida deve ser derivada do escopo canônico. Consultas empíricas
excluem protocolos contextuais por padrão. O ranqueamento BM25 indica relevância
lexical, não qualidade, validade ou suporte científico. Ausência de resultado
não demonstra ausência do conceito no documento, especialmente em PDFs sem
texto extraível ou em consultas cujos termos não coexistam no mesmo trecho.

No uso científico, os vínculos de referência e papel devem ser complementados
pelos hashes dos PDFs registrados no manifesto revisado. Assim, a substituição
da fonte seguida de nova extração também exige revisão do manifesto. O modo
genérico, sem esses vínculos, não confirma identidade documental. Os hashes
identificam bytes; não demonstram autoria, autenticidade editorial ou validade.

Os manifestos públicos registram somente procedência, localizadores e decisões
de revisão explicitamente delimitadas. Texto integral, banco SQLite e feedback
pessoal não são distribuídos. O estado `SUPPORTED` significa suporte documental
à afirmação atribuída sob os limites registrados, não validação do artigo,
avaliação independente humana ou conclusão do MMAT.

Após obter licitamente os PDFs correspondentes aos hashes do manifesto, o uso
local pode ser reproduzido a partir da raiz do repositório:

```python
import csv
import json
from pathlib import Path
from research.src.validation.evidence_retrieval import EvidenceIndex, extract_chunks

scope = list(csv.DictReader(Path("research/data/current_synthesis_scope.csv").open(encoding="utf-8")))
registry = {row["study_id"]: {"bib_key": row["study_key"],
            "synthesis_role": row["synthesis_role"]} for row in scope}
manifest = json.loads(Path("research/data/evidence_sources_current.json").read_text(encoding="utf-8"))
for record in manifest["sources"]:
    if record.get("sha256"):
        registry[record["study_id"]]["sha256"] = record["sha256"]
allowed_ids = set(registry)
source = {"study_id": "2", "bib_key": "Implementation2025_000",
          "synthesis_role": "empirical_evidence",
          "source_url": "https://www.ijiet.org/vol15/IJIET-V15N1-2228.pdf"}
with EvidenceIndex(Path("research/.cache/evidence/index.sqlite"), allowed_ids=allowed_ids,
                   source_registry=registry) as index:
    index.add(extract_chunks(Path("research/.cache/evidence/study-2.pdf"), source))
    passages = index.search("hybrid sampling", study_ids={"2"})
```

O relatório `research/exports/analysis/evidence_retrieval_evaluation.json`
contém nove casos fixos com fonte, páginas esperadas, resultados e hashes.
Essa avaliação limitada verifica localização e fronteiras de escopo; não mede
recall semântico do corpus nem substitui a leitura crítica. Os testes novos
executam sem rede e integram a validação de fontes do CI.
