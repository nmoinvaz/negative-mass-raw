"""Where does convergence.py's variant spread come from? scipy D of each variant at a few (l, gamma), against the base."""
import sys, time
sys.path.insert(0, '/Users/nathan/Source/negative-mass-i186/phase2/nonradial')
import numpy as np, background as B
from polar_solver import PolarProblem
w = 0.7603
st60 = B.solve_star(w, -1)
st90 = B.solve_star(w, -1, guess=st60, R=90.0)
V = {'base': dict(st=st60), 'rtol 1e-12': dict(st=st60, rtol=1e-12), 'phi_cut 1e-12': dict(st=st60, phi_cut=1e-12),
     'R=90': dict(st=st90), 'r0=3e-3': dict(st=st60, r0=3e-3)}
for l, g in [(2, 1.0), (2, 10.0), (6, 10.0)]:
    res = {}
    for k, v in V.items():
        v = dict(v); st = v.pop('st')
        p = PolarProblem(st, l, **v)
        t = time.time(); res[k] = (p.D(g), p.rm, time.time() - t)
    b = res['base'][0]
    print(f"l={l} gamma={g}: " + "; ".join(f"{k}: D={d:+.9e} rel to base {d / b - 1:+.2e} (rm {rm:.4f}, {s:.1f}s)" for k, (d, rm, s) in res.items()), flush=True)
