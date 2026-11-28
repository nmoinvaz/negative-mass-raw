#!/usr/bin/env python3
"""ind263: the coordinator's check of #263. (1) The closed form of Omega5 evaluated at 60 digits against the note's 100-digit value.
(2) The ln 2 structure: with eps = 1/s, s(1 + sum Omega_k eps^(k+1)) = s exp(-4 ln2 eps) F(eps), F free of ln 2 through eps^6,
from the closed forms of Omega0 ... Omega5 (README.md, omega3.md, omega4.md, omega5.md), typed here from the notes.
    python3 ind263.py [--mutate=om5|om3]
"""
import sys
import mpmath as mp
import sympy as sp
MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
L, p, z3, z5 = sp.symbols("L pi z3 z5")       # L = ln 2
Om = {
    0: -4 * L,
    1: 2 * p ** 2 / 3 + 8 * L ** 2,            # Omega1 (W^2 a^2 = s + Omega0 + Omega1/s + ...); A1: run 1 typed Omega1/2
    2: 80 * z3 - sp.Rational(8, 3) * p ** 2 * L - sp.Rational(32, 3) * L ** 3,
    3: sp.Rational(22, 45) * p ** 4 + sp.Rational(16, 3) * p ** 2 * L ** 2 + sp.Rational(32, 3) * L ** 4 - 320 * z3 * L - 384 * z3,
    4: (-10432 * z5 - 160 * p ** 2 * z3 + 640 * z3 * L ** 2 - sp.Rational(64, 9) * p ** 2 * L ** 3 - sp.Rational(88, 45) * p ** 4 * L
        - sp.Rational(128, 15) * L ** 5 - sp.Rational(2432, 45) * p ** 4 + 1536 * z3 * L + 3072 * z3),
    5: (sp.Rational(256, 45) * L ** 6 + sp.Rational(64, 9) * p ** 2 * L ** 4 - sp.Rational(2560, 3) * z3 * L ** 3 + sp.Rational(176, 45) * p ** 4 * L ** 2
        - 3072 * z3 * L ** 2 + 640 * p ** 2 * z3 * L + sp.Rational(9728, 45) * p ** 4 * L - 12288 * z3 * L + 41728 * z5 * L
        - sp.Rational(38812, 315) * p ** 6 + 3200 * z3 ** 2 - sp.Rational(256, 3) * p ** 2 * z3 + 74240 * z5 + sp.Rational(39424, 45) * p ** 4 - 36864 * z3),
}
if MUT == "om5":
    Om[5] = Om[5] + 2 * z3 * L ** 3          # one coefficient changed
if MUT == "om3":
    Om[3] = Om[3] + z3 * L                   # Omega3's ln 2 term off by one
mp.mp.dps = 120
val = {L: mp.log(2), p: mp.pi, z3: mp.zeta(3), z5: mp.zeta(5)}
om5 = mp.mpf(sp.N(Om[5].subs({L: sp.log(2), p: sp.pi, z3: sp.zeta(3), z5: sp.zeta(5)}), 110))
note = mp.mpf("40860.455354525687312544064826033704278039372215373284079454102667838994220332959565447528072780104912968505385")
d = abs(om5 - note)
ok1 = d < mp.mpf("1e-95")
print(f"[{'PASS' if ok1 else 'FAIL'}] K1: closed form of Omega5 against the note's value: |difference| {mp.nstr(d, 3)} (bar 1e-95)")
e = sp.symbols("e")
series = 1 + sum(Om[k] * e ** (k + 1) for k in range(6))
F = sp.series(series * sp.exp(4 * L * e), e, 0, 7).removeO()
coeffs = [sp.expand(F.coeff(e, k)) for k in range(7)]
dl = [sp.simplify(sp.diff(c, L)) for c in coeffs]
ok2 = all(x == 0 for x in dl)
print(f"[{'PASS' if ok2 else 'FAIL'}] K2: d/d(ln 2) of F's coefficients f0 ... f6: {dl}")
print("  F =", " + ".join(f"({sp.factor(c)}) e^{k}" for k, c in enumerate(coeffs) if c != 0))
sys.exit(0 if ok1 and ok2 else 1)
