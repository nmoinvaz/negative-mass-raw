import sys, time
from p4 import *
K_=int(sys.argv[1])
t0=time.time()
Gs,=Fseries(K_)
Gs=Gs+Fi
c=build(Gs)
w2,E,Bc,L2,L1=EB(c)
w=w2.sqrt()
h=c["h"]
Ok=(E+w*Bc)*h*K(2); Om=(E-w*Bc)*h*K(2)
Sm=(E)*h*K(4); Df=(w*Bc)*h*K(4)
for nm,s in (("w",w),("E",E),("wB",w*Bc),("O_k+O_m (4hE)",Sm),("O_k-O_m (4h w B)",Df),("O_k",Ok),("O_m",Om)):
    print(nm); s.show(10)
print(time.time()-t0)
