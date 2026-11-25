#!/usr/bin/env python3
"""Check quotes.txt and proposal.md of I164-rpi5 against the fetched sources; write quotes.md.

usage: python3 -I check_quotes.py [--write] [--write-pdftext] [--mutate=NAME]
Run from any directory. Exit 0 only if every check passes. Exit 3: all checks passed but C2 (PDF text) could not run,
because neither pdftotext (poppler) nor the cached pdftext/<key>.txt is available.

C1  every @tex occurs in its source TeX (comments removed, whitespace collapsed), and in every @also version;
    every @absent source lacks it
C2  every @pdf fragment occurs on one page of its PDF text (squashed to lower-case alphanumerics); every @pdfnum string
    occurs on that page. PDF text is `pdftotext` output, or the cache pdftext/<key>.txt when pdftotext is missing
C3  every sentence of every proposed row cites existing quote ids, and the row's table cell, bullets or entry equal its
    sentences joined
C4  sha256 of every file in sha256sums.txt equals the file on disk
C5  every number in a proposed sentence occurs in a cited quote
C6  every double-quoted string in a proposed sentence occurs in a cited quote
C7  every @lacks term is absent from the TeX and the PDF text of every source of its record, and every @has term of
    the same record is present (the search can find things)
C8  the section label computed from the TeX headings is a prefix of every quote's @loc
C10 every double-quoted string in the narrative sections of proposal.md (from '## Answers') occurs in some record
C9  the diff block of proposal.md is the diff `make_diff.py` derives from the sentences and the stored base note (a
    sentence tagged {KEEP} must occur in the base note), and `patch --dry-run` applies it
CALC1 is a pseudo-id for recompute_jc.py (a recompute, valid only if recompute_run1.log passed)
Mutations (each must exit 1): quote pdf cite dangling sha number absent cell quoted bullet entry loc lacks also diff anchor keep answer
"""
import hashlib
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
# key -> (TeX, PDF, label, heading style)
SRC = {
    "L1": ("src/2301.05243v1/sr_ellis.tex", "dl/2301.05243v1/pdf", "arXiv:2301.05243 v1", "named"),
    "L2": ("src/2301.05243v2/paper8.tex", "dl/2301.05243v2/pdf", "arXiv:2301.05243 v2", "arabic"),
    "M1": ("src/2403.08387v1/main.tex", "dl/2403.08387v1/pdf", "arXiv:2403.08387 v1", "roman"),
    "H1": ("src/2510.11406v1/main.tex", "dl/2510.11406v1/pdf", "arXiv:2510.11406 v1", "named"),
    "H2": ("src/2510.11406v2/main.tex", "dl/2510.11406v2/pdf", "arXiv:2510.11406 v2", "named"),
    "N1": ("src/2607.18399v1/main.tex", "dl/2607.18399v1/pdf", "arXiv:2607.18399 v1", "arabic"),
    "N2": ("src/2607.18399v2/main.tex", "dl/2607.18399v2/pdf", "arXiv:2607.18399 v2", "arabic"),
    "SN": ("../I152-rpi5/src/2610.29941v2/research.tex", "../I152-rpi5/pdf/2610.29941v2.pdf",
           "arXiv:2610.29941 v2 ([SN26b])", "roman"),
    "BG": ("../I152-rpi5/src/2610.38659/main.tex", "../I152-rpi5/pdf/2610.38659.pdf",
           "arXiv:2610.38659 v1 ([BGKKKN26])", "named"),
}
BASE_NOTE = (HERE / "src/critical_ghost_dffa582.md").read_text(encoding="utf-8") if (HERE / "src/critical_ghost_dffa582.md").exists() else ""
MUT = None
for a in sys.argv[1:]:
    if a.startswith("--mutate="):
        MUT = a.split("=", 1)[1]
WRITE = "--write" in sys.argv
WRITE_PDFTEXT = "--write-pdftext" in sys.argv
fails = []
pdf_not_run = []
pdf_source = {}


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


def pdf_pages(key):
    """Pages of PDF text for source `key`, from pdftotext if present, else from the cache pdftext/<key>.txt."""
    path = HERE / SRC[key][1]
    cache = HERE / "pdftext" / f"{key}.txt"
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True)
        if r.returncode != 0:
            print("pdftotext failed:", r.stderr[:200])
            sys.exit(2)
        if WRITE_PDFTEXT:
            cache.parent.mkdir(exist_ok=True)
            cache.write_text(r.stdout, encoding="utf-8")
        pdf_source[key] = "pdftotext"
        text = r.stdout
    elif cache.exists():
        pdf_source[key] = "cache"
        text = cache.read_text(encoding="utf-8")
    else:
        pdf_not_run.append(key)
        return None
    return [unicodedata.normalize("NFKC", p) for p in text.split("\f")]


