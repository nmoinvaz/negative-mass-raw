#!/usr/bin/env python3
"""v_c = 2 sqrt(S) / (pi I)^(1/3), I = int_0^inf |f'|^3 r^2 dr, S = 3 (pi/2)^(4/3), tanh profile with R = 1, at 30 digits
(mpmath quad split at the wall), against tanh_spectrum.py (adaptive quad) and tanh_spectrum_check.py (400-point Gauss)."""
from mpmath import mp, mpf, tanh, cosh, quad, sqrt, pi, inf
mp.dps = 30
S = 3 * (pi / 2) ** (mpf(4) / 3)
for sig in (2, 4, 8, 16):
    s = mpf(sig)
    fp = lambda r: s * (1 / cosh(s * (r + 1))**2 - 1 / cosh(s * (r - 1))**2) / (2 * tanh(s))
    pts = [0] + [1 + k / s for k in range(-8, 9) if 1 + k / s > 0] + [1 + 60 / s, inf]
    I = quad(lambda r: abs(fp(r))**3 * r**2, sorted(set(pts)))
    print(f'sigma R = {sig:2d}: v_c = {mp.nstr(2 * sqrt(S) / (pi * I) ** (mpf(1) / 3), 15)}')
