# Registro da revisão do TCC

A revisão é acompanhada pela issue #5 e pelo PR #6.

## Decisões aplicadas

- A revisão sistemática da literatura é a etapa de pesquisa concluída.
- A seleção de tecnologias e bases, a implementação e a validação experimental permanecem como etapas posteriores.
- Trechos prospectivos herdados do PTC foram corrigidos quando descreviam procedimentos já realizados.
- Alegações sem artefatos reproduzíveis sobre protótipo, experimentos, validação escolar e defesa foram removidas.
- O PRISMA 2020 é apresentado como diretriz de relato.
- O PRISMA-P é apresentado como orientação para protocolos; não se declara conformidade integral porque não houve registro prospectivo.
- O limiar usado na elegibilidade representa relevância temática e não qualidade metodológica.
- O MMAT é reportado por Q1--Q5, sem nota geral, média, ranking ou categoria de qualidade.
- A reutilização do cache é explicada como métrica dependente da execução; os valores conflitantes de 63% e 92% foram removidos por não constituírem uma medida estável e versionada da mesma execução.
- Desempenho observado, proficiência estimada, competência e aprendizagem são tratados como conceitos relacionados, mas distintos.

## Referência institucional e normativa

A normalização deve observar, em conjunto:

1. a página do curso de Ciência da Computação do IFC Campus Videira, que publica modelos LaTeX para PTC, TC tradicional e TC de desenvolvimento;
2. o modelo institucional divulgado pelo Sistema Integrado de Bibliotecas do IFC, cuja página informa que os trabalhos de conclusão devem observar o template institucional conforme a Portaria Normativa nº 6/2022 do CONSEPE;
3. as edições vigentes das normas de apresentação de trabalhos acadêmicos, citações, referências, resumos e sumário disponibilizadas pelos serviços institucionais de normalização.

O repositório contém uma customização LaTeX institucional criada em 2017. Ela foi mantida para evitar uma troca silenciosa que alterasse capa, folha de rosto, paginação e demais elementos institucionais sem uma comparação controlada. O documento agora compila automaticamente e o PDF é disponibilizado como artefato do CI. Antes da entrega definitiva, o resultado renderizado deve ser comparado com o modelo LaTeX de TC aplicável ao enquadramento definido pelo curso e com os elementos institucionais obrigatórios.

Mudanças já aplicadas incluem palavras-chave separadas por ponto e vírgula, fontes autorais com ano, remoção de referência obsoleta à NBR 14724:2011 no arquivo principal, correção de espaçamento entre legenda e fonte e registro explícito da limitação do template legado.

## Contrato de validação

Pull requests que alteram o TCC devem:

1. verificar erros de whitespace no diff contra a `main`;
2. compilar os fontes Python;
3. executar os testes do MMAT;
4. executar os testes específicos dos pontos do retorno do orientador;
5. compilar o documento LaTeX em modo de interrupção no primeiro erro;
6. publicar o PDF e o log de compilação como artefatos;
7. registrar a inspeção visual das páginas afetadas.

Os testes do retorno do orientador verificam, entre outros pontos:

- ausência de comandos LaTeX de ênfase duplicados;
- ausência das taxas conflitantes de cache no texto do TCC;
- diferenciação entre PRISMA-P e PRISMA 2020;
- explicação de TF-IDF e similaridade do cosseno;
- análise textual antes da tabela longa da seção de síntese;
- formatação quebrável de `RandomForestClassifier`;
- ausência de alegações de etapas ainda não realizadas;
- distinção entre aprendizagem, competência, proficiência e desempenho;
- MMAT sem agregação numérica e com origem dos julgamentos registrada;
- padronização das fontes elaboradas pelo autor.

## Etapa posterior

Depois da consolidação desta revisão, a pesquisa deverá comparar fontes de dados candidatas, definir o problema computacional, estabelecer modelos de referência, selecionar a arquitetura mínima e implementar um protótipo reproduzível. Nenhuma tecnologia ou modelo será considerado escolhido apenas por ter aparecido com maior frequência na literatura.
