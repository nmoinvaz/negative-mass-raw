import pickle, sys, sympy as sp
G = pickle.load(open("gens_l2.pkl","rb"))
Dl = sp.sympify(pickle.load(open("delta.pkl","rb"))[0])
U,B,V,S = sp.symbols('u b v s')
u0 = int(sys.argv[1]); p = int(sys.argv[2]); gens = sys.argv[3].split(",")
def sg(e): return str(e).replace("**","^")
def slice_poly(d):
    out = {}
    for (mu,mb,mv,ms),c in d.items():
        out[(mb,mv,ms)] = out.get((mb,mv,ms),0) + sp.Rational(c)*sp.Rational(u0)**mu
    terms=[]
    for (mb,mv,ms),c in out.items():
        if c==0: continue
        terms.append(f"({c.p}{'/'+str(c.q) if c.q!=1 else ''})*b^{mb}*v^{mv}*s^{ms}")
    return "+".join(terms)
txt = f"ring r={p},(t,b,v,s),dp;\noption(redSB);\nshort=0;\n"
for nm in gens: txt += f"poly {nm}={slice_poly(G[nm])};\n"
txt += f"poly Dl={sg(Dl.subs(U,u0))};\npoly Dp=({u0})*(1-s^2)-2*s;\npoly P=v*b*s*(s^2-1)*(s^2+1)*Dp*Dl;\n"
txt += f"int t0=rtimer;\nmatrix T;\nideal J={','.join(gens)},1-t*P;\nideal Gb=liftstd(J,T);\n\"u0={u0} liftstd time\",rtimer-t0,\"size\",size(Gb),\"dim\",dim(Gb),\"G[1]\",Gb[1];\n"
txt += "int i; for(i=1;i<=ncols(J);i++){ \"cofactor\",i,\"terms\",size(T[i,1]),\"deg\",deg(T[i,1]); }\nquit;\n"
open(f"p14_u{u0}.sing","w").write(txt)
