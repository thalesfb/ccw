"""Check rendered chart structure and counts, independently of PNG hashes."""

from unittest.mock import patch
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.patches import Wedge

from src.analysis.visualizations import ReviewVisualizer


def test_coverage_is_one_chart_with_counts_and_proper_source_names(tmp_path):
    frame = pd.DataFrame({"database": ["crossref"] * 3 + ["openalex"] * 2})
    visualizer = ReviewVisualizer(tmp_path)
    with patch.object(plt, "close"):
        output = visualizer.database_coverage(frame)
        figure = plt.gcf()
        assert output.is_file()
        assert len(figure.axes) == 1
        axes = figure.axes[0]
        assert all(isinstance(slice_, Wedge) for slice_ in axes.patches)
        assert len(axes.patches) == 2
        assert round(sum(slice_.theta2 - slice_.theta1 for slice_ in axes.patches)) == 360
        assert axes.get_title() == ""
        labels = [text.get_text() for text in axes.texts]
        assert any("3 (60,0%)" in label for label in labels)
        assert any("2 (40,0%)" in label for label in labels)
        assert any("Crossref" in label for label in labels)
        assert any("OpenAlex" in label for label in labels)
        assert not figure.texts
    plt.close(figure)


def test_coverage_pie_includes_missing_sources_in_its_denominator(tmp_path):
    visualizer = ReviewVisualizer(tmp_path)
    frame = pd.DataFrame({"database": ["crossref", None, None]})
    with patch.object(plt, "close"):
        visualizer.database_coverage(frame)
        figure = plt.gcf()
        labels = [text.get_text() for text in figure.axes[0].texts]
        assert any("Sem fonte registrada" in label for label in labels)
        assert any("2 (66,7%)" in label for label in labels)
        assert any("1 (33,3%)" in label for label in labels)
    plt.close(figure)


@pytest.mark.parametrize("frame", [pd.DataFrame({"database": [None, None]}),
                                   pd.DataFrame({"title": ["A", "B"]})])
def test_coverage_without_provenance_still_accounts_for_every_record(tmp_path, frame):
    visualizer = ReviewVisualizer(tmp_path)
    with patch.object(plt, "close"):
        output = visualizer.database_coverage(frame)
        assert output.is_file()
        figure = plt.gcf()
        labels = [text.get_text() for text in figure.axes[0].texts]
        assert labels == ["Sem fonte registrada\n2 (100,0%)"]
        assert not figure.texts
    plt.close(figure)


def test_prisma_missing_audit_is_not_reported_as_zero_duplicates(tmp_path):
    visualizer = ReviewVisualizer(tmp_path)
    stats = {"identification": 11904, "duplicates_removed": 27, "screening": 11877,
             "eligibility": 2486, "included": 18}
    with patch.object(plt, "close"):
        visualizer.prisma_flow_diagram(stats)
        figure = plt.gcf()
        labels = " ".join(text.get_text() for text in figure.axes[0].texts)
        assert "(n = 27)" in labels
        assert "Detalhamento DOI/URL indisponível" in labels
        assert "0 excedentes DOI + 0 excedentes URL" not in labels
    plt.close(figure)


def test_prisma_labels_remain_readable_at_a_16_cm_print_width(tmp_path):
    """Catch tiny labels after reducing a slide-sized chart into the manuscript."""
    visualizer = ReviewVisualizer(tmp_path)
    stats = {"identification": 11904, "duplicates_removed": 27, "screening": 11877,
             "eligibility": 2486, "included": 18}
    with patch.object(plt, "close"):
        visualizer.prisma_flow_diagram(stats)
        figure = plt.gcf()
        figure.canvas.draw()
        axes = figure.axes[0]
        nodes = [text for text in axes.texts if "(n = " in text.get_text()]
        assert len(nodes) == 7
        scale = 16 / (figure.get_figwidth() * 2.54)
        assert min(node.get_fontsize() * scale for node in nodes) >= 10
        renderer = figure.canvas.get_renderer()
        for node in nodes:
            label_box = node.get_window_extent(renderer)
            matching_boxes = [rectangle.get_window_extent(renderer)
                              for rectangle in axes.patches
                              if rectangle.get_window_extent(renderer).contains(
                                  *axes.transData.transform(node.get_position()))]
            assert len(matching_boxes) == 1
            box = matching_boxes[0]
            assert box.x0 <= label_box.x0 <= label_box.x1 <= box.x1
            assert box.y0 <= label_box.y0 <= label_box.y1 <= box.y1
        labels = " ".join(text.get_text() for text in axes.texts)
        assert "não equivale à elegibilidade" in labels
        assert "elegibilidade no fluxo" not in labels
    plt.close(figure)


