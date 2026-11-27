import sympy as sp
lg, u, C, w1, q, th, Lc = sp.symbols("ell u C w1 q th Lc2")
c2s = 1/(1+u**2)
b = -16*(3 - 2*c2s)*lg**2 - 32*q*(5 - 2*c2s)*lg + 32*u*(1 + c2s)*C - 64*q**2 - 2*w1*(1 + 2*c2s)
# check against l3explore's printout
chk = (-16*(3*u**2+1)/(u**2+1)*lg**2 - 32*q*(5*u**2+3)/(u**2+1)*lg + 32*u*(u**2+2)/(u**2+1)*C - 2*(32*q**2*(u**2+1) + (u**2+3)*w1)/(u**2+1))
print("b matches:", sp.simplify(b - chk))
def D(f):
    return sp.diff(f, u)*(1+u**2) + sp.diff(f, lg)*(-u) + sp.diff(f, C)*(2*lg + 2*q) + sp.diff(f, th) + sp.diff(f, Lc)*lg**2
mons = [1, th, lg, lg**2, C, Lc, th*lg, lg*C, th*C]
deg = 4
unk = []; F = 0
for i, m in enumerate(mons):
    cs = sp.symbols(f"a{i}_0:{deg+1}")
    unk += cs
    F += sum(c*u**k for k, c in enumerate(cs))/(1+u**2)*m
res = sp.expand(sp.together(D(F) - b)*(1+u**2)**2)
P = sp.Poly(res, u, lg, C, th, Lc)
eqs = [co for mon, co in P.terms()]
sol = sp.solve(eqs, unk, dict=True)
print(len(sol))
if sol:
    Fs = sp.simplify(F.subs(sol[0]).subs({x: 0 for x in unk}))
    print("B =", sp.collect(sp.expand(Fs), [Lc, C, th, lg], evaluate=True))
