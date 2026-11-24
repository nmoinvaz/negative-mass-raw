#!/usr/bin/env python3
"""ind50: the coordinator's independent check of #50 (critical_ghost.md's reading gaps and the Frolov map).

Criteria H1-H5 in I50-mac/README.md. Fetches its own sources (GET only) into --dl; formulas typed from the fetched TeX.
Shares no code with I50-rpi5's scripts.
"""
import argparse
import gzip
import hashlib
import io
import json
import os
import re
import sys
import tarfile
import urllib.request

import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument('--raw', required=True)
ap.add_argument('--dl', required=True)
ap.add_argument('--mutate', default='')
args = ap.parse_args()
MUT = args.mutate
FAIL = []
UA = {'User-Agent': 'research-client/1.0'}


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}", flush=True)
    if not ok:
        FAIL.append(name)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def texts(data, out):
    """All .tex text of an e-print (gzip of one file, or a gzipped tar); '' if neither."""
    os.makedirs(out, exist_ok=True)
    try:
        raw = gzip.decompress(data)
    except OSError:
        return ''
    if tarfile.is_tarfile(io.BytesIO(raw)):
        with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
            tf.extractall(out, filter='data')
        t = ''
        for root, _, files in os.walk(out):
            for f in files:
                if f.endswith('.tex') or f.endswith('.bbl'):
                    t += open(os.path.join(root, f), encoding='utf-8', errors='replace').read() + '\n'
        return t
    open(os.path.join(out, 'main.tex'), 'wb').write(raw)
    return raw.decode('utf-8', 'replace')


# ---------------------------------------------------------------- H1
exp = {}
for ln in open(os.path.join(args.raw, 'I50-rpi5', 'fetch.log')):
    f = [x.strip() for x in ln.split(' | ')]
    if len(f) >= 5 and f[3].endswith('eprint.bin') and f[4].startswith('sha256 '):
        exp[f[2]] = f[4].split()[1]
URLS = {'brady': 'https://arxiv.org/e-print/gr-qc/9402023', 'fro': 'https://arxiv.org/e-print/gr-qc/9704040v1',
        'mae': 'https://arxiv.org/e-print/0811.2962v2', 'sn': 'https://arxiv.org/e-print/2610.13206v2',
        'cdk': 'https://arxiv.org/e-print/2406.02466v2'}
if MUT == 'hash':
    exp[URLS['fro']] = '0' * 64
T, rows, ok1 = {}, [], True
for k, u in URLS.items():
    d = get(u)
    h = hashlib.sha256(d).hexdigest()
    ok = h == exp.get(u)
    ok1 = ok1 and ok
    rows.append(f"{k} {ok}")
    T[k] = texts(d, os.path.join(args.dl, k))
check('H1', ok1, '; '.join(rows))

# ---------------------------------------------------------------- H2: each paper's solution in its own equations
u, v = sp.symbols('u v')
s, b, w = sp.symbols('s b w', positive=True)
alpha = (1 - s**2) / (4 * b**2)                 # Brady: s = sqrt(1 - 4 alpha beta), beta = b^2
beta = b**2
QB = alpha * v**2 + (-beta if MUT == 'brady' else beta) * u**2 - u * v
phiB = sp.log((2 * alpha * v - u * (1 + s)) / (2 * alpha * v - u * (1 - s))) / 2


def eqs(Q, ph, sgn):
    """sigma = 0 field equations in the form both papers print, with r = sqrt(Q); each returned value must vanish.
    sgn = -1: Brady, (r^2)_uv = -1; Frolov's (R^2)_uv + 1 = 0 is the same."""
    Qu, Qv = sp.diff(Q, u), sp.diff(Q, v)
    pu, pv = sp.diff(ph, u), sp.diff(ph, v)
    e3 = sp.diff(Q, u, v) + 1
    e4 = -Qu * Qv / (2 * Q**2) - 1 / Q + 2 * pu * pv                     # 2 sigma_uv - 2 r_u r_v / r^2 = 1/r^2 - 2 phi_u phi_v
    e5 = 2 * Q * sp.diff(Q, v, 2) - Qv**2 + 4 * Q**2 * pv**2             # 4 Q^{3/2} (r_vv + r phi_v^2)
    e6 = 2 * Q * sp.diff(Q, u, 2) - Qu**2 + 4 * Q**2 * pu**2
    e7 = 2 * sp.diff(ph, u, v) + Qv / Q * pu + Qu / Q * pv              # 2 phi_uv + (ln r^2)_v phi_u + (ln r^2)_u phi_v
    return [sp.cancel(sp.together(e)) for e in (e3, e4, e5, e6, e7)]


