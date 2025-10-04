"""Schema definition for the systematic review database."""

from dataclasses import dataclass
from typing import Optional, List

# Schema completo baseado no notebook
PAPERS_SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    -- Identificadores únicos
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doi TEXT UNIQUE,
    url TEXT,
    paper_id TEXT,  -- ID específico da API (ex: Semantic Scholar paperId)
    
    -- Informações bibliográficas básicas
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    publication_date TEXT,
    venue TEXT,  -- Journal/Conference
    source_publication TEXT,
    
    -- Conteúdo
    abstract TEXT,
    keywords TEXT,
    full_text TEXT,
    
    -- Metadados da busca
    database TEXT,  -- API de origem
    search_engine TEXT,
    query TEXT,  -- Query que retornou o artigo
    search_terms TEXT,
    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Métricas e classificação
    citation_count INTEGER,
    influential_citation_count INTEGER,
    is_open_access BOOLEAN DEFAULT 0,
    open_access_pdf TEXT,
    
    -- Classificação e análise
    comp_techniques TEXT,  -- Técnicas computacionais identificadas
    edu_approach TEXT,  -- Abordagem educacional
    study_type TEXT,  -- Tipo de estudo (experimental, survey, etc)
    eval_methods TEXT,  -- Métodos de avaliação
    
    -- Processo de seleção PRISMA
    selection_stage TEXT DEFAULT 'identification',  -- identification, screening, eligibility, included
    exclusion_reason TEXT,
    inclusion_criteria_met TEXT,
    relevance_score REAL,
    
    -- Controle e notas
    status TEXT DEFAULT 'pending',  -- pending, reviewed, included, excluded
    notes TEXT,
    tags TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

SEARCHES_SCHEMA = """
CREATE TABLE IF NOT EXISTS searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_summary TEXT NOT NULL,
    query TEXT,
    api TEXT,
    results_summary TEXT,  -- JSON
    results_count INTEGER,
    filtered_count INTEGER,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT,
    error_message TEXT
)
"""

CACHE_SCHEMA = """
CREATE TABLE IF NOT EXISTS cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_hash TEXT UNIQUE NOT NULL,
    query TEXT NOT NULL,
    api TEXT NOT NULL,
    results TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0
)
"""

ANALYSIS_SCHEMA = """
CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id INTEGER,
    analysis_type TEXT,  -- gap_analysis, technique_extraction, etc
    results TEXT,  -- JSON
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers(id)
)
"""

# Índices para otimização
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi)",
    "CREATE INDEX IF NOT EXISTS idx_papers_year ON papers(year)",
    "CREATE INDEX IF NOT EXISTS idx_papers_database ON papers(database)",
    "CREATE INDEX IF NOT EXISTS idx_papers_status ON papers(status)",
    "CREATE INDEX IF NOT EXISTS idx_papers_selection ON papers(selection_stage)",
    "CREATE INDEX IF NOT EXISTS idx_cache_query ON cache(query_hash)",
    "CREATE INDEX IF NOT EXISTS idx_cache_api ON cache(api)",
]

# Views úteis
VIEWS = [
    """
    CREATE VIEW IF NOT EXISTS v_included_papers AS
    SELECT * FROM papers 
    WHERE selection_stage = 'included' 
    ORDER BY relevance_score DESC, year DESC
    """,
    
    """
    CREATE VIEW IF NOT EXISTS v_papers_by_year AS
    SELECT year, COUNT(*) as count, 
           AVG(citation_count) as avg_citations
    FROM papers 
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year DESC
    """,
    
    """
    CREATE VIEW IF NOT EXISTS v_papers_by_technique AS
    SELECT comp_techniques, COUNT(*) as count
    FROM papers
    WHERE comp_techniques IS NOT NULL
    GROUP BY comp_techniques
    ORDER BY count DESC
    """
]


@dataclass
class PaperRecord:
    """Dataclass representing a paper record."""
    
    # Identificadores
    doi: Optional[str] = None
    url: Optional[str] = None
    paper_id: Optional[str] = None
    
    # Informações básicas
    title: str = ""
    authors: Optional[str] = None
    year: Optional[int] = None
    publication_date: Optional[str] = None
    venue: Optional[str] = None
    source_publication: Optional[str] = None
    
    # Conteúdo
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    full_text: Optional[str] = None
    
    # Metadados
    database: Optional[str] = None
    search_engine: Optional[str] = None
    query: Optional[str] = None
    search_terms: Optional[str] = None
    
    # Métricas
    citation_count: Optional[int] = None
    influential_citation_count: Optional[int] = None
    is_open_access: bool = False
    open_access_pdf: Optional[str] = None
    
    # Classificação
    comp_techniques: Optional[str] = None
    edu_approach: Optional[str] = None
    study_type: Optional[str] = None
    eval_methods: Optional[str] = None
    
    # Seleção
    selection_stage: str = "identification"
    exclusion_reason: Optional[str] = None
    inclusion_criteria_met: Optional[str] = None
    relevance_score: Optional[float] = None
    
    # Status
    status: str = "pending"
    notes: Optional[str] = None
    tags: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary for database insertion."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
