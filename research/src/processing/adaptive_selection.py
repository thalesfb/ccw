"""
Seleção adaptativa baseada no notebook original.
"""

import logging
from typing import List, Dict, Any, Optional
from .scoring import RelevanceScorer

logger = logging.getLogger(__name__)


class AdaptiveSelection:
    """
    Seleção adaptativa baseada no notebook original.
    Ajusta critérios dinamicamente para garantir resultados mínimos.
    """

    def __init__(self, target_size: int = 100, min_size: int = 20):
        self.target_size = target_size
        self.min_size = min_size
        self.scorer = RelevanceScorer()

        # Critérios adaptativos baseados no notebook original
        self.criteria_levels = [
            {
                "name": "Nível 1 - Critérios rigorosos",
                "year_min": 2020,
                "min_score": 7,
                "require_abstract": True,
                "require_math_focus": True,
                "require_tech_focus": True
            },
            {
                "name": "Nível 2 - Critérios moderados",
                "year_min": 2018,
                "min_score": 5,
                "require_abstract": True,
                "require_math_focus": True,
                "require_tech_focus": False
            },
            {
                "name": "Nível 3 - Critérios flexíveis",
                "year_min": 2015,
                "min_score": 3,
                "require_abstract": False,
                "require_math_focus": False,
                "require_tech_focus": False
            }
        ]

        logger.info(
            f"Adaptive selection initialized: target={self.target_size}, min={self.min_size}")

    def select_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Seleciona artigos usando critérios adaptativos.
        """
        if not articles:
            logger.warning("Nenhum artigo para selecionar")
            return []

        # Calcular scores de relevância
        for article in articles:
            article['relevance_score'] = self.scorer.calculate_score(article)

        # Tentar cada nível de critérios
        for level in self.criteria_levels:
            selected = self._apply_criteria_level(articles, level)
            if len(selected) >= self.min_size:
                logger.info(
                    f"Seleção bem-sucedida no {{level['name']}}: {{len(selected)}} artigos")
                return selected[:self.target_size]

        # Se nenhum nível produziu resultados suficientes, usar critérios mínimos
        logger.warning(
            "Nenhum nível produziu resultados suficientes - usando critérios mínimos")
        return self._apply_minimal_criteria(articles)

    def _apply_criteria_level(self, articles: List[Dict[str, Any]],
                              level: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Aplica um nível específico de critérios.
        """
        selected = []

        for article in articles:
            if self._meets_criteria(article, level):
                selected.append(article)

        return selected

    def _meets_criteria(self, article: Dict[str, Any], level: Dict[str, Any]) -> bool:
        """
        Verifica se um artigo atende aos critérios do nível.
        """
        # Ano mínimo
        if article.get('year', 0) < level['year_min']:
            return False

        # Score mínimo
        if article.get('relevance_score', 0) < level['min_score']:
            return False

        # Resumo obrigatório
        if level['require_abstract'] and not article.get('abstract'):
            return False

        # Foco em matemática
        if level['require_math_focus']:
            text = (article.get('title', '') + ' ' +
                    article.get('abstract', '')).lower()
            math_terms = ['mathematics', 'math',
                          'algebra', 'geometry', 'calculus']
            if not any(term in text for term in math_terms):
                return False

        # Foco em tecnologia
        if level['require_tech_focus']:
            text = (article.get('title', '') + ' ' +
                    article.get('abstract', '')).lower()
            tech_terms = ['machine learning', 'ai',
                          'learning analytics', 'adaptive', 'intelligent']
            if not any(term in text for term in tech_terms):
                return False

        return True

    def _apply_minimal_criteria(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aplica critérios mínimos para garantir alguns resultados.
        """
        # Ordenar por score de relevância
        sorted_articles = sorted(articles, key=lambda x: x.get(
            'relevance_score', 0), reverse=True)

        # Retornar os melhores até o tamanho mínimo
        return sorted_articles[:self.min_size]

    # --- Compatibility helpers expected by tests ---
    def select_adaptive(self, df):
        """
        Backwards-compatible method expected by tests to run adaptive
        selection from a pandas DataFrame input.

        Parameters
        ----------
        df : pandas.DataFrame
            Input articles DataFrame with at least title/abstract/year.

        Returns
        -------
        pandas.DataFrame
            Selected articles as DataFrame.
        """
        try:
            import pandas as pd  # Local import to keep module light
        except Exception:  # pragma: no cover
            raise

        if df is None or getattr(df, 'empty', True):
            return df

        selected_list = self.select_articles(df.to_dict('records'))
        return pd.DataFrame(selected_list)

    def get_selection_report(self, original_df, selected_df):
        """
        Produce a simple selection report dictionary for diagnostics.

        Parameters
        ----------
        original_df : pandas.DataFrame
            Original dataset prior to selection.
        selected_df : pandas.DataFrame
            Resulting selected dataset.

        Returns
        -------
        dict
            Report with counts and basic rates.
        """
        total = 0 if original_df is None else len(original_df)
        selected = 0 if selected_df is None else len(selected_df)
        rate = 0.0 if total == 0 else round((selected / total) * 100.0, 2)
        return {"total": total, "selected": selected, "selection_rate_pct": rate}
