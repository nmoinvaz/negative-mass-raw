import sys
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i185/notes/warp")
sys.argv=[sys.argv[0]]
import sympy as sp
import det_classify as dc
F0,F1,F2,eta = dc.F0_,dc.F1_,dc.F2_,dc.ETA
N = sp.expand(dc.conical_N())
F,P,Q,e = sp.symbols("F P Q e")
Nt = sp.expand(sp.expand(N.subs({F0:F, F1:P/e, F2:(Q-P)/e**2, eta:e}))*e**4)
Nt = sp.simplify(Nt)
Nt = sp.expand(Nt)
print("is polynomial in e:", sp.Poly(Nt, e).degree(), [m for m in sp.Poly(Nt,e).monoms()])
pe = sp.Poly(Nt, e)
N0 = pe.coeff_monomial(e**0)
print("N0 =", sp.factor(N0))
for k in (2,4,6):
    print(k, sp.factor(pe.coeff_monomial(e**k)))
print("odd:", [pe.coeff_monomial(e**k) for k in (1,3,5)])
