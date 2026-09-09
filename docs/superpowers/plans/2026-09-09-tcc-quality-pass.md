# Plano de implementação — qualidade científica, apresentação e portal

**Data:** 2026-09-09

**Base:** `origin/main` em `07f991c` após o merge do PR #79.

**Estado:** em execução nesta branch; este documento acompanha implementação, testes e revisão, não substitui os artefatos entregues.

## Objetivo

Elevar o material do TCC de uma apresentação visualmente correta para uma comunicação acadêmica mais clara, responsiva, legível e metodologicamente proporcional à evidência efetivamente produzida.

## Evidências e restrições

- A revisão vigente retém 18 registros: 17 candidatos empíricos provisórios e 1 protocolo contextual.
- O MMAT permanece preliminar, por critério, sem escore agregado ou ranking.
- O PRISMA 2020 é tratado como diretriz de relato; o PRISMA-P não é declarado como conformidade integral.
- A especificação do protótipo é conceitual; não deve ser apresentada como aplicação funcional ou eficácia pedagógica demonstrada.
- As issues abertas #7, #24, #25, #26, #27, #28 e #29 continuam como contexto de continuidade e não serão encerradas por inferência.

## Frentes paralelas

1. **Apresentação Slidev:** melhorar hierarquia narrativa, contraste, densidade textual e responsividade sem alterar números ou reivindicações científicas.
2. **Portal público:** corrigir o header em larguras móveis e intermediárias, mantendo navegação acessível, foco visível e identificação da página.
3. **Capítulo de especificação:** transformar listas explicativas em prosa acadêmica nos princípios, requisitos não funcionais, critérios de dados, protocolo e arquitetura; preservar listas apenas quando a enumeração for o objeto.
4. **Resultados e Apêndice A:** auditar a seção de tendências/lacunas e o mapeamento PRISMA contra o texto e os artefatos atuais, corrigindo linguagem de conformidade e localizadores incorretos.
5. **Auditoria transversal:** revisar introdução, metodologia, resultados, conclusão, resumo e materiais de apresentação para termos temporais, relações entre evidência e afirmação, e distinção entre realizado, especificado e futuro.

## Critérios de aceite

- As seções solicitadas deixam de funcionar como uma sequência de tópicos telegráficos; a prosa explica relações, decisões e limites.
- Nenhum número, resultado, avaliação MMAT ou afirmação de eficácia é ampliado sem fonte versionada.
- O Apêndice A identifica itens completos, parciais e não apresentados com localizadores verificáveis; não afirma atendimento integral sem evidência.
- O header funciona em 375 px, 768 px e desktop, sem overflow horizontal e com navegação utilizável por teclado.
- `npm test`, `npm run validate`, build Slidev, compilação LaTeX e validações de pesquisa passam.
- A inspeção visual cobre capa, slides densos, fluxo PRISMA, MMAT, próximos passos e encerramento com QR code.
- O PR registra claramente mudanças implementadas, pendências científicas e limitações restantes.

## Integração

Cada frente editará um conjunto de arquivos sem sobreposição. Após o retorno dos agentes, a integração será revisada contra este plano, seguida de testes completos, inspeção visual e uma revisão final de qualidade em cinco eixos: correção, legibilidade, arquitetura, segurança e desempenho.
