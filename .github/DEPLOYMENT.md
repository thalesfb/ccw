# 🚀 Guia de Deployment - GitHub Pages

Este guia descreve como configurar e publicar os relatórios da revisão sistemática no GitHub Pages.

## 📋 Pré-requisitos

- Repositório no GitHub (público ou privado com GitHub Pro/Team/Enterprise)
- Python 3.11+ instalado localmente
- Dependências instaladas (`pip install -r requirements.txt`)
- Banco de dados SQLite com dados (`research/systematic_review.db`)

## 🔧 Configuração Inicial

### 1. Habilitar GitHub Pages

1. Acesse seu repositório no GitHub
2. Vá em **Settings** → **Pages**
3. Em **Source**, selecione **GitHub Actions**
4. Salve as configurações

### 2. Configurar Permissões do Workflow

1. Vá em **Settings** → **Actions** → **General**
2. Em **Workflow permissions**, selecione:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
3. Clique em **Save**

### 3. Verificar o Workflow

O workflow já está configurado em `.github/workflows/publish-reports.yml`

Verifique se o arquivo existe e está correto:

```bash
cat .github/workflows/publish-reports.yml
```

## 🎯 Primeira Publicação

### Opção A: Commit e Push (Automático)

```bash
# Adicionar arquivos do workflow
git add .github/workflows/publish-reports.yml
git add .github/workflows/README.md
git add docs/README.md
git commit -m "🚀 ci: add GitHub Pages workflow for automated report publishing"

# Push para branch principal
git push origin develop
```

O workflow será executado automaticamente.

### Opção B: Execução Manual

1. Vá em **Actions** no GitHub
2. Selecione **Publish Reports to GitHub Pages**
3. Clique em **Run workflow**
4. Escolha a branch (main ou develop)
5. Clique em **Run workflow** (verde)

## 📊 Acompanhando a Publicação

### Monitorar o Workflow

1. Vá em **Actions** no GitHub
2. Clique no workflow em execução
3. Acompanhe os logs de cada step:
   - ✅ Checkout repository
   - ✅ Setup Python
   - ✅ Install dependencies
   - ✅ Generate reports
   - ✅ Prepare Pages content
   - ✅ Deploy to GitHub Pages

### Verificar Publicação

Após 2-3 minutos, acesse:

```
https://thalesfb.github.io/ccw/
```

Ou verifique a URL em **Settings** → **Pages**

## 🔄 Atualizações Automáticas

O workflow é executado automaticamente quando:

1. **Push para main ou develop**
   ```bash
   git push origin develop
   ```

2. **Merge de Pull Request**
   - Após merge para main/develop

3. **Execução manual**
   - Via Actions UI no GitHub

## 📁 Estrutura Publicada

```
https://thalesfb.github.io/ccw/
├── index.html                    # Sumário executivo
├── papers.html                   # Artigos incluídos
├── gap-analysis.html             # Análise de lacunas
└── visualizations/
    ├── prisma_flow.png          # Diagrama PRISMA
    ├── selection_funnel.png     # Funil de seleção
    ├── papers_by_year.png       # Distribuição temporal
    ├── techniques_distribution.png
    ├── database_coverage.png
    └── relevance_distribution.png
```

## 🎨 Customização

### Modificar Layout da Página Principal

Edite o template HTML em:

`.github/workflows/publish-reports.yml` (seção "Create navigation page")

Ou crie um arquivo `docs/index.html` personalizado que será preservado.

### Adicionar Arquivos Extras

No workflow, após "Prepare Pages content":

```yaml
- name: Add custom files
  run: |
    cp custom-page.html docs/
    cp -r assets/ docs/assets/
```

### Mudar Domínio Customizado

1. Em **Settings** → **Pages**
2. Em **Custom domain**, adicione seu domínio
3. Configure DNS CNAME apontando para `thalesfb.github.io`

## 🐛 Troubleshooting

### Erro: "Permission denied to deploy"

**Solução:**
```bash
# 1. Verifique permissões em Settings → Actions → General
# 2. Marque "Read and write permissions"
# 3. Re-execute o workflow
```

### Erro: "Database not found"

**Solução:**
```bash
# Opção 1: Commitar o banco
git add research/systematic_review.db
git commit -m "chore: add database for reports"
git push

# Opção 2: O workflow criará página básica sem relatórios
```

### Páginas não atualizam

**Soluções:**
```bash
# 1. Limpar cache do navegador (Ctrl+Shift+R)
# 2. Aguardar 5-10 minutos para propagação
# 3. Verificar logs do workflow
# 4. Tentar em modo anônimo
```

### Workflow falha em "Install dependencies"

**Solução:**
```bash
# Testar localmente primeiro
pip install -r requirements.txt

# Se falhar, verificar requirements.txt
# Considerar usar constraints ou pip-tools
```

### Deploy não acontece

**Verificações:**
```bash
# 1. Checar se o ambiente "github-pages" existe
# 2. Verificar se há permissão id-token: write
# 3. Confirmar que Pages está habilitado em Settings
# 4. Revisar logs completos do workflow
```

## 📈 Monitoramento e Analytics

### Adicionar Google Analytics

Edite o template HTML e adicione:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### GitHub Insights

Vá em **Insights** → **Traffic** para ver:
- Visualizações de página
- Visitantes únicos
- Fontes de tráfego
- Conteúdo popular

## 🔐 Segurança

### Dados Sensíveis

⚠️ **Atenção:** GitHub Pages é público por padrão.

**Não publique:**
- Credenciais ou tokens
- Dados pessoais não anonimizados
- Informações confidenciais de pesquisa

**Para tornar privado:**
- Requer GitHub Enterprise Cloud
- Configure em Settings → Pages → Visibility

### Review antes de Publicar

```bash
# Gerar localmente primeiro
python -m research.src.cli export

# Revisar arquivos
ls -la research/exports/reports/
ls -la research/exports/visualizations/

# Verificar conteúdo sensível
grep -r "senha\|token\|secret" research/exports/
```

## 📝 Checklist de Deployment

- [ ] GitHub Pages habilitado em Settings
- [ ] Workflow permissions configuradas (read + write)
- [ ] Workflow file commitado (`.github/workflows/publish-reports.yml`)
- [ ] Banco de dados populado (`research/systematic_review.db`)
- [ ] Primeiro push feito para main/develop
- [ ] Workflow executado com sucesso (Actions)
- [ ] URL acessível (https://thalesfb.github.io/ccw/)
- [ ] Relatórios visíveis e corretos
- [ ] Imagens carregando corretamente
- [ ] Links de navegação funcionando
- [ ] Testado em diferentes navegadores
- [ ] Analytics configurado (opcional)
- [ ] Custom domain configurado (opcional)

## 🎓 Recursos Adicionais

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jekyll Themes](https://pages.github.com/themes/) (se quiser usar)
- [Custom Domain Setup](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## 💡 Dicas Avançadas

### Cache de Dependências

O workflow já usa cache do pip. Para melhorar:

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### Notificações

Adicione ao workflow para receber notificações:

```yaml
- name: Notify on success
  if: success()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Versionamento de Relatórios

Preserve versões históricas:

```yaml
- name: Archive reports
  run: |
    VERSION=$(date +%Y%m%d-%H%M%S)
    mkdir -p docs/archive/$VERSION
    cp -r docs/*.html docs/archive/$VERSION/
```

## 🆘 Suporte

Problemas? Abra uma issue no repositório ou consulte:

- GitHub Community: https://github.community/
- Stack Overflow: tag `github-pages`
- Documentação oficial do projeto
