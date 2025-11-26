"""
Testes para preservação de selection_stage durante deduplicação.

Valida que a lógica de _select_best_duplicate preserva o stage mais alto
do registro original quando o duplicate vencedor tem qualidade melhor mas
stage inferior.
"""
import pytest
import pandas as pd


def test_preserve_stage_when_duplicate_has_better_quality():
    """
    Cenário: Duplicate tem abstract mais longo e mais citações, mas original
    está em stage 'included'. O duplicate vencedor deve herdar stage 'included'.
    """
    # Import aqui para evitar problemas de importação circular
    from src.exports.excel import _select_best_duplicate
    
    group = pd.DataFrame([
        {
            'doi': '10.1234/test',
            'title': 'Test Paper',
            'abstract': 'Short abstract',  # 15 chars
            'citation_count': 10,
            'open_access_pdf': None,
            'selection_stage': 'included',
            'status': 'accepted',
            'is_duplicate': False  # Original
        },
        {
            'doi': '10.1234/test',
            'title': 'Test Paper',
            'abstract': 'Much longer and more detailed abstract with more information',  # 61 chars
            'citation_count': 50,
            'open_access_pdf': 'https://example.com/paper.pdf',
            'selection_stage': 'screening',
            'status': 'pending',
            'is_duplicate': True  # Duplicate com qualidade superior
        }
    ])
    
    # Executar seleção com preservação de stage (default)
    best = _select_best_duplicate(group, preserve_stage=True)
    
    # Validações:
    # 1. Duplicate deve vencer por qualidade (abstract + citations + PDF)
    assert best['abstract'] == 'Much longer and more detailed abstract with more information'
    assert best['citation_count'] == 50
    assert best['open_access_pdf'] == 'https://example.com/paper.pdf'
    
    # 2. Stage do original deve ser preservado
    assert best['selection_stage'] == 'included', \
        "Stage 'included' do original deveria ser preservado no duplicate vencedor"
    assert best['status'] == 'accepted', \
        "Status do original deveria ser preservado junto com stage"


def test_no_stage_preservation_when_disabled():
    """
    Cenário: Com preserve_stage=False, duplicate vencedor mantém seu próprio stage.
    """
    from src.exports.excel import _select_best_duplicate
    
    group = pd.DataFrame([
        {
            'doi': '10.1234/test',
            'abstract': 'Short',
            'citation_count': 10,
            'selection_stage': 'included',
            'is_duplicate': False
        },
        {
            'doi': '10.1234/test',
            'abstract': 'Very long detailed abstract',
            'citation_count': 50,
            'selection_stage': 'screening',
            'is_duplicate': True
        }
    ])
    
    best = _select_best_duplicate(group, preserve_stage=False)
    
    # Sem preservação, stage deve ser do duplicate vencedor
    assert best['selection_stage'] == 'screening'


def test_stage_hierarchy_included_over_eligibility():
    """
    Cenário: Original 'included' vs duplicate 'eligibility' - preservar 'included'.
    """
    from src.exports.excel import _select_best_duplicate
    
    group = pd.DataFrame([
        {
            'doi': '10.1234/test',
            'abstract': 'Short',
            'selection_stage': 'included',
            'is_duplicate': False
        },
        {
            'doi': '10.1234/test',
            'abstract': 'Much longer abstract text',
            'selection_stage': 'eligibility',
            'is_duplicate': True
        }
    ])
    
    best = _select_best_duplicate(group, preserve_stage=True)
    assert best['selection_stage'] == 'included'


def test_stage_hierarchy_eligibility_over_screening():
    """
    Cenário: Original 'eligibility' vs duplicate 'screening' - preservar 'eligibility'.
    """
    from src.exports.excel import _select_best_duplicate
    
    group = pd.DataFrame([
        {
            'doi': '10.1234/test',
            'abstract': 'Short',
            'selection_stage': 'eligibility',
            'is_duplicate': False
        },
        {
            'doi': '10.1234/test',
            'abstract': 'Much longer abstract text',
            'selection_stage': 'screening',
            'is_duplicate': True
        }
    ])
    
    best = _select_best_duplicate(group, preserve_stage=True)
    assert best['selection_stage'] == 'eligibility'


