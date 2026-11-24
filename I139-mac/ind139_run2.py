#!/usr/bin/env python3
"""ind139: the coordinator's independent check of #139 (#2's bracket table against #104's, l = 2..3000).

Reads the two csv files with its own parser, checks the overlap and RESULTS.md 4.3's claims on both, checks that #2's table
is the same on the Mac and on rpi5, and re-solves c r_* and c r_neg at five l from Lemma A's chi in mpmath (the N root and
the largest zero of V-hat = 2g^2 - V), a route neither #2 (rescaled series, exact intervals) nor #104 (mpmath iv) uses.
Shares no code with compare_brackets.py, threshold_isolation.py, rescaled.py or #104's scripts. Criteria K1-K4 in README.md.
"""
import argparse
import csv
import sys
from fractions import Fraction as Fr
from math import factorial

import mpmath as mp

ap = argparse.ArgumentParser()
ap.add_argument('--ours', required=True)     # I139-rpi5/brackets_i2.csv (#2, exact p/q)
ap.add_argument('--theirs', required=True)   # I104-rpi5/sweep_brackets.csv (#104, 20-digit decimals)
ap.add_argument('--mac', required=True)      # the Mac rerun's brackets_i2_mac.csv
ap.add_argument('--mutate', default='')
args = ap.parse_args()
MUT = args.mutate
FAIL = []


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}", flush=True)
    if not ok:
        FAIL.append(name)


def load(path):
    with open(path, newline='') as fh:
        rd = csv.reader(fh)
        head = next(rd)
        rows = [r for r in rd if r]
    return head, rows


COLS = ['rstar_lo', 'rstar_hi', 'rneg_lo', 'rneg_hi']


def table(path):
    head, rows = load(path)
    ix = {h: head.index(h) for h in ['l', 'c'] + COLS}
    out, dup = {}, 0
    for r in rows:
        l = int(r[ix['l']])
        dup += l in out
        out[l] = dict(c=int(r[ix['c']]), **{k: Fr(r[ix[k]]) for k in COLS})
    return out, dup, len(rows)


A, dupA, nA = table(args.ours)
B, dupB, nB = table(args.theirs)
if MUT == 'shift':   # shift: #2's c r_* bracket at l = 2222 moved up by 1e-12
    A[2222]['rstar_lo'] += Fr(1, 10**12)
    A[2222]['rstar_hi'] += Fr(1, 10**12)
if MUT == 'mono':    # mono: #2's rows l = 1000 and 1001 exchanged
    A[1000], A[1001] = A[1001], A[1000]

# K1: the comparison
L = set(range(2, 3001))
okc = all(T[l]['c'] == (l + 2) * (l - 1) for T in (A, B) for l in T)
okw = all(T[l][k + '_lo'] < T[l][k + '_hi'] for T in (A, B) for l in T for k in ('rstar', 'rneg'))
ovl, gap, bad = None, Fr(0), []
for l in sorted(L & set(A) & set(B)):
    for k in ('rstar', 'rneg'):
        o = min(A[l][k + '_hi'], B[l][k + '_hi']) - max(A[l][k + '_lo'], B[l][k + '_lo'])
        if o < 0:
            bad.append((l, k))
        ovl = o if ovl is None else min(ovl, o)
        mid = abs((A[l][k + '_lo'] + A[l][k + '_hi']) - (B[l][k + '_lo'] + B[l][k + '_hi'])) / 2
        gap = max(gap, mid)
wA = max(A[l][k + '_hi'] - A[l][k + '_lo'] for l in A for k in ('rstar', 'rneg'))
wB = max(B[l][k + '_hi'] - B[l][k + '_lo'] for l in B for k in ('rstar', 'rneg'))
claims = abs(float(wA) / 2.0e-13 - 1) < 0.01 and abs(float(wB) / 2.0e-14 - 1) < 0.01 and abs(float(gap) / 4.59e-15 - 1) < 0.01
check('K1', set(A) == L and set(B) == L and nA == nB == 2999 and not dupA and not dupB and okc and okw and not bad and claims,
      f"rows {nA}, {nB}, l sets = 2..3000 {set(A) == L}, {set(B) == L}; c = (l+2)(l-1) {okc}; lo < hi {okw}; disjoint pairs "
      f"{len(bad)} {bad[:3]}; smallest overlap {float(ovl):.6e}; widest #2 {float(wA):.6e}, #104 {float(wB):.6e}; largest "
      f"midpoint gap {float(gap):.6e} (claims 2.0e-13, 2.0e-14, 4.59e-15: {claims})")

# K2: #2's table is the same on the Mac and on rpi5
ma, mb = open(args.mac, 'rb').read(), open(args.ours, 'rb').read()
if MUT == 'bytes':   # bytes: one digit of the Mac file changed
    i = ma.index(b'\n') + 10
    ma = ma[:i] + (b'1' if ma[i:i + 1] != b'1' else b'2') + ma[i + 1:]
check('K2', ma == mb, f"Mac csv {len(ma)} bytes, rpi5 csv {len(mb)} bytes, identical {ma == mb}")

# K3: RESULTS 4.3's claims, on #2's table and on #104's, every l
RHO_S_LO, RHO_S_HI = Fr('8.485700966'), Fr('8.485700968')   # rho_* = 8.485700967... (RESULTS 4.4)
RHO_N_LO, RHO_N_HI = Fr('9.635989442'), Fr('9.635989444')   # rho_neg = 9.635989443...
if MUT == 'rho':     # rho: rho_* taken as 8.4858
    RHO_S_LO = RHO_S_HI = Fr('8.4858')
