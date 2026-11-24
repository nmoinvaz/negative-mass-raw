#!/usr/bin/env python3
"""ind140: the coordinator's independent recount of #140's window counts from #96's and #75's stored arrays.

Per sector: mu = muA * vc and muB * vc (the arrays as stored), the cut = the modulus of the first eigenvalue of A, by
decreasing exact modulus, above 1e-3 with no eigenvalue of B within 1e-5 relative; the window = every eigenvalue with
exact |mu|^2 >= cut^2 (squares of the floats' exact rational values). Shares no code with retab.py, tanh_spectrum.py or
sector_numbers.py; shares the stored arrays and the definitions. Criteria W1-W6 in README.md.
"""
import argparse
import csv
import os
import sys
from fractions import Fraction as Fr

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--raw', default=os.path.expanduser('~/Source/negative-mass-raw'))
ap.add_argument('--mutate', default='')
args = ap.parse_args()
MUT = args.mutate
FAIL = []
TOL = 1e-4 if MUT == 'tol4' else 1e-5   # tol4: the match tolerance 1e-4


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}", flush=True)
    if not ok:
        FAIL.append(name)


def sq(z):
    return Fr(float(z.real))**2 + Fr(float(z.imag))**2


def sector(path, sig=None, m=None):
    d = np.load(path)
    vc = float(d['vc'])
    A, B = d['muA'] * vc, d['muB'] * vc
    a2 = np.abs(A)
    top = np.argsort(-a2)[:400]                     # candidates; exact order among them
    qa = {int(i): sq(A[i]) for i in top}
    order = sorted(qa, key=lambda i: -qa[i])
    cut2, kz = None, None
    for i in order:
        if qa[i] < Fr(1, 10**6):                    # floor 1e-3 on |mu| v_c
            break
        rel = np.min(np.abs(B - A[i])) / a2[i]
        if rel > TOL:
            if abs(rel / TOL - 1) < 1e-6:
                print(f"  note: {path}: eigenvalue {i} within 1e-6 of the tolerance ({rel:.9e})")
            cut2, kz = qa[i], A[i]
            break
    if cut2 is None:
        return None
    if MUT == 'pair' and (sig, m) == (16, 7.5):
        j = int(np.argmin(np.abs(A - np.conj(kz))))
        A = np.delete(A, j)
    lo2 = max(cut2, Fr(1, 10**6))
    candA = [z for z in A[np.abs(A) > np.sqrt(float(lo2)) * (1 - 1e-9)]]
    candB = [z for z in B[np.abs(B) > np.sqrt(float(lo2)) * (1 - 1e-9)]]
    if MUT == 'strict':                               # strict: the window is |mu| > cut
        wA = [z for z in candA if sq(z) > lo2]
        wB = [z for z in candB if sq(z) > lo2]
    else:
        wA = [z for z in candA if sq(z) >= lo2]
        wB = [z for z in candB if sq(z) >= lo2]
    ties = [z for z in candA if sq(z) == cut2]
    others = [abs(float(sq(z) - cut2)) for z in A[np.abs(A) > np.sqrt(float(cut2)) * 0.9] if sq(z) != cut2]
    margin = min(others) / (2 * np.sqrt(float(cut2))) if others else float('inf')  # |  |z| - cut | to first order
    sym = max(np.min(np.abs(A + z)) / abs(z) for z in wA) if wA else 0.0
    return dict(nwA=len(wA), nwB=len(wB), cut=float(np.sqrt(float(cut2))), ties=len(ties),
                tiepair=len(ties) == 2 and np.conj(ties[0]) == ties[1], margin=margin, sym=sym, nstrict=len(wA) -
                sum(1 for z in wA if sq(z) == cut2))


MS = [k + 0.5 for k in range(11)]
FILES = {8: 'I96-win', 16: 'I96-dh610'}
res = {}
for sig, folder in FILES.items():
    for m in MS:
        res[(sig, m)] = sector(os.path.join(args.raw, folder, 'eig', f'tanh_sigma{sig}_m{m:g}.npz'), sig, m)

ref = {(int(r['sigma']), float(r['m'])): r for r in csv.DictReader(open(os.path.join(args.raw, 'I140-rpi5', 'retab_rpi5.csv')))}
bad = []
for k, r in res.items():
    q = ref[k]
    if r is None or (r['nwA'], r['nwB']) != (int(q['nwA']), int(q['nwB'])) or f"{r['cut']:.4f}" != q['cut4']:
        bad.append((k, None if r is None else (r['nwA'], r['nwB'], f"{r['cut']:.4f}"), (q['nwA'], q['nwB'], q['cut4'])))
check('W1', not bad, f"22 sectors: window A, B and cut equal retab_rpi5.csv: {not bad}; differ {bad[:4]}")

tot = {s: (sum(res[(s, m)]['nwA'] for m in MS), sum(res[(s, m)]['nwB'] for m in MS)) for s in FILES}
NEW = {(8, 3.5): 26, (8, 6.5): 18, (8, 7.5): 18, (8, 8.5): 18, (16, 0.5): 22, (16, 3.5): 18, (16, 5.5): 18, (16, 7.5): 14}
okn = all(res[k]['nwA'] == v for k, v in NEW.items())
check('W2', tot == {8: (262, 284), 16: (194, 216)} and okn,
      f"totals A / B: sigma R = 8 {tot[8]}, 16 {tot[16]} (claim 262 / 284, 194 / 216); the 8 changed rows as listed {okn}")

okt = all(r['tiepair'] for r in res.values())
mg = min(r['margin'] for r in res.values())
check('W3', okt and mg >= 1.9e-12,
      f"exact tie group at the cut = the eigenvalue and its conjugate in {sum(r['tiepair'] for r in res.values())} of 22; "
      f"smallest margin to a non-tied modulus {mg:.2e} (claim >= 1.9e-12)")

oks = all(r['nwA'] - r['nstrict'] == 2 for r in res.values())
check('W4', oks, f"the strict window |mu| > cut holds exactly 2 fewer in every sector: {oks}")

sbad = [(k, f"{r['sym']:.1e}", ref[k]['sym2']) for k, r in res.items() if f"{r['sym']:.1e}" != ref[k]['sym2']]
check('W5', not sbad, f"symmetry value to 2 digits equals retab_rpi5.csv in 22 sectors: {not sbad}; differ {sbad[:4]}")

sup = {}
for sig in (2, 4):
    rs = [sector(os.path.join(args.raw, 'I75-dh170', f'tanh_sigma{sig}_m{m:g}.npz')) for m in MS]
    sup[sig] = (sum(r['nwA'] for r in rs), sum(r['nwB'] for r in rs))
check('W6', sup == {2: (654, 676), 4: (406, 424)},
      f"supplement, I75-dh170: totals A / B sigma R = 2 {sup[2]}, 4 {sup[4]} (claim 654 / 676, 406 / 424)")

r = res[(16, 7.5)]
print(f"re-solve, sigma R = 16, m = 15/2: cut {r['cut']:.12f}, window A {r['nwA']}, B {r['nwB']}, tie group {r['ties']}, "
      f"margin {r['margin']:.2e}, symmetry {r['sym']:.2e}")
print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL))
sys.exit(1 if FAIL else 0)
