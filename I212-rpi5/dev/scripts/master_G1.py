exec(open('red2.py').read().split("res = {}")[0])
E = pickle.load(open('E_G1.pkl','rb'))
Rp = sp.diff(R, rho); Ap = sp.diff(A, rho)
Ls = (sp.diff(Y, rho) - Ap*Y/(2*A))/Rp
# scalar eq: solve for N'
Np = sp.Symbol('Np')
S = E['S'].subs(sp.diff(N, rho), Np)
Npsol = sp.solve(S, Np)[0]
print('N\' =', sp.simplify(Npsol.subs(L, Ls).doit()))
# theta-theta
e22 = E[(2,2)].subs(sp.diff(N, rho), Np).subs(Np, Npsol)
e22 = e22.subs(L, Ls).doit()
e22 = bg(e22)
Ypp = sp.solve(e22, sp.diff(Y, rho, 2))[0]
Ypp = sp.simplify(Ypp)
print('Y\'\' =', Ypp)
pickle.dump((Ypp, Ls, Npsol), open('masterG1.pkl','wb'))
# check tt, rr
def check(key):
    e = E[key]
    e = e.subs(sp.diff(N, rho, 2), sp.diff(Npsol, rho)).subs(sp.diff(N, rho), Npsol)
    e = e.subs(L, Ls).doit()
    for _ in range(3):
        e = e.subs(sp.diff(Y, rho, 3), sp.diff(Ypp, rho)).subs(sp.diff(Y, rho, 2), Ypp)
        e = e.doit()
    e = e.subs(L, Ls).doit()
    for _ in range(3):
        e = e.subs(sp.diff(Y, rho, 3), sp.diff(Ypp, rho)).subs(sp.diff(Y, rho, 2), Ypp).doit()
    return bg(e)
for key in [(0,0),(1,1)]:
    print(key, 'residual:', check(key))
