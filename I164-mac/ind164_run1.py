#!/usr/bin/env python3
"""ind164: the coordinator's independent check of #164 (slow-rotation and charged-wormhole papers).

Criteria P0-P4 in negative-mass-raw I164-mac/README.md. Imports nothing from I164-rpi5.
usage: python3 -I ind164.py DATA_DIR DATA152_DIR [--mutate=NAME]
"""
import hashlib
import json
import math
import re
import sys
import time
import unicodedata
from pathlib import Path

MUTS = ['sha', 'author', 'quote', 'absent', 'area', 'cross']
args = [a for a in sys.argv[1:] if not a.startswith('--mutate=')]
MUT = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mutate=')), '')
if MUT and MUT not in MUTS:
    sys.exit(f"unknown mutation {MUT!r}; known: {MUTS}")
D, D152 = Path(args[0]), Path(args[1])
HERE = Path(__file__).resolve().parent
FAIL = []
T0 = time.time()


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}  ({time.time() - T0:.1f} s)", flush=True)
    if not ok:
        FAIL.append(name)


TEX = {'L': D / 'x_2301.05243v2/paper8.tex', 'M': D / 'x_2403.08387v1/main.tex', 'H': D / 'x_2510.11406v2/main.tex',
       'N': D / 'x_2607.18399v2/main.tex', 'G': D152 / 'x_2610.38659v1/main.tex', 'S': D152 / 'x_2610.29941v2/research.tex'}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'(?<!\\)%.*', '', s)
    s = re.sub(r'\\cite[a-z]*\{[^}]*\}', '', s)
    s = re.sub(r'\\(emph|textit|textbf|mathrm|rm|it|bf|text)\b', '', s)
    s = s.replace('~', ' ').replace('$', '').replace('{', '').replace('}', '')
    s = s.replace('``', '"').replace("''", '"')
    return re.sub(r'\s+', ' ', s)


raw = {k: p.read_text(encoding='utf-8', errors='replace') for k, p in TEX.items()}
src = {k: norm(v) for k, v in raw.items()}
nospace = lambda s: re.sub(r'\s+', '', s)

# P0 -------------------------------------------------------------------------------------------------------------
print("== P0: sources ==")
want = {}
for line in (HERE.parent / 'I164-rpi5/sha256sums.txt').read_text().splitlines():
    h, name = line.split()
    want[name] = h
mine = {'src/2301.05243v1/sr_ellis.tex': D / 'x_2301.05243v1/sr_ellis.tex', 'src/2301.05243v2/paper8.tex': TEX['L'],
        'src/2403.08387v1/main.tex': TEX['M'], 'src/2510.11406v1/main.tex': D / 'x_2510.11406v1/main.tex',
        'src/2510.11406v2/main.tex': TEX['H'], 'src/2607.18399v1/main.tex': D / 'x_2607.18399v1/main.tex',
        'src/2607.18399v2/main.tex': TEX['N']}
for v in ('2301.05243v1', '2301.05243v2', '2403.08387v1', '2510.11406v1', '2510.11406v2', '2607.18399v1', '2607.18399v2'):
    mine[f'dl/{v}/pdf'] = D / f'pdf_{v}.pdf'
if MUT == 'sha':
    k = 'src/2403.08387v1/main.tex'
    want[k] = ('0' if want[k][0] != '0' else '1') + want[k][1:]
bad = [n for n, p in mine.items() if hashlib.sha256(p.read_bytes()).hexdigest() != want.get(n)]
check('P0', not bad and len(mine) == 15, f"{len(mine) - len(bad)} of {len(mine)} files match; differ: {bad}")

# P1 -------------------------------------------------------------------------------------------------------------
print("\n== P1: metadata ==")
api = (D / 'api.xml').read_text(encoding='utf-8')
entries = {}
for e in re.findall(r'<entry>(.*?)</entry>', api, re.S):
    aid = re.search(r'<id>https?://arxiv.org/abs/([0-9.]+)v\d+</id>', e).group(1)
    title = re.sub(r'\s+', ' ', re.search(r'<title>(.*?)</title>', e, re.S).group(1)).strip()
    names = [n.strip() for n in re.findall(r'<name>(.*?)</name>', e)]
    entries[aid] = (title, names)


