import sys
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i185/notes/warp")
sys.argv=[sys.argv[0]]
import sympy as sp, det_classify as dc
F0,F1,F2,ETA = dc.F0_,dc.F1_,dc.F2_,dc.ETA
N = sp.expand(dc.conical_N())
f,g,x,e = sp.symbols("f g x e")
P = sp.Poly(N, F2)
a3,a2,a1,a0 = (sp.expand(c.subs({F0:f,F1:g,ETA:e})) for c in P.all_coeffs())
print("a3", sp.factor(a3)); print("a2", sp.factor(a2)); print("a1 at 0", sp.factor(a1.subs(e,0))); print("a0 at 0", sp.factor(a0.subs(e,0)))
print("a3 e^2 coeff", sp.Poly(a3,e).coeff_monomial(e**2), " a2 e coeff", sp.Poly(a2,e).coeff_monomial(e))
