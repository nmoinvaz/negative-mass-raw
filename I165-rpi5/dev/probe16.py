import pickle, sys, sympy as sp
G = pickle.load(open("gens_l2.pkl","rb"))
Dl = sp.sympify(pickle.load(open("delta.pkl","rb"))[0])
U,B,V,S = sp.symbols('u b v s')
s0 = sp.Rational(sys.argv[1]); p = sys.argv[2]; gens = sys.argv[3].split(","); name=sys.argv[4]
def sg(e): return str(e).replace("**","^")
def slice_poly(d):
    out = {}
    for (mu,mb,mv,ms),c in d.items():
        out[(mu,mb,mv)] = out.get((mu,mb,mv),0) + sp.Rational(c)*s0**ms
    return "+".join(f"({c.p}{'/'+str(c.q) if c.q!=1 else ''})*u^{a}*b^{bb}*v^{cc}" for (a,bb,cc),c in out.items() if c!=0)
txt = f"ring r={p},(t,u,b,v),dp;\noption(redSB);\nshort=0;\n"
for nm in gens: txt += f"poly {nm}={slice_poly(G[nm])};\n"
DlS = sp.expand(Dl.subs(S, s0))
txt += f"poly Dl={sg(DlS)};\npoly P=u*Dl;\n"
txt += f"int t0=rtimer;\nmatrix T;\nideal J={','.join(gens)},1-t*P;\nideal Gb=liftstd(J,T);\n\"{name} liftstd time\",rtimer-t0,\"size\",size(Gb),\"G[1]\",Gb[1];\n"
txt += "int i; for(i=1;i<=ncols(J);i++){ \"cofactor\",i,\"terms\",size(T[i,1]),\"deg\",deg(T[i,1]); }\nquit;\n"
open(f"p16_{name}.sing","w").write(txt)
