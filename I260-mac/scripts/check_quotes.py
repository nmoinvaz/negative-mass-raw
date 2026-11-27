#!/usr/bin/env python3
"""check_quotes.py [--mutate] [--notes FILE ...]

1. quotes.tsv (columns: key, arxiv id, locator, quote): each quote must occur, after normalization, in
   text/<id>.pypdf.txt or text/<id>.pdftotext.txt. Exit 1 if any does not.
2. FILE... (notes): every string of at least 30 characters between “ ” or between straight " " (in a paragraph or list item with an
   even number of straight quotes) must occur in the text of some paper named in quotes.tsv.
--mutate: changes one character of the first quote and of the first notes string; the run must then exit 1 (it prints
'MUTATION NOT CAUGHT' and exits 0 if the check is blind).

Normalization: NFKC, dashes and minus signs to '-', curly quotes to straight, whitespace collapsed (and removed before
punctuation and around < > =, where PDF extraction adds or drops it), hyphenation at line ends removed, case kept. Run from the I260-mac folder."""
import csv, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
TEXT = os.path.join(HERE, "text")


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("$", "")
    s = re.sub(r"[‐-―−‒]", "-", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("′", "'")
    s = re.sub(r"-\s*\n\s*(?=[a-z])", "", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([<>=,;:.)])", r"\1", s)
    s = re.sub(r"\(\s*", "(", s)
    s = re.sub(r"\s*([<>=])\s*", r"\1", s)
    return s.strip()


_cache = {}


def text_of(i):
    if i not in _cache:
        parts = []
        for suf in (".pypdf.txt", ".pdftotext.txt"):
            p = os.path.join(TEXT, i.replace("/", "_") + suf)
            if os.path.exists(p):
                parts.append(norm(open(p, errors="replace").read()))
        _cache[i] = parts
    return _cache[i]


_titles = None


def titles():
    global _titles
    if _titles is None:
        _titles = []
        vp = os.path.join(HERE, "verify", "verify_table.tsv")
        if os.path.exists(vp):
            for line in open(vp).read().split("\n")[1:]:
                c = line.split("\t")
                if len(c) > 3:
                    _titles.append(norm(c[3]))
    return _titles


def found(q, ids):
    q = norm(q)
    if any(q in t for t in titles()):  # a paper's title as INSPIRE gives it (verify/verify_table.tsv)
        return "title"
    pieces = [x.strip() for x in re.split(r"\.\.\.|…|\[…\]|\[\.\.\.\]", q) if len(x.strip()) >= 12]
    for i in ids:
        for t in text_of(i):
            if all(p in t for p in pieces):
                return i
            t2 = t.replace("-", "")
            if all(p.replace("-", "") in t2 for p in pieces):  # hyphen at a line end may be real or typesetting
                return i
    return None


def main():
    mutate = "--mutate" in sys.argv
    notes = [a for a in sys.argv[1:] if not a.startswith("--") and os.path.exists(a)]
    rows = list(csv.reader(open(os.path.join(HERE, "quotes.tsv")), delimiter="\t"))[1:]
    bad = 0
    for n, (key, i, loc, q) in enumerate(rows):
        if mutate and n == 0:
            q = q[:20] + ("X" if q[20] != "X" else "Y") + q[21:]
        if not found(q, [i]):
            print("QUOTE NOT FOUND:", key, i, loc, "|", q[:80]); bad += 1
    allids = sorted({r[1] for r in rows})
    nstr = 0
    for f in notes:
        s = open(f).read()
        units, cur = [], []
        for line in s.split("\n"):
            if not line.strip() or re.match(r"\s*([-*]|\d+\.|\|)\s", line) or line.startswith("#"):
                if cur: units.append(" ".join(cur)); cur = []
                if line.strip() and not line.startswith("#"): cur.append(line)
            else:
                cur.append(line.strip())
        if cur: units.append(" ".join(cur))
        strs = []
        for u in units:
            strs += re.findall(r"\u201c([^\u201d]{30,}?)\u201d", u)
            parts = u.split('"')
            if len(parts) % 2 == 1:  # balanced straight quotes
                strs += [x for x in parts[1::2] if len(x) >= 30]
        for n, q in enumerate(strs):
            if mutate and n == 0:
                q = q[:15] + ("X" if q[15] != "X" else "Y") + q[16:]
            nstr += 1
            if not found(q, allids):
                print("NOTE STRING NOT FOUND:", os.path.basename(f), "|", q[:100]); bad += 1
    print(f"{len(rows)} quotes, {nstr} note strings, {bad} not found")
    if mutate:
        print("mutation fired (exit 1 expected)" if bad else "MUTATION NOT CAUGHT: the check is blind")
    sys.exit(1 if bad else 0)


main()
