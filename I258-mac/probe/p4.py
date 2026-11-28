import sys, math, numpy as np
sys.argv = [sys.argv[0]]
from p3 import *
def dm_of(s, dr, drT, dF=0.0):
    b = bgs(s)
    # dm = dr (1/2 - e^F s^2 r'^2) - r e^F s r' (s r' dF + dr_T)
    eF = 1.0 / b['E']
    return dr*(0.5 - eF*s*s*b['rp']**2) - b['r']*eF*s*b['rp']*(s*b['rp']*dF + drT)
# direction of end vector at SR
v = AB[:, 2]
print("end vector", v, "dm(v) =", dm_of(SR, v[0], v[1]))
# hom solutions from SL with unit data, evaluate dm at SR
for y0 in ((1.0, 0.0), (0.0, 1.0)):
    sol = solve_even(lambda s: 0.0, lambda s: 0.0, y0=y0)
    print("hom y0", y0, "-> end", sol.y[:, -1], "dm", dm_of(SR, *sol.y[:, -1]))
# dm of particular solutions: should equal end-vector dm for each basis: compare with energy integral later
for i, c in enumerate(centers):
    print(c, "dm_end =", dm_of(SR, AB[0, i], AB[1, i]))
