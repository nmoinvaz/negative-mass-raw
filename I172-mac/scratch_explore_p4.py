import sys, pickle, time
import sympy as sp
sys.path.insert(0,'.')
from lser import *
def Fseries(K_, fi=None, c=None, prec=None):
    d=pickle.load(open(f"series_K{K_}.pkl","rb"))
    out={}
    Fi_s,a4=sp.symbols("Fi a4_0")
    for k,v in d.items():
        e=sp.sympify(v,locals={"Fi":Fi_s,"a4_0":a4})
        if fi is not None: e=e.subs({Fi_s:fi,a4:c})
        else: e=e.subs({a4:sp.Symbol("C")}).subs({Fi_s:sp.Symbol("Fi")})
        out[k]=K.from_expr(e)
    return L(out, K_+1), 
def build(Gser):
    """Gser = F as series (includes Fi constant term)."""
    G=Gser
    p=G.Dt(); q=p.Dt()
    nu2=L({(2,0):K(1)})
    nu1=L({(1,0):K(1)})
    P=-(nu2*(p*p+G*(q-p)))
    Q=-(q*K(sp.Rational(1,2)))
    Z=-(nu1*q*K(sp.Rational(1,2)))
    Y=-(nu1*(p*p+G*q*K(sp.Rational(1,2))))
    h=p*p*K(sp.Rational(1,2))
    A=P-h; B=-P-h
    hi=h.inv()
    S11=B-Y*Y*hi; S01=Q-Z*Y*hi; S00=A-Z*Z*hi
    return dict(G=G,p=p,q=q,P=P,Q=Q,Z=Z,Y=Y,h=h,A=A,B=B,hi=hi,S11=S11,S01=S01,S00=S00)
def dX(f): return L({k:v for k,v in f.Dt().d.items()},f.prec).shift(1)
def dR(f): return -(f.Dt())
def EB(c):
    G,h,hi=c["G"],c["h"],c["hi"]
    S11=c["S11"]
    w2=-(S11*hi)
    L2=[c["Z"]*hi, c["Y"]*hi, L.const(1)]
    L1=[c["S01"]/S11, L.const(1), L.const(0)]
    def coord(a): return [a[0]+a[1]*G, a[1], a[2]]
    def Wd(a,b):
        a=coord(a); b=coord(b)
        return a[0]*(dX(b[2])-dR(b[1]))+a[1]*dR(b[0])-a[2]*dX(b[0])
    dw=[L.const(0), dX(w2), dR(w2)]
    cl2,cl1=coord(L2),coord(L1)
    det3=(cl2[0]*(dw[1]*cl1[2]-dw[2]*cl1[1])-cl2[1]*(dw[0]*cl1[2]-dw[2]*cl1[0])+cl2[2]*(dw[0]*cl1[1]-dw[1]*cl1[0]))
    E=Wd(L2,L2)+w2*Wd(L1,L1)
    Bc=Wd(L2,L1)+Wd(L1,L2)+det3/(w2*K(2))
    return w2,E,Bc,L2,L1
if __name__=="__main__":
    K_=int(sys.argv[1]); fi=sp.Rational(sys.argv[2]); cc=sp.Rational(sys.argv[3])
    t0=time.time()
    Gs,=Fseries(K_,fi,cc)
    Gs=Gs+K(fi)
    c=build(Gs)
    for nm in ("h","S11","S01","S00"):
        print(nm); c[nm].show(8)
    w2,E,Bc,L2,L1=EB(c)
    print("w2"); w2.show(8)
    print("E"); E.show(14)
    print("Bc"); Bc.show(14)
    print(time.time()-t0)
