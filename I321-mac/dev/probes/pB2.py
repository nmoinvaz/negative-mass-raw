import mpmath as mp, time, sys
mp.mp.dps=30
kap0=2/mp.pi
A=lambda y: -(y*y)+kap0*(y+(y*y+1)*mp.atan(y))
dA=lambda y: mp.diff(A,y)
def static_run(Lv, U, Vb, Vs, fixed_kappa=False):
    dl=1/Lv-1
    rh=mp.findroot(lambda y: A(y)+dl, -dl/(2*kap0))
    kL=dA(rh)/2
    kc=kap0 if fixed_kappa else kL
    F=lambda y: A(y)+dl
    rb=rh-U*Vb
    wb=mp.log(Vb)
    f=lambda tau,y: -F(y)/(2*kc)
    sol=mp.odefun(f,0,rb)
    out=[]
    for V in Vs:
        w=mp.log(V); y=sol(wb-w)
        out.append(mp.sqrt(2)/(1+y*y)*F(y)/(2*kc*V))
    return out
def delta(U,Vb,Vs,eps,fixed):
    p=static_run(1+eps,U,Vb,Vs,fixed); m=static_run(1-eps,U,Vb,Vs,fixed)
    return [(a-b)/(2*eps) for a,b in zip(p,m)]
t0=time.time()
Vs=[mp.mpf(10)**(-k) for k in (3,4,5,6,7,8)]
for fixed in (False,True):
    for U in (mp.mpf('-0.5'),mp.mpf('-1')):
        vals=delta(U,mp.mpf(1),Vs,mp.mpf('1e-9'),fixed)
        sl=[(vals[i+1]-vals[i])/(mp.log(Vs[i+1])-mp.log(Vs[i])) for i in range(len(Vs)-1)]
        print('fixed kappa' if fixed else 'own kappa','U',U,[mp.nstr(s,4) for s in sl], 'scale -(pi/sqrt2)*0.5 =',mp.nstr(-mp.pi/mp.sqrt(2)/2,4))
print(time.time()-t0)
