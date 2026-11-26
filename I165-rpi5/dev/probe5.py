import time, sympy as sp, collections, pickle
exec(open("probe4.py").read().split("Cb = X(")[0])   # reuse the field setup (fields X1c,X2c, sx, sr)
t1=time.time()
U_,B_,V_,S_=sp.symbols('u b v s')
NC = pickle.load(open("NC4new.pkl","rb"))[0]
F0 = K.from_expr(NC)
g1 = X(F0, X1c); g2 = X(F0, X2c)
print("X1 N_C, X2 N_C", time.time()-t1)
for nm,g in (("g1",g1),("g2",g2)):
    n = g.numer; dn = g.denom
    print(nm, "numer terms", len(n.terms()), "denom terms", len(dn.terms()))
    fl = sp.factor_list(n.as_expr())
    print(nm, "numer factors", [(len(sp.Poly(f,U_,B_,V_,S_).terms()), m, sp.Poly(f,U_,B_,V_,S_).total_degree()) for f,m in fl[1]], time.time()-t1)
    print(nm, "small factors:", [(f,m) for f,m in fl[1] if len(sp.Poly(f,U_,B_,V_,S_).terms())<8])
    print(nm, "denom:", sp.factor_list(dn.as_expr())[1].__repr__()[:300])
    pickle.dump((fl, sp.factor_list(dn.as_expr())), open(f"{nm}_fl.pkl","wb"))
