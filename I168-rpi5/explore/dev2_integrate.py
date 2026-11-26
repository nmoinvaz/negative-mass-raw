import numpy as np, math
def hugeroot(G,sig,y):
    # x>0, w=-x, cubic P(-x)=0 ; om=2/y (r = G y, om = 2G/r)
    om=2.0/y; b=G*G*sig; a=G*sig
    kap=1-b+sig; mu=1+3*sig-b+2*sig**2-6*b*sig; c=1+2*sig
    M=mu+(b-sig)*om
    x=M/(2*a*kap)
    for _ in range(60):
        f=2*a*kap*x**3 - M*x**2 - 4*a*c*x + c*c-om*om
        d=6*a*kap*x**2 - 2*M*x - 4*a*c
        dx=f/d; x-=dx
        if abs(dx)<1e-15*x: break
    return x,a
def rhs_red(t,Y,sig0):
    lnG,y=Y; G=math.exp(lnG); sig=sig0*math.exp(-2*t)
    x,a=hugeroot(G,sig,y)
    e=y*y*(1-2*a*x)
    return np.array([sig*y, y*(4-y)/2 - sig*y*y + e/2]), e
def rk4(f,t,Y,h,*args):
    k1=f(t,Y,*args)[0]; k2=f(t+h/2,Y+h/2*k1,*args)[0]; k3=f(t+h/2,Y+h/2*k2,*args)[0]; k4=f(t+h,Y+h*k3,*args)[0]
    return Y+h/6*(k1+2*k2+2*k3+k4)
# direct integration of N=0 in (G,p): N(G,p,q,nu) with nu^2=sig, solve q by Newton from huge branch
def Nfun(G,p,q,s):
    A0=p**2*(p**2-q)*(p**2+q)
    A1=G**2*p**2*q**2+4*G*p**4*q-2*G*q**3+4*p**6-3*p**2*q**2
    A2=2*(G*(q-p)+p**2)*(G**2*q**2+2*G*p**3+2*G*p**2*q+2*p**4-q**2)
    return A0+s*A1+s*s*A2
def qroot(G,p,s,q0):
    q=q0
    for _ in range(100):
        f=Nfun(G,p,q,s); h=1e-7*max(abs(q),1e-30); d=(Nfun(G,p,q+h,s)-Nfun(G,p,q-h,s))/(2*h)
        dq=f/d; q-=dq
        if abs(dq)<1e-14*abs(q): break
    return q
def rhs_dir(t,Y,sig0):
    G,p=Y; s=sig0*math.exp(-2*t)
    q0=-p*p/(2*G*s)
    q=qroot(G,p,s,q0)
    return np.array([p,q]),q
for G0 in [0.5,2.0]:
    sig0=1/(1000*(1+G0**2)); zeta0=0.2; y0=4+zeta0
    # reduced
    Yr=np.array([math.log(G0),y0]); t=0; h=0.002
    # direct: p = sig*r = sig*G*y
    Yd=np.array([G0,sig0*G0*y0])
    out=[]
    for k in range(int(8/h)):
        Yr=rk4(rhs_red,t,Yr,h,sig0); Yd=rk4(rhs_dir,t,Yd,h,sig0); t+=h
        if k%1000==999:
            sig=sig0*math.exp(-2*t); Gr=math.exp(Yr[0]); yr=Yr[1]
            Gd=Yd[0]; yd=Yd[1]/(sig*Gd)
            print(f"G0={G0} t={t:.1f} red G={Gr:.12f} y={yr:.12f}  dir G={Gd:.12f} y={yd:.12f}  diff G={abs(Gr-Gd):.2e} y={abs(yr-yd):.2e}")
