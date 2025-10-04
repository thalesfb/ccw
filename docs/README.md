# Relatórios da Revisão Sistemática

Este diretório contém os relatórios publicados automaticamente via GitHub Actions.

## 📊 Conteúdo

Os seguintes arquivos são gerados e publicados:

- **`index.html`** - Sumário executivo da revisão sistemática
- **`papers.html`** - Lista detalhada dos artigos incluídos
- **`gap-analysis.html`** - Análise de lacunas e oportunidades
- **`visualizations/`** - Gráficos e diagramas

## 🔄 Atualização

Os relatórios são atualizados automaticamente quando:

- Há push para `main` ou `develop`
- O workflow é executado manualmente

## 🌐 Acesso Online

Após habilitar GitHub Pages, os relatórios estarão disponíveis em:

```
https://thalesfb.github.io/ccw/
```

## 📝 Geração Local

Para gerar os relatórios localmente:

```bash
# Executar pipeline completo
python -m research.src.cli run-pipeline

# Ou apenas exportar do banco existente
python -m research.src.cli export
```

Os arquivos serão salvos em `research/exports/`.

## 🛠️ Workflow

O processo de publicação é gerenciado pelo workflow:

`.github/workflows/publish-reports.yml`

Consulte o README do workflow para mais detalhes sobre configuração e troubleshooting.
