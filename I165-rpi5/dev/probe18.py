import pickle, sys, sympy as sp
G = pickle.load(open("gens_l2.pkl","rb"))
Dl = sp.sympify(pickle.load(open("delta.pkl","rb"))[0])
U,B,V,S = sp.symbols('u b v s')
s0 = sp.Rational(sys.argv[1]); nprimes = int(sys.argv[2]); tag = sys.argv[3]
primes = []
q = 2147483647
while len(primes) < nprimes:
    q -= 2
    if sp.isprime(q): primes.append(q)
print("primes", primes)
def sg(e): return str(e).replace("**","^")
def slice_poly(d):
    out = {}
    for (mu,mb,mv,ms),c in d.items():
        out[(mu,mb,mv)] = out.get((mu,mb,mv),0) + sp.Rational(c)*s0**ms
    return "+".join(f"({c.p}{'/'+str(c.q) if c.q!=1 else ''})*u^{a}*b^{bb}*v^{cc}" for (a,bb,cc),c in out.items() if c!=0)
slc = {nm: slice_poly(G[nm]) for nm in ["f0","f1","f2","f11"]}
DlS = sg(sp.expand(Dl.subs(S, s0)))
Dp = sg(sp.expand(U*(1-s0**2)-2*s0))
for p in primes:
    txt = f"ring r={p},(t,u,b,v),dp;\noption(redSB);\nshort=0;\n"
    for nm,t_ in slc.items(): txt += f"poly {nm}={t_};\n"
    txt += f"poly Dl={DlS};\npoly Dp={Dp};\npoly P=u*v*b*Dp*Dl;\nideal J=f0,f1,f2,f11,1-t*P;\nmatrix T; ideal Gb=liftstd(J,T);\n"
    txt += f'string fn="{tag}_p{p}.txt";\nwrite(":w "+fn, "G1 "+string(Gb[1])+" n "+string(size(Gb)));\nint i; for(i=1;i<=ncols(J);i++){{ write(":a "+fn, "C "+string(i)+" "+string(T[i,1])); }}\nquit;\n'
    open(f"{tag}_p{p}.sing","w").write(txt)
open(f"{tag}_primes.txt","w").write("\n".join(map(str,primes)))
