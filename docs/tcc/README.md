# Governança de engenharia documental do TCC

Este diretório registra decisões de engenharia relacionadas à produção, validação e manutenção do documento acadêmico do TCC. O objetivo é separar explicitamente três dimensões que não devem ser confundidas: conteúdo científico, requisitos institucionais e normativos, e implementação técnica em LaTeX.

## Estado

**Documentação de arquitetura e trabalho futuro.**

Os documentos deste diretório não alteram, por si só, a classe LaTeX, o conteúdo científico, a formatação do TCC ou os workflows existentes. Qualquer implementação futura deve ocorrer em pull requests próprios, com escopo reduzido, evidências de regressão e revisão humana.

## Documentos

- [`NORMATIVE_GOVERNANCE.md`](NORMATIVE_GOVERNANCE.md): política para fontes normativas e institucionais, preservação de particularidades do IFC, detecção de drift e resolução de conflitos.
- [`DOCUMENT_ENGINEERING_ROADMAP.md`](DOCUMENT_ENGINEERING_ROADMAP.md): arquitetura proposta para previews de PR, verificações de conformidade, monitoramento de mudanças externas e eventual contribuição upstream após a conclusão do TCC.
- [`PROJECT_INTEGRATION.md`](PROJECT_INTEGRATION.md): posicionamento da engenharia documental em relação à issue #7, ao merge do PR #6 e à sequência de revisão dos PRs científicos e técnicos.
- [`../adr/0001-preserve-ifc-institutional-formatting.md`](../adr/0001-preserve-ifc-institutional-formatting.md): registro da decisão arquitetural de não substituir automaticamente particularidades institucionais durante atualizações normativas.

## Princípios

1. **A norma não é o código.** Normas e regulamentos descrevem requisitos; classes, pacotes e comandos LaTeX são implementações desses requisitos.
2. **A classe LaTeX não é a autoridade normativa.** O comportamento atual deve ser rastreado até uma fonte institucional, normativa ou decisão técnica explícita.
3. **Particularidades institucionais são preservadas por padrão.** Elementos como capa, folha de rosto, identidade visual e outros componentes definidos pelo IFC não devem ser substituídos em razão de uma atualização genérica de ABNT sem análise de aplicabilidade.
4. **Conflitos devem ser visíveis.** Divergências entre norma, orientação institucional e implementação devem ser registradas como drift, nunca resolvidas silenciosamente.
5. **Automação não substitui julgamento acadêmico ou institucional.** O CI pode verificar propriedades objetivas e sinalizar riscos; decisões interpretativas permanecem humanas.
6. **Toda decisão relevante deve ser reproduzível.** Fonte, versão, data de verificação, componente afetado, decisão e evidência de validação devem ser registradas.

## Escopo excluído

Esta documentação não:

- declara conformidade integral do TCC com qualquer edição da ABNT;
- reproduz o conteúdo integral de normas técnicas protegidas;
- substitui instruções da Coordenação de TCC, do orientador, do Colegiado ou do Sistema Integrado de Bibliotecas do IFC;
- autoriza migração automática da classe `abntex2-IFC`;
- define que uma norma geral sempre prevalece sobre uma particularidade institucional;
- propõe alterações de conteúdo científico como consequência de mudanças editoriais.

## Baseline de verificação

As fontes públicas institucionais descritas nos documentos deste diretório foram verificadas em **2026-08-07**. Como páginas, regulamentos, templates e normas podem mudar, essa data é parte da proveniência e não deve ser interpretada como garantia de vigência futura.
