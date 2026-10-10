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
        blocks = re.findall(r"\\begin\{(?:grafico|figure|fluxograma)\}.*?\\end\{(?:grafico|figure|fluxograma)\}", review, re.S)
        self.assertEqual(len(blocks), 2)
        self.assertIn(r"\begin{fluxograma}[H]", review)
        self.assertIn(r"\caption{Fluxo de seleção da revisão sistemática.}", review)
        self.assertNotIn(r"\label{fig:selection-funnel}", review)
        for block in blocks:
            self.assertLess(block.index(r"\caption"), block.index(r"\includegraphics"))

    def test_limitations_are_tied_to_consulted_studies_and_bounded(self):
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        gaps = review.split(r"\section{Tendências e Lacunas}", 1)[1].split(
            r"\section{Limitações e Contribuições da Revisão}", 1
        )[0]
        for citation in (
            r"\citeonline[pp.~1, 16, 31--35]{He2025_6915}",
            r"\citeonline[pp.~14, 22]{Villegas2025_6916}",
            r"\citeonline[pp.~101--105]{Enhancing2025_012}",
            r"\citeonline[pp.~66, 69--70]{Echeveria2025_6920}",
        ):
            self.assertIn(citation, gaps)
        self.assertIn("doze registros tiveram o texto primário consultado", gaps)
        self.assertIn("cinco foram apreciados com base em resumo e metadados", gaps)
        self.assertIn("não permite estimar a frequência", gaps)
        self.assertNotIn("aparecem menos desenvolvidas", gaps)

        slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
        gap_slide = slides.split('<div class="slide-kicker">19 / EVIDÊNCIAS E LIMITES</div>', 1)[1].split(
            'class: content-slide tcc-specification-slide', 1
        )[0]
        for author, locator in (
            ("He et al. (2025)", "pp. 1, 16, 31–35"),
            ("Villegas-Ch et al. (2025)", "pp. 14, 22"),
            ("Nyantah et al. (2025)", "pp. 101–105"),
            ("Echeveria et al. (2025)", "pp. 66, 69–70"),
        ):
            self.assertIn(author, gap_slide)
            self.assertIn(locator, gap_slide)
        self.assertIn("12 de 17 textos primários", gap_slide)
        self.assertIn("não estimativa de prevalência", gap_slide)

    def test_defense_deck_and_parallel_pptx_are_distinguished(self):
        slidev_readme = (ROOT / "presentation/README.md").read_text(encoding="utf-8")
        pptx_readme = (TCC / "presentation/README.md").read_text(encoding="utf-8")
        storyboard = (TCC / "presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md").read_text(encoding="utf-8")
        speaker_notes = (TCC / "presentation/ROTEIRO_FALAS_TCC.md").read_text(encoding="utf-8")
        normalized_pptx_readme = re.sub(r"\s+", " ", pptx_readme.lower())
        self.assertIn("deck canônico da defesa", slidev_readme.lower())
        self.assertIn("25 slides", slidev_readme)
        self.assertIn("export editável paralelo", pptx_readme.lower())
        self.assertIn("19 slides", pptx_readme)
        self.assertIn("não é o arquivo da defesa", normalized_pptx_readme)
        self.assertEqual(len(re.findall(r"^### \d+\.", storyboard, re.M)), 25)
        self.assertEqual(len(re.findall(r"^## \d+\.", speaker_notes, re.M)), 19)

    def test_public_evidence_note_states_scope_without_private_workflow(self):
        note_path = ROOT / "docs/TCC_REPRODUCIBILITY_NOTE.md"
        note = note_path.read_text(encoding="utf-8")
        self.assertIn("12 dos 17", note)
        self.assertIn("SUPPORTED", note)
        self.assertIn("adjudicação humana", note.lower())
        self.assertIn("as oito afirmações têm adjudicação humana", note)
        self.assertNotIn("feedback/private", note)
        self.assertNotIn("compile_tcc.py", note)
        self.assertFalse((ROOT / "docs/TCC_FEEDBACK_WORKFLOW.md").exists())

    def test_public_status_and_defense_artifacts_are_currently_distinguished(self):
        status = (ROOT / "docs/tcc/ESTADO-ATUAL-TCC.md").read_text(encoding="utf-8")
        self.assertIn("10 de outubro de 2026", status)
        self.assertIn("Doze textos primários", status)
        self.assertIn("Slidev em 25 slides", status)
        self.assertIn("19 slides", status)
        self.assertIn("exportação paralela", status)
        self.assertNotIn("Colab CLI", status)
        self.assertNotIn("MCP", status)

    def test_prototype_specification_uses_fewer_cohesive_sections(self):
        specification = (TCC / "conteudo/prototipo.tex").read_text(encoding="utf-8")
        headings = re.findall(r"^\\section\{([^}]+)\}", specification, re.M)
        self.assertEqual(
            headings,
            [
                "Princípios e Requisitos",
                "Dados, Modelagem e Avaliação",
                "Arquitetura de Referência",
            ],
        )
        self.assertNotIn(r"\begin{itemize}", specification)
        self.assertNotIn(r"\begin{enumerate}", specification)
        self.assertIn("No plano funcional", specification)
        self.assertIn("No plano não funcional", specification)

    def test_discussion_bounds_gap_claims_and_avoids_prose_bold(self):
        discussion = (TCC / "conteudo/resultados.tex").read_text(encoding="utf-8")
        self.assertNotIn("lacunas mais recorrentes", discussion.lower())
        self.assertNotIn(r"\textbf{OE", discussion)
        self.assertIn(r"\ref{sec:tendencias-lacunas}", discussion)
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        gaps = review.split(r"\section{Tendências e Lacunas}", 1)[1].split(
            r"\section{Limitações e Contribuições da Revisão}", 1
        )[0]
        self.assertIn("não permite estimar a frequência", gaps)

    def test_abstract_reports_operational_selection_and_limits_gap_claims(self):
        abstract = (TCC / "pretextuais/resumo.tex").read_text(encoding="utf-8")
        self.assertIn("2.486 para a priorização operacional", abstract)
        self.assertIn("12 tiveram textos primários consultados", abstract)
        self.assertIn("a cobertura não permite estimar a frequência", abstract)
        self.assertNotIn("2.486 para a elegibilidade", abstract)
        self.assertNotIn("lacunas relacionadas à explicabilidade", abstract)

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

    def test_public_status_distinguishes_prioritization_from_eligibility(self):
        status = (ROOT / "docs/tcc/ESTADO-ATUAL-TCC.md").read_text(encoding="utf-8")
        normalized = " ".join(status.split())
        self.assertIn("2.486 submetidos à priorização operacional", normalized)
        self.assertIn("nessa etapa, 2.468 foram excluídos", normalized)
        self.assertNotIn("2.486 submetidos à elegibilidade", normalized)

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
        table = (ROOT / "research/exports/references/mmat_current_tcc_table.tex").read_text(encoding="utf-8")
        mmat = review.split(r"\section{Avaliação Metodológica com o MMAT}", 1)[1]
        self.assertIn(r"\fontsize{10}{11.5}", mmat)
        self.assertIn(r"\setlength{\tabcolsep}{2pt}", generator)
        self.assertIn(r"\setlength{\LTcapwidth}{\textwidth}", generator)
        self.assertIn(r"\multicolumn{10}{r}{\textit{Continua na próxima página}}", generator)
        for width in ("3.0", "2.5", "3.6"):
            self.assertIn("p{" + width + "cm}", generator)
        self.assertNotIn(r"\resizebox", generator)
        self.assertIn(r"\Needspace{18\baselineskip}", review)
        self.assertIn(r"\textbf{S1}", table)
        self.assertIn(r"\textbf{S2}", table)
        self.assertNotIn(r"\textbf{Estado}", table)
        self.assertIn("julgamentos empíricos são preliminares e aguardam adjudicação", table)
        self.assertIn(r"\renewcommand{\arraystretch}{1.0}", mmat)

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
