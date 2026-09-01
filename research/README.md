# Revisão Sistemática da Literatura — CCW Research

Este diretório contém o código e os artefatos versionados usados na revisão sistemática sobre técnicas computacionais aplicadas ao ensino de matemática.

## Evidência histórica preservada

A execução usada pelo TCC deve ser interpretada a partir de evidências versionadas, e não apenas da configuração atual do código.

As referências principais são:

1. `research/protocol_execution_2025.json` — manifesto reconstruído da execução de 2025, com evidências e limitações;
2. `research/exports/reports/summary.json` — export preservado com as contagens consolidadas do corpus;
3. `research/src/search_terms.py` — gerador canônico da estratégia de busca;
4. `research/data/mmat_assessments.csv` — fonte canônica das avaliações MMAT atuais.

O banco usado em tempo de execução tem caminho padrão `research/systematic_review.sqlite`, conforme `src/config.py`, mas **não é versionado** na branch atual. Por isso, uma terceira pessoa pode auditar os números fixos pelos exports preservados e pode reexecutar o código, mas não deve ser levada a acreditar que possui o banco histórico original ou que as APIs externas retornarão hoje exatamente as mesmas respostas de 2025.

## Protocolo reconstruído da execução de 2025

### Estratégia de busca

O gerador canônico versionado possui **72 consultas canônicas**:

- 48 em inglês: 2 termos matemáticos × 12 termos computacionais × 2 termos educacionais;
- 24 em português: 1 termo matemático × 12 termos computacionais × 2 termos educacionais.

Cada consulta segue a estrutura:

```text
termo matemático AND termo computacional AND termo educacional
```

Exemplos:

```text
mathematics AND machine learning AND education
math AND intelligent tutor AND learning
matemática AND aprendizado de máquina AND educacao
```

O histórico preservado comprova a estratégia versionada de 72 consultas antes dos relatórios finais de 2025. Não existe, contudo, um log completo por consulta que permita reconstruir retrospectivamente o número exato de requisições HTTP disparadas durante a coleta. Portanto, **72 é a contagem da estratégia canônica**, não uma alegação de auditoria de todas as chamadas de rede da execução histórica.

### Fontes

O relatório consolidado registra contribuições de quatro fontes:

| Fonte | Registros no export consolidado |
| --- | ---: |
| Crossref | 2.865 |
| OpenAlex | 1.817 |
| Semantic Scholar | 1.786 |
| CORE | 446 |

### Recorte temporal

O snapshot versionado do relatório gerado em 25/11/2025 registra explicitamente:

```text
year_range = 2015-2025
```

O export consolidado também registra 312 documentos de 2015 no conjunto reportado. Nenhum dos 17 estudos finais incluídos é de 2015, mas a presença desses registros confirma que o ano integrou a janela executada.

### Contagens usadas no TCC

| Etapa | Contagem |
| --- | ---: |
| Identificação | 9.431 |
| Duplicatas removidas | 2.517 |
| Registros únicos / triagem | 6.914 |
| Elegibilidade | 1.883 |
| Excluídos na elegibilidade | 1.866 |
| Incluídos | 17 |

Essas contagens são preservadas em `research/exports/reports/summary.json`.

## Configuração atual

`src/config.py` mantém como padrão:

- período: 2015–2025;
- idiomas: inglês e português;
- limiar de relevância temática: 4,0;
- banco de execução: `systematic_review.sqlite`.

A pontuação de relevância é uma heurística de aderência temática e **não** é usada como nota de qualidade metodológica. A apreciação metodológica dos estudos incluídos é realizada separadamente com o MMAT.

## Execução

Instale as dependências a partir da raiz do repositório:

```bash
python -m pip install -r research/requirements.txt
```

Com o ambiente configurado, os comandos principais são:

```bash
python -m research.src.cli run-pipeline --min-score 4.0
python -m research.src.cli stats
python -m research.src.cli export
```

Uma nova execução consulta serviços externos mutáveis. Seus resultados devem ser tratados como **nova execução**, com data, configuração e artefatos próprios, e não como reconstrução automática do corpus histórico.

## Estrutura relevante

```text
research/
├── protocol_execution_2025.json   # manifesto da execução histórica
├── src/
│   ├── config.py                  # configuração do pipeline
│   ├── search_terms.py            # consultas canônicas
│   ├── ingestion/                 # clientes das fontes
│   ├── processing/                # seleção, scoring e deduplicação
│   └── pipeline/                  # orquestração
├── data/
│   ├── mmat_assessments.csv
│   └── reference_audit.csv
├── exports/
│   ├── analysis/
│   ├── references/
│   ├── reports/
│   └── visualizations/
└── tests/
```

## Validação

A CI do TCC executa as regressões de pesquisa que cobrem, entre outros pontos:

- auditoria bibliográfica;
- consistência dos artefatos MMAT;
- consistência entre protocolo executado, exports e texto do TCC;
- requisitos editoriais/metodológicos do TCC;
- compilação LaTeX.

Para executar as regressões de pesquisa localmente:

```bash
cd research
python -m pytest tests -q
```

## Atualização da literatura em 2026

Uma eventual atualização do corpus está registrada na issue #26 e permanece condicionada à decisão com a orientação. Se aprovada, deverá ser tratada como atualização incremental e reproduzível, preservando o corpus de 2025 separadamente até a deduplicação e a nova triagem.