def vdates(aid):
    t = re.sub(r'<[^>]+>', ' ', (D / f'abs_{aid}.html').read_text(encoding='utf-8'))
    return dict(re.findall(r'\[(v\d)\]\s+\w{3}, (\d{1,2} \w{3} \d{4})', t))


def jref(aid):
    js = json.loads((D / f'inspire_{aid}.json').read_text(encoding='utf-8'))
    hits = js['hits']['hits']
    if not hits:
        return None
    pis = hits[0]['metadata'].get('publication_info', [])
    for pi in pis:
        if 'journal_title' in pi:
            return f"{pi['journal_title']} {pi.get('journal_volume', '')} {pi.get('artid', pi.get('page_start', ''))}"
    return None


A4 = ['Azad', 'Blázquez-Salcedo', 'Kho' if MUT == 'author' else 'Khoo', 'Kunz']
A5 = ['Blázquez-Salcedo', 'González-Romero', 'Khoo', 'Kunz', 'Navarro Moreno']
exp = {'2301.05243': ("Are slowly rotating Ellis-Bronnikov wormholes stable?", A4, ('v2', '23 Nov 2023'), 'Phys.Lett.B 848 138349'),
       '2403.08387': ("Radial perturbations of Ellis-Bronnikov wormholes in slow rotation up to second order", A4,
                      ('v1', '13 Mar 2024'), 'Phys.Rev.D 109 124051'),
       '2510.11406': ("Radial perturbations of charged wormholes", A5, ('v2', '13 Mar 2026'), 'Phys.Lett.B 875 140335'),
       '2607.18399': ("Nonradial perturbations of static charged wormholes", A5, ('v2', '8 Oct 2026'), 'Phys.Rev.D 114 084019')}
p1, msgs = True, []
for aid, (title, surn, (v, d), jr) in exp.items():
    t, names = entries.get(aid, ('', []))
    ok_t = t.lower() == title.lower()
    ok_a = len(names) == len(surn) and all(n.endswith(s) for n, s in zip(names, surn))
    vd = vdates(aid)
    ok_d = vd.get(v) == d and f'v{int(v[1:]) + 1}' not in vd
    got = jref(aid)
    ok_j = got is not None and nospace(got) == nospace(jr)
    p1 &= ok_t and ok_a and ok_d and ok_j
    msgs.append(f"{aid}: title {ok_t}, authors {ok_a}, latest {v} {vd.get(v)} {ok_d}, journal {got!r} {ok_j}")
check('P1', p1, "; ".join(msgs))

# P2 -------------------------------------------------------------------------------------------------------------
print("\n== P2: quoted strings ==")
Q = [('L', "for every value of C we have studied"), ('L', "merge and vanish" if MUT == 'quote' else "merge and disappear"),
     ('L', "slightly above 30\\%"), ('L', "the radial instability will disappear at even smaller values of the angular momentum"),
     ('L', "for sufficiently rapid rotation the wormholes will be stable"),
     ('L', "is indicating a deficiency of the applied quadratic approximation"),
     ('M', "independent of C"),
     ('M', "is slightly smaller than the angular momentum, where the two perturbatively obtained branches of unstable radial modes cross"),
     ('M', "will need more sophisticated methods than perturbation theory"), ('M', "excellent approximations for most of the range"),
     ('M', "up to 50-60"), ('H', "have two radially unstable modes"), ('H', "merged around 1/3"),
     ('H', "can only be confirmed by a non-perturbative study"),
     ('H', "one might be tempted to conjecture that the radial instability disappears at the critical value"),
     ('H', "not yet fully radially stable"), ('H', "two modes that possess the same imaginary part but opposite real parts"),
     ('N', "will therefore be relaxed for fast rotation"), ('N', "should be clarified"),
     ('N', "does not seem to completely vanish as long as"),
     ('G', "can now be recognized as the same characteristic spectral mechanism"),
     ('S', "the zero of their second-order rate for this family"), ('S', "33\\%")]
