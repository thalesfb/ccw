# Relatório autônomo de apoio docente

## Objetivo

A interface do protótipo foi materializada como um relatório HTML autônomo. A escolha reduz dependências operacionais, evita envio de dados a serviços externos e permite que o artefato seja aberto localmente, arquivado e auditado junto aos resultados do experimento.

O relatório não é uma aplicação de diagnóstico. Ele organiza evidências, probabilidades e limitações para revisão humana.

## Entradas

O gerador utiliza somente artefatos produzidos pelo pipeline:

- perfil por estudante e habilidade em Parquet;
- métricas globais e por habilidade em JSON;
- importância por permutação em CSV;
- metadados informados na execução, como base e versão do modelo.

A interface não recalcula o modelo e não modifica os resultados.

## Privacidade

Os identificadores originais dos estudantes não são inseridos no HTML. Cada identificador é transformado por SHA-256 com um sal fornecido no momento da exportação.

O sal:

- não deve ser commitado;
- pode ser fornecido pela variável `TCC_PSEUDONYM_SALT`;
- deve ser diferente entre contextos quando não houver necessidade de vinculação;
- não transforma dados pessoais em dados anônimos por si só, mas reduz exposição direta no relatório.

A proteção completa depende da origem, dos demais atributos e da política de acesso ao arquivo.

## Conteúdo

O relatório apresenta:

- base e versão do modelo;
- contagem de estudantes e habilidades;
- quantidade de perfis com evidência insuficiente;
- seleção de estudante pseudonimizado;
- probabilidade estimada por habilidade;
- quantidade de evidências;
- desempenho observado e intervalo de Wilson;
- estado de suficiência das evidências;
- nível ordinal somente quando previamente ativado;
- comparação técnica dos modelos;
- importância por permutação;
- campo local para notas de revisão docente;
- exportação do perfil selecionado em CSV;
- opção de impressão.

## Acessibilidade

O HTML usa:

- estrutura semântica com cabeçalhos, seções, tabelas e rótulos;
- navegação por teclado;
- foco visível;
- aviso com função de alerta;
- contraste textual;
- layout responsivo;
- versão adequada para impressão;
- texto, e não apenas cor, para indicar evidência insuficiente.

A acessibilidade deverá ser verificada manualmente e com ferramentas automatizadas antes de qualquer uso externo.

## Segurança do conteúdo

Dados incorporados ao HTML são serializados como JSON e caracteres capazes de encerrar o elemento `script` são escapados. A tabela é construída com `textContent`, evitando interpretar habilidades ou valores como marcação HTML.

O relatório não carrega bibliotecas, fontes, scripts ou recursos remotos. Depois de gerado, nenhuma informação é enviada pela página.

## Limitações

- notas digitadas não são persistidas automaticamente;
- o arquivo pode conter informações educacionais sensíveis mesmo com pseudônimos;
- a visualização não substitui um fluxo institucional de controle de acesso;
- intervalos exibidos descrevem o desempenho observado, não toda a incerteza preditiva;
- a interface não foi submetida a avaliação de usabilidade com professores;
- sua existência não demonstra eficácia pedagógica.

## Comando

```bash
export TCC_PSEUDONYM_SALT='valor-secreto-local'

tcc-prototype build-teacher-report \
  --profiles data/reports/candidate_temporal_seed_2026.skill_profiles.parquet \
  --metrics data/reports/candidate_temporal_seed_2026.metrics.json \
  --importance data/reports/candidate_temporal_seed_2026.permutation_importance.csv \
  --output data/reports/teacher-report.html \
  --dataset-label 'ASSISTments Skill Builder 2009–2010 corrigido' \
  --model-version '0.2.0'
```

O relatório gerado deverá ser tratado como artefato derivado e associado ao mesmo manifesto, configuração, seed e commit dos resultados de origem.
