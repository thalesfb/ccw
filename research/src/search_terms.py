"""
Módulo de termos de busca baseado no notebook original.
Gera 6 × 22 = 132 combinações.
"""

import itertools
from typing import List

# Termos primários do notebook original
FIRST_TERMS = ['mathematics education', 'ensino de matemática', 'math learning', 'aprendizagem matemática', 'mathematics teaching', 'educação matemática']

# Termos secundários do notebook original  
SECOND_TERMS = ['adaptive learning', 'aprendizagem adaptativa', 'personalized learning', 'aprendizagem personalizada', 'intelligent tutoring systems', 'sistemas de tutoria inteligente', 'learning analytics', 'análise de aprendizagem', 'educational data mining', 'mineração de dados educacionais', 'machine learning', 'aprendizado de máquina', 'artificial intelligence', 'inteligência artificial', 'automated assessment', 'avaliação automatizada', 'competency identification', 'identificação de competências', 'student modeling', 'modelagem de estudantes', 'predictive analytics', 'análise preditiva']

def queries_generator(first: List[str], second: List[str]) -> List[str]:
    """
    Generate all combinations of primary and secondary terms for searching in databases.
    Baseado na função do notebook original.
    
    Args:
        first (list): List the first terms.
        second (list): List the second terms.
        
    Returns:
        list: List string with all combinations of terms.
    """
    # Gera combinações de termos primários e secundários
    queries = [
        f'{p} AND {s}'
        for p, s in itertools.product(first, second)
    ]

    print(f"📝 Geradas {len(queries)} combinações de termos de busca")

    return queries

def get_all_queries() -> List[str]:
    """
    Retorna todas as combinações de termos de busca.
    """
    return queries_generator(FIRST_TERMS, SECOND_TERMS)

if __name__ == "__main__":
    queries = get_all_queries()
    print(f"Total de combinações: {len(queries)}")
    print("Primeiras 5 combinações:")
    for i, query in enumerate(queries[:5]):
        print(f"  {i+1}. {query}")
