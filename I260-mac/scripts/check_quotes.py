#!/usr/bin/env python3
"""check_quotes.py [--mutate] [--notes FILE ...]

1. quotes.tsv (columns: key, arxiv id, locator, quote): each quote must occur, after normalization, in
   text/<id>.pypdf.txt or text/<id>.pdftotext.txt. Exit 1 if any does not.
2. --notes FILE...: every string of at least 30 characters between “ ” or " " in FILE that is followed within 60 characters
   by a [KEY] naming a key of quotes.tsv, or that sits on a line of a quotes.tsv quote, is checked the same way.
   (Cheap form: every “…” string of >= 30 characters in FILE must occur in the text of some paper of quotes.tsv.)
--mutate: changes one character of the first quote and of the first notes string; the run must then exit 1 (it prints
'MUTATION NOT CAUGHT' and exits 0 if the check is blind).

Normalization: NFKC, dashes and minus signs to '-', curly quotes to straight, whitespace collapsed (and removed before
punctuation and around < > =, where PDF extraction adds or drops it), hyphenation at line ends removed, case kept. Run from the I260-mac folder."""
import csv, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
TEXT = os.path.join(HERE, "text")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
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


def found(q, ids):
    q = norm(q)
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
    for f in notes:
        s = open(f).read()
        strs = re.findall(r"“([^”]{30,}?)”", s)
        for n, q in enumerate(strs):
            if mutate and n == 0:
                q = q[:15] + ("X" if q[15] != "X" else "Y") + q[16:]
            if not found(q, allids):
                print("NOTE STRING NOT FOUND:", os.path.basename(f), "|", q[:90]); bad += 1
    print(f"{len(rows)} quotes, {sum(len(re.findall(chr(0x201c)+'[^'+chr(0x201d)+']{30,}?'+chr(0x201d), open(f).read())) for f in notes)} note strings, {bad} not found")
    if mutate:
        print("mutation fired (exit 1 expected)" if bad else "MUTATION NOT CAUGHT: the check is blind")
    sys.exit(1 if bad else 0)


main()
