"""Validate front-matter page references against a freshly compiled TCC PDF.

This is an artifact consistency check, not a scientific or ABNT certification.
The auxiliary directory must come from the same isolated build as the PDF.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader


def normalize(text: str) -> str:
    return "".join(character for character in unicodedata.normalize("NFD", text.casefold())
                   if character.isalnum())


def list_entries(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\\contentsline\s*\{[^}]+\}\{.*\}\{(\d+)\}\{([^}]+)\}", text)


def validate(pdf: Path, auxiliaries: Path) -> dict:
    reader = PdfReader(pdf)
    destinations = reader.named_destinations
    pages = [page.extract_text() or "" for page in reader.pages]
    intro_aux = (auxiliaries / "conteudo/introducao.aux").read_text(encoding="utf-8")
    intro_anchor = re.search(r"\\newlabel\{cap:introducao\}.*\{(chapter\.[^}]+)\}", intro_aux)
    if not intro_anchor or intro_anchor[1] not in destinations:
        raise ValueError("Missing introduction destination")
    start = reader.get_destination_page_number(destinations[intro_anchor[1]])
    front = normalize(" ".join(pages[:start]))
    for obsolete in ("Construção Ativa do Conhecimento", "Contribuições de Teorias de Aprendizagem",
                     "Critérios de Inclusão", "Critérios de Exclusão", "Recorte Temporal"):
        if normalize(obsolete) in front:
            raise ValueError(f"Obsolete front-matter entry: {obsolete}")
    for expected in ("Contribuições Pedagógicas para a Especificação", "Limitações e Contribuições da Revisão"):
        if normalize(expected) not in front:
            raise ValueError(f"Missing current TOC entry: {expected}")
    checked = []
    for suffix in ("toc", "lof", "loq", "lot"):
        entries = list_entries((auxiliaries / f"main.{suffix}").read_text(encoding="utf-8"))
        if not entries:
            raise ValueError(f"Empty front-matter file: {suffix}")
        for printed, anchor in entries:
            if anchor not in destinations:
                raise ValueError(f"Missing destination {anchor} from {suffix}")
            index = reader.get_destination_page_number(destinations[anchor])
            # The printed page number is a standalone line even on rotated pages.
            if not re.search(rf"(?m)^\s*{re.escape(printed)}\s*$", pages[index]):
                raise ValueError(f"{suffix}: {anchor} lists {printed}, but PDF page {index + 1} disagrees")
            checked.append({"list": suffix, "printed_page": int(printed), "physical_page": index + 1})
    if len(list_entries((auxiliaries / "main.loq").read_text(encoding="utf-8"))) != 5:
        raise ValueError("Expected five quadros: search, PICOS, synthesis, MMAT and PRISMA checklist")
    if not any(name.startswith("cite.") for name in destinations):
        raise ValueError("Missing citation destinations")
    return {"pages": len(pages), "checked_entries": len(checked), "front_matter": checked}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--aux", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(validate(args.pdf, args.aux), ensure_ascii=False))


if __name__ == "__main__":
    main()
