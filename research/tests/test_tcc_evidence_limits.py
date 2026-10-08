"""Guard explicit inference boundaries, not scientific truth by string matching."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_prediction_is_not_an_unvalidated_proficiency_scale():
    text = (ROOT / 'results/tcc/conteudo/prototipo.tex').read_text(encoding='utf-8')
    assert 'estimativas de proficiência acompanhadas' not in text
    assert 'modelo de mensuração' in text
    assert 'probabilidade preditiva' in text
    assert 'escala' in text


def test_he_synthesis_distinguishes_the_components_of_the_primary_study():
    text = (ROOT / 'results/tcc/conteudo/resultadosesperados.tex').read_text(encoding='utf-8')
    row = text.split(r'\citeonline{He2025_6915}', 1)[1].split(r'\\', 1)[0]
    assert 'tamanhos de efeito' in row
    assert 'O resumo reporta' not in row
    assert '423' in text
    assert 'professores' in text


def test_normative_baseline_includes_the_corrected_14724_version():
    text = (ROOT / 'docs/tcc/ABNT-2025-CORRECOES.md').read_text(encoding='utf-8')
    assert '14724:2024' in text
    assert '01.04.2025' in text
    assert 'não declara conformidade integral' in text


def test_prisma_support_declaration_is_generic_and_locatable():
    methodology = (ROOT / 'results/tcc/conteudo/metodologia.tex').read_text(encoding='utf-8')
    assert 'recursos próprios, sem financiamento externo' in methodology
    assert r'\label{sec:apoio-pesquisa}' in methodology
    appendix = (ROOT / 'results/tcc/postextuais/apendice.tex').read_text(encoding='utf-8')
    support_row = next(line for line in appendix.splitlines() if line.startswith('25 &'))
    assert 'Localizado' in support_row
    assert r'\ref{sec:apoio-pesquisa}' in support_row
    assert 'Não apresentado' not in support_row
    assert 'ChatGPT' not in methodology
