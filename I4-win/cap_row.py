"""
Row of a convergence table for a gamma whose rtol 1e-12 evaluation was stopped at the 5 h cap (issue #4).
Reads convergence_l{l}_w{w}.partial.csv and prints the row in the format of convergence.py, from the variants that
finished, with the rtol 1e-12 entry marked not completed.  Not part of the repo scripts.
Usage: python cap_row.py <partial.csv> <gamma> <wall seconds its worker had run when stopped> [--exclude "<variant>"]
--exclude drops a finished variant to rehearse the row on a complete partial file (the row must then equal
the convergence.py row in every field that does not depend on the dropped variant).
"""
import sys, json, numpy as np

BASE = 'base (rtol1e-10, phi_cut1e-9, R60)'
RTOL = 'rtol 1e-12'
PHI = 'phi_cut 1e-12 (larger r_m)'
OTHERS = [BASE, 'background R=90', 'r0 = 3e-3']


def row(path, g, secs, exclude=()):
    res = {}
    for line in open(path):
        k, gg, v, dt = json.loads(line)
        if gg == g and k not in exclude:
            res[k] = (v, dt)
    Ds = {k: res[k][0] for k in [BASE, RTOL, PHI, 'background R=90', 'r0 = 3e-3'] if k in res}
    done_rtol = RTOL in Ds
    qi, qe = res['q'][0]
    T = sum(res[k][1] for k in res)
    signs = sorted(set(np.sign(list(Ds.values()))))
    same = [Ds[k] for k in Ds if 'phi_cut' not in k]
    spread = (max(same) - min(same)) / abs(np.mean(same))
    s = (f"gamma={g:8.3g}: D_base={Ds[BASE]:+.6e}  signs={signs}  rel.spread (same r_m)={spread:.1e}  "
         f"D(r_m~34)={Ds[PHI]:+.3e}  q_int={qi:+.6e} q_ext={qe:+.6e}  ({T:.0f}s)")
    if not done_rtol:
        s += (f"  [rtol 1e-12 not completed, stopped after its worker had run {secs:.0f}s of wall time, past the 5 h cap (18000s); signs and spread are over "
              f"{len(Ds)} variants]")
    return s


if __name__ == "__main__":
    path, g, secs = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    ex = tuple(sys.argv[sys.argv.index('--exclude') + 1:]) if '--exclude' in sys.argv else ()
    print(row(path, g, secs, ex))
