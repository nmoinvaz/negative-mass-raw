import sympy as sp, time
G,r,W,c=sp.symbols("G r W c",real=True)
def Npoly(ep,s,W2sub=None,gp_drop=False):
    W2 = (G**2+2*c**2) if W2sub is None else W2sub
    H=(G**2+4*c**2)*W + s*(5*c*ep*W2 - 2*c*G*r)
    Gp=ep*W2-(0 if gp_drop else G*r)
    Hp=sp.diff(H,G)*Gp+sp.diff(H,W)*(G*Gp/W)+sp.diff(H,r)*(-r**2)
    rs=sp.solve(H,r)[0]
    num=sp.expand(sp.numer(sp.together(Hp.subs(r,rs))))
    P=sp.Poly(num,W); p0=p1=0
    for (e,),co in P.terms():
        if e%2==0: p0+=co*W2**(e//2)
        else: p1+=co*W2**(e//2)
    return sp.factor(sp.expand(p0**2-p1**2*W2))
for ep in (1,-1):
    for s in (1,-1):
        print(ep,s,Npoly(ep,s))
print("mut W2=G^2+c^2:",Npoly(1,1,G**2+c**2))
print("mut no friction:",Npoly(1,1,gp_drop=True))
