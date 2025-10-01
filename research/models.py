"""
Data models for systematic review pipeline.
"""
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Paper:
    """Data class representing a research paper."""
    title: str = ""
    authors: str = ""
    year: int = 0
    source_publication: str = ""
    abstract: str = ""
    full_text: str = ""
    doi_url: str = ""
    database: str = ""
    search_terms: str = ""
    is_open_access: bool = False
    country: str = ""
    study_type: str = ""
    comp_techniques: str = ""
    eval_methods: str = ""
    math_topic: str = ""
    main_results: str = ""
    identified_gaps: str = ""
    relevance_score: int = 0
    selection_stage: str = "Identificação"
    exclusion_reason: str = ""
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert Paper to dictionary."""
        return asdict(self)
