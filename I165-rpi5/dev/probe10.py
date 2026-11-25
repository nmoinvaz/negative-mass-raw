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
    terms=[]
    for (mu,mb,mv),c in out.items():
        if c==0: continue
        terms.append(f"({c.p})*u^{mu}*b^{mb}*v^{mv}" if c.q==1 else f"({c.p}/{c.q})*u^{mu}*b^{mb}*v^{mv}")
    return "+".join(terms) if terms else "0"
Dp = f"(u*(1-({s0})^2)-2*({s0}))"
names = ["f0","f1","f2","f11","f12","f21","f22"]
txt = f"ring r={p},(t,u,b,v),dp;\noption(redSB);\nshort=0;\n"
for nm in names: txt += f"poly {nm}={slice_poly(G[nm])};\n"
txt += f"poly Dl={sg(Dl.subs(S, s0))};\npoly Dp={Dp};\n"
txt += """proc rep(string nm, ideal J){ ideal G=std(J); nm,": size",size(G),"dim",dim(G),"mult",mult(G),"unit",(G[1]==1); }\n"""
sat_factors = {"u":"u","v":"v","b":"b","D":"Dp","Dl":"Dl"}
gsets = [["f0","f1","f2","f11","f12","f21","f22"], ["f0","f1","f2","f11","f12","f22"], ["f0","f1","f2","f11"], ["f0","f1","f2","f12"], ["f0","f1","f2","f22"], ["f0","f1","f2","f11","f22"], ["f0","f1","f2","f11","f12"]]
for gs in gsets:
    for k in range(5,0,-1):
        pass
    for sf in [list(sat_factors), ["u","v","b","D"], ["u","v","b"], ["u","v"], ["v","b"], ["u"], ["v"], ["b"], ["Dl"], ["D"], []]:
        P = "*".join(sat_factors[x] for x in sf) if sf else "1"
        txt += f"rep(\"{'+'.join(gs)} | sat by {','.join(sf) or '-'}\", ideal({','.join(gs)},1-t*({P})));\n"
txt += "quit;\n"
open(f"p10_s{s0}_p{p}.sing","w").write(txt)
