#!/usr/bin/env python3
"""C0: verify the four arXiv ids of #164 against their abs pages and the citing papers' bibliographies.

usage: python3 -I verify_ids.py [--mutate=NAME]      (from this folder; exit 0 only if every check passes)

For each id (the abs page is dl/<id>/abs.html, fetched 2026-11-25 by fetch.sh) it checks that
  V1  the abs page's title equals the title the citing paper prints for that reference
  V2  every author's family name in the citing paper's reference occurs, in order, among the abs page's authors,
      and the author counts agree
  V3  the journal reference (volume, page, year) the citing paper prints occurs in the abs page's journal reference;
      an abs page with no journal reference is reported as a note, not a failure
  V4  the versions listed on the abs page are exactly the versions fetched (dl/<id>v<n>/)
The citing papers are the I152 TeX files (../I152-rpi5/src): [BGKKKN26] 2610.38659 (comment bibliography with
arXiv ids) and [SN26b] 2610.29941 v2 (\\bibitem entries). Mutations (each must exit 1): title author jref version.
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
I152 = HERE.parent / "I152-rpi5" / "src"
BG = I152 / "2610.38659" / "main.tex"
SN = I152 / "2610.29941v2" / "research.tex"
IDS = ["2301.05243", "2403.08387", "2510.11406", "2607.18399"]
MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
fails, notes = [], []


def fail(m):
    fails.append(m)
    print("FAIL", m)


def squash(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s.lower() if c.isalnum())


def detex(s):
    s = re.sub(r"\\['`^\"~=.]\{?([A-Za-z])\}?", r"\1", s)  # \'a, {\'a}, \"o
    s = re.sub(r"\\(newblock|textbf)\b", " ", s)
    return re.sub(r"[{}~]", " ", s).replace("``", "").replace("''", "")


def abs_info(i):
    t = (HERE / f"dl/{i}/abs.html").read_text(encoding="utf-8")

    def g(p):
        m = re.search(p, t, re.S)
        return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""

    title = re.sub(r"^Title:\s*", "", g(r'<h1 class="title[^"]*">(.*?)</h1>'))
    authors = [a.strip() for a in re.sub(r"^Authors:\s*", "", g(r'<div class="authors">(.*?)</div>')).split(",")]
    hist = g(r'<div class="submission-history">(.*?)</div>')
    versions = sorted(set(re.findall(r"\[(v\d+)\]", hist)))
    return title, authors, g(r'<td class="tablecell jref">(.*?)</td>'), versions


def cite_bg(i):
    """Title, authors line, journal line of the [BGKKKN26] bibliography entry that names arXiv:<i> in its comments."""
    txt = BG.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", txt)
    for b in blocks:
        if f"arXiv:{i}" in b:
            t = re.search(r"%``(.*?),''", b, re.S)
            body = re.search(r"\\bibitem\{[^}]*\}\n(.*?)\n(?:%|$)", b, re.S)
            m = re.search(r"\\bibitem\{[^}]*\}\n(.*?)(?=\n%|\Z)", b, re.S)
            lines = [ln for ln in b.splitlines() if ln and not ln.startswith("%")]
            # lines: \bibitem{key}, authors, journal
            return (" ".join(t.group(1).split()) if t else None), (lines[1] if len(lines) > 1 else ""), (lines[2] if len(lines) > 2 else "")
    return None, "", ""


def cite_sn(title):
    """Authors and journal of the [SN26b] \\bibitem whose title squashes to <title>."""
    txt = SN.read_text(encoding="utf-8")
    for b in re.split(r"\\bibitem", txt)[1:]:
        m = re.search(r"``(.*?),''", b, re.S)
        if m and squash(m.group(1)) == squash(title):
            lines = [ln for ln in b.splitlines()[1:] if ln.strip()]
            return lines[0], " ".join(ln for ln in lines if "Phys" in ln or "Univ" in ln)
    return "", ""


def family_names(authors_tex):
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+", detex(authors_tex).replace("\n", " "))
    out = []
    for p in parts:
        p = re.sub(r"^\s*and\s+", "", p.strip())
        if not p:
            continue
        p = re.sub(r"^(?:[A-Z]\.\s*)+", "", p).strip()  # strip initials
        out.append(squash(p))
    return out


def numbers(s):
    return set(re.findall(r"\d+", s))


for i in IDS:
    title, authors, jref, versions = abs_info(i)
    bt, bauth, bjour = cite_bg(i)
    if bt is None:
        fail(f"{i}: [BGKKKN26] bibliography has no entry naming arXiv:{i}")
        continue
    stitle_authors, sjour = cite_sn(bt)
    want_title = bt if MUT != "title" else bt + " (altered)"
    if squash(title) != squash(want_title):
        fail(f"V1 {i}: abs title {title!r} != [BGKKKN26] bibliography title {want_title!r}")
    fam = family_names(bauth)
    if MUT == "author":
        fam = fam[:-1]
    if len(fam) != len(authors) or any(not squash(a).endswith(f) for a, f in zip(authors, fam)):
        fail(f"V2 {i}: abs authors {authors} vs [BGKKKN26] family names {fam}")
    if stitle_authors:  # [SN26b] cites this title too: authors must agree with the abs page
        fam2 = family_names(stitle_authors)
        if len(fam2) != len(authors) or any(not squash(a).endswith(f) for a, f in zip(authors, fam2)):
            fail(f"V2 {i}: abs authors {authors} vs [SN26b] family names {fam2}")
    jn = numbers(bjour)
    if MUT == "jref":
        jn = {"999999"}
    if not jref:
        notes.append(f"{i}: abs page shows no journal reference; [BGKKKN26] prints {bjour.strip()!r}")
    elif not jn <= numbers(jref):
        fail(f"V3 {i}: journal numbers {sorted(jn)} of [BGKKKN26] not all in abs journal ref {jref!r}")
    if sjour and jn and not numbers(sjour) >= (jn - {"999999"}) and MUT is None:
        fail(f"V3 {i}: [SN26b] journal {sjour!r} lacks numbers of [BGKKKN26] {bjour!r}")
    fetched = sorted(p.name.split("v")[-1] and "v" + p.name.rsplit("v", 1)[1] for p in (HERE / "dl").glob(f"{i}v*"))
    if MUT == "version":
        fetched = fetched[:-1]
    if fetched != versions:
        fail(f"V4 {i}: abs versions {versions} != fetched {fetched}")
    print(f"{i}: {title} | {', '.join(authors)} | {jref or '(no journal ref)'} | {versions}"
          f" | [SN26b] cites it: {'yes' if stitle_authors else 'no (title not found)'}")

for n in notes:
    print("NOTE", n)
print(f"{len(IDS)} ids, {len(fails)} failures" + (f" (mutation {MUT})" if MUT else ""))
sys.exit(1 if fails else 0)