def test_prisma_full_text_exclusion_label_does_not_group_two_records_as_one(tmp_path):
    visualizer = ReviewVisualizer(tmp_path)
    stats = {
        "identification": 11904,
        "duplicates_removed": 27,
        "screening": 11877,
        "screening_excluded": 9391,
        "prioritization": 2486,
        "prioritization_excluded": 2468,
        "shortlisted": 18,
        "abstract_screening_excluded": 1,
        "reports_sought": 17,
        "reports_not_retrieved": 1,
        "eligibility": 16,
        "eligibility_excluded": 1,
        "included": 15,
    }
    with patch.object(plt, "close"):
        visualizer.prisma_flow_diagram(stats)
        labels = " ".join(text.get_text() for text in plt.gcf().axes[0].texts)

    assert "Protocolo sem resultados concluídos" in labels
    assert "estudo contextual e protocolo" not in labels


def test_current_prisma_figure_uses_summary_and_separates_duplicate_sources(tmp_path):
    summary_path = Path(__file__).resolve().parents[1] / "exports" / "reports" / "summary.json"
    prisma = json.loads(summary_path.read_text(encoding="utf-8"))["statistics"]["prisma"]

    visualizer = ReviewVisualizer(tmp_path)
    with patch.object(plt, "close"):
        visualizer.prisma_flow_diagram(prisma)
        labels = " ".join(text.get_text() for text in plt.gcf().axes[0].texts)

    assert "29 duplicatas removidas" in labels
    assert "27 DOI/URL" in labels
    assert "2 relatórios iguais (manual)" in labels
    assert "n = 11.875" in labels
    assert "n = 9.393" in labels
    assert "n = 2.482" in labels
    assert "n = 2.464" in labels
    plt.close("all")


def test_flow_and_funnel_do_not_duplicate_external_captions(tmp_path):
    visualizer = ReviewVisualizer(tmp_path)
    stats = {"identification": 100, "duplicates_removed": 10, "screening": 90,
             "eligibility": 20, "included": 3}
    with patch.object(plt, "close"):
        visualizer.prisma_flow_diagram(stats)
        figure = plt.gcf()
        text = " ".join(item.get_text() for item in figure.axes[0].texts)
        assert "Fluxo PRISMA da Revisão Sistemática" not in text
        assert "população adjudicada" not in text
        assert "corpus provisório" in text
    plt.close(figure)
    with patch.object(plt, "close"):
        visualizer.selection_stages_funnel(pd.DataFrame({"selection_stage": ["included"]}), stats=stats)
        figure = plt.gcf()
        assert figure.axes[0].get_title() == ""
        assert figure.axes[0].get_xlabel() == "Número de registros"
        assert [bar.get_width() for bar in figure.axes[0].patches] == [100, 90, 20, 3]
        stage_labels = [label.get_text() for label in figure.axes[0].get_yticklabels()]
        assert "Priorização operacional\n(n=20)" in stage_labels
        assert all("Elegibilidade" not in label for label in stage_labels)
    plt.close(figure)


def test_full_text_flow_does_not_certify_study_independence_or_threshold_only_exclusions(tmp_path):
    """Scope decisions share the operational stage; retained rows are provisional."""
    stats = {
        "identification": 100, "duplicates_removed": 3, "screening": 97,
        "screening_excluded": 70, "prioritization": 27,
        "prioritization_excluded": 9, "shortlisted": 18,
        "abstract_screening_excluded": 1, "reports_sought": 17,
        "reports_not_retrieved": 1, "eligibility": 16,
        "eligibility_excluded": 1, "included": 15,
    }
    with patch.object(plt, "close"):
        ReviewVisualizer(tmp_path).prisma_flow_diagram(stats)
        figure = plt.gcf()
        labels = [item.get_text() for item in figure.axes[0].texts]
        assert "Seleção histórica\n(n = 15)" in labels
        assert "Não avançaram na priorização histórica\n(n = 9)" in labels
    plt.close(figure)


