#!/usr/bin/env python3
"""Print the README's file table from sha256sums.txt, fetch.log and the abs pages (so no hash is typed by hand)."""
import re, sys
from pathlib import Path
H = Path(__file__).resolve().parent
sha = {}
for line in (H / "sha256sums.txt").read_text().splitlines():
    h, n = line.split(None, 1)
    sha[n.strip()] = h
tex = {"2301.05243v1": "sr_ellis.tex", "2301.05243v2": "paper8.tex"}
abbr = lambda h: h[:8] + "…" + h[-4:]
print("| paper, version | e-print | TeX (committed) | PDF | PDF pages |")
print("|---|---|---|---|---|")
import subprocess
for d in sorted((H / "dl").glob("[0-9]*v[0-9]")):
    n = d.name
    t = tex.get(n, "main.tex")
    pages = [l for l in subprocess.run(["pdfinfo", str(d / "pdf")], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")][0].split()[-1]
    print(f"| arXiv:{n} | `dl/{n}/eprint` {abbr(sha[f'dl/{n}/eprint'])} | `src/{n}/{t}` {abbr(sha[f'src/{n}/{t}'])} | `dl/{n}/pdf` {abbr(sha[f'dl/{n}/pdf'])} | {pages} |")
