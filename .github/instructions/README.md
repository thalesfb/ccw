---
applyTo: '**'
---
# Instrucoes CCW

Este indice coleta as diretrizes que orientam o trabalho com o repositorio `ccw`.

## Estrutura das instrucoes

- [copilot-core.instructions.md](./copilot-core.instructions.md)
  Diretrizes gerais para comportamento do assistente, fluxo de trabalho e ferramentas suportadas.
- [architecture-refactoring.instructions.md](./architecture-refactoring.instructions.md)
  Padroes de design e limites de complexidade para o codigo Python deste repositorio.
- [operation-modes.instructions.md](./operation-modes.instructions.md)
  Modos de operacao (planejamento, depuracao, analise de performance) usados pela equipe.
- [testing-documentation.instructions.md](./testing-documentation.instructions.md)
  Expectativas de testes automatizados, organizacao de fixtures e requisitos de documentacao tecnica.
- [git-commits.instructions.md](./git-commits.instructions.md)
  Convencao de commits baseada em Conventional Commits e emojis opcionais.

## Como aplicar

- Codigo Python (`*.py`, scripts CLI, pacotes em `research/src`)
  aplicar architecture-refactoring, testing-documentation e security quando relevante.
- Documentos Markdown (`*.md`)
  seguir estrutura deste indice e registrar decisoes tecnicas relevantes.
- Tarefas gerais
  seguir copilot-core, operation-modes e git-commits.

## Metas globais

- Cobertura de testes minima: 70% no pipeline critico (`research/tests`).
- Complexidade ciclomatica alvo: ate 10 por funcao (radon).
- Arquivos de script: preferir funcoes puras e logs padronizados.
- Commits pequenos com verificacao de testes antes de subir alteracoes.
