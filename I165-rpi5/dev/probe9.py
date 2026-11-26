import pickle, sys, sympy as sp
from sympy import QQ
from sympy.polys.rings import ring
R, u,b,v,s = ring("u,b,v,s", QQ)
G = pickle.load(open("gens_l2.pkl","rb"))
Dl = sp.sympify(pickle.load(open("delta.pkl","rb"))[0])
U,B,V,S = sp.symbols('u b v s')
def sg(e): return str(e).replace("**","^")
s0 = int(sys.argv[1]); p = int(sys.argv[2])
def slice_poly(d):
    e = 0
    # sum over terms with s0 substituted, in Python ints/rationals
    out = {}
    for (mu,mb,mv,ms),c in d.items():
        out[(mu,mb,mv)] = out.get((mu,mb,mv),0) + sp.Rational(c)*sp.Rational(s0)**ms
    terms=[]
    for (mu,mb,mv),c in out.items():
        if c==0: continue
        terms.append(f"({c.p})*u^{mu}*b^{mb}*v^{mv}" if c.q==1 else f"({c.p}/{c.q})*u^{mu}*b^{mb}*v^{mv}")
    return "+".join(terms) if terms else "0"
Dp = f"(u*(1-({s0})^2)-2*({s0}))"
DeltaS = sg(Dl.subs(S, s0))
names = ["f0","f1","f2","f11","f12","f21","f22"]
txt = f"ring r={p},(t,u,b,v),dp;\noption(redSB);\nshort=0;\n"
for nm in names: txt += f"poly {nm}={slice_poly(G[nm])};\n"
txt += f"poly Dl={DeltaS};\npoly P=u*v*b*{Dp}*Dl;\npoly sat=1-t*P;\n"
txt += """
proc rep(string nm, ideal J){ int t0=rtimer; ideal G=std(J); "";
  nm,": std time",rtimer-t0,"size",size(G),"dim",dim(G),"mult",mult(G),"is unit:",(G[1]==1); }
rep("L0 f0 sat", ideal(f0,sat));
rep("L1 f0,f1,f2 plain", ideal(f0,f1,f2));
rep("L1 f0,f1,f2 sat", ideal(f0,f1,f2,sat));
rep("L2 +f11,f12,f21,f22 sat", ideal(f0,f1,f2,f11,f12,f21,f22,sat));
rep("L2 f0,f1,f2,f11,f22,f12 sat", ideal(f0,f1,f2,f11,f12,f22,sat));
quit;
"""
open(f"p9_s{s0}_p{p}.sing","w").write(txt)
