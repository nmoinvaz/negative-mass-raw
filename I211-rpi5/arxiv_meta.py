#!/usr/bin/env python3
"""Reads arXiv's own abstract page (abs.html, saved by fetch.sh) for each paper directory: title, authors, version list,
journal reference. This is the arXiv-side verification of each identifier, used where the API returned HTTP 429.
    arxiv_meta.py <papers-dir>
"""
import html
import os
import re
import sys

root = sys.argv[1]
for d in sorted(os.listdir(root)):
    p = os.path.join(root, d, "abs.html")
    if not os.path.isfile(p):
        continue
    s = open(p, encoding="utf-8", errors="replace").read()
    meta = lambda n: [html.unescape(m) for m in re.findall(rf'<meta name="{n}" content="([^"]*)"', s)]  # noqa: E731
    ver = re.findall(r"\[v(\d+)\]\s*(?:</a>)?\s*(?:<[^>]*>)*\s*([A-Z][a-z]{2} \d{4}|[0-9]+ [A-Z][a-z]{2} [0-9]{4})", s)
    sub = re.findall(r"Submitted on ([0-9]+ [A-Za-z]+ [0-9]{4})", s)
    last = re.findall(r"last revised ([0-9]+ [A-Za-z]+ [0-9]{4})", s)
    jref = re.findall(r'class="tablecell jref">([^<]*)<', s)
    doi = meta("citation_doi")
    print(f"{d}\n  id: {(meta('citation_arxiv_id') or ['?'])[0]}\n  title: {(meta('citation_title') or ['?'])[0]}")
    print(f"  authors: {'; '.join(meta('citation_author'))}\n  submitted: {sub[:1]} last revised: {last[:1]}")
    print(f"  jref: {jref}  doi: {doi}")
