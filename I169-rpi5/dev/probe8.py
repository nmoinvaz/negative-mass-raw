import sympy as sp, time
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
exec(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i169/331aac0b-19cd-46a3-93e4-a8cf021dbd98/scratchpad/probe3.py").read().split("# case (b)")[0])
t=time.time()
D = Dpoly()
# rank-1 sub-form X2 = 0 -> B0=B1=B2=0 (R2 arbitrary irrelevant); x-vars (A0,A1,A2), rho vars (a0,a1,a2)
D1 = Dpoly(B0=0,B1=0,B2=0,b0=0,b1=0,b2=0)
print("rank-1 sub-form", rank_of(D1,(A0,A1,A2),(a0,a1,a2),(None,0,sp.Rational(1,3),1)))
# irreducibility
t=time.time()
fl = sp.factor_list(D)
print("factor_list: const",fl[0],"factors",[(len(sp.Poly(f).terms()),m) for f,m in fl[1]], time.time()-t)
