# Governança normativa e institucional do documento

## 1. Objetivo

Este documento define a política de governança para requisitos de apresentação, normalização e identidade institucional aplicáveis ao TCC. Seu propósito é permitir que mudanças em normas técnicas, orientações do IFC ou implementação LaTeX sejam avaliadas de forma rastreável, sem converter automaticamente uma mudança externa em alteração de código.

A política adota um princípio central:

> Uma atualização normativa invalida pressupostos que dependem da norma, mas não invalida automaticamente particularidades institucionais. Cada regra afetada deve ser reavaliada no domínio em que se aplica.

## 2. Separação de responsabilidades

A manutenção do documento deve distinguir quatro camadas.

### 2.1 Conteúdo científico

Compreende problema de pesquisa, objetivos, fundamentação, metodologia, resultados, discussão, conclusões e demais argumentos acadêmicos. Mudanças editoriais ou normativas não autorizam alterações científicas automáticas.

### 2.2 Autoridade institucional

Compreende regulamentos, instruções da Coordenação de TCC, decisões do Colegiado, templates institucionais e orientações do Sistema Integrado de Bibliotecas do IFC. Esses artefatos podem definir particularidades próprias, inclusive sobre elementos pré-textuais e procedimentos de entrega.

### 2.3 Autoridade normativa

Compreende normas técnicas aplicáveis, especialmente as relacionadas à apresentação de trabalhos acadêmicos, citações, referências, resumos, sumário e demais elementos de normalização. O conteúdo normativo deve ser consultado pelos canais licenciados disponibilizados pelo IFC quando necessário.

### 2.4 Implementação técnica

Compreende a classe `abntex2-IFC`, classes-base, pacotes, comandos LaTeX, scripts, workflows, validadores, conversores e demais mecanismos usados para produzir e verificar o documento. Essa camada implementa decisões; não constitui, por si só, fonte de autoridade normativa.

## 3. Fontes institucionais de referência

Baseline pública verificada em **2026-08-07**:

| Identificador | Fonte | Papel |
|---|---|---|
| `ifc-videira-tcc-page` | https://videira.ifc.edu.br/ciencia-da-computacao/defesas-de-tc/ | Página do curso que publica modelos LaTeX para PTC, TC tradicional e TC de desenvolvimento, além do regulamento. |
| `ifc-videira-tcc-regulation-2023` | https://videira.ifc.edu.br/ciencia-da-computacao/wp-content/uploads/sites/11/2024/06/regulamento-TC-2023.pdf | Regulamento de PTCC/TCC do Bacharelado em Ciência da Computação do Campus Videira. |
| `ifc-sibi-tcc-templates` | https://biblioteca.ifc.edu.br/tcc/ | Templates e orientações do Sistema Integrado de Bibliotecas do IFC, incluindo referência à Portaria Normativa nº 6/2022 do CONSEPE. |
| `ifc-sibi-abnt-access` | https://biblioteca.ifc.edu.br/acesso-as-normas-da-abnt/ | Canal institucional para consulta das normas ABNT disponibilizadas à comunidade acadêmica. |

O regulamento de 2023 estabelece, para PTCC e TCC, a observância dos padrões nacionais adotados pela ABNT **ou de critérios definidos pelo Coordenador do TCC para elaboração**. Também atribui à Coordenação de TCC a possibilidade de estabelecer instruções complementares e ao orientador a orientação sobre normas técnicas. Consequentemente, não é tecnicamente correto modelar a governança como uma precedência total e automática do tipo `ABNT > IFC`.

### 3.1 Observação sobre os modelos públicos

Na data de verificação, a página pública do curso direcionava os modelos LaTeX para arquivos disponibilizados por Google Drive. Não foi identificado, a partir dessa página institucional, um repositório Git público explicitamente indicado como fonte canônica dos modelos. Uma futura contribuição upstream deve primeiro identificar o mantenedor e o repositório canônico, ou confirmar com a instituição o canal apropriado para contribuição.

## 4. Modelo de autoridade por domínio

