"""Canonical source for search query generation.

Distribuição das combinações:
Para consultas em inglês:
    total_en = len(en_base_terms) * len(en_tech_terms) * len(en_edu_terms)
Para consultas em português:
    total_pt = len(pt_base_terms) * len(pt_tech_terms) * len(pt_edu_terms)
Total geral = total_en + total_pt

Explicação:
Para cada idioma, para cada trio (base, técnica, educacional) geramos:
    1 query: ``base AND tecnica AND edu``
Logo, por trio (base, técnica, educacional) = 1 query.
Multiplicando por len(base_terms), len(tech_terms) e len(edu_terms) obtemos o total por idioma.

Exemplo real com config atual:
    len(en_base_terms) = 2  # ["mathematics", "math"]
    len(en_tech_terms) = 12 # termos de técnicas em inglês
    len(en_edu_terms) = 2   # ["education", "learning"]
    total_en = 2 * 12 * 2 = 48
    len(pt_base_terms) = 1  # ["matemática"]
    len(pt_tech_terms) = 12 # termos de técnicas em português
    len(pt_edu_terms) = 2   # ["educacao", "ensino"]
    total_pt = 1 * 12 * 2 = 24
    total = 48 + 24 = 72

Este módulo é a única fonte de queries para o pipeline.
"""

from typing import List, Optional


def generate_search_queries(
    en_base_terms: Optional[List[str]] = None,
    en_tech_terms: Optional[List[str]] = None,
    en_edu_terms: Optional[List[str]] = None,
    pt_base_terms: Optional[List[str]] = None,
    pt_tech_terms: Optional[List[str]] = None,
    pt_edu_terms: Optional[List[str]] = None
) -> List[str]:
    """
    Generate bilingual search queries with 3-tier expansion, separated by language.

    This is the canonical query generator used by the pipeline.
    Produces unique queries combining base math terms with
    technique and education keywords, ensuring language consistency.

    Parameters
    ----------
    en_base_terms : list of str, optional
        Base mathematics terms in English. Defaults to ["mathematics", "math"]
    en_tech_terms : list of str, optional
        AI/ML technique terms in English. Defaults to English tech terms
    en_edu_terms : list of str, optional
        Education domain terms in English. Defaults to English edu terms
    pt_base_terms : list of str, optional
        Base mathematics terms in Portuguese. Defaults to ["matemática"]
    pt_tech_terms : list of str, optional
        AI/ML technique terms in Portuguese. Defaults to Portuguese tech terms
    pt_edu_terms : list of str, optional
        Education domain terms in Portuguese. Defaults to Portuguese edu terms

    Returns
    -------
    list of str
        Unique search queries (defaults geram 72: 48 EN + 24 PT)

    Examples
    --------
    >>> queries = generate_search_queries()
    >>> len(queries)
    72
    """
    # Default English base terms
    if en_base_terms is None:
        en_base_terms = ["mathematics", "math"]

    # Default English tech terms
    if en_tech_terms is None:
        en_tech_terms = [
            "adaptive", "personalized", "tutoring", "analytics", "mining",
            "machine learning", "ai", "assessment", "student modeling", "predictive",
            "intelligent tutor", "artificial intelligence"
        ]

    # Default English education terms
    if en_edu_terms is None:
        en_edu_terms = ["education", "learning"]

    # Default Portuguese base terms
    if pt_base_terms is None:
        pt_base_terms = ["matemática"]

    # Default Portuguese tech terms
    if pt_tech_terms is None:
        pt_tech_terms = [
            "adaptivo", "personalizado", "tutor", "analitica", "mineração",
            "aprendizado de máquina", "ia", "avaliação", "modelagem do aluno",
            "preditivo", "tutor inteligente", "inteligência artificial"
        ]

    # Default Portuguese education terms
    if pt_edu_terms is None:
        pt_edu_terms = ["educacao", "ensino"]

    queries: List[str] = []
    seen = set()

    # Generate English queries
    for base in en_base_terms:
        for tech in en_tech_terms:  
            for edu in en_edu_terms:
                q_full = f"{base} AND {tech} AND {edu}"
                if q_full not in seen:
                    queries.append(q_full)
                    seen.add(q_full)

    # Generate Portuguese queries
    for base in pt_base_terms:
        for tech in pt_tech_terms:
            for edu in pt_edu_terms:
                q_full = f"{base} AND {tech} AND {edu}"
                if q_full not in seen:
                    queries.append(q_full)
                    seen.add(q_full)

    return queries


def get_all_queries() -> List[str]:
    """Retorna todas as queries canônicas com parâmetros padrão."""
    return generate_search_queries()

if __name__ == "__main__":
    qs = get_all_queries()
    print(f"Total de queries: {len(qs)}")
    print("Exemplos:")
    for i, q in enumerate(qs[:5]):
        print(f"  {i+1}. {q}")
