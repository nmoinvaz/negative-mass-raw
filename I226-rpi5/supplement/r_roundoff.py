#!/usr/bin/env python3
"""Exploratory, written after the runs of record, not a declared check: the roundoff error in r itself, against its truncation error.
On the diagonal t of the static case (default 3.5, before the static wormhole departs) or of family S at p*_h - 1e-8 (p*_h from pstar_table.json), the same
data in float64 and in binary128: max |r_float64 - r_binary128| (roundoff), max |r_float64 - r_exact| for the static case (truncation plus the data's
1e-13), and max |r_h - r_2h| on the common nodes. Run from notes/wormhole_evolution:  python3 <this file> [D] [t] [static|S]"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.expanduser("~/Source/negative-mass-i226/notes/wormhole_evolution")))
import dn, constraint_plateau as cp

D = int(sys.argv[1]) if len(sys.argv) > 1 else 6
T = float(sys.argv[2]) if len(sys.argv) > 2 else 3.5
FAM = sys.argv[3] if len(sys.argv) > 3 else "static"
tab = json.load(open(os.path.expanduser("~/Source/negative-mass-raw/I226-rpi5/pstar_table.json")))[str(D)]
n = D - 2


def diag_r(k, dtype):
    h, A = tab["h"][k], (0.0 if FAM == "static" else tab["pstar"][k] - 1e-8)
    X = cp.CP["X"]["static"] if FAM == "static" else cp.CP["X"]["S"][D]
    N = int(round(X / h))
    s0 = int(round(T * cp.SQ2 / h))
    pulses, sym, eps = cp.pulses_of(FAM, A)
    d = cp.ellis_rays_x(n, N, h, pulses=pulses, symmetric=sym, eps=eps, dtype=dtype)
    par = dn.kernel_params(n, d.eps, 1)
    prev2, prev1 = None, None
    cur = np.zeros((d.nf, N + 1), dtype)
    cur[:, 0] = d.Sp[:, 0]
    diags = {0: cur}
    for s in range(1, s0 + 1):
        nd = np.zeros((d.nf, N + 1), dtype)
        I = np.arange(max(1, s - N), min(N, s - 1) + 1)
        if len(I):
            nd[:, I] = dn.cell_np(diags[s - 2][:, I - 1] if s >= 2 else None, diags[s - 1][:, I], diags[s - 1][:, I - 1], h, par, d.eps)
        if s <= N:
            nd[:, 0] = d.Sm[:, s]
            nd[:, s] = d.Sp[:, s]
        diags[s] = nd
        diags.pop(s - 2, None)
    return h, s0, np.arange(N + 1), diags[s0][0].astype(np.float64)


h1, s1, i1, r8 = diag_r(2, np.float64)
_, _, _, r16 = diag_r(2, np.longdouble)
h2, s2, i2, rc = diag_r(1, np.float64)
ok = (np.arange(len(r8)) >= 1) & (np.arange(len(r8)) <= s1 - 1)
print(f"D = {D}, family {FAM}, diagonal t = {s1 * h1 / cp.SQ2:.4f}, h = {h1:.6f}")
print(f"  max |r_float64 - r_binary128| = {np.max(np.abs(r8 - r16)[ok]):.3e}")
# coarse nodes i2 correspond to fine nodes 2 i2 (h2 = 2 h1); the diagonals t agree to the nearest cell: compare on the coarse diagonal's nodes
f = r8[::2][: len(rc)]
m = min(len(f), len(rc)) - 1
print(f"  max |r_h - r_2h| on the common nodes (coarse diagonal i + j = {s2}) = {np.max(np.abs(f[1:m] - rc[1:m])):.3e}  (the diagonals differ by {abs(s1 * h1 - s2 * h2) / cp.SQ2:.1e} in t)")
if FAM == "static":
    sol, q = dn.ellis_dense(n, 40.0)
    ii = np.arange(len(r8))
    l = (ii - (s1 - ii)) * h1 / cp.SQ2
    rex = sol(np.abs(l))[0]
    print(f"  max |r_float64 - r_exact(l)| = {np.max(np.abs(r8 - rex)[ok]):.3e}   max |r_binary128 - r_exact(l)| = {np.max(np.abs(r16 - rex)[ok]):.3e}")
