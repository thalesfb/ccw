"""Módulos para exportação de resultados."""

import re
from typing import Any, Dict, List

import pandas as pd

__all__ = [
    "excel",
    "reports",
    "redact_contact_emails",
    "redact_contact_emails_in_frame",
    "redact_contact_emails_in_records",
]

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
REDACTED_EMAIL = "[e-mail removido]"
# Identifier/link fields are never text-redacted.
_NON_TEXT_FIELDS = {"doi", "url", "open_access_pdf"}


def redact_contact_emails(text: Any) -> Any:
    """Replace e-mail addresses of third parties in a text value; other values pass through."""
    if not isinstance(text, str):
        return text
    return _EMAIL_RE.sub(REDACTED_EMAIL, text)


def redact_contact_emails_in_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``df`` with e-mail addresses redacted in text columns (rows and order unchanged)."""
    result = df.copy()
    for column in result.select_dtypes(include=["object", "string"]).columns:
        if column not in _NON_TEXT_FIELDS:
            result[column] = result[column].map(redact_contact_emails)
    return result


def redact_contact_emails_in_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return copies of JSON-like records with e-mail addresses redacted in text fields."""
    return [
        {
            key: value if key in _NON_TEXT_FIELDS else redact_contact_emails(value)
            for key, value in record.items()
        }
        for record in records
    ]
