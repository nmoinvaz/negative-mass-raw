#!/usr/bin/env python3
"""DG08's Lemma 1 (crc) converted to zeta'(r_s)/zeta(r_s) and compared with c* (#146).

Run: ~/Source/negative-mass-venv314/bin/python -I lemma1_conversion.py [--mutate=sign|h_typo|zm6]
Exit 0: every check PASS. Exit 1: a check FAILED.

Formulas are typed from the TeX lines named in the comments (not read from the files).
  DG08 v3 = I149-rpi5/dg08_v3/ivps03.tex (sha256 87c422ca...), v2 = dg08_v2/ivps02.tex (0747688e...).
  DG06 v2 = I149-rpi5/dg06_v2/nakedsingularity2.tex (4da32b56..., = I146-rpi5/dg06_src).
c* of #146 is typed only in the last step (C3 of the README: it is not used before the comparison).
"""
import sys
import sympy as sp

MUT = ""
for a in sys.argv[1:]:
    if a.startswith("--mutate="):
        MUT = a.split("=", 1)[1]

fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" : " + detail) if detail else ""))
    if not ok:
        fails.append(name)


r, M, lam, mu, rho = sp.symbols("r M lambda mu rho")
cm1, c0, c1, c2, ell = sp.symbols("c_m1 c_0 c_1 c_2 ell")

# ---- A1: the stated substitution ---------------------------------------------------------------
# DG08 v3 line 217 (lam): lambda = (ell-1)(ell+2)/2.  Lemma 1, line 365-370 (crc):
#   Psi_z = sum_{j>=-1} c_j (r - r_s)^j,  c_0 = lambda^2 c_{-1} / (3 M (3 + 2 lambda)),  r_s = -3M/lambda (line 359).
# DG06 v2 line 267 (AppB1): zeta = (2 lambda r - 3 mu) psi_Z;  line 114 "we define mu = -2M" (v1 line 253, v2 line 262).
# DG08's Psi_z is DG06's psi_Z (A4 below).
crc_c0 = lam**2 * cm1 / (3 * M * (3 + 2 * lam))
if MUT == "sign":
    crc_c0 = -crc_c0
r_s = -3 * M / lam
Psi = cm1 / rho + crc_c0 + c1 * rho + c2 * rho**2          # rho = r - r_s
zeta = sp.expand((2 * lam * r - 3 * mu) * Psi.subs(rho, r - r_s))
zeta = zeta.subs(mu, -2 * M)                                 # mu = -2M
# 2*lam*r - 3*mu = 2*lam*r + 6M = 2*lam*(r - r_s)
zeta = sp.simplify(zeta)
z_rs = sp.simplify(zeta.subs(r, r_s))
zp_rs = sp.simplify(sp.diff(zeta, r).subs(r, r_s))
ratio_M = sp.simplify(zp_rs / z_rs)
ratio_mu = sp.simplify(ratio_M.subs(M, -mu / 2))
print("zeta(r_s) =", sp.factor(z_rs), "  zeta'(r_s) =", sp.factor(zp_rs))
print("zeta'/zeta (r_s), in M :", sp.factor(ratio_M))
print("zeta'/zeta (r_s), in mu:", sp.factor(ratio_mu))
check("A1.0 zeta(r_s) = 2 lambda c_-1 and zeta'(r_s) = 2 lambda c_0",
      sp.simplify(z_rs - 2 * lam * cm1) == 0 and sp.simplify(zp_rs - 2 * lam * crc_c0) == 0)

# ---- A2: DG08 (zm6) in ell --------------------------------------------------------------------
# DG08 v3 line 848-849 (zm6): psi = a0 (r-r_s)^-1 + a0 (l+2)^2 (l-1)^2 / (12 M (l^2+l+1)) + ...
zm6_den = ell**2 + ell + (2 if MUT == "zm6" else 1)
zm6 = (ell + 2) ** 2 * (ell - 1) ** 2 / (12 * M * zm6_den)
lam_ell = (ell - 1) * (ell + 2) / 2
check("A2 (zm6) coefficient = lambda^2/(3M(3+2 lambda)) at lambda=(l-1)(l+2)/2",
      sp.simplify(zm6 - (lam**2 / (3 * M * (3 + 2 * lam))).subs(lam, lam_ell)) == 0)

