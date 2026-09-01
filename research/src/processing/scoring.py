"""Módulo para cálculo de relevância e scoring de artigos."""

from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

# Termos técnicos para identificação (baseado no notebook)
ML_TERMS = r"(machine learning|deep learning|data mining|neural network|svm|random forest|bayes|lstm|artificial intelligence|AI|predictive|classification|clustering)"
LA_TERMS = r"(learning analytics|educational data mining|intelligent tutor|adaptive learning|personalized learning|student modeling|competenc|skill|assessment)"
EDU_MATH = r"(mathematics|matemática|algebra|geometry|geometria|calculus|cálculo|fractions?|fraç(ões|ao)|arithmetic|trigonometry)"

# Tipos de estudo
STUDY_TYPES = {
    "experimental": r"(experiment(al)?|randomized controlled trial|RCT|controlled study)",
    "quasi-experimental": r"(quasi-experiment(al)?|pre-post|comparison group)",
    "case study": r"(case stud(y|ies)|pilot study)",
    "user study": r"(user stud(y|ies)|usability test|user experience)",
    "survey": r"(survey|questionnaire|interview)",
    "review": r"(review|meta-analysis|systematic review|literature review)",
    "proposal": r"(proposal|position paper|framework|architecture|design)"
}

# Métodos de avaliação
EVAL_METHODS = {
    "statistical": r"(statistical analysis|t-test|anova|chi-square|regression|correlation|significance)",
    "performance": r"(accuracy|precision|recall|f1-score|auc|rmse|mae|error rate)",
    "qualitative": r"(qualitative|interview|observation|content analysis|thematic analysis)",
    "user_feedback": r"(user feedback|satisfaction|likert|rating|evaluation)"
}


