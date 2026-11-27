#!/usr/bin/env python3
"""ind211: a sample of #211's references against arXiv's metadata, and [SH02]'s fit form (criteria in README.md)."""
import argparse
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["title", "fitform"])
O = ap.parse_args()
R = []


def check(n, ok, d):
    R.append((n, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {n}: {d}", flush=True)


def norm(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))   # A1: drop accents
    s = re.sub(r"\\[a-zA-Z]+|[{}$^_]", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


lit = subprocess.run(["git", "-C", "/Users/nathan/Source/negative-mass", "show", "origin/wip/i211-universe-lit:notes/literature.md"],
                     capture_output=True, text=True).stdout
ns = {"a": "http://www.w3.org/2005/Atom"}
root = ET.parse("arxiv_sample.xml").getroot()
notes, ok1 = [], True
for i, e in enumerate(root.findall("a:entry", ns)):
    aid = re.sub(r"v\d+$", "", e.find("a:id", ns).text.split("/abs/")[1])
    title = " ".join(e.find("a:title", ns).text.split())
    if O.mutate == "title" and i == 0:
        title = title.replace(title.split()[0], "Zebra", 1)
    first = e.find("a:author/a:name", ns).text.split()[-1]
    # the paragraph (entry) that cites this id
    paras = [p for p in re.split(r"\n(?=- )", lit) if aid in p]
    hit = any(norm(title) in norm(p) for p in paras) and any(norm(first) in norm(p) for p in paras)
    ok1 &= hit
    notes.append(f"{aid}: {'ok' if hit else 'MISSING'} ({first}, \"{title[:50]}…\")")
check("K1", ok1 and len(notes) == 7, f"{len(notes)} sampled: " + "; ".join(notes))
src = open("sh02_src/x/wh_main.tex").read() + open("sh02_src/x/wh_tables.tex").read()
pat = r"1\s*\+\s*b_4\s*\\exp\s*\(\s*-\s*H" if O.mutate == "fitform" else r"r/a\s*=\s*1\s*\+\s*b_4\s*\\exp\s*\(\s*H\s*\(\s*\\tau"
fit = re.search(pat, src)
hval = "1.12" in src
quoted = "1.12" in lit
check("K2", bool(fit) and hval and quoted, f"fit form found: {bool(fit)}; H = 1.12 in SH02's table: {hval}; quoted in literature.md: {quoted}")
bad = [n for n, ok in R if not ok]
print(f"\n{len(R)} criteria, {len(R) - len(bad)} pass; failed: {bad}")
sys.exit(1 if bad else 0)
