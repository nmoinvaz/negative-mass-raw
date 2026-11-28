import sys, time, random
sys.path.insert(0,'.')
import lib1 as L, lib2 as M
from lib1 import Ser, DOM
import sympy as sp
L.setdom(False); L.KAPVAL=sp.Rational(1,1); L.TRUNC=10
random.seed(1)
bg=L.build_background(1,7,False)
env=M.make_env(bg)
E0j,ops=M.load_ops()
coef={}
for k,lst in ops.items():
    coef[k]=[(fn,a,b,M.evaluate(co,env)) for fn,a,b,co in lst]
r0,Om0,Th0=[L.pi_to_ser(bg[x]) for x in ('r','Om','th')]
def rnd(deg):
    return Ser({(i,j):L.cv(sp.Rational(random.randint(-5,5),random.randint(1,4))) for i in range(deg+1) for j in range(deg+1-i)})
def pure_gauge(xiV,xiU,dn_only=False):
    f={}
    f['dr']=xiV*r0.dV()+xiU*r0.dU()
    f['dth']=xiV*Th0.dV()+xiU*Th0.dU()
    f['dOm']=xiV*Om0.dV()+xiU*Om0.dU()+Om0*(xiV.dV()+xiU.dU())
    f['hv']=Om0*xiU.dV()*(-2)
    f['hu']=Om0*xiV.dU()*(-2)
    return f
def residual(f, coef, sign=1):
    out={}
    for k,lst in coef.items():
        tot=Ser()
        for fn,a,b,C in lst:
            tot=tot+C*f[fn].jet(a,b)
        out[k]=tot
    return out
xiV=rnd(5); xiU=rnd(5)
f=pure_gauge(xiV,xiU)
res=residual(f,coef)
print('general gauge:',{k:(s.mindeg_nonzero()) for k,s in res.items()})
# double-null preserving gauge xiV(V), xiU(U)
xiV1=Ser({(i,0):L.cv(sp.Rational(random.randint(1,5),3)) for i in range(1,6)})
xiU1=Ser({(0,j):L.cv(sp.Rational(random.randint(1,5),3)) for j in range(0,6)})
f=pure_gauge(xiV1,xiU1)
print('hv,hu zero?', f['hv'].d=={}, f['hu'].d=={})
res=residual(f,coef)
print('dn gauge:',{k:(s.mindeg_nonzero()) for k,s in res.items()})
# mutation: sign of dOm term
f=pure_gauge(xiV1,xiU1); f['dOm']=xiV1*Om0.dV()+xiU1*Om0.dU()-Om0*(xiV1.dV()+xiU1.dU())
res=residual(f,coef)
print('mut gauge sign:',{k:(s.mindeg_nonzero()) for k,s in res.items()})
