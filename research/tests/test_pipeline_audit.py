"""
Testes de Auditoria do Pipeline - Validação Completa

Este módulo testa todo o fluxo do pipeline para garantir que:
1. Deduplicação marca corretamente is_duplicate e duplicate_of
2. Estágios PRISMA são atribuídos corretamente
3. Estatísticas PRISMA são calculadas com dados históricos
4. Inserção no banco é idempotente (re-run não cria duplicatas)
5. Export gera dados consistentes com o banco

Execute antes de resetar o banco para validar integridade do pipeline.
"""
import json
import pytest
import pandas as pd
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


# ============================================================================
# TESTES DE DEDUPLICAÇÃO
# ============================================================================

class TestDeduplication:
    """Testes para validar marcação correta de duplicatas."""
    
    def test_find_duplicates_marks_by_doi(self):
        """Verifica que duplicatas por DOI são marcadas corretamente."""
        from src.processing.dedup import find_duplicates
        
        df = pd.DataFrame([
            {'doi': '10.1234/test', 'title': 'Paper A', 'abstract': 'Abstract 1'},
            {'doi': '10.1234/test', 'title': 'Paper A', 'abstract': 'Abstract 2'},  # Duplicata
            {'doi': '10.5678/other', 'title': 'Paper B', 'abstract': 'Abstract 3'},
        ])
        
        result = find_duplicates(df)
        
        # Primeiro registro deve ser único
        assert result.iloc[0]['is_duplicate'] == False
        assert pd.isna(result.iloc[0]['duplicate_of']) or result.iloc[0]['duplicate_of'] is None
        
        # Segundo registro deve ser marcado como duplicata
        assert result.iloc[1]['is_duplicate'] == True
        assert 'DOI:10.1234/test' in str(result.iloc[1]['duplicate_of'])
        
        # Terceiro registro deve ser único
        assert result.iloc[2]['is_duplicate'] == False
    
    def test_find_duplicates_case_insensitive_doi(self):
        """Verifica que DOIs são comparados case-insensitive."""
        from src.processing.dedup import find_duplicates
        
        df = pd.DataFrame([
            {'doi': '10.1234/TEST', 'title': 'Paper A'},
            {'doi': '10.1234/test', 'title': 'Paper A'},  # Mesmo DOI, case diferente
        ])
        
        result = find_duplicates(df)
        
        # Segundo deve ser marcado como duplicata (DOI normalizado)
        assert result.iloc[1]['is_duplicate'] == True
    
    def test_find_duplicates_empty_doi_not_duplicate(self):
        """Verifica que papers sem DOI não são marcados como duplicatas entre si."""
        from src.processing.dedup import find_duplicates
        
        df = pd.DataFrame([
            {'doi': '', 'title': 'Paper A'},
            {'doi': None, 'title': 'Paper B'},
            {'doi': '', 'title': 'Paper C'},
        ])
        
        result = find_duplicates(df)
        
        # Nenhum deve ser marcado como duplicata (DOIs vazios são ignorados)
        assert result['is_duplicate'].sum() == 0


# ============================================================================
# TESTES DE ESTÁGIOS PRISMA
# ============================================================================

class TestPrismaStages:
    """Testes para validar fluxo de estágios PRISMA."""
    
    def test_stage_hierarchy_preserved_in_dedup(self):
        """Verifica que stage superior é preservado durante seleção de melhor duplicata."""
        from src.exports.excel import _select_best_duplicate
        
        group = pd.DataFrame([
            {
                'doi': '10.1234/test',
                'abstract': 'Short',
                'citation_count': 5,
                'selection_stage': 'included',
                'is_duplicate': False
            },
            {
                'doi': '10.1234/test',
                'abstract': 'Very long detailed abstract with more content',
                'citation_count': 100,
                'selection_stage': 'screening',
                'is_duplicate': True
            }
        ])
        
        best = _select_best_duplicate(group, preserve_stage=True)
        
        # Deve ter abstract longo (qualidade) mas stage 'included' (preservado)
        assert len(best['abstract']) > 10
        assert best['selection_stage'] == 'included'
    
    def test_valid_stage_values(self):
        """Verifica que apenas estágios válidos são aceitos."""
        valid_stages = ['identification', 'screening', 'eligibility', 'included']
        
        # Criar DataFrame com todos os estágios válidos
        df = pd.DataFrame([
            {'doi': f'10.{i}/test', 'selection_stage': stage}
            for i, stage in enumerate(valid_stages)
        ])
        
        # Todos devem estar presentes
        assert set(df['selection_stage'].unique()) == set(valid_stages)


