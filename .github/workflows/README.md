# GitHub Actions Workflows

## 📄 `publish-reports.yml`

Workflow para publicação automática dos relatórios da revisão sistemática no GitHub Pages.

### Quando é executado

- **Push** para branches `main` ou `develop`
- **Manualmente** via GitHub Actions UI (workflow_dispatch)

### O que faz

1. **Checkout** do código
2. **Setup Python 3.11** com cache de dependências
3. **Instala** requirements.txt
4. **Verifica** se existe banco de dados SQLite
5. **Gera relatórios** executando `python -m research.src.cli export`
6. **Prepara conteúdo** para GitHub Pages:
   - Copia relatórios HTML mais recentes
   - Copia visualizações PNG
   - Cria página de navegação se necessário
7. **Publica** no GitHub Pages

### Arquivos publicados

```
docs/
├── index.html              # Sumário executivo (ou página de navegação)
├── papers.html             # Lista de artigos incluídos
├── gap-analysis.html       # Análise de lacunas
└── visualizations/
    ├── prisma_flow.png
    ├── selection_funnel.png
    ├── papers_by_year.png
    ├── techniques_distribution.png
    ├── database_coverage.png
    └── relevance_distribution.png
```

### Permissões necessárias

O workflow requer permissões especiais configuradas no repositório:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

### Como habilitar GitHub Pages

1. Vá em **Settings** → **Pages** no repositório
2. Em **Source**, selecione **GitHub Actions**
3. O workflow publicará automaticamente após o próximo push

### Execução manual

Você pode executar o workflow manualmente:

1. Vá em **Actions** no GitHub
2. Selecione **Publish Reports to GitHub Pages**
3. Clique em **Run workflow**
4. Escolha a branch e confirme

### Observações

- O workflow verifica se `research/systematic_review.db` existe antes de gerar relatórios
- Se o banco não existir, apenas cria uma página de navegação básica
- Usa cache do pip para acelerar instalação de dependências
- Previne execuções concorrentes do workflow
- Funciona em Ubuntu latest (runner do GitHub)

### Troubleshooting

**Erro: "Permission denied"**
- Verifique se as permissões do workflow estão corretas no repositório
- Vá em Settings → Actions → General → Workflow permissions
- Marque "Read and write permissions"

**Erro: "Database not found"**
- Certifique-se de que `research/systematic_review.db` está commitado
- Ou execute o pipeline antes: `python -m research.src.cli run-pipeline`
- Ou faça commit do banco gerado localmente

**Páginas não atualizam**
- GitHub Pages pode levar alguns minutos para atualizar
- Limpe o cache do navegador (Ctrl+Shift+R)
- Verifique logs do workflow em Actions

### Melhorias futuras

- [ ] Adicionar geração de PDF dos relatórios
- [ ] Criar arquivo sitemap.xml
- [ ] Adicionar versionamento dos relatórios
- [ ] Implementar comparação entre versões
- [ ] Adicionar analytics (Google Analytics ou similar)
- [ ] Criar RSS feed das atualizações
