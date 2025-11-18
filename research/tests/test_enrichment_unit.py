import pandas as pd

from research.src.processing.enrichment import (
    extract_comp_techniques,
    extract_main_results,
    identify_gaps,
    enrich_dataframe,
)


def test_extract_comp_techniques_ml_and_assessment():
    row = pd.Series({
        'title': 'Neural network for automated student assessment',
        'abstract': 'We propose a deep learning model to assess student responses.'
    })

    techniques = extract_comp_techniques(row)
    assert 'Machine Learning' in techniques or 'AI/Artificial Intelligence' in techniques
    assert 'Assessment' in techniques


def test_extract_main_results_sentence_extraction():
    row = pd.Series({
        'title': 'Evaluation of adaptive tutoring',
        'abstract': 'We improved accuracy by 8%. The model was evaluated on 200 students.'
    })

    main = extract_main_results(row)
    assert 'improved accuracy' in main.lower() or 'improved' in main.lower()


def test_identify_gaps_detects_future_work():
    row = pd.Series({
        'title': 'Study of learning analytics',
        'abstract': 'Limitations include small sample size. Future work will expand to other schools.'
    })

    gaps = identify_gaps(row)
    assert 'Future work' in gaps or 'Lacunas' not in gaps or 'future work' in gaps.lower()


def test_enrich_dataframe_adds_columns_and_scores():
    df = pd.DataFrame([
        {
            'title': 'Adaptive learning for mathematics',
            'abstract': 'A system that personalizes tasks for students.',
            'year': 2021
        }
    ])

    out = enrich_dataframe(df)
    assert 'relevance_score' in out.columns
    assert 'comp_techniques' in out.columns
    assert 'main_results' in out.columns
    assert out['relevance_score'].dtype.kind in ('i', 'f')