def normalize_text(text: Optional[str]) -> str:
    """Normalize text to plain ascii lowercase (utility shared by filters).

    Kept lightweight to avoid pulling heavy dependencies; used by
    compatibility shim and by selection heuristics when needed.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    import unicodedata
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    return text


def is_relevant_paper(paper: Dict, year_min: int, langs: List[str],
                      keywords: List[str], tech_terms: List[str]) -> Tuple[bool, str]:
    """Lightweight pre-filter for candidate papers.

    This mirrors the previous `filtering_patterns.is_relevant_paper` logic but
    lives in the canonical `processing.scoring` module so callers import
    from a single, authoritative place.
    """
    # Year
    try:
        year_val = int(paper.get('year') or 0)
    except Exception:
        year_val = 0
    if year_val < int(year_min):
        return False, f"Ano < {year_min}"

    # Title or abstract empty
    if not paper.get('title') and not paper.get('abstract'):
        return False, "Título e Resumo vazios"

    text_to_check = (str(paper.get('title', '')) + " " + str(paper.get('abstract', ''))).lower()

    # Language heuristic (simple)
    if text_to_check and langs:
        lang_detected = False
        if any(w in text_to_check for w in ['the', 'a', 'is', 'in', 'of', 'and']):
            if 'en' in langs:
                lang_detected = True
        if any(w in text_to_check for w in ['o', 'a', 'é', 'em', 'de', 'e']):
            if 'pt' in langs:
                lang_detected = True

    # Keywords preference or EDU_MATH regex fallback
    if keywords:
        if not any(k.lower() in text_to_check for k in keywords):
            return False, "Sem palavra-chave de educacao"
    else:
        if not re.search(EDU_MATH, text_to_check, re.IGNORECASE):
            return False, "Sem foco educacional detectado"

    return True, ""


def extract_techniques(text: str) -> List[str]:
    """Extract computational techniques from text.

    Args:
        text: Text to analyze (title + abstract)

    Returns:
        List of identified techniques
    """
    if not text:
        return []

    text_lower = text.lower()
    techniques = []

    # Check ML techniques
    if re.search(ML_TERMS, text_lower, re.IGNORECASE):
        techniques.append("machine_learning")

    # Check Learning Analytics
    if re.search(LA_TERMS, text_lower, re.IGNORECASE):
        techniques.append("learning_analytics")

    # Check for specific algorithms
    specific_algos = {
        "neural_network": r"(neural network|deep learning|cnn|rnn|lstm|transformer)",
        "tree_based": r"(decision tree|random forest|xgboost|gradient boost)",
        "statistical": r"(regression|bayes|markov|statistical model)",
        "clustering": r"(cluster|k-means|hierarchical|dbscan)",
    }

    for name, pattern in specific_algos.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            techniques.append(name)

    return list(set(techniques))


def identify_study_type(text: str) -> Optional[str]:
    """Identify the type of study from text.

    Args:
        text: Text to analyze

    Returns:
        Study type or None
    """
    if not text:
        return None

    text_lower = text.lower()

    for study_type, pattern in STUDY_TYPES.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            return study_type

    return None


def identify_eval_methods(text: str) -> List[str]:
    """Identify evaluation methods from text.

    Args:
        text: Text to analyze

    Returns:
        List of evaluation methods
    """
    if not text:
        return []

    text_lower = text.lower()
    methods = []

    for method_type, pattern in EVAL_METHODS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            methods.append(method_type)

    return list(set(methods))


def calculate_relevance_score(paper: Dict, config: Optional[Dict] = None) -> float:
    """Calculate relevance score for a paper.

    Args:
        paper: Paper data as dictionary
        config: Scoring configuration

    Returns:
        Relevance score (0-10)
    """
    if not paper:
        return 0.0

    # Default configuration
    default_config = {
        "weights": {
            "domain_relevance": 0.3,
            "technical_relevance": 0.3,
            "methodology": 0.2,
            "recency": 0.1,
            "quality": 0.1
        },
        "min_year": 2015,
        "max_year": 2025
    }

    config = config or default_config
    weights = config["weights"]

    score = 0.0

    # Combine title and abstract for analysis
    title = paper.get("title", "")
    abstract = paper.get("abstract", "")
    text = f"{title} {abstract}".strip()

    if not text:
        return 0.0

    # 1. Domain relevance (mathematics education)
    domain_score = 0.0
    if re.search(EDU_MATH, text, re.IGNORECASE):
        domain_score = 3.0
        # Bonus for specific math topics
        math_topics = ["algebra", "geometry",
                       "calculus", "fractions", "arithmetic"]
        for topic in math_topics:
            if re.search(topic, text, re.IGNORECASE):
                domain_score += 0.5

    score += domain_score * weights["domain_relevance"]

    # 2. Technical relevance (computational techniques)
    tech_score = 0.0
    techniques = extract_techniques(text)

    if "machine_learning" in techniques:
        tech_score += 2.0
    if "learning_analytics" in techniques:
        tech_score += 2.0
    if "neural_network" in techniques:
        tech_score += 1.0
    if "tree_based" in techniques:
        tech_score += 1.0

    # Bonus for multiple techniques
    tech_score += min(len(techniques) * 0.5, 2.0)

    score += tech_score * weights["technical_relevance"]

    # 3. Methodology quality
    methodology_score = 0.0
    study_type = identify_study_type(text)
    eval_methods = identify_eval_methods(text)

    # Study type scoring
    study_type_scores = {
        "experimental": 3.0,
        "quasi-experimental": 2.5,
        "case study": 2.0,
        "user study": 2.0,
        "survey": 1.5,
        "review": 1.0,
        "proposal": 0.5
    }

    if study_type:
        methodology_score += study_type_scores.get(study_type, 1.0)

    # Evaluation methods scoring
    methodology_score += len(eval_methods) * 0.5

    score += methodology_score * weights["methodology"]

    # 4. Recency
    recency_score = 0.0
    year = paper.get("year")

    if year:
        if year >= 2023:
            recency_score = 3.0
        elif year >= 2020:
            recency_score = 2.0
        elif year >= 2018:
            recency_score = 1.0
        elif year >= 2015:
            recency_score = 0.5

    score += recency_score * weights["recency"]

    # 5. Quality indicators
    quality_score = 0.0

    # Abstract length
    if abstract:
        quality_score += min(len(abstract) / 100, 2.0)

    # DOI availability
    if paper.get("doi"):
        quality_score += 1.0

    # Venue quality (simplified)
    venue = paper.get("venue", "") or ""
    venue = venue.lower()
    if any(keyword in venue for keyword in ["journal", "conference", "proceedings"]):
        quality_score += 1.0

    score += quality_score * weights["quality"]

    # Normalize to 0-10 scale
    score = min(max(score, 0.0), 10.0)

    return round(score, 2)


def compute_relevance_scores(
    df: pd.DataFrame,
    config: Optional[Dict] = None
) -> pd.DataFrame:
    """Compute relevance scores for all papers in DataFrame.

    Args:
        df: DataFrame with papers
        config: Scoring configuration

    Returns:
        DataFrame with added relevance_score column
    """
    if df.empty:
        return df

    logger.info(f"Computing relevance scores for {len(df)} papers")

    # Calculate scores
    scores = []
    techniques_list = []
    study_types = []
    eval_methods_list = []

    # ✅ CORREÇÃO: Importar DatabaseManager para persistir análises
    from ..database.manager import DatabaseManager
    db_manager = DatabaseManager()

    for _, row in df.iterrows():
        paper_dict = row.to_dict()

        # Calculate score
        score = calculate_relevance_score(paper_dict, config)
        scores.append(score)

        # Extract additional metadata
        text = f"{paper_dict.get('title', '')} {paper_dict.get('abstract', '')}"
        techniques = extract_techniques(text)
        study_type = identify_study_type(text)
        eval_methods = identify_eval_methods(text)

        techniques_list.append("; ".join(techniques) if techniques else None)
        study_types.append(study_type)
        eval_methods_list.append(
            "; ".join(eval_methods) if eval_methods else None)
        
        # ✅ CORREÇÃO: Não persistir análises aqui ainda (papers não existem)
        # As análises serão salvas após os papers serem inseridos no banco
        # try:
        #     # Preparar dados da análise
        #     analysis_results = {
        #         'relevance_score': float(score),
        #         'comp_techniques': techniques,
        #         'study_type': study_type,
        #         'eval_methods': eval_methods
        #     }
        #     
        #     # Salvar na tabela analysis (usando hash como paper_id temporário)
        #     paper_id = hash(f"{paper_dict.get('title', '')}{paper_dict.get('doi', '')}") % 1000000
        #     db_manager.save_analysis(
        #         paper_id=paper_id,
        #         analysis_type='relevance_scoring',
        #         results=analysis_results,
        #         confidence=score/10.0  # Normalizar para 0-1
        #     )
        # except Exception as e:
        #     logger.warning(f"Failed to save analysis: {e}")

    # Add columns to DataFrame
    result = df.copy()
    # Preserve attrs (e.g., dedup_stats) so downstream modules can access them
    try:
        result.attrs = getattr(df, 'attrs', {}).copy() if getattr(df, 'attrs', None) else {}
    except Exception:
        pass
    result["relevance_score"] = scores
    result["comp_techniques"] = techniques_list
    result["study_type"] = study_types
    result["eval_methods"] = eval_methods_list

    # Sort by relevance score
    result = result.sort_values("relevance_score", ascending=False)

    # Log statistics
    logger.info(f"Relevance scores: min={min(scores):.2f}, max={max(scores):.2f}, "
                f"mean={sum(scores)/len(scores):.2f}")

    high_relevance = sum(1 for s in scores if s >= 7.0)
    medium_relevance = sum(1 for s in scores if 4.0 <= s < 7.0)
    low_relevance = sum(1 for s in scores if s < 4.0)

    logger.info(f"Distribution: High({high_relevance}), Medium({medium_relevance}), "
                f"Low({low_relevance})")

    return result


def filter_by_relevance(
    df: pd.DataFrame,
    min_score: float = 4.0,
    top_n: Optional[int] = None
) -> pd.DataFrame:
    """Filter papers by relevance score.

    Args:
        df: DataFrame with papers and relevance scores
        min_score: Minimum relevance score
        top_n: Keep only top N papers

    Returns:
        Filtered DataFrame
    """
    if df.empty:
        return df

    if "relevance_score" not in df.columns:
        logger.warning(
            "No relevance_score column found, computing scores first")
        df = compute_relevance_scores(df)

    # Filter by minimum score
    filtered = df[df["relevance_score"] >= min_score].copy()

    # Keep only top N if specified
    if top_n and len(filtered) > top_n:
        filtered = filtered.nlargest(top_n, "relevance_score")

    logger.info(f"Filtered from {len(df)} to {len(filtered)} papers "
                f"(min_score={min_score}, top_n={top_n})")

    return filtered


class RelevanceScorer:
    """Classe para cálculo de scores de relevância de artigos."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize relevance scorer.

        Args:
            config: Scoring configuration
        """
        self.config = config or {
            "weights": {
                "domain_relevance": 0.3,
                "technical_relevance": 0.3,
                "methodology": 0.2,
                "recency": 0.1,
                "quality": 0.1
            },
            "min_year": 2015,
            "max_year": 2025
        }

    def calculate_score(self, paper: Dict) -> float:
        """Calculate relevance score for a paper.

        Args:
            paper: Paper data as dictionary

        Returns:
            Relevance score (0-10)
        """
        return calculate_relevance_score(paper, self.config)

    def extract_techniques(self, text: str) -> List[str]:
        """Extract computational techniques from text.

        Args:
            text: Text to analyze

        Returns:
            List of identified techniques
        """
        return extract_techniques(text)

    def identify_study_type(self, text: str) -> Optional[str]:
        """Identify the type of study from text.

        Args:
            text: Text to analyze

        Returns:
            Study type or None
        """
        return identify_study_type(text)

    def identify_eval_methods(self, text: str) -> List[str]:
        """Identify evaluation methods from text.

        Args:
            text: Text to analyze

        Returns:
            List of evaluation methods
        """
        return identify_eval_methods(text)
