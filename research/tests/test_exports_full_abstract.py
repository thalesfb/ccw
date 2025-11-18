from research.src.analysis.reports import ReportGenerator


def test_exports_preserve_full_abstract(tmp_path):
    """Ensure the papers report rendering preserves the full abstract text
    (no truncation).
    """
    long_abstract = "This is a long abstract. " + ("X" * 2000)

    paper = {
        'title': 'Sample Paper for Abstract Preservation',
        'authors': 'Doe, J.',
        'year': 2021,
        'venue': 'Sample Conf',
        'abstract': long_abstract,
        'relevance_score': 8.5,
        'comp_techniques': 'machine_learning',
        'study_type': 'experimental',
        'inclusion_criteria_met': 'Yes',
    }

    rg = ReportGenerator(output_dir=tmp_path)
    html = rg._create_papers_html([paper], stage='included')

    # The full abstract must be present in the rendered HTML
    assert long_abstract in html
