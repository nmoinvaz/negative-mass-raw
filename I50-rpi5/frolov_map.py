"""Map from the Roberts parameters (C1, C2) of [Mae09] to [Fro97]'s p, and its check (#50).

Formulas are typed here from the quoted TeX lines (quotes.md), not read from the files.

[Mae09] (arXiv:0811.2962v2, eq. roberts1, roberts2, roberts-mass), G = c = 1:
    ds^2 = -2 du dv + (-uv + C1 v^2 + C2 u^2) dOmega^2,  R^mu_nu = 8 pi eps phi^,mu phi_,nu,
    phi = phi0 +- (1/(2 sqrt(pi))) atanh((1 - 2 C1 v/u)/sqrt(1 - 4 C1 C2)),
    m_MS = -(1 - 4 C1 C2) u v / (4 sqrt(-uv + C1 v^2 + C2 u^2)).
[Fro97] (arXiv:gr-qc/9704040v1, eq. metric, es, ss_soln, const_phi, mass, ah):
    ds^2 = -2 e^{2 Sigma} du dv + R^2 dOmega^2, Sigma = 0, R^2 = u^2 - uv - p v^2,
    Phi = (1/2) ln[-(2 p v + u (1 - sqrt(1+4p)))/(2 p v + u (1 + sqrt(1+4p)))] + varphi(p),
    equations (es:3)-(es:7), 1 - 2M/R = 2 g^{uv} R_,u R_,v, apparent horizon R_,v = 0, region u < 0 < v.

Claimed map (C2 > 0):  U = sqrt(C2) u,  V = v / sqrt(C2),  p = -C1 C2,  Phi = 2 sqrt(pi) phi up to sign and a constant.

usage: python -I frolov_map.py [--mutate=NAME]
  NAME: p_sign, no_c2, p_double, p_shift (change p(C1, C2)); no_rescale, swap_uv (change the coordinates);
        eps_sign (flip the sign of the scalar energy in the Einstein equations).
Exit 0 only if every check passes; exit 1 if any fails (each mutation must exit 1).
"""
import sys
import sympy as sp
import mpmath as mp

MUT = None
for a in sys.argv[1:]:
    if a.startswith('--mutate='):
        MUT = a.split('=', 1)[1]
    else:
        sys.exit('unknown argument ' + a)
if MUT not in (None, 'p_sign', 'no_c2', 'p_double', 'p_shift', 'no_rescale', 'swap_uv', 'eps_sign'):
    sys.exit('unknown mutation ' + str(MUT))

FAILS = []
NPASS = 0


def check(name, ok, detail=''):
    global NPASS
    if ok:
        NPASS += 1
    else:
        FAILS.append(name)
    print('PASS' if ok else 'FAIL', name, detail)


def zero(e):
    return sp.simplify(sp.together(e)) == 0


# ---- the claim, with the mutations applied to it ---------------------------------------------------------
def p_claim(C1x, C2x):
    """[Fro97]'s p as a function of the Roberts parameters."""
    if MUT == 'p_sign':
        return C1x * C2x
    if MUT == 'no_c2':
        return -C1x
    if MUT == 'p_double':
        return -2 * C1x * C2x
    if MUT == 'p_shift':
        return -C1x * C2x + sp.Rational(1, 4)
    return -C1x * C2x


def coords_claim(uu, vv, cc):
    """Frolov's (U, V) as functions of Maeda's (u, v); cc = sqrt(C2)."""
    if MUT == 'no_rescale':
        return uu, vv
    if MUT == 'swap_uv':
        return vv, uu
    return cc * uu, vv / cc


EPS_SIGN = -1 if MUT == 'eps_sign' else 1      # the claimed sign of the scalar energy where phi is real

# ---- symbols: c = sqrt(C2) > 0, t = sqrt(1 - 4 C1 C2) (real: normal side; imaginary: ghost side) ---------
u, v, c, t = sp.symbols('u v c t')
C2 = c**2
C1 = (1 - t**2) / (4 * c**2)
assert sp.simplify(1 - 4 * C1 * C2 - t**2) == 0

# [Mae09]
Q_M = -u * v + C1 * v**2 + C2 * u**2
phi_M = sp.atanh((1 - 2 * C1 * v / u) / t) / (2 * sp.sqrt(sp.pi))
m_M = -(1 - 4 * C1 * C2) * u * v / (4 * sp.sqrt(Q_M))

