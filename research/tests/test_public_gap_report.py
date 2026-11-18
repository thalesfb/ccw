from pathlib import Path

import pandas as pd

from research.src.analysis.reports import ReportGenerator, _normalise_external_url


def test_report_url_normalization_only_keeps_http_and_https() -> None:
    assert _normalise_external_url("10.1234/example.paper") == "https://doi.org/10.1234/example.paper"
    assert _normalise_external_url("https://example.org/paper?a=1&b=2") == "https://example.org/paper?a=1&b=2"
    assert _normalise_external_url("http://example.org/paper") == "http://example.org/paper"
    assert _normalise_external_url("javascript:alert(1)") == ""
    assert _normalise_external_url("//example.org/paper") == ""
    assert _normalise_external_url("https://example.org@attacker.invalid/paper") == ""
    assert _normalise_external_url("https://example.org:invalid/paper") == ""
    assert _normalise_external_url("https://example.org/\nheader") == ""


def test_public_papers_report_escapes_record_text_and_rejects_active_url(tmp_path: Path) -> None:
    generator = ReportGenerator(output_dir=tmp_path / "reports")
    report_path = generator.generate_papers_report(
        pd.DataFrame(
            [
                {
                    "title": "Study <script>alert(1)</script>",
                    "authors": "<img src=x onerror=alert(1)>",
                    "abstract": "<svg onload=alert(1)>",
                    "url": "javascript:alert(1)",
                    "selection_stage": "included",
                }
            ]
        )
    )

    html = report_path.read_text(encoding="utf-8")
    assert "Study &lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html
    assert "&lt;svg onload=alert(1)&gt;" in html
    assert "href=\"javascript:" not in html
    assert "<script>alert(1)</script>" not in html


def test_gap_report_describes_heuristics_without_claiming_literature_gaps(tmp_path: Path) -> None:
    records = pd.DataFrame(
        {
            "year": [2015, *([2016] * 9)],
            "study_type": ["experimental", *([None] * 9)],
            "comp_techniques": [None] * 10,
        }
    )
    generator = ReportGenerator(output_dir=tmp_path / "reports")

    gaps = generator._identify_research_gaps(records)
    html = generator._create_gap_analysis_html(gaps, record_count=len(records))

    assert any("2015: 1 registro no export" in item and "(5,0)" in item for item in gaps["temporal_gaps"])
    assert any(
        "A etiqueta operacional “experimental” aparece em 1 de 10 registros" in item
        and "frequência fica abaixo do limite descritivo de 30%" in item
        and "não avalia rigor metodológico" in item
        for item in gaps["methodological_gaps"]
    )
    assert any(
        "Nenhum dos 10 registros recebeu a etiqueta operacional “longitudinal”" in item
        and "9 registros não têm tipo preenchido" in item
        and "não demonstra ausência de estudos longitudinais" in item
        for item in gaps["methodological_gaps"]
    )
    assert "A distribuição geográfica não é calculada" in gaps["geographical_gaps"][0]
    assert "10 registros" in html
    assert "não integram as conclusões do TCC" in html
    assert "não comprova baixa produção na literatura" in html
    assert "Nenhuma lacuna significativa identificada" not in html
    assert "Poucos estudos experimentais rigorosos" not in html
    assert "Recomendações para Pesquisas Futuras" not in html
