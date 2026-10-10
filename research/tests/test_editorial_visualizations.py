"""Check rendered chart structure and counts, independently of PNG hashes."""

from unittest.mock import patch

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.patches import Wedge

from src.analysis.visualizations import ReviewVisualizer


def test_coverage_is_one_chart_with_counts_and_snapshot_scope(tmp_path):
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
        assert any("n=5" in text.get_text() for text in figure.texts)
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
        assert any("n=2" in text.get_text() for text in figure.texts)
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
