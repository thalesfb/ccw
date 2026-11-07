"""Guard document alignment; these checks do not certify scientific validity."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "results/tcc/conteudo"


class ObjectiveAlignmentTests(unittest.TestCase):
    def test_intro_and_results_reference_only_four_unique_objectives(self):
        intro = (CONTENT / "introducao.tex").read_text(encoding="utf-8")
        results = (CONTENT / "resultados.tex").read_text(encoding="utf-8")
        objectives = intro.split(r"\section{Objetivos}", 1)[1].split(
            r"\section{Estrutura do Trabalho}", 1
        )[0]
        labels = re.findall(r"^\\item \((OE\d+)\) ", objectives, re.M)
        self.assertEqual(labels, ["OE1", "OE2", "OE3", "OE4"])
        self.assertNotRegex(results, r"\\textbf\{OE\d+\}")
        for phrase in ("O OE1 foi desenvolvido", "O OE2 identificou",
                       "O OE3 resultou", "O OE4 resultou"):
            self.assertIn(phrase, results)
        self.assertIn(r"\begin{alineas}", objectives)
        self.assertIn(r"\end{alineas}", objectives)
        self.assertNotIn(r"\subsection", objectives)
        self.assertNotIn(r"\textbf", objectives)
        self.assertNotIn(r"\begin{itemize}", objectives)
        self.assertNotIn("consiste em", objectives)
        self.assertIn("definiu-se como objetivo geral propor", objectives)
        self.assertIn("Para alcançá-lo, foram definidos os seguintes objetivos específicos", objectives)
        self.assertIn("(OE1) categorizar as abordagens e técnicas computacionais", objectives)
        self.assertIn("(OE2) identificar limitações e lacunas técnicas", objectives)
        self.assertIn("(OE3) formular a especificação técnica e pedagógica", objectives)
        self.assertIn(
            "(OE4) propor um protocolo para avaliar a viabilidade e a coerência da especificação conceitual, "
            "considerando sua fundamentação, a consistência dos requisitos e as condições técnicas e pedagógicas de execução.",
            objectives,
        )
        self.assertIn("metodológicas", objectives)
        prototype = (CONTENT / "prototipo.tex").read_text(encoding="utf-8")
        self.assertIn("sua aplicação permanece pendente", prototype)
        self.assertIn("A regra de decisão e sua justificativa deverão ser definidas antes de eventual comparação", prototype)
        self.assertIn("não define as colunas habilitadas", prototype)
        self.assertIn("a rotina de explicação local decompõe", prototype)
        self.assertIn("até as 20 primeiras linhas do conjunto de teste, ordenadas pelo identificador", prototype)
        self.assertIn("pela ordem da interação e pelo identificador do registro de origem", prototype)
        self.assertIn("não uma amostra aleatória", prototype)
        self.assertNotIn("teste alinhado por execução", prototype)
        self.assertIn("O produto do trabalho é documental", intro)

    def test_piaget_is_not_cited_in_active_manuscript(self):
        source = "\n".join(path.read_text(encoding="utf-8")
                           for path in CONTENT.glob("*.tex"))
        self.assertFalse(re.search(r"\\cite(?:online)?(?:\[[^]]*\])?\{[^}]*Piaget", source),
                         "Piaget must not remain cited in the active manuscript")
        theory = (CONTENT / "fundamentacao.tex").read_text(encoding="utf-8")
        pedagogical = theory.split(r"\section{Contribuições", 1)[1].split(
            r"\section{Tecnologia", 1
        )[0]
        self.assertNotIn(r"\subsection", pedagogical)
        for key in ("Vygotsky1978", "Ausubel1968", "WoodBrunerRoss1976",
                    "BlackWiliam1998", "HattieTimperley2007"):
            self.assertIn(key, pedagogical)

    def test_slidev_and_editable_generator_have_four_objectives(self):
        slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
        objectives = slides.split("06 / OBJETIVOS ESPECÍFICOS", 1)[1].split("\n---", 1)[0]
        self.assertEqual(objectives.count('class="tcc-objective-step"'), 4)
        self.assertIn("<strong>Propor o protocolo</strong>", objectives)
        self.assertNotIn("7 objetivos", slides)
        generator = (ROOT / "scripts/generate_tcc_presentation.py").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'\("(OE\d+)"', generator),
                         ["OE1", "OE2", "OE3", "OE4"])

    def test_evaluation_is_proposed_not_claimed_as_completed(self):
        results = (CONTENT / "resultados.tex").read_text(encoding="utf-8")
        alignment = results.split(r"\section{Atendimento aos Objetivos}", 1)[1].split(
            r"\section{Discussão Integrada}", 1
        )[0]
        self.assertIn("protocolo documental", alignment)
        self.assertIn("A aplicação do painel e a avaliação de uma implementação não foram realizadas neste trabalho", alignment)
        self.assertIn("escopo documental", alignment)
        self.assertIn(r"\ref{sec:limitacoes-revisao}", alignment)

    def test_protocol_covers_the_proposed_pedagogical_review(self):
        source = (CONTENT / "prototipo.tex").read_text(encoding="utf-8")
        self.assertNotIn("especificação validada documentalmente", source)
        protocol = source.split(r"\section{Protocolo de Avaliação da Especificação Conceitual}", 1)[1].split(
            r"\section{Arquitetura de Referência}", 1
        )[0]
        self.assertIn(r"\input{conteudo/protocolo-docente}", protocol)
        teacher_protocol = (CONTENT / "protocolo-docente.tex").read_text(encoding="utf-8")
        for phrase in ("cinco docentes distintos", "educação básica", "ensino superior",
                       "segunda rodada individual", "quatro dos cinco docentes", "coerente",
                       "evidência insuficiente", "Plataforma Brasil", "aguardar a decisão",
                       "sem participantes convidados ou avaliação realizada"):
            self.assertIn(phrase, teacher_protocol)
        self.assertIn("não foi executado", protocol)
        self.assertIn("não substituiria um estudo empírico", protocol)


if __name__ == "__main__":
    unittest.main()
