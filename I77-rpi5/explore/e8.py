import sys, time, random, pickle
src = open("e7.py").read().split("t1 = time.time()")[0]
exec(src)
th0 = (sp.Rational(int(sys.argv[1]), int(sys.argv[2])), sp.Rational(int(sys.argv[3]), int(sys.argv[2])))
t1 = time.time()
Ric = ricci_at(th0)
out = {}
for k, e in Ric.items():
    num, den = sp.fraction(sp.cancel(sp.together(e)))
    num = sp.expand(num.subs(r, 1))
    P = sp.Poly(num, *Wd[:5])
    f = sp.factor_list(num)
    print(k, "terms", len(P.terms()), "deg", P.total_degree(), "factors", [(sp.Poly(g, *Wd[:5]).total_degree(), m, len(sp.Poly(g,*Wd[:5]).terms())) for g, m in f[1]], "time", time.time()-t1, flush=True)
    out[k] = (str(num), str(sp.factor(den.subs(r,1))))
pickle.dump(out, open(f"ricnum_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}.pkl", "wb"))
