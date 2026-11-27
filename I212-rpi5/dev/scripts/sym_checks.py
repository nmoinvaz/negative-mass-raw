exec(open('red2.py').read().split("res = {}")[0])
Fpp, Ls, Npsol = pickle.load(open('masterBK.pkl','rb'))
Ypp, LsG, NpG = pickle.load(open('masterG1.pkl','rb'))
Rp = sp.diff(R, rho); Ap = sp.diff(A, rho); Pp = sp.diff(P0, rho)
cF1 = sp.simplify(Fpp.coeff(sp.diff(F, rho)))
rest = sp.expand(Fpp - cF1*sp.diff(F, rho))
cF0 = sp.simplify(rest.coeff(F))
Ut = cF0 - W**2/A**2
# (1) (41) symbolic: A*Ut == (eps Pp^2/Rp^2 (R^2 V - 1) + 2 Pp R Vp/Rp + eps Vpp)
rhs41 = eps*Pp**2/Rp**2*(R**2*Vs - 1) + 2*Pp*R*Vp/Rp + eps*Vpp
d = A*Ut - rhs41
d = bg(d.subs(eps**2, 1))
print('(41) symbolic difference (eps generic):', sp.simplify(d.subs(eps, -1)), '| eps=+1:', sp.simplify(d.subs(eps, 1)))
# (2) gauge map F = -P0' Y / R'   (G1 -> BK)
Yf = sp.Function('Y')(rho)
Fm = -Pp*Yf/Rp
expr = sp.diff(Fm, rho, 2) - (Fpp.subs(F, Fm).subs(sp.diff(F, rho), sp.diff(Fm, rho)))
expr = expr.doit()
for _ in range(3):
    expr = expr.subs(sp.diff(Yf, rho, 3), sp.diff(Ypp, rho)).subs(sp.diff(Yf, rho, 2), Ypp).doit()
print('gauge map residual:', bg(expr))
