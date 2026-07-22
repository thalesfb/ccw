# Gate de integração acadêmica dos resultados

## Finalidade

O pipeline produz dados, métricas, perfis e relatórios automaticamente. A redação acadêmica, porém, não deve ser atualizada apenas porque arquivos foram gerados.

Este gate determina quando uma execução está apta a fornecer tabelas para a metodologia e os resultados do TCC.

## Condições obrigatórias

A geração dos artefatos LaTeX exige:

1. manifesto final de execução;
2. commit Git completo e válido;
3. integridade de todos os artefatos por tamanho e SHA-256;
4. ausência de dados brutos na pasta da execução;
5. fonte registrada em `prototype/config/data_sources.json`;
6. domínio matemático;
7. papel `primary` ou `replication`;
8. manifesto de fonte consistente com o manifesto da execução;
9. fonte não identificada como dado sintético;
10. métricas declaradas para cada experimento;
11. perfil da execução selecionada;
12. níveis ordinais desabilitados;
13. alerta binário desabilitado.

Qualquer falha interrompe a geração.

## Artefatos produzidos

O comando:

```bash
tcc-prototype generate-academic-artifacts \
  --run-manifest data/runs/assistments-v1-primary/run.manifest.json \
  --approved-sources config/data_sources.json \
  --output-dir ../results/tcc/generated/assistments-v1-primary
```

produz quatro entradas LaTeX:

- `prototype_model_comparison.tex`;
- `prototype_data_quality.tex`;
- `prototype_skill_summary.tex`;
- `prototype_provenance.tex`.

### Comparação dos modelos

A tabela contém protocolo, modelo, semente, log-loss, Brier Score, ROC-AUC e erro esperado de calibração. Todas as combinações registradas no manifesto são incluídas.

### Qualidade dos dados

A tabela contém registros de entrada e saída, duplicatas, registros inválidos, estudantes, itens e habilidades.

### Síntese das habilidades

A tabela apresenta uma síntese descritiva do perfil selecionado:

- quantidade de estudantes;
- quantidade de evidências;
- probabilidade média estimada;
- quantidade de perfis com evidência insuficiente.

Ela não lista estudantes nem permite interpretar a probabilidade média como prevalência populacional de domínio.

### Proveniência

O bloco de proveniência registra execução, data, commit, fonte, versão, hash, partições, sementes e limites científicos.

## O que o comando não faz

- não edita capítulos do TCC;
- não escolhe o melhor modelo;
- não declara hipótese confirmada;
- não interpreta diferenças pequenas;
- não ativa níveis ou alertas;
- não gera conclusões causais;
- não publica dados estudantis;
- não substitui revisão humana dos resultados.

## PR final de integração

Depois da execução real, deverá ser aberto um PR específico contendo apenas:

1. manifesto da execução selecionada ou referência auditável a ele;
2. tabelas geradas;
3. figuras geradas por código;
4. atualização da metodologia com procedimentos efetivamente executados;
5. resultados quantitativos;
6. análise de calibração e erros;
7. análise de estabilidade entre seeds;
8. limitações e ameaças à validade;
9. atualização da conclusão sem alegar eficácia pedagógica.

Código de aquisição, preparação ou modelagem não deve ser misturado nesse PR final. Caso uma falha metodológica seja identificada, ela deve ser corrigida em um PR técnico anterior e o experimento deve ser executado novamente com outro `run-id`.

## Prática científica recomendada

Antes de redigir os resultados:

- conferir qualidade e cobertura das habilidades;
- verificar prevalência do alvo por partição;
- comparar variação entre sementes;
- avaliar calibração global e por habilidade;
- inspecionar erros e casos com baixa confiança;
- examinar dependência de itens e habilidades raros;
- registrar limitações da habilidade primária em interações multirrótulo;
- determinar se o candidato não linear oferece ganho relevante sobre a regressão;
- conservar todos os artefatos e configurações analisados.

O texto deve distinguir claramente resultado calculado, interpretação do autor e implicação pedagógica hipotética.
