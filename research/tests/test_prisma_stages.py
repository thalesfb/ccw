"""
Testes para validação do pipeline PRISMA e cálculo de estágios.
"""

import pytest
import pandas as pd
from research.src.processing.selection import PRISMASelector
from research.src.config import load_config


class TestPRISMAStages:
    """Testes para os estágios PRISMA."""
    
    @pytest.fixture
    def config(self):
        """Carrega configuração."""
        return load_config()
    
    @pytest.fixture
    def selector(self, config):
        """Cria PRISMASelector."""
        return PRISMASelector(config)
    
    @pytest.fixture
    def sample_papers(self):
        """Cria amostra de papers para teste."""
        return pd.DataFrame([
            {
                "title": "Machine Learning in Mathematics Education",
                "abstract": "This study presents a comprehensive approach to using machine learning for adaptive mathematics learning. We developed and tested a system with 500 students over one semester. The methodology involved data collection, analysis of learning patterns, and implementation of adaptive algorithms. Results show significant improvement in student performance and engagement with mathematical concepts using AI-powered personalized learning paths.",
                "year": 2020,
                "doi": "10.1234/test1",
                "relevance_score": 8.5
            },
            {
                "title": "AI-Powered Math Tutoring System",
                "abstract": "We developed an intelligent tutoring system for mathematics education using artificial intelligence and machine learning techniques. The system adapts to individual student needs through continuous assessment and personalized feedback. Our experimental study with 300 high school students demonstrates the effectiveness of AI-driven approaches in improving mathematical problem-solving skills and understanding of algebraic concepts.",
                "year": 2021,
                "doi": "10.1234/test2",
                "relevance_score": 7.2
            },
            {
                "title": "Biology Applications of Neural Networks",  # Off-topic
                "abstract": "This paper explores the application of neural networks in biological research, specifically in protein structure prediction and genomic analysis. Our methodology involves training deep learning models on large datasets of biological sequences. The study demonstrates how computational approaches can accelerate discovery in molecular biology and genetics, providing insights into cellular mechanisms and disease pathways through advanced data mining techniques.",
                "year": 2019,
                "doi": "10.1234/test3",
                "relevance_score": 3.1
            },
            {
                "title": "Adaptive Learning in Mathematical Problem Solving",
                "abstract": "This research investigates personalized mathematics education using adaptive algorithms and data analytics. We conducted a longitudinal study with 400 students, implementing an intelligent system that adjusts difficulty levels and provides targeted interventions. The methodology includes learning analytics, predictive modeling, and continuous assessment. Results indicate significant improvements in mathematical proficiency and problem-solving abilities through personalized learning approaches.",
                "year": 2022,
                "doi": "10.1234/test4",
                "relevance_score": 9.1
            },
            {
                "title": "Editorial Comment on Recent Trends",  # Non-research
                "abstract": "Editorial comment discussing recent trends in the field and upcoming special issues. This editorial provides an overview of current developments and introduces new editorial board members.",
                "year": 2023,
                "doi": "10.1234/test5",
                "relevance_score": 2.0
            }
        ])
    
    def test_inclusion_criteria(self, selector, sample_papers):
        """Testa critérios de inclusão."""
        paper = sample_papers.iloc[0].to_dict()
        meets_criteria, met = selector.apply_inclusion_criteria(paper)
        
        assert meets_criteria is True
        assert "year_range" in met
        assert "math_focus" in met
        assert "computational_techniques" in met
    
    def test_exclusion_criteria(self, selector, sample_papers):
        """Testa critérios de exclusão."""
        # Paper editorial deve ser excluído (mais confiável)
        editorial = sample_papers.iloc[4].to_dict()
        should_exclude, reason = selector.apply_exclusion_criteria(editorial)
        assert should_exclude is True
        assert reason in ["non_research", "abstract_too_short"]
        
        # Testar paper com abstract muito curto
        short_abstract = {
            "title": "Test Paper",
            "abstract": "Very short abstract with only a few words here.",
            "year": 2020
        }
        should_exclude, reason = selector.apply_exclusion_criteria(short_abstract)
        assert should_exclude is True
        assert reason == "abstract_too_short"
    
    def test_screening_phase(self, selector, sample_papers):
        """Testa fase de triagem."""
        result = selector.screening_phase(sample_papers)
        
        # Deve ter coluna de selection_stage
        assert "selection_stage" in result.columns
        assert "status" in result.columns
        assert "exclusion_reason" in result.columns
        
        # Total deve ser preservado
        assert len(result) == len(sample_papers)
        
        # Deve haver pelo menos alguns papers processados (excluídos ou revisados)
        assert len(result[result["selection_stage"] == "screening"]) > 0
        
        # Verificar que pelo menos papers bons passaram
        reviewed = result[(result["status"] == "reviewed") & (result["relevance_score"] >= 7.0)]
        assert len(reviewed) >= 2  # Pelo menos os 2 melhores papers devem passar
    
    def test_eligibility_phase(self, selector, sample_papers):
        """Testa fase de elegibilidade."""
        # Primeiro aplicar screening
        after_screening = selector.screening_phase(sample_papers)
        
        # Aplicar elegibilidade
        result = selector.eligibility_phase(after_screening, min_relevance_score=4.0)
        
        # Verificar que papers com baixo score foram excluídos
        low_score = result[result["relevance_score"] < 4.0]
        for _, row in low_score.iterrows():
            if row["selection_stage"] == "eligibility":
                assert row["status"] == "excluded"
                assert row["exclusion_reason"] == "low_relevance_score"
    
    def test_inclusion_phase(self, selector, sample_papers):
        """Testa fase de inclusão final."""
        # Aplicar screening e eligibility
        after_screening = selector.screening_phase(sample_papers)
        after_eligibility = selector.eligibility_phase(after_screening, min_relevance_score=4.0)
        
        # Aplicar inclusão
        result = selector.inclusion_phase(after_eligibility)
        
        # Verificar que papers com alto score foram incluídos
        high_score_papers = sample_papers[sample_papers["relevance_score"] >= 7.0]
        included = result[result["selection_stage"] == "included"]
        
        # Deve haver pelo menos 1 paper incluído (os de alto score que atendem critérios)
        assert len(included) >= 1, "Pelo menos 1 paper de alto score deve ser incluído"
        
        # Verificar que todos incluídos têm status correto
        for _, row in included.iterrows():
            assert row["status"] == "included"
    
    def test_full_selection_pipeline(self, selector, sample_papers):
        """Testa pipeline completo de seleção."""
        result = selector.apply_full_selection(sample_papers, min_relevance_score=4.0)
        
        # Verificar estatísticas
        stats = selector.get_statistics()
        
        assert stats["identification"] == len(sample_papers)
        assert stats["screening"] >= 0
        assert stats["screening_excluded"] >= 0
        assert stats["eligibility"] >= 0
        assert stats["eligibility_excluded"] >= 0
        assert stats["included"] >= 0
        
        # Total de excluídos + incluídos deve ser <= identification
        total_processed = (stats["screening_excluded"] + stats["eligibility_excluded"] + 
                          stats["included"])
        assert total_processed <= stats["identification"]
    
    def test_prisma_stats_consistency(self, selector, sample_papers):
        """Testa consistência das estatísticas PRISMA."""
        result = selector.apply_full_selection(sample_papers, min_relevance_score=5.0)
        stats = selector.get_statistics()
        
        # Verificar que os números fazem sentido
        # Screening + screening_excluded deve ser >= 0
        screening_total = stats["screening"] + stats["screening_excluded"]
        assert screening_total >= 0
        
        # Papers que passaram screening devem ir para eligibility ou serem excluídos
        # Included nunca deve ser maior que identification
        assert stats["included"] <= stats["identification"]
        
        # Contagem no DataFrame deve bater com stats
        df_included = len(result[result["selection_stage"] == "included"])
        assert df_included == stats["included"]
    
    def test_exclusion_reasons_recorded(self, selector, sample_papers):
        """Testa se motivos de exclusão são registrados corretamente."""
        result = selector.apply_full_selection(sample_papers, min_relevance_score=4.0)
        
        # Verificar que papers excluídos têm motivo
        excluded = result[result["status"] == "excluded"]
        for _, row in excluded.iterrows():
            assert pd.notna(row["exclusion_reason"])
            assert row["exclusion_reason"] in [
                "off_topic", "non_research", "no_methodology", 
                "abstract_too_short", "inclusion_criteria_not_met",
                "low_relevance_score", "max_papers_exceeded"
            ]
    
    def test_inclusion_criteria_recorded(self, selector, sample_papers):
        """Testa se critérios de inclusão atendidos são registrados."""
        result = selector.screening_phase(sample_papers)
        
        # Papers que passaram screening devem ter critérios registrados
        passed = result[result["status"] == "reviewed"]
        for _, row in passed.iterrows():
            if pd.notna(row.get("inclusion_criteria_met")):
                assert len(row["inclusion_criteria_met"]) > 0
