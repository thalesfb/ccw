"""Deterministic editorial regressions, not certification of scientific claims."""

import csv
from datetime import date
import json
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
        self.assertIn(r"\begin{fluxograma}[htbp]", review)
        self.assertIn(r"\caption{Fluxo de seleção da revisão sistemática.}", review)
        self.assertNotIn(r"\label{fig:selection-funnel}", review)
        for block in blocks:
            self.assertLess(block.index(r"\caption"), block.index(r"\includegraphics"))

    def test_limitations_are_tied_to_consulted_studies_and_bounded(self):
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        limitations = review.split(r"\section{Limitações e Contribuições da Revisão}", 1)[1]
        for citation in (
            r"\citeonline[p.~1, 16, 31--35]{He2025_6915}",
            r"\citeonline[p.~2, 14, 22]{Villegas2025_6916}",
            r"\citeonline[p.~101--105]{Enhancing2025_012}",
            r"\citeonline[p.~65, 69--70]{Echeveria2025_6920}",
        ):
            self.assertIn(citation, limitations)
        self.assertIn("O corpus final reúne 15 estudos empíricos", review)
        self.assertIn("A inclusão no corpus não comprova leitura integral dos textos, figuras e apêndices", limitations)
        self.assertNotIn("núcleo empírico", limitations)
        self.assertIn(r"O texto integral de \citeonline{Zeng2025_6923} não foi recuperado", limitations)
        gaps = review.split(r"\section{Tendências e Lacunas}", 1)[1].split(
            r"\section{Limitações e Contribuições da Revisão}", 1
        )[0]
        self.assertIn("sem estimativa de frequência ou atribuição de ausência a toda a literatura", gaps)
        self.assertNotIn("aparecem menos desenvolvidas", gaps + limitations)

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
        self.assertIn(r"\citeonline[p.~2, 14, 22]{Villegas2025_6916}", manuscript)
        self.assertNotIn(r"\\citeonline", manuscript)

    def test_temporal_and_sample_frames_are_reported_without_false_reconciliation(self):
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        gaps = review.split(r"\section{Limitações e Contribuições da Revisão}", 1)[1]
        self.assertIn("um semestre acadêmico", gaps)
        self.assertIn("período experimental de seis semanas", gaps)
        self.assertIn("subanálise de programação", gaps)
        self.assertIn("oitava semana", gaps)
        self.assertIn("não reconcilia essas janelas temporais", gaps)
        self.assertNotIn("os resultados se estendem até a oitava semana", gaps)
        self.assertIn("2023--2024", gaps)
        self.assertIn("2022--2023", gaps)
        self.assertIn("sem esclarecer se são grupos distintos de estudantes", gaps)

        audit = (ROOT / "docs/tcc/AUDITORIA-ESTUDOS-SINTESE.md").read_text(encoding="utf-8")
        self.assertIn("semestre", audit)
        self.assertIn("2023--2024 e 2022--2023", audit)
        self.assertIn("Excluído após resumo", audit)
        self.assertIn("A triagem não encontrou resultado explícito de aprendizagem matemática no resumo", audit)
        results = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn("Pendente: texto integral da tese não recuperado; MMAT não aplicado.", results)
        self.assertIn("não tratados como verificados no texto integral", results)
        slides = " ".join(
            (ROOT / "presentation/slides.md").read_text(encoding="utf-8").split()
        )
        self.assertIn("material associado aos 15 registros provisórios", slides)
        results = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn("Pendente: texto integral da tese não recuperado; MMAT não aplicado.", results)

    def test_defense_deck_and_parallel_pptx_are_distinguished(self):
        slidev_readme = (ROOT / "presentation/README.md").read_text(encoding="utf-8")
        pptx_readme = (TCC / "presentation/README.md").read_text(encoding="utf-8")
        storyboard = (TCC / "presentation/APRESENTACAO_TCC_SLIDES_CONTEUDO.md").read_text(encoding="utf-8")
        slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
        normalized_pptx_readme = re.sub(r"\s+", " ", pptx_readme.lower())
        self.assertIn("deck canônico da defesa", slidev_readme.lower())
        self.assertIn("25 slides", slidev_readme)
        self.assertIn("export editável paralelo", pptx_readme.lower())
        self.assertIn("19 slides", pptx_readme)
        self.assertIn("não é o arquivo da defesa", normalized_pptx_readme)
        self.assertEqual(len(re.findall(r"^### \d+\.", storyboard, re.M)), 25)
        self.assertEqual(len(re.findall(r"^layout: \w+$", slides, re.M)), 25)

    def test_speech_is_deferred_until_content_approval(self):
        for path in (
            ROOT / "presentation/README.md",
            TCC / "presentation/README.md",
            ROOT / "docs/tcc/PRESENTATION_GOVERNANCE.md",
        ):
            document = " ".join(path.read_text(encoding="utf-8").lower().split())
            self.assertIn("a fala não integra esta revisão semifinal", document)
            self.assertIn("após a revisão dos prs e a validação da orientação", document)

    def test_public_evidence_note_states_scope_without_private_workflow(self):
        note_path = ROOT / "docs/TCC_REPRODUCIBILITY_NOTE.md"
        note = note_path.read_text(encoding="utf-8")
        normalized_note = " ".join(note.split())
        self.assertIn("15 registros permanecem provisoriamente no núcleo empírico", normalized_note)
        self.assertIn("15 têm triagem S1/S2 e apreciação dos critérios", normalized_note)
        self.assertIn("SUPPORTED", normalized_note)
        self.assertIn("adjudicação humana", normalized_note.lower())
        self.assertIn("as nove afirmações têm adjudicação humana", normalized_note)
        self.assertNotIn("feedback/private", normalized_note)
        self.assertNotIn("compile_tcc.py", normalized_note)
        self.assertFalse((ROOT / "docs/TCC_FEEDBACK_WORKFLOW.md").exists())

    def test_public_status_and_defense_artifacts_are_currently_distinguished(self):
        status = (ROOT / "docs/tcc/ESTADO-ATUAL-TCC.md").read_text(encoding="utf-8")
        coverage = json.loads(
            (ROOT / "research/data/study_contribution_current.json").read_text(encoding="utf-8")
        )
        self.assertIn(date.fromisoformat(coverage["review_date"]).strftime("%d/%m/%Y"), status)
        self.assertIn("15 têm triagem S1/S2 e apreciação dos critérios", status)
        self.assertIn("Slidev em 25 slides", status)
        self.assertIn("19 slides", status)
        self.assertIn("exportação paralela", status)
        self.assertNotIn("Colab CLI", status)
        self.assertNotIn("MCP", status)
        slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
        pptx_source = (ROOT / "scripts/generate_tcc_presentation.py").read_text(encoding="utf-8")
        self.assertIn("Versão revisada: 28/10/2026", slides)
        self.assertNotIn("Snapshot: 03/09/2026", slides)
        self.assertNotIn("Snapshot adjudicado: 03/09/2026", pptx_source)
        self.assertIn("Versão revisada: 28/10/2026", pptx_source)
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
            record["empirical_status"] == "empirical_outside_mathematics_scope"
            for record in candidates
        )
        self.assertEqual(
            (len(candidates), primary_text_reviewed, pending_full_text, abstract_excluded),
            (17, 15, 1, 1),
        )

        governance = " ".join((ROOT / "docs/tcc/PRESENTATION_GOVERNANCE.md").read_text(encoding="utf-8").split())
        self.assertIn("núcleo empírico mantém provisoriamente 15 registros", governance)
        self.assertIn("15 têm triagem S1/S2 e apreciação dos critérios", governance)
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
        self.assertIn("Conferir as 15 apreciações preliminares e suas rotas operacionais", slides)
        self.assertIn("15 triagens S1/S2 e 15 conjuntos de critérios", slides)

    def test_study_specific_quantitative_claims_have_primary_source_locators(self):
        results = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn(r"\cite[seção~6]{UniversityMathematics2026_6919}", results)
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
        self.assertIn("classifica estudantes em categorias operacionais de desempenho", audit)
        self.assertNotIn("classifica estudantes em níveis de proficiência matemática", audit)
        self.assertIn("não são uma medida validada de proficiência individual", audit)
        self.assertIn("diferença relativa entre os ganhos médios dos grupos", audit)
        self.assertIn("primeiro ano de Engenharia Industrial, com dados de 2017 a 2021", audit)

    def test_recovered_studies_are_cited_with_precise_units_and_boundaries(self):
        foundation = (TCC / "conteudo/fundamentacao.tex").read_text(encoding="utf-8")
        self.assertIn("classifica estudantes em três categorias operacionais de desempenho", foundation)
        self.assertIn("50 estudantes do primeiro ano de Engenharia Industrial, observados entre 2017 e 2021", foundation)

        results = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        limitations = results.split(r"\section{Limitações e Contribuições da Revisão}", 1)[1]
        self.assertIn("as três categorias operacionais não têm equivalência demonstrada com os níveis oficiais do PISA", limitations)
        self.assertIn(r"\citeonline[p.~50--53]{Math2021_001}", results)
        self.assertIn(r"\citeonline[p.~4--5]{Machine2024_009}", results)
        self.assertIn(r"\citeonline[p.~650, 653--654]{Design2025_004}", results)
        self.assertIn("taxa de melhoria do efeito de aprendizagem", results.lower())
        self.assertIn("a taxa é definida pelos autores", results.lower())
        self.assertIn("4.568 passos nos quais os estudantes executaram as próprias ações.", results)
        self.assertIn("A nota 5 esclarece que o subconjunto inclui", results)

        conclusion = (TCC / "conteudo/conclusao.tex").read_text(encoding="utf-8")
        for purpose in ("predição/classificação (oito estudos)", "personalização ou STI (três)",
                        "intervenção didática (dois)", "modelagem cognitiva (um)", "integração curricular (um)"):
            self.assertIn(purpose, conclusion)

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
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        limitations = review.split(r"\section{Limitações e Contribuições da Revisão}", 1)[1]
        self.assertNotIn("lacunas mais recorrentes", discussion.lower())
        self.assertIn("A inclusão no corpus não comprova leitura integral dos textos, figuras e apêndices", limitations)
        self.assertNotIn("adjudicação", discussion)
        self.assertIn(r"As contagens MMAT do Quadro~\ref{qua:mmat-contagens}", discussion)
        self.assertIn("sem contar os três estudos mistos novamente", discussion)
        self.assertNotIn("parte deles se baseou em resumos e metadados", discussion)
        self.assertNotIn(r"\textbf{OE", discussion)
        self.assertIn(r"\ref{sec:limitacoes-revisao}", discussion)
        gaps = review.split(r"\section{Tendências e Lacunas}", 1)[1].split(
            r"\section{Limitações e Contribuições da Revisão}", 1
        )[0]
        self.assertIn("sem estimativa de frequência ou atribuição de ausência a toda a literatura", gaps)

    def test_abstract_reports_operational_selection_and_limits_gap_claims(self):
        abstract = (TCC / "pretextuais/resumo.tex").read_text(encoding="utf-8")
        self.assertIn("18 foram encaminhados para leitura", abstract)
        self.assertIn("um corpus de 15 estudos empíricos", abstract)
        for removed in ("priorização operacional", "mantidos provisoriamente", "adjudicação", "único pesquisador", "DOI/URL"):
            self.assertNotIn(removed, abstract)
        self.assertIn("por critério, sem escore", abstract)
        self.assertIn("diferenças entre desempenho, previsão, proficiência, competência e aprendizagem", abstract)
        self.assertIn("base documental de apoio à interpretação docente", abstract)
        prototype = (TCC / "conteudo/prototipo.tex").read_text(encoding="utf-8")
        self.assertIn("apoiar a decisão pedagógica sem substituir o professor", prototype)
        self.assertNotIn("2.486 para a elegibilidade", abstract)
        self.assertNotIn("lacunas relacionadas à explicabilidade", abstract)
        # Process details live in the body, not in the abstract.
        for detail in ("S1/S2", "Q1--Q5", "estudo 8", "busca histórica"):
            self.assertNotIn(detail, abstract)
        results = (TCC / "conteudo/resultados.tex").read_text(encoding="utf-8")
        method = (TCC / "conteudo/metodologia.tex").read_text(encoding="utf-8")
        conclusion = (TCC / "conteudo/conclusao.tex").read_text(encoding="utf-8")
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn(r"As contagens MMAT do Quadro~\ref{qua:mmat-contagens}", results)
        self.assertIn(r"A tese de \citeonline{Zeng2025_6923} não foi apreciada por falta do texto integral", review)
        self.assertIn(r"o relatório de \citeonline{Zeng2025_6923} não foi recuperado", conclusion)
        self.assertIn("sem estimativa de frequência", review)
        self.assertIn("tampouco equivale à elegibilidade por texto completo", review)
        self.assertIn(r"\ref{sec:limitacoes-revisao}", method)
        self.assertIn("não permite reconstruir integralmente as consultas históricas", conclusion)

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
        self.assertEqual(re.findall(r"\\subsection\{([^}]+)\}", technical), ["Trabalhos Relacionados"])
        self.assertIn(r"\label{sec:trabalhos-relacionados}", technical)
        for phrase in ("alvo e da unidade de análise", "classe majoritária",
                       "proporção de classificações corretas", "não são sinônimos",
                       "James2021"):
            self.assertIn(phrase, technical)

    def test_coverage_caption_names_post_deduplication_universe(self):
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn("Registros após a remoção de duplicatas, por fonte científica", review)
        self.assertNotIn("recorte versionado", review)
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
        self.assertIn("author = {{BRASIL}}", bncc)
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
        self.assertIn(r"\fontsize{10}{12}", table)
        self.assertIn(r"\setlength{\tabcolsep}{2pt}", generator)
        self.assertIn(r"\setlength{\LTcapwidth}{\textwidth}", generator)
        self.assertIn(r"\multicolumn{9}{r}{\textit{Continua na próxima página}}", generator)
        for width in ("4.5",):
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
        self.assertIn("A conferência humana permanece pendente", review)
        self.assertIn("não foram convertidos em escore agregado ou síntese final de qualidade", review)
        self.assertIn("15 estudos do corpus", table)
        note = table.split(r"\textit{Nota:}", 1)[1].splitlines()[0]
        self.assertLessEqual(len(note), 450)
        self.assertIn(r"A categoria 4 foi adaptada à modelagem computacional da tese de \citeonline{Computational2017_008}", review)
        self.assertIn(r"\SingleSpacing", table)

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
        limitations = review.split(r"\section{Limitações e Contribuições da Revisão}", 1)[1]
        self.assertIn("componente escolar", mmat)
        self.assertIn("quantitativo não randomizado", mmat)
        self.assertIn("controle de confundidores", mmat)
        self.assertIn("administração da intervenção", mmat)
        self.assertNotIn("adjudicação", mmat)
        self.assertIn(r"\citeonline[seção 4.1, p.~9--11 e Tabela~2]{Innovative2023_005}", mmat)
        self.assertIn(r"p=0{,}583", limitations)
        self.assertIn("18 casos sem desfecho válido", limitations)
        self.assertIn("procedimento de alocação", limitations)
        self.assertIn(r"\citeonline[p.~44--49, 52--56]{Computational2017_008}", mmat)
        self.assertIn("79 estudantes", review)
        self.assertIn("10.052 passos", review)
        self.assertIn("unidade de avaliação", mmat)
        self.assertNotIn("S1, S2 e Q1--Q5 ficaram sem resposta", mmat)
        self.assertIn("categoria 4 adaptada", mmat)
        self.assertIn("S1, S2 e Q1 receberam Y", mmat)
        self.assertIn("Q2--Q5 permaneceram CT", mmat)
        self.assertIn("não demonstra eficácia do protótipo", review)
        self.assertNotIn("quantitativo descritivo", mmat)
        self.assertNotIn("próprios de outra categoria", mmat)

    def test_defense_demonstrates_traceability_and_distinguishes_proposal_from_application(self):
        slides = (ROOT / "presentation/slides.md").read_text(encoding="utf-8")
        for phrase in ("R02", "R20", "26 grupos", "rastreabilidade", "consistência arquitetural",
                       "correspondência conceitual", "condições de viabilidade",
                       "11.877 registros após deduplicação", "fonte da versão mantida",
                       "Page et al. (2021)", "Hong et al. (2018)", "National Research Council (2001)"):
            self.assertIn(phrase, slides)
        self.assertNotIn("um futuro protocolo de avaliação", slides)

    def test_reader_facing_technical_terms_have_context_not_only_acronyms(self):
        method = (TCC / "conteudo/metodologia.tex").read_text(encoding="utf-8")
        appendix = (TCC / "postextuais/apendice.tex").read_text(encoding="utf-8")
        theory = (TCC / "conteudo/fundamentacao.tex").read_text(encoding="utf-8")
        review = (TCC / "conteudo/resultadosesperados.tex").read_text(encoding="utf-8")
        self.assertIn("O processo reuniu identificação, deduplicação, triagem, priorização por relevância e verificação de elegibilidade", method)
        self.assertIn("funciona como índice da origem dos dados analisados", appendix)
        self.assertIn("resumos criptográficos", appendix)
        self.assertIn("diferença entre reproduzir o conjunto analisado e iniciar uma nova coleta", appendix)
        for phrase in ("média harmônica", "falsos positivos", "concordância", "calibração"):
            self.assertIn(phrase, theory)
        for phrase in ("regras de classificação", "redes neurais multicamadas",
                       "campos aleatórios condicionais", "comparação de modelos",
                       "aprendizagem cooperativa"):
            self.assertIn(phrase, (theory + review).lower())

    def test_active_acronym_list_is_alphabetical_and_covers_terms_used_in_text(self):
        main = (TCC / "main.tex").read_text(encoding="utf-8")
        glossary = re.search(r"\\begin\{siglas\}(.*?)\\end\{siglas\}", main, re.S)
        self.assertIsNotNone(glossary)
        entries = re.findall(r"\\item\[([^\]]+)\]", glossary.group(1))
        self.assertEqual(entries, sorted(entries, key=str.casefold))

        for acronym in (
            "AIC", "BIC", "CORE", "CRF", "CSV", "CT", "EEG", "F1", "HTML", "JSON", "MLP",
            "PCA", "PDF", "PICO", "PICOS", "RN", "ROC", "ROC-AUC", "SHA-256",
            "TIMSS", "URL", "RIPPER",
        ):
            self.assertIn(fr"\item[{acronym}]", glossary.group(1))

    def test_abstract_reports_the_prisma_flow_without_counting_unretrieved_text_as_excluded(self):
        abstract = (TCC / "pretextuais/resumo.tex").read_text(encoding="utf-8")
        portuguese = abstract.split(r"\begin{resumo}", 1)[1].split(
            r"\end{resumo}", 1
        )[0]
        english = abstract.split(r"\begin{resumo}[Abstract]", 1)[1].split(
            r"\end{otherlanguage*}", 1
        )[0]

        for phrase in (
            "um foi excluído após resumo",
            "17 relatórios procurados",
            "um não foi recuperado",
            "16 foram avaliados",
            "um protocolo sem resultados concluídos foi excluído",
            "15 estudos empíricos",
        ):
            self.assertIn(phrase, " ".join(portuguese.lower().split()))
        self.assertNotIn("excluídos um registro fora do escopo, um texto integral não recuperado",
                         " ".join(portuguese.lower().split()))

        for phrase in (
            "one was excluded after abstract screening",
            "17 reports sought",
            "one was not retrieved",
            "16 were assessed",
            "one protocol without completed results was excluded",
            "15 empirical studies",
        ):
            self.assertIn(phrase, " ".join(english.lower().split()))

    def test_prisma_appendix_keeps_abstract_gaps_and_links_public_materials(self):
        appendix = (TCC / "postextuais/apendice.tex").read_text(encoding="utf-8")
        normalized = " ".join(appendix.split())
        self.assertIn("2 & Resumo & Parcial:", normalized)
        self.assertIn("critérios gerais", normalized)
        self.assertIn("data individual da última consulta", normalized)
        self.assertIn("total agregado de participantes", normalized)
        self.assertIn("financiamento", normalized)
        self.assertIn("pré-registro", normalized)
        self.assertIn("https://github.com/thalesfb/ccw/tree/main/research", normalized)
        self.assertIn("título não identifica o trabalho como revisão sistemática", normalized)

    def test_new_abbreviations_are_expanded_before_first_use(self):
        abstract = (TCC / "pretextuais/resumo.tex").read_text(encoding="utf-8")
        methodology = (TCC / "conteudo/metodologia.tex").read_text(encoding="utf-8")
        appendix = (TCC / "postextuais/apendice.tex").read_text(encoding="utf-8")
        for text in (abstract,):
            self.assertIn(r"Preferred Reporting Items for Systematic Reviews and Meta-Analyses} (PRISMA)", text)
            self.assertIn(r"Mixed Methods Appraisal Tool} (MMAT)", text)
        self.assertIn(r"Secure Hash Algorithm} de 256 bits (SHA-256)", appendix)
        theory = (TCC / "conteudo/fundamentacao.tex").read_text(encoding="utf-8")
        self.assertIn(r"Repeated Incremental Pruning to Produce Error Reduction} (RIPPER)", theory)
        self.assertIn(r"Digital Object Identifier} (DOI", methodology)
        self.assertIn(r"Uniform Resource Locator} (URL", methodology)
        self.assertIn(r"Comma-Separated Values} (CSV", methodology)
        self.assertIn(r"JavaScript Object Notation} (JSON", appendix)
        self.assertIn(r"HyperText Markup Language} (HTML", methodology)
        self.assertIn(r"Can't tell} (CT", (TCC / "conteudo/metodologia.tex").read_text(encoding="utf-8"))
        self.assertIn(r"COnnecting REpositories} (CORE)", abstract)
        main = (TCC / "main.tex").read_text(encoding="utf-8")
        pdf_definition = r"\item[PDF] \textit{Portable Document Format}"
        self.assertIn(pdf_definition, main)
        self.assertLess(main.index(pdf_definition), main.index(r"\include{conteudo/introducao}"))
        self.assertIn("a ausência de avaliação é distinta de ct e não constitui resposta adicional do instrumento", methodology.lower())


if __name__ == "__main__":
    unittest.main()
