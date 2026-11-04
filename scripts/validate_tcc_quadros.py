"""Check the declared quadro style and its PDF output; not a legibility certification."""
from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PT_TO_PDF = 72 / 72.27


def inventory(root: Path = ROOT) -> dict:
    return json.loads((root / "scripts/tcc_quadros.json").read_text(encoding="utf-8"))


def included_sources(root: Path) -> dict[str, str]:
    """Follow only the manuscript inputs, excluding commented-out templates."""
    pending = [root / "results/tcc/main.tex"]
    sources = {}
    while pending:
        path = pending.pop().resolve()
        relative = path.relative_to(root).as_posix()
        if relative in sources:
            continue
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text(encoding="utf-8"))
        sources[relative] = text
        for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
            child = root / "results/tcc" / name
            if child.suffix != ".tex":
                child = child.with_suffix(".tex")
            pending.append(child)
    return sources


def validate_sources(root: Path = ROOT) -> None:
    rows = inventory(root)["quadros"]
    sources = included_sources(root)
    calls = [(path, label) for path, text in sources.items()
             for label in re.findall(r"\\TCCQuadroSetup\{([^}]+)\}", text)]
    expected = [(row["source"], row["label"]) for row in rows]
    if sorted(calls) != sorted(expected) or len(rows) != 15:
        raise ValueError("The active manuscript must contain exactly the 15 inventoried quadro calls")
    count = sum(len(re.findall(r"\\begin\{(?:quadro|longtable)\}", text))
                for text in sources.values())
    if count != len(rows):
        raise ValueError("An active quadro/longtable is missing from the inventory")
    for row in rows:
        text = sources[row["source"]]
        start = text.index(r"\TCCQuadroSetup{" + row["label"] + "}")
        caption = text.index(r"\caption{", start)
        label = text.index(r"\label{" + row["label"] + "}", start)
        end = re.search(r"\\end\{(?:longtable|tabularx|tabular)\}", text[label:])
        if not end:
            raise ValueError(f"Missing body end: {row['label']}")
        body_end = label + end.end()
        source = text.find(r"\fonte{", body_end)
        next_caption = text.find(r"\caption{", body_end)
        if not start < caption < label < body_end < source or (0 <= next_caption < source):
            raise ValueError(f"Expected title/number, body, source: {row['label']}")
        body = text[start:body_end]
        if re.search(r"\\(?:fontsize|small|footnotesize|scriptsize|tiny|normalsize|large|Large|LARGE|huge|Huge|resizebox|scalebox)\b", body):
            raise ValueError(f"Local size or scaling overrides the shared style: {row['label']}")


def validate_style_log(log: str, policy: dict) -> None:
    rows = re.findall(r"TCCQUADRO\|([^|]+)\|size=([\d.]+)\|baseline=([\d.]+)pt", log)
    if [row[0] for row in rows] != [row["label"] for row in policy["quadros"]]:
        raise ValueError("Compiled quadro inventory/order differs from the declared manuscript")
    if any(float(size) != policy["body_pt"] or float(leading) != policy["baseline_pt"]
           for _, size, leading in rows):
        raise ValueError("Every compiled quadro must select 10 pt with 12 pt baseline")


def expected_size(actual: float, tex_points: float) -> bool:
    return abs(actual - tex_points * PT_TO_PDF) <= 0.12


def compact(text: str) -> str:
    return re.sub(r"[\W_]+", "", text.casefold())


def caption_texts(root: Path, policy: dict) -> dict[int, str]:
    sources = included_sources(root)
    result = {}
    for row in policy["quadros"]:
        text = sources[row["source"]]
        stop = text.index(r"\label{" + row["label"] + "}")
        start = text.rfind(r"\caption{", 0, stop)
        title = re.match(r"\\caption\{([^{}]+)\}", text[start:])[1]
        result[row["number"]] = f"Quadro {row['number']} – {title}"
    return result


def unscaled(cm, tm) -> bool:
    """Compose the linear text and graphics transforms; ignore translations."""
    a, b = tm[0] * cm[0] + tm[1] * cm[2], tm[0] * cm[1] + tm[1] * cm[3]
    c, d = tm[2] * cm[0] + tm[3] * cm[2], tm[2] * cm[1] + tm[3] * cm[3]
    return all(abs(value - target) <= .001
               for value, target in zip((a, b, c, d), (1, 0, 0, 1)))


