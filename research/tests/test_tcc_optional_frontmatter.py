from pathlib import Path

import pytest


TCC = Path(__file__).resolve().parents[2] / "results" / "tcc"
OPTIONAL_PAGES = ("dedicatoria", "agradecimentos", "epigrafe", "folhadeautorizacao")


@pytest.mark.parametrize("name", OPTIONAL_PAGES)
def test_optional_frontmatter_remains_available_for_author_editing(name: str) -> None:
    source = TCC / "pretextuais" / f"{name}.tex"

    assert source.is_file(), f"Preserve the editable optional template: {source.name}"
    assert source.read_text(encoding="utf-8").strip()


@pytest.mark.parametrize("name", OPTIONAL_PAGES)
def test_unfilled_optional_frontmatter_is_disabled_by_default(name: str) -> None:
    lines = (TCC / "main.tex").read_text(encoding="utf-8").splitlines()
    include = rf"\include{{pretextuais/{name}}}"

    assert any(line.lstrip().startswith("%") and include in line for line in lines)
    assert all(include not in line for line in lines if not line.lstrip().startswith("%"))


def test_optional_templates_do_not_publish_sample_personal_statements() -> None:
    for name in OPTIONAL_PAGES:
        source = (TCC / "pretextuais" / f"{name}.tex").read_text(encoding="utf-8")
        assert "Dedico este trabalho a..." not in source
        assert "Agradeço primeiramente..." not in source
        assert "Nelson Mandela" not in source
        assert "XXXXXXXXXXXXXX" not in source
