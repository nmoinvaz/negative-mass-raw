import sympy as sp
lg, u, C, D3, w0, w1, w2, q, th = sp.symbols("ell u C D3 w0 w1 w2 q th")
S = u**2/(1+u**2); c2s = 1/(1+u**2)
L1 = -2*w0 + 4*lg; L2 = -2*w1 - 4*w0*lg + 16*lg**2 + 16*u*C
Y1 = 2*lg; Y2 = 4*w0*lg - 6*lg**2; Y3 = 4*w1*lg - 4*lg**3 + 32*lg**2 - 16*w0*lg + 32*u*C - 16*D3
c1 = w0 - 3*lg - 1 + c2s
c2 = -2*w0*lg + w1 + lg**2 - 2*lg + 2*lg*c2s
c3 = 2*w0*lg**2 - 2*w1*lg + w2 - 2*lg**3 - 2*lg**2 + 2*lg**2*c2s
h3 = S*L2 + c3 + Y1*c2 + Y2*c1 + Y3/2
def D(f):
    return sp.diff(f, u)*(1+u**2) + sp.diff(f, lg)*(-u) + sp.diff(f, C)*(2*lg + 2*q) + sp.diff(f, D3)*2*C
b = sp.together(sp.expand(D(h3)/u).subs(w0, -4*q))
b = sp.apart(sp.expand(sp.simplify(b)), u)
b = sp.expand(b)
for term in sorted(sp.Add.make_args(b), key=str)[:0]: print(term)
# group by generator monomials
P = sp.Poly(b, lg, C, D3)
for mon, co in P.terms():
    print(mon, sp.factor(sp.simplify(co)))