def inspect_pdf(reader: PdfReader, first_page: int, policy: dict,
                captions: dict[int, str]) -> list[dict]:
    """Check font runs, wrapped/continued captions and complete source/notes blocks."""
    records = {}
    active = None
    caption_remaining = []
    body_started = source_started = False
    source_y = None
    source_page = None
    for index, page in enumerate(reader.pages):
        if source_started and source_page != index:
            active, source_started = None, False
        size = (float(page.mediabox.width), float(page.mediabox.height))
        rotated = int(page.get("/Rotate", 0)) % 180 != 0
        if abs(size[0] - 595.276) > 1 or abs(size[1] - 841.89) > 1:
            raise ValueError(f"PDF page {index + 1} is not A4")
        if rotated and not policy["landscape_allowlist"]:
            raise ValueError(f"Unapproved landscape page: {index + 1}")
        if index < first_page:
            continue

        def visit(text, cm, tm, font, font_size):
            nonlocal active, body_started, caption_remaining
            nonlocal source_started, source_y, source_page
            text = text.strip()
            if not text:
                return
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            caption = re.match(r"Quadro\s+(\d+)\s*[–-]", text)
            if source_started and not caption:
                # Source and note paragraphs are 10 pt. Normal prose resumes at
                # 12 pt after a vertical paragraph gap, not in a wrapped source line.
                if expected_size(font_size, 12) and source_y - y >= 18:
                    active, source_started = None, False
                else:
                    if not expected_size(font_size, policy["source_pt"]) or not unscaled(cm, tm):
                        raise ValueError(f"Quadro {active}: source/notes run has invalid typography")
                    records[active]["source_seen"] |= bool(compact(text).removeprefix("fonte"))
                    source_y = y
                    return
            if caption:
                number = int(caption[1])
                if number not in captions:
                    raise ValueError(f"Unexpected quadro number {number}")
                if active is not None and not source_started and active != number:
                    raise ValueError(f"Quadro {active}: missing source before the next quadro")
                active, body_started, source_started = number, False, False
                caption_remaining = [compact(captions[number]), compact(f"Quadro {number} – Continuação")]
                records.setdefault(number, {"number": number, "pages": set(), "body_runs": 0,
                                             "source_seen": False})
            if active is None:
                return
            record = records[active]
            record["pages"].add(index + 1)
            if not unscaled(cm, tm):
                raise ValueError(f"Quadro {active}: scaled PDF text")
            if rotated and policy["quadros"][active - 1]["label"] not in policy["landscape_allowlist"]:
                raise ValueError(f"Quadro {active}: landscape not allowlisted")
            if caption_remaining:
                fragment = compact(text)
                candidates = [tail[len(fragment):] for tail in caption_remaining if tail.startswith(fragment)]
                if not candidates or not expected_size(font_size, policy["caption_pt"]):
                    raise ValueError(f"Quadro {active}: caption content or typography differs")
                caption_remaining = [] if "" in candidates else candidates
                return
            if text.startswith("Fonte:"):
                if not body_started or not expected_size(font_size, policy["source_pt"]):
                    raise ValueError(f"Quadro {active}: missing body or source typography")
                source_started, source_page, source_y = True, index, y
                record["source_seen"] = bool(compact(text).removeprefix("fonte"))
                return
            if not expected_size(font_size, policy["body_pt"]):
                raise ValueError(f"Quadro {active}: body run {text[:45]!r} uses {font_size} PDF pt")
            body_started = True
            record["body_runs"] += 1

        page.extract_text(visitor_text=visit)
    if set(records) != set(range(1, 16)):
        raise ValueError("Not all fifteen quadro titles were found in the PDF")
    for row in records.values():
        if not row["source_seen"] or not row["body_runs"]:
            raise ValueError(f"Incomplete rendered quadro {row['number']}")
        row["pages"] = sorted(row["pages"])
    return [records[number] for number in sorted(records)]


def validate_bbox(path: Path, pages: set[int]) -> None:
    """Optional Poppler word bounds: catches margin overflow, not all clipping."""
    # Poppler can expose PDF control-code glyphs that XML 1.0 cannot represent.
    # Replace only those characters; coordinates remain untouched.
    xml = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "\ufffd", path.read_text(encoding="utf-8"))
    document = ET.fromstring(xml)
    rendered_pages = document.findall(".//{*}page")
    if not pages.issubset(set(range(1, len(rendered_pages) + 1))):
        raise ValueError("Missing quadro pages in the Poppler word-bounds document")
    for number, page in enumerate(rendered_pages, 1):
        if number not in pages:
            continue
        width, height = float(page.attrib["width"]), float(page.attrib["height"])
        for word in page.findall(".//{*}word"):
            left, right = float(word.attrib["xMin"]), float(word.attrib["xMax"])
            top, bottom = float(word.attrib["yMin"]), float(word.attrib["yMax"])
            if left < 30 / 25.4 * 72 - 2 or right > width - 20 / 25.4 * 72 + 2:
                raise ValueError(f"Page {number}: word exceeds horizontal text margins: {word.text}")
            if top < -1 or bottom > height + 1:
                raise ValueError(f"Page {number}: word exceeds paper bounds: {word.text}")


def validate(pdf: Path, auxiliaries: Path, log: Path, root: Path = ROOT,
             bbox: Path | None = None) -> dict:
    validate_sources(root)
    policy = inventory(root)
    validate_style_log(log.read_text(encoding="utf-8", errors="replace"), policy)
    reader = PdfReader(pdf)
    loq = (auxiliaries / "main.loq").read_text(encoding="utf-8")
    anchors = re.findall(r"\\contentsline\s*\{[^}]+\}\{.*\}\{(\d+)\}\{([^}]+)\}", loq)
    if len(anchors) != 15:
        raise ValueError("The list of quadros must contain exactly fifteen entries")
    first_page = reader.get_destination_page_number(reader.named_destinations[anchors[0][1]])
    rows = inspect_pdf(reader, first_page, policy, caption_texts(root, policy))
    if bbox:
        validate_bbox(bbox, {page for row in rows for page in row["pages"]})
    return {"quadros": rows, "body_pt": policy["body_pt"],
            "baseline_pt": policy["baseline_pt"], "landscape_allowlist": policy["landscape_allowlist"],
            "word_bounds_checked": bbox is not None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--aux", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--bbox", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.pdf, args.aux, args.log, bbox=args.bbox), ensure_ascii=False))


if __name__ == "__main__":
    main()