# [Fro97]; s = sqrt(1+4p), p = (s^2-1)/4 keeps the derivatives rational
Uf, Vf, s = sp.symbols('U V s')
p_s = (s**2 - 1) / 4
Q_F = Uf**2 - Uf * Vf - p_s * Vf**2
Phi_F = sp.log(-(2 * p_s * Vf + Uf * (1 - s)) / (2 * p_s * Vf + Uf * (1 + s))) / 2     # + varphi(p), a constant

# ---- Ricci tensor of -2 du dv + Q(u,v) dOmega^2, from the metric with an undetermined Q --------------------
X = sp.symbols('x0 x1 x2 x3')
Qf = sp.Function('Q')(X[0], X[1])
g = sp.zeros(4)
g[0, 1] = g[1, 0] = -1
g[2, 2] = Qf
g[3, 3] = Qf * sp.sin(X[2])**2
gi = g.inv()


def Gam(a, b, cc):
    return sum(gi[a, d] * (sp.diff(g[d, b], X[cc]) + sp.diff(g[d, cc], X[b]) - sp.diff(g[b, cc], X[d])) for d in range(4)) / 2


G3 = [[[sp.simplify(Gam(a, b, cc)) for cc in range(4)] for b in range(4)] for a in range(4)]


def Ric(b, cc):
    return sp.simplify(sum(sp.diff(G3[a][b][cc], X[a]) - sp.diff(G3[a][b][a], X[cc])
                           + sum(G3[a][a][d] * G3[d][b][cc] - G3[a][cc][d] * G3[d][b][a] for d in range(4))
                           for a in range(4)))


RIC = (Ric(0, 0), Ric(1, 1), Ric(0, 1), Ric(2, 2))


def ricci_of(Qexpr, uu, vv):
    """(Ric_uu, Ric_vv, Ric_uv, Ric_theta,theta) of the metric with Q = Qexpr(uu, vv)."""
    rep = {Qf: Qexpr.subs({uu: X[0], vv: X[1]})}
    return [sp.simplify(e.subs(rep).doit().subs({X[0]: uu, X[1]: vv})) for e in RIC]


# R0: the Ricci code on a known case and against the reduced formulas -----------------------------------------
r0 = ricci_of((u - v / 2)**2, u, v)
check('R0.flat', all(zero(e) for e in r0), 'Ricci of R^2 = (u - v/2)^2 (C1 C2 = 1/4) vanishes')
q = sp.Function('q')(u, v)
rg = ricci_of(q, u, v)
red = [-sp.diff(q, u, 2) / q + sp.diff(q, u)**2 / (2 * q**2),
       -sp.diff(q, v, 2) / q + sp.diff(q, v)**2 / (2 * q**2),
       -sp.diff(q, u, v) / q + sp.diff(q, u) * sp.diff(q, v) / (2 * q**2)]
check('R0.reduced', all(zero(a - b) for a, b in zip(rg[:3], red)), 'Ric_AB = -2 R_;AB / R with R = sqrt(q)')

# F: the typed [Fro97] solution solves the typed [Fro97] equations (Sigma = 0) -------------------------------
Rf = sp.sqrt(Q_F)
Pu, Pv = sp.diff(Phi_F, Uf), sp.diff(Phi_F, Vf)
F_eqs = {
    'F1.es3': sp.diff(Q_F, Uf, Vf) + 1,
    'F2.es4': -2 * sp.diff(Rf, Uf) * sp.diff(Rf, Vf) / Q_F - 1 / Q_F + 2 * Pu * Pv,
    'F3.es5': sp.diff(Rf, Vf, 2) + Rf * Pv**2,
    'F4.es6': sp.diff(Rf, Uf, 2) + Rf * Pu**2,
    'F5.es7': sp.diff(Phi_F, Uf, Vf) + sp.diff(Rf, Vf) * Pu / Rf + sp.diff(Rf, Uf) * Pv / Rf,
}
for k, e in F_eqs.items():
    check(k, zero(e), '(p = (s^2-1)/4)')
rF = ricci_of(Q_F, Uf, Vf)
check('F6.norm', zero(rF[0] - 2 * Pu**2) and zero(rF[1] - 2 * Pv**2) and zero(rF[2] - 2 * Pu * Pv) and zero(rF[3]),
      'Ric_AB = 2 Phi_,A Phi_,B, Ric_theta,theta = 0, so Phi = 2 sqrt(pi) phi when Ric = 8 pi phi phi')

