#!/usr/bin/env python3
"""ind225: T(gamma1) at the stall member by an even interpolation of three published values (criteria in README.md)."""
import sys
MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
pts = [(0.0, 0.846045), (0.5, 0.758357), (1.0, 0.675)]
if MUT == "odd":
    f = [lambda g: 1.0, lambda g: g, lambda g: g * g]
else:
    f = [lambda g: 1.0, lambda g: g * g, lambda g: g ** 4]
import numpy as np
A = np.array([[fk(g) for fk in f] for g, _ in pts]); y = np.array([t for _, t in pts])
coef = np.linalg.solve(A, y)
T = sum(c * fk(0.048) for c, fk in zip(coef, f))
e = T * 1.0028
ok = abs(e - 0.8472) <= 1e-3 and abs(e - 0.8475) <= 1e-3
print(f"[{'PASS' if ok else 'FAIL'}] K1: T(0.048) = {T:.6f}, e-fold T r_th = {e:.6f}; against the note's 0.8472 ({e - 0.8472:+.1e}) and the measured 0.8475 ({e - 0.8475:+.1e}); mutation {MUT}")
sys.exit(0 if ok else 1)
