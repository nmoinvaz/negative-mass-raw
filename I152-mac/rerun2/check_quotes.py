#!/usr/bin/env python3
"""Check quotes.txt and proposal.md of I152-rpi5 against the fetched sources; write quotes.md.

usage: python3 -I check_quotes.py [--write] [--mutate=NAME]
Run from this folder. Needs pdftotext (poppler). Exit 0 only if every check passes.

C1  every @tex occurs in its source TeX (comments removed, whitespace collapsed); every @absent source lacks it
C2  every @pdf fragment occurs in its PDF (squashed to lower-case alphanumerics), on one page; every @pdfnum string on that page
C3  every sentence of every proposed row cites existing quote ids, and the row's table cell equals its sentences joined
C4  sha256 of every file in sha256sums.txt equals the file on disk
C5  every number in a proposed sentence occurs in a cited quote
C6  every double-quoted string in a proposed sentence occurs in a cited quote
CALC1 is a pseudo-id for jovera_check.py (a recompute, valid only if jovera_run1.log passed)
Mutations (each must exit 1): quote pdf cite dangling sha number absent cell quoted bullet
"""
import hashlib
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = {  # key -> (TeX, PDF, label)
    "A": ("src/2610.38659/main.tex", "pdf/2610.38659.pdf", "arXiv:2610.38659 v1"),
    "S": ("src/2610.29941v2/research.tex", "pdf/2610.29941v2.pdf", "arXiv:2610.29941 v2"),
    "S1": ("src/2610.29941v1/research.tex", "pdf/2610.29941v1.pdf", "arXiv:2610.29941 v1"),
    "D": ("src/1309.2448/rotworm.tex", "pdf/1309.2448.pdf", "arXiv:1309.2448 v1"),
}
MUT = None
for a in sys.argv[1:]:
    if a.startswith("--mutate="):
        MUT = a.split("=", 1)[1]
WRITE = "--write" in sys.argv
fails = []


def fail(msg):
    fails.append(msg)
    print("FAIL", msg)


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def tex_text(path):
    """TeX with comments removed and whitespace collapsed; returns (text, line number of each char)."""
    out, lines = [], []
    for n, line in enumerate((HERE / path).read_text(encoding="utf-8").splitlines(), 1):
        line = re.sub(r"(?<!\\)%.*$", "", line)
        out.append(line + " ")
        lines.extend([n] * (len(line) + 1))
    raw = "".join(out)
    text, tl, prev_space = [], [], False
    for ch, n in zip(raw, lines):
        if ch.isspace():
            if prev_space:
                continue
            ch, prev_space = " ", True
        else:
            prev_space = False
        text.append(ch)
        tl.append(n)
    return "".join(text), tl


