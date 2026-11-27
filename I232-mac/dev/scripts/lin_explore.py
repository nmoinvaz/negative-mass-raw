import sympy as sp
EPS=-1
# background jets
r,rp,rm,E,phi,php,phm,V0,V1,V2 = sp.symbols("r rp rm E phi php phm V0 V1 V2")   # E = e^{-f}
# perturbation jets
a,ap,am,d,dp,dm,e,ep,em = sp.symbols("a ap am d dp dm e ep em")
s=sp.Symbol("s")
# nonlinear RHS as functions of (r,rp,rm,E,phi,php,phm) with V(phi)=V0+V1(phi-phi0)+V2/2 (phi-phi0)^2
x = sp.Symbol("x") # phi - phi0
Vf = V0 + V1*x + V2*x**2/2
Vpf = V1 + V2*x
Fr = -(rp*rm+E/2)/r + sp.Rational(1,2)*Vf*r*E
Ff = -2*(rp*rm+E/2)/r**2 + EPS*php*phm
Fp = -(rp*phm+rm*php)/r - sp.Rational(EPS,2)*E*Vpf
# perturb: r->r+s a, rp->rp+s ap, rm->rm+s am, E-> E*(1 - s d) (f -> f+ s d), phi-> phi + s e (x = s e), php->php+s ep, phm->phm+s em
sub = {r:r+s*a, rp:rp+s*ap, rm:rm+s*am, E:E*sp.exp(-s*d), php:php+s*ep, phm:phm+s*em, x:s*e}
def lin(F):
    return sp.simplify(sp.diff(F.subs(sub, simultaneous=True), s).subs(s,0))
Lr, Lf, Lp = [lin(F) for F in (Fr,Ff,Fp)]
for n,L in (("r",Lr),("f",Lf),("phi",Lp)):
    print(n, sp.collect(sp.expand(L),[a,ap,am,d,e,ep,em]))
