import pickle, sys, itertools, sympy as sp
G = pickle.load(open("gens_l2.pkl","rb"))
Dl = sp.sympify(pickle.load(open("delta.pkl","rb"))[0])
U,B,V,S = sp.symbols('u b v s')
s0 = int(sys.argv[1]); p = int(sys.argv[2])
def sg(e): return str(e).replace("**","^")
def slice_poly(d):
    out = {}
    for (mu,mb,mv,ms),c in d.items():
        out[(mu,mb,mv)] = out.get((mu,mb,mv),0) + sp.Rational(c)*sp.Rational(s0)**ms
    return "+".join(f"({c.p}{'/'+str(c.q) if c.q!=1 else ''})*u^{a}*b^{bb}*v^{cc}" for (a,bb,cc),c in out.items() if c!=0)
names = ["f0","f1","f2","f11","f12","f21","f22"]
txt = f"ring r={p},(t,u,b,v),dp;\noption(redSB);\nshort=0;\n"
for nm in names: txt += f"poly {nm}={slice_poly(G[nm])};\n"
txt += f"poly Dl={sg(Dl.subs(S, s0))};\npoly Dp=u*(1-({s0})^2)-2*({s0});\n"
txt += """proc rep(string nm, ideal J){ ideal G=std(J); nm," | size",size(G),"dim",dim(G),"unit",(G[1]==1); }\n"""
fac = {"u":"u","v":"v","b":"b","D":"Dp","L":"Dl"}
gsets = [["f0","f1","f2","f11"],["f0","f1","f11"],["f0","f2","f12"],["f0","f2","f22"],["f0","f1","f12"],["f0","f1","f2"],["f0","f11"],["f0","f1","f2","f12"]]
for gs in gsets:
    for r in range(5,0,-1):
        for sf in itertools.combinations(fac, r):
            P = "*".join(fac[x] for x in sf)
            txt += f"rep(\"{'+'.join(gs)} | sat {''.join(sf)}\", ideal({','.join(gs)},1-t*({P})));\n"
txt += "quit;\n"
open(f"p15_s{s0}.sing","w").write(txt)
