import sys, time, random
sys.path.insert(0, "/home/nathan/Source/negative-mass-i166/notes/warp")
import sympy as sp
import phantom_source as ps
import same_sign_scalars as sss
import two_scalars as ts
t0=time.time()
# (a) forms
t, x, rho, ph = sp.symbols("t x rho phi", positive=True)
c=sp.Function("c")(t); C=sp.Function("C")(t); d=sp.Function("d")(t)
b = c*x + C*sp.log(rho) + d
gam = sp.diff(C,t)/(2*C); w = gam - c
v1 = C/rho; v2 = w
alpha = [v1*b, v1, v2, 0]
X4=[t,x,rho,ph]
# alpha ^ d alpha ^ dphi coefficient on dt dx drho dphi
da = lambda i,j: sp.diff(alpha[j],X4[i]) - sp.diff(alpha[i],X4[j])
F = alpha[0]*da(1,2) + alpha[1]*da(2,0) + alpha[2]*da(0,1)   # alpha . curl alpha in (t,x,rho): a_t (d_x a_rho - d_rho a_x)+...
F = sp.simplify(F)
Fexp = C**3/rho**3 + (C/rho)*(-sp.diff(w,t) + (2*gam-c)*w)
print("F - claim:", sp.simplify(F-Fexp), " d_rho(rho F/C):", sp.simplify(sp.diff(rho*F/C, rho)))
# commutator
n = [1, -b, 0, 0]; K2 = [0, v2, -v1, 0]
br = [sp.simplify(sum(n[a]*sp.diff(K2[m],X4[a]) - K2[a]*sp.diff(n[m],X4[a]) for a in range(4))) for m in range(4)]
res = [sp.simplify(br[m] - (sp.diff(C,t)/C)*K2[m]) for m in range(4)]
print("bracket - (C'/C) K2:", res)
r = res[1]
print("r - claim:", sp.simplify(r - (sp.diff(w,t) + w*c - 2*gam*w - C**2/rho**2)), "d_rho r:", sp.simplify(sp.diff(r,rho)))
# (c) gauge ODE
D = sp.Function("D")(t)
dd = -c*D - sp.diff(D,t) + d   # d~ = d - cD - D'
Dsol = sp.exp(-sp.Integral(c,t))*sp.Integral(d*sp.exp(sp.Integral(c,t)), t)
print("gauge D solves D' + cD = d:", sp.simplify(sp.diff(Dsol,t) + c*Dsol - d))
# (d) const f case
p1,m1,f0,ra,rb,ia,ib,s = sp.symbols("p1 m1 f0 ra rb ia ib s")
def EB(p,m,F,g): return m**2*g - p*m**2*F + p**2
eqs2=[EB(p1,m1,f0**2,f0**2*ia**2/4), EB(p1,m1,f0**2,f0**2*ib**2/4), ia*ra-1, ib*rb-1]
Gu = sp.groebner(eqs2+[1-s*p1*m1*f0*(ra-rb)*(ia+ib)], s,p1,m1,f0,ra,rb,ia,ib, order="grevlex")
print("const f case:", Gu.exprs, f"{time.time()-t0:.1f}s")
# (b) closure2 on T4, P3, P4
rho_ = sp.Symbol("rho", positive=True)
tt, xx, ph_ = sp.symbols("t x varphi", real=True)
Lg = sp.Symbol("Lg", real=True)
En, Th, Ti = sp.symbols("En Th Ti", real=True)
X4b=[tt,xx,rho_,ph_]
def Dd(E,k):
    if k==0: return sp.diff(E,tt)+sp.diff(E,En)*2*En+sp.diff(E,Th)*(1-Th**2)+sp.diff(E,Ti)*(-Ti**2)
    if k==2: return sp.diff(E,rho_)+sp.diff(E,Lg)/rho_
    return sp.diff(E,X4b[k])
def shift_g(b): return sp.Matrix([[-1+b**2,b,0,0],[b,1,0,0],[0,0,1,0],[0,0,0,rho_**2]])
fams = {
 "T4": -Ti*xx + Ti**2*Lg,
 "P3": sp.Rational(3,2)*xx + 2*Lg + Th,
 "P4": sp.Rational(3,2)*(xx-Th) + 2*Lg + sp.Rational(1,5) - (1-Th**2),
}
for nm,bb in fams.items():
    Ric = ps.ricci(shift_g(bb), X4b, Dd, sss.simp_r)
    Cc = Dd(bb,2)*rho_  # rho b_rho = C
    gm = Dd(Cc,0)/(2*Cc); cc = Dd(bb,1)
    lam = Dd(bb,2)**2/2 + (gm-cc)**2
    M = (Ric - lam*shift_g(bb)).applyfunc(sss.simp_r)
    cl = sss.closure2(M, Dd, sss.simp_r, lam)
    random.seed(11)
    res=[]
    for _ in range(3):
        p={rho_:sp.Rational(random.randint(5,30),10), Lg:ts.rq(), tt:ts.rq(), xx:ts.rq(), En:abs(ts.rq())+sp.Rational(1,3), Th:sp.Rational(random.randint(-8,8),9), Ti:sp.Rational(random.randint(1,9),random.randint(1,5))}
        at=lambda e: sp.Rational(sp.cancel(sp.sympify(e).subs(p)))
        c_ = sss.same_sign_form(Ric.applyfunc(at), shift_g(bb).applyfunc(at))
        res.append(([(sp.N(x_["lam"],6),x_["sig"],x_["pats"]) for x_ in c_], sp.N(at(lam),6)))
    print(nm, "dim", cl["dim"], "integrable", cl["integrable"], res, f"{time.time()-t0:.0f}s", flush=True)
