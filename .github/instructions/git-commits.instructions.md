---
applyTo: '**'
---
# 📝 Git & Commits - Conventional Commits com Emojis

## 1. Estrutura da Mensagem de Commit

### 1.1 Formato Padrão
```
<emoji> <tipo>[escopo opcional]: <descrição resumida em imperativo>

[corpo opcional — detalhes, impactos, instruções]

[rodapé opcional — Refs #TICKET, Reviewed-by:]
```

### 1.2 Regras de Formatação
- **Primeira linha** ≤ 72 caracteres
- **Imperativo** na descrição (ex.: "adicionar", "corrigir", "remover")
- **Escopo** opcional entre parênteses (ex.: `feat(api):`, `fix(auth):`)
- **Linha em branco** separando título do corpo
- **Corpo** explicativo quando necessário (máximo 100 caracteres por linha)

## 2. Tipos de Commit e Emojis

### 2.1 Tipos Principais (Semantic Versioning)
| Tipo | Emoji | Descrição | Impacto Versão |
|------|-------|-----------|----------------|
| `feat` | ✨ `:sparkles:` | Nova funcionalidade | MINOR |
| `fix` | 🐛 `:bug:` | Correção de bug | PATCH |
| `BREAKING CHANGE` | 💥 `:boom:` | Mudança incompatível | MAJOR |

### 2.2 Tipos de Manutenção
| Tipo | Emoji | Descrição | Impacto |
|------|-------|-----------|---------|
| `docs` | 📚 `:books:` | Apenas documentação | Nenhum |
| `style` | 💄 `:lipstick:` | Formatação, lint (sem lógica) | Nenhum |
| `refactor` | ♻️ `:recycle:` | Refatoração sem mudança externa | Nenhum |
| `perf` | ⚡ `:zap:` | Melhoria de performance | PATCH |
| `test` | 🧪 `:test_tube:` | Testes adicionados/corrigidos | Nenhum |

### 2.3 Tipos de Infraestrutura
| Tipo | Emoji | Descrição | Impacto |
|------|-------|-----------|---------|
| `build` | 📦 `:package:` | Sistema de build, dependências | Nenhum |
| `ci` | 🧱 `:bricks:` | Integração contínua | Nenhum |
| `chore` | 🔧 `:wrench:` | Manutenção geral | Nenhum |

### 2.4 Tipos Específicos do Projeto
| Tipo | Emoji | Descrição | Uso |
|------|-------|-----------|-----|
| `raw` | 🗃️ `:card_file_box:` | Dados, fixtures, configurações | Arquivos de dados |
| `cleanup` | 🧹 `:broom:` | Limpeza de código morto | Remoção de código |
| `remove` | 🗑️ `:wastebasket:` | Exclusão de funcionalidades | Depreciação |
| `security` | 🔒 `:lock:` | Correções de segurança | Vulnerabilidades |
| `upgrade` | ⬆️ `:arrow_up:` | Upgrade de dependências | Atualizações |
| `downgrade` | ⬇️ `:arrow_down:` | Downgrade de dependências | Rollback |

## 3. Exemplos Práticos

### 3.1 Commits Simples
```bash
# Feature nova
✨ feat(api): adicionar endpoint de criação de usuários

# Bug fix
🐛 fix(auth): corrigir validação de token expirado

# Documentação
📚 docs: atualizar README com instruções de instalação

# Refatoração
♻️ refactor(user): extrair validação em classe separada

# Performance
⚡ perf(database): otimizar consulta de usuários ativos

# Teste
🧪 test(user): adicionar testes unitários para UserService
```

### 3.2 Commits com Corpo
```bash
✨ feat(payment): implementar processamento de pagamentos PIX

- Adicionar integração com API do Banco Central
- Implementar validação de chave PIX
- Criar modelos para transações PIX
- Adicionar testes de integração

Refs #123
```

```bash
🐛 fix(auth): corrigir vazamento de memória em sessões

O middleware de autenticação não estava limpando adequadamente
as sessões expiradas, causando acúmulo de memória em produção.

- Implementar limpeza automática de sessões
- Adicionar job cron para limpeza periódica
- Melhorar logs de debug para monitoramento

Fixes #456
Reviewed-by: @tech-lead
```

### 3.3 Breaking Changes
```bash
💥 feat(api)!: refatorar estrutura de resposta da API

BREAKING CHANGE: A estrutura de resposta da API foi alterada
para incluir metadados de paginação em um envelope.

Antes:
```json
[{id: 1, name: "User"}]
```

Depois:
```json
{
  "data": [{id: 1, name: "User"}],
  "meta": {"page": 1, "total": 50}
}
```

Migração necessária nos clientes da API.

Refs #789
```

## 4. Escopos Recomendados

### 4.1 Por Módulo/Camada
```bash
# Backend
feat(api): ...          # Endpoints REST
feat(auth): ...         # Autenticação/autorização
feat(database): ...     # Modelos e migrações
feat(services): ...     # Lógica de negócio
feat(utils): ...        # Utilitários

# Frontend
feat(ui): ...           # Componentes de interface
feat(pages): ...        # Páginas/rotas
feat(hooks): ...        # React hooks
feat(state): ...        # Gerenciamento de estado
feat(api): ...          # Cliente API/HTTP

# DevOps/Infra
feat(docker): ...       # Containers
feat(deploy): ...       # Scripts de deploy
feat(monitoring): ...   # Logs/métricas
```