miss = [(k, q) for k, q in Q if q not in src[k]]
check('P2', not miss, f"{len(Q) - len(miss)} of {len(Q)} found; missing: {miss}")

# P3 -------------------------------------------------------------------------------------------------------------
print("\n== P3: absent strings ==")
ABS = [(k, '33\\%') for k in 'LMHN'] + [(k, s) for k in 'HN' for s in ('oscillating growth', 'oscillatory instability')]
ABS += [(k, s) for k in 'LM' for s in ('nearly symmetric', 'reliable range')]
if MUT == 'absent':
    ABS.append(('H', 'merged around 1/3'))
present = [(k, s) for k, s in ABS if nospace(s).lower() in nospace(src[k]).lower()]
check('P3', not present, f"{len(ABS) - len(present)} of {len(ABS)} absent as required; present: {present}")

# P4 -------------------------------------------------------------------------------------------------------------
print("\n== P4: re-solve from the printed tables ==")


def tabulars(text):
    text = re.sub(r'(?<!\\)%.*', '', text)
    out = []
    for m in re.finditer(r'\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}', text, re.S):
        rows = []
        for r in m.group(1).replace('\\hline', ' ').split('\\\\'):
            cells = [c.strip() for c in r.split('&')]
            try:
                rows.append([float(c) for c in cells])
            except ValueError:
                continue
        out.append((m.end(), rows))
    return out


def table_by_label(text, label):
    i = text.index('\\label{' + label + '}')
    cands = [rows for end, rows in tabulars(text) if end < i]
    return cands[-1]


main_M = {r[0]: (r[1], r[2]) for r in table_by_label(raw['M'], 'ImOm_coeff_main_moreC')}
sec_M = {r[0]: r[1] for r in table_by_label(raw['M'], 'ImOm_coeff_sec')}
tl = tabulars(raw['L'])
main_L = {r[0]: (r[1], r[2]) for r in tl[0][1]}
sec_L = {r[0]: r[1] for r in tl[1][1]}
agree = all(main_L[c] == main_M[c] for c in main_L if c in main_M) and all(sec_L[c] == sec_M[c] for c in sec_L if c in sec_M)
area_ok = nospace('A=4\\pi r_0^2 e^\\frac\\pi C2r_0') in nospace(src['L'])
A = (lambda C: 4 * math.pi) if MUT == 'area' else (lambda C: 4 * math.pi * math.exp(math.pi * C / 2))
w0, Dm = main_M[1.0]
Jc = math.sqrt(-w0 / Dm)
pc = 100 * 8 * math.pi * Jc / A(1.0)
cross = {}
main_all = {**main_L, **main_M}
for C in (0.0, 0.05, 0.1, 0.2):
    w0c, Dc = main_all[C]
    Ds = sec_L[C]
    Jx = math.sqrt(-w0c / ((Dc + Ds) if MUT == 'cross' else (Dc - Ds)))
    cross[C] = (Jx / A(C), 100 * 8 * math.pi * Jx / A(C))
want_x = {0.0: 32.6, 0.05: 32.8, 0.1: 32.9, 0.2: 33.0}
okx = all(round(cross[C][1], 1) == want_x[C] and round(cross[C][0], 3) == 0.013 for C in cross)
p4 = agree and area_ok and round(pc, 1) == 41.9 and okx
check('P4', p4, f"L and M tables agree where shared: {agree}; area formula in L: {area_ok}; C = 1: J_c = {Jc:.5f}, "
      f"8 pi J_c/A = {pc:.2f} %; crossings (J_x/A, 8 pi J_x/A %): "
      f"{ {C: (round(a, 5), round(b, 2)) for C, (a, b) in cross.items()} }")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.1f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)
