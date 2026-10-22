# Coerência entre manuscrito, documentação e apresentação

O texto do TCC é a fonte do relato científico. Os artefatos estruturados
versionados sustentam contagens, disposições e localizadores; uma divergência
entre eles e o manuscrito deve ser investigada, não resolvida escolhendo o
número mais conveniente. Slides, páginas, READMEs e imagens são consumidores
desse relato, não versões independentes do método ou dos objetivos.

## Fontes e consumidores

| Informação | Fonte | Consumidores que devem ser conferidos juntos |
| --- | --- | --- |
| Pergunta, objetivo geral e objetivos específicos | `results/tcc/conteudo/introducao.tex` | READMEs, Slidev, storyboard, export PPTX e infográfico |
| Fluxo de seleção e datas do snapshot | `research/exports/reports/reproducibility_manifest.json`, confrontado com o escopo e os exports | Manuscrito, reconciliação, relatórios, site, slides e infográfico |
| Respostas MMAT e seus denominadores | CSVs de escopo, reapreciação e componentes em `research/data/` | Tabelas geradas, manuscrito, página MMAT, resumos, slides e infográfico |
| Disponibilidade e cobertura documental | `study_contribution_current.json` e `evidence_sources_current.json` | Matriz de cobertura, auditoria de estudos, notas de estado e páginas |
| Estado técnico do código | Código, testes e evidência de execução | Guias operacionais e notas de estado, sem alegação de eficácia educacional |
| Exigência institucional ou normativa | Fonte e comparação registradas na governança normativa | Fontes LaTeX, documentação de conformidade e material visual afetado |

Os caminhos sem prefixo da quarta linha pertencem a `research/data/`. O registro
de revisão enumera as superfícies atualmente acompanhadas. Documentos novos ou
novos espelhamentos devem ser adicionados ao contrato, não deixados implícitos.

## Procedimento na mesma alteração

Depois de alterar a fonte canônica, execute, na raiz do repositório:

```bash
python scripts/sync_project_docs.py --write
```

Esse comando atualiza somente os blocos `ccw-sync` registrados no script: objetivos,
resumo do snapshot, fluxo e cobertura por fonte. Não consulta APIs, não lê o
SQLite operacional, não altera respostas MMAT e não decide elegibilidade.
Os testes existentes continuam responsáveis por confrontar as contagens com
os ledgers e por validar os demais artefatos derivados.

Em seguida, revise os trechos manuais das páginas, os resumos de cada apresentação
e as imagens. Resumir é permitido; mudar o sentido, o estágio ou a ressalva não.
Confira tipografia, números e palavras desenhadas nas imagens. Preserve snapshots
históricos com data e aviso explícitos, sem convertê-los em resultados atuais.
A fala da defesa continua fora desta rodada, até a aprovação do conteúdo.

Somente após essa conferência, registre a revisão de consistência assistida:

```bash
python scripts/sync_project_docs.py --record-review
python scripts/sync_project_docs.py --check
python -m pytest research/tests/test_documentation_sync.py -q
```

O registro público armazena hashes dos insumos e das superfícies conferidas,
normalizando apenas finais de linha de arquivos textuais. Não armazena caminhos
privados, PDFs de terceiros ou transcrições. A revisão científica humana continua
marcada como pendente; esse registro não é assinatura, aprovação da orientação
ou certificação semântica automática.

## Limites e publicação

`--check` é somente leitura e falha quando um bloco diverge da fonte, faltam
marcadores ou os insumos e resumos mudaram depois da revisão registrada. O modo
`--write` não renova essa revisão automaticamente. O CI executa a conferência
antes de considerar os documentos consistentes; não faz commits de correção.

O controle detecta desatualização no conjunto registrado, mas não prova a
corretude de todas as frases. É possível registrar uma revisão insuficiente;
por isso, o PR deve informar o que foi confrontado e conservar a revisão humana.
Criar uma página, imagem ou export novo exige atualizar a lista de consumidores
e seus testes. O contrato também não substitui as verificações de PDF,
visualizações derivadas, página MMAT ou renderização do Slidev.

Um PR ou build local atualizado não significa que a versão pública já mudou.
A publicação exige integração à `main` e conclusão do workflow de Pages. A
revisão deve distinguir explicitamente conteúdo proposto, integrado e publicado.