def test_current_funnel_rendered_values_match_the_versioned_summary(tmp_path):
    summary = json.loads((Path(__file__).resolve().parents[1] / 'exports/reports/summary.json').read_text(encoding='utf-8'))
    stats = summary['statistics']['prisma']
    expected = [stats[key] for key in ('identification', 'screening', 'prioritization', 'shortlisted', 'included')]
    with patch.object(plt, 'close'):
        ReviewVisualizer(tmp_path).selection_stages_funnel(pd.DataFrame({'selection_stage': ['included']}), stats=stats)
        figure = plt.gcf()
        assert [bar.get_width() for bar in figure.axes[0].patches] == expected
        labels = [label.get_text() for label in figure.axes[0].get_yticklabels()]
        assert labels == [f'{name}\n(n={value:,})'.replace(',', '.') for name, value in zip(
            ('Identificação', 'Após deduplicação', 'Priorização histórica', 'Lista preliminar', 'Seleção histórica'), expected)]
    plt.close(figure)


def test_current_prisma_is_legible_and_does_not_mislabel_source_denominators(tmp_path):
    summary = json.loads((Path(__file__).resolve().parents[1] / 'exports/reports/summary.json').read_text(encoding='utf-8'))
    with patch.object(plt, 'close'):
        ReviewVisualizer(tmp_path).prisma_flow_diagram(summary['statistics']['prisma'], source_counts=summary['statistics']['databases'])
        figure = plt.gcf()
        figure.canvas.draw()
        nodes = [text for text in figure.axes[0].texts if text.get_text()]
        labels = ' '.join(node.get_text() for node in nodes)
        for prefix, key in (
            ('Registros identificados', 'identification'),
            ('29 duplicatas removidas', 'screening'),
            ('Priorização histórica', 'prioritization'),
            ('Lista preliminar', 'shortlisted'),
            ('Relatórios procurados', 'reports_sought'),
            ('Relatórios avaliados', 'eligibility'),
            ('Seleção histórica', 'included'),
        ):
            node = next(n for n in nodes if n.get_text().startswith(prefix))
            match = re.search(r'\(n = ([\d.]+)\)', node.get_text())
            assert int(match.group(1).replace('.', '')) == summary['statistics']['prisma'][key]
        assert '11.904' in labels and '11.875' in labels and '2.482' in labels
        assert 'após deduplicação' in labels
        for name in ('Crossref', 'OpenAlex', 'Semantic Scholar', 'CORE'):
            assert name in labels
        assert 'A priorização é heurística' not in labels
        assert min(node.get_fontsize() * 16 / (figure.get_figwidth() * 2.54) for node in nodes) >= 8
        renderer = figure.canvas.get_renderer()
        for node in nodes:
            extent = node.get_window_extent(renderer)
            boxes = [p.get_window_extent(renderer) for p in figure.axes[0].patches
                     if p.get_window_extent(renderer).contains(*figure.axes[0].transData.transform(node.get_position()))]
            assert len(boxes) == 1
            assert boxes[0].contains(extent.x0, extent.y0) and boxes[0].contains(extent.x1, extent.y1)
    plt.close(figure)


def test_generate_all_keeps_records_without_source_in_the_flow(tmp_path):
    stats = dict(identification=3, duplicates_removed=1, screening=2,
                 screening_excluded=0, prioritization=2, prioritization_excluded=1,
                 shortlisted=1, abstract_screening_excluded=0, reports_sought=1,
                 reports_not_retrieved=0, eligibility=1, eligibility_excluded=0, included=1)
    frame = pd.DataFrame({'database': ['crossref', None], 'selection_stage': ['included', 'screening']})
    visualizer = ReviewVisualizer(tmp_path)
    with patch.object(visualizer, 'papers_by_year', return_value=tmp_path/'years.png'), \
         patch.object(visualizer, 'techniques_distribution', return_value=tmp_path/'techniques.png'), \
         patch.object(visualizer, 'relevance_score_distribution', return_value=tmp_path/'relevance.png'):
        output = visualizer.generate_all_visualizations(frame, stats)
    assert len(output) == 6
    assert (tmp_path/'prisma_flow.png').is_file()
