from pathlib import Path

import pandas as pd
import pytest

from tcc_prototype.reporting.teacher_report import build_teacher_report


def _profiles() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "student_id": ["raw-student-1", "raw-student-1", "raw-student-2"],
            "skill_id": ["fractions", "ratio", "geometry"],
            "evidence_count": [5, 2, 7],
            "predicted_probability": [0.35, 0.75, 0.85],
            "prediction_std": [0.08, 0.04, 0.03],
            "observed_accuracy": [0.4, 1.0, 0.86],
            "observed_accuracy_lower": [0.12, 0.34, 0.49],
            "observed_accuracy_upper": [0.77, 1.0, 0.97],
            "evidence_status": [
                "estimated",
                "insufficient_evidence",
                "estimated",
            ],
            "level": [None, None, None],
            "threshold_version": [None, None, None],
            "interpretation_limit": ["not a diagnosis"] * 3,
        }
    )


def test_teacher_report_pseudonymizes_students_and_embeds_warnings(
    tmp_path: Path,
) -> None:
    output = tmp_path / "report.html"

    build_teacher_report(
        profiles=_profiles(),
        metrics={
            "split_strategy": "temporal",
            "seed": 2026,
            "models": {
                "random_forest": {"brier_score": 0.18, "log_loss": 0.55}
            },
        },
        importance=pd.DataFrame(
            {
                "feature": ["prior_student_skill_accuracy"],
                "importance_mean": [0.12],
                "importance_std": [0.01],
            }
        ),
        output_path=output,
        pseudonym_salt="test-salt",
        dataset_label="ASSISTments corrected test fixture",
        model_version="0.2.0",
    )

    html = output.read_text(encoding="utf-8")
    assert "raw-student-1" not in html
    assert "raw-student-2" not in html
    assert "Estudante-" in html
    assert "não constitui diagnóstico definitivo" in html
    assert "Evidência insuficiente" in html
    assert 'aria-label="Selecionar estudante"' in html
    assert "Exportar perfil selecionado" in html
    assert "ASSISTments corrected test fixture" in html


def test_teacher_report_escapes_embedded_json(tmp_path: Path) -> None:
    profiles = _profiles()
    profiles.loc[0, "skill_id"] = "</script><script>alert(1)</script>"
    output = tmp_path / "report.html"

    build_teacher_report(
        profiles=profiles,
        metrics={"models": {}},
        importance=pd.DataFrame(
            columns=["feature", "importance_mean", "importance_std"]
        ),
        output_path=output,
        pseudonym_salt="test-salt",
        dataset_label="fixture",
        model_version="test",
    )

    html = output.read_text(encoding="utf-8")
    assert "</script><script>alert(1)</script>" not in html
    assert "\\u003c/script\\u003e" in html


def test_teacher_report_rejects_missing_profile_columns(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="missing profile columns"):
        build_teacher_report(
            profiles=pd.DataFrame({"student_id": ["s1"]}),
            metrics={"models": {}},
            importance=pd.DataFrame(
                columns=["feature", "importance_mean", "importance_std"]
            ),
            output_path=tmp_path / "report.html",
            pseudonym_salt="salt",
            dataset_label="fixture",
            model_version="test",
        )