def parse_records(path):
    recs, cur, key = [], None, None
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
                recs.append(cur)
            else:
                cur[k] = (cur.get(k, "") + " " + v).strip()
            key = k
        elif cur is not None and key and key != "id":
            cur[key] += " " + line.strip()
    return recs


# ---------------------------------------------------------------- headings (C8)
def balanced(T, i):
    """T[i] == '{'; returns (inner text, index after the closing brace)."""
    depth, j = 0, i
    while j < len(T):
        if T[j] == "{" and (j == 0 or T[j - 1] != "\\"):
            depth += 1
        elif T[j] == "}" and (j == 0 or T[j - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return T[i + 1:j], j + 1
        j += 1
    return T[i + 1:], len(T)


def roman(n):
    out = ""
    for v, s in [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v:
            out += s
            n -= v
    return out


def headings(key, T):
    """[(position, label)] sorted by position; label as the paper numbers the section."""
    style = SRC[key][3]
    hs = []
    for m in re.finditer(r"\\begin\{abstract\}", T):
        hs.append((m.start(), "Abstract"))
        e = T.find("\\end{abstract}", m.start())
        if e > 0:
            hs.append((e, "(front matter)"))
    if style in ("arabic", "roman"):
        cnt = [0, 0, 0]
        for m in re.finditer(r"\\(section|subsection|subsubsection)(\*?)\{", T):
            lvl = {"section": 0, "subsection": 1, "subsubsection": 2}[m.group(1)]
            title, _ = balanced(T, m.end() - 1)
            if m.group(2):
                hs.append((m.start(), f'Sec. (unnumbered) "{collapse(title)}"'))
                continue
            cnt[lvl] += 1
            for k in range(lvl + 1, 3):
                cnt[k] = 0
            if style == "arabic":
                lab = ".".join(str(c) for c in cnt[:lvl + 1])
            else:
                lab = roman(cnt[0]) + (f" {chr(64 + cnt[1])}" if lvl >= 1 else "") + (f"{cnt[2]}" if lvl >= 2 else "")
            hs.append((m.start(), f"Sec. {lab}"))
    else:
        for m in re.finditer(r"\\prlsec\{|\\noindent\{\\textbf\{|\\paragraph\{", T):
            title, _ = balanced(T, m.end() - 1)
            if title.lstrip().startswith("\\textbf"):
                continue
            hs.append((m.start(), f'run-in "{collapse(title).rstrip(".:")}"'))
    hs.sort()
    return hs


def section_of(hs, pos):
    lab = "(before the first heading)"
    for p, l in hs:
        if p <= pos:
            lab = l
    return lab


# ---------------------------------------------------------------- C4
def check_sha():
    for line in (HERE / "sha256sums.txt").read_text().splitlines():
        if not line.strip():
            continue
        want, name = line.split(None, 1)
        if MUT == "sha":
            want = want[:-1] + ("0" if want[-1] != "0" else "1")
        got = hashlib.sha256((HERE / name.strip()).read_bytes()).hexdigest()
        if got != want:
            fail(f"C4 sha256 differs: {name.strip()}")


# ---------------------------------------------------------------- C1, C2, C7, C8
def check_records(recs):
    texts = {k: tex_text(v[0]) for k, v in SRC.items()}
    heads = {k: headings(k, texts[k][0]) for k in SRC}
    pages = {k: pdf_pages(k) for k in SRC}
    sq_pages = {k: ([squash(p) for p in v] if v else None) for k, v in pages.items()}
    seen = set()
    n_mut = {"quote": 0, "pdf": 0, "absent": 0, "also": 0, "loc": 0, "lacks": 0}
    first_quote = next((r["id"] for r in recs if "tex" in r), None)
    first_also = next((r["id"] for r in recs if "tex" in r and r.get("also")), None)
    first_absent = next((r["id"] for r in recs if "tex" in r and r.get("absent")), None)
    first_lacks = next((r["id"] for r in recs if "lacks" in r), None)
    for q in recs:
        qid = q["id"]
        if qid in seen:
            fail(f"duplicate id {qid}")
        seen.add(qid)
        srcs = q.get("src", "").split()
        for s in srcs:
            if s not in SRC:
                fail(f"{qid}: unknown source {s!r}")
        if not srcs or any(s not in SRC for s in srcs):
            continue
        if "lacks" in q:  # ---- C7
            terms = [t.strip() for t in q["lacks"].split(";") if t.strip()]
            has = [t.strip() for t in q.get("has", "").split(";") if t.strip()]
            if not has:
                fail(f"C7 {qid}: no @has term, so the search has no positive control")
            if MUT == "lacks" and qid == first_lacks:
                n_mut["lacks"] += 1
                terms = terms + [has[0]]
            def found_in(term, tex_low, pdf_sq, pdf_raw):
                """(in TeX, in PDF text or None); a term 're:<regex>' is a case-insensitive regex on the collapsed text."""
                if term.startswith("re:"):
                    rx = re.compile(term[3:], re.I)
                    return bool(rx.search(tex_low)), (None if pdf_raw is None else bool(rx.search(pdf_raw)))
                return term.lower() in tex_low.lower(), (None if pdf_sq is None else squash(term) in pdf_sq)

            for s in srcs:
                T = texts[s][0]
                pdf_sq = "".join(sq_pages[s]) if sq_pages[s] else None
                pdf_raw = collapse(" ".join(pages[s])) if pages[s] else None
                for t in terms:
                    in_t, in_p = found_in(t, T, pdf_sq, pdf_raw)
                    if in_t:
                        fail(f"C7 {qid}: {t!r} occurs in {SRC[s][0]}")
                    if in_p:
                        fail(f"C7 {qid}: {t!r} occurs in the PDF text of {SRC[s][1]}")
                for t in has:
                    in_t, in_p = found_in(t, T, pdf_sq, pdf_raw)
                    if not in_t:
                        fail(f"C7 {qid}: @has {t!r} not in {SRC[s][0]}")
                    if in_p is False:
                        fail(f"C7 {qid}: @has {t!r} not in the PDF text of {SRC[s][1]}")
            q["page"] = None
            continue
        src = srcs[0]
        tex = collapse(q.get("tex", ""))
        if MUT == "quote" and qid == first_quote:
            n_mut["quote"] += 1
            altered = re.sub(r"^\S+", "Xqzv", tex, count=1)
            tex = altered
        if not tex:
            fail(f"{qid}: empty @tex")
            continue
        T, TL = texts[src]
        i = T.find(tex)
        if i < 0:
            fail(f"C1 {qid}: not in {SRC[src][0]}: {tex[:70]}...")
            q["line"] = None
            q["label"] = "?"
        else:
            q["line"] = f"{TL[i]}-{TL[i + len(tex) - 1]}" if TL[i] != TL[i + len(tex) - 1] else str(TL[i])
            q["label"] = section_of(heads[src], i)
            loc = q.get("loc", "")
            if MUT == "loc" and qid == first_quote:
                n_mut["loc"] += 1
                loc = "Sec. 99 " + loc
            if not loc.startswith(q["label"]):  # ---- C8
                fail(f"C8 {qid}: @loc {loc!r} does not start with the computed label {q['label']!r}")
        also = q.get("also", "").split()
        if MUT == "also" and qid == first_also:
            n_mut["also"] += 1
            also = ["N2" if not src.startswith("N") else "L2"]
        for ab in also:
            if ab not in SRC:
                fail(f"{qid}: unknown @also source {ab!r}")
            elif tex not in texts[ab][0]:
                fail(f"C1 {qid}: not in the @also source {SRC[ab][0]}")
        for ab in q.get("absent", "").split():
            ab_text = texts[ab][0] if not (MUT == "absent" and qid == first_absent) else texts[src][0]
            if MUT == "absent" and qid == first_absent:
                n_mut["absent"] += 1
            if tex in ab_text:
                fail(f"C1 {qid}: should be absent from {SRC[ab][0]} but occurs")
        # ---- C2
        frag = q.get("pdf")
        psrc = src
        if MUT == "pdf" and qid == first_quote:
            n_mut["pdf"] += 1
            psrc = next(k for k in ("N2", "L2") if k[0] != src[0] and sq_pages[k])
        if not frag:
            fail(f"C2 {qid}: no @pdf fragment")
            continue
        if sq_pages[psrc] is None:
            q["page"] = "?"
            continue
        found = []  # pages of the fragments (several fragments, separated by ' || ', when the quote crosses a page)
        for one in [x.strip() for x in frag.split("||") if x.strip()]:
            sf = squash(one)
            if len(sf) < 20:
                fail(f"C2 {qid}: @pdf fragment too short to mean anything ({len(sf)} chars): {one[:40]}")
            hit = [n for n, p in enumerate(sq_pages[psrc], 1) if sf in p]
            if not hit:
                fail(f"C2 {qid}: @pdf fragment not in {SRC[psrc][1]}: {one[:70]}...")
                continue
            found.append(hit[0])
        if not found:
            q["page"] = None
            continue
        q["page"] = "-".join(str(x) for x in sorted(set(found)))
        for num in q.get("pdfnum", "").split():
            if not any(num in collapse(pages[psrc][pg - 1]) for pg in found):
                fail(f"C2 {qid}: {num!r} not on PDF page(s) {q['page']}")
    for m, n in n_mut.items():
        if MUT == m and n == 0:
            fail(f"mutation {m} is inert (no record has the field it changes)")
    return recs


# ---------------------------------------------------------------- proposal
def parse_proposal(path):
    lines = (HERE / path).read_text(encoding="utf-8").splitlines()
    sents, types = {}, {}
    for line in lines:
        m = re.match(r"^### Row (R\d+) (table|bullets|entry)\b", line)
        if m:
            types[m.group(1)] = m.group(2)
        m = re.match(r"^- (R\d+)\.(\d+) (.+) \{([^}]*)\}\s*$", line)
        if m:
            sents.setdefault(m.group(1), []).append((int(m.group(2)), m.group(3), [c.strip() for c in m.group(4).split(",") if c.strip()]))

    def runs(first, cont):
        out, cur = [], None
        for ln in lines:
            m = re.match(first, ln)
            if m:
                cur = [m.group(1).strip()]
                out.append(cur)
            elif cur is not None and re.match(cont, ln):
                cur.append(ln[1:].strip())
            else:
                cur = None
        return [" ".join(b) for b in out]

    plus = [ln[1:] for ln in lines if ln.startswith("+|")]
    bullets = runs(r"^\+ {4}- (.*)$", r"^\+ {6}\S")
    entries = runs(r"^\+ {2}- (.*)$", r"^\+ {4}\S")
    return sents, types, plus, bullets, entries


def check_proposal(recs):
    if not (HERE / "proposal.md").exists():
        print("proposal.md not present yet: C3, C5, C6 skipped")
        if MUT in ("cite", "dangling", "number", "quoted", "cell", "bullet", "entry", "keep", "answer"):
            fail(f"mutation {MUT} needs proposal.md, which is not present")
        return
    ids = {q["id"] for q in recs}
    sents, types, plus, bullets, entries = parse_proposal("proposal.md")
    qd = {q["id"]: q for q in recs}
    if not sents:
        fail("C3 no sentences found in proposal.md")
    ti = 0
    first_row = next((r for r in sorted(sents) if types.get(r) == "table"), None)
    n_mut = {"cite": 0, "dangling": 0, "number": 0, "quoted": 0, "cell": 0, "bullet": 0, "entry": 0, "keep": 0}
    num_re = r"\d+\.\d+|\d{2,}"

    def first_where(pred):
        for row_, items_ in sorted(sents.items()):
            for n_, s_, _ in sorted(items_):
                if pred(s_):
                    return (row_, n_)
        return None

    tgt_cite = first_where(lambda s_: True)
    tgt_keep = None
    for row_, items_ in sorted(sents.items()):
        for n_, s_, cites_ in sorted(items_):
            if cites_ == ["KEEP"] and tgt_keep is None:
                tgt_keep = (row_, n_)
    tgt_number = first_where(lambda s_: re.search(num_re, re.sub(r"\[[A-Za-z0-9]+\]|#\d+|arXiv:\d+\.\d+|\d{4}-\d{2}-\d{2}", "", s_)))
    tgt_quoted = first_where(lambda s_: re.search(r'"([^"]+)"', s_))
    stats = {"sentences": 0, "numbers": 0, "quoted strings": 0, "KEEP": 0}
    for row, items in sorted(sents.items()):
        items.sort()
        for k, (n, s, cites) in enumerate(items):
            stats["sentences"] += 1
            if MUT == "cite" and (row, n) == tgt_cite:
                cites = []
                n_mut["cite"] += 1
            if MUT == "dangling" and (row, n) == tgt_cite:
                cites = cites + ["Q99"]
                n_mut["dangling"] += 1
            if MUT == "number" and (row, n) == tgt_number:
                head = re.sub(r"\[[A-Za-z0-9]+\]|#\d+|arXiv:\d+\.\d+|\d{4}-\d{2}-\d{2}", "", s)
                num = re.search(num_re, head).group(0)
                s = s.replace(num, str(int(num.replace(".", "")) + 1), 1)
                n_mut["number"] += 1
            if MUT == "keep" and (row, n) == tgt_keep:
                s = s + " Z"
                n_mut["keep"] += 1
            if not cites:
                fail(f"C3 {row}.{n}: sentence cites no quote")
            if cites == ["KEEP"]:  # existing text of the note: must occur in the base note, no quote to check
                stats["KEEP"] += 1
                if s.rstrip(".") not in BASE_NOTE:
                    fail(f"C9 {row}.{n}: a {{KEEP}} sentence is not in the base note: {s[:60]}")
                items[k] = (n, s, cites)
                continue
            for c in cites:
                if c == "CALC1":
                    log = HERE / "recompute_run1.log"
                    if not (log.exists() and log.read_text().strip().endswith("failures: 0")):
                        fail(f"C3 {row}.{n}: CALC1 cited but recompute_run1.log is not a passing run")
                elif c not in ids:
                    fail(f"C3 {row}.{n}: cited id {c} not in quotes.txt")
            pool = " ".join(collapse(qd[c].get("tex", "")) + " " + qd[c].get("pdf", "") + " " + qd[c].get("pdfnum", "")
                            + " " + qd[c].get("lacks", "") + " " + qd[c].get("has", "") for c in cites if c in qd)
            if "CALC1" in cites:
                log = HERE / "recompute_run1.log"
                pool += " " + " ".join(ln for ln in (log.read_text().splitlines() if log.exists() else []) if ln.startswith("VALUE"))
            pool = pool.replace("\\,", "").replace("~", "")
            if MUT == "quoted" and (row, n) == tgt_quoted:
                n_mut["quoted"] += 1
                s = re.sub(r'"([^"]+)"', lambda m: '"' + m.group(1) + ' zqx"', s, count=1)
            sp = squash(pool)
            for qs_ in re.findall(r'"([^"]+)"', s):
                stats["quoted strings"] += 1
                if squash(qs_) not in sp:
                    fail(f"C6 {row}.{n}: quoted string not in a cited quote: {qs_[:60]}")
            claim = re.sub(r"\[[A-Za-z0-9]+\]|#\d+|arXiv:\d+\.\d+|\d{4}-\d{2}-\d{2}", "", s)  # tags, issue numbers, ids, dates
            for num in re.findall(r"\d+\.\d+|\d{2,}", claim):
                stats["numbers"] += 1
                if num not in pool:
                    fail(f"C5 {row}.{n}: number {num} not in a cited quote")
            items[k] = (n, s, cites)
        joined = [s for _, s, _ in items]
        typ = types.get(row)
        if typ == "table":
            cells_of = [[x.strip() for x in re.split(r"(?<!\\)\|", pl) if x.strip() != ""] for pl in plus]
            want_cell = " ".join(joined)
            if MUT == "cell" and row == first_row:
                n_mut["cell"] += 1
                want_cell += " extra."
            if not any(len(cl) > 1 and cl[1] == want_cell for cl in cells_of):
                fail(f"C3 {row}: no '+|' diff row whose result cell equals the joined sentences")
        elif typ in ("bullets", "entry"):
            got = bullets if typ == "bullets" else entries
            want = list(joined)
            if MUT in ("bullet", "entry") and ((MUT == "bullet") == (typ == "bullets")):
                n_mut[MUT] += 1
                want = want[:-1] + [want[-1] + " extra."]
            if not any(got[i:i + len(want)] == want for i in range(len(got) - len(want) + 1)):
                fail(f"C3 {row}: diff {typ} differ from the sentences ({len(got)} found, {len(want)} sentences)")
        else:
            fail(f"C3 {row}: no '### Row {row} table|bullets|entry' header")
    print("proposal: " + ", ".join(f"{v} {k}" for k, v in stats.items()) + " checked")
    for m, n in n_mut.items():
        if MUT == m and n == 0:
            fail(f"mutation {m} is inert (the proposal has nothing it changes)")


def check_narrative(recs):
    """C10: every double-quoted string in the narrative sections of proposal.md occurs in some record (squashed)."""
    p = HERE / "proposal.md"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    i = text.find("## Answers")
    if i < 0:
        fail("C10 proposal.md has no '## Answers' section")
        return
    narrative = text[i:]
    pool = squash(" ".join(collapse(r.get("tex", "")) + " " + r.get("lacks", "") + " " + r.get("has", "") for r in recs))
    strings = [collapse(x) for x in re.findall(r'"([^"]+)"', narrative)]
    if MUT == "answer":
        strings = [strings[0] + " zqx"] + strings[1:]
    n = 0
    for st in strings:
        n += 1
        if len(squash(st)) < 4:
            continue
        if squash(st) not in pool:
            fail(f"C10 quoted string of the narrative is in no record: {st[:70]}")
    print(f"narrative: {n} quoted strings checked")


def write_md(recs):
    qs = {}
    for q in recs:
        for x in re.split(r"[,\s]+", q.get("q", "")):
            if x:
                qs.setdefault(x, []).append(q["id"])
    out = ["# quotes.md: quotes with locations (generated by `check_quotes.py --write`; do not edit)", "",
           "Each entry: id, source and version, location in the paper, PDF page of the fetched PDF, TeX line(s) in the",
           "committed source, versions that contain the same quote, questions. The quote is the TeX source text",
           "(comments removed, whitespace collapsed). `check_quotes.py` proves each quote occurs in its source and each PDF",
           "fragment in its PDF. Records with `@lacks` state that a string is absent from the source (C7).", "",
           "Source keys: " + "; ".join(f"{k} = {v[2]}" for k, v in SRC.items()) + ".", "",
           "| question | ids |", "|---|---|"]
    for k in sorted(qs):
        out.append(f"| {k} | {', '.join(qs[k])} |")
    out.append("")
    for q in recs:
        srcs = q["src"].split()
        if "lacks" in q:
            out.append(f"### {q['id']}: {', '.join(SRC[s][2] for s in srcs)}, {q['loc']}")
            out.append(f"{q.get('q', '')}.")
            out.append("")
            out.append(f"> absent (TeX and PDF text, case-insensitive): {q['lacks']}. Present, as a control: {q['has']}.")
            out.append("")
            continue
        _, _, label, _ = SRC[srcs[0]]
        out.append(f"### {q['id']}: {label}, {q['loc']}")
        also = q.get("also", "").split()
        extra = f"; also in {', '.join(SRC[a][2] for a in also)}" if also else ""
        out.append(f"PDF p. {q.get('page', '?')}; TeX line {q.get('line', '?')} of `{SRC[srcs[0]][0]}`{extra}; {q.get('q', '')}.")
        out.append("")
        out.append("> " + collapse(q["tex"]).replace("\n", " "))
        if q.get("note"):
            out.append("")
            out.append(f"Note: {q['note']}")
        if q.get("absent"):
            out.append("")
            out.append(f"Not in {', '.join(SRC[a][2] for a in q['absent'].split())} (checked).")
        out.append("")
    (HERE / "quotes.md").write_text("\n".join(out), encoding="utf-8")


def main():
    recs = parse_records("quotes.txt")
    check_sha()
    recs = check_records(recs)
    check_proposal(recs)
    check_narrative(recs)
    if (HERE / "proposal.md").exists():  # C9
        flags = {"diff": ["--mutate=text"], "anchor": ["--mutate=anchor"]}.get(MUT, [])
        r = subprocess.run([sys.executable, "-I", str(HERE / "make_diff.py"), "--check"] + flags, capture_output=True, text=True)
        if r.returncode != 0:
            fail("C9 " + (r.stdout + r.stderr).strip().replace("\n", " | ")[:300])
        else:
            print(r.stdout.strip().splitlines()[-1])
    elif MUT in ("diff", "anchor"):
        fail(f"mutation {MUT} needs proposal.md, which is not present")
    if WRITE and not fails:
        write_md(recs)
    n = len(recs)
    srcs = ", ".join(f"{k}:{v}" for k, v in sorted(pdf_source.items()))
    print(f"{n} records, {len(fails)} failures" + (f" (mutation {MUT})" if MUT else "") + (f"; PDF text from {srcs}" if srcs else ""))
    if not fails and pdf_not_run:
        print("C2 NOT RUN: no pdftotext and no pdftext/ cache for " + ", ".join(sorted(set(pdf_not_run))))
        sys.exit(3)
    sys.exit(1 if fails else 0)


main()
