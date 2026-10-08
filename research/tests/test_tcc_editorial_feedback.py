"""Deterministic editorial regressions, not certification of scientific claims."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TCC = ROOT / "results/tcc"


class EditorialFeedbackTests(unittest.TestCase):
    def test_eligibility_is_continuous_prose_without_losing_document_types(self):
        method = (TCC / "conteudo/metodologia.tex").read_text(encoding="utf-8")
        criteria = method.split(r"\section{Critérios de Seleção}", 1)[1].split(
            r"\section{Processo de Seleção}", 1
        )[0]
        self.assertNotIn(r"\subsection", criteria)
        for phrase in ("teses de doutorado", "dissertações de mestrado", "literatura cinzenta",
                       "editoriais", "comentários", "erratas", "relatórios internos",
                       "2015 a 2026", "31 de agosto de 2026", "inglês", "português"):
            self.assertIn(phrase, criteria)
        self.assertNotIn(r"\begin{enumerate}", criteria)

    def test_illustration_captions_precede_images(self):
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        blocks = re.findall(r"\\begin\{(?:grafico|figure)\}.*?\\end\{(?:grafico|figure)\}", review, re.S)
        self.assertEqual(len(blocks), 3)
        for block in blocks:
            self.assertLess(block.index(r"\caption"), block.index(r"\includegraphics"))

    def test_technical_term_is_defined_without_unclear_translation(self):
        theory = (TCC / "conteudo/fundamentacao.tex").read_text(encoding="utf-8")
        self.assertNotIn("andaimento", theory)
        self.assertIn("suporte temporário", theory)
        self.assertIn("WoodBrunerRoss1976", theory)

    def test_research_question_follows_colon_in_same_paragraph(self):
        intro = (TCC / "conteudo/introducao.tex").read_text(encoding="utf-8")
        self.assertRegex(intro, r"problema de pesquisa: como [^\n]+\?")

    def test_architecture_uses_prose_without_bold_stage_labels(self):
        prototype = (TCC / "conteudo/prototipo.tex").read_text(encoding="utf-8")
        for term in ("Ingestão", "preparação", "modelagem", "avaliação e explicabilidade", "apresentação"):
            self.assertNotIn(r"\textbf{" + term + "}", prototype)

    def test_legacy_longtable_caption_type_has_explicit_compatibility(self):
        config = (TCC / "config_inicial.tex").read_text(encoding="utf-8")
        self.assertIn(r"\usepackage{ltcaption}", config)

    def test_search_layers_and_picos_are_quadros_not_lists(self):
        method = (TCC / "conteudo/metodologia.tex").read_text(encoding="utf-8")
        search = method.split(r"\section{Estratégia de Busca}", 1)[1].split(
            r"\section{Processo de Seleção}", 1
        )[0]
        self.assertIn(r"\label{qua:camadas-busca}", search)
        self.assertIn(r"\label{qua:picos}", search)
        self.assertNotIn(r"\begin{itemize}", search)
        self.assertNotIn(r"\begin{enumerate}", search)
        self.assertIn("CochraneChapter3", search)

    def test_technical_section_connects_targets_and_explains_terms(self):
        theory = (TCC / "conteudo/fundamentacao.tex").read_text(encoding="utf-8")
        technical = theory.split(r"\section{Técnicas Computacionais na Educação}", 1)[1].split(
            r"\section{Avaliação Automatizada e Métricas}", 1
        )[0]
        self.assertNotIn(r"\subsection", technical)
        for phrase in ("alvo e da unidade de análise", "classe majoritária",
                       "proporção de classificações corretas", "não são sinônimos",
                       "James2021"):
            self.assertIn(phrase, technical)

    def test_coverage_caption_names_post_deduplication_universe(self):
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn("Registros do snapshot após deduplicação", review)
        self.assertNotIn("Registros identificados por fonte científica", review)
        self.assertIn(r"\section{Limitações e Contribuições da Revisão}", review)
        self.assertNotIn(r"\section{Contribuições para a Especificação do Protótipo}", review)

    def test_bncc_short_call_preserves_institutional_responsibility(self):
        bib = (TCC / "referencias.bib").read_text(encoding="utf-8")
        bncc = bib.split("@misc{BNCC2018,", 1)[1].split("\n}", 1)[0]
        self.assertIn("author = {{Brasil}}", bncc)
        self.assertIn("organization = {Ministério da Educação}", bncc)

    def test_captions_follow_the_mandatory_institutional_template(self):
        config = (TCC / "config_inicial.tex").read_text(encoding="utf-8")
        self.assertIn(r"\captionstyle{\centering}", config)

    def test_mmat_preserves_readable_type_in_a_portrait_width_table(self):
        generator = (ROOT / "research/src/analysis/mmat_current_tcc_table.py").read_text(encoding="utf-8")
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        mmat = review.split(r"\section{Avaliação Metodológica com o MMAT}", 1)[1]
        self.assertIn(r"\fontsize{10}{11.5}", mmat)
        self.assertIn(r"\setlength{\tabcolsep}{2pt}", generator)
        self.assertIn(r"\setlength{\LTcapwidth}{\textwidth}", generator)
        for width in ("3.0", "1.9", "2.3", "2.8"):
            self.assertIn("p{" + width + "cm}", generator)
        self.assertNotIn(r"\resizebox", generator)

    def test_reader_facing_technical_terms_have_context_not_only_acronyms(self):
        intro = (TCC / "conteudo/introducao.tex").read_text(encoding="utf-8")
        method = (TCC / "conteudo/metodologia.tex").read_text(encoding="utf-8")
        theory = (TCC / "conteudo/fundamentacao.tex").read_text(encoding="utf-8")
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn("sequência automatizada de etapas", intro)
        self.assertIn("versão congelada dos registros", method)
        for phrase in ("média harmônica", "falsos positivos", "concordância", "calibração"):
            self.assertIn(phrase, theory)
        for phrase in ("regras de classificação", "redes neurais multicamadas",
                       "modelos probabilísticos", "comparação de modelos",
                       "aprendizagem cooperativa"):
            self.assertIn(phrase, theory + review)


if __name__ == "__main__":
    unittest.main()
