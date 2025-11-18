"""
Exportação de referências bibliográficas em formato BibTeX.
=============================================================

Gera arquivos .bib a partir dos papers incluídos na revisão sistemática,
formatados segundo padrões acadêmicos (ABNT, APA, IEEE).

Autor: Thales Ferreira
Data: Outubro 2025
"""

import re
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def sanitize_bibtex_key(text: str, year: str = "") -> str:
    """
    Gera chave BibTeX válida a partir de título/autor.
    
    Formato: PrimeiroAutorAnoKeyword
    Exemplo: Silva2024Machine
    """
    if not text:
        return f"Unknown{year}"
    
    # Remover caracteres especiais, manter apenas alfanuméricos
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Pegar primeira palavra significativa (> 3 chars)
    words = [w for w in clean.split() if len(w) > 3]
    keyword = words[0].capitalize() if words else "Paper"
    
    return f"{keyword}{year}"


def format_authors_bibtex(authors: str) -> str:
    """
    Formata autores para BibTeX.
    
    Entrada: "Silva, J.; Costa, M.; Lima, P."
    Saída: "Silva, J. and Costa, M. and Lima, P."
    """
    if not authors or pd.isna(authors):
        return "Anonymous"
    
    # Substituir separadores por " and "
    authors_clean = authors.replace(';', ' and ').replace(',', ' and ')
    # Remover múltiplos "and" consecutivos
    authors_clean = re.sub(r'\s+and\s+and\s+', ' and ', authors_clean)
    
    return authors_clean.strip()


def infer_publication_type(row: Dict[str, Any]) -> str:
    """
    Infere tipo de publicação (article, inproceedings, book, etc).
    
    Ordem de prioridade:
    1. publication_types (Semantic Scholar)
    2. venue (contém "Conference", "Journal", "arXiv")
    3. doi (começa com "10.1109" = IEEE conference)
    """
    # 1. Usar publication_types se disponível
    pub_types = row.get('ss_publication_types', '')
    if pub_types and not pd.isna(pub_types):
        if 'JournalArticle' in pub_types:
            return 'article'
        elif 'Conference' in pub_types:
            return 'inproceedings'
        elif 'Review' in pub_types:
            return 'article'
    
    # 2. Inferir por venue
    venue = row.get('venue', '')
    if venue and not pd.isna(venue):
        venue_lower = venue.lower()
        if any(kw in venue_lower for kw in ['conference', 'proceedings', 'workshop', 'symposium']):
            return 'inproceedings'
        elif any(kw in venue_lower for kw in ['journal', 'transactions', 'letters', 'magazine']):
            return 'article'
        elif 'arxiv' in venue_lower:
            return 'misc'
    
    # 3. Inferir por DOI (IEEE conferences começam com 10.1109)
    doi = row.get('doi', '')
    if doi and not pd.isna(doi):
        if doi.startswith('10.1109'):
            return 'inproceedings'
    
    # Default: article (mais comum)
    return 'article'


def generate_bibtex_entry(row: Dict[str, Any], index: int) -> str:
    """
    Gera entrada BibTeX individual para um paper.
    
    Campos obrigatórios:
    - @article: author, title, journal, year
    - @inproceedings: author, title, booktitle, year
    
    Campos opcionais:
    - volume, number, pages, doi, url, keywords, abstract
    """
    # Determinar tipo de publicação
    pub_type = infer_publication_type(row)
    
    # Gerar chave BibTeX única
    year = str(row.get('year', ''))
    title = row.get('title', '')
    bibtex_key = sanitize_bibtex_key(title, year) + f"_{index:03d}"
    
    # Campos obrigatórios
    author = format_authors_bibtex(row.get('authors', ''))
    title_clean = title.replace('{', '').replace('}', '')  # BibTeX usa {} para preservar case
    year = year if year else 'n.d.'
    
    # Campos específicos por tipo
    venue = row.get('venue', 'Unknown Venue')
    
    # Montar entrada
    entry_lines = [f"@{pub_type}{{{bibtex_key},"]
    entry_lines.append(f"  author = {{{author}}},")
    entry_lines.append(f"  title = {{{{{title_clean}}}}},")  # Double braces preservam case
    
    if pub_type == 'article':
        entry_lines.append(f"  journal = {{{venue}}},")
    elif pub_type == 'inproceedings':
        entry_lines.append(f"  booktitle = {{{venue}}},")
    else:
        entry_lines.append(f"  howpublished = {{{venue}}},")
    
    entry_lines.append(f"  year = {{{year}}},")
    
    # Campos opcionais
    if row.get('doi') and not pd.isna(row.get('doi')):
        entry_lines.append(f"  doi = {{{row['doi']}}},")
    
    if row.get('url') and not pd.isna(row.get('url')):
        entry_lines.append(f"  url = {{{row['url']}}},")
    
    # Keywords (comp_techniques + edu_approach)
    keywords = []
    if row.get('comp_techniques') and not pd.isna(row.get('comp_techniques')):
        keywords.extend([k.strip() for k in str(row['comp_techniques']).split(';')])
    if row.get('edu_approach') and not pd.isna(row.get('edu_approach')):
        keywords.extend([k.strip() for k in str(row['edu_approach']).split(';')])
    
    if keywords:
        keywords_str = ', '.join(set(keywords))  # Remove duplicatas
        entry_lines.append(f"  keywords = {{{keywords_str}}},")
    
    # Abstract (opcional, útil para análise)
    if row.get('abstract') and not pd.isna(row.get('abstract')):
        abstract = str(row['abstract'])[:500]  # Limitar tamanho
        abstract_clean = abstract.replace('{', '').replace('}', '').replace('\n', ' ')
        entry_lines.append(f"  abstract = {{{abstract_clean}...}},")
    
    # Notas adicionais (score, database)
    notes = []
    if row.get('relevance_score') and not pd.isna(row.get('relevance_score')):
        notes.append(f"Relevance: {row['relevance_score']:.1f}/10")
    if row.get('database') and not pd.isna(row.get('database')):
        notes.append(f"Source: {row['database']}")
    
    if notes:
        notes_str = '; '.join(notes)
        entry_lines.append(f"  note = {{{notes_str}}},")
    
    entry_lines.append("}")
    
    return '\n'.join(entry_lines)


