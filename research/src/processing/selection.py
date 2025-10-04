"""Módulo para aplicação de critérios de seleção PRISMA."""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd

from ..config import AppConfig, load_config

logger = logging.getLogger(__name__)


class PRISMASelector:
    """Applies PRISMA selection criteria to papers."""
    
    def __init__(self, config: Optional[AppConfig] = None):
        """Initialize selector with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config or load_config()
        self.stats = {
            "identification": 0,
            "duplicates_removed": 0,
            "screening": 0,
            "screening_excluded": 0,
            "eligibility": 0,
            "eligibility_excluded": 0,
            "included": 0
        }
    
    def apply_inclusion_criteria(self, paper: Dict) -> Tuple[bool, List[str]]:
        """Check if paper meets inclusion criteria.
        
        Args:
            paper: Paper data as dictionary
            
        Returns:
            Tuple of (meets_criteria, list_of_met_criteria)
        """
        met_criteria = []
        
        # 1. Year criteria
        year = paper.get("year")
        if year:
            try:
                year_int = int(year)
                if self.config.review.year_min <= year_int <= self.config.review.year_max:
                    met_criteria.append("year_range")
            except (ValueError, TypeError):
                pass
        
        # 2. Language criteria (if abstract exists)
        abstract = paper.get("abstract", "")
        if abstract:
            # Simple language detection (can be improved with langdetect)
            languages = self.config.review.languages
            if any(lang in ["en", "english"] for lang in languages):
                # Check for English patterns
                if re.search(r'\b(the|and|of|in|to|for|with|is|are)\b', abstract.lower()):
                    met_criteria.append("language_en")
            
            if any(lang in ["pt", "portuguese", "português"] for lang in languages):
                # Check for Portuguese patterns
                if re.search(r'\b(de|da|do|para|com|em|que|não)\b', abstract.lower()):
                    met_criteria.append("language_pt")
        
        # 3. Mathematics focus
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        if re.search(r"(mathematics|matemática|math\b|algebra|geometry|calculus)", text, re.IGNORECASE):
            met_criteria.append("math_focus")
        
        # 4. Computational techniques
        if re.search(r"(machine learning|artificial intelligence|AI|data mining|analytics|tutor|adaptive|personalized)", 
                    text, re.IGNORECASE):
            met_criteria.append("computational_techniques")
        
        # 5. Abstract requirement
        if not self.config.review.abstract_required or abstract:
            met_criteria.append("has_abstract")
        
        # Paper must meet minimum criteria
        required = ["year_range", "math_focus", "computational_techniques"]
        meets_all = all(crit in met_criteria for crit in required)
        
        return meets_all, met_criteria
    
    def apply_exclusion_criteria(self, paper: Dict) -> Tuple[bool, Optional[str]]:
        """Check if paper should be excluded.
        
        Args:
            paper: Paper data as dictionary
            
        Returns:
            Tuple of (should_exclude, exclusion_reason)
        """
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        
        # 1. Check for insufficient methodology description
        if paper.get("abstract"):
            abstract_lower = paper["abstract"].lower()
            
            # Very short abstract (likely incomplete)
            if len(abstract_lower.split()) < 50:
                return True, "abstract_too_short"
            
            # No methodology indicators
            methodology_terms = r"(method|approach|experiment|study|analysis|evaluation|test|assess)"
            if not re.search(methodology_terms, abstract_lower):
                # Check if it's not a review/survey
                if not re.search(r"(review|survey|meta-analysis)", abstract_lower):
                    return True, "no_methodology"
        
        # 2. Check for off-topic content
        off_topic_terms = r"(biology|chemistry|physics(?! education)|medicine|health|medical)"
        if re.search(off_topic_terms, text, re.IGNORECASE):
            # Check if it's not in educational context
            if not re.search(r"(education|learning|teaching|student)", text, re.IGNORECASE):
                return True, "off_topic"
        
        # 3. Check for non-research content
        non_research = r"(editorial|erratum|correction|retraction|comment|reply|letter to)"
        if re.search(non_research, text, re.IGNORECASE):
            return True, "non_research"
        
        # 4. Duplicate detection (should be handled separately)
        # This is a placeholder - actual duplicate detection is in dedup.py
        
        return False, None
    
    def screening_phase(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply screening phase (title and abstract).
        
        Args:
            df: DataFrame with papers
            
        Returns:
            DataFrame with screening results
        """
        if df.empty:
            return df
        
        logger.info(f"Starting screening phase with {len(df)} papers")
        
        result = df.copy()
        selection_stages: list[str] = []
        exclusion_reasons: list[Optional[str]] = []
        inclusion_criteria: list[Optional[str]] = []
        statuses: list[str] = []

        for _, row in result.iterrows():
            paper = row.to_dict()

            # Check exclusion criteria first
            should_exclude, reason = self.apply_exclusion_criteria(paper)

            if should_exclude:
                # Mantém 'screening' e marca status como excluído
                selection_stages.append("screening")
                exclusion_reasons.append(reason)
                inclusion_criteria.append(None)
                statuses.append("excluded")
                self.stats["screening_excluded"] += 1
            else:
                # Check inclusion criteria
                meets_criteria, met = self.apply_inclusion_criteria(paper)

                selection_stages.append("screening")
                if meets_criteria:
                    exclusion_reasons.append(None)
                    inclusion_criteria.append("; ".join(met))
                    statuses.append("reviewed")
                    self.stats["screening"] += 1
                else:
                    exclusion_reasons.append("inclusion_criteria_not_met")
                    inclusion_criteria.append("; ".join(met) if met else None)
                    statuses.append("excluded")
                    self.stats["screening_excluded"] += 1

        result["selection_stage"] = selection_stages
        result["exclusion_reason"] = exclusion_reasons
        result["inclusion_criteria_met"] = inclusion_criteria
        result["status"] = statuses
        
        logger.info(f"Screening complete: {self.stats['screening']} passed, "
                   f"{self.stats['screening_excluded']} excluded")
        
        return result
    
    def eligibility_phase(
        self,
        df: pd.DataFrame,
        min_relevance_score: float = 4.0
    ) -> pd.DataFrame:
        """Apply eligibility phase (full-text review).
        
        Args:
            df: DataFrame with papers from screening phase
            min_relevance_score: Minimum relevance score required
            
        Returns:
            DataFrame with eligibility results
        """
        # Filter only papers that passed screening
        eligible_df = df[df["selection_stage"] == "screening"].copy()
        
        if eligible_df.empty:
            logger.warning("No papers passed screening phase")
            return df
        
        logger.info(f"Starting eligibility phase with {len(eligible_df)} papers")
        
        # Apply relevance score threshold
        if "relevance_score" in eligible_df.columns:
            high_relevance = eligible_df["relevance_score"] >= min_relevance_score

            # Update selection stage (sempre 'eligibility') e status conforme limiar
            df.loc[eligible_df.index, "selection_stage"] = "eligibility"
            df.loc[eligible_df[high_relevance].index, "status"] = "reviewed"
            df.loc[eligible_df[~high_relevance].index, "status"] = "excluded"
            df.loc[eligible_df[~high_relevance].index, "exclusion_reason"] = "low_relevance_score"

            self.stats["eligibility"] = int(high_relevance.sum())
            self.stats["eligibility_excluded"] = int((~high_relevance).sum())
        else:
            # If no relevance score, all screening papers go to eligibility
            df.loc[eligible_df.index, "selection_stage"] = "eligibility"
            df.loc[eligible_df.index, "status"] = "reviewed"
            self.stats["eligibility"] = len(eligible_df)
        
        logger.info(f"Eligibility complete: {self.stats['eligibility']} passed, "
                   f"{self.stats['eligibility_excluded']} excluded")
        
        return df
    
    def inclusion_phase(
        self,
        df: pd.DataFrame,
        max_papers: Optional[int] = None
    ) -> pd.DataFrame:
        """Apply final inclusion phase.
        
        Args:
            df: DataFrame with papers from eligibility phase
            max_papers: Maximum number of papers to include
            
        Returns:
            DataFrame with final inclusion results
        """
        # Filter only papers that passed eligibility (status not excluded)
        elig = df["selection_stage"] == "eligibility"
        status_series = df.get("status", pd.Series(["reviewed"] * len(df), index=df.index)).fillna("reviewed")
        not_excluded = status_series != "excluded"
        includable_df = df[elig & not_excluded].copy()
        
        if includable_df.empty:
            logger.warning("No papers passed eligibility phase")
            return df
        
        logger.info(f"Starting inclusion phase with {len(includable_df)} papers")
        
        # Sort by relevance score if available
        if "relevance_score" in includable_df.columns:
            includable_df = includable_df.sort_values("relevance_score", ascending=False)
        
        # Apply maximum limit if specified
        if max_papers and len(includable_df) > max_papers:
            included_indices = includable_df.head(max_papers).index
            excluded_indices = includable_df.tail(len(includable_df) - max_papers).index
            
            df.loc[included_indices, "selection_stage"] = "included"
            df.loc[included_indices, "status"] = "included"
            df.loc[excluded_indices, "selection_stage"] = "eligibility"
            df.loc[excluded_indices, "status"] = "excluded"
            df.loc[excluded_indices, "exclusion_reason"] = "max_papers_exceeded"
            
            self.stats["included"] = len(included_indices)
        else:
            df.loc[includable_df.index, "selection_stage"] = "included"
            df.loc[includable_df.index, "status"] = "included"
            self.stats["included"] = len(includable_df)
        
        logger.info(f"Inclusion complete: {self.stats['included']} papers included")
        
        return df
    
    def apply_full_selection(
        self,
        df: pd.DataFrame,
        min_relevance_score: float = 4.0,
        max_papers: Optional[int] = None
    ) -> pd.DataFrame:
        """Apply full PRISMA selection process.
        
        Args:
            df: DataFrame with all papers
            min_relevance_score: Minimum relevance score
            max_papers: Maximum papers to include
            
        Returns:
            DataFrame with selection results
        """
        if df.empty:
            return df
        
        self.stats["identification"] = len(df)
        logger.info(f"Starting PRISMA selection with {len(df)} papers")
        
        # Phase 1: Screening
        result = self.screening_phase(df)
        
        # Phase 2: Eligibility
        result = self.eligibility_phase(result, min_relevance_score)
        
        # Phase 3: Inclusion
        result = self.inclusion_phase(result, max_papers)
        
        # Log final statistics
        self.print_prisma_flow()
        
        return result
    
    def print_prisma_flow(self):
        """Print PRISMA flow diagram statistics."""
        print("\n" + "="*60)
        print("PRISMA FLOW DIAGRAM")
        print("="*60)
        print(f"📚 Identification: {self.stats['identification']} papers")
        print(f"   └─ Sem duplicatas: {self.stats['identification'] - self.stats['duplicates_removed']}")
        print(f"\n🔍 Screening: {self.stats['screening'] + self.stats['screening_excluded']} papers")
        print(f"   ├─ Included: {self.stats['screening']}")
        print(f"   └─ Excluded: {self.stats['screening_excluded']}")
        print(f"\n📖 Eligibility: {self.stats['eligibility'] + self.stats['eligibility_excluded']} papers")
        print(f"   ├─ Included: {self.stats['eligibility']}")
        print(f"   └─ Excluded: {self.stats['eligibility_excluded']}")
        print(f"\n✅ Final Inclusion: {self.stats['included']} papers")
        print("="*60 + "\n")
    
    def get_statistics(self) -> Dict:
        """Get selection statistics.
        
        Returns:
            Dictionary with statistics
        """
        return self.stats.copy()


def apply_prisma_selection(
    df: pd.DataFrame,
    config: Optional[AppConfig] = None,
    min_relevance_score: float = 4.0,
    max_papers: Optional[int] = None
) -> pd.DataFrame:
    """Apply PRISMA selection criteria to papers.
    
    Args:
        df: DataFrame with papers
        config: Application configuration
        min_relevance_score: Minimum relevance score
        max_papers: Maximum papers to include
        
    Returns:
        DataFrame with selection results
    """
    selector = PRISMASelector(config)
    return selector.apply_full_selection(df, min_relevance_score, max_papers)
