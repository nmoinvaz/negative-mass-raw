#!/usr/bin/env python3
"""screen.py TEXTDIR PATTERNS OUTTSV OUTCTX [ids...]: apply the patterns to every TEXTDIR/<id>.pypdf.txt (or the given ids).
OUTTSV: id<TAB>chars<TAB>count per pattern. OUTCTX: the matching contexts (120 chars each side), at most 8 per pattern."""
import os, re, sys
td, pf, out_tsv, out_ctx = sys.argv[1:5]
ids = sys.argv[5:] or sorted(f[:-len(".pypdf.txt")] for f in os.listdir(td) if f.endswith(".pypdf.txt"))
pats = []
for l in open(pf):
    if l.startswith("#") or not l.strip(): continue
    n, rx = l.rstrip("\n").split("\t", 1); pats.append((n, re.compile(rx, re.I)))
with open(out_tsv, "w") as t, open(out_ctx, "w") as c:
    t.write("id\tchars\t" + "\t".join(n for n, _ in pats) + "\n")
    for i in ids:
        p = os.path.join(td, i + ".pypdf.txt")
        if not os.path.exists(p): continue
        raw = open(p, errors="replace").read()
        txt = re.sub(r"-\n(?=[a-z])", "", raw)
        txt = re.sub(r"\s+", " ", txt)
        row = []
        for n, rx in pats:
            ms = list(rx.finditer(txt)); row.append(len(ms))
            for m in ms[:8]:
                a, b = max(0, m.start() - 120), min(len(txt), m.end() + 120)
                c.write(f"[{i}] <{n}> ...{txt[a:b]}...\n")
        t.write(f"{i}\t{len(txt)}\t" + "\t".join(map(str, row)) + "\n")
