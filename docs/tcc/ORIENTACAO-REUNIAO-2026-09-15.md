# Preparação para a reunião de orientação — versão de 14/09/2026

Este registro congela o estado que deve ser apresentado ao orientador e ao
coorientador. Ele separa o que já existe no repositório, o que foi validado
com testes e o que ainda depende de decisão científica. Nenhuma execução com
dados reais é autorizada por este documento.

## Estado que pode ser apresentado

### Revisão e MMAT

- O snapshot vigente da revisão é de 31/08/2026.
- O fluxo PRISMA atual registra 11.904 identificados, 11.877 após remoções
  determinísticas, 2.486 em elegibilidade e 18 retidos.
- Os 18 retidos estão separados em 17 candidatos empíricos provisórios e um
  protocolo/proposta contextual, mantido em *hold* e sem apreciação empírica.
- O ledger MMAT atual preserva as duas perguntas de triagem, S1 e S2, e os
  critérios Q1–Q5 conforme o delineamento. A legenda operacional é Y (sim), N
  (não) e CT (não é possível concluir com a evidência disponível).
- Nove registros tiveram texto primário revisado externamente; oito ainda
  dependem de recuperação de fonte ou foram apreciados somente por
  resumo/metadados. A leitura foi feita por um único revisor e a adjudicação
  metodológica final permanece pendente.
- Portanto, o MMAT é uma apreciação documental preliminar por critério; não há
  escore agregado, ranking de estudos ou conclusão de eficácia.

### Implementação/protótipo

- O pipeline em `prototype/` já está implementado: ingestão manifestada,
  normalização do ASSISTments, construção de atributos sem vazamento,
  separação temporal e por estudante, modelos candidatos, métricas e
  bootstrap agrupado por estudante.
- A suíte local passa com 44 testes quando executada com as dependências de
  desenvolvimento.
- Isso valida o comportamento do código e os guardrails sintéticos. Ainda não
  houve execução com a fonte real, treinamento em dados reais, avaliação de
  eficácia pedagógica, participação de estudantes ou validação em escola.
- Os limiares mínimos de tamanho da fonte e do conjunto de teste ainda estão
  deliberadamente não congelados. A decisão sobre implementar ou não o
  protótipo deve ocorrer antes da execução real.

## Decisões para a reunião

1. Confirmar se o TCC permanece como revisão sistemática + especificação
   conceitual ou se haverá um estudo computacional exploratório separado.
2. Se houver execução, aprovar fonte, licença/termos de acesso, unidade de
   análise, desfecho `correct_next`, limiares mínimos e protocolo de divisão.
3. Definir se a apresentação deve manter o deck conceitual de 25 slides como
   fonte canônica, mantendo o PPTX histórico de 19 slides apenas como exportação
   não equivalente.
4. Confirmar se a adjudicação do MMAT será feita pelo supervisor/coorientação e
   quais fontes primárias e localizadores precisam ser recuperados primeiro.

## Colab, CLI e governança da execução futura

O serviço lembrado é o **Google Colab**, que oferece notebooks Python no
navegador. A documentação oficial do Google One informa que o Google AI Pro
inclui benefícios do Colab e anuncia 200 unidades de computação (CCUs) para o
plano elegível. A FAQ do Colab ressalta que benefícios, GPUs/TPUs, execução em
segundo plano e limites dependem do plano efetivamente associado à conta.

Antes de qualquer uso, confirmar em Colab → Settings → Subscription qual plano
está ativo. A oferta estudantil pode variar por país, período e conta; não se
deve inferir a disponibilidade somente pelo nome “AI Studio”.

O repositório não assume que um “Colab CLI” ou MCP de terceiros seja uma
interface oficial do benefício consumidor. A rota de menor risco para a reunião
é documentar um notebook reprodutível e decidir depois entre:

- Colab web para a primeira validação e o treinamento exploratório;
- execução automatizada local do mesmo notebook, por exemplo com Jupyter, para
  testes de transformação e CI;
- Colab Enterprise/Vertex AI somente se for aprovado um projeto Google Cloud,
  orçamento, identidade e governança próprios.

Quando a execução for autorizada, o notebook deverá registrar versão da fonte,
data de acesso, hash dos artefatos, configuração, divisão, métricas, avisos e
relatório. Dados brutos restritos não devem ser commitados nem publicados; o
repositório deve receber apenas código, manifesto, dados derivados permitidos e
resultados auditáveis. Métricas preditivas não deverão ser apresentadas como
aprendizagem ou eficácia pedagógica.

Fontes oficiais consultadas:

- [Google One — benefícios do Google AI Pro e Colab](https://support.google.com/googleone/answer/14534406?hl=en)
- [Google Colab — perguntas frequentes e limites dos planos](https://research.google.com/colaboratory/faq.html)
- [Google Colab — runtimes locais](https://research.google.com/colaboratory/local-runtimes.html)
- [Google Cloud — runtimes do Colab Enterprise](https://docs.cloud.google.com/vertex-ai/docs/colab/create-runtime)

## Critério de saída da reunião

Até existir decisão registrada, o estado correto é: **código implementado,
testes sintéticos verdes, experimento real pendente e MMAT preliminar**. A
apresentação deve comunicar exatamente esse limite.
