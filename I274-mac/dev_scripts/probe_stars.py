"""probe: the crate's star (taylor_polar star) against the scipy path's star for the four (omega, eps) of #126's D boxes, and the scipy path's r_m.
Run from phase2/nonradial of the worktree. Prints one line per star."""
import os, sys, json, subprocess, time
import numpy as np
HERE = os.getcwd()
sys.path.insert(0, HERE)
import background as B
from polar_solver import PolarProblem
CB = os.path.join(HERE, "taylor_polar", "target", "complex", "release", "taylor_polar")
LAM, MU = 10240.0, 10240.0 ** 2 / 4.8
print("B.LAM, B.MU:", B.LAM, B.MU, " equal to taylor_polar.py's:", B.LAM == LAM, B.MU == MU)
for (w, eps) in [(0.7603, -1), (0.70, -1), (0.85, -1), (0.75, 1)]:
    t = time.time()
    st = B.solve_star(w, eps)
    t1 = time.time() - t
    P = PolarProblem(st, 2)
    out = subprocess.run(["nice", "-n", "10", CB, "star", f"omega={w}", f"eps={float(eps)}", f"lam={LAM}", f"mu={MU!r}"], capture_output=True, text=True)
    o = json.loads(out.stdout.splitlines()[0]) if out.returncode == 0 else None
    print(f"w={w} eps={eps:+d}: scipy star {t1:.1f} s, M={st.M:.6f} phi_c={st.phic:.10f} alpha_c={st.alpha_c:.10f} R={st.R} r0={st.r0} rm={P.rm!r}")
    print("   crate:", out.returncode, (o if o else out.stderr[-300:]))
    if o:
        print(f"   phi_c ratio {o['phic'] / st.phic - 1:+.2e}   alpha_c ratio {o['alpha_c'] / st.alpha_c - 1:+.2e}")
