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
        self.assertEqual(re.findall(r"\\textbf\{(OE\d+)\}", intro),
                         ["OE1", "OE2", "OE3", "OE4"])
        self.assertNotRegex(results, r"\\textbf\{OE\d+\}")
        for phrase in ("o primeiro objetivo específico foi desenvolvido", "O segundo foi desenvolvido",
                       "O terceiro foi operacionalizado", "O quarto resultou na proposição"):
            self.assertIn(phrase, results)
        objectives = intro.split(r"\subsection{Objetivos Específicos}", 1)[1].split(
            r"\section{Estrutura do Trabalho}", 1
        )[0]
        self.assertNotIn(r"\begin{itemize}", objectives)
        self.assertIn("metodológicas", objectives)
        self.assertIn("viabilidade e a coerência da especificação conceitual", objectives)
        self.assertIn("não equivale à realização da avaliação", objectives)

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

    def test_evaluation_is_proposed_not_claimed_as_completed(self):
        results = (CONTENT / "resultados.tex").read_text(encoding="utf-8")
        alignment = results.split(r"\section{Atendimento aos Objetivos}", 1)[1].split(
            r"\section{Discussão Integrada}", 1
        )[0]
        self.assertIn("proposição", alignment)
        self.assertIn("não", alignment)
        self.assertIn("Sua aplicação não foi realizada", alignment)
        self.assertIn("contingência separada", alignment)
        self.assertIn("não equivalem a uma síntese final do corpus", alignment)

    def test_protocol_covers_the_proposed_pedagogical_review(self):
        source = (CONTENT / "prototipo.tex").read_text(encoding="utf-8")
        self.assertNotIn("especificação validada documentalmente", source)
        protocol = source.split(r"\section{Protocolo de Avaliação da Especificação Conceitual}", 1)[1].split(
            r"\section{Arquitetura de Referência}", 1
        )[0]
        for phrase in ("revisão documental por docentes", "nível de ensino",
                       "evidência documental", "não foi executado",
                       "não substituiria um estudo empírico"):
            self.assertIn(phrase, protocol)


if __name__ == "__main__":
    unittest.main()
