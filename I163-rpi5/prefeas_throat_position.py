import math
from scipy.integrate import quad
for g in (0.5,1,2,2.5,3,4,6,8,10):
    lam=math.exp(2*g*math.atan(g))
    f=lambda y: math.exp(2*g*(math.atan(g)-math.atan(y)))
    rt=quad(f,0,g,limit=500)[0]
    print(g, "lam=%.3e"%lam, "rho~(throat)=%.4g"%rt, "e^{2g atan(1/g)}=%.3f"%math.exp(2*g*math.atan(1/g)))
