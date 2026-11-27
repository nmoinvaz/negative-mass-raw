exec(open('red2.py').read().split("res = {}")[0])
import mpmath as mp
Fpp, Ls, Npsol = pickle.load(open('masterBK.pkl','rb'))
cF1 = sp.simplify(Fpp.coeff(sp.diff(F, rho)))
rest = sp.expand(Fpp - cF1*sp.diff(F, rho))
cF0 = sp.simplify(rest.coeff(F))
Ut = cF0 - W**2/A**2          # U-tilde: F'' + (A'/A+2R'/R) F' - (W^2/A^2 + Ut) F = 0
b, c, m = sp.symbols('b c m', positive=True)
Rx = sp.sqrt(rho**2 + b**2)
Ax = Rx**2*(c/b**2 + 1/Rx**2 + 3*m/b**3*(b*rho/Rx**2 + sp.atan(rho/b)))
P0x = sp.sqrt(2)*sp.atan(rho/b)
Vx = -(sp.diff(Ax, rho, 2)*Rx**2 + 2*sp.diff(Ax, rho)*Rx*sp.diff(Rx, rho))/(2*Rx**2)
psi = sp.atan(rho/b)
Vclosed = -(c/b**2)*(3 - 2*sp.cos(psi)**2) - 3*m/b**3*(3*sp.sin(psi)*sp.cos(psi) + psi*(3 - 2*sp.cos(psi)**2))
# V_phi, V_phiphi on the background
Vp_x = sp.diff(Vclosed, rho)/sp.diff(P0x, rho)
Vpp_x = sp.diff(Vp_x, rho)/sp.diff(P0x, rho)
subsd = {c: sp.Rational(-3,10), m: sp.Rational(1,3), b: sp.Rational(1)*sp.pi/2*sp.Rational(1)}
def num(expr, r0):
    f = sp.lambdify(rho, expr.subs(subsd), 'mpmath')
    return f(r0)
mp.mp.dps = 30
# bg check
for r0 in [mp.mpf('0.7'), mp.mpf('-1.3'), mp.mpf('2.4')]:
    d = num(Vx - Vclosed, r0)
    print('V(4) vs -(A R^2... )/ : ', mp.nstr(d, 5))
# Ut on the family
Ut_f = Ut.subs({A: Ax, R: Rx, P0: P0x, eps: -1}).doit()
Ut_f = Ut_f.subs(W, 0)
eps_v = -1
Rp, Pp = sp.diff(Rx, rho), sp.diff(P0x, rho)
rhs41 = eps_v*Pp**2/Rp**2*(Rx**2*Vclosed - 1) + 2*Pp*Rx*Vp_x/Rp + eps_v*Vpp_x
rhs41_flip = eps_v*Pp**2/Rp**2*(1 - Rx**2*Vclosed) - 2*Pp*Rx*Vp_x/Rp + eps_v*Vpp_x
for r0 in [mp.mpf('0.7'), mp.mpf('-1.3'), mp.mpf('2.4')]:
    u = num(Ut_f, r0); a = num(Ax, r0); r41 = num(rhs41, r0)
    print(f'rho={r0}: Ut={mp.nstr(u,12)}  A={mp.nstr(a,8)}  (41)rhs={mp.nstr(r41,12)}  Ut/(41)rhs={mp.nstr(u/r41,8)}  1/A={mp.nstr(1/a,8)}  A={mp.nstr(a,8)}')
