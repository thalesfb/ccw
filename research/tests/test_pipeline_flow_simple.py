import pandas as pd

from research.src.pipeline.run import SystematicReviewPipeline


def test_pipeline_flow_enrichment_and_selection():
    # Build a small dataset with one education paper and one finance paper
    df = pd.DataFrame([
        {
            'title': 'Adaptive learning system for mathematics',
            'abstract': 'We improved student performance using personalized tasks.',
            'year': 2021,
            'doi': '10.1000/edu1'
        },
        {
            'title': 'Stock market prediction using neural networks',
            'abstract': 'We forecast stock prices using deep learning.',
            'year': 2020,
            'doi': '10.1000/fin1'
        }
    ])

    pipeline = SystematicReviewPipeline()

    # Inject the small dataset as if it were collected
    pipeline.results = df

    # Process data: compute scores and apply enrichment
    processed = pipeline.process_data(deduplicate_data=False, compute_scores=True, save_to_db=False)

    # Sanity checks on processing
    assert 'relevance_score' in processed.columns
    assert 'comp_techniques' in processed.columns

    # Apply selection with a low threshold to allow inspection of selection stage behavior
    selected = pipeline.apply_selection_criteria(min_score=0.0, max_papers=None)

    # After selection, the DataFrame should have a 'selection_stage' column
    assert 'selection_stage' in selected.columns
