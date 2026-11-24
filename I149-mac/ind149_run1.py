#!/usr/bin/env python3
"""ind149: the coordinator's independent check of #149 (DG06 and DG08 across arXiv versions). Criteria P1-P5 in I149-mac/README.md.

Fetches the five arXiv e-prints itself into --dl (GET only), unpacks them there, and reads the TeX with its own patterns.
Shares no code with I149-rpi5's scripts; reads the expected sha256 values from I149-rpi5/fetch.log.
"""
import argparse
import gzip
import hashlib
import io
import os
import re
import sys
import tarfile
import urllib.request

import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument('--raw', required=True)          # negative-mass-raw
ap.add_argument('--dl', required=True)           # empty download folder
ap.add_argument('--mutate', default='')
args = ap.parse_args()
MUT = args.mutate
FAIL = []
UA = {'User-Agent': 'research-client/1.0'}


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}", flush=True)
    if not ok:
        FAIL.append(name)


def sha(b):
    return hashlib.sha256(b).hexdigest()


# expected hashes from I149-rpi5/fetch.log
log = open(os.path.join(args.raw, 'I149-rpi5', 'fetch.log')).read().splitlines()
exp_bin, exp_tex = {}, {}
for i, ln in enumerate(log):
    m = re.match(r'^https://arxiv\.org/e-print/(\S+) 200 ', ln)
    if m and i + 1 < len(log):
        h = log[i + 1].split()[0]
        exp_bin[m.group(1)] = h
    m2 = re.match(r'^([0-9a-f]{64})\s+(dg0[68]_v\d)/(\S+\.tex)$', ln)
    if m2:
        exp_tex[m2.group(2)] = (m2.group(3), m2.group(1))
if MUT == 'hash':
    exp_bin['gr-qc/0604021v1'] = '0' * 64

VERS = {'dg06_v1': 'gr-qc/0604021v1', 'dg06_v2': 'gr-qc/0604021v2', 'dg08_v1': '0809.3615v1', 'dg08_v2': '0809.3615v2',
        'dg08_v3': '0809.3615v3'}
TEX, ok1, rows = {}, True, []
for key, ver in VERS.items():
    data = urllib.request.urlopen(urllib.request.Request(f'https://arxiv.org/e-print/{ver}', headers=UA), timeout=60).read()
    okb = sha(data) == exp_bin.get(ver)
    out = os.path.join(args.dl, key)
    os.makedirs(out, exist_ok=True)
    raw = gzip.decompress(data)
    texname, texhash = exp_tex[key]
    if raw[:262][257:262] == b'ustar' or tarfile.is_tarfile(io.BytesIO(raw)):
        with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
            tf.extractall(out, filter='data')
    else:
        open(os.path.join(out, texname), 'wb').write(raw)
    tb = open(os.path.join(out, texname), 'rb').read()
    okt = sha(tb) == texhash
    TEX[key] = tb.decode('utf-8', 'replace')
    ok1 = ok1 and okb and okt
    rows.append(f"{ver}: e-print {okb}, {texname} {okt}")
check('P1', ok1, '; '.join(rows))


def norm(s):
    return re.sub(r'\s+', '', s)


def block(tex, label):
    i = tex.index('\\label{%s}' % label)
    j = tex.index('\\end{', i)
    return tex[i:j]


# P2: labels by version
need = ['\\label{cz}', '\\label{nv1}', '\\label{im}']
lack_v1 = need + (['\\label{RW1}'] if MUT == 'v1lab' else [])
v1 = TEX['dg06_v1']
v2 = TEX['dg06_v2']
ok2 = not any(x in v1 for x in lack_v1) and 'Lemma 1' not in v1 and all(x in v2 for x in need) and 'Lemma 1' in v2
check('P2', ok2, f"v1 has {[x for x in lack_v1 if x in v1]}, 'Lemma 1' {'Lemma 1' in v1}; v2 lacks {[x for x in need if x not in v2]}, "
      f"'Lemma 1' {'Lemma 1' in v2}")

# P3: the printed forms in DG06 v2
cz = norm(block(v2, 'cz'))
want_cz = '-\\frac{2\\lambda^2}{3\\mu(2\\lambda+3)}' if MUT == 'minus' else '=\\left.\\frac{2\\lambda^2}{3\\mu(2\\lambda+3)}'
cz_ok = want_cz in cz and (MUT == 'minus' or '-\\frac{2\\lambda^2}' not in cz)
i = v2.index('\\label{nv1}')
nv1 = norm(v2[v2.rindex('\\begin{eqnarray}', 0, i): v2.index('\\end{eqnarray}', i)])
h1_ok = '{r(r+\\mu)(2\\lambdar-3\\mu)}' in nv1
h2_ok = '+\\frac{3\\mu^2-6\\lambda\\mur+4\\lambda^2r^2}{2r^2(2\\lambdar-3\\mu)^2}' in nv1
check('P3', cz_ok and h1_ok and h2_ok, f"(cz) right-hand side + 2 lambda^2/(3 mu (2 lambda + 3)) {cz_ok}; (nv1) H1 denominator "
      f"r (r+mu)(2 lambda r - 3 mu) {h1_ok}; H2 zeta term with + {h2_ok}")

# P4: DG08
d1 = TEX['dg08_v1']
near = [m.start() for m in re.finditer('sign error', d1)]
ok_v1 = any('(16)' in d1[max(0, k - 200): k + 200] for k in near)
cform = 'c_0=\\frac{\\lambda^2c_{-1}}{3M(3+2\\lambda)}'
ok_l = {}
for key in ('dg08_v2', 'dg08_v3'):
    t = TEX[key]
    k = t.find('{\\bf Lemma 1:}')
    ok_l[key] = k >= 0 and cform in norm(t[k:k + 1500])
bib = re.search(r'\\bibitem\{dg\}(.{0,200})', d1, re.S)
check('P4', ok_v1 and all(ok_l.values()), f"v1 'sign error' near '(16)' {ok_v1}; Lemma 1 with c_0 = lambda^2 c_-1/(3M(3+2 lambda)) "
      f"{ok_l}; v1 bibitem dg: {norm(bib.group(1))[:90] if bib else None!r}")

# P5: the conversion
r, lam, mu, M, cm1, c0, c1 = sp.symbols('r lambda mu M c_m1 c_0 c_1')
rs = 3 * mu / (2 * lam)
Psi = cm1 / (r - rs) + c0 + c1 * (r - rs)
zeta = sp.cancel((2 * lam * r - 3 * mu) * Psi)
ratio = sp.cancel(sp.diff(zeta, r).subs(r, rs) / zeta.subs(r, rs))
dg08 = (-1 if MUT == 'sign' else 1) * lam**2 / (3 * M * (3 + 2 * lam))
cstar = -2 * lam**2 / (3 * mu * (2 * lam + 3))
a5 = sp.simplify(ratio - c0 / cm1) == 0
b5 = sp.simplify(dg08.subs(M, -mu / 2) - cstar) == 0
check('P5', a5 and b5, f"zeta'/zeta at r_s = {ratio} (= c_0/c_-1 {a5}); DG08's c_0/c_-1 at M = -mu/2 equals c* {b5}")

for doi in ('10.1088/0264-9381/23/15/021', '10.1088/0264-9381/26/21/215002'):
    try:
        st = urllib.request.urlopen(urllib.request.Request('https://doi.org/' + doi, headers=UA), timeout=30).status
    except Exception as e:  # noqa: BLE001
        st = getattr(e, 'code', type(e).__name__)
    print(f"  observation: doi {doi}: {st}")
print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL))
sys.exit(1 if FAIL else 0)