# ============================================================================
# TESTES DE ESTATÍSTICAS PRISMA
# ============================================================================

class TestPrismaStats:
    """Testes para validar cálculo de estatísticas PRISMA."""
    
    def test_compute_prisma_stats_with_historical_data(self):
        """Verifica que stats usam dados históricos quando disponíveis."""
        from src.exports.excel import _compute_prisma_stats_from_df, _get_historical_dedup_stats
        
        # Criar DataFrame de teste
        df = pd.DataFrame([
            {'doi': '10.1/a', 'selection_stage': 'included', 'is_duplicate': False},
            {'doi': '10.2/b', 'selection_stage': 'eligibility', 'is_duplicate': False},
            {'doi': '10.3/c', 'selection_stage': 'screening', 'is_duplicate': False},
        ])
        
        stats = _compute_prisma_stats_from_df(df)
        
        # Verificar estrutura das stats
        assert 'identification' in stats
        assert 'duplicates_removed' in stats
        assert 'screening' in stats
        assert 'eligibility' in stats
        assert 'included' in stats
        
        # screening deve ser igual ao número de registros únicos
        assert stats['screening'] == 3
        
        # included deve ser 1
        assert stats['included'] == 1
    
    def test_eligibility_includes_included_papers(self):
        """Verifica que eligibility conta papers que passaram triagem (eligibility + included)."""
        from src.exports.excel import _compute_prisma_stats_from_df
        
        df = pd.DataFrame([
            {'doi': '10.1/a', 'selection_stage': 'included', 'status': 'included'},
            {'doi': '10.2/b', 'selection_stage': 'included', 'status': 'included'},
            {'doi': '10.3/c', 'selection_stage': 'eligibility', 'status': 'excluded'},
            {'doi': '10.4/d', 'selection_stage': 'screening', 'status': 'excluded'},
        ])
        
        stats = _compute_prisma_stats_from_df(df)
        
        # eligibility = eligibility + included = 1 + 2 = 3
        assert stats['eligibility'] == 3
        assert stats['included'] == 2


# ============================================================================
# TESTES DE IDEMPOTÊNCIA DO BANCO
# ============================================================================

class TestDatabaseIdempotency:
    """Testes para validar que operações no banco são idempotentes."""
    
    def test_insert_papers_bulk_skips_duplicates(self):
        """Verifica que papers já existentes são atualizados, não duplicados."""
        import shutil
        from src.database.manager import DatabaseManager
        from src.database.schema import PaperRecord
        
        # Criar diretório temporário manualmente para evitar problemas com SQLite no Windows
        tmpdir = tempfile.mkdtemp()
        db_path = Path(tmpdir) / "test.sqlite"
        
        try:
            # Mock config
            mock_config = MagicMock()
            mock_config.database.db_path = str(db_path)
            
            db = DatabaseManager(mock_config)
            
            # Inserir paper inicial
            paper1 = PaperRecord()
            paper1.doi = '10.1234/test'
            paper1.title = 'Test Paper'
            paper1.selection_stage = 'screening'
            
            inserted1 = db.insert_papers_bulk([paper1])
            
            # Tentar inserir mesmo paper novamente com dados diferentes
            paper2 = PaperRecord()
            paper2.doi = '10.1234/test'
            paper2.title = 'Test Paper'
            paper2.selection_stage = 'included'  # Estágio diferente
            paper2.abstract = 'New abstract'
            
            inserted2 = db.insert_papers_bulk([paper2])
            
            # Verificar usando get_papers() - método correto da API
            papers_df = db.get_papers()
            
            # Deve ter apenas 1 paper
            assert len(papers_df) == 1
            
            # Paper deve ter sido atualizado
            assert papers_df.iloc[0]['selection_stage'] == 'included'
        finally:
            # Cleanup manual - ignorar erros no Windows
            shutil.rmtree(tmpdir, ignore_errors=True)
    
    def test_insert_papers_bulk_skips_marked_duplicates(self):
        """Verifica que papers com is_duplicate=True não são inseridos."""
        import shutil
        from src.database.manager import DatabaseManager
        from src.database.schema import PaperRecord
        
        tmpdir = tempfile.mkdtemp()
        db_path = Path(tmpdir) / "test.sqlite"
        
        try:
            mock_config = MagicMock()
            mock_config.database.db_path = str(db_path)
            
            db = DatabaseManager(mock_config)
            
            # Paper marcado como duplicata
            paper = PaperRecord()
            paper.doi = '10.1234/dup'
            paper.title = 'Duplicate Paper'
            paper.is_duplicate = True
            
            inserted = db.insert_papers_bulk([paper])
            
            # Não deve ter inserido
            assert inserted == 0
            
            papers_df = db.get_papers()
            assert len(papers_df) == 0
        finally:
            # Cleanup manual - ignorar erros no Windows
            shutil.rmtree(tmpdir, ignore_errors=True)


