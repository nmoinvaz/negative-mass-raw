#!/usr/bin/env python3
"""Coordinator's independent check of #96 (thin-wall tanh spectrum). Criteria G1-G3 in I96-mac2/README.md, fixed before
the first run. Drives #94's B-spline solver (notes/warp/tanh_spectrum_check.py, ARPACK) and compares with #96's tables.
Usage: ind96.py --repo=DIR --out=DIR [--mutate=ref|sig|vc]"""
import os
import subprocess
import sys
import time

import numpy as np

ARGS = dict(a.lstrip('-').split('=', 1) for a in sys.argv[1:])
MUT = ARGS.get('mutate')
assert MUT in (None, 'ref', 'sig', 'vc'), MUT
REPO, OUT = ARGS['repo'], ARGS['out']
CHK = os.path.join(REPO, 'notes/warp/tanh_spectrum_check.py')
VC96 = {8: 1.562434, 16: 0.985030}
REF96 = {(8, 0.5): (0.29951080, 0.224930), (8, 10.5): (0.102782, 0.093657),
         (16, 0.5): (0.22508330, 0.184364), (16, 10.5): (0.102918, 0.095278)}
if MUT == 'ref':
    REF96 = {k: (a * (1 + 1e-3), b * (1 + 1e-3)) for k, (a, b) in REF96.items()}
failed = []


def check(cid, name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + cid + ' ' + name + ('  ' + detail if detail else ''), flush=True)
    if not ok and cid not in failed:
        failed.append(cid)


def solve(sig, disc, m):
    fn = os.path.join(OUT, f's{sig:g}_{disc}_m{int(2 * m)}.npz')
    if not os.path.exists(fn):
        t0 = time.time()
        r = subprocess.run([sys.executable, '-u', CHK, '--part=solve', f'--sigma={sig:g}', f'--disc={disc}', f'--ms={m:g}',
                            '--solver=arpack', '--floor=0.08', f'--out={OUT}'], capture_output=True, text=True)
        print(r.stdout.strip().replace('\n', '\n    '), f'[{time.time() - t0:.0f} s, exit {r.returncode}]', flush=True)
        if r.returncode:
            print(r.stderr[-2000:])
            sys.exit(2)
    d = np.load(fn)
    return d['mu'], float(d['vc'])


def lead_next(mu, vc):
    a = np.sort(np.abs(mu))[::-1] * vc
    nxt = next(x for x in a if x < a[0] * (1 - 1e-6))
    return a[0], nxt


t00 = time.time()
print(f'ind96 mutation={MUT}')
for sig in (8, 16):
    ssolve = 8.1 if (MUT == 'sig' and sig == 8) else sig
    for m in (0.5, 10.5):
        muA, vcA = solve(ssolve, 'A', m)
        muB, vcB = solve(ssolve, 'B', m)
        if MUT == 'vc':
            vcA *= 1 + 1e-5
        check('G1', f'sR={sig} m={m:g} v_c', abs(vcA - VC96[sig]) < 1e-6, f'{vcA:.7f} against #96 {VC96[sig]}')
        la, na = lead_next(muA, vcA)
        lb, nb = lead_next(muB, vcB)
        check('G2', f'sR={sig} m={m:g} A and B agree on the leading |mu| v_c', abs(la - lb) / la < 1e-4,
              f'A {la:.8f}, B {lb:.8f}, rel {abs(la - lb) / la:.1e}')
        r1, r2 = REF96[(sig, m)]
        e1, e2 = abs(la - r1) / r1, abs(na - r2) / r2
        check('G3', f'sR={sig} m={m:g} leading and second |mu| v_c against #96', e1 < 1e-4 and e2 < 1e-4,
              f'lead {la:.8f} vs {r1} (rel {e1:.1e}), next {na:.6f} vs {r2} (rel {e2:.1e})')
print(f'FAILED: {failed}' if failed else 'ALL PASS', f'({time.time() - t00:.0f} s)')
sys.exit(1 if failed else 0)
