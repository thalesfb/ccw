"""Extract private manuscript feedback without treating annotations as instructions.

Sticky notes identify a position, not an exact quotation. Their associated
excerpt remains unset; the original page text supports subsequent human review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _annotation_record(annotation, page: int, index: int, source_hash: str) -> dict:
    """Preserve metadata; never infer the text targeted by a sticky note."""
    return {
        "annotation_id": f"PDF-{source_hash[:12]}-p{page:03d}-a{index:03d}",
        "page": page,
        "type": str(annotation.get("/Subtype", "Unknown")).lstrip("/"),
        "author": str(annotation.get("/T", "")),
        "contents": str(annotation.get("/Contents", "")),
        "rect": [float(value) for value in annotation.get("/Rect", [])],
        "quadpoints": [float(value) for value in annotation.get("/QuadPoints", [])],
        "created_at": str(annotation.get("/CreationDate", "")),
        "modified_at": str(annotation.get("/M", "")),
        "associated_excerpt": None,
        "association_status": "not_anchored",
        "source_sha256": source_hash,
    }


def extract_feedback(path: Path) -> dict:
    """Return stable page-level text and markup, excluding links and popups."""
    path = Path(path)
    source_hash = _sha256(path.read_bytes())
    reader = PdfReader(path)
    pages, annotations = [], []
    types = Counter()
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({
            "page": number,
            "text": text,
            "text_sha256": _sha256(text.encode("utf-8")),
            "text_integrity": "extracted" if text.strip() else "no_extractable_text",
        })
        for index, reference in enumerate(page.get("/Annots", []), start=1):
            annotation = reference.get_object()
            subtype = str(annotation.get("/Subtype", "Unknown"))
            types[subtype] += 1
            if subtype not in ("/Link", "/Popup", "/Widget"):
                annotations.append(_annotation_record(annotation, number, index, source_hash))
    return {
        "schema_version": 1,
        "source_name": path.name,
        "source_sha256": source_hash,
        "page_count": len(pages),
        "annotation_types": dict(types),
        "extraction_method": "pypdf",
        "pages": pages,
        "annotations": annotations,
    }


def extract_transcript(path: Path) -> dict:
    """Retain the entire available transcript with verifiable character offsets."""
    path = Path(path)
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    segments = []
    for match in re.finditer(r"[^\r\n]+(?:\r?\n[^\r\n]+)*", text):
        segment_text = match.group().strip()
        if not segment_text:
            continue
        start = match.start() + len(match.group()) - len(match.group().lstrip())
        segments.append({
            "segment_id": f"AUDIO-{len(segments) + 1:03d}",
            "char_start": start,
            "char_end": start + len(segment_text),
            "text": segment_text,
        })
    return {
        "schema_version": 1,
        "source_name": path.name,
        "source_sha256": _sha256(data),
        "original_text": text,
        "segments": segments,
        "audio_verification_status": "transcript_only_not_verified_against_audio",
    }


def render_comments(feedback: dict) -> str:
    """Render a local audit report with explicit limits on excerpt association."""
    lines = [
        "# Comentários do PDF — material privado",
        "",
        f"Fonte: {feedback['source_name']}",
        f"SHA-256: {feedback['source_sha256']}",
        f"Páginas físicas do PDF: {feedback['page_count']}",
        "",
        "As páginas são contadas a partir de 1, incluindo capa e pré-textuais. "
        "Notas adesivas não delimitam uma citação: as coordenadas e o texto da "
        "página foram preservados, mas o trecho associado não foi inventado.",
    ]
    for note in feedback["annotations"]:
        lines.extend([
            "", f"## {note['annotation_id']} — página {note['page']}", "",
            f"Tipo: {note['type']}; autor informado no PDF: {note['author']}",
            f"Coordenadas: {note['rect']}", "",
            *["> " + line for line in note["contents"].splitlines()],
        ])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[3] / "feedback/private")
    args = parser.parse_args()
    feedback = extract_feedback(args.pdf)
    transcript = extract_transcript(args.transcript)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, document in (("comentarios_pdf.json", feedback), ("audio_feedback.json", transcript)):
        (args.output / name).write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "comentarios_pdf.md").write_text(render_comments(feedback), encoding="utf-8")
    print(json.dumps({"pages": feedback["page_count"], "annotations": len(feedback["annotations"]),
                      "transcript_segments": len(transcript["segments"]), "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
