import sys, random, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i166/notes/warp")
import sympy as sp
import phantom_source as ps
import same_sign_scalars as sss
import two_scalars as ts
t0=time.time()
rho = sp.Symbol("rho", positive=True)
tt, xx, ph = sp.symbols("t x varphi", real=True)
Lg = sp.Symbol("Lg", real=True)
En, Th = sp.symbols("En Th", real=True)
X4=[tt,xx,rho,ph]
def D(E,k):
    if k==0: return sp.diff(E,tt)+sp.diff(E,En)*2*En+sp.diff(E,Th)*(1-Th**2)
    if k==2: return sp.diff(E,rho)+sp.diff(E,Lg)/rho
    return sp.diff(E,X4[k])
def shift_g(b): return sp.Matrix([[-1+b**2,b,0,0],[b,1,0,0],[0,0,1,0],[0,0,0,rho**2]])
fams = {
 "T1": (xx/2 + En*Lg, lambda u: (D(u,2)**2/2 + (1 - 1/sp.Integer(2))**2)),   # lam = C^2/(2rho^2) + (gamma-c)^2, gamma=1,c=1/2
 "T2": ((sp.Rational(1,2)+En/3)*xx + En*Lg, lambda u: (D(u,2)**2/2 + (1 - sp.Rational(1,2)-En/3)**2)),
 "T3": (-Th*xx + En*(1-Th**2)*Lg, lambda u: (D(u,2)**2/2 + 1)),
 "static": (sp.Rational(3,2)*xx + 2*Lg + sp.Rational(1,5), lambda u: D(u,2)**2/2 + sp.Rational(9,4)),
}
for nm,(b,lamf) in fams.items():
    Ric = ps.ricci(shift_g(b), X4, D, sss.simp_r)
    lam = lamf(b)
    M = (Ric - lam*shift_g(b)).applyfunc(sss.simp_r)
    cl = sss.closure2(M, D, sss.simp_r, lam)
    print(nm, "dim", cl["dim"], "integrable", cl["integrable"], "bracket", [str(e) for e in cl.get("bracket",[])], f"{time.time()-t0:.0f}s", flush=True)
