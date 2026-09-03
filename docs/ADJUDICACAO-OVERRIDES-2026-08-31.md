# Registro de adjudicação dos overrides do snapshot

**Status:** decisão científica pendente; este documento não altera a população
do snapshot, o TCC, o MMAT, a bibliografia ou as figuras.

## Finalidade

O snapshot de 31/08/2026 contém sete registros que foram excluídos
operacionalmente após a triagem, mas cuja decisão ainda precisa ser confirmada
com base no protocolo e em fontes primárias. Este registro separa evidência
observada de decisão do supervisor. A conversa interna, o número do registro e
o score do pipeline não são tratados como evidência científica.

O fluxo numérico versionado permanece:

```text
11.904 identificados - 27 identidades determinísticas = 11.877 na triagem
11.877 - 9.391 excluídos na triagem = 2.486 na elegibilidade
2.486 - 2.470 excluídos na elegibilidade = 16 incluídos operacionalmente
```

Esses números descrevem o snapshot exportado. Eles não constituem, por si
sós, a decisão final de elegibilidade dos sete registros nem resolvem o
conflito temporal do registro 6918.

## Regras que precisam ser aplicadas

Cada decisão deve ser justificada por uma fonte primária ou institucional e
pelas regras versionadas em `research/data/current_eligibility_protocol.csv`:

1. matemática deve ser central para a intervenção, população ou desfecho;
2. a técnica computacional deve ser ativa e avaliada, e não apenas uma forma
   passiva de comunicação;
3. a publicação deve apresentar resultados empíricos analisáveis concluídos;
4. um desfecho STEM composto só pode entrar na síntese matemática quando o
   componente de matemática for separável e analisável;
5. tipo documental, ano, identidade e status da fonte devem ser verificados
   separadamente.

Quando qualquer regra não puder ser verificada, o estado correto é `hold`, e
não uma inclusão ou exclusão silenciosa.

## Matriz de decisão

| Registro | Evidência primária/institucional observada | Questão de protocolo | Estado antes da decisão |
| --- | --- | --- | --- |
| 14 | O artigo descreve ensino de teoremas de círculo com animação computacional, grupos experimental e controle, pré/pós-teste e teste de Mann–Whitney. [Fonte publicadora](https://journals.eduped.org/index.php/IJMME/article/view/1299) | A redação `técnicas computacionais` inclui tecnologia educacional não baseada em ML, como animação computacional? | `hold`: recuperar/arquivar o texto primário e decidir a abrangência da regra computacional. |
| 15 | O artigo relata entrevistas semiestruturadas e vídeos de sala com 12 professores; podcasts e webinars aparecem como possibilidades, não como intervenção computacional avaliada. [PDF publicador](https://pdf.ejmse.com/EJMSE_5_2_93.pdf) | Confirmar exclusão por ausência de intervenção computacional aplicada, separando-a de uma exclusão por score. | `proposed_excluded`: confirmação do supervisor. |
| 6915 | O artigo publicado apresenta modelos preditivos de IA para tecnologia educacional matemática, meta-análise e validação experimental em escola. [Fonte Springer](https://link.springer.com/article/10.1186/s40561-025-00415-z) | Definir se um estudo com meta-análise e experimento de validação é uma unidade elegível da síntese e arquivar o texto primário. | `hold`: forte sinal de inclusão, sem alterar o snapshot. |
| 6918 | O registro operacional informa 2025, mas a fonte institucional da ETH identifica a tese como de 2014. [Auditoria de proveniência](RECONCILIACAO-METADADOS-6918.md) | O ano canônico 2014 viola o recorte 2015–2026; confirmar a decisão temporal e a chave bibliográfica. | `hold`: não usar na síntese até resolver a incompatibilidade. |
| 6919 | O artigo descreve ensino universitário de matemática, desenho comparativo e avaliação com questionários assistidos por IA, rastreamento ocular e EEG; o contexto industrial também é central. [Fonte publicadora](https://www.mdpi.com/2071-1050/18/4/1900) | Verificar no texto completo se o desfecho educacional matemático é central e interpretável para o protocolo. | `hold`: recuperar/arquivar o texto primário. |
| 6922 | O documento institucional descreve o projeto Testbed Math, integração tecnológica e estudos de caso; trata-se de relatório final de projeto. [Repositório institucional](https://oa.tib.eu/renate/bitstreams/e3609f68-18dd-419a-b27c-5dd5234f5214/download) | Confirmar se o protocolo exclui relatório de projeto da síntese empírica e registrar a razão como tipo documental, não como ausência de tecnologia. | `proposed_excluded`: confirmação do supervisor. |
| 6925 | O artigo publicado usa seis modelos de ML sobre PISA 2022; o desfecho é a média de proficiência em matemática e ciências. [Fonte Springer](https://link.springer.com/article/10.1186/s40594-025-00590-y) | A regra atual exige que o resultado matemático seja separável; confirmar se o desfecho STEM composto pode ser usado. | `hold`: decisão sobre especificidade do desfecho. |
| 6926 | O artigo avalia ML para educação moral; matemática, leitura e escrita aparecem como preditores de raciocínio moral. [Registro bibliográfico](https://doi.org/10.1016/j.aej.2025.03.095) | Confirmar exclusão porque matemática não é o domínio educacional nem o desfecho principal. | `proposed_excluded`: confirmação do supervisor. |

## Consequências controladas

Até que a matriz seja resolvida e registrada em artefato versionado:

- o conjunto de 16 permanece apenas operacional;
- não se altera o número relatado no TCC;
- não se altera a síntese empírica, o MMAT ou as conclusões;
- não se regeneram figuras com uma composição diferente;
- não se traduzem nem se reescrevem títulos bibliográficos;
- não se misturam os estados do SQLite com os estados da exportação;
- 6918 permanece fora de qualquer afirmação dependente do recorte temporal;
- 6921 continua contextual e fora da síntese empírica, conforme o escopo
  versionado atual.

Após as decisões, deve-se gerar uma população derivada imutável, atualizar os
artefatos de exportação e somente então sincronizar o TCC, o MMAT, as figuras
e a apresentação. A adjudicação deve preservar a trilha entre regra, fonte,
localizador, decisão e artefato derivado.