A resolução deve considerar **qual componente está sendo regulado** e **qual fonte possui autoridade sobre aquele componente**. Não se adota uma hierarquia global única.

### 4.1 Componentes institucionais com preservação estrita

Exemplos:

- capa;
- folha de rosto;
- folha de aprovação;
- logotipos, brasões e identidade visual;
- textos institucionais obrigatórios;
- composição definida por template oficial do IFC;
- requisitos específicos de depósito ou entrega institucional.

Esses componentes recebem classificação `institutional-strict`. Uma atualização de norma geral pode abrir uma revisão, mas não autoriza substituição automática.

### 4.2 Componentes predominantemente normativos

Exemplos:

- estrutura e ordem de elementos acadêmicos quando não houver especialização institucional;
- regras de citações;
- referências bibliográficas;
- numeração progressiva;
- sumário;
- propriedades gerais de apresentação quando não houver regra institucional específica.

Esses componentes recebem classificação `normative-derived` e podem ser atualizados após análise de aplicabilidade e teste de regressão.

### 4.3 Componentes técnicos internos

Exemplos:

- pacotes LaTeX;
- organização de arquivos;
- comandos auxiliares;
- mecanismo de compilação;
- cache;
- geração de PDF/A;
- lint e testes de CI.

Esses componentes recebem classificação `technical-internal`. Podem evoluir desde que preservem os requisitos observáveis das camadas superiores.

## 5. Regra de preservação institucional

Nenhum workflow de conformidade deve modificar automaticamente componentes classificados como `institutional-strict`.

Uma mudança nesses componentes exige, no mínimo:

1. identificação da fonte que motivou a revisão;
2. comparação com a fonte institucional vigente;
3. registro do tipo de drift;
4. avaliação humana;
5. decisão documentada;
6. teste de regressão visual e estrutural;
7. pull request dedicado.

A ausência de atualização recente de uma classe ou template não constitui evidência suficiente de não conformidade. Da mesma forma, a existência de um pacote LaTeX mais novo não constitui evidência suficiente para substituição.

## 6. Taxonomia de drift

### `NORMATIVE_DRIFT`

Uma norma utilizada pela baseline foi revisada, substituída, corrigida ou teve sua aplicabilidade alterada.

**Efeito:** revisar regras derivadas daquela norma. Não alterar automaticamente particularidades institucionais.

### `INSTITUTIONAL_DRIFT`

O IFC, o Campus Videira, a Coordenação de TCC, o Colegiado ou o SIBI alterou regulamento, template, orientação ou procedimento relevante.

**Efeito:** comparar o comportamento atual com a nova orientação e identificar componentes afetados.

### `IMPLEMENTATION_DRIFT`

O código LaTeX ou pipeline produz comportamento divergente da baseline institucional/normativa declarada, ainda que as fontes externas não tenham mudado.

**Efeito:** corrigir a implementação em PR próprio, preservando os requisitos superiores.

### `NORMATIVE_INSTITUTIONAL_CONFLICT`

Uma nova interpretação ou versão normativa parece entrar em conflito com uma particularidade institucional vigente.

**Efeito:** bloquear correção automática, registrar evidências e encaminhar para decisão humana. Quando necessário, consultar Coordenação de TCC, orientação ou biblioteca antes de alterar a implementação.

## 7. Protocolo de avaliação de mudança

Toda mudança externa relevante deve seguir o seguinte fluxo:

1. **Detectar:** identificar qual fonte mudou e em que data.
2. **Delimitar:** identificar as regras potencialmente afetadas.
3. **Mapear:** associar cada regra aos componentes observáveis do PDF e aos arquivos de implementação.
4. **Classificar:** marcar o componente como `institutional-strict`, `normative-derived` ou `technical-internal`.
5. **Comparar:** avaliar fonte anterior, fonte atual, comportamento vigente e comportamento proposto.
6. **Classificar o drift:** usar uma das categorias da Seção 6.
7. **Decidir:** registrar se a ação é `no-change`, `update`, `exception` ou `needs-institutional-review`.
8. **Validar:** executar verificações automáticas, inspeção visual e revisão humana aplicáveis.
9. **Rastrear:** vincular decisão, evidências, commit, PR e resultado dos checks.

