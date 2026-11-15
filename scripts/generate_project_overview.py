"""Generate the README overview from the current public TCC records."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("results/tcc/images/project_overview_2026-11-15.png")
SELECTION = Path("research/data/selection_status_current.json")
MMAT = Path("research/data/mmat_reassessment_current.csv")
STATUS = Path("docs/tcc/ESTADO-ATUAL-TCC.md")
REQUIREMENTS = Path("results/tcc/conteudo/rastreabilidade-requisitos.tex")
PROTOTYPE = Path("results/tcc/conteudo/prototipo.tex")
CONCLUSION = Path("results/tcc/conteudo/conclusao.tex")
VALID_RESPONSES = {"Y", "N", "CT"}
WORD_NUMBERS = {"one": 1, "two": 2, "three": 3}


def fmt(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def facts(root: Path = ROOT) -> dict[str, object]:
    selection = json.loads((root / SELECTION).read_text(encoding="utf-8"))
    flow = selection["data_reconciliation"]["corrected_prisma_flow"]
    if selection["status"] != "historical_snapshot_unchanged":
        raise ValueError("the overview expects the current historical selection snapshot")

    retrieval = selection["prisma_reporting"]
    retrieval_match = re.search(
        r"(?P<sought>\d+) reports sought, (?P<missing>one|two|three) "
        r"without a verifiable copy \((?P<missing_names>[^)]+)\), "
        r"(?P<assessed>\d+) assessed at full text, "
        r"(?P<protocol>one|two|three) protocol excluded, and "
        r"(?P<recovered>\d+) recovered empirical reports",
        retrieval,
    )
    if not retrieval_match:
        raise ValueError("cannot parse the public source-retrieval summary")
    retrieval_facts = retrieval_match.groupdict()
    retrieval_numbers = {
        key: WORD_NUMBERS.get(value, int(value) if value.isdigit() else -1)
        for key, value in retrieval_facts.items()
        if key in {"sought", "missing", "assessed", "protocol", "recovered"}
    }
    missing_names = [name.strip() for name in retrieval_facts["missing_names"].split("and")]
    if not {"Sokkhey", "Zeng"}.issubset(set(missing_names)):
        raise ValueError("the retrieval summary no longer identifies Sokkhey and Zeng")

    with (root / MMAT).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    criteria = ("s1", "s2", "q1", "q2", "q3", "q4", "q5")
    appraised = [row for row in rows if any(row[field] in VALID_RESPONSES for field in criteria)]
    response_count = sum(
        row[field] in VALID_RESPONSES for row in appraised for field in criteria
    )
    if len(appraised) != 14 or response_count != 98:
        raise ValueError(
            "current MMAT counts changed; review the overview before regenerating "
            f"(studies={len(appraised)}, responses={response_count})"
        )
    if any(sum(row[field] in VALID_RESPONSES for field in criteria) != 7 for row in appraised):
        raise ValueError("an MMAT row has an incomplete criterion set")

    status_text = " ".join((root / STATUS).read_text(encoding="utf-8").split())
    conference_match = re.search(
        r"Em (?P<day>\d{2}/\d{2}/\d{4}), o autor conferiu (?P<responses>\d+) "
        r"respostas dos (?P<studies>\d+) estudos com texto recuperado contra as "
        r"evidências localizadas: (?P<retained>\d+) foram mantidas e "
        r"(?P<changed>\d+) alteradas",
        status_text,
    )
    if not conference_match:
        raise ValueError("cannot locate the current MMAT conference note")
    conference = conference_match.groupdict()
    if int(conference["responses"]) != response_count or int(conference["studies"]) != len(appraised):
        raise ValueError("the MMAT conference note and current ledger disagree")
    if int(conference["retained"]) + int(conference["changed"]) != response_count:
        raise ValueError("the MMAT conference totals do not add up")

    requirements_text = (root / REQUIREMENTS).read_text(encoding="utf-8")
    requirement_groups = sorted(set(re.findall(r"^R(\d{2})\s*&", requirements_text, re.M)))
    if len(requirement_groups) != 26:
        raise ValueError(f"expected 26 requirement groups, found {len(requirement_groups)}")
    prototype_text = " ".join((root / PROTOTYPE).read_text(encoding="utf-8").split())
    conclusion_text = " ".join((root / CONCLUSION).read_text(encoding="utf-8").split())
    if "O procedimento de revisão docente não foi executado" not in prototype_text:
        raise ValueError("the manuscript no longer confirms that the teacher review was not applied")
    if "sem a realização de ensaios empíricos em escolas" not in conclusion_text:
        raise ValueError("the manuscript no longer supports the school-validation limit")

    return {
        "identified": flow["identification"],
        "duplicates": flow["duplicates_removed"],
        "screened": flow["screening"],
        "screening_excluded": flow["screening_excluded"],
        "prioritization": flow["prioritization"],
        "prioritization_excluded": flow["prioritization_excluded"],
        "shortlisted": flow["shortlisted"],
        "historical_included": flow["included"],
        "reports_sought": retrieval_numbers["sought"],
        "not_retrieved": retrieval_numbers["missing"],
        "reports_assessed": retrieval_numbers["assessed"],
        "protocol_excluded": retrieval_numbers["protocol"],
        "empirical_reports": retrieval_numbers["recovered"],
        "appraised_studies": len(appraised),
        "mmat_responses": response_count,
        "mmat_retained": int(conference["retained"]),
        "mmat_changed": int(conference["changed"]),
        "conference_date": conference["day"],
        "requirement_groups": len(requirement_groups),
        "cutoff": selection["current_relevance_threshold"],
    }


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf")
        if bold
        else (r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\segoeui.ttf")
    )
    linux_candidates = (
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        if bold
        else ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",)
    )
    for candidate in (*candidates, *linux_candidates):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    raise FileNotFoundError("Arial or DejaVu Sans is required to render the overview")


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, selected_font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}".strip()
            if line and draw.textbbox((0, 0), candidate, font=selected_font)[2] > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines


def paragraph(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    width: int,
    selected_font: ImageFont.FreeTypeFont,
    fill: str,
    line_gap: int = 7,
) -> int:
    x, y = xy
    for line in wrap_lines(draw, text, selected_font, width):
        draw.text((x, y), line, font=selected_font, fill=fill)
        box = draw.textbbox((x, y), line, font=selected_font)
        y += box[3] - box[1] + line_gap
    return y


def draw_tile(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    value: str,
    label: str,
    accent: str,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, fill="#13283a", outline="#29495d", width=2)
    draw.text((x1 + 20, y1 + 12), value, font=font(43, True), fill=accent)
    paragraph(draw, label, (x1 + 22, y1 + 67), x2 - x1 - 44, font(19), "#e4edf4", 3)


def render(data: dict[str, object]) -> bytes:
    image = Image.new("RGB", (1800, 1080), "#091725")
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((44, 38, 1756, 164), radius=28, fill="#10283b", outline="#1e5268", width=2)
    draw.text((78, 56), "Ensino Personalizado de Matemática", font=font(50, True), fill="#f4f8fb")
    draw.text((82, 119), "Revisão sistemática e especificação conceitual", font=font(24), fill="#7fe1ee")

    left = (54, 198, 888, 925)
    right_top = (916, 198, 1746, 555)
    right_bottom = (916, 580, 1746, 925)
    for box in (left, right_top, right_bottom):
        draw.rounded_rectangle(box, radius=26, fill="#0f2233", outline="#26455a", width=2)

    draw.text((86, 225), "REVISÃO DA LITERATURA", font=font(25, True), fill="#64d8ec")
    tile_x = (88, 484)
    tile_y = (276, 414)
    tile_specs = [
        (fmt(data["identified"]), "registros identificados", "#42d8ef"),
        (fmt(data["screened"]), f"únicos na triagem · {fmt(data['duplicates'])} duplicatas", "#71dfcb"),
        (fmt(data["prioritization"]), "avançaram à priorização", "#8fe68e"),
        (fmt(data["shortlisted"]), "na lista preliminar", "#ffd16a"),
    ]
    for index, (value, label, accent) in enumerate(tile_specs):
        x = tile_x[index % 2]
        y = tile_y[index // 2]
        draw_tile(draw, (x, y, x + 360, y + 120), value, label, accent)

    y = 565
    y = paragraph(draw, f"Triagem: {fmt(data['screening_excluded'])} registros excluídos.", (88, y), 740, font(21), "#e4edf4", 8)
    y = paragraph(draw, f"Priorização: {fmt(data['prioritization_excluded'])} não avançaram sob a regra histórica; o corte {data['cutoff']:.1f} foi mantido.", (88, y), 740, font(21), "#e4edf4", 8)
    y = paragraph(
        draw,
        f"Texto integral: {data['reports_sought']} relatórios procurados; {data['not_retrieved']} sem cópia verificável; {data['reports_assessed']} avaliados; {data['protocol_excluded']} protocolo excluído; {data['empirical_reports']} relatórios empíricos recuperados.",
        (88, y), 740, font(19), "#c7d6e2", 7,
    )
    y += 5
    paragraph(
        draw,
        f"Seleção histórica: {data['historical_included']} estudos, incluindo Sokkhey sem cópia verificável; Zeng está fora da seleção.",
        (88, y), 740, font(19, True), "#f3c76b", 6,
    )

    draw.text((950, 225), "APRECIAÇÃO METODOLÓGICA · MMAT 2018", font=font(24, True), fill="#c69aff")
    draw.text((960, 280), str(data["appraised_studies"]), font=font(65, True), fill="#d4b2ff")
    paragraph(draw, "estudos com texto recuperado e respostas atuais", (1065, 298), 610, font(23, True), "#f3f5f8", 4)
    draw.line((960, 376, 1702, 376), fill="#334f64", width=2)
    draw.text((960, 395), str(data["mmat_responses"]), font=font(42, True), fill="#64d8ec")
    paragraph(draw, f"respostas conferidas em {data['conference_date']}", (1060, 408), 610, font(20), "#e4edf4", 4)
    paragraph(
        draw,
        f"{data['mmat_retained']} mantidas · {data['mmat_changed']} alteradas · sem escore agregado. Sokkhey mantém respostas históricas não revalidadas.",
        (960, 466), 735, font(18), "#c7d6e2", 5,
    )

    draw.text((950, 607), "ESPECIFICAÇÃO CONCEITUAL", font=font(25, True), fill="#71dfcb")
    draw.text((960, 660), str(data["requirement_groups"]), font=font(54, True), fill="#71dfcb")
    paragraph(draw, "grupos de requisitos", (1058, 678), 600, font(24, True), "#f3f5f8", 4)
    paragraph(
        draw,
        "Arquitetura de referência e cenários de aceitação compõem o produto documental.",
        (960, 747), 730, font(21), "#e4edf4", 7,
    )
    paragraph(
        draw,
        "O protocolo de avaliação docente foi proposto, mas não aplicado. Esta versão não demonstra eficácia educacional nem validação em escola.",
        (960, 820), 730, font(19), "#c7d6e2", 6,
    )

    draw.rounded_rectangle((54, 955, 1746, 1032), radius=18, fill="#12273a", outline="#26455a", width=2)
    draw.text((82, 978), "Síntese visual de dados versionados. Não substitui o TCC nem certifica qualidade metodológica ou eficácia.", font=font(21), fill="#b7c9d7")

    from io import BytesIO

    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if the PNG is stale")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    target = args.root / OUTPUT
    try:
        rendered = render(facts(args.root))
        if args.check:
            if not target.exists() or target.read_bytes() != rendered:
                print(f"Overview image is missing or stale: {OUTPUT}", file=sys.stderr)
                return 1
            print(f"Overview image is current: {OUTPUT}")
            return 0
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(rendered)
        print(f"Generated {OUTPUT}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Project overview generation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