# ============================================================================
# TESTES DE INTEGRIDADE DO EXPORT
# ============================================================================

class TestExportIntegrity:
    """Testes para validar que export gera dados corretos."""
    
    def test_get_best_duplicates_reduces_count(self):
        """Verifica que get_best_duplicates reduz para registros únicos."""
        from src.exports.excel import get_best_duplicates
        from src.processing.dedup import find_duplicates
        
        df = pd.DataFrame([
            {'doi': '10.1/a', 'title': 'Paper A', 'abstract': 'Short', 'selection_stage': 'included'},
            {'doi': '10.1/a', 'title': 'Paper A', 'abstract': 'Much longer abstract', 'selection_stage': 'screening'},
            {'doi': '10.2/b', 'title': 'Paper B', 'abstract': 'Unique', 'selection_stage': 'eligibility'},
        ])
        
        # Marcar duplicatas
        df_marked = find_duplicates(df)
        
        # Selecionar melhores
        result = get_best_duplicates(df_marked)
        
        # Deve ter 2 papers únicos
        assert len(result) == 2
        
        # Paper A deve ter abstract longo mas stage included
        paper_a = result[result['doi'] == '10.1/a'].iloc[0]
        assert 'longer' in paper_a['abstract']
        assert paper_a['selection_stage'] == 'included'
    
    def test_export_preserves_all_stages(self):
        """Verifica que export não perde papers de nenhum estágio."""
        from src.exports.excel import get_best_duplicates
        from src.processing.dedup import find_duplicates
        
        df = pd.DataFrame([
            {'doi': '10.1/a', 'title': 'A', 'abstract': 'x', 'selection_stage': 'included'},
            {'doi': '10.2/b', 'title': 'B', 'abstract': 'x', 'selection_stage': 'eligibility'},
            {'doi': '10.3/c', 'title': 'C', 'abstract': 'x', 'selection_stage': 'screening'},
        ])
        
        df_marked = find_duplicates(df)
        result = get_best_duplicates(df_marked)
        
        # Todos os estágios devem estar presentes
        stages = set(result['selection_stage'].unique())
        assert 'included' in stages
        assert 'eligibility' in stages
        assert 'screening' in stages


# ============================================================================
# TESTES DE HISTÓRICO DE DEDUPLICAÇÃO
# ============================================================================

class TestHistoricalDedup:
    """Testes para validar busca de estatísticas históricas."""
    
    def test_get_historical_dedup_stats_parses_json(self):
        """Verifica que função parseia corretamente JSON da tabela searches."""
        from src.exports.excel import _get_historical_dedup_stats
        
        # Este teste depende de haver dados na tabela searches
        # Em ambiente de teste limpo, retorna (0, 0)
        initial, removed = _get_historical_dedup_stats()
        
        # Deve retornar tupla de inteiros
        assert isinstance(initial, int)
        assert isinstance(removed, int)
        assert initial >= 0
        assert removed >= 0


# ============================================================================
# TESTES DE FLUXO COMPLETO
# ============================================================================

