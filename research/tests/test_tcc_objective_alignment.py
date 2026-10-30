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
        self.assertEqual(re.findall(r"^O (OE\d+) consiste em ", intro, re.M),
                         ["OE1", "OE2", "OE3", "OE4"])
        self.assertNotRegex(results, r"\\textbf\{OE\d+\}")
        for phrase in ("O OE1 foi desenvolvido", "O OE2 identificou",
                       "O OE3 resultou", "O OE4 resultou"):
            self.assertIn(phrase, results)
        objectives = intro.split(r"\section{Objetivos}", 1)[1].split(
            r"\section{Estrutura do Trabalho}", 1
        )[0]
        self.assertNotIn(r"\subsection", objectives)
        self.assertNotIn(r"\textbf", objectives)
        self.assertNotIn(r"\begin{itemize}", objectives)
        self.assertIn("metodológicas", objectives)
        self.assertIn("viabilidade e a coerência da especificação conceitual", objectives)
        prototype = (CONTENT / "prototipo.tex").read_text(encoding="utf-8")
        self.assertIn("sua aplicação permanece pendente", prototype)
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
        self.assertIn("A aplicação do painel e a avaliação de uma implementação são etapas posteriores", alignment)
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
