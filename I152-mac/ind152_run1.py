#!/usr/bin/env python3
"""ind152: the coordinator's independent check of #152 (reading of the rotating-wormhole stability papers).

Criteria P0-P5 in negative-mass-raw I152-mac/README.md. Imports nothing from I152-rpi5.
usage: python3 -I ind152.py DATA_DIR [--mutate=NAME]   (DATA_DIR: the coordinator's fetch, with x_<id>/ unpacked)
"""
import hashlib
import html
import math
import re
import sys
import time
import unicodedata
from pathlib import Path

MUTS = ['sha', 'author', 'date', 'quote', 'number', 'v1v2', 'G1']
args = [a for a in sys.argv[1:] if not a.startswith('--mutate=')]
MUT = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mutate=')), '')
if MUT and MUT not in MUTS:
    sys.exit(f"unknown mutation {MUT!r}; known: {MUTS}")
DATA = Path(args[0])
HERE = Path(__file__).resolve().parent
FAIL = []
T0 = time.time()


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}  ({time.time() - T0:.1f} s)", flush=True)
    if not ok:
        FAIL.append(name)


TEX = {'D': DATA / 'x_1309.2448v1/rotworm.tex', 'A': DATA / 'x_2610.38659v1/main.tex',
       'S1': DATA / 'x_2610.29941v1/research.tex', 'S': DATA / 'x_2610.29941v2/research.tex'}


def norm_tex(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'(?<!\\)%.*', '', s)  # comments
    s = re.sub(r'\\cite[a-z]*\{[^}]*\}', '', s)
    s = re.sub(r'\\(emph|textit|textbf|mathrm|rm|it|bf|text)\b', '', s)
    s = s.replace('~', ' ').replace('$', '').replace('{', '').replace('}', '')
    s = s.replace('``', '"').replace("''", '"')
    return re.sub(r'\s+', ' ', s)


def nospace(s):
    return re.sub(r'\s+', '', s)


src = {k: norm_tex(p.read_text(encoding='utf-8', errors='replace')) for k, p in TEX.items()}

# P0 -------------------------------------------------------------------------------------------------------------
print("== P0: sources ==")
want = {}
for line in (HERE.parent / 'I152-rpi5/sha256sums.txt').read_text().splitlines():
    h, name = line.split()
    want[name] = h
mine = {'src/1309.2448/rotworm.tex': TEX['D'], 'src/2610.38659/main.tex': TEX['A'],
        'src/2610.29941v1/research.tex': TEX['S1'], 'src/2610.29941v2/research.tex': TEX['S'],
        'pdf/1309.2448.pdf': DATA / 'pdf_1309.2448v1.pdf', 'pdf/2610.38659.pdf': DATA / 'pdf_2610.38659v1.pdf',
        'pdf/2610.29941v1.pdf': DATA / 'pdf_2610.29941v1.pdf', 'pdf/2610.29941v2.pdf': DATA / 'pdf_2610.29941v2.pdf'}
if MUT == 'sha':
    h = want['src/2610.38659/main.tex']
    want['src/2610.38659/main.tex'] = ('0' if h[0] != '0' else '1') + h[1:]
bad = [n for n, p in mine.items() if hashlib.sha256(p.read_bytes()).hexdigest() != want.get(n)]
check('P0', not bad and len(mine) == len(want), f"{len(mine) - len(bad)} of {len(want)} files match rpi5's sha256; differ: {bad}")

# P1 -------------------------------------------------------------------------------------------------------------
print("\n== P1: arXiv metadata ==")
api = (DATA / 'api.xml').read_text(encoding='utf-8')
entries = {}
for e in re.findall(r'<entry>(.*?)</entry>', api, re.S):
    aid = re.search(r'<id>http[s]?://arxiv.org/abs/([0-9.]+)v\d+</id>', e).group(1)
    title = re.sub(r'\s+', ' ', html.unescape(re.search(r'<title>(.*?)</title>', e, re.S).group(1))).strip()
    names = [html.unescape(n).strip() for n in re.findall(r'<name>(.*?)</name>', e)]
    jr = re.search(r'<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>', e, re.S)
    entries[aid] = (title, names, jr.group(1).strip() if jr else '')


def vdates(aid):
    t = (DATA / f'abs_{aid}.html').read_text(encoding='utf-8')
    t = re.sub(r'<[^>]+>', ' ', t)
    return dict(re.findall(r'\[(v\d)\]\s+\w{3}, (\d{1,2} \w{3} \d{4})', t))


