"""Check rendered chart structure and counts, independently of PNG hashes."""

from unittest.mock import patch

import matplotlib.pyplot as plt
import pandas as pd

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
        assert sorted(bar.get_width() for bar in axes.patches) == [2, 3]
        assert axes.get_title() == ""
        labels = [text.get_text() for text in axes.texts]
        assert "3 (60,0%)" in labels
        assert "2 (40,0%)" in labels
        assert any("n=5" in text.get_text() for text in figure.texts)
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
    plt.close(figure)
