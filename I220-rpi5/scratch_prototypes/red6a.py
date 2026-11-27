"""dev: the decomposition of the reduced integrand of G6 as Laurent polynomials in u"""
import pickle
import sys
sys.path.insert(0, "/tmp/claude-1000/-home-nathan-Source-negative-mass-i220/e48dd6bd-94ac-46f2-8d9d-42321d8492dd/scratchpad")
import sympy as sp  # noqa: E402
import proto6 as P  # noqa: E402

lg, S, u, C, D3, Lc, th, q = P.lg, P.S, P.u, P.C, P.D3, P.Lc, P.th, P.q
w = P.w
I6 = P.I6
# S -> u^2/(1+u^2)
I6u = sp.expand(sp.together(I6.subs(S, u**2 / (1 + u**2))))
num, den = sp.fraction(sp.together(I6u))
print("denominator:", sp.factor(den))
I6u = sp.expand(sp.cancel(I6u))
poly = sp.Poly(I6u, C, D3, Lc)
out = {}
for mon, cf in poly.terms():
    cf = sp.expand(cf)
    # Laurent in u: multiply by u^k to make polynomial
    cfr = sp.together(cf)
    n, d = sp.fraction(cfr)
    print(mon, "denominator", sp.factor(d))
    out[mon] = cfr
pickle.dump(out, open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i220/e48dd6bd-94ac-46f2-8d9d-42321d8492dd/scratchpad/I6_parts.pkl", "wb"))
for mon, cf in out.items():
    cf = sp.expand(cf)
    pu = sp.collect(cf, u, evaluate=False)
    print("== monomial (C, D3, Lc) exponents", mon)
    def ex(e):
        return 0 if e == 1 else e.as_base_exp()[1]
    for k in sorted(pu, key=ex):
        print("   u-part", k, ":", sp.factor(pu[k]))
