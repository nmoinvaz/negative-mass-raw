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
En, Th = sp.symbols("En Th", real=True)   # En = exp(2t), Th = tanh t
X4=[tt,xx,rho,ph]
def D(E,k):
    if k==0: return sp.diff(E,tt)+sp.diff(E,En)*2*En+sp.diff(E,Th)*(1-Th**2)
    if k==2: return sp.diff(E,rho)+sp.diff(E,Lg)/rho
    return sp.diff(E,X4[k])
def shift_g(b): return sp.Matrix([[-1+b**2,b,0,0],[b,1,0,0],[0,0,1,0],[0,0,0,rho**2]])
fams = {
 "T1: x/2 + En ln rho": (xx/2 + En*Lg*1),   # c=1/2? need c = 1/2 + k En with k=0 -> c' = 0 ; gamma=1 -> c'=2c-1 -> c=1/2 ok
 "T2: (1/2+En/3) x + En ln rho": ((sp.Rational(1,2)+En/3)*xx + En*Lg),
 "T3: -Th x + En(1-Th^2) ln rho": (-Th*xx + En*(1-Th**2)*Lg),
 "bad: (1/2+En/3+1/5) x + En ln rho": ((sp.Rational(1,2)+En/3+sp.Rational(1,5))*xx + En*Lg),
}
for nm,b in fams.items():
    Ric = ps.ricci(shift_g(b), X4, D, sss.simp_r)
    random.seed(7)
    res=[]
    for _ in range(3):
        p={rho:sp.Rational(random.randint(5,30),10), Lg:ts.rq(), tt:ts.rq(), xx:ts.rq(), En:abs(ts.rq())+sp.Rational(1,3), Th:ts.rq()}
        at=lambda e: sp.Rational(sp.cancel(sp.sympify(e).subs(p)))
        c = sss.same_sign_form(Ric.applyfunc(at), shift_g(b).applyfunc(at))
        res.append([(float(sp.N(x["lam"],6)),x["sig"],x["pats"]) for x in c])
    print(nm, res, f"{time.time()-t0:.0f}s", flush=True)
