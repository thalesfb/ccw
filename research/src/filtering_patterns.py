"""
Padrões de filtragem baseados no notebook original.
"""

import re
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional

# Regex patterns do notebook original
ML_TERMS = r"(machine learning|deep learning|data mining|neural network|svm|random forest|bayes|lstm)"
LA_TERMS = r"(learning analytics|educational data mining|intelligent tutor|adaptive learning|personalized learning|student modeling)"
EDU_MATH = r"(mathematics|matemática|algebra|geometry|geometria|calculus|cálculo|fractions?|fraç(ões|ao))"

# Combinar termos computacionais
COMPUTE_TERMS = "|".join([ML_TERMS, LA_TERMS])

# Regex para tipos de estudo (do notebook original)
STUDY_TYPE_REGEX = {'experimental': '(experiment(al)?|randomized controlled trial|RCT)', 'quasi-experimental': '(quasi-experiment(al)?)', 'case study': '(case stud(y|ies))',
                    'user study': '(user stud(y|ies)|usability test)', 'survey': '(survey|questionnaire)', 'review': '(review|meta-analysis|systematic review)', 'proposal/position': '(proposal|position paper|framework)'}

# Regex para métodos de avaliação (do notebook original)
EVAL_METHODS_REGEX = {'statistical analysis': '(statistical analysis|t-test|anova|chi-square|regression)', 'performance metrics': '(accuracy|precision|recall|f1-score|auc|rmse)',
                      'qualitative analysis': '(qualitative|interview|observation|content analysis)', 'user feedback': '(user feedback|satisfaction|survey)'}


def is_relevant_paper(paper: Dict[str, Any], year_min: int, langs: List[str],
                      keywords: List[str], tech_terms: List[str]) -> Tuple[bool, str]:
    """
    Filtro genérico para artigos baseado no notebook original.
    """
    # Ano
    if not isinstance(paper.get('year'), int) or paper.get('year', 0) < year_min:
        return False, f"Ano < {year_min}"

    # Título ou Resumo vazio
    if not paper.get('title') and not paper.get('abstract'):
        return False, "Título e Resumo vazios"

    text_to_check = (paper.get('title', '') + " " +
                     paper.get('abstract', '')).lower()

    # Idioma (heurística: verifica se há palavras-chave em português ou inglês)
    if text_to_check and langs:
        lang_detected = False
        # Simple check if common words exist - adjust if needed
        # English check
        if any(w in text_to_check for w in ['the', 'a', 'is', 'in', 'of', 'and']):
            if 'en' in langs:
                lang_detected = True
        # Portuguese check
        if any(w in text_to_check for w in ['o', 'a', 'é', 'em', 'de', 'e']):
            if 'pt' in langs:
                lang_detected = True

    # Palavras-chave de educação
    if keywords and not any(k.lower() in text_to_check for k in keywords):
        return False, "Sem palavra-chave de educação"

    # Palavras-chave de tecnologia
    if tech_terms and not any(t.lower() in text_to_check for t in tech_terms):
        return False, "Sem termo de tecnologia"

    return True, ""


def normalize_text(text: str) -> str:
    """
    Normaliza texto (acentos, minúsculas) baseado no notebook original.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    import unicodedata
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    return text


def calculate_relevance_score(paper: Dict[str, Any], config: Optional[Dict] = None) -> float:
    """
    Calcula score de relevância baseado no notebook original.
    """
    score = 0
    title = str(paper.get('title', '')).lower()
    abstract = str(paper.get('abstract', '')).lower()

    # Pontos por ano (mais recente = mais pontos)
    year = paper.get('year', 0)
    if year >= 2022:
        score += 3
    elif year >= 2020:
        score += 2
    elif year >= 2018:
        score += 1

    # Pontos por acesso aberto
    if paper.get('is_open_access', False):
        score += 1

    # Pontos por ter resumo
    if len(abstract) > 100:
        score += 1

    # Pontos por termos relevantes
    math_terms = ['mathematics', 'math', 'algebra',
                  'geometry', 'calculus', 'statistics']
    tech_terms = ['machine learning', 'ai',
                  'learning analytics', 'adaptive', 'intelligent']

    for term in math_terms:
        if term in title:
            score += 2
        if term in abstract:
            score += 1

    for term in tech_terms:
        if term in title:
            score += 2
        if term in abstract:
            score += 1

    return min(score, 10)  # Máximo 10
