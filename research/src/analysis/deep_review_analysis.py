"""
Análise Aprofundada dos Papers Incluídos na Revisão Sistemática
=================================================================

Este script realiza análise qualitativa aprofundada dos papers marcados
como 'included' no banco de dados SQLite canônico (ver `research/systematic_review.db`).
Os números exatos (total de papers incluídos) são obtidos dinamicamente a partir
do banco antes da execução; não há contagens hard-coded neste script.

Estratégias:
1. Enriquecimento via Semantic Scholar API (tldr, citations, references)
2. Análise temática via LLM (clustering, gaps, metodologias)
3. Geração de relatório Markdown estruturado
4. Visualizações de redes (co-citação, co-autoria)

Autor: Thales Ferreira
Data: Outubro 2025
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Any
import requests
from collections import Counter, defaultdict
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


class DeepReviewAnalyzer:
    """Analisador aprofundado de papers da revisão sistemática."""
    
    def __init__(self, db_path: str = "research/systematic_review.db"):
        self.db_path = db_path
        self.papers = []
        self.enriched_papers = []
        self.output_dir = Path("research/docs/deep_analysis")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_included_papers(self) -> List[Dict[str, Any]]:
        """Carrega os papers marcados como 'included' no banco de dados.

        The exact number of included papers is read from the canonical SQLite
        database at runtime; this method does not assume a fixed count.
        """
        logger.info("Carregando papers incluídos do banco de dados...")
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, doi, url, paper_id, title, authors, year, venue,
                abstract, keywords, database, citation_count,
                is_open_access, open_access_pdf, comp_techniques,
                edu_approach, study_type, eval_methods, relevance_score,
                tags, notes
            FROM papers 
            WHERE selection_stage = 'included'
            ORDER BY relevance_score DESC, citation_count DESC
        """)
        
        papers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        logger.info(f"✅ {len(papers)} papers carregados")
        self.papers = papers
        return papers
    
    def enrich_with_semantic_scholar(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """Enriquece paper com dados do Semantic Scholar API."""
        
        # Tentar buscar por DOI primeiro, depois paper_id
        identifiers = []
        if paper.get('doi'):
            identifiers.append(f"DOI:{paper['doi']}")
        if paper.get('paper_id') and paper.get('database') == 'semantic_scholar':
            identifiers.append(paper['paper_id'])
        
        if not identifiers:
            logger.warning(f"⚠️ Paper sem identificador: {paper.get('title', 'N/A')[:50]}")
            return paper
        
        # Tentar cada identificador
        for identifier in identifiers:
            try:
                url = f"https://api.semanticscholar.org/graph/v1/paper/{identifier}"
                params = {
                    "fields": "title,abstract,year,authors,citations,references,tldr,embedding,fieldsOfStudy,publicationTypes,citationStyles"
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Enriquecer paper
                    paper['ss_tldr'] = data.get('tldr', {}).get('text') if data.get('tldr') else None
                    paper['ss_citations_count'] = len(data.get('citations', [])) if data.get('citations') else 0
                    paper['ss_references_count'] = len(data.get('references', [])) if data.get('references') else 0
                    paper['ss_fields_of_study'] = data.get('fieldsOfStudy', []) or []
                    paper['ss_publication_types'] = data.get('publicationTypes', []) or []
                    
                    # Citar papers mais influentes
                    citations = data.get('citations', [])
                    if citations:
                        influential = sorted(
                            citations, 
                            key=lambda x: x.get('citationCount', 0), 
                            reverse=True
                        )[:5]
                        paper['ss_top_citations'] = [
                            {
                                'title': c.get('title'),
                                'year': c.get('year'),
                                'citationCount': c.get('citationCount')
                            }
                            for c in influential
                        ]
                    
                    logger.info(f"✅ Enriquecido: {paper.get('title', 'N/A')[:50]}")
                    time.sleep(4)  # Rate limiting
                    return paper
                
                elif response.status_code == 429:
                    logger.warning("⚠️ Rate limit atingido, aguardando...")
                    time.sleep(10)
                    continue
                    
            except Exception as e:
                logger.error(f"❌ Erro ao enriquecer paper: {e}")
                continue
        
        return paper
    
    def enrich_all_papers(self) -> List[Dict[str, Any]]:
        """Enriquece todos os papers com dados de APIs."""
        logger.info("Iniciando enriquecimento de papers...")
        
        enriched = []
        for i, paper in enumerate(self.papers, 1):
            logger.info(f"Processando paper {i}/{len(self.papers)}...")
            enriched_paper = self.enrich_with_semantic_scholar(paper)
            enriched.append(enriched_paper)
        
        self.enriched_papers = enriched
        
        # Salvar cache
        cache_file = self.output_dir / "enriched_papers_cache.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(enriched, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✅ Cache salvo em: {cache_file}")
        return enriched
    
    def analyze_themes(self) -> Dict[str, Any]:
        """Analisa temas e técnicas computacionais."""
        logger.info("Analisando temas e técnicas...")
        
        # Técnicas computacionais
        techniques = []
        for paper in self.enriched_papers:
            tech = paper.get('comp_techniques', '')
            if tech:
                techniques.extend([t.strip() for t in tech.split(',')])
        
        technique_counts = Counter(techniques)
        
        # Abordagens educacionais
        edu_approaches = []
        for paper in self.enriched_papers:
            approach = paper.get('edu_approach', '')
            if approach:
                edu_approaches.extend([a.strip() for a in approach.split(',')])
        
        edu_counts = Counter(edu_approaches)
        
        # Tipos de estudo
        study_types = []
        for paper in self.enriched_papers:
            stype = paper.get('study_type', '')
            if stype:
                study_types.append(stype.strip())
        
        study_counts = Counter(study_types)
        
        # Campos de estudo (Semantic Scholar)
        fields = []
        for paper in self.enriched_papers:
            fos = paper.get('ss_fields_of_study', [])
            if fos:  # Verificar se não é None
                fields.extend(fos)
        
        field_counts = Counter(fields)
        
        return {
            'techniques': dict(technique_counts.most_common(15)),
            'edu_approaches': dict(edu_counts.most_common(10)),
            'study_types': dict(study_counts.most_common()),
            'fields_of_study': dict(field_counts.most_common(10)),
            'total_papers': len(self.enriched_papers)
        }
    
    def analyze_temporal_trends(self) -> Dict[str, Any]:
        """Analisa tendências temporais."""
        logger.info("Analisando tendências temporais...")
        
        years = [p.get('year') for p in self.enriched_papers if p.get('year')]
        year_counts = Counter(years)
        
        # Técnicas por período
        techniques_by_period = defaultdict(list)
        for paper in self.enriched_papers:
            year = paper.get('year')
            tech = paper.get('comp_techniques', '')
            if year and tech:
                period = f"{(year // 5) * 5}-{(year // 5) * 5 + 4}"
                techniques_by_period[period].extend([t.strip() for t in tech.split(',')])
        
        return {
            'papers_by_year': dict(sorted(year_counts.items())),
            'techniques_by_period': {
                period: dict(Counter(techs).most_common(5))
                for period, techs in techniques_by_period.items()
            }
        }
    
    def analyze_citation_network(self) -> Dict[str, Any]:
        """Analisa rede de citações."""
        logger.info("Analisando rede de citações...")
        
        # Papers mais citados
        citations = [
            (p.get('title'), p.get('citation_count', 0))
            for p in self.enriched_papers
        ]
        most_cited = sorted(citations, key=lambda x: x[1], reverse=True)[:10]
        
        # Papers mais influentes (Semantic Scholar)
        ss_citations = [
            (p.get('title'), p.get('ss_citations_count', 0))
            for p in self.enriched_papers
            if p.get('ss_citations_count')
        ]
        most_influential = sorted(ss_citations, key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'most_cited': most_cited,
            'most_influential': most_influential,
            'avg_citations': sum(c for _, c in citations) / len(citations) if citations else 0
        }
    
    def generate_markdown_report(self, analyses: Dict[str, Any]) -> str:
        """Gera relatório completo em Markdown."""
        logger.info("Gerando relatório Markdown...")
        
        report = f"""# 📊 Análise Aprofundada dos Papers Incluídos

**Data da análise**: {time.strftime('%d/%m/%Y %H:%M')}  
**Total de papers analisados**: {len(self.enriched_papers)}  
**Fonte**: Revisão Sistemática - Base de dados SQLite

---

## 📈 Visão Geral

### Estatísticas Gerais

- **Papers incluídos**: {len(self.enriched_papers)}
- **Período coberto**: {min(p.get('year', 9999) for p in self.enriched_papers)} - {max(p.get('year', 0) for p in self.enriched_papers)}
- **Média de citações**: {analyses['citations']['avg_citations']:.1f}
- **Bases de dados**: {len(set(p.get('database') for p in self.enriched_papers))} diferentes

---

## 🧠 Técnicas Computacionais Mais Utilizadas

"""
        
        # Técnicas
        for i, (tech, count) in enumerate(analyses['themes']['techniques'].items(), 1):
            pct = (count / analyses['themes']['total_papers']) * 100
            report += f"{i}. **{tech}**: {count} papers ({pct:.1f}%)\n"
        
        report += f"""
---

## 🎓 Abordagens Educacionais

"""
        
        # Abordagens educacionais
        for i, (approach, count) in enumerate(analyses['themes']['edu_approaches'].items(), 1):
            pct = (count / analyses['themes']['total_papers']) * 100
            report += f"{i}. **{approach}**: {count} papers ({pct:.1f}%)\n"
        
        report += f"""
---

## 📚 Tipos de Estudo

"""
        
        # Tipos de estudo
        for stype, count in analyses['themes']['study_types'].items():
            pct = (count / analyses['themes']['total_papers']) * 100
            report += f"- **{stype}**: {count} papers ({pct:.1f}%)\n"
        
        report += f"""
---

## 📅 Tendências Temporais

### Distribuição por Ano

"""
        
        # Anos
        for year, count in sorted(analyses['temporal']['papers_by_year'].items()):
            report += f"- **{year}**: {count} papers\n"
        
        report += f"""
---

## 🌟 Papers Mais Citados (Top 10)

"""
        
        # Citações
        for i, (title, citations) in enumerate(analyses['citations']['most_cited'], 1):
            report += f"{i}. *{title[:80]}...* ({citations} citações)\n"
        
        report += f"""
---

## 🔗 Papers Mais Influentes (Semantic Scholar)

"""
        
        # Influentes
        if analyses['citations']['most_influential']:
            for i, (title, citations) in enumerate(analyses['citations']['most_influential'], 1):
                report += f"{i}. *{title[:80]}...* ({citations} citações no SS)\n"
        else:
            report += "*Dados de Semantic Scholar não disponíveis para todos os papers*\n"
        
        report += f"""
---

## 🔍 Campos de Estudo (Semantic Scholar)

"""
        
        # Campos
        for field, count in analyses['themes']['fields_of_study'].items():
            report += f"- **{field}**: {count} papers\n"
        
        report += f"""
---

## 📖 Resumos Executivos (TL;DR)

"""
        
        # TL;DR dos papers com maior relevância
        top_papers = sorted(
            self.enriched_papers,
            key=lambda x: (x.get('relevance_score', 0), x.get('citation_count', 0)),
            reverse=True
        )[:10]
        
        for i, paper in enumerate(top_papers, 1):
            tldr = paper.get('ss_tldr', 'N/A')
            report += f"""
### {i}. {paper.get('title', 'N/A')}

**Ano**: {paper.get('year', 'N/A')}  
**Venue**: {paper.get('venue', 'N/A')}  
**Relevância**: {paper.get('relevance_score', 0):.1f}/10  
**Citações**: {paper.get('citation_count', 0)}

**TL;DR**: {tldr if tldr else 'Resumo não disponível'}

**DOI**: {paper.get('doi', 'N/A')}

---
"""
        
        return report
    
    def run_full_analysis(self):
        """Executa análise completa."""
        logger.info("=== INICIANDO ANÁLISE APROFUNDADA ===")
        
        # 1. Carregar papers
        self.load_included_papers()
        
        # 2. Enriquecer com APIs
        logger.info("\n📡 Fase 1: Enriquecimento via APIs")
        self.enrich_all_papers()
        
        # 3. Análises
        logger.info("\n🔬 Fase 2: Análises Temáticas e Temporais")
        themes = self.analyze_themes()
        temporal = self.analyze_temporal_trends()
        citations = self.analyze_citation_network()
        
        analyses = {
            'themes': themes,
            'temporal': temporal,
            'citations': citations
        }
        
        # 4. Gerar relatório
        logger.info("\n📝 Fase 3: Geração de Relatório")
        report = self.generate_markdown_report(analyses)
        
        # Salvar relatório
        report_file = self.output_dir / "DEEP_ANALYSIS_REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"✅ Relatório salvo em: {report_file}")
        
        # Salvar análises em JSON
        analyses_file = self.output_dir / "analyses_summary.json"
        with open(analyses_file, 'w', encoding='utf-8') as f:
            json.dump(analyses, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✅ Análises salvas em: {analyses_file}")
        
        logger.info("\n🎉 ANÁLISE COMPLETA!")
        
        # Calcular métricas para retorno
        year_min = min((p.get('year', 9999) for p in self.enriched_papers if p.get('year')), default=0)
        year_max = max((p.get('year', 0) for p in self.enriched_papers if p.get('year')), default=0)
        avg_citations = sum(p.get('citation_count', 0) for p in self.enriched_papers) / len(self.enriched_papers) if self.enriched_papers else 0
        
        return {
            'total_papers': len(self.enriched_papers),
            'year_range': f"{year_min}-{year_max}" if year_min and year_max else 'N/A',
            'avg_citations': avg_citations,
            'report_file': str(report_file),
            'analyses_file': str(analyses_file)
        }


if __name__ == "__main__":
    analyzer = DeepReviewAnalyzer()
    results = analyzer.run_full_analysis()
    print(f"\n✅ Análise concluída: {results}")
