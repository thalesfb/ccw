---
applyTo: '**/*.py,**/tests/**,**/*.md'
---
# Testes e Documentacao

## Estrategia de testes
- Piramide: 70% unitarios, 20% integracao, 10% ponta a ponta simplificado
- Cobertura minima global: 70% (verificada com `pytest --cov`)
- Executar `pytest` antes de abrir PR; priorizar testes em `research/tests`

## Padroes pytest
- Nome de arquivo: `test_<assunto>.py` ou `<assunto>_test.py`
- Nome de funcao: `test_<condicao>_<resultado>()`
- Usar fixtures em `conftest.py` (criar se necessario) para setup de banco e arquivos temporarios
- Marcar cenarios pesados com `@pytest.mark.slow` e isolar em `tests/slow/`

## Boas praticas
- AAA: Arrange, Act, Assert claramente separados por comentarios
- Evitar acesso a rede real; mockar com `requests-mock` ou `pytest monkeypatch`
- Usar `tmp_path` para arquivos temporarios; limpar recursos ao final
- Garantir determinismo configurando seeds (`random.seed`, `numpy.random.seed`)

## Documentacao
- Atualizar `README.md` quando fluxo ou comandos mudarem
- Registrar decisoes tecnicas em `docs/` ou `research/docs/`
- Manter docstrings claras (resumo, parametros, retorno, excecoes)
- Utilizar exemplos executaveis nas docstrings quando possivel (`>>> exemplo()`)

## Comandos uteis
```
pytest --maxfail=1 --disable-warnings
pytest --cov=research --cov-report=term-missing
radon cc research/src --min B
```
