import sys
from p4 import *
Gs = L({(2,0): -2*Fi, (4,0): C, (4,1): Bb}, 5) + Fi
c = build(Gs)
w2,E,Bc,L2,L1 = EB(c)
w = w2.sqrt()
h = c["h"]
for nm,s in (("O_k",(E+w*Bc)*h*K(2)),("O_m",(E-w*Bc)*h*K(2))):
    print(nm); s.show()
Gs = L({(2,0): -2*Fi}, 3) + Fi
try:
    c = build(Gs); w2,E,Bc,L2,L1 = EB(c); w=w2.sqrt(); h=c["h"]
    (E*h).show()
except Exception as e: print("K=2:", repr(e))
