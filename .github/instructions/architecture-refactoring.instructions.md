---
applyTo: '**/*.py'
---
# Arquitetura e Refatoracao - Python

## Metricas alvo
- Arquivo ate 350 linhas; dividir scripts longos em modulos `research/src`
- Funcao ate 50 linhas e 5 parametros
- Complexidade ciclomatica maxima 10 (`radon cc`)
- Evitar aninhamento maior que 4 niveis; preferir retornos antecipados

## Padrao de organizacao
```
ccw/
  research/
    src/
      adapters/        # acessos externos (APIs, file IO)
      core/            # regras de negocio da revisao sistematica
      pipelines/       # comandos de alto nivel
      utils/           # funcoes auxiliares sem efeito colateral
  scripts/
    migrate_cache.py
    run_full_collection.py
```

## Diretrizes de codigo
- Transformar blocos procedurais em funcoes puras reaproveitaveis
- Centralizar configuracoes em objetos/dataclasses carregados de `.env`
- Preparar funcoes de banco usando contexto `with sqlite3.connect` e commits explicitos
- Injetar dependencias (clients HTTP, conectores) via parametros opcionais para facilitar testes
- Usar `Path` do `pathlib` ao lidar com caminhos em vez de strings cruas

## Refatoracao incremental
1. Identificar trecho com alta complexidade (`radon cc -n B caminho.py`)
2. Extrair funcoes ou classes com responsabilidade unica
3. Criar validacoes de entrada explicitas (ValueError, dataclasses)
4. Adicionar testes antes de mover arquivos entre pacotes

## Logs e erros
- Padrao de logger: `logger = logging.getLogger(__name__)`
- Logs informativos para passos principais e de debug controlados por flag
- Nao capturar excecoes largamente; propagar com contexto ou reerguer com mensagem clara

## Revisao automatica sugerida
- `radon cc --min B research/src`
- `radon mi --min B research/src`
- `ruff check` ou `flake8` para estilo basico
