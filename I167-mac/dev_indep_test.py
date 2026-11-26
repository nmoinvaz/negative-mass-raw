import sys, time, pickle, mpmath as mp, sympy as sp
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i167/notes/warp")
import det_classify as dc
mp.mp.dps = 25
F0s,F1s,F2s,es = dc.F0_, dc.F1_, dc.F2_, dc.ETA
P = sp.Poly(sp.expand(dc.conical_N()), F0s, F1s, F2s, es)
terms = [(a,b,c,m,int(co)) for (a,b,c,m),co in zip(P.monoms(), P.coeffs())]
def coefs(f0,f1,e, mut=False):
    cs=[mp.mpf(0)]*4
    for a,b,c,m,co in terms:
        if mut and (a,b,c,m)==(1,2,1,2): co = -4
        cs[c] += co*f0**a*f1**b*e**m
    return cs  # index = power of F2
d = pickle.load(open("series_k14.pkl","rb"))
Fi, a = sp.symbols("Fi a4_0", real=True)
T = {k: sp.sympify(v, locals={"Fi":Fi,"a4_0":a}) for k,v in d.items()}
def start(fi, c, eta):
    nu=mp.mpf(1)/eta; t=mp.log(eta); G=mp.mpf(fi); p=mp.mpf(0)
    for (n,j),v in T.items():
        val = mp.mpf(sp.N(v.subs({Fi: sp.nsimplify(fi), a: sp.nsimplify(c)}), 30))
        G += val*nu**n*t**j
        p += val*nu**n*(-n*t**j + (j*t**(j-1) if j else 0))
    return G, p*nu
def run(fi, c, eta_end, mut=False):
    e0=mp.mpf(200); G,F1=start(fi,c,e0)
    # initial F2 from the series q
    last=[None]
    def root(f0,f1,e):
        cs=coefs(f0,f1,e,mut)
        rts=mp.polyroots(cs[::-1], maxsteps=200, extraprec=60)
        re=[r.real for r in rts if abs(r.imag) < mp.mpf(10)**-12*max(1,abs(r))]
        g = last[0]
        r = min(re, key=lambda x: abs(x-g)) if g is not None else None
        return r
    # first guess: leading balance q = -p^2/(2 G nu^2): F2 = (q-p) nu^2
    p0=e0*F1; q0=-p0**2*e0**2/(2*G); last[0]=(q0-p0)/e0**2
    def rhs(tau, y):
        e = e0 - tau
        f2 = root(y[0], y[1], e); last[0]=f2
        return [-y[1], -f2]
    t0=time.time()
    sol = mp.odefun(rhs, 0, [G,F1], tol=mp.mpf(10)**-15, degree=10)
    y = sol(e0-mp.mpf(eta_end))
    return y, time.time()-t0
for fi,c in ((1,0),):
    y,dt = run(fi,c,4)
    print(fi,c, [mp.nstr(v,15) for v in y], "time", dt)
