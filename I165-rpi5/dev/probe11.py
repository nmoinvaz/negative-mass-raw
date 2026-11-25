import pickle, sys, sympy as sp
G = pickle.load(open("gens_l2.pkl","rb"))
Dl = sp.sympify(pickle.load(open("delta.pkl","rb"))[0])
U,B,V,S = sp.symbols('u b v s')
p = int(sys.argv[1]); gens = sys.argv[2].split(","); capname = sys.argv[3]
def sg(e): return str(e).replace("**","^")
def poly_txt(d):
    return "+".join(f"({sp.Rational(c).p}{'/'+str(sp.Rational(c).q) if sp.Rational(c).q!=1 else ''})*u^{a}*b^{bb}*v^{c2}*s^{dd}" for (a,bb,c2,dd),c in d.items())
txt = f"ring r=({p},s),(t,u,b,v),dp;\noption(redSB);\nshort=0;\n"
for nm in gens: txt += f"poly {nm}={poly_txt(G[nm])};\n"
txt += f"poly Dl={sg(Dl)};\npoly Dp=u*(1-s^2)-2*s;\npoly P=u*v*b*Dp*Dl;\n"
txt += f"int t0=rtimer;\nideal J={','.join(gens)},1-t*P;\nideal Gb=std(J);\n\"{capname} param-s std: time\",rtimer-t0,\"size\",size(Gb),\"dim\",dim(Gb),\"unit\",(Gb[1]==1);\n"
txt += "if (Gb[1]==1) { \"G[1] =\", Gb[1]; }\nquit;\n"
open(f"p11_{capname}.sing","w").write(txt)
