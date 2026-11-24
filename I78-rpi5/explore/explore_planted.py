# Scratch check of the planted metrics' R - lam g before the script is written (old coordinates, no shear)
import sys, time
sys.path.insert(0, '/home/nathan/Source/negative-mass-i78/notes/warp')
import sympy as sp
import phantom_source as ps
t, z, X, Y = sp.symbols('t z X Y', real=True)
Ro = sp.Symbol('Ro', positive=True)
simp = lambda e: sp.cancel(sp.together(e))
def run(name, g, X4, lamv):
    t0 = time.time()
    Ric = ps.ricci(g, X4, lambda E, k: sp.diff(E, X4[k]), simp)
    M = (Ric - lamv * g).applyfunc(simp)
    print(name, "M =", M.tolist(), f"({time.time()-t0:.1f} s)")
Th = sp.Symbol('Th', real=True)
run("P1 AdS2 x R2", sp.diag(-1/z**2, 1/z**2, 1, Ro**2), [t, z, Ro, Th], -1)
run("P2 dS2 x R2", sp.diag(-1/t**2, 1/t**2, 1, Ro**2), [t, z, Ro, Th], 1)
eps = sp.Rational(1, 10)
Mx = run("D1", sp.diag(-1/z**2, 1/z**2, 1, Ro**2*(1+eps*Ro**2)), [t, z, Ro, Th], -1)
gam = sp.Rational(1, 10)
E = 1 + gam*(z**2 - t**2)
run("D2", sp.diag(-1, 1, E**2, E**2), [t, z, X, Y], -4*gam/E)