def export_to_bibtex(df: pd.DataFrame, output_path: Path = None) -> Path:
    """
    Exporta DataFrame de papers para arquivo BibTeX.
    
    Args:
        df: DataFrame com papers (colunas: title, authors, year, venue, doi, etc)
        output_path: Caminho do arquivo .bib (default: research/references/generated.bib)
    
    Returns:
        Path do arquivo gerado
    """
    if output_path is None:
        output_path = Path("research/references/generated_references.bib")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Gerando arquivo BibTeX com {len(df)} entradas...")
    
    # Cabeçalho do arquivo
    header = f"""% BibTeX References - Systematic Review
% Generated automatically from database
% Total entries: {len(df)}
% Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
%
% Usage in LaTeX:
%   \\bibliography{{{output_path.stem}}}
%   \\bibliographystyle{{abntex2-num}}  % or ieeetr, apalike, etc.
%

"""
    
    entries = []
    for idx, row in df.iterrows():
        try:
            entry = generate_bibtex_entry(row.to_dict(), idx)
            entries.append(entry)
        except Exception as e:
            logger.warning(f"Erro ao gerar entrada BibTeX para paper {idx}: {e}")
            continue
    
    # Escrever arquivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write('\n\n'.join(entries))
        f.write('\n')
    
    logger.info(f"✅ Arquivo BibTeX gerado: {output_path} ({len(entries)} entradas)")
    
    return output_path


def export_bibtex_by_category(df: pd.DataFrame, output_dir: Path = None) -> Dict[str, Path]:
    """
    Exporta múltiplos arquivos BibTeX organizados por categoria.
    
    Categorias:
    - all.bib: Todos os papers
    - included.bib: Apenas papers incluídos
    - high_relevance.bib: Score >= 7.0
    - by_technique.bib: Separados por técnica computacional
    
    Returns:
        Dict com mapeamento categoria -> caminho do arquivo
    """
    if output_dir is None:
        output_dir = Path("research/references")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    files = {}
    
    # 1. Todos os papers
    if not df.empty:
        files['all'] = export_to_bibtex(df, output_dir / "all_papers.bib")
    
    # 2. Apenas incluídos
    if 'selection_stage' in df.columns:
        included = df[df['selection_stage'] == 'included']
        if not included.empty:
            files['included'] = export_to_bibtex(included, output_dir / "included_papers.bib")
    
    # 3. Alta relevância
    if 'relevance_score' in df.columns:
        high_rel = df[df['relevance_score'] >= 7.0]
        if not high_rel.empty:
            files['high_relevance'] = export_to_bibtex(high_rel, output_dir / "high_relevance.bib")
    
    # 4. Por técnica (top 3 técnicas)
    if 'comp_techniques' in df.columns:
        techniques_count = Counter()
        for tech_str in df['comp_techniques'].dropna():
            techniques = [t.strip() for t in str(tech_str).split(';')]
            techniques_count.update(techniques)
        
        top_techniques = [tech for tech, _ in techniques_count.most_common(3)]
        
        for tech in top_techniques:
            tech_df = df[df['comp_techniques'].str.contains(tech, case=False, na=False)]
            if not tech_df.empty:
                safe_tech = re.sub(r'[^a-z0-9]', '_', tech.lower())
                files[f'technique_{safe_tech}'] = export_to_bibtex(
                    tech_df, 
                    output_dir / f"technique_{safe_tech}.bib"
                )
    
    logger.info(f"✅ Gerados {len(files)} arquivos BibTeX em {output_dir}")
    
    return files


if __name__ == "__main__":
    # Teste standalone
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    
    from research.src.db import read_papers
    from research.src.config import load_config
    
    cfg = load_config()
    df = read_papers(cfg)
    
    if not df.empty:
        included = df[df['selection_stage'] == 'included']
        files = export_bibtex_by_category(included)
        
        print("\n✅ Arquivos BibTeX gerados:")
        for category, path in files.items():
            print(f"  {category}: {path}")
    else:
        print("❌ Nenhum paper encontrado no banco de dados")
