import sys; sys.path.insert(0,'/tmp/claude-1000/-home-nathan-Source-negative-mass-i168/8e4f5756-108b-457a-974a-8882f6064c2d/scratchpad')
import mpmath as mp, time
from fractions import Fraction as Fr
import ser
mp.mp.dps=34
G0=mp.mpf(1); zeta0=mp.mpf('0.2'); eta0=mp.mpf(45); sig0=1/eta0**2
def hugeroot(G,sig,y):
    om=2/y; b=G*G*sig; a=G*sig
    kap=1-b+sig; mu=1+3*sig-b+2*sig**2-6*b*sig; c=1+2*sig
    M=mu+(b-sig)*om
    x=M/(2*a*kap)
    for _ in range(80):
        f=2*a*kap*x**3-M*x**2-4*a*c*x+c*c-om*om
        d=6*a*kap*x**2-2*M*x-4*a*c
        dx=f/d; x-=dx
        if abs(dx)<mp.mpf(10)**-31*x: break
    return x,a
def rhs(t,Y):
    lnG,y=Y; G=mp.e**lnG; sig=sig0*mp.e**(-2*t)
    x,a=hugeroot(G,sig,y); e=y*y*(1-2*a*x)
    return [sig*y, y*(4-y)/2-sig*y*y+e/2]
etaend=mp.mpf(10)**7
t1=mp.log(etaend/eta0)
t0=time.time()
f=mp.odefun(rhs,0,[mp.log(G0),4+zeta0],tol=mp.mpf(10)**-28,degree=12)
Y=f(t1); print("integrated",round(time.time()-t0,1),"s",flush=True)
sg=1/etaend**2
Finf=mp.e**Y[0]*mp.e**(2*sg)    # int_t^inf sigma y ~ 2 sigma
print("Finf =",Finf,flush=True)
def Fr_of(x,dig=30): return Fr(int(mp.nint(x*mp.mpf(10)**dig)),10**dig)
Fi=Fr_of(Finf)
def series_val(eta,Cval,m):
    g,_=ser.solve_series(Fi,Fr_of(Cval,20))
    T=mp.log(eta); nu=1/eta; tot=Finf
    for (n,j),v in g.d.items():
        if n<=2*m: tot+=mp.mpf(v.numerator)/mp.mpf(v.denominator)*nu**n*T**j
    return tot
# C is linear-ish; get it by 2-step secant (the series is polynomial in C of degree <=3)
Fref=mp.e**f(mp.log(mp.mpf(1000)/eta0))[0]
def fC(Cv): return series_val(mp.mpf(1000),Cv,4)-Fref
c0,c1=mp.mpf(0),mp.mpf(1)
f0,f1=fC(c0),fC(c1)
for _ in range(6):
    c2=c1-f1*(c1-c0)/(f1-f0); c0,f0=c1,f1; c1=c2; f1=fC(c1)
C=c1; print("C =",C,"resid",f1,flush=True)
g,_=ser.solve_series(Fi,Fr_of(C))
def sv(eta,m):
    T=mp.log(eta); nu=1/eta; tot=Finf
    for (n,j),v in g.d.items():
        if n<=2*m: tot+=mp.mpf(v.numerator)/mp.mpf(v.denominator)*nu**n*T**j
    return tot
for eta in [100,200,400,800]:
    Fn=mp.e**f(mp.log(mp.mpf(eta)/eta0))[0]
    row=[]
    for m in [1,2,3,4]:
        err=abs(Fn-sv(mp.mpf(eta),m)); norm=err/((mp.mpf(1)/eta)**(2*m+2)*(1+mp.log(eta))**m)
        row.append((m,mp.nstr(err,3),mp.nstr(norm,4)))
    print(eta,row,flush=True)
