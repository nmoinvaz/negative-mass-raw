"""
Coordinator's independent check of #133 (the count of the tanh wall's Type III points, he_type3_count.md).

Shares no code with he_type3_count.py or he_type3.py and imports nothing from the repository. E1 and E2 come from the
coordinator's own Ricci route of #102's review (ind102.py, raw I102-mac, copied here): the coordinate Ricci tensor of
g = -dt^2 + (dx + w dt)^2 + dy^2 + dz^2 with w the second-order Taylor polynomial of v (1 - f) about r0 (c, s, 0),
frame block B, M = eta B, E1 = c2^2 - 3 c1, E2 = 27 c0 - c2^3. The profile is evaluated in the cosh form
f = (1 + C)/(cosh z + C), z = 2 sigma r, C = cosh 2 sigma R_b (#132, Lean-certified in #134), not in #133's eps form, and
checked against the tanh form. Scans are grids: what they show is numerical evidence, not a proof; the exact parts
(D1) are exact. Usage: python ind133.py [--mutate=lead|sigma|asym|common]

Variables: phi = v F, A = v r a, B = v r^2 b (u = 1/r scaled to 1), w = c^2, y = B - A, psi = A + 2 phi, delta = y.

Criteria, fixed before the first run:
  D0  The cosh form and its z-derivatives agree with the tanh form f = [tanh s(r + R) - tanh s(r - R)] / (2 tanh sR)
      and its r-derivatives at 3 radii per wall to 1e-40 (60 digits).
  D1  Exact. E1, E2 are weighted-homogeneous (a, u weight 1, b weight 2) of weights 4 and 6; at u = 1 with F = phi/v,
      a = A/v, b = B/v they are free of v. sympy.resultant(E1, E2, w) = (27/256) phi^3 (A - B)^3 P exactly with
      P in Z[phi, A, B], neither phi nor A - B dividing P; P has 167 terms, total degrees {10, 12, 14, 16, 18},
      (A, B)-degrees 9 to 15 (every term has j + k >= 9); P(phi, psi - 2 phi, psi - 2 phi + delta) has 358 terms of
      weights 24 to 66 (phi weight 2, psi and delta weight 4), and its weight-24 part is exactly 774144 phi^8 delta^2.
      The phi^3 B^9 coefficient of P is 4.
  D2  Small z. By sympy series with symbolic C: phi = z^2 Phi0 + O(z^4), psi = z^4 Psi0 + O(z^6), delta = z^4 Delta0
      + O(z^6) with Phi0 = v/(2(1 + C)), Psi0 = v (5 - C)/(12 (1 + C)^2), Delta0 = v (5 - C)/(3 (1 + C)^2).
      Numerically at 200 digits on 120 log-spaced z in [1e-8, 1/4] at each wall: P > 0 and delta < 0, and
      P / (774144 Phi0^8 Delta0^2 z^24) is within 1e-6 of 1 at z = 1e-8.
  D3  Large z. At 60 digits on 150 log-spaced z in [z_t, 1e6] (z_t = 40 Le, 60 Rodal): P > 0 and y > 0, and
      P / (4 phi^3 B^9) is within 1e-4 of 1 at z = 1e6.
  D4  Grid scan of [1/4, z_t] in z, step 1e-4, float64 in the cosh form; every sign change confirmed and bisected at
      50 digits in the tanh form. (a) float64 and 50-digit signs of P agree at every 997th grid point. (b) P changes
      sign exactly 4 (Le) and 6 (Rodal) times, at the radii of he_type3_count.md section 5 within 1e-9. (c) Direct
      common roots without the resultant: on each real root branch w1 <= w2 of E1, E2(w) changes sign; each change is
      bisected at 50 digits and is a common root when |E2(w)| <= 1e-30 sum |terms|. The common roots are exactly at
      P's roots (within 1e-9 in r), with w = 0.0600518, 58.459064, 0.0409869, 0.912867 (Le) and 0.957639, 4.1006549,
      8.7172638, 0.284767, 1.030003, 0.977030 (Rodal) within 1e-6, and T = b + a u != 0 (|T| > 1e-3) at each; the 3
      with 0 < w < 1 at each wall are the admissible points. Any other sign change of a branch lies within 1e-6 of
      the root of y (D5) and is not a common root.
  D5  The spurious factor and the coordinator's #102 review (ind102.py C8, 5 and 7 sign changes). (a) y = B - A
      changes sign exactly once on D4's grid, at r = 0.9921149667 (Le) and 4.993740859 (Rodal) within 1e-9.
      (b) There the w^2 coefficient of E1 vanishes to 1e-30 relative, and the finite root of E1 is within 1e-5 of
      -0.358483 (Le) and -6.30241 (Rodal), the w ind102 printed as "rejected"; min over the real roots of E1 of
      |E2(w)| / sum |terms of E2| exceeds 1e-6 at r_y (no common root). (c) The Sylvester resultant of E1 and E2
      (own determinant, 50 digits) changes sign across r_y +- 1e-7 while P does not.
Mutations (each must make the script exit 1):
  lead    the expected weight-24 coefficient 774145: D1 must fail.
  sigma   Le's sigma 8.001 in D4 and D5: D4 and D5 must fail.
  asym    the expected large-z leading term 5 phi^3 B^9: D3 must fail.
  common  D5(b)'s no-common-root test made at Le's first admissible radius instead of r_y: D5 must fail.
Exit 1 if any criterion fails.
"""
import sys, time
import numpy as np
import mpmath as mp
import sympy as sp

