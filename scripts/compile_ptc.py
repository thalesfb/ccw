#!/usr/bin/env python
"""Automatiza a compilação multi-pass do documento LaTeX PTC.

Contexto: No PTC não há capítulo de conclusão. O script NÃO cria mais placeholder
nem exige flags para ignorar a conclusão. Basta remover ou comentar o include no main.tex.

Pipeline:
    pdflatex -> bibtex -> pdflatex -> pdflatex

Funções:
    - Limpeza opcional de artefatos (--clean)
    - Análise de log (citações/ref indefinidas, destinos duplicados)

Exit codes:
    0: sucesso
    1: citações ou referências indefinidas persistem
    2: destinos duplicados (se --halt-on-warn)
    3: main.tex ausente

Uso:
    python scripts/compile_ptc.py --root results/ptc [--clean] [--keep-log] [--halt-on-warn]
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

PDFLATEX_CMD = ["pdflatex", "-interaction=nonstopmode", "main.tex"]
BIBTEX_CMD = ["bibtex", "main"]
AUX_EXTS = {"aux","log","out","toc","bbl","blg","lof","lot","acn","acr","glsdefs","ist","idx","brf"}

UNDEFINED_CIT_RE = re.compile(r"Citation `([^']+)` undefined")
UNDEFINED_REF_RE = re.compile(r"Reference `([^']+)` undefined")
DUP_DEST_RE = re.compile(r"pdfTeX warning.*duplicate destination.*?\(([^)]+)\)")

def run(cmd: List[str], cwd: Path) -> Tuple[int,str]:
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out, _ = proc.communicate()
    return proc.returncode, out

def analyze_log(log_text: str) -> dict:
    undefined_cits = UNDEFINED_CIT_RE.findall(log_text)
    undefined_refs = UNDEFINED_REF_RE.findall(log_text)
    dup_dests = list(set(DUP_DEST_RE.findall(log_text)))
    return {
        "undefined_citations": sorted(set(undefined_cits)),
        "undefined_references": sorted(set(undefined_refs)),
        "duplicate_destinations": sorted(dup_dests),
    }

def clean_aux(root: Path) -> None:
    for ext in AUX_EXTS:
        for f in root.glob(f"*.{ext}"):
            if f.exists():
                try: f.unlink()
                except Exception: pass

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/ptc", help="Diretório contendo main.tex")
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--keep-log", action="store_true")
    ap.add_argument("--halt-on-warn", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    main_tex = root / "main.tex"
    if not main_tex.exists():
        print(json.dumps({"error":"main.tex não encontrado","path":str(main_tex)}))
        return 3

    all_logs = []
    steps = []
    # Pass 1
    code, out = run(PDFLATEX_CMD, root)
    all_logs.append(out)
    steps.append({"step":"pdflatex-1","returncode":code})
    # BibTeX (only if .aux produced)
    if (root / "main.aux").exists():
        code, out = run(BIBTEX_CMD, root)
        all_logs.append(out)
        steps.append({"step":"bibtex","returncode":code})
    # Pass 2 & 3
    for i in (2,3):
        code, out = run(PDFLATEX_CMD, root)
        all_logs.append(out)
        steps.append({"step":f"pdflatex-{i}","returncode":code})

    full_log = "\n".join(all_logs)
    analysis = analyze_log(full_log)

    log_file = root / "compile_ptc.log"
    if args.keep_log:
        log_file.write_text(full_log, encoding="utf-8")
    elif log_file.exists():
        try: log_file.unlink()
        except Exception: pass

    if args.clean:
        clean_aux(root)

    result = {
        "root": str(root),
        "steps": steps,
        "analysis": analysis,
        "pdf_exists": (root/"main.pdf").exists(),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    exit_code = 0
    if analysis["undefined_citations"] or analysis["undefined_references"]:
        exit_code = 1
    if args.halt_on_warn and analysis["duplicate_destinations"]:
        exit_code = max(exit_code, 2)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
