from pathlib import Path
import re

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
        active = "\n".join(line.split("%", 1)[0] for line in source.splitlines())
        assert "Dedico este trabalho a..." not in active
        assert "Agradeço primeiramente..." not in active
        assert "Nelson Mandela" not in active
        assert "XXXXXXXXXXXXXX" not in source


def test_authorization_preserves_the_complete_editable_institutional_form() -> None:
    source = (TCC / "pretextuais/folhadeautorizacao.tex").read_text(encoding="utf-8")
    assert r"\begin{folhadeautorizacao}" in source
    assert r"\end{folhadeautorizacao}" in source
    for field in ("matrícula", "CPF:", "Assinatura:"):
        assert field in source
    assert "19 de Novembro de 2016" not in source
    assert not re.search(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", source)
    assert r"\rule" in source


@pytest.mark.parametrize("name,example", [
    ("dedicatoria", "Dedico este trabalho a..."),
    ("agradecimentos", "Agradeço primeiramente..."),
    ("epigrafe", "Nelson Mandela"),
])
def test_template_examples_are_preserved_only_as_editable_comments(name, example) -> None:
    source = (TCC / "pretextuais" / f"{name}.tex").read_text(encoding="utf-8")
    assert any(line.lstrip().startswith("%") and example in line for line in source.splitlines())
