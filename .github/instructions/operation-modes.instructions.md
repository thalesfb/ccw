---
applyTo: '**'
---
# Modos de Operacao Copilot

## Modo Planejador
Ative quando receber tarefas amplas ou multiplos arquivos.
1. Mapear objetivos, entradas e safras de dados (CSV, SQLite, APIs).
2. Levantar duvidas essenciais (prazo, ambiente, impacto em scripts existentes).
3. Montar plano em fases: analise, implementacao, testes, documentacao.
4. Executar uma fase por vez e revisar com solicitante antes de avancar.
5. Registrar progresso: feito, proximo passo, riscos e bloqueios.

## Modo Depurador
Use para bugs ou falhas de execucao.
1. Formular ate 5 hipoteses (dados ausentes, permissao, dependencia, IO, logica).
2. Instrumentar com logs temporarios padronizados `TEMP_DEBUG` e nivel DEBUG.
3. Reproduzir o problema em ambiente isolado (usar `python -m` quando possivel).
4. Validar solucao com teste direcionado ou script de exemplo.
5. Limpar logs temporarios e documentar causa raiz.

## Modo Analise de Performance
Acione quando houver lentidao em pipelines.
1. Medir baseline com `time`, `cProfile` ou logs de duracao.
2. Identificar gargalos (consultas SQLite, chamadas HTTP, loops custosos).
3. Aplicar otimizacao incremental (cache, batch, paralelismo seguro).
4. Comparar resultados com baseline e registrar ganho.
5. Propor monitoramento continuo (dashboards, alertas simples).
