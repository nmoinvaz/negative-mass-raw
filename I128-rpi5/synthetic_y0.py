#!/usr/bin/env python3
"""
Planted-truth control of diagnose_plant.py's --y0 (#128), run before the real caches. Usage:

  python synthetic_y0.py PATH/diagnose_plant.py [--mutate=wrongcount]   (exit 1 when any case fails)

Each case writes a pickle cache of a known function F on a dyadic grid of every contour edge (t = j / 2560, so every
point the counter asks for to depth 8 is there), runs diagnose_plant.py on it and compares what it prints with the
analytic answer. The pass criteria are fixed here, before any real cache is replayed:
  U1  upper box, rational F with 2 zeros and 1 pole inside (and 2 zeros outside), planted zero inside:
      exit 0, count of F +1.0000, of F times the factor +2.0000, the chain's counts equal to the steps'.
  U2  as U1 with the planted zero below the box: exit 0, +1.0000 and +1.0000.
  S1  symmetric box, F real on the real axis with 2 zeros and 2 poles of conjugate pairs inside, and 2 zeros inside:
      exit 0, count +2.0000, with the planted pair +4.0000 (the doubling of the symmetric box is kept).
  U1n U1 without --y0: exit 1, the replay stops on a point the cache lacks (the contour starts at (x1, 0)).
  A1  upper box, F = exp(2 pi i 40 (x / (x1 - x0) + y / (y1 - y0))): every step of depth <= 2 sees a multiple of 2 pi,
      so the counter loses 40 turns on each of the four edges (the dense chain sees them): exit 1, and the printed
      difference/2pi is +-40.0000 on all 4 edges for F, and of absolute value above 30 on all 4 edges for F times the
      factor. (First run: 40 for all eight. The factor's own phase near its zero makes the counter subdivide a few
      steps on two edges, which then see 36 of the 40 turns. Criterion changed to the above, before any real cache.)
  --mutate=wrongcount  expects +2 instead of +1 for U1's F (U1 must fail).
"""
import os, pickle, re, subprocess, sys, tempfile
import numpy as np

DP = sys.argv[1]
MUT = next((a.split('=', 1)[1] for a in sys.argv[2:] if a.startswith('--mutate=')), None)
assert MUT in (None, 'wrongcount'), MUT
PY = sys.executable
TMP = tempfile.mkdtemp(prefix='synthetic_y0_')


def rational(zeros, poles):
    return lambda s: np.prod([s - z for z in zeros]) / np.prod([s - p for p in poles])


def inside(z, box, sym):
    x0, x1, y0, y1 = box
    return x0 < z.real < x1 and ((abs(z.imag) < y1) if sym else (y0 < z.imag < y1))


def contour(box, sym):
    x0, x1, y0, y1 = box
    return ([complex(x1, 0), complex(x1, y1), complex(x0, y1), complex(x0, 0)] if sym else
            [complex(x1, y0), complex(x1, y1), complex(x0, y1), complex(x0, y0), complex(x1, y0)])


def run(name, box, F, plant, sym, y0opt=True, expect_exit=0):
    cs = contour(box, sym)
    cache = {}
    for a, b in zip(cs[:-1], cs[1:]):
        for j in range(2561):
            s = a + (b - a) * (j / 2560)
            cache[complex(round(s.real, 12), round(s.imag, 12))] = complex(F(s))
    cf = os.path.join(TMP, name + '.pkl')
    pickle.dump(cache, open(cf, 'wb'))
    x0, x1, y0, y1 = box
    cmd = [PY, DP, cf, str(x0), str(x1), str(y1), f"{plant.real},{plant.imag}", '--guard=all', '--expect=none']
    if not sym and y0opt:
        cmd.append(f"--y0={y0}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout


tot = re.compile(r"total adaptive ([+-]\d+\.\d+) -> count ([+-]\d+\.\d+);  dense chain ([+-]\d+\.\d+) -> count ([+-]\d+\.\d+)")
dif = re.compile(r"^  edge .*difference/2pi ([+-]\d+\.\d+)$", re.M)
bad = []


def report(name, what, ok, extra=''):
    print(f"  {name}: {what}  {'PASS' if ok else 'FAIL'}{extra}")
    if not ok:
        bad.append(name)


def counts(name, box, zeros, poles, plant, sym, expect_f, expect_p):
    rc, out = run(name, box, rational(zeros, poles), plant, sym)
    t = [tuple(float(v) for v in m) for m in tot.findall(out)]
    ok = rc == 0 and len(t) == 2 and all(abs(c[1] - c[3]) < 5e-5 for c in t) and \
        abs(t[0][1] - expect_f) < 5e-5 and abs(t[1][1] - expect_p) < 5e-5
    report(name, f"exit {rc}, count of F {t[0][1]:+.4f} (expected {expect_f:+.4f}), with the factor "
                 f"{t[1][1]:+.4f} (expected {expect_p:+.4f}), chain counts {t[0][3]:+.4f} and {t[1][3]:+.4f}" if len(t) == 2
           else f"exit {rc}, no counts printed", ok)


UB = (0.1, 2.0, 2.5, 6.0)
Z = [1.0 + 3.0j, 0.5 + 4.0j, 0.3 + 1.5j, 2.5 + 4.0j]
P = [1.5 + 5.0j]
nin = sum(inside(z, UB, False) for z in Z) - sum(inside(p, UB, False) for p in P)
print(f"# control of diagnose_plant.py --y0 on synthetic caches; zeros minus poles inside the upper box {UB}: {nin}"
      + (f"  [mutate={MUT}]" if MUT else ""))
assert nin == 1
counts('U1', UB, Z, P, 0.3 + 2.7j, False, nin + (1 if MUT == 'wrongcount' else 0), nin + 1)
counts('U2', UB, Z, P, 0.3 + 1.0j, False, nin, nin)

SB = (0.1, 2.0, 0.0, 2.5)
SZ = [1 + 2j, 1 - 2j, 1.5 + 0.5j, 1.5 - 0.5j]
SP = [0.5 + 1j, 0.5 - 1j]
counts('S1', SB, SZ, SP, 0.3 + 1.76j, True, 2.0, 4.0)

rc, out = run('U1n', UB, rational(Z, P), 0.3 + 2.7j, False, y0opt=False)
report('U1n', f"without --y0 exit {rc}, " + ("stops on a missing point" if 'the cache lacks the point' in out else "no missing point"),
       rc == 1 and 'the cache lacks the point' in out)

alias = lambda s: np.exp(2j * np.pi * 40 * ((s.real) / (UB[1] - UB[0]) + s.imag / (UB[3] - UB[2])))
rc, out = run('A1', UB, alias, 0.3 + 2.7j, False)
d = [float(v) for v in dif.findall(out)]
report('A1', f"exit {rc}, difference/2pi per edge for F then F times the factor: " + ' '.join(f"{v:+.4f}" for v in d),
       rc == 1 and len(d) == 8 and all(abs(abs(v) - 40) < 5e-3 for v in d[:4]) and all(abs(v) > 30 for v in d[4:]))
print("RESULT: " + ("every case as expected" if not bad else "FAILED: " + ", ".join(bad)) + (f"  [mutate={MUT}]" if MUT else ""))
sys.exit(1 if bad else 0)