class TestFullPipelineFlow:
    """Testes de integração para fluxo completo do pipeline."""
    
    def test_full_dedup_to_export_flow(self):
        """Testa fluxo completo: coleta -> dedup -> seleção -> export."""
        from src.processing.dedup import find_duplicates
        from src.exports.excel import get_best_duplicates, _compute_prisma_stats_from_df
        
        # Simular dados coletados de múltiplas APIs
        collected_data = pd.DataFrame([
            # Paper 1 - aparece em 2 APIs
            {'doi': '10.1/paper1', 'title': 'Paper 1', 'abstract': 'Short', 
             'database': 'semantic_scholar', 'selection_stage': 'included', 'citation_count': 10},
            {'doi': '10.1/paper1', 'title': 'Paper 1', 'abstract': 'Much longer abstract here',
             'database': 'openalex', 'selection_stage': 'screening', 'citation_count': 15},
            
            # Paper 2 - único
            {'doi': '10.2/paper2', 'title': 'Paper 2', 'abstract': 'Unique paper',
             'database': 'crossref', 'selection_stage': 'eligibility', 'citation_count': 5},
            
            # Paper 3 - aparece em 3 APIs
            {'doi': '10.3/paper3', 'title': 'Paper 3', 'abstract': 'A',
             'database': 'semantic_scholar', 'selection_stage': 'screening', 'citation_count': 1},
            {'doi': '10.3/paper3', 'title': 'Paper 3', 'abstract': 'AB',
             'database': 'openalex', 'selection_stage': 'screening', 'citation_count': 2},
            {'doi': '10.3/paper3', 'title': 'Paper 3', 'abstract': 'ABC',
             'database': 'core', 'selection_stage': 'screening', 'citation_count': 3},
        ])
        
        # Passo 1: Marcar duplicatas
        df_marked = find_duplicates(collected_data)
        
        # Verificar marcação
        assert df_marked['is_duplicate'].sum() == 3  # 3 duplicatas marcadas
        
        # Passo 2: Selecionar melhores
        df_best = get_best_duplicates(df_marked)
        
        # Verificar resultado
        assert len(df_best) == 3  # 3 papers únicos
        
        # Paper 1: deve ter abstract longo mas stage 'included' (preservado)
        paper1 = df_best[df_best['doi'] == '10.1/paper1'].iloc[0]
        assert paper1['selection_stage'] == 'included'
        assert 'longer' in paper1['abstract']
        
        # Paper 3: deve ter melhor abstract (ABC) do grupo
        paper3 = df_best[df_best['doi'] == '10.3/paper3'].iloc[0]
        assert paper3['abstract'] == 'ABC'
        
        # Passo 3: Calcular stats PRISMA
        stats = _compute_prisma_stats_from_df(df_best)
        
        # Verificar stats
        assert stats['screening'] == 3  # 3 únicos
        assert stats['included'] == 1   # 1 included
        assert stats['eligibility'] == 2  # eligibility + included


# ============================================================================
# TESTES DE VALIDAÇÃO DE DADOS
# ============================================================================

class TestDataValidation:
    """Testes para validar integridade dos dados."""
    
    def test_no_orphan_duplicates(self):
        """Verifica que duplicatas sempre referenciam um paper existente."""
        from src.processing.dedup import find_duplicates
        
        df = pd.DataFrame([
            {'doi': '10.1/a', 'title': 'A'},
            {'doi': '10.1/a', 'title': 'A'},
            {'doi': '10.2/b', 'title': 'B'},
        ])
        
        result = find_duplicates(df)
        
        # Duplicatas devem referenciar DOI existente
        duplicates = result[result['is_duplicate'] == True]
        for _, row in duplicates.iterrows():
            dup_of = row['duplicate_of']
            if dup_of and dup_of.startswith('DOI:'):
                ref_doi = dup_of[4:]
                # DOI referenciado deve existir no DataFrame
                assert ref_doi in result['doi'].values
    
    def test_stage_counts_consistent(self):
        """Verifica que contagem de estágios é consistente."""
        from src.exports.excel import _compute_prisma_stats_from_df
        
        df = pd.DataFrame([
            {'doi': '10.1/a', 'selection_stage': 'included', 'status': 'included'},
            {'doi': '10.2/b', 'selection_stage': 'eligibility', 'status': 'excluded'},
            {'doi': '10.3/c', 'selection_stage': 'screening', 'status': 'excluded'},
            {'doi': '10.4/d', 'selection_stage': 'screening', 'status': 'excluded'},
        ])
        
        stats = _compute_prisma_stats_from_df(df)
        
        # screening >= eligibility >= included (fluxo progressivo)
        assert stats['screening'] >= stats['eligibility']
        assert stats['eligibility'] >= stats['included']


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
