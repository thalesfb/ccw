# Roadmap de engenharia documental do TCC

## 1. Propósito

Este documento registra uma arquitetura futura para tornar a revisão do TCC mais rastreável, reproduzível e segura. A proposta cobre geração de previews por pull request, verificações de conformidade, detecção de mudanças em fontes externas e auditoria da implementação LaTeX.

**Estado:** planejamento. A implementação está deliberadamente adiada para não ampliar o escopo técnico durante a consolidação do TCC.

## 2. Objetivos de engenharia

A evolução futura deve permitir que um revisor:

1. leia o PDF integral correspondente ao SHA atual de um PR sem compilar localmente;
2. compare visualmente o documento proposto com a base de referência;
3. identifique quais verificações objetivas passaram ou falharam;
4. diferencie erro de compilação, possível não conformidade e decisão que requer julgamento humano;
5. saiba quais fontes institucionais ou normativas fundamentam cada regra;
6. detecte drift sem alterar automaticamente particularidades do IFC;
7. reproduza os artefatos a partir do commit registrado.

## 3. Não objetivos

A arquitetura não deve:

- reescrever automaticamente o conteúdo acadêmico;
- declarar conformidade integral com ABNT por heurística;
- substituir automaticamente a classe institucional;
- modificar capa, folha de rosto ou identidade visual em resposta a atualizações genéricas;
- selecionar uma interpretação normativa sem evidência e revisão humana;
- transformar métricas técnicas de compilação em avaliação de qualidade científica;
- incorporar ao TCC atual uma contribuição upstream ao template institucional.

## 4. Fase A — preview de pull request

### 4.1 Workflow proposto

Nome sugerido: `tcc-preview.yml`.

Disparadores:

- `pull_request` quando houver alteração em fontes LaTeX, bibliografia, imagens, artefatos que alimentam o documento ou código de geração relacionado;
- `workflow_dispatch` para regeneração explícita.

### 4.2 Artefatos

Cada execução deve produzir:

- `tcc-preview.pdf`: documento integral limpo;
- `tcc-diff.pdf`: comparação renderizada quando tecnicamente possível;
- `build.log`: log completo de compilação;
- `manifest.json`: proveniência da execução;
- relatório resumido de warnings relevantes.

### 4.3 Manifesto mínimo

```json
{
  "pull_request": 0,
  "base_ref": "main",
  "base_sha": "...",
  "head_ref": "...",
  "head_sha": "...",
  "latex_entrypoint": "results/tcc/main.tex",
  "generated_at": "...",
  "pdf_sha256": "...",
  "status": "success"
}
```

### 4.4 Experiência de revisão

O PR deve receber um comentário persistente, atualizado a cada execução, contendo:

- status da compilação;
- SHA compilado;
- acesso ao PDF integral;
- acesso ao diff quando disponível;
- acesso aos logs e manifesto;
- aviso explícito quando o preview estiver desatualizado em relação ao HEAD do PR.

O comentário deve ser atualizado, não duplicado, mediante marcador estável.

### 4.5 Publicação

Preferência arquitetural:

1. preview navegável por PR, sem commit de PDF na branch de origem;
2. artefato do GitHub Actions como fallback;
3. retenção suficiente para revisão acadêmica prolongada;
4. remoção ou arquivamento controlado após fechamento do PR.

O mecanismo de publicação deve ser avaliado considerando permissões, segurança de conteúdo de forks e manutenção do GitHub Pages.

## 5. Fase B — pipeline de conformidade

### 5.1 Workflow proposto

Nome sugerido: `tcc-compliance.yml`.

O workflow deve produzir um relatório estruturado, não apenas um código de saída.

### 5.2 Categorias de resultado

- `PASS`: propriedade objetiva verificada.
- `FAIL`: regra objetiva não atendida e suficientemente bem especificada.
- `WARN`: indício técnico que merece atenção.
- `REVIEW`: decisão que exige inspeção humana.
- `NOT_APPLICABLE`: regra não aplicável ao documento ou ao escopo atual.

### 5.3 Verificações candidatas

#### Compilação e integridade

- build LaTeX completo;
- referências cruzadas indefinidas;
- citações sem entrada bibliográfica;
- recursos ausentes;
- erros de BibTeX/Biber;
- comandos de revisão remanescentes.

#### PDF

- formato de página;
- fontes incorporadas;
- metadados;
- hyperlinks e bookmarks;
- páginas vazias inesperadas;
- PDF/A quando requerido para entrega;
- hash do artefato.

#### Tipografia e layout

- `overfull`/`underfull boxes` com política de severidade explícita;
- possíveis violações de margem;
- consistência de legendas e fontes;
- posição aproximada de elementos verificáveis.

#### Estrutura acadêmica

- presença dos elementos obrigatórios conhecidos;
- ordem estrutural quando objetivamente definida;
- referências bibliográficas resolvidas;
- ausência de elementos temporários ou placeholders explicitamente proibidos pelo projeto.

### 5.4 Limite epistemológico

O resultado do workflow deve evitar a afirmação genérica “ABNT compliant”. A automação comprova somente as propriedades que efetivamente testa. Uma execução bem-sucedida significa que os checks implementados passaram; não significa conformidade normativa total nem aprovação acadêmica.

## 6. Fase C — baseline normativa versionada