mut = next((q.split('=', 1)[1] for q in sys.argv[1:] if q.startswith('--mutate=')), None)
assert mut in (None, 'lead', 'sigma', 'asym', 'common')
T0 = time.time()
Q = sp.Rational
fails = []


def report(name, ok, detail):
    print(f"  {name}: {detail}: {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
    if not ok:
        fails.append(name)


# ---- E1, E2 from the Ricci tensor (copied from ind102.py) ----
v, F, a, b, u, c, s = sp.symbols('v F a b u c s', real=True)
xx, W = sp.symbols('x w')
t, X1, X2, X3 = crd = sp.symbols('t X1 X2 X3', real=True)
d = [X1, X2, X3]
nv = [c, s, 0]
wi = [-v * a * nv[i] for i in range(3)]
wij = [[-v * (b * nv[i] * nv[j] + a * u * ((1 if i == j else 0) - nv[i] * nv[j])) for j in range(3)] for i in range(3)]
wsh = v * F + sum(wi[i] * d[i] for i in range(3)) + sum(wij[i][j] * d[i] * d[j] for i in range(3) for j in range(3)) / 2
g = sp.Matrix([[-1 + wsh ** 2, wsh, 0, 0], [wsh, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
gi = sp.Matrix([[-1, wsh, 0, 0], [wsh, 1 - wsh ** 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
assert (g * gi - sp.eye(4)).applyfunc(sp.expand) == sp.zeros(4)
dg = [[[sp.diff(g[m, n], crd[k]) for k in range(4)] for n in range(4)] for m in range(4)]
Gam = [[[sp.expand(sum(gi[l, m] * (dg[m][i][j] + dg[m][j][i] - dg[i][j][m]) for m in range(4)) / 2)
         for j in range(4)] for i in range(4)] for l in range(4)]
at0 = {X1: 0, X2: 0, X3: 0, t: 0}
G0 = [[[Gam[l][i][j].subs(at0) for j in range(4)] for i in range(4)] for l in range(4)]
Ric = sp.zeros(4)
for i in range(4):
    for j in range(i, 4):
        e = sum(sp.diff(Gam[l][i][j], crd[l]).subs(at0) - sp.diff(Gam[l][i][l], crd[j]).subs(at0) for l in range(4))
        e += sum(G0[l][l][m] * G0[m][i][j] - G0[l][j][m] * G0[m][i][l] for l in range(4) for m in range(4))
        Ric[i, j] = Ric[j, i] = sp.expand(e)
Efr = [[1, -v * F, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
Bm = sp.Matrix(3, 3, lambda i, j: sp.expand(sum(Efr[i][p] * Efr[j][q] * Ric[p, q] for p in range(4) for q in range(4))))
M = sp.diag(-1, 1, 1) * Bm


def red(e):
    p = sp.Poly(sp.expand(e), s)
    return sp.expand(sum(cf * s ** (k % 2) * (1 - c ** 2) ** (k // 2) for (k,), cf in p.terms()))


cp = sp.Poly(sp.expand((xx * sp.eye(3) - M).det()), xx).all_coeffs()
c2, c1, c0 = cp[1], cp[2], cp[3]
E1 = red(c2 ** 2 - 3 * c1)
E2 = red(27 * c0 - c2 ** 3)
assert not E1.has(s) and not E2.has(s)
print(f"# ind133: E1, E2 from the Ricci tensor in {time.time() - T0:.0f} s" + (f", mutate={mut}" if mut else ""),
      flush=True)

# ---- D1 exact ----
ph, A, Bv, psi, dl, lm = sp.symbols('phi A B psi delta lam')
hom1 = sp.expand(E1.subs({a: lm * a, b: lm ** 2 * b, u: lm * u}, simultaneous=True) - lm ** 4 * E1) == 0
hom2 = sp.expand(E2.subs({a: lm * a, b: lm ** 2 * b, u: lm * u}, simultaneous=True) - lm ** 6 * E2) == 0
sub = {F: ph / v, a: A / v, b: Bv / v, u: 1}
E1s = sp.expand(E1.subs(sub, simultaneous=True).subs(c, sp.sqrt(W)))
E2s = sp.expand(E2.subs(sub, simultaneous=True).subs(c, sp.sqrt(W)))
vfree = not E1s.has(v) and not E2s.has(v)
Res = sp.expand(sp.resultant(sp.Poly(E1s, W), sp.Poly(E2s, W)).as_expr())
gens = (ph, A, Bv)
fac = sp.Poly(Q(27, 256) * ph ** 3 * (A - Bv) ** 3, *gens)
qP, rP = sp.Poly(Res, *gens).div(fac)
P = qP
ok_div = rP.is_zero
ok_int = all(cf.is_integer for cf in P.coeffs())
nodiv = not P.div(sp.Poly(ph, *gens))[1].is_zero and not P.div(sp.Poly(A - Bv, *gens))[1].is_zero
terms = P.terms()
tdeg = sorted({sum(m) for m, _ in terms})
abdeg = sorted({m[1] + m[2] for m, _ in terms})
Pe = P.as_expr()
Ph = sp.Poly(sp.expand(Pe.subs({A: psi - 2 * ph, Bv: psi - 2 * ph + dl}, simultaneous=True)), ph, psi, dl)
wts = sorted({2 * m[0] + 4 * m[1] + 4 * m[2] for m, _ in Ph.terms()})
w24 = sum(cf * ph ** m[0] * psi ** m[1] * dl ** m[2] for m, cf in Ph.terms() if 2 * m[0] + 4 * m[1] + 4 * m[2] == 24)
lead = 774145 if mut == 'lead' else 774144
c39 = P.coeff_monomial(ph ** 3 * Bv ** 9)
ok1 = (hom1 and hom2 and vfree and ok_div and ok_int and nodiv and len(terms) == 167 and tdeg == [10, 12, 14, 16, 18]
       and abdeg == list(range(9, 16)) and len(Ph.terms()) == 358 and wts[0] == 24 and wts[-1] == 66
       and sp.expand(w24 - lead * ph ** 8 * dl ** 2) == 0 and c39 == 4)
report("D1 exact", ok1, f"homogeneous {hom1} {hom2}; v-free {vfree}; Res = (27/256) phi^3 (A - B)^3 P: {ok_div}; P integer "
       f"{ok_int}; no extra phi, A - B factor {nodiv}; {len(terms)} terms, total degrees {tdeg}, (A, B)-degrees "
       f"{abdeg[0]}..{abdeg[-1]}; P-hat {len(Ph.terms())} terms, weights {wts[0]}..{wts[-1]}, weight-24 part {w24} "
       f"(expected {lead} phi^8 delta^2); phi^3 B^9 coefficient {c39}")

# ---- numerical machinery ----
e1c = [sp.expand(q) for q in reversed(sp.Poly(E1s, W).all_coeffs())]      # e0, e1, e2
e2c = [sp.expand(q) for q in reversed(sp.Poly(E2s, W).all_coeffs())]      # f0..f3
fP_mp = sp.lambdify(gens, Pe, 'mpmath')
fE1_mp = sp.lambdify(gens, e1c, 'mpmath')
fE2_mp = sp.lambdify(gens, e2c, 'mpmath')
fE2abs_mp = sp.lambdify(gens + (W,), sum(abs(tm) for tm in sp.Add.make_args(E2s)), 'mpmath')
fP_np = sp.lambdify(gens, Pe, 'numpy')
fE1_np = sp.lambdify(gens, e1c, 'numpy')
fE2_np = sp.lambdify(gens, e2c, 'numpy')


def cosh_jets(z, C, vv, lib):
    """phi, A, B from the cosh form at z = 2 sigma r: A = v z f_z, B = v z^2 f_zz."""
    ch, sh = lib.cosh(z), lib.sinh(z)
    den = ch + C
    f_z = -(1 + C) * sh / den ** 2
    f_zz = (1 + C) * (2 * sh ** 2 - ch * den) / den ** 3
    Fv = 2 * lib.sinh(z / 2) ** 2 / den
    return vv * Fv, vv * z * f_z, vv * z ** 2 * f_zz


def tanh_jets(r, sg, Rb, vv):
    tp, tm = mp.tanh(sg * (r + Rb)), mp.tanh(sg * (r - Rb))
    k = 2 * mp.tanh(sg * Rb)
    f = (tp - tm) / k
    f1 = sg * ((1 - tp ** 2) - (1 - tm ** 2)) / k
    f2 = -2 * sg ** 2 * (tp * (1 - tp ** 2) - tm * (1 - tm ** 2)) / k
    return vv * (1 - f), vv * r * f1, vv * r ** 2 * f2, f1, f2


walls = {"Le": dict(sg=mp.mpf('8.001') if mut == 'sigma' else mp.mpf(8), Rb=mp.mpf(1), v=mp.mpf(1) / 2, zt=40,
                    Proots=['0.990567889806', '1.0063451866', '1.02393326111', '1.09466230932'],
                    wref=[0.0600518, 58.459064, 0.0409869, 0.912867], ry='0.9921149667', wy=-0.358483),
         "Rodal": dict(sg=mp.mpf(4), Rb=mp.mpf(5), v=mp.mpf(1), zt=60,
                       Proots=['4.71448517823', '5.02043486647', '5.03374094665', '5.07106634302', '5.07635399285',
                               '5.10338056385'],
                       wref=[0.957639, 4.1006549, 8.7172638, 0.284767, 1.030003, 0.977030], ry='4.993740859',
                       wy=-6.30241)}

# ---- D0 ----
mp.mp.dps = 60
worst = mp.mpf(0)
for nm, W_ in walls.items():
    sg, Rb, vv = W_['sg'], W_['Rb'], W_['v']
    C = mp.cosh(2 * sg * Rb)
    for r in (Rb * mp.mpf('0.3'), Rb * mp.mpf('0.99'), Rb * mp.mpf('1.4')):
        p1, A1, B1, _, _ = tanh_jets(r, sg, Rb, vv)
        p2, A2, B2 = cosh_jets(2 * sg * r, C, vv, mp)
        worst = max(worst, abs(p1 - p2), abs(A1 - A2), abs(B1 - B2))
report("D0 cosh form = tanh form", worst < mp.mpf(10) ** -40, f"largest difference of (phi, A, B) {mp.nstr(worst, 3)}")

# ---- D2 small z ----
zs, Cs, vs = sp.symbols('z C v_', positive=True)
fz = (1 + Cs) / (sp.cosh(zs) + Cs)
phs = vs * (1 - fz)
As = vs * zs * sp.diff(fz, zs)
Bs = vs * zs ** 2 * sp.diff(fz, zs, 2)
ser = lambda e, n: sp.series(e, zs, 0, n).removeO()
s_phi = sp.simplify(ser(phs, 4).coeff(zs, 2))
s_psi = sp.simplify(ser(As + 2 * phs, 6).coeff(zs, 4))
s_dl = sp.simplify(ser(Bs - As, 6).coeff(zs, 4))
low = [sp.simplify(ser(As + 2 * phs, 4)), sp.simplify(ser(Bs - As, 4))]
want = [vs / (2 * (1 + Cs)), vs * (5 - Cs) / (12 * (1 + Cs) ** 2), vs * (5 - Cs) / (3 * (1 + Cs) ** 2)]
okser = all(sp.simplify(x - y) == 0 for x, y in zip([s_phi, s_psi, s_dl], want)) and low == [0, 0]
mp.mp.dps = 200
det2 = [f"series Phi0 {s_phi}, Psi0 {s_psi}, Delta0 {s_dl}, lower orders {low}: {okser}"]
ok2 = okser
for nm, W_ in walls.items():
    sg, Rb, vv = W_['sg'], W_['Rb'], W_['v']
    C = mp.cosh(2 * sg * Rb)
    zgrid = [mp.mpf(10) ** (-8 + k * (8 + mp.log10(mp.mpf(1) / 4)) / 119) for k in range(120)]
    pos = neg = True
    for z in zgrid:
        p_, A_, B_ = cosh_jets(z, C, vv, mp)
        pos &= fP_mp(p_, A_, B_) > 0
        neg &= (B_ - A_) < 0
    z = zgrid[0]
    p_, A_, B_ = cosh_jets(z, C, vv, mp)
    Phi0, Dl0 = vv / (2 * (1 + C)), vv * (5 - C) / (3 * (1 + C) ** 2)
    ratio = fP_mp(p_, A_, B_) / (774144 * Phi0 ** 8 * Dl0 ** 2 * z ** 24)
    ok2 &= pos and neg and abs(ratio - 1) < 1e-6
    det2.append(f"{nm}: P > 0 on all {len(zgrid)}: {pos}, delta < 0: {neg}, ratio at z = 1e-8 is 1 + {mp.nstr(ratio - 1, 3)}")
report("D2 small z", ok2, "; ".join(det2))

# ---- D3 large z ----
mp.mp.dps = 60
ok3, det3 = True, []
kas = 5 if mut == 'asym' else 4
for nm, W_ in walls.items():
    sg, Rb, vv = W_['sg'], W_['Rb'], W_['v']
    C = mp.cosh(2 * sg * Rb)
    lz0, lz1 = mp.log(W_['zt']), mp.log(mp.mpf(10) ** 6)
    pos = ypos = True
    for k in range(150):
        z = mp.exp(lz0 + k * (lz1 - lz0) / 149)
        p_, A_, B_ = cosh_jets(z, C, vv, mp)
        pos &= fP_mp(p_, A_, B_) > 0
        ypos &= (B_ - A_) > 0
    p_, A_, B_ = cosh_jets(mp.mpf(10) ** 6, C, vv, mp)
    ratio = fP_mp(p_, A_, B_) / (kas * p_ ** 3 * B_ ** 9)
    ok3 &= pos and ypos and abs(ratio - 1) < 1e-4
    det3.append(f"{nm}: P > 0 on all 150 of [{W_['zt']}, 1e6]: {pos}, y > 0: {ypos}, P/({kas} phi^3 B^9) at 1e6 = 1 + "
                f"{mp.nstr(ratio - 1, 3)}")
report("D3 large z", ok3, "; ".join(det3))

# ---- D4, D5 grid ----
mp.mp.dps = 50


def mp_at_r(r, W_):
    p_, A_, B_, f1, f2 = tanh_jets(r, W_['sg'], W_['Rb'], W_['v'])
    return p_, A_, B_, f2 + f1 / r                      # T = b + a u


def bisect(fun, lo, hi, n=120):
    flo = fun(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = fun(mid)
        if fm * flo > 0:
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def e1roots_mp(p_, A_, B_):
    e0, e1, e2 = fE1_mp(p_, A_, B_)
    return [mp.re(q) for q in mp.polyroots([e2, e1, e0], maxsteps=200, extraprec=200) if abs(mp.im(q)) < 1e-30] \
        if abs(e2) > mp.mpf(10) ** -40 * (abs(e0) + abs(e1)) else [-e0 / e1]


def E2rel(p_, A_, B_, w_):
    f0, f1_, f2_, f3 = fE2_mp(p_, A_, B_)
    return abs(f0 + w_ * (f1_ + w_ * (f2_ + w_ * f3))) / fE2abs_mp(p_, A_, B_, w_)


def branch_val(r, W_, ib):
    p_, A_, B_, _ = mp_at_r(r, W_)
    e0, e1, e2 = fE1_mp(p_, A_, B_)
    dsc = e1 ** 2 - 4 * e2 * e0
    if dsc < 0:
        return None
    sq = mp.sqrt(dsc)
    ws = sorted([(-e1 - sq) / (2 * e2), (-e1 + sq) / (2 * e2)])
    f0, f1_, f2_, f3 = fE2_mp(p_, A_, B_)
    w_ = ws[ib]
    return f0 + w_ * (f1_ + w_ * (f2_ + w_ * f3)), w_


ok4, ok5, det4, det5 = True, True, [], []
for nm, W_ in walls.items():
    sg, Rb, vv, zt = W_['sg'], W_['Rb'], W_['v'], W_['zt']
    C = float(mp.cosh(2 * sg * Rb))
    z = np.arange(0.25, zt + 1e-12, 1e-4)
    rr = z / (2 * float(sg))
    p_, A_, B_ = cosh_jets(z, C, float(vv), np)
    Pn = fP_np(p_, A_, B_)
    # (a) float64 against 50 digits
    agree = all(np.sign(Pn[k]) == mp.sign(fP_mp(*mp_at_r(mp.mpf(rr[k]), W_)[:3])) for k in range(0, len(z), 997))
    # (b) P's sign changes
    idx = np.nonzero(np.sign(Pn[:-1]) * np.sign(Pn[1:]) < 0)[0]
    Proot = [bisect(lambda r_: fP_mp(*mp_at_r(r_, W_)[:3]), mp.mpf(rr[k]), mp.mpf(rr[k + 1])) for k in idx]
    okb = len(Proot) == len(W_['Proots']) and all(abs(x - mp.mpf(y)) < 1e-9 for x, y in zip(Proot, W_['Proots']))
    # (c) direct common roots on E1's real branches
    e0, e1, e2 = [np.broadcast_to(q, z.shape) for q in fE1_np(p_, A_, B_)]
    dsc = e1 ** 2 - 4 * e2 * e0
    real = dsc >= 0
    sq = np.sqrt(np.where(real, dsc, 0))
    wa, wb = (-e1 - sq) / (2 * e2), (-e1 + sq) / (2 * e2)
    wlo, whi = np.minimum(wa, wb), np.maximum(wa, wb)
    fc = [np.broadcast_to(q, z.shape) for q in fE2_np(p_, A_, B_)]
    common, other = [], []
    for ib, wbr in enumerate((wlo, whi)):
        h = fc[0] + wbr * (fc[1] + wbr * (fc[2] + wbr * fc[3]))
        ch = np.nonzero(real[:-1] & real[1:] & (np.sign(h[:-1]) * np.sign(h[1:]) < 0))[0]
        for k in ch:
            lo, hi = mp.mpf(rr[k]), mp.mpf(rr[k + 1])
            if branch_val(lo, W_, ib) is None or branch_val(hi, W_, ib) is None:
                other.append((mp.mpf(rr[k]), 'complex at an end'))
                continue
            try:
                rm = bisect(lambda r_: branch_val(r_, W_, ib)[0], lo, hi)
            except TypeError:
                other.append((lo, 'complex inside the step'))
                continue
            pm, Am, Bmv, Tm = mp_at_r(rm, W_)
            wm = branch_val(rm, W_, ib)[1]
            if E2rel(pm, Am, Bmv, wm) <= mp.mpf(10) ** -30:
                common.append((rm, wm, Tm))
            else:
                other.append((rm, f"w = {mp.nstr(wm, 6)}, |E2|/sum = {mp.nstr(E2rel(pm, Am, Bmv, wm), 3)}"))
    common.sort()
    okc = (len(common) == len(W_['Proots'])
           and all(abs(cr[0] - mp.mpf(y)) < 1e-9 for cr, y in zip(common, W_['Proots']))
           and all(abs(cr[1] - wr) < 1e-6 for cr, wr in zip(common, W_['wref']))
           and all(abs(cr[2]) > 1e-3 for cr in common))
    adm = [cr for cr in common if 0 < cr[1] < 1]
    # D5 (a) y's sign changes
    yn = B_ - A_
    iy = np.nonzero(np.sign(yn[:-1]) * np.sign(yn[1:]) < 0)[0]
    yroot = [bisect(lambda r_: (lambda q: q[2] - q[1])(mp_at_r(r_, W_)), mp.mpf(rr[k]), mp.mpf(rr[k + 1])) for k in iy]
    oka = len(yroot) == 1 and abs(yroot[0] - mp.mpf(W_['ry'])) < 1e-9
    okoth = all(yroot and abs(o[0] - yroot[0]) < 1e-6 for o in other)
    ok4 &= agree and okb and okc and len(adm) == 3 and okoth
    det4.append(f"{nm}: {len(z)} points; float64 = 50-digit signs at every 997th: {agree}; P sign changes at r = "
                f"{[mp.nstr(x, 12) for x in Proot]} (note's radii within 1e-9: {okb}); common roots (r, w, T) "
                f"{[(mp.nstr(x, 12), mp.nstr(y, 8), mp.nstr(tt, 6)) for x, y, tt in common]} (match: {okc}); admissible "
                f"{len(adm)}; other branch sign changes {[(mp.nstr(o[0], 10), o[1]) for o in other]} (all at the root "
                f"of y: {okoth})")
    # D5 (b), (c)
    r_y = yroot[0] if yroot else mp.mpf(W_['ry'])
    r_b = mp.mpf(walls['Le']['Proots'][0]) if (mut == 'common' and nm == 'Le') else r_y
    pb, Ab, Bb, _ = mp_at_r(r_b, W_)
    e0b, e1b, e2b = fE1_mp(pb, Ab, Bb)
    e2small = abs(e2b) <= mp.mpf(10) ** -30 * (abs(e0b) + abs(e1b))
    wf = -e0b / e1b
    rts = e1roots_mp(pb, Ab, Bb)
    minrel = min((E2rel(pb, Ab, Bb, q) for q in rts), default=mp.inf)
    okb5 = (mut == 'common' and nm == 'Le' or (e2small and abs(wf - W_['wy']) < 1e-5)) and minrel > 1e-6

    def sylv(r_):
        p2, A2, B2, _ = mp_at_r(r_, W_)
        Ac = list(reversed(fE1_mp(p2, A2, B2)))
        Bc = list(reversed(fE2_mp(p2, A2, B2)))
        S_ = mp.zeros(5)
        for i in range(3):
            for j, q in enumerate(Ac):
                S_[i, i + j] = q
        for i in range(2):
            for j, q in enumerate(Bc):
                S_[3 + i, i + j] = q
        return mp.det(S_)
    hs = mp.mpf(10) ** -7
    rs_ = mp.sign(sylv(r_y - hs)) * mp.sign(sylv(r_y + hs))
    ps_ = mp.sign(fP_mp(*mp_at_r(r_y - hs, W_)[:3])) * mp.sign(fP_mp(*mp_at_r(r_y + hs, W_)[:3]))
    okc5 = rs_ < 0 and ps_ > 0
    ok5 &= oka and okb5 and okc5
    det5.append(f"{nm}: y changes sign at r = {[mp.nstr(x, 12) for x in yroot]} ({oka}); at r = {mp.nstr(r_b, 12)}: "
                f"E1's w^2 coefficient / sum {mp.nstr(abs(e2b) / (abs(e0b) + abs(e1b)), 3)}, finite root "
                f"{mp.nstr(wf, 8)} (ind102 printed {W_['wy']}), min |E2|/sum over E1's real roots "
                f"{mp.nstr(minrel, 3)}: {okb5}; resultant sign product across r_y +- 1e-7 {rs_}, P's {ps_}: {okc5}")
report("D4 grid scan and direct common roots", ok4, "; ".join(det4))
report("D5 the spurious factor and ind102's extra sign change", ok5, "; ".join(det5))
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS", f"[{time.time() - T0:.0f} s]")
sys.exit(1 if fails else 0)
