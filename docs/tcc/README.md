# Governança de engenharia documental do TCC

Este diretório registra decisões de engenharia relacionadas à produção, validação e manutenção do documento acadêmico do TCC. O objetivo é separar explicitamente três dimensões que não devem ser confundidas: conteúdo científico, requisitos institucionais e normativos, e implementação técnica em LaTeX.

## Estado

Este diretório contém tanto notas do estado implementado quanto políticas e
propostas futuras. A nota de estado, a cobertura das fontes e as auditorias
descrevem evidências e pendências atuais; o roadmap identifica trabalho futuro.
Uma proposta documentada não comprova sua implementação. Alterações na classe,
no conteúdo ou nos workflows exigem mudanças verificáveis e revisão humana.

## Documentos

- [`NORMATIVE_GOVERNANCE.md`](NORMATIVE_GOVERNANCE.md): política para fontes normativas e institucionais, preservação de particularidades do IFC, detecção de drift e resolução de conflitos.
- [`ABNT-2025-CORRECOES.md`](ABNT-2025-CORRECOES.md): linha de base normativa documentada, correções verificáveis e limites de conformidade institucional.
- [`DOCUMENT_ENGINEERING_ROADMAP.md`](DOCUMENT_ENGINEERING_ROADMAP.md): arquitetura proposta para previews de PR, verificações de conformidade, monitoramento de mudanças externas e eventual contribuição upstream após a conclusão do TCC.
- [`PROJECT_INTEGRATION.md`](PROJECT_INTEGRATION.md): separação entre conteúdo científico, engenharia documental, implementação computacional e requisitos institucionais.
- [`PRESENTATION_GOVERNANCE.md`](PRESENTATION_GOVERNANCE.md): governança da apresentação Slidev do TCC, distinção entre o template de referência e requisitos do trabalho, identidade IFC, QR e critérios de legibilidade.
- [`ESTADO-ATUAL-TCC.md`](ESTADO-ATUAL-TCC.md): estado público, limites interpretativos e decisões metodológicas pendentes da versão atual.
- [`AUDITORIA-ESTUDOS-SINTESE.md`](AUDITORIA-ESTUDOS-SINTESE.md): papel sustentado, limites e pendências dos 18 candidatos, não 18 inclusões empíricas finais.
- [`SOURCE-COVERAGE-AND-CONTRIBUTIONS.md`](SOURCE-COVERAGE-AND-CONTRIBUTIONS.md): matriz de cobertura e contribuições derivada dos registros estruturados.
- [`REUNIAO-DECISAO-ESCOPO.md`](REUNIAO-DECISAO-ESCOPO.md): material comparativo dos cenários A/B/C para a reunião de decisão de escopo (#27); não registra decisão.
- [`DOCUMENTATION_SYNC.md`](DOCUMENTATION_SYNC.md): fontes, consumidores e verificação das informações espelhadas.
- [`PUBLICATION_GOVERNANCE.md`](PUBLICATION_GOVERNANCE.md): critérios para separar relato acadêmico, proveniência técnica e fluxo público de desenvolvimento.
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

O registro inicial das fontes institucionais foi feito em **2026-08-07**. As páginas
do SIBI/IFC, da Biblioteca do Campus Videira e do curso foram reconsultadas em
**2026-10-11**; os links do Drive solicitaram autenticação nessa consulta.
Posteriormente, o pacote tradicional de 2026 fornecido localmente foi comparado
em **2026-10-14**, conforme
[`ABNT-2025-CORRECOES.md`](ABNT-2025-CORRECOES.md). A identidade criptográfica com
o arquivo remoto e o pacote de desenvolvimento não foram confirmados. A decisão
institucional sobre capa e folha de rosto continua pendente; não se declara
conformidade integral. As datas registram a consulta, não garantem vigência futura.
