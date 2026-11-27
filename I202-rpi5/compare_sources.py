#!/usr/bin/env python3
"""Compares the three readings of TS13's Table I: (1) ts13_table_I.txt (typed from the page image), (2) the PDF text layer
(pdftotext -layout), (3) the TeX source. Run from this folder: python3 -I compare_sources.py. Exit 1 on any difference."""
import re
import subprocess
import sys

R1 = {}
for line in open("ts13_table_I.txt", encoding="utf8"):
    m = re.match(r"^\s{2}(\d+)\s+[−-]\s?(\d+\.\d+)\s*$", line)
    if m:
        R1[int(m.group(1))] = "-" + m.group(2)
txt = subprocess.run(["pdftotext", "-layout", "-f", "5", "-l", "5", "ts13_download/pdf/1309.2058v1.pdf", "-"],
                     capture_output=True, text=True, check=True).stdout
R2 = {}
lines = txt.splitlines()
for i, line in enumerate(lines):
    for m in re.finditer(r"(?:^|\s)(\d+)\s+[−-]\s?(\d+\.\d{12,14})\b", line):          # "4      −1.39705243371511"
        R2[int(m.group(1))] = "-" + m.group(2)
# the text layer splits two rows (n = 6, 50): the number sits on its own line
for i, line in enumerate(lines):
    m = re.search(r"\s{10,}[−-]\s?(\d+\.\d{12,14})\s*$", line)
    if m:
        for j in (i - 1, i - 2, i + 1, i + 2):
            mm = re.search(r"\s(6|50)\s*$", lines[j]) if 0 <= j < len(lines) else None
            if mm and int(mm.group(1)) not in R2:
                R2[int(mm.group(1))] = "-" + m.group(1)
R3 = {}
for line in open("ts13_download/src/NdimWH_130910rev2.tex", encoding="latin-1"):
    m = re.match(r"^(?:~~)?(\d+)&\$(?:~~)?(-\d+\.\d+)", line)
    if m:
        R3[int(m.group(1))] = m.group(2)
bad = 0
print("  n   image reading (1)    text layer (2)       TeX source (3)       equal")
for n in sorted(set(R1) | set(R2) | set(R3)):
    a, b, c = R1.get(n), R2.get(n), R3.get(n)
    ok = a == b == c and a is not None
    bad += not ok
    print(f"  {n:<3d} {str(a):<20s} {str(b):<20s} {str(c):<20s} {'yes' if ok else 'NO'}")
print(f"rows: {len(R1)}, {len(R2)}, {len(R3)}; {bad} differ")
sys.exit(1 if bad or not (len(R1) == len(R2) == len(R3) == 11) else 0)
