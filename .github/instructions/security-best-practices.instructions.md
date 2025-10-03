---
applyTo: '**/*.py,**/*.env*,**/cache/**,**/logs/**'
---
# Segurança em Projetos Científicos

## Proteção de dados sensíveis
- **Nunca** versionar chaves de API em `.env` ou scripts
- Usar `.env.example` com valores placeholders para documentar variáveis esperadas
- Considerar dados pessoais em PDFs/artigos; anonimizar quando necessário
- Cache de APIs (`cache/`) pode conter dados proprietários; incluir em `.gitignore`

## Gestão de credenciais
- Armazenar chaves em `.env` na raiz do projeto
- Carregar com `python-dotenv` ou `os.environ.get()` com fallbacks seguros
- Para APIs públicas acadêmicas (Crossref, Semantic Scholar), usar rate limiting respeitoso
- Documentar requisitos de autenticação em `README.md`

## Validação de entrada
- Sanitizar parâmetros de busca antes de consultar APIs externas
- Validar schemas de resposta JSON com `jsonschema` se possível
- Limitar tamanho de downloads (PDFs, CSVs) para evitar DoS acidental
- Usar `pathlib.Path.resolve()` para evitar path traversal em operações de arquivo

## Logs seguros
- Não loggar tokens completos; usar truncamento (`token[:8]+"..."`)
- Separar logs de debug de produção; configurar níveis apropriados
- Rotacionar logs grandes automaticamente
- Revisar logs antes de compartilhar em issues/PRs

## Dependências
- Executar `safety check` periodicamente para vulnerabilidades conhecidas
- Manter `requirements.txt` atualizado com versões específicas
- Usar ambientes virtuais isolados por projeto
- Considerar `pip-audit` para análise adicional de segurança

## Backup e recuperação
- Fazer backup periódico de bancos SQLite importantes (`research/systematic_review.db`)
- Versionamento de schemas de banco com migrações incrementais
- Cache regenerável pode ser excluído; dados processados devem ter backup
- Documentar procedimentos de restauração em caso de corrupção

## Boas práticas específicas
- Rate limiting responsivo para APIs acadêmicas (ex: 1 req/segundo)
- Timeout adequado em requests HTTP (10-30 segundos)
- Validar integridade de downloads (checksums quando disponível)
- Monitorar espaço em disco para evitar falha por cache excessivo