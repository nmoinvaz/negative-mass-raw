import sys, time, pickle
import sympy as sp
from lin import *
T0 = time.time()
H0, H1, H2, K = [sp.Function(n)(rho) for n in ("H0", "H1", "H2", "K")]
h = sp.zeros(4, 4)
h[0, 0] = A * H0 * Yf * ex; h[0, 1] = h[1, 0] = H1 * Yf * ex; h[1, 1] = H2 * Yf * ex / A
h[2, 2] = R2 * K * Yf * ex; h[3, 3] = R2 * sp.sin(th)**2 * K * Yf * ex
dE, dS, E0, S0 = linearize(h, 0)
def clean(z):
    z = sp.expand(sp.simplify(z / ex))
    z = Asub(angsub(Asub(z)))
    return z
P = {}
for (a, b) in [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2), (2, 2), (3, 3)]:
    P[(a, b)] = clean(dE[a, b])
P['S'] = clean(dS)
ct = sp.cos(th) / sp.sin(th)
E = {}
E['tt'] = sp.simplify(P[(0, 0)].coeff(Ys)); E['tr'] = sp.simplify(P[(0, 1)].coeff(Ys)); E['rr'] = sp.simplify(P[(1, 1)].coeff(Ys))
E['tth'] = sp.simplify(P[(0, 2)].coeff(Yps)); E['rth'] = sp.simplify(P[(1, 2)].coeff(Yps))
E['S'] = sp.simplify(P['S'].coeff(Ys))
Rthth = P[(2, 2)]; Rphph = sp.expand(sp.simplify(P[(3, 3)] / sp.sin(th)**2))
E['ang_tr'] = sp.simplify(sp.expand(Rthth + Rphph).coeff(Ys))
tl = sp.simplify(sp.expand(Rthth - Rphph).coeff(Yps))
print("traceless coefficient (L generic):", sp.factor(sp.simplify(tl / ct)))
for k, v in E.items():
    print(k, ":", sp.factor(v.subs(L, 2)))
pickle.dump(E, open("l1_eqs.pkl", "wb"))