## 8. Registro de regra

Uma implementação futura pode manter regras em estrutura versionada semelhante a:

```yaml
id: pretextual.cover.layout
domain: pretextual.cover
classification: institutional-strict
authority:
  source: ifc-videira-tcc-template
  verified_at: 2026-08-07
verification:
  mode: visual
  severity: error
implementation:
  files:
    - results/tcc/abntex2-IFC.cls
change_policy:
  automatic_update: false
  institutional_review_on_conflict: true
```

Esse registro deve armazenar apenas metadados, interpretação operacional e referências necessárias para auditoria. O texto integral de normas técnicas não deve ser versionado no repositório quando sua licença não permitir redistribuição.

## 9. Classes de verificação

### 9.1 Automática

Adequada a propriedades objetivamente observáveis, por exemplo:

- compilação sem erro;
- referências e citações resolvidas;
- presença de elementos obrigatórios conhecidos;
- tamanho da página;
- fontes incorporadas;
- metadados do PDF;
- conformidade PDF/A quando requerida;
- inexistência de arquivos ou recursos ausentes.

Uma verificação automática pode bloquear merge somente quando a regra, a interpretação e o mecanismo de teste forem suficientemente objetivos.

### 9.2 Semiautomática

Adequada quando a ferramenta pode detectar indícios, mas não concluir conformidade, por exemplo:

- margens aproximadas;
- posição de números de página;
- espaçamento de blocos;
- citações longas;
- legendas;
- possíveis violações tipográficas.

O resultado deve ser `REVIEW` ou `WARN`, não uma declaração absoluta de conformidade.

### 9.3 Manual

Obrigatória para aspectos interpretativos ou institucionais, incluindo:

- fidelidade de capa e folha de rosto ao modelo vigente;
- conflito entre norma e instrução institucional;
- qualidade acadêmica e linguística;
- pertinência de exceções;
- decisões que dependam de orientação da Coordenação, orientador, banca ou biblioteca.

## 10. Evidência e rastreabilidade

Toda decisão normativa ou institucional material deve registrar:

- fonte e URL;
- versão, edição ou identificação disponível;
- data de verificação;
- seção ou dispositivo relevante quando permitido;
- interpretação operacional adotada;
- componente afetado;
- classificação de autoridade;
- classificação de drift;
- decisão;
- responsável pela revisão;
- PR/commit que implementou a decisão;
- evidências de teste e inspeção visual.

O histórico Git registra quando o código mudou; esse registro deve explicar **por que** ele mudou.

## 11. Política para normas protegidas

O repositório não deve redistribuir textos integrais de normas técnicas sem autorização. Para normas acessíveis pela assinatura institucional, deve-se registrar metadados, referências de seção quando necessário, interpretação resumida e testes derivados. A consulta da fonte primária deve ocorrer pelo canal institucional disponibilizado pelo SIBI.

## 12. Política de mudança da classe LaTeX

A classe atual deve ser tratada como implementação legada a ser auditada, e não como especificação imutável nem como artefato descartável.

Uma futura auditoria deve decompor seu comportamento em:

1. identidade e particularidades do IFC;
2. regras derivadas de normas técnicas;
3. escolhas técnicas internas e legado de implementação.

Somente as categorias 2 e 3 são candidatas naturais a modernização por mudança normativa ou técnica. A categoria 1 deve ser preservada até existir orientação institucional explícita que justifique sua alteração.

## 13. Contribuição upstream futura

Após a conclusão do TCC, uma eventual contribuição ao modelo institucional deve ser tratada como projeto independente. Antes de propor mudanças ao IFC, deve-se:

1. confirmar qual é a fonte canônica e quem mantém o modelo;
2. reproduzir o comportamento vigente em fixtures de teste;
3. separar correções normativas de identidade institucional;
4. documentar compatibilidade e regressões;
5. propor mudanças incrementais;
6. respeitar a decisão dos mantenedores e o processo institucional de aprovação.

Essa contribuição futura não integra o escopo de conclusão do TCC atual.
