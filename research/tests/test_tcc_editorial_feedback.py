"""Deterministic editorial regressions, not certification of scientific claims."""

import csv
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
            r"\citeonline[pp.~2, 14, 22]{Villegas2025_6916}",
            r"\citeonline[pp.~101--105]{Enhancing2025_012}",
            r"\citeonline[pp.~65, 69--70]{Echeveria2025_6920}",
        ):
            self.assertIn(citation, gaps)
        self.assertIn("15 registros mantidos provisoriamente no núcleo empírico, sem pressupor leitura humana integral", gaps)
        self.assertIn("Um registro aguarda recuperação do texto", gaps)
        self.assertIn("não permite estimar a frequência", gaps)
        self.assertNotIn("aparecem menos desenvolvidas", gaps)

        slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
        gap_slide = slides.split('<div class="slide-kicker">19 / EVIDÊNCIAS E LIMITES</div>', 1)[1].split(
            'class: content-slide tcc-specification-slide', 1
        )[0]
        for author, locator in (
            ("He et al. (2025)", "pp. 1, 16, 31–35"),
            ("Villegas-Ch et al. (2025)", "pp. 2, 14, 22"),
            ("Nyantah et al. (2025)", "pp. 101–105"),
            ("Echeveria et al. (2025)", "pp. 65, 69–70"),
        ):
            self.assertIn(author, gap_slide)
            self.assertIn(locator, gap_slide)
        self.assertIn("15 registros provisórios", gap_slide)
        self.assertIn("ainda sujeitos à conferência humana", gap_slide)
        self.assertIn("não estimativa de prevalência", gap_slide)
        self.assertNotIn("pp. 1, 14, 22", gap_slide)
        manuscript = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn(r"\citeonline[pp.~2, 14, 22]{Villegas2025_6916}", manuscript)
        self.assertNotIn(r"\\citeonline", manuscript)

    def test_temporal_and_sample_frames_are_reported_without_false_reconciliation(self):
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        gaps = review.split(r"\section{Tendências e Lacunas}", 1)[1].split(
            r"\section{Limitações e Contribuições da Revisão}", 1
        )[0]
        self.assertIn("um semestre acadêmico", gaps)
        self.assertIn("período experimental de seis semanas", gaps)
        self.assertIn("subanálise de programação", gaps)
        self.assertIn("oitava semana", gaps)
        self.assertIn("não reconcilia essas janelas temporais", gaps)
        self.assertNotIn("os resultados se estendem até a oitava semana", gaps)
        self.assertIn("2023--2024", gaps)
        self.assertIn("2022--2023", gaps)
        self.assertIn("sem esclarecer se são coortes distintas", gaps)

        audit = (ROOT / "docs/tcc/AUDITORIA-ESTUDOS-SINTESE.md").read_text(encoding="utf-8")
        self.assertIn("semestre", audit)
        self.assertIn("2023--2024 e 2022--2023", audit)
        self.assertIn("Excluído após resumo", audit)
        self.assertIn("A triagem não encontrou resultado explícito de aprendizagem matemática no resumo", audit)
        results = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn("Pendente: texto integral da dissertação não recuperado; MMAT não aplicado.", results)
        self.assertIn("não tratados como verificados no texto integral", results)
        slides = " ".join(
            (ROOT / "presentation/slides.md").read_text(encoding="utf-8").split()
        )
        self.assertIn("material associado aos 15 registros provisórios", slides)
        results = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn("Pendente: texto integral da dissertação não recuperado; MMAT não aplicado.", results)

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
        normalized_note = " ".join(note.split())
        self.assertIn("15 registros permanecem provisoriamente no núcleo empírico", normalized_note)
        self.assertIn("14 têm triagem S1/S2 e 11 têm apreciação dos critérios da categoria", normalized_note)
        self.assertIn("SUPPORTED", normalized_note)
        self.assertIn("adjudicação humana", normalized_note.lower())
        self.assertIn("as nove afirmações têm adjudicação humana", normalized_note)
        self.assertNotIn("feedback/private", normalized_note)
        self.assertNotIn("compile_tcc.py", normalized_note)
        self.assertFalse((ROOT / "docs/TCC_FEEDBACK_WORKFLOW.md").exists())

    def test_public_status_and_defense_artifacts_are_currently_distinguished(self):
        status = (ROOT / "docs/tcc/ESTADO-ATUAL-TCC.md").read_text(encoding="utf-8")
        self.assertIn("15 de outubro de 2026", status)
        self.assertIn("14 têm triagem S1/S2 e 11 têm apreciação dos critérios da categoria", status)
        self.assertIn("Slidev em 25 slides", status)
        self.assertIn("19 slides", status)
        self.assertIn("exportação paralela", status)
        self.assertNotIn("Colab CLI", status)
        self.assertNotIn("MCP", status)
        slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
        pptx_source = (ROOT / "scripts/generate_tcc_presentation.py").read_text(encoding="utf-8")
        self.assertIn("Versão revisada: 15/10/2026", slides)
        self.assertNotIn("Snapshot: 03/09/2026", slides)
        self.assertNotIn("Snapshot adjudicado: 03/09/2026", pptx_source)
        self.assertIn("Versão revisada: 15/10/2026", pptx_source)
        self.assertIn("não recebeu MMAT", pptx_source)
        self.assertNotIn("não receberam MMAT", pptx_source)

    def test_presentation_governance_matches_current_article_access_counts(self):
        registry_path = ROOT / "research/data/mmat_current_study_registry.csv"
        with registry_path.open(encoding="utf-8-sig", newline="") as source:
            records = list(csv.DictReader(source))

        candidates = [
            record for record in records
            if record["empirical_status"] != "empirical_status_not_applicable"
        ]
        primary_text_reviewed = sum(
            record["empirical_status"] == "empirical_confirmed_external"
            for record in candidates
        )
        pending_full_text = sum(
            record["empirical_status"] == "empirical_full_text_pending"
            for record in candidates
        )
        abstract_excluded = sum(
            record["empirical_status"] == "empirical_abstract_only"
            for record in candidates
        )
        self.assertEqual(
            (len(candidates), primary_text_reviewed, pending_full_text, abstract_excluded),
            (17, 15, 1, 1),
        )

        governance = " ".join((ROOT / "docs/tcc/PRESENTATION_GOVERNANCE.md").read_text(encoding="utf-8").split())
        self.assertIn("corpus mantém provisoriamente 15 estudos empíricos", governance)
        self.assertIn("14 têm triagem S1/S2 e 11 têm apreciação dos critérios da categoria", governance)
        self.assertIn("1 aguarda texto integral", governance)
        self.assertIn("um registro foi excluído após resumo", governance)
        self.assertNotIn("cinco foram apreciados", governance)
        self.assertNotIn("nove dos 17 candidatos empíricos", governance)
        note = (ROOT / "docs/TCC_REPRODUCIBILITY_NOTE.md").read_text(encoding="utf-8")
        normalized_note = " ".join(note.split())
        self.assertIn("um texto integral não foi recuperado", normalized_note)
        self.assertIn("Um foi excluído após a triagem do resumo", normalized_note)
        self.assertNotIn("os cinco candidatos restantes foram apreciados", normalized_note)
        slides = " ".join(
            (ROOT / "presentation/slides.md").read_text(encoding="utf-8").split()
        )
        self.assertIn("Texto não recuperado: sem apreciação", slides)
        self.assertIn("exclusão após resumo", slides)
        self.assertNotIn("cinco candidatos foram apreciados por resumo/metadados", slides)
        self.assertNotIn("17 estudos empíricos provisórios", slides)
        self.assertIn("Adjudicar a elegibilidade e a unidade de análise do estudo 8", slides)
        self.assertIn("14 triagens S1/S2 e 11 conjuntos de critérios de categoria", slides)

    def test_study_specific_quantitative_claims_have_primary_source_locators(self):
        results = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn(r"\citeonline[seção~6]{UniversityMathematics2026_6919}", results)
        self.assertIn("não demonstra equivalência", results)
        self.assertIn("Tabela~3, p.~105", results)
        self.assertIn("pré-teste", results)
        self.assertIn("não isolam o efeito", results)

    def test_recovered_article_authors_and_limit_locator_match_primary_texts(self):
        bibliography = (TCC / "referencias.bib").read_text(encoding="utf-8")
        self.assertIn(
            r"author = {Aleksandar Peji{\'c} and Piroska Stani{\'c} Molcer",
            bibliography,
        )
        audit = (ROOT / "docs/tcc/AUDITORIA-ESTUDOS-SINTESE.md").read_text(encoding="utf-8")
        self.assertIn("PDF p. 5; artigo p. 654", audit)
        self.assertIn("classifica estudantes em níveis de proficiência matemática", audit)
        self.assertIn("diferença relativa entre os ganhos médios dos grupos", audit)
        self.assertIn("primeiro ano de Engenharia Industrial, com dados de 2017 a 2021", audit)

    def test_recovered_studies_are_cited_with_precise_units_and_boundaries(self):
        foundation = (TCC / "conteudo/fundamentacao.tex").read_text(encoding="utf-8")
        self.assertIn("classifica estudantes em três categorias operacionais de desempenho", foundation)
        self.assertIn("sem equivalência demonstrada com os níveis oficiais", foundation)
        self.assertIn("50 estudantes do primeiro ano de Engenharia Industrial, observados entre 2017 e 2021", foundation)

        results = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn(r"\citeonline[pp.~50--53]{Math2021_001}", results)
        self.assertIn(r"\citeonline[pp.~4--5]{Machine2024_009}", results)
        self.assertIn(r"\citeonline[pp.~650, 653--654]{Design2025_004}", results)
        self.assertIn("taxa de melhoria do efeito de aprendizagem", results.lower())
        self.assertIn("a taxa é definida pelos autores", results.lower())
        self.assertIn("4.568 passos nos quais os estudantes executaram as próprias ações.", results)
        self.assertIn("A nota 5 esclarece que o subconjunto inclui", results)

        conclusion = (TCC / "conteudo/conclusao.tex").read_text(encoding="utf-8")
        for key in ("Math2021_001", "Machine2024_009", "Design2025_004", "UniversityMathematics2026_6919"):
            self.assertIn(f"\\citeonline{{{key}}}", conclusion)

    def test_prototype_specification_uses_fewer_cohesive_sections(self):
        specification = (TCC / "conteudo/prototipo.tex").read_text(encoding="utf-8")
        headings = re.findall(r"^\\section\{([^}]+)\}", specification, re.M)
        self.assertEqual(
            headings,
            [
                "Princípios e Requisitos",
                "Protocolo de Avaliação da Especificação Conceitual",
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
        self.assertIn("sem comprovar leitura humana integral de todos os textos", discussion)
        self.assertIn("14 receberam respostas S1/S2 e 11 tiveram os critérios específicos da categoria apreciados", discussion)
        self.assertNotIn("parte deles se baseou em resumos e metadados", discussion)
        self.assertNotIn(r"\textbf{OE", discussion)
        self.assertIn(r"\ref{sec:tendencias-lacunas}", discussion)
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        gaps = review.split(r"\section{Tendências e Lacunas}", 1)[1].split(
            r"\section{Limitações e Contribuições da Revisão}", 1
        )[0]
        self.assertIn("não permite estimar a frequência", gaps)

    def test_abstract_reports_operational_selection_and_limits_gap_claims(self):
        abstract = (TCC / "pretextuais/resumo.tex").read_text(encoding="utf-8")
        self.assertIn("2.486 para priorização operacional", abstract)
        self.assertIn("15 registros empíricos mantidos provisoriamente", abstract)
        self.assertIn("14 desses registros receberam respostas S1/S2 e 11 tiveram os critérios da categoria apreciados", abstract)
        self.assertIn("A dissertação não recuperada também não recebeu apreciação MMAT", abstract)
        self.assertIn("sem estimar sua frequência", abstract)
        self.assertNotIn("2.486 para a elegibilidade", abstract)
        self.assertNotIn("lacunas relacionadas à explicabilidade", abstract)

    def test_technical_term_is_defined_without_unclear_translation(self):
        theory = (TCC / "conteudo/fundamentacao.tex").read_text(encoding="utf-8")
        self.assertNotIn("andaimento", theory)
        self.assertIn("apoio pedagógico temporário", theory)
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
        self.assertIn("Registros do recorte versionado após deduplicação", review)
        self.assertNotIn("Registros identificados por fonte científica", review)
        self.assertIn(r"\section{Limitações e Contribuições da Revisão}", review)
        self.assertNotIn(r"\section{Contribuições para a Especificação do Protótipo}", review)

    def test_public_status_distinguishes_prioritization_from_eligibility(self):
        status = (ROOT / "docs/tcc/ESTADO-ATUAL-TCC.md").read_text(encoding="utf-8")
        normalized = " ".join(status.split())
        self.assertIn("2.486 submetidos à priorização operacional", normalized)
        self.assertIn("2.468 não avançaram dessa etapa", normalized)
        self.assertNotIn("2.486 submetidos à elegibilidade", normalized)

    def test_bncc_short_call_preserves_institutional_responsibility(self):
        bib = (TCC / "referencias.bib").read_text(encoding="utf-8")
        bncc = bib.split("@misc{BNCC2018,", 1)[1].split("\n}", 1)[0]
        self.assertIn("author = {{Brasil}}", bncc)
        self.assertIn("organization = {Ministério da Educação}", bncc)

    def test_captions_follow_the_2026_institutional_template(self):
        config = (TCC / "config_inicial.tex").read_text(encoding="utf-8")
        self.assertIn(r"\captionstyle[\raggedright]{}", config)
        self.assertNotIn(r"\captionstyle{\centering}", config)

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
        self.assertNotIn(r"\Needspace{18\baselineskip}", review)
        self.assertNotIn(r"\Needspace{18\baselineskip}", generator)
        self.assertIn(r"\textbf{S1}", table)
        self.assertIn(r"\textbf{S2}", table)
        self.assertNotIn(r"\textbf{Estado}", table)
        self.assertLess(
            table.index(r"\fonte{Elaborado pelo autor (2026).}"),
            table.index(r"\textit{Nota:}"),
        )
        self.assertEqual(table.count(r"\fonte{Elaborado pelo autor (2026).}"), 2)
        self.assertEqual(table.count(r"\textit{Nota:}"), 2)
        self.assertNotIn("Um registro foi excluído após a triagem", table)
        self.assertIn("conferência humana pendente, sem escore agregado", table)
        self.assertIn("Denominador: 14 registros", table)
        note = table.split(r"\textit{Nota:}", 1)[1].splitlines()[0]
        self.assertLessEqual(len(note), 450)
        self.assertIn("O estudo 8 permanece no fluxo e no núcleo sem respostas", review)
        self.assertIn(r"\renewcommand{\arraystretch}{1.0}", mmat)

    def test_he_mmat_interpretation_matches_the_provisional_ledger_design(self):
        with (ROOT / "research/data/mmat_reassessment_current.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            he = next(row for row in csv.DictReader(handle) if row["study_id"] == "6915")
        self.assertEqual(he["design"], "quantitative_nonrandomized")

        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        mmat = review.split(r"\section{Avaliação Metodológica com o MMAT}", 1)[1].split(
            r"\section{Tendências e Lacunas}", 1
        )[0]
        self.assertIn("componente escolar", mmat)
        self.assertIn("quantitativo não randomizado", mmat)
        self.assertIn("controle de confundidores", mmat)
        self.assertIn("administração da intervenção", mmat)
        self.assertIn("adjudicação independente", mmat)
        self.assertIn(r"\citeonline[seção 4.1, pp.~9--11 e Tabela~2]{Innovative2023_005}", mmat)
        self.assertIn(r"p=0{,}583", mmat)
        self.assertIn("18 casos sem desfecho válido", mmat)
        self.assertIn("procedimento de alocação", mmat)
        self.assertIn(r"\citeonline[pp.~44--49, 52--56]{Computational2017_008}", mmat)
        self.assertIn("79 estudantes", mmat)
        self.assertIn("10.052 passos", mmat)
        self.assertIn("unidade de avaliação", mmat)
        self.assertIn("S1, S2 e Q1--Q5 permanecem sem resposta", mmat)
        self.assertNotIn("seguem como CT", mmat)
        self.assertIn("a ausência de apreciação não deve ser interpretada como CT", mmat)
        self.assertIn("sem inferir eficácia", mmat)
        self.assertNotIn("quantitativo descritivo", mmat)
        self.assertNotIn("próprios de outra categoria", mmat)

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
