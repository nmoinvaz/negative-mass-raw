import mpmath as mp, time
mp.mp.dps=40
kap=2/mp.pi
A=lambda y: -(y*y)+kap*(y+(y*y+1)*mp.atan(y))        # c=-1, K=kappa
def Fin(w,y,beta):
    s=beta*mp.e**w
    return A(y)-(1+kap*y)*s/(1+s)
def ray(beta,wb,rb):
    # integrate backward in tau = wb - w
    f=lambda tau,y: -Fin(wb-tau,y,beta)/(2*kap)
    return mp.odefun(f,0,rb)
def dphidV_beta(wb,rb,eps,Vs):
    out=[]
    sol_p=ray(eps,wb,rb); sol_m=ray(-eps,wb,rb)
    res=[]
    for V in Vs:
        w=mp.log(V); tau=wb-w
        yp,ym=sol_p(tau),sol_m(tau)
        def dV(y,beta):
            return mp.sqrt(2)/(1+y*y)*Fin(w,y,beta)/(2*kap*V)
        res.append((dV(yp,eps)-dV(ym,-eps))/(2*eps))
    return res
t0=time.time()
Vb=mp.mpf(1); U=mp.mpf('-0.5'); rb=-U*Vb
Vs=[mp.mpf(10)**(-k) for k in (3,4,5,6,7,8)]
vals=dphidV_beta(mp.log(Vb),rb,mp.mpf('1e-12'),Vs)
c2=mp.mpf(1)/2
want=-mp.pi/mp.sqrt(2)*c2
print('time',time.time()-t0)
for i in range(len(Vs)-1):
    slope=(vals[i+1]-vals[i])/(mp.log(Vs[i+1])-mp.log(Vs[i]))
    print(mp.nstr(Vs[i+1],3), mp.nstr(slope/want,12))