# M1: metric function under the claimed map ---------------------------------------------------------------------
p_map = p_claim(C1, C2)
U_of, V_of = coords_claim(u, v, c)
Q_F_map = (Uf**2 - Uf * Vf - p_map * Vf**2).subs({Uf: U_of, Vf: V_of})
check('M1.metric', zero(Q_F_map - Q_M), 'R_F^2(U(u,v), V(u,v); p(C1,C2)) = -uv + C1 v^2 + C2 u^2')

# M2: scalar, as a derivative identity (constants drop out), Phi = sigma 2 sqrt(pi) phi, sigma = +-1 ----------
s_map = t if sp.simplify(1 + 4 * p_map - t**2) == 0 else sp.sqrt(sp.simplify(1 + 4 * p_map))
PhiF_p = sp.log(-(2 * p_map * Vf + Uf * (1 - s)) / (2 * p_map * Vf + Uf * (1 + s))) / 2
dPu = sp.diff(PhiF_p, Uf).subs(s, s_map).subs({Uf: U_of, Vf: V_of})
dPv = sp.diff(PhiF_p, Vf).subs(s, s_map).subs({Uf: U_of, Vf: V_of})
du_F = c * dPu           # dU/du = c   (claimed map)
dv_F = dPv / c           # dV/dv = 1/c
du_M = 2 * sp.sqrt(sp.pi) * sp.diff(phi_M, u)
dv_M = 2 * sp.sqrt(sp.pi) * sp.diff(phi_M, v)
sigma = [sg for sg in (1, -1) if zero(du_F - sg * du_M) and zero(dv_F - sg * dv_M)]
check('M2.scalar', len(sigma) == 1, 'Phi_F,u = sigma 2 sqrt(pi) phi_M,u and the v derivative, sigma = %s' % sigma)

# M3: Einstein equations of the Maeda side, an identity in t (t real: normal, t imaginary: ghost) ---------------
rM = ricci_of(Q_M, u, v)
phu, phv = sp.diff(phi_M, u), sp.diff(phi_M, v)
check('M3.einstein', zero(rM[0] - 8 * sp.pi * EPS_SIGN * phu**2) and zero(rM[1] - 8 * sp.pi * EPS_SIGN * phv**2)
      and zero(rM[2] - 8 * sp.pi * EPS_SIGN * phu * phv) and zero(rM[3]),
      'Ric_AB = 8 pi eps phi_,A phi_,B and Ric_theta,theta = 0, eps = %d for real phi (t real); t imaginary gives phi imaginary, eps = -1' % EPS_SIGN)

# M4: where the thresholds sit, from the claimed p(C1, C2) ----------------------------------------------------
A1, A2 = sp.symbols('A1 A2', positive=True)
pc = p_claim(A1, A2)
crit = sp.simplify(p_claim(sp.Integer(0), A2))
flat = sp.solve(sp.Eq(1 + 4 * pc, 0), A1)
check('M4.critical_member', crit == 0, 'p(C1 = 0, C2) = %s' % crit)
check('M4.flat_point', len(flat) == 1 and sp.simplify(flat[0] - 1 / (4 * A2)) == 0, '1 + 4p = 0 at C1 = %s (Minkowski: 4 C1 C2 = 1)' % flat)
check('M4.sign_BH', bool(sp.simplify(sp.diff(pc, A1)).is_negative),
      'p decreases as C1 rises: BH (p > 0) is C1 < 0, dispersal is C1 > 0')

# M5: apparent horizon R_,v = 0 ------------------------------------------------------------------------------
Vah = sp.solve(sp.Eq(sp.diff(Uf**2 - Uf * Vf - p_map * Vf**2, Vf), 0), Vf)[0]
rel = sp.simplify(Vah.subs(Uf, U_of) - V_of)
us = sp.solve(sp.Eq(rel, 0), u)
check('M5.horizon', len(us) == 1 and zero(us[0] - 2 * C1 * v), 'R_F,V = 0 maps to u = 2 C1 v (theta_v = 0 line of bh_to_wormhole.md sec. 2): %s' % us)

