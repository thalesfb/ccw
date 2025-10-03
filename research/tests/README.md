# Testes do Pipeline de Revisão Sistemática

Esta pasta contém todos os testes para validar o funcionamento do pipeline refatorado.

## 📁 Arquivos de Teste

### 🧪 Testes Básicos

- **`test_pipeline_simple.py`** - Teste básico dos componentes principais
- **`test_pipeline_complete.py`** - Teste completo dos componentes (sem APIs reais)

### 🚀 Testes de Pipeline

- **`test_minimal_pipeline.py`** - Teste mínimo com dados simulados
- **`test_improved_corrections.py`** - Teste das correções implementadas
- **`test_improved_pipeline.py`** - Teste do pipeline melhorado

### 📊 Testes de Auditoria

- **`test_audit_logging.py`** - Teste do sistema de logs de auditoria

## 🎯 Como Executar os Testes

### Teste Básico (Recomendado primeiro)

```bash
cd tests
python test_pipeline_simple.py
```

### Teste Mínimo do Pipeline

```bash
cd tests
python test_minimal_pipeline.py
```

### Teste do Sistema de Logs

```bash
cd tests
python test_audit_logging.py
```

### Teste Completo (sem APIs reais)

```bash
cd tests
python test_pipeline_complete.py
```

## 📊 Resultados Esperados

### ✅ Teste Básico

- Configuração carregada
- 132 queries geradas
- Logger de auditoria criado
- Funções de normalização e scoring funcionando

### ✅ Teste Mínimo

- Pipeline completo executado
- 5 artigos processados
- Dados salvos no banco SQLite
- CSV exportado com resultados

### ✅ Teste de Auditoria

- Logs estruturados gerados
- Relatórios JSON e Excel criados
- Gráficos de performance gerados

## 🔧 Configuração

Os testes usam a configuração padrão do projeto. Para testar com APIs reais, configure as variáveis de ambiente:

```bash
export SEMANTIC_SCHOLAR_API_KEY="your_key"
export USER_EMAIL="your_email"
export CORE_API_KEY="your_key"
```

## 📈 Logs de Teste

Os logs de teste são salvos em:

- `../logs/` - Logs de auditoria
- `../audit_charts/` - Gráficos de performance
- `../exports/` - Resultados exportados

## 🚨 Solução de Problemas

### Erro de Import

Se houver erro de import, verifique se está executando do diretório correto:

```bash
cd research/tests
python test_pipeline_simple.py
```

### Erro de Dependências

Instale as dependências necessárias:

```bash
pip install pandas numpy requests tqdm matplotlib seaborn
```

### Erro de Banco de Dados

O banco SQLite será criado automaticamente. Se houver problemas, verifique permissões de escrita no diretório.

## 📝 Notas

- Os testes usam dados simulados para evitar chamadas desnecessárias às APIs
- O sistema de logs é testado com dados reais de auditoria
- Todos os testes devem passar para validar o pipeline
- Os resultados são salvos para análise posterior
