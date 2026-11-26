# dev probe: build the chain generators f0,f1,f2 and level 2 in (u,b,v,s); pickle as dict monom->coeff
import time, pickle, sympy as sp
from sympy import QQ
from sympy.polys.fields import field
t0=time.time()
exec(open("probe4.py").read().split("Cb = X(")[0].replace('print(','(lambda *a,**k:None)('))
Cb = X(sr, X1c) - X(sx, X2c) + sx
R = K.ring
def strip(num, nv):
    n = num
    for q in nv:
        while True:
            qq, rr = divmod(n, q)
            if rr == 0: n = qq
            else: break
    # primitive, sign
    from math import gcd
    cs = [c for c in n.coeffs()]
    from sympy import ilcm, igcd
    den = 1
    for c in cs: den = ilcm(den, sp.Rational(c).q)
    n = n*den
    g = 0
    for c in n.coeffs(): g = igcd(g, int(c))
    n = n.quo_ground(g) if hasattr(n,'quo_ground') else n/g
    if n.LC < 0: n = -n
    return n
us, bs, vs, ss = R.gens
Dpol = us*(1-ss**2) - 2*ss
# Delta' = the big factor of sx denominator
dfac = sp.factor_list(sx.denom.as_expr())[1]
print("sx denom factors (terms):", [(len(sp.Poly(f).terms()), m) for f,m in dfac])
Delta = [R.from_expr(f) for f,m in dfac if len(sp.Poly(f).terms())>10][0]
NV = [us, ss, vs, bs, ss-1, ss+1, ss**2+1, Dpol, Delta]
NV = [q for q in NV]
print("NV set; time", time.time()-t0)
C0 = strip(Cb.numer, NV)
print("f0 terms", len(C0.terms()), "deg", C0.degree(), time.time()-t0)
gens = {"f0": C0}
def step(name, F):
    Fe = K.new(F, R.one) if hasattr(K,'new') else K(F)
    out = {}
    for i,Y in ((1,X1c),(2,X2c)):
        g = X(Fe, Y)
        out[i] = strip(g.numer, NV)
        print(name, "X%d"%i, "terms", len(out[i].terms()), "deg", out[i].degree(), time.time()-t0, flush=True)
    return out
l1 = step("f0", C0)
gens["f1"], gens["f2"] = l1[1], l1[2]
l21 = step("f1", gens["f1"]); gens["f11"], gens["f12"] = l21[1], l21[2]
l22 = step("f2", gens["f2"]); gens["f21"], gens["f22"] = l22[1], l22[2]
pickle.dump({k:dict(v.terms()) for k,v in gens.items()}, open("gens_l2.pkl","wb"))
pickle.dump((str(Delta.as_expr()),), open("delta.pkl","wb"))
print("done", time.time()-t0)