# ---- A4: same Psi_z in DG06 and DG08 ----------------------------------------------------------
# DG06 v2 (RW2) lines 168-172, (RW2a) 177-181, (RW3a) 209-212;  DG08 v3 (RW2) 254-262, (RW2a) 263-267, (zeri) 269-273.
# Both print: K = q Psi + (1-2M/r) Psi_r;  H1 = h Psi_t + r Psi_tr;  H2 = d/dr[(1-2M/r)(h Psi + r Psi_r)] - K.
q = (lam * (lam + 1) * r**2 + 3 * lam * M * r + 6 * M**2) / (r**2 * (lam * r + 3 * M))
h_num = lam * r**2 - 3 * lam * r * M - (3 if MUT != "h_typo" else -3) * M**2
h = h_num / ((r - 2 * M) * (lam * r + 3 * M))
h_dg06 = (lam * r**2 - 3 * lam * r * M - 3 * M**2) / ((r - 2 * M) * (lam * r + 3 * M))
q_dg06 = (lam * (lam + 1) * r**2 + 3 * lam * M * r + 6 * M**2) / (r**2 * (lam * r + 3 * M))
check("A4 q, h of DG08 (RW2a) equal f, h of DG06 (RW2a)",
      sp.simplify(q - q_dg06) == 0 and sp.simplify(h - h_dg06) == 0)

# ---- A3: first principles from (RW2), (RW2a): smoothness of K and H1 for a Laurent Psi_z -------
# Psi = c_-1/rho + c_0 + c_1 rho + c_2 rho^2 (c_0 free); K and H1/s must have no pole at rho = 0.
c0f = sp.Symbol("c0f")
Psi_f = cm1 / rho + c0f + c1 * rho + c2 * rho**2
Psi_r = Psi_f.subs(rho, r - r_s)
Kexpr = q * Psi_r + (1 - 2 * M / r) * sp.diff(Psi_r, r)
H1expr = h * Psi_r + r * sp.diff(Psi_r, r)          # H1 = s * this for e^{st}


def pole_coeffs(expr):
    e = sp.together(expr.subs(r, r_s + rho))
    ser = sp.series(e, rho, 0, 1).removeO()
    return [sp.simplify(ser.coeff(rho, -k)) for k in (2, 1)]


Kp = pole_coeffs(Kexpr)
Hp = pole_coeffs(H1expr)
print("K  pole coefficients (rho^-2, rho^-1):", [sp.factor(x) for x in Kp])
print("H1 pole coefficients (rho^-2, rho^-1):", [sp.factor(x) for x in Hp])
sol_K = sp.solve(Kp[1], c0f)
sol_H = sp.solve(Hp[1], c0f)
check("A3.0 double poles vanish identically for a simple-pole Psi_z", Kp[0] == 0 and Hp[0] == 0)
okK = len(sol_K) == 1 and sp.simplify(sol_K[0] - crc_c0) == 0
okH = len(sol_H) == 1 and sp.simplify(sol_H[0] - crc_c0) == 0
check("A3.K  K pole-free  <=>  c_0 = DG08 (crc)", okK,
      "c_0 = " + (str(sp.factor(sol_K[0])) if sol_K else "none"))
check("A3.H1 H1 pole-free <=>  c_0 = DG08 (crc)", okH,
      "c_0 = " + (str(sp.factor(sol_H[0])) if sol_H else "none"))

# ---- C3: comparison with c* and with DG06's printed (cz), only now -----------------------------
# c* of #146 (zerilli_gauge_rs.md section 1): c* = -2 lam^2/(3 mu (2 lam+3)) = lam^2/(3 M (2 lam+3)).
cstar_mu = -2 * lam**2 / (3 * mu * (2 * lam + 3))
cstar_M = lam**2 / (3 * M * (2 * lam + 3))
# DG06 v2 line 317-319 (cz): zeta' = + 2 lam^2/(3 mu (2 lam+3)) zeta  at r = 3 mu/(2 lam)
cz_printed = 2 * lam**2 / (3 * mu * (2 * lam + 3))
print("c* (#146), mu form :", cstar_mu, "   M form:", cstar_M)
print("DG06 v2 (cz) printed:", cz_printed)
check("C1 DG08 Lemma 1 converted = c* (mu form)", sp.simplify(ratio_mu - cstar_mu) == 0)
check("C1' DG08 Lemma 1 converted = c* (M form)", sp.simplify(ratio_M - cstar_M) == 0)
check("C1'' DG06 v2 printed (cz) = - (DG08 Lemma 1 converted)", sp.simplify(cz_printed + ratio_mu) == 0)
check("C1''' r_s: -3M/lambda = 3 mu/(2 lambda) at mu = -2M", sp.simplify(r_s.subs(M, -mu / 2) - 3 * mu / (2 * lam)) == 0)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all PASS")