exp = {
    '2610.38659': ("Exact rotating wormholes in five dimensions and their exceptional-point instability",
                   ['Blázquez-Salcedo', 'González-Romero', 'Kho' if MUT == 'author' else 'Khoo', 'Kleihaus', 'Kunz',
                    'Navarro Moreno'], None, ('v1', '28 Oct 2026')),
    '2610.29941': ("Rotation slows the instability of Ellis-Bronnikov wormholes", ['Shirokov', 'Nachevsky'], None,
                   ('v2', '7 Nov 2026' if MUT == 'date' else '6 Nov 2026')),
    '1309.2448': ("Rotating wormholes in five dimensions", ['Dzhunushaliev', 'Folomeev', 'Kleihaus', 'Kunz', 'Radu'],
                  'Phys. Rev. D 88, 124028 (2013)', None),
}
p1, msgs = True, []
for aid, (title, surn, jref, vd_want) in exp.items():
    t, names, jr = entries.get(aid, ('', [], ''))
    ok_t = t.lower() == title.lower()
    ok_a = len(names) == len(surn) and all(n.endswith(s) for n, s in zip(names, surn))
    ok_j = jref is None or jr == jref
    vd = vdates(aid)
    ok_d = vd_want is None or vd.get(vd_want[0]) == vd_want[1]
    p1 &= ok_t and ok_a and ok_j and ok_d
    msgs.append(f"{aid}: title {ok_t}, authors {ok_a} ({', '.join(names)}), journal {ok_j} ({jr}), dates {vd} {ok_d}")
check('P1', p1, "; ".join(msgs))

# P2 -------------------------------------------------------------------------------------------------------------
print("\n== P2: quoted strings ==")
QUOTES = [('D', "within the type of modes investigated"), ('D', "may stabilize wormholes"),
          ('D', "no new unstable modes of a different type appear"),
          ('D', "vanishes when the angular momentum exceeds some critical value"),
          ('A', "no stabilization" if MUT == 'quote' else "not stabilization"), ('A', "correctly located the merger"),
          ('S', "evidence of prolonged radial stability"), ('S', "bound growth only over that span"),
          ('S', "without identifying a second eigenmode")]
miss = [(k, q) for k, q in QUOTES if q not in src[k]]
check('P2', not miss, f"{len(QUOTES) - len(miss)} of {len(QUOTES)} quoted strings found; missing: {miss}")

# P3 -------------------------------------------------------------------------------------------------------------
print("\n== P3: numbers ==")
NUMS = [('D', '0.10063'), ('D', '0.1381'), ('A', '0.100629' if MUT == 'number' else '0.100628'), ('A', '2.190024'),
        ('A', '0.48717')]
NUMS += [('S', n) for n in ('150', '28', '81', '5.4', '13.3', '24', '32', '33', '28.8', '0.2', '80.8')]
STRS = [('A', '10^-6'), ('A', '(|J|/A-0.5)^6'), ('S', '128/192/256'), ('S', 'D90'), ('S', 'D75'), ('S', 'D80'),
        ('S', 'G=c=1')]
missn = [(k, n) for k, n in NUMS if not re.search(r'(?<![\d.])' + re.escape(n) + r'(?![\d])', src[k])]
misss = [(k, s_) for k, s_ in STRS if nospace(s_) not in nospace(src[k])]
check('P3', not missn and not misss, f"{len(NUMS) - len(missn)} of {len(NUMS)} numbers, {len(STRS) - len(misss)} of "
      f"{len(STRS)} strings found; missing: {missn + misss}")

# P4 -------------------------------------------------------------------------------------------------------------
print("\n== P4: [SN26b] v1 against v2 ==")
v1, v2 = ('S', 'S1') if MUT == 'v1v2' else ('S1', 'S')
V1ONLY = ["no evidence of instability", "addresses the four-dimensional stability question"]
p4 = [(q, q in src[v1], q not in src[v2]) for q in V1ONLY]
check('P4', all(a and b for _, a, b in p4), f"(phrase, in v1, absent from v2): {p4}")

# P5 -------------------------------------------------------------------------------------------------------------
print("\n== P5: |J|/A from the exact solution ==")


def j_over_a(lam, G):
    s = math.pi * lam / 4
    e2a = math.sin(s)**2 / (1 - math.cos(s))
    eq = lam * math.sin(s) / (2 * (1 - math.cos(s)))
    kap = math.sqrt(-lam**3 * math.cos(s) / (16 * math.sin(s)**3))
    p = 0.5
    return kap * math.sqrt(e2a * eq) / (32 * math.pi * G * p**1.5)


Gpass = 1.0 if MUT == 'G1' else 1 / (4 * math.pi)
Gfail = 1 / (4 * math.pi) if MUT == 'G1' else 1.0
CASES = [(2.190024, 0.100628, 6), (2.059523, 0.05475, 5), (3.948341, 0.48717, 5)]
okp = [(lam, round(j_over_a(lam, Gpass), nd) == v, j_over_a(lam, Gpass)) for lam, v, nd in CASES]
okf = [round(j_over_a(lam, Gfail), nd) != v for lam, v, nd in CASES]
lim = j_over_a(4 - 1e-9, Gpass)
pat = [r'G=1', r'4\\piG=1', r'8\\piG=1', r'16\\piG=1']
hits = [(k, pt) for k in ('A', 'D') for pt in pat if re.search(r'(?<![A-Za-z])' + pt, nospace(src[k]))]
p5 = all(o for _, o, _ in okp) and all(okf) and abs(lim - 0.5) < 1e-6 and not hits
check('P5', p5, f"with G = {Gpass:.6f}: {[(l, round(v, 8), o) for l, o, v in okp]}; lambda -> 4: {lim:.9f}; with G = {Gfail:.6f} "
      f"none rounds: {all(okf)}; G-fixing statements in the 5D sources: {hits}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.1f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)
