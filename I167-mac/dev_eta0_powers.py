import sys, sympy as sp
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i167/notes/warp")
import det_classify as dc
F0,F1,F2,eta = dc.F0_, dc.F1_, dc.F2_, dc.ETA
N = sp.expand(dc.conical_N())
print("N(0) =", sp.factor(N.subs(eta,0)))
f,c,p = sp.symbols("f c p", positive=True)
x = sp.Symbol("x", positive=True)
# F = f + c x^p
sub = {F0: f + c*x**p, F1: p*c*x**(p-1), F2: p*(p-1)*c*x**(p-2), eta: x}
e = sp.expand(N.subs(sub))
e = sp.powsimp(sp.expand(e))
# collect by powers of x: terms are x^(a p + b) form; lowest for p>1 is x^(3p-4)
lead = sp.expand(e.coeff(x, 3*p-4)) if False else None
# do it by substituting x**p -> y symbolic: set x^p = X
X = sp.Symbol("X", positive=True)
e2 = sp.expand(sp.powsimp(sp.expand(N.subs({F0: f + c*X, F1: p*c*X/x, F2: p*(p-1)*c*X/x**2, eta: x}))))
poly = sp.Poly(e2, X)
for k in range(0, 7):
    ck = poly.coeff_monomial(X**k)
    if ck != 0: print("X^%d:"%k, sp.factor(ck))
# f = 0
e0 = sp.expand(sp.powsimp(sp.expand(N.subs({F0: c*X, F1: p*c*X/x, F2: p*(p-1)*c*X/x**2, eta: x}))))
poly0 = sp.Poly(e0, X)
for k in range(0, 7):
    ck = poly0.coeff_monomial(X**k)
    if ck != 0: print("f=0 X^%d:"%k, sp.factor(ck))
# log type: F = f + p0 ln x
p0, L = sp.symbols("p0 L")
e3 = sp.expand(N.subs({F0: f + p0*L, F1: p0/x, F2: -p0/x**2, eta: x}))
print("log type, w=0:", sp.factor(e3))
