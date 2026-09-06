# GitHub Actions: publicação e validação

## Publicação em GitHub Pages

O workflow [publish-reports.yml](publish-reports.yml), denominado **Deploy
Reports to GitHub Pages**, executa após push na `main` ou por acionamento manual.
Ele publica relatórios previamente gerados e versionados. Não consulta o
SQLite nem executa uma nova coleta.

O job de preparação:

1. verifica os diretórios de relatórios e visualizações e os três relatórios
   HTML obrigatórios;
2. valida as seis imagens canônicas, suas cópias no TCC e na apresentação e o
   manifesto de entradas versionadas;
3. instala as dependências com `npm ci`, valida o conteúdo e compila o Slidev;
4. monta `_site/` com as páginas, exports e resultados versionados;
5. envia o artefato para o job de implantação em GitHub Pages.

```text
_site/
├── index.html
├── research/
│   ├── index.html
│   └── exports/
├── results/
│   ├── ptc/
│   └── tcc/
└── presentation/
```

Os PDFs e o PPTX presentes em `results/` são copiados do repositório. A compilação
LaTeX e a validação do PowerPoint pertencem ao workflow de qualidade; o deploy
compila a apresentação Slidev.

## Preparação dos artefatos

Para conferir a população publicada e as imagens sem distribuir o banco:

```bash
python -m research.src.validation.versioned_snapshot
python -m research.src.processing.adjudicated_snapshot --check
python -m research.src.validation.derived_assets --check
```

Quando necessário, regenere os relatórios a partir do snapshot adjudicado:

```bash
python -m research.src.processing.adjudicated_snapshot
```

Revise e versione os artefatos produzidos em um PR. O SQLite permanece local;
não deve ser comitado para viabilizar a publicação. Uma exportação de execução
local precisa incorporar as decisões científicas aplicáveis antes de substituir
o snapshot publicado.

O comando `python -m research.src.validation.derived_assets --sync` copia as
imagens canônicas para os consumidores e atualiza o manifesto. Ele não gera os
gráficos: use-o após a regeneração e confira o resultado. O check de sincronização
verifica hashes e entradas, mas não constitui validação científica do conteúdo
das figuras.

## Qualidade do TCC

O workflow [tcc-quality.yml](tcc-quality.yml) executa em PRs, push na `main` e
acionamento manual. Ele verifica fontes Python, snapshot, adjudicação,
bibliografia, tabelas MMAT, testes de pesquisa e protótipo, apresentação Slidev,
PPTX e compilação LaTeX. Em PRs do próprio repositório, a etapa
`canonical-pdf-sync` pode atualizar o PDF compilado na branch e solicitar nova
validação.

Checks aprovados demonstram as propriedades verificadas pelo código. A leitura
das fontes primárias, o julgamento metodológico e a revisão do texto continuam
necessários para aprovação acadêmica.

## Configuração e diagnóstico

Em **Settings → Pages**, selecione **GitHub Actions** como fonte de publicação.
O workflow declara `contents: read`, `pages: write` e `id-token: write`. Para
acionamento manual, abra **Actions → Deploy Reports to GitHub Pages → Run
workflow** e selecione a referência desejada.

- **Export ausente:** regenere, revise e versione o artefato exigido; o workflow
  interrompe a publicação quando um relatório obrigatório falta.
- **Imagem ou manifesto divergente:** regenere os gráficos a partir das entradas
  corretas, sincronize as cópias e examine o diff antes de abrir o PR.
- **Falha no Slidev:** reproduza `npm ci`, `npm run validate` e
  `npm run build -- --base /ccw/presentation/` no diretório `presentation/`.
- **Página desatualizada:** confira o commit e os logs do último deploy; a
  aprovação do PR, isoladamente, não demonstra publicação bem-sucedida.