def squash(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return "".join(c for c in s if c.isalnum())


def pdf_pages(path):
    r = subprocess.run(["pdftotext", str(HERE / path), "-"], capture_output=True, text=True)
    if r.returncode != 0:
        print("pdftotext failed:", r.stderr[:200])
        sys.exit(2)
    pages = r.stdout.split("\f")
    return [unicodedata.normalize("NFKC", p) for p in pages]


def parse_quotes(path):
    quotes, cur, key = [], None, None
    for line in (HERE / path).read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            continue
        if not line.strip():
            key = None
            continue
        m = re.match(r"@(\w+)\s?(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2)
            if k == "id":
                cur = {"id": v.strip()}
                quotes.append(cur)
            cur[k] = (cur.get(k, "") + " " + v).strip() if k != "id" else v.strip()
            key = k
        elif cur is not None and key:
            cur[key] += " " + line.strip()
    return quotes


# ---------------------------------------------------------------- C4
def check_sha():
    for line in (HERE / "sha256sums.txt").read_text().splitlines():
        want, name = line.split(None, 1)
        if MUT == "sha":
            want = want[:-1] + ("0" if want[-1] != "0" else "1")
        got = hashlib.sha256((HERE / name.strip()).read_bytes()).hexdigest()
        if got != want:
            fail(f"C4 sha256 differs: {name.strip()}")


# ---------------------------------------------------------------- C1, C2
def check_quotes(quotes):
    texts = {k: tex_text(v[0]) for k, v in SRC.items()}
    pages = {k: pdf_pages(v[1]) for k, v in SRC.items()}
    sq_pages = {k: [squash(p) for p in v] for k, v in pages.items()}
    seen = set()
    for q in quotes:
        qid = q["id"]
        if qid in seen:
            fail(f"duplicate id {qid}")
        seen.add(qid)
        src = q.get("src")
        if src not in SRC:
            fail(f"{qid}: unknown source {src!r}")
            continue
        tex = collapse(q.get("tex", ""))
        if MUT == "quote" and qid == quotes[0]["id"]:
            altered = re.sub(r"^\S+", "Xqzv", tex, count=1)
            if altered == tex:
                fail("mutation quote is inert")
            tex = altered
        if not tex:
            fail(f"{qid}: empty @tex")
            continue
        T, TL = texts[src]
        i = T.find(tex)
        if i < 0:
            fail(f"C1 {qid}: not in {SRC[src][0]}: {tex[:70]}...")
            q["line"] = None
        else:
            q["line"] = f"{TL[i]}-{TL[i + len(tex) - 1]}" if TL[i] != TL[i + len(tex) - 1] else str(TL[i])
        for ab in q.get("absent", "").split():
            ab_text = texts[ab][0] if MUT != "absent" else texts[src][0]
            if tex in ab_text:
                fail(f"C1 {qid}: should be absent from {SRC[ab][0]} but occurs")
        # PDF
        frag = q.get("pdf")
        psrc = src
        if MUT == "pdf" and qid == quotes[0]["id"]:
            psrc = "D"
        if not frag:
            fail(f"C2 {qid}: no @pdf fragment")
            continue
        sf = squash(frag)
        if len(sf) < 20:
            fail(f"C2 {qid}: @pdf fragment too short to mean anything ({len(sf)} chars)")
        hit = [n for n, p in enumerate(sq_pages[psrc], 1) if sf in p]
        if not hit:
            fail(f"C2 {qid}: @pdf fragment not in {SRC[psrc][1]}: {frag[:70]}...")
            q["page"] = None
            continue
        q["page"] = hit[0]
        for num in q.get("pdfnum", "").split():
            if num not in collapse(pages[psrc][hit[0] - 1]):
                fail(f"C2 {qid}: {num!r} not on PDF page {hit[0]}")
    return quotes


# ---------------------------------------------------------------- proposal
def parse_proposal(path, quotes):
    ids = {q["id"] for q in quotes}
    lines = (HERE / path).read_text(encoding="utf-8").splitlines()
    sents, types = {}, {}
    for line in lines:
        m = re.match(r"^### Row (R\d+) (table|bullets)\b", line)
        if m:
            types[m.group(1)] = m.group(2)
        m = re.match(r"^- (R\d+)\.(\d+) (.+) \{([^}]*)\}\s*$", line)
        if m:
            sents.setdefault(m.group(1), []).append((int(m.group(2)), m.group(3), [c.strip() for c in m.group(4).split(",") if c.strip()]))
    plus = [ln[1:] for ln in lines if ln.startswith("+|")]
    bullets, cur = [], None  # sentence bullets of the diff: "+" lines indented 4+ spaces then "- ", with continuation lines
    for ln in lines:
        m = re.match(r"^\+\s{4,}- (.*)$", ln)
        if m:
            cur = [m.group(1).strip()]
            bullets.append(cur)
        elif cur is not None and re.match(r"^\+\s{6,}\S", ln):
            cur.append(ln[1:].strip())
        else:
            cur = None
    bullets = [" ".join(b) for b in bullets]
    return sents, types, plus, bullets, ids


def check_proposal(quotes):
    if not (HERE / "proposal.md").exists():
        print("proposal.md not present yet: C3, C5, C6 skipped")
        return
    sents, types, plus, bullets, ids = parse_proposal("proposal.md", quotes)
    qd = {q["id"]: q for q in quotes}
    if not sents:
        fail("C3 no sentences found in proposal.md")
    ti = 0
    for row, items in sorted(sents.items()):
        items.sort()
        for k, (n, s, cites) in enumerate(items):
            if MUT == "cite" and row == "R1" and n == 1:
                cites = []
            if MUT == "dangling" and row == "R1" and n == 1:
                cites = cites + ["Q99"]
            if MUT == "number" and row == "R1" and n == 2:
                s = re.sub(r"0\.10063", "0.10064", s, count=1)
            if not cites:
                fail(f"C3 {row}.{n}: sentence cites no quote")
            for c in cites:
                if c == "CALC1":
                    log = HERE / "jovera_run1.log"
                    if not (log.exists() and log.read_text().strip().endswith("failures: 0")):
                        fail(f"C3 {row}.{n}: CALC1 cited but jovera_run1.log is not a passing run")
                elif c not in ids:
                    fail(f"C3 {row}.{n}: cited id {c} not in quotes.txt")
            pool = " ".join(collapse(qd[c]["tex"]) + " " + qd[c].get("pdf", "") + " " + qd[c].get("pdfnum", "") for c in cites if c in qd)
            pool = pool.replace("\\,", "").replace("~", "")
            if MUT == "quoted" and row == "R1" and n == 5:
                s = s.replace("may stabilize", "will stabilize")
            sp = squash(pool)
            for qs_ in re.findall(r'"([^"]+)"', s):
                if squash(qs_) not in sp:
                    fail(f"C6 {row}.{n}: quoted string not in a cited quote: {qs_[:60]}")
            for num in re.findall(r"\d+\.\d+|\d{2,}", re.sub(r"\[[A-Za-z0-9]+\]", "", s)):
                if num not in pool:
                    fail(f"C5 {row}.{n}: number {num} not in a cited quote")
            items[k] = (n, s, cites)
        joined = [s for _, s, _ in items]
        typ = types.get(row)
        if typ == "table":
            if ti >= len(plus):
                fail(f"C3 {row}: no '+|' diff row")
            else:
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", plus[ti]) if c.strip() != ""]
                cell = cells[1] if len(cells) > 1 else ""
                if MUT == "cell" and row == "R1":
                    cell += " extra."
                if cell != " ".join(joined):
                    fail(f"C3 {row}: table cell differs from the joined sentences")
            ti += 1
        elif typ == "bullets":
            want = joined if MUT != "bullet" else joined[:-1] + [joined[-1] + " extra."]
            if bullets != want:
                fail(f"C3 {row}: diff bullets differ from the sentences ({len(bullets)} bullets, {len(want)} sentences)")
        else:
            fail(f"C3 {row}: no '### Row {row} table|bullets' header")


def write_md(quotes):
    qs = {}
    for q in quotes:
        for x in re.split(r"[,\s]+", q.get("q", "")):
            if x:
                qs.setdefault(x, []).append(q["id"])
    out = ["# quotes.md: quotes with locations (generated by `check_quotes.py --write`; do not edit)", "",
           "Each entry: id, source file and version, location in the paper, PDF page of the fetched PDF, TeX line(s) in the",
           "committed source, questions. The quote is the TeX source text (comments removed, whitespace collapsed).",
           "`check_quotes.py` proves each quote occurs in its source and each PDF fragment in its PDF.", "",
           "Source keys: A = arXiv:2610.38659 v1, S = arXiv:2610.29941 v2 (current), S1 = arXiv:2610.29941 v1, D = arXiv:1309.2448 v1 ([DFKKR13]).",
           "", "| question | quote ids |", "|---|---|"]
    for k in sorted(qs):
        out.append(f"| {k} | {', '.join(qs[k])} |")
    out.append("")
    for q in quotes:
        _, _, label = SRC[q["src"]]
        out.append(f"### {q['id']}: {label}, {q['loc']}")
        out.append(f"PDF p. {q.get('page', '?')}; TeX line {q.get('line', '?')} of `{SRC[q['src']][0]}`; {q.get('q', '')}.")
        out.append("")
        out.append("> " + collapse(q["tex"]).replace("\n", " "))
        if q.get("skip"):
            out.append("")
            out.append(f"PDF check limited: {q['skip']}.")
        if q.get("absent"):
            out.append("")
            out.append(f"Not in {', '.join(SRC[a][2] for a in q['absent'].split())} (checked).")
        out.append("")
    (HERE / "quotes.md").write_text("\n".join(out), encoding="utf-8")


def main():
    quotes = parse_quotes("quotes.txt")
    check_sha()
    quotes = check_quotes(quotes)
    check_proposal(quotes)
    if WRITE and not fails:
        write_md(quotes)
    n = len(quotes)
    print(f"{n} quotes, {len(fails)} failures" + (f" (mutation {MUT})" if MUT else ""))
    sys.exit(1 if fails else 0)


main()
