import sys, pickle, mpmath as mp, sympy as sp
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i167/notes/warp")
import det_classify as dc
mp.mp.dps = 60
F0s,F1s,F2s,es = dc.F0_, dc.F1_, dc.F2_, dc.ETA
N = sp.expand(dc.conical_N())
Nf = sp.lambdify((F0s,F1s,F2s,es), N, "mpmath")
terms = pickle.load(open("series_k14.pkl","rb"))
Fi, a = sp.symbols("Fi a4_0", real=True)
T = {k: sp.sympify(v, locals={"Fi":Fi,"a4_0":a}) for k,v in terms.items()}
def state(fi, c, eta, nmax):
    nu = mp.mpf(1)/eta; t = mp.log(eta)
    G = mp.mpf(fi); p = mp.mpf(0); q = mp.mpf(0)
    for (n,j),v in T.items():
        if n > nmax: continue
        val = mp.mpf(sp.N(v.subs({Fi: sp.Rational(fi), a: sp.Rational(c)}), 60))
        G += val*nu**n*t**j
        p += val*nu**n*(-n*t**j + (j*t**(j-1) if j else 0))
        q += val*nu**n*(n*n*t**j - 2*n*j*(t**(j-1) if j else 0) + (j*(j-1)*t**(j-2) if j>1 else 0))
    return G, p*nu, (q-p)*nu**2
for nmax in (9, 13, 14):
    G,F1,F2 = state(1, 0, mp.mpf(200), nmax)
    val = Nf(G,F1,F2,mp.mpf(200))
    print(nmax, mp.nstr(G,20), mp.nstr(F1,20), mp.nstr(F2,20), "N=", mp.nstr(val,5))
