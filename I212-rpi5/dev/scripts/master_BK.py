exec(open('red2.py').read().split("res = {}")[0])
E = pickle.load(open('E_BK.pkl','rb'))
Rp = sp.diff(R, rho); Ap = sp.diff(A, rho); Pp = sp.diff(P0, rho)
Ls = eps*Pp*R*F/(2*Rp)
Np = sp.Symbol('Np')
e22 = E[(2,2)].subs(sp.diff(N, rho), Np)
e22 = e22.subs(L, Ls).doit()
Npsol = sp.solve(e22, Np)[0]
S = E['S'].subs(sp.diff(N, rho), Np).subs(Np, Npsol).subs(L, Ls).doit()
S = bg(S)
Fpp = sp.simplify(sp.solve(S, sp.diff(F, rho, 2))[0])
print('F\'\' =', Fpp)
pickle.dump((Fpp, Ls, Npsol), open('masterBK.pkl','wb'))
# coefficients
cF1 = sp.simplify(Fpp.coeff(sp.diff(F, rho)))
rest = sp.expand(Fpp - cF1*sp.diff(F, rho))
cF0 = sp.simplify(rest.coeff(F))
print('F\' coeff:', cF1)
print('F coeff:', cF0)
# checks (0,0),(1,1)
def check(key):
    e = E[key]
    e = e.subs(sp.diff(N, rho, 2), sp.diff(Npsol, rho)).subs(sp.diff(N, rho), Npsol)
    e = e.subs(L, Ls).doit()
    for _ in range(3):
        e = e.subs(sp.diff(F, rho, 3), sp.diff(Fpp, rho)).subs(sp.diff(F, rho, 2), Fpp).doit()
    e = e.subs(L, Ls).doit()
    for _ in range(3):
        e = e.subs(sp.diff(F, rho, 3), sp.diff(Fpp, rho)).subs(sp.diff(F, rho, 2), Fpp).doit()
    return bg(e)
for key in [(0,0),(1,1)]:
    print(key, 'residual:', check(key))
