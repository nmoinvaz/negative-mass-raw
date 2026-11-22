"""For each sector file of one sigma R (argument), the real eigenvalues of A (|Im| < 1e-9 |mu|) counted two ways: above 1e-8 in
|mu| v_c (the real-eigenvalue table's column) and above 1e-8 in |mu| (the unscaled floor tanh_spectrum.py's solve_sector uses
to pick the eigenfunctions of the identity check). Also lists the real eigenvalues of A that B reproduces (persisting())
with the values. Run with the venv python, -X utf8: reals_check.py <sigma R> [eig dir]. Reads only; writes to stdout."""
import os
import sys

import numpy as np

R = os.path.dirname(os.path.abspath(__file__))
sig = sys.argv[1]
eig = sys.argv[2] if len(sys.argv) > 2 else os.path.join(R, "eig")
ms = [0.5 + k for k in range(11)]
print(r"| m | real, \|mu\|v_c > 1e-8 | real, \|mu\| > 1e-8 (evaluated by the identity check) | between | "
      r"B reproduces (A, B, relative difference) |")
print("|---|---|---|---|---|")
for m in ms:
    d = np.load(os.path.join(eig, f"tanh_sigma{sig}_m{m:g}.npz"))
    vc = float(d["vc"])
    muA, muB = d["muA"] * vc, d["muB"] * vc
    real = lambda mu: mu[np.abs(mu.imag) < 1e-9 * np.abs(mu)]  # noqa: E731
    sc = real(muA[np.abs(muA) > 1e-8])
    un = real(d["muA"][np.abs(d["muA"]) > 1e-8])
    pers = []
    for z in sc:
        j = int(np.argmin(np.abs(muB - z)))
        if abs(muB[j] - z) < 1e-4 * abs(z) and abs(muB[j].imag) < 1e-9 * abs(muB[j]):
            pers.append(f"{z.real:+.5e}, {muB[j].real:+.5e}, {abs(muB[j] - z) / abs(z):.1e}")
    print(f"| {m:g} | {len(sc)} | {len(un)} | {len(sc) - len(un)} | {'; '.join(pers) if pers else '0'} |")
