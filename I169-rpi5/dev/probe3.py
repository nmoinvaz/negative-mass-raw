import sympy as sp, time
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
A0,A1,A2,B0,B1,B2,a0,a1,a2,b0,b1,b2,v = sp.symbols("A0 A1 A2 B0 B1 B2 a0 a1 a2 b0 b1 b2 v")
def Dpoly(A0=A0,A1=A1,A2=A2,B0=B0,B1=B1,B2=B2,a0=a0,a1=a1,a2=a2,b0=b0,b1=b1,b2=b2):
    u = A0*a0+B0*b0+v
    ux = A1*a0+B1*b0; uxx = A2*a0+B2*b0; ur = A0*a1+B0*b1; uxr = A1*a1+B1*b1; lap = A0*a2+B0*b2
    P = -(ux**2+u*uxx); Q=-lap/2; Z=uxr/2; Y=ux*ur+u*uxr/2; h=ur**2/2
    return sp.expand(8*(h*(h**2-P**2-Q**2+Y**2+Z**2) - P*(Y**2-Z**2)+2*Q*Y*Z))
def rank_of(D, xv, rv, vs=(None,)):
    out=[]
    for vv in vs:
        Dn = D if vv is None else sp.expand(D.subs(v,vv))
        Pl = sp.Poly(Dn, *xv, *rv, *( (v,) if vv is None else ()))
        rows,cols,ent={},{},{}
        nx=len(xv)
        for mon,co in Pl.terms():
            ri=rows.setdefault(mon[:nx],len(rows)); ci=cols.setdefault(mon[nx:],len(cols)); ent[(ri,ci)]=co
        M=sp.zeros(len(rows),len(cols))
        for (i,j),co in ent.items(): M[i,j]=co
        out.append((vv,len(rows),len(cols),DomainMatrix.from_Matrix(M).convert_to(QQ).rank()))
    return out
# case (b): X2 = 1: B0=1,B1=0,B2=0
Db = Dpoly(B0=1,B1=0,B2=0)
print("case b  (x: X,X',X'' ; rho: a0,a1,a2,b0,b1,b2,v):", rank_of(Db,(A0,A1,A2),(a0,a1,a2,b0,b1,b2),(None,0,sp.Rational(1,3),1)))
# case (c): R2 = 1 const: b0=1,b1=0,b2=0
Dc = Dpoly(b0=1,b1=0,b2=0)
print("case c:", rank_of(Dc,(A0,A1,A2,B0,B1,B2),(a0,a1,a2),(None,0,sp.Rational(1,3),1)))
# additive (a): A.. X2=1,R1=1
Da = Dpoly(B0=1,B1=0,B2=0,a0=1,a1=0,a2=0)
print("case a additive", rank_of(Da,(A0,A1,A2),(b0,b1,b2),(None,0,sp.Rational(1,3),1)))
