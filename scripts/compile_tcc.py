"""Compile the TCC in a fresh source tree, never mixing include auxiliaries.

Requires pdflatex and BibTeX. Local scratch files are preserved; only the
requested output PDF and its diagnostic log are replaced after a valid build.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_EXTENSIONS = {".tex", ".bib", ".cls", ".sty", ".bst", ".png", ".jpg", ".jpeg", ".pdf", ".eps"}
AUX_EXTENSIONS = {".aux", ".toc", ".lof", ".lot", ".loq", ".out", ".brf", ".bbl"}


def stage_sources(root: Path, stage: Path) -> Path:
    """Copy only document inputs, including generated reference tables."""
    target = stage / "results/tcc"
    for relative in ("results/tcc", "research/exports/references"):
        source = root / relative
        for path in source.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in SOURCE_EXTENSIONS:
                continue
            if relative == "results/tcc" and path.relative_to(source).parts[0] == "abntex2":
                continue  # Never copy a stale developer-generated alias.
            if path.name == "main.pdf":
                continue
            destination = stage / path.relative_to(root)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
    # The historical checkout spells this directory abnetx2; the class loads abntex2.
    shutil.copytree(target / "abnetx2", target / "abntex2")
    return target


def aux_fingerprint(directory: Path) -> str:
    """Include chapter auxiliaries and all front-matter lists in convergence."""
    digest = hashlib.sha256()
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix in AUX_EXTENSIONS:
            digest.update(path.relative_to(directory).as_posix().encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_log(log: str) -> None:
    if re.search(r"undefined (?:references|citations)|(?:Citation|Reference) .+ undefined|"
                 r"Rerun to get|Label\(s\) may have changed|rerunfilecheck Warning", log, re.I):
        raise RuntimeError("TCC build still has unresolved references or a rerun request")


def compile_document(root: Path, output: Path, diagnostics: Path | None = None) -> None:
    engine_version = subprocess.run(["pdflatex", "--version"], capture_output=True,
                                    text=True, check=True).stdout
    command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape"]
    if "miktex" in engine_version.lower():
        command.append("-disable-installer")
    command.append("main.tex")
    env = dict(os.environ)
    # Do not allow external source-search overrides to supply stale auxiliaries.
    env.pop("TEXINPUTS", None)
    with tempfile.TemporaryDirectory(prefix="ccw-tcc-") as temporary:
        directory = stage_sources(root, Path(temporary))
        transcript: list[str] = []

        def run(arguments: list[str]) -> None:
            process = subprocess.run(arguments, cwd=directory, env=env,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     text=True, encoding="utf-8", errors="replace")
            transcript.append(process.stdout)
            if process.returncode:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.with_suffix(".log").write_text("\n".join(transcript), encoding="utf-8")
                raise RuntimeError(f"{arguments[0]} failed ({process.returncode}):\n{process.stdout[-6000:]}")

        run(command)
        run(["bibtex", "main"])
        previous = aux_fingerprint(directory)
        for _ in range(8):
            run(command)
            # Back-reference and bibliography options are themselves written to
            # auxiliaries; regenerate BibTeX while the complete tree converges.
            run(["bibtex", "main"])
            current = aux_fingerprint(directory)
            if current == previous:
                output.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(directory / "main.log", output.with_suffix(".log"))
                try:
                    validate_log((directory / "main.log").read_text(encoding="utf-8", errors="replace"))
                except RuntimeError:
                    continue
                else:
                    break
            previous = current
        else:
            raise RuntimeError("TCC auxiliaries did not converge after eight additional passes")
        pdf = directory / "main.pdf"
        if not pdf.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError("The compiler did not produce a PDF")
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pdf, output)
        shutil.copyfile(directory / "main.log", output.with_suffix(".log"))
        if diagnostics:
            diagnostics.mkdir(parents=True, exist_ok=True)
            for path in directory.rglob("*"):
                if path.is_file() and path.suffix in AUX_EXTENSIONS:
                    destination = diagnostics / path.relative_to(directory)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, destination)
        print(f"Converged TCC PDF: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "results/tcc/main.pdf")
    parser.add_argument("--diagnostics", type=Path)
    args = parser.parse_args()
    compile_document(args.root.resolve(), args.output.resolve(), args.diagnostics)


if __name__ == "__main__":
    main()