def test_no_preservation_when_duplicate_has_higher_stage():
    """
    Cenário: Duplicate tem stage mais alto que original - não preservar (manter duplicate).
    """
    from src.exports.excel import _select_best_duplicate
    
    group = pd.DataFrame([
        {
            'doi': '10.1234/test',
            'abstract': 'Short',
            'selection_stage': 'screening',
            'is_duplicate': False
        },
        {
            'doi': '10.1234/test',
            'abstract': 'Much longer abstract text',
            'selection_stage': 'included',
            'is_duplicate': True
        }
    ])
    
    best = _select_best_duplicate(group, preserve_stage=True)
    # Duplicate já tem stage mais alto, manter seu próprio
    assert best['selection_stage'] == 'included'


def test_get_best_duplicates_preserves_included_papers():
    """
    Teste de integração: get_best_duplicates não deve perder papers 'included'.
    """
    from src.exports.excel import get_best_duplicates
    
    # Import find_duplicates inline to avoid import issues
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
    from processing.dedup import find_duplicates
    
    # Create test data WITHOUT manual duplicate flags (pipeline marks them)
    df = pd.DataFrame([
        # Grupo 1: Original included, duplicate screening com qualidade superior
        {
            'doi': '10.1111/paper1',
            'title': 'Paper 1',
            'abstract': 'Short',
            'citation_count': 5,
            'selection_stage': 'included'
        },
        {
            'doi': '10.1111/paper1',
            'title': 'Paper 1',
            'abstract': 'Very long detailed abstract with lots of information',
            'citation_count': 100,
            'selection_stage': 'screening'
        },
        # Grupo 2: Original screening, duplicate screening (sem preservação necessária)
        {
            'doi': '10.2222/paper2',
            'title': 'Paper 2',
            'abstract': 'Medium length',
            'citation_count': 10,
            'selection_stage': 'screening'
        },
        {
            'doi': '10.2222/paper2',
            'title': 'Paper 2',
            'abstract': 'Longer abstract',
            'citation_count': 20,
            'selection_stage': 'screening'
        },
        # Paper único (não duplicado)
        {
            'doi': '10.3333/paper3',
            'title': 'Paper 3',
            'abstract': 'Unique paper',
            'citation_count': 15,
            'selection_stage': 'eligibility'
        }
    ])

    # Mark duplicates like pipeline does
    df_marked = find_duplicates(df)

    # Now select best duplicates
    result = get_best_duplicates(df_marked)
    
    # Validações:
    # 1. Total deve ser 3 papers únicos
    assert len(result) == 3
    
    # 2. Paper 1 deve estar com stage 'included' (preservado do original)
    paper1 = result[result['doi'] == '10.1111/paper1'].iloc[0]
    assert paper1['selection_stage'] == 'included', \
        "Paper 1 deveria ter stage 'included' preservado do original"
    
    # 3. Paper 1 deve ter abstract longo do duplicate (qualidade venceu)
    assert 'Very long detailed abstract' in paper1['abstract']
    
    # 4. Contagem de stages deve estar correta
    stage_counts = result['selection_stage'].value_counts()
    assert stage_counts.get('included', 0) == 1, "Deve ter exatamente 1 paper 'included'"
    assert stage_counts.get('eligibility', 0) == 1, "Deve ter exatamente 1 paper 'eligibility'"
    assert stage_counts.get('screening', 0) == 1, "Deve ter exatamente 1 paper 'screening'"


def test_audit_logging_captures_stage_loss(caplog):
    """
    Verifica que audit logs alertam quando papers included/eligibility são removidos.
    """
    from src.exports.excel import get_best_duplicates
    import logging
    caplog.set_level(logging.WARNING)
    
    df = pd.DataFrame([
        {
            'doi': '10.1111/test',
            'abstract': 'Short',
            'selection_stage': 'included',
            'is_duplicate': False,
            'duplicate_of': None
        },
        {
            'doi': '10.1111/test',
            'abstract': 'Longer abstract',
            'selection_stage': 'screening',
            'is_duplicate': True,
            'duplicate_of': '10.1111/test'
        }
    ])
    
    result = get_best_duplicates(df)
    
    # Com preservação correta, NÃO deve haver warning
    # (porque stage 'included' foi preservado)
    warning_msgs = [r.message for r in caplog.records if r.levelname == 'WARNING']
    stage_loss_warnings = [m for m in warning_msgs if 'papers' in m and 'deduplicação' in m]
    
    # Se a lógica estiver correta, não deve remover nenhum paper 'included'
    assert len(stage_loss_warnings) == 0, \
        "Não deveria haver warnings de perda de stage se preservação funcionou"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
