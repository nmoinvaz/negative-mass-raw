import sys, sympy as sp
sys.argv=[sys.argv[0]]
sys.path.insert(0,"/home/nathan/Source/negative-mass-i169/notes/warp")
import sum_products as sp_
from sum_products import *
u,ux,ur,uxx,uxr,lap = two_jets(v)
P,Q,Z,Y,h = blocks(u,ux,ur,uxx,uxr,lap)
cands = {
 "drop -2P(Y2-Z2)": sp.expand(E_SYM + 8*P*(Y**2-Z**2)),
 "drop 2QYZ": sp.expand(E_SYM - 8*2*Q*Y*Z),
 "drop hY^2": sp.expand(E_SYM - 8*h*Y**2),
 "drop hQ^2": sp.expand(E_SYM + 8*h*Q**2),
 "drop hP^2": sp.expand(E_SYM + 8*h*P**2),
}
for name,E0 in cands.items():
    out=[]
    for key,expect in (("0",0),("1/3",sp.Rational(1,3)),("1",1),("v",None)):
        E = E0 if expect is None else sp.expand(E0.subs(v,expect))
        nr,nc,rk = bil_rank(E, XV, RV + ((v,) if expect is None else ()))
        out.append((key,rk,RANKS["full"][key]))
    print(name, out, flush=True)
