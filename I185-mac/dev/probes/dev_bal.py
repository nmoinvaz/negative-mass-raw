import sys
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i185/notes/warp")
sys.argv=[sys.argv[0]]
import sympy as sp
import det_classify as dc
from conical_eta0_balance import *
F0,F1,F2,eta = dc.F0_,dc.F1_,dc.F2_,dc.ETA
N = sp.expand(dc.conical_N())
e = sp.Symbol("e")
Nt = sp.expand(sp.expand(N.subs({F0:Fs, F1:Ps/e, F2:(Qs-Ps)/e**2, eta:e}))*e**4)
E = sp.expand(Nt.subs(e, sp.sqrt(Ss)))
print(sp.Poly(E, Fs,Ps,Qs,Ss).total_degree())
f = sp.Rational(1,3)
for f in (sp.Symbol("f"), sp.Rational(1,3), sp.Rational(0), sp.Rational(1), sp.Rational(-1), sp.Rational(2)):
    print("==== f =", f)
    try:
        for r in regime_exp(E, f): print("  exp", r)
    except Exception as ex:
        print("  exp ERR", repr(ex))
    try:
        for r in regime_alg(E, f): print("  alg", r)
    except Exception as ex:
        print("  alg ERR", repr(ex))
print("const", regime_const(E)[0])
print("iter", regime_iter(E)[0])
print("big", regime_big(E))
