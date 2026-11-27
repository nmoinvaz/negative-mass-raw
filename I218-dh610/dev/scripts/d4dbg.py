import sys, pickle, sympy as sp
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import polar_derive as pd
from polar_derive import *
r = reduce_l2(); M4 = matrix_l2(r)
Me = M4.subs({As: 1, A1: 0})
H0s, Ps, Ks, Fs = sp.symbols("H0 Pi K F")
v = sp.Matrix([H0s, Ps, Ks, Fs])
mine_up = sp.simplify((Me * v)[3] / sp.sqrt(2))
Wv = sp.sqrt(lam); om = sp.I * Wv; H1v = Wv * Ps; u = Fs / sp.sqrt(2)
theirs = -((2 * om**2 * R2 + (L - 2)) * Ks + (L - 2) * H0s - 2 * sp.I * om * rho * H1v) / 4 - 2 * rho / R2 * u
d = sp.simplify(mine_up - theirs)
print("mine u' =", sp.collect(sp.expand(mine_up), [H0s, Ps, Ks, Fs]))
print("theirs  =", sp.collect(sp.expand(theirs), [H0s, Ps, Ks, Fs]))
print("diff    =", sp.collect(sp.expand(d), [H0s, Ps, Ks, Fs]))
