import sys, sympy as sp
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i167/notes/warp")
import det_classify as dc
F0,F1,F2,eta = dc.F0_, dc.F1_, dc.F2_, dc.ETA
N = sp.expand(dc.conical_N())
x = sp.Symbol("x")
cs = sp.symbols("c1:9")   # F = 1 + c1 x + c2 x^2 + ...
F = 1 + sum(cs[i]*x**(i+1) for i in range(8))
e = sp.expand(N.subs({F0: F, F1: sp.diff(F,x), F2: sp.diff(F,x,2), eta: x}))
P = sp.Poly(e, x)
for k in range(0, 9):
    ck = sp.factor(P.coeff_monomial(x**k))
    if ck != 0:
        print("order", k, ":", ck if len(str(ck))<400 else str(ck)[:400]+"...")
