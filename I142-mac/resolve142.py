#!/usr/bin/env python3
"""Re-solve of one case of #142: the x-series of Vhat at l = 2 by exact series reversion (sympy), DG09 eq. (61)."""
import sympy as sp

r, y = sp.symbols('r y', positive=True)
a = sp.symbols('a2:6')
chi = sp.Rational(3, 2) * r - sp.Rational(3, 4) * r**3 + sp.Rational(1, 4) * r**4   # Lemma A, l = 2 (RESULTS 1(iii))
c, lam = 4, 2
f = 1 + 2 / r
psi = chi / (c * r - 6)
g = f * sp.diff(psi, r) / psi
vh_def = sp.cancel(g**2 - f * sp.diff(g, r))                    # definition
V = 2 * f * (lam**2 * r**2 * ((lam + 1) * r - 3) + 9 * (lam * r - 1)) / (r**3 * (lam * r - 3)**2)
vh_z = sp.cancel(2 * g**2 - V)                                   # Theorem 3 (Z) route
print('Vhat by definition == 2g^2 - V:', sp.cancel(vh_def - vh_z) == 0)
rs = 2 * y + sum(a[i] * y**(i + 2) for i in range(4))
xs = sp.expand(sp.series(r - 2 * sp.log(1 + r / 2), r, 0, 8).removeO().subs(r, rs))
sol = {}
for p in range(3, 7):
    eq = xs.coeff(y, p).subs(sol)
    ai = a[p - 3]
    sol[ai] = sp.solve(eq, ai)[0]
print('r(y), y = sqrt(x):', sp.expand(rs.subs(sol)))
ser = sp.series(sp.cancel(y**4 * vh_def.subs(r, rs.subs(sol))), y, 0, 3).removeO()
co = [sp.nsimplify(ser.coeff(y, i)) for i in range(3)]
print('coefficients of x^-2, x^-3/2, x^-1:', co)
print('DG09 (61) prints: 3/4, (l^2+l-1)/4 =', sp.Rational(5, 4), ', -l(l+1)/4 =', sp.Rational(-6, 4))
ok = co == [sp.Rational(3, 4), sp.Rational(5, 4), 0]
print('re-solve agrees with #142 (x^-1 coefficient 0):', ok)
raise SystemExit(0 if ok else 1)