Uma implementação futura deve manter um registro legível por máquina das fontes e regras operacionais, sem redistribuir conteúdo protegido.

Estrutura candidata:

```text
compliance/
├── sources.yml
├── rules/
│   ├── institutional.yml
│   ├── normative.yml
│   └── technical.yml
├── fixtures/
│   └── normative-sample.tex
└── schemas/
    └── rule.schema.json
```

### 6.1 Fixture normativa

`normative-sample.tex` deve exercitar, de forma mínima e estável:

- capa e folha de rosto;
- resumo e palavras-chave;
- sumário;
- múltiplos níveis de seção;
- citações diretas curta e longa;
- citação indireta;
- figura, quadro e tabela;
- equação;
- nota de rodapé;
- referências de naturezas distintas;
- apêndice e anexo.

O objetivo é produzir uma superfície de regressão independente do conteúdo científico do TCC.

## 7. Fase D — monitoramento de drift

### 7.1 Workflow proposto

Nome sugerido: `normative-watch.yml`.

Frequência: baixa e adequada ao ritmo de mudança das fontes, por exemplo semanal ou mensal, além de execução manual.

### 7.2 Fontes monitoráveis

- página do curso de Ciência da Computação do Campus Videira;
- regulamento de PTCC/TCC;
- links dos modelos institucionais;
- página do SIBI para templates e orientações;
- catálogo institucional de normas;
- versões de dependências técnicas utilizadas pela compilação.

### 7.3 Comportamento

O monitoramento deve comparar metadados e fingerprints públicos quando tecnicamente e juridicamente apropriado. Ao detectar alteração, deve gerar um evento de revisão, preferencialmente uma issue, contendo:

- fonte;
- fingerprint anterior e atual;
- data da detecção;
- tipo provável de drift;
- componentes potencialmente afetados;
- ação requerida: revisão humana.

**O workflow não deve alterar automaticamente a classe LaTeX.**

## 8. Fase E — auditoria da classe institucional

A classe `abntex2-IFC` deve ser auditada por comportamento, não por idade.

A auditoria deve classificar cada customização como:

1. `institutional-strict`;
2. `normative-derived`;
3. `technical-internal`;
4. `unknown`, quando não houver proveniência suficiente.

Para cada item deve ser documentado:

- comportamento atual;
- origem provável;
- fonte de autoridade confirmada;
- risco de mudança;
- fixture ou página de regressão;
- decisão de preservar, corrigir ou substituir.

Uma possível migração de classe ou pacote só deve ser avaliada depois dessa decomposição.

## 9. Fase F — contribuição upstream pós-TCC

Após a conclusão do TCC e fora do escopo de entrega acadêmica atual, os resultados da auditoria podem fundamentar uma contribuição ao modelo institucional.

A contribuição deve seguir princípios de software livre e engenharia institucional responsável:

- identificar mantenedores e fonte canônica;
- abrir discussão antes de mudanças incompatíveis;
- separar correções de bug, atualização normativa e refatoração técnica;
- preservar identidade institucional por padrão;
- incluir fixtures e testes de regressão;
- documentar migração;
- evitar dependência do repositório deste TCC para funcionamento do modelo institucional;
- aceitar que a decisão final pertence aos mantenedores e às instâncias institucionais responsáveis.

## 10. Estratégia de pull requests

A implementação futura deve ser incremental. Sequência sugerida:

1. preview e manifesto;
2. comentário persistente no PR;
3. checks objetivos de integridade;
4. fixture normativa;
5. baseline de fontes e regras;
6. verificações semiautomáticas;
7. monitoramento de drift;
8. auditoria completa da classe;
9. eventuais correções técnicas;
10. eventual contribuição upstream.

Cada PR deve ter um objetivo verificável e não misturar revisão científica do TCC com modernização da infraestrutura editorial.

## 11. Critérios de aceite arquitetural

A primeira versão operacional do sistema de engenharia documental será considerada adequada quando:

- todo PR relevante produzir PDF rastreado por SHA;
- o PDF puder ser lido sem checkout local;
- uma nova execução substituir claramente a anterior;
- falhas de compilação bloquearem mudanças relevantes;
- o relatório diferenciar `FAIL`, `WARN` e `REVIEW`;
- regras possuírem proveniência;
- componentes `institutional-strict` não puderem ser modificados automaticamente;
- drift externo abrir revisão, não patch automático;
- o histórico permitir reconstruir por que uma mudança editorial foi aprovada.

## 12. Riscos principais

| Risco | Mitigação |
|---|---|
| Falso senso de conformidade | Evitar selo global; reportar apenas checks implementados. |
| Substituição acidental de identidade IFC | `institutional-strict` + revisão humana obrigatória. |
| Fonte externa muda sem aviso | monitoramento de drift e datas de verificação. |
| Regra protegida é copiada para o repositório | armazenar somente metadados e interpretação operacional permitida. |
| Preview não corresponde ao PR atual | manifesto e validação do `head_sha`. |
| Modernização técnica altera layout | fixture estável e regressão visual. |
| Pipeline cresce durante o TCC | implementação explicitamente adiada e separada do conteúdo científico. |

## 13. Condição para iniciar implementação

A execução deste roadmap deve começar somente quando houver uma decisão explícita de retomar engenharia documental, preferencialmente após a consolidação acadêmica do TCC e sem concorrência com revisões essenciais à defesa ou entrega final.