bB = [e == 0 for e in eqs(QB, phiB, -1)]
p = (w**2 - 1) / 4                               # Frolov: w = sqrt(1 + 4p)
QF = u**2 - u * v - p * v**2
phiF = sp.log(-(2 * p * v + u * (1 - w)) / (2 * p * v + u * (1 + w))) / 2
bF = [e == 0 for e in eqs(QF, phiF, -1)]
check('H2', all(bB) and all(bF), f"Brady (3)-(7) vanish {bB}; Frolov (es) vanish {bF}")

# ---------------------------------------------------------------- H3: the map U = b u, V = v / b, p = -alpha beta
U, V = b * u, v / b
pm = (alpha * beta) if MUT == 'pmap' else -alpha * beta
wm = sp.sqrt(sp.factor(1 + 4 * pm))
wm = s if sp.simplify(wm - s) == 0 else wm
QFm = U**2 - U * V - pm * V**2
phiFm = sp.log(-(2 * pm * V + U * (1 - wm)) / (2 * pm * V + U * (1 + wm))) / 2
a3 = sp.cancel(QFm - QB) == 0
sig = [g for g in (1, -1) if all(sp.cancel(sp.together(sp.diff(phiFm, x_) - g * sp.diff(phiB, x_))) == 0 for x_ in (u, v))]
b3 = len(sig) == 1
r_ = sp.sqrt(QB)
m_brady = -u * v * (1 - 4 * alpha * beta) / (4 * r_)
M_def = r_ * (1 + 2 * sp.diff(r_, u) * sp.diff(r_, v)) / 2            # 1 - 2m/r = 2 g^{uv} r_u r_v with g^{uv} = -1
c3 = sp.simplify(M_def - m_brady) == 0
d3 = sp.simplify(pm.subs(s, 1)) == 0 and sp.simplify(pm.subs(s, 0) + sp.Rational(1, 4)) == 0
check('H3', a3 and b3 and c3 and d3, f"(a) R^2 = r^2 {a3}; (b) sign sigma with Phi_F = sigma phi_B + const: {sig}; "
      f"(c) Brady's m = the definition's {c3}; (d) alpha = 0 <-> p = 0 and 4 alpha beta = 1 <-> p = -1/4 {d3}")

# ---------------------------------------------------------------- H4: Maeda's form
C1, C2 = alpha, beta
k = 1 / sp.sqrt(sp.pi) if MUT == 'maeda' else 1 / (2 * sp.sqrt(sp.pi))
z = (1 - 2 * C1 * (v / u)) / s
phiM = k * sp.atanh(z)
QM = -u * v + C1 * v**2 + C2 * u**2
sgM = [g for g in (1, -1) if all(sp.cancel(sp.together(2 * sp.sqrt(sp.pi) * g * sp.diff(phiM, x_) - sp.diff(phiB, x_))) == 0
                                 for x_ in (u, v))]
a4 = sp.cancel(QM - QB) == 0 if MUT != 'brady' else sp.cancel(QM - (alpha * v**2 + beta * u**2 - u * v)) == 0
check('H4', a4 and len(sgM) == 1, f"(roberts1) = Brady (8) with (C1, C2) = (alpha, beta) {a4}; sign with phi_B = s 2 sqrt(pi) phi_M + const: {sgM}")

# ---------------------------------------------------------------- H5: quotes
def norm(t):
    return re.sub(r'\s+', ' ', t).lower()


sn, cdk = norm(T['sn']), norm(T['cdk'])
q1 = 'do not establish the scaling' if MUT != 'quote' else 'do not establish the exponent'
h_sn = q1 in sn and 'consistent with a type-i critical solution' in sn
shi = texts(get('https://arxiv.org/e-print/2604.00071'), os.path.join(args.dl, 'shi'))
shn = norm(shi)
ctx = [shn[max(0, m.start() - 150): m.end() + 150] for m in re.finditer(r'stress', shn)]
half = [c for c in ctx if re.search(r'0\.5|1/2|\\frac\{1\}\{2\}|\\tfrac\{1\}\{2\}|half', c)]
h_shi = bool(half)
h_cdk = 'not a black hole' in cdk
ins = json.loads(get('https://inspirehep.net/api/arxiv/2610.38659'))
abst = norm(' '.join(a.get('value', '') for a in ins['metadata'].get('abstracts', [])))
h_ins = '0.100628' in abst and 'not stabilization' in abst
check('H5', h_sn and h_shi and h_cdk and h_ins, f"SN26 v2 quotes {h_sn}; Shi26a factor 1/2 near 'stress' {h_shi} "
      f"(source {'TeX' if shi else 'not TeX'}; first context: {half[0][:160] if half else None!r}); CDK24 'not a black hole' {h_cdk}; "
      f"INSPIRE 2610.38659 '0.100628' and 'not stabilization' {h_ins}")

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL))
sys.exit(1 if FAIL else 0)