# M6: Misner-Sharp mass, [Fro97] 1 - 2M/R = 2 g^{uv} R_,u R_,v with g^{uv} = -1, against the printed (roberts-mass).
# Compare squares (rational) and the sign at u < 0 < v.
Rp = sp.sqrt(Uf**2 - Uf * Vf - p_map * Vf**2)
M_F = (Rp / 2 * (1 + 2 * sp.diff(Rp, Uf) * sp.diff(Rp, Vf))).subs({Uf: U_of, Vf: V_of})
sq_ok = zero(sp.simplify(M_F**2 - m_M**2))
pt = {u: sp.Rational(-13, 10), v: sp.Rational(7, 10), c: sp.Rational(3, 2), t: sp.Rational(7, 10)}
sign_ok = abs(sp.N((M_F - m_M).subs(pt), 30)) < sp.Float('1e-20')
check('M6.mass', bool(sq_ok and sign_ok), 'M_F(U(u,v), V(u,v); p) = m_MS of (roberts-mass): squares equal %s, value equal at u=-1.3, v=0.7, c=1.5, t=0.7: %s' % (sq_ok, sign_ok))

# ---- N: numeric check of the typed log formula, principal branch, in three sectors -------------------------------
mp.mp.dps = 30


def PhiF_num(U, V, p):
    sq = mp.sqrt(1 + 4 * p)
    varphi = -mp.log((sq - 1) / (sq + 1)) / 2
    return mp.log(-(2 * p * V + U * (1 - sq)) / (2 * p * V + U * (1 + sq))) / 2 + varphi


Uu, Vv = mp.mpf('-1.3'), mp.mpf('0.7')
a = PhiF_num(Uu, Vv, mp.mpf('0.3'))
b = PhiF_num(Uu, Vv, mp.mpf('-0.1'))
cg = PhiF_num(Uu, Vv, mp.mpf('-0.9'))
tol = mp.mpf('1e-20')
if MUT == 'eps_sign':
    ok_ghost = abs(mp.im(cg)) < tol                       # claim: no imaginary part on the ghost side
else:
    ok_ghost = abs(mp.re(cg)) < tol and abs(mp.im(cg)) > mp.mpf('1e-3')
check('N1.real_BH', abs(mp.im(a)) < tol and abs(a) > mp.mpf('1e-3'), 'p = 0.3: Phi real, %s' % mp.nstr(a, 8))
check('N2.real_dispersal', abs(mp.im(b)) < tol and abs(b) > mp.mpf('1e-3'), 'p = -0.1: Phi real, %s' % mp.nstr(b, 8))
check('N3.imaginary_ghost', ok_ghost, 'p = -0.9 < -1/4: Phi purely imaginary, %s' % mp.nstr(cg, 8))
check('N4.v0', abs(PhiF_num(Uu, mp.mpf(0), mp.mpf('0.3'))) < mp.mpf('1e-25'), 'Phi(u, v = 0) = 0 at p = 0.3')

# numeric cross-check of M2: C2 = 2.25, one point per sector; inverse of the claimed p(C1, C2) taken from p_claim itself
C2n = mp.mpf('2.25')
cn = mp.sqrt(C2n)
un, vn = mp.mpf('-0.8'), mp.mpf('0.5')
for name, pt_ in (('BH', mp.mpf('0.3')), ('dispersal', mp.mpf('-0.1')), ('ghost', mp.mpf('-0.9'))):
    # solve p_claim(C1n, C2n) = pt_ for C1n numerically
    C1n = mp.findroot(lambda z: mp.mpf(sp.N(p_claim(sp.Float(str(z), 30), sp.Float(str(C2n), 30)), 30)) - pt_, -pt_ / C2n)
    tn = mp.sqrt(1 - 4 * C1n * C2n + 0j)
    fM = lambda uu: mp.atanh((1 - 2 * C1n * vn / uu) / tn) / (2 * mp.sqrt(mp.pi))
    dM = 2 * mp.sqrt(mp.pi) * mp.diff(fM, un)
    Uc, Vc = coords_claim(un, vn, cn)

    def gF(uu):
        Ux, Vx = coords_claim(uu, vn, cn)
        return PhiF_num(Ux, Vx, pt_)
    dF = mp.diff(gF, un)
    r = min(abs(dF - dM), abs(dF + dM)) / max(abs(dM), mp.mpf('1e-30'))
    check('N5.d_u_' + name, r < mp.mpf('1e-15'), 'p = %s, C1 = %s: |Phi_F,u -+ 2 sqrt(pi) phi_M,u| / |.| = %s' % (mp.nstr(pt_, 3), mp.nstr(C1n, 6), mp.nstr(r, 3)))

print()
print('mutation:', MUT, '| PASS', NPASS, '| FAIL', len(FAILS), FAILS)
sys.exit(1 if FAILS else 0)
