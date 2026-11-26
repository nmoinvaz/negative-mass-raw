import sys, pickle, math
import numpy as np, sympy as sp
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i167/notes/warp")
import det_classify as dc
F0s,F1s,F2s,es = dc.F0_, dc.F1_, dc.F2_, dc.ETA
N = sp.expand(dc.conical_N())
P = sp.Poly(N, F2s)
cf = [sp.lambdify((F0s,F1s,es), P.coeff_monomial(F2s**c), "math") for c in range(4)]
# series
d = pickle.load(open("series_k14.pkl","rb"))
Fi, a = sp.symbols("Fi a4_0", real=True)
nu, T = sp.symbols("nu T")
terms = {k: sp.sympify(v, locals={"Fi":Fi,"a4_0":a}) for k,v in d.items()}
G = Fi + sum(v*nu**n*T**j for (n,j),v in terms.items() if n<=13)
p_ = sum(v*(-n*nu**n*T**j + (j*nu**n*T**(j-1) if j else 0)) for (n,j),v in terms.items() if n<=13)
Gf = sp.lambdify((Fi,a,nu,T), G, "math"); pf = sp.lambdify((Fi,a,nu,T), p_, "math")
def start(Fv, Cv, eta=200.0):
    nv, Tv = 1/eta, math.log(eta)
    return Gf(Fv,Cv,nv,Tv), pf(Fv,Cv,nv,Tv)/eta   # F, F' = p/eta
def roots(f, f1, e):
    c = [cf[i](f,f1,e) for i in range(4)]
    r = np.roots(c[::-1])
    return [x.real for x in r if abs(x.imag) < 1e-9*max(1,abs(x))], c
class Branch:
    def __init__(self, f2): self.f2 = f2
    def f2at(self, f, f1, e):
        rs, c = roots(f, f1, e)
        if not rs: raise RuntimeError("no real root")
        x = min(rs, key=lambda r: abs(r-self.f2))
        return x, c
def integrate_inward(Fv, Cv, e_end=0.0, e0=200.0, hfun=None):
    f, f1 = start(Fv, Cv, e0)
    # initial F2 from the leading branch
    rs, c = roots(f, f1, e0)
    f2_0 = -(e0*f1)**2/(2*f*e0**2)*1 # rough: q=-p^2/(2G nu^2), F2=(q-p)nu^2
    pp = e0*f1; q0 = -pp**2*e0**2/(2*f); f2g = (q0-pp)/e0**2
    br = Branch(f2g)
    e = e0; y = np.array([f, f1])
    def rhs(e, y):
        f2, c = br.f2at(y[0], y[1], e)
        return np.array([y[1], f2])
    log = []
    while e > e_end + 1e-15:
        h = min(0.002*max(e,0.05) , e-e_end) if hfun is None else hfun(e)
        h = min(h, e - e_end)
        try:
            k1 = rhs(e, y); f2 = br.f2
            k2 = rhs(e-h/2, y-h/2*k1); k3 = rhs(e-h/2, y-h/2*k2); k4 = rhs(e-h, y-h*k3)
        except RuntimeError as ex:
            return ("noroot", e, y, br.f2)
        y = y - h/6*(k1+2*k2+2*k3+k4); e -= h
        f2n, c = br.f2at(y[0], y[1], e); 
        if abs(f2n-br.f2) > 0.3*max(1,abs(f2n)) + 5: return ("jump", e, y, br.f2)
        br.f2 = f2n
        if abs(y[0]) > 1e6 or abs(f2n) > 1e8: return ("blow", e, y, f2n)
    return ("ok", e, y, br.f2)
if __name__ == "__main__":
    for Fv in (0.5, 1.0, 2.0):
        for Cv in (-30., -10., -3., 0., 3., 10., 30.):
            r = integrate_inward(Fv, Cv, 0.0)
            print(Fv, Cv, r[0], "eta=%.4g"%r[1], "F=%.6g F'=%.6g F2=%.6g"%(r[2][0], r[2][1], r[3]))
