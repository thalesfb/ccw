# Otimização de Planos de Ensino de Matemática

**Trabalho de Conclusão de Curso - Ciência da Computação - IFC Videira**

## Sobre o Projeto

Este repositório contém o desenvolvimento de uma ferramenta tecnológica para auxiliar professores de matemática na otimização de seus planos de ensino, através da identificação automatizada das competências individuais dos alunos.

### Tema

"Apoio à Otimização dos Planos de Ensino de Matemática por meio da identificação automatizada das competências individuais dos alunos usando técnicas computacionais."

## Orientação

- **Orientador:** Prof. Me. Rafael Zanin (IFC)
- **Coorientador:** Prof. Dr. Manassés Ribeiro (IFC)

## Objetivos

### Objetivo Geral

Desenvolver uma ferramenta tecnológica que permita ao professor diagnosticar competências individuais dos alunos e sugerindo planos de ensino adaptativos.

### Objetivos Específicos

1. Realizar revisão sistemática da literatura sobre tecnologias computacionais aplicadas à educação (learning analytics, personalização do ensino, sistemas tutores inteligentes).
2. Explorar técnicas de machine learning e análise preditiva para avaliação de desempenho em matemática.
3. Projetar e implementar um protótipo de software capaz de analisar dados de avaliação e gerar recomendações pedagógicas.
4. Validar o protótipo em ambiente experimental usando dados reais de turmas de matemática.

## Estrutura do Repositório

``` bash
├── .gitignore              # Arquivos a serem ignorados pelo Git
├── .env.sample             # Exemplo de configuração de variáveis de ambiente
├── docs/                   # Documentos como proposta e fundamentação teórica
├── research/               # 📚 Módulo de Revisão Sistemática Automatizada
│   ├── __init__.py         # Inicialização do módulo
│   ├── config.py           # Configurações e constantes
│   ├── models.py           # Modelos de dados (Paper)
│   ├── improved_pipeline.py # Pipeline principal
│   ├── cli.py              # Interface de linha de comando
│   ├── database.py         # Gerenciador SQLite
│   ├── deduplication.py    # Lógica de deduplicação
│   ├── exports.py          # Gerenciamento de exports
│   ├── api_clients/        # Clientes de APIs acadêmicas
│   │   ├── semantic_scholar.py
│   │   ├── openalex.py
│   │   ├── crossref.py
│   │   └── core.py
│   ├── utils/              # Funções utilitárias
│   ├── tests/              # Suite de testes
│   │   ├── quick/          # Testes rápidos unitários
│   │   ├── full/           # Testes de integração
│   │   └── benchmark/      # Testes de desempenho
│   ├── cache/              # Cache de respostas das APIs (gitignored)
│   ├── exports/            # Planilhas e relatórios gerados (gitignored)
│   ├── logs/               # Logs de auditoria (gitignored)
│   ├── systematic_review.db # Banco de dados SQLite (gitignored)
│   ├── systematic_review.ipynb # Notebook original (referência)
│   └── refactoring_plan.md # Plano de refatoração do módulo
├── results/                # Relatórios de validação
├── src/                    # Scripts de análise e notebooks
├── LICENSE                 # Licença do projeto
├── README.md               # Documentação do projeto
└── requirements.txt        # Dependências do projeto
```

## Módulo de Revisão Sistemática

O módulo `research/` implementa um pipeline automatizado para condução de revisões sistemáticas da literatura, conforme diretrizes PRISMA.

### Características

- **Busca automatizada** em múltiplas bases acadêmicas (Semantic Scholar, OpenAlex, Crossref, CORE)
- **Deduplicação inteligente** usando TF-IDF e fuzzy matching
- **Cache de respostas** para reduzir chamadas às APIs
- **Banco de dados SQLite** para armazenamento persistente
- **Exports em múltiplos formatos** (Excel, CSV, relatórios texto)
- **Interface CLI** para execução e gerenciamento
- **Logging completo** para auditoria e reprodutibilidade
- **Testes automatizados** para garantir qualidade

### Uso Rápido

```bash
# Configurar variáveis de ambiente
cp .env.sample .env
# Editar .env com suas credenciais de API

# Executar pipeline completo
python research/improved_pipeline.py

# Ou via CLI com opções
python research/cli.py run --max-results 10 --year-min 2015

# Ver estatísticas
python research/cli.py stats

# Exportar dados
python research/cli.py export --format excel

# Ver informações de configuração
python research/cli.py info
```

### Comandos CLI Disponíveis

- `run`: Executa o pipeline completo de busca e processamento
- `export`: Exporta papers do banco de dados
- `stats`: Mostra estatísticas dos papers armazenados
- `clear`: Limpa o banco de dados
- `info`: Exibe informações de configuração

### APIs Integradas

1. **Semantic Scholar** - Busca em texto completo com filtros de campo
2. **OpenAlex** - Metadados de acesso aberto com reconstrução de abstracts
3. **Crossref** - Dados bibliográficos com resolução de DOIs
4. **CORE** - Artigos de acesso aberto com texto completo

### Documentação Completa

Para detalhes sobre arquitetura, design patterns aplicados (SOLID/DRY/KISS/YAGNI), e planos futuros, consulte [refactoring_plan.md](research/refactoring_plan.md).

### Testes

```bash
# Testes rápidos (unitários)
pytest research/tests/quick/

# Todos os testes
pytest research/tests/

# Com cobertura
pytest --cov=research research/tests/
```

## Status do Projeto

🚧 Em desenvolvimento 🚧

## Próximos Passos

- [x] Completar protocolo de revisão sistemática
- [x] Definir bases de dados, termos de busca e critérios de inclusão/exclusão
- [x] Realizar busca nas bases de dados
- [x] Analisar e categorizar os artigos encontrados
- [ ] Investigar ferramentas semelhantes (ex: Edmodo, Google Classroom, Moodle, Khan Academy, etc.)
- [ ] Desenvolver cronograma detalhado do projeto
- [ ] Modelo de projeto em LaTeX


## Autor

Thales Ferreira - Graduando em Ciência da Computação - IFC Videira