### 4.2 Por Funcionalidade
```bash
feat(users): ...        # Gestão de usuários
feat(orders): ...       # Gestão de pedidos
feat(payments): ...     # Sistema de pagamentos
feat(reports): ...      # Relatórios
feat(notifications): ... # Sistema de notificações
```

## 5. Hooks e Validação

### 5.1 Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/commit-msg

commit_regex='^(✨|🐛|📚|💄|♻️|⚡|🧪|📦|🧱|🔧|🗃️|🧹|🗑️|🔒|⬆️|⬇️|💥)\s(feat|fix|docs|style|refactor|perf|test|build|ci|chore|raw|cleanup|remove|security|upgrade|downgrade)(\(.+\))?\!?:\s.{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Commit message format invalid!"
    echo ""
    echo "Expected format:"
    echo "<emoji> <type>[scope]: <description>"
    echo ""
    echo "Examples:"
    echo "✨ feat(api): add user creation endpoint"
    echo "🐛 fix(auth): correct token validation"
    echo "📚 docs: update API documentation"
    exit 1
fi
```

### 5.2 Commitlint Configuration
```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test',
        'build', 'ci', 'chore', 'raw', 'cleanup', 'remove', 'security',
        'upgrade', 'downgrade'
      ]
    ],
    'subject-max-length': [2, 'always', 50],
    'header-max-length': [2, 'always', 72],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-empty': [2, 'never'],
    'type-empty': [2, 'never'],
  },
  parserPreset: {
    parserOpts: {
      headerPattern: /^(.*?)\s+(feat|fix|docs|style|refactor|perf|test|build|ci|chore|raw|cleanup|remove|security|upgrade|downgrade)(\(.+\))?\!?:\s(.+)$/,
      headerCorrespondence: ['emoji', 'type', 'scope', 'subject']
    }
  }
};
```

## 6. Workflow Git Recomendado

### 6.1 Feature Branch Flow
```bash
# 1. Criar branch para feature
git checkout -b feat/user-registration

# 2. Commits incrementais
git add .
git commit -m "✨ feat(auth): adicionar modelo de usuário"

git add .
git commit -m "✨ feat(auth): implementar validação de email"

git add .
git commit -m "🧪 test(auth): adicionar testes para registro de usuário"

# 3. Rebase interativo para limpar histórico (opcional)
git rebase -i main

# 4. Push da branch
git push origin feat/user-registration

# 5. Criar Pull Request
```

### 6.2 Hotfix Flow
```bash
# 1. Criar branch de hotfix
git checkout -b fix/critical-security-issue

# 2. Commit da correção
git commit -m "🔒 fix(auth): corrigir vulnerabilidade de injeção SQL

Corrige vulnerabilidade crítica que permitia injeção SQL
através do parâmetro de busca na API de usuários.

CVE-2024-XXXX
Refs #urgent-123"

# 3. Deploy direto para produção
git checkout main
git merge fix/critical-security-issue
git tag v1.2.1
```

## 7. Configuração do VS Code

### 7.1 Settings.json
```json
{
  "git.inputValidation": "always",
  "git.inputValidationLength": 72,
  "git.inputValidationSubjectLength": 50,
  "gitlens.advanced.messages": {
    "suppressCommitHasNoPreviousCommitWarning": false
  },
  "conventionalCommits.scopes": [
    "api", "auth", "database", "ui", "pages", 
    "hooks", "utils", "docker", "ci", "docs"
  ]
}
```

### 7.2 Extensões Recomendadas
```json
{
  "recommendations": [
    "vivaxy.vscode-conventional-commits",
    "eamodio.gitlens",
    "mhutchie.git-graph",
    "waderyan.gitblame"
  ]
}
```

## 8. Boas Práticas

### 8.1 Do's ✅
- Use **um emoji por commit** (o mais representativo)
- Seja **específico** na descrição
- **Explique o porquê** no corpo quando necessário
- **Vincule issues** com `Refs #123`
- **Marque revisores** com `Reviewed-by:`
- **Agrupe mudanças** relacionadas em um commit
- **Teste antes** de fazer commit

### 8.2 Don'ts ❌
- Evite descrições genéricas ("ajustes", "correções")
- Não use múltiplos emojis no mesmo commit
- Não misture tipos diferentes no mesmo commit
- Não faça commits gigantes (>50 arquivos alterados)
- Não commite código que quebra testes
- Não use gírias ou abreviações excessivas
- Não esqueça de revisar diff antes do commit

### 8.3 Checklist de Commit
```markdown
## ✅ Pre-commit Checklist

- [ ] Código testado localmente
- [ ] Testes passando
- [ ] Lint/formatação ok
- [ ] Documentação atualizada (se necessário)
- [ ] Mensagem segue padrão conventional
- [ ] Emoji apropriado selecionado
- [ ] Escopo correto definido
- [ ] Descrição clara e concisa
- [ ] Issue referenciada (se aplicável)
```