for nm, T in (('#2', A), ('#104', B)):
    order = all(T[l]['rstar_hi'] < T[l]['rneg_lo'] for l in range(2, 3001))
    dec = all(T[l + 1][k + '_hi'] < T[l][k + '_lo'] for l in range(2, 3000) for k in ('rstar', 'rneg'))
    above = all(T[l]['rstar_lo'] > RHO_S_HI and T[l]['rneg_lo'] > RHO_N_HI for l in range(2, 3001))
    sc = lambda l: Fr(l * l, (l + 2) * (l - 1))
    inc = all(sc(l + 1) * T[l + 1][k + '_lo'] > sc(l) * T[l][k + '_hi'] for l in range(5, 3000) for k in ('rstar', 'rneg'))
    min5 = all(sc(5) * T[5][k + '_hi'] < sc(l) * T[l][k + '_lo'] for l in range(2, 3001) if l != 5 for k in ('rstar', 'rneg'))
    below = all(sc(l) * T[l]['rstar_hi'] < RHO_S_LO and sc(l) * T[l]['rneg_hi'] < RHO_N_LO for l in range(3, 3001))
    v5 = (float(sc(5) * T[5]['rstar_lo']), float(sc(5) * T[5]['rneg_lo']))
    ok5 = abs(v5[0] - 7.6826) < 5e-5 and abs(v5[1] - 8.7803) < 5e-5
    check(f'K3:{nm}', order and dec and above and inc and min5 and below and ok5,
          f"r_* < r_neg {order}; c r decreasing {dec}; above rho {above}; l^2 r increasing from l = 5 {inc}; minimum at l = 5 "
          f"{min5} ({v5[0]:.6f}, {v5[1]:.6f}; RESULTS 7.6826, 8.7803); below rho for l >= 3 {below}")

# K4: re-solve c r_* and c r_neg from Lemma A in mpmath
mp.mp.dps = 80


def poch(a, m):  # run 2: (a)_m for m < 0 is 1/((a-1)...(a-m)) (run 1 returned 1, so c_1 was wrong)
    if m < 0:
        p = 1
        for j in range(1, -m + 1):
            p *= a - j
        return Fr(1, p)
    p = 1
    for j in range(m):
        p *= a + j
    return p


def cn(l, n):
    v = Fr((n - 2) * ((n - 4) * l * (l + 1) + n - 1) * poch(l - n + 3, 2 * n - 4), 2**n * factorial(n - 1)**2)
    if MUT == 'chi' and n == 3:   # chi: c_3 scaled by 1 + 1e-6
        v *= Fr(1000001, 1000000)
    return v


rows4, ok4 = [], True
for l in (2, 3, 10, 100, 1500):
    c = (l + 2) * (l - 1)
    a = [mp.mpf(0)] + [mp.mpf(x.numerator) / x.denominator for x in (cn(l, n) * Fr(c)**(1 - n) for n in range(1, l + 3))]
    da = [n * a[n] for n in range(len(a))]
    def hor(cf, p):
        v = mp.mpf(0)
        for x in reversed(cf):
            v = v * p + x
        return v
    X = lambda p: hor(a, p)            # X(rho) = c chi(rho/c) = sum a_n rho^n
    dX = lambda p: hor(da[1:], p)
    N = lambda p: X(p) - (p - 6) * dX(p)

    def Vh(p):
        r = p / c
        f = 1 + 2 / r
        g = f * c * (dX(p) / X(p) - 1 / (p - 6))   # g = f psi0'/psi0, psi0 = chi/(c r - 6), d/dr = c d/drho
        lam = mp.mpf(c) / 2
        V = 2 * f * (lam**2 * r**2 * ((lam + 1) * r - 3) + 9 * (lam * r - 1)) / (r**3 * (lam * r - 3)**2)
        return 2 * g**2 - V

    def roots(fn, lo, hi, step):
        out, p, fp = [], mp.mpf(lo), fn(mp.mpf(lo))
        while p < hi:
            q = p + step
            fq = fn(q)
            if fp * fq < 0:
                x, y, fx = p, q, fp
                for _ in range(200):
                    m = (x + y) / 2
                    fm = fn(m)
                    if fm * fx > 0:
                        x, fx = m, fm
                    else:
                        y = m
                out.append((x + y) / 2)
            p, fp = q, fq
        return out

    rs = roots(N, mp.mpf(6) + mp.mpf('1e-6'), 20, mp.mpf('0.01'))
    rn = roots(Vh, rs[0] + mp.mpf('1e-9'), 40, mp.mpf('0.01')) if rs else []
    inside = lambda x, T, k: T[l][k + '_lo'] <= Fr(mp.nstr(x, 40)) <= T[l][k + '_hi']
    okl = len(rs) == 1 and len(rn) == 1
    if okl:
        okl = all(inside(rs[0], T, 'rstar') and inside(rn[0], T, 'rneg') for T in (A, B))
    ok4 = ok4 and okl
    rows4.append(f"l = {l}: N roots on (6, 20] {[mp.nstr(x, 16) for x in rs]}, V-hat zeros on (c r_*, 40] "
                 f"{[mp.nstr(x, 16) for x in rn]}, inside both brackets {okl}")
check('K4', ok4, '; '.join(rows4))

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL))
sys.exit(1 if FAIL else 0)
