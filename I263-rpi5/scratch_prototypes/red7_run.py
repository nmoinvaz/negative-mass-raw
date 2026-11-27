import sys, time, pickle
from red7_lib import *

I = pickle.load(open('I7.pkl', 'rb'))
Fs = []          # (name, F)
t0 = time.time()


def P_b(b):
    return [th, C / 2, K2, K3][b]


def primitive_c(c):
    """primitive in th of c = alpha(lt) + beta(lt) u^-2 + gamma(lt) (u-free otherwise): lt^b -> P_b, lt^b (1 + ui^2) -> -lt^b ui - b P_{b-1}"""
    c = sp.expand(c)
    cu = sp.collect(c, u, evaluate=False)
    assert set(cu) <= {sp.Integer(1), u**-2}, list(cu)
    alpha, beta = sp.expand(cu.get(sp.Integer(1), 0)), sp.expand(cu.get(u**-2, 0))
    c0, c1 = sp.expand(alpha - beta), beta               # c = c0 + c1 (1 + ui^2)
    A = 0
    for b in range(sp.Poly(c0, lt).degree() + 1 if c0 != 0 else 0):
        pass
    if c0 != 0:
        pc0 = sp.Poly(c0, lt)
        A += sum(pc0.coeff_monomial(lt**b) * P_b(b) for b in range(pc0.degree() + 1))
    if c1 != 0:
        pc1 = sp.Poly(c1, lt)
        A += sum(pc1.coeff_monomial(lt**b) * (-lt**b * ui - (b * P_b(b - 1) if b else 0)) for b in range(pc1.degree() + 1))
    return sp.expand(A)


def check_primitive(A, c):
    r = sp.expand(dth(A).subs(ui, 1 / u) - c)
    return sp.simplify(r)


def coeff(I, a, b, c):
    P = sp.Poly(sp.expand(I), C, D3, K2)
    return sp.expand(P.coeff_monomial(C**a * D3**b * K2**c))


def apply(name, F):
    global I
    dF = sp.expand(dth(F).subs(ui, 1 / u) if F.has(ui) else dth(F))
    I = sp.expand(I - dF)
    Fs.append((name, F))


def view(tag):
    P = sp.Poly(sp.expand(I), C, D3, K2)
    print(f"--- after {tag} ({time.time()-t0:.0f} s)")
    for m, cf in sorted(P.terms(), key=lambda mc: (-sum(mc[0]), mc[0])):
        cu = sp.collect(sp.expand(cf), u, evaluate=False)
        out = []
        for k, vv in sorted(cu.items(), key=lambda kv: str(kv[0])):
            vv = sp.expand(vv)
            dl = sp.Poly(vv, lt).degree() if vv.has(lt) else 0
            dt = sp.Poly(vv, th).degree() if vv.has(th) else 0
            out.append(f"{k}: lt^{dl} th^{dt}")
        print(m, "; ".join(out))


view("start")
# 1. LL
cLL = coeff(I, 0, 0, 2)
a1 = sp.expand(cLL / u**2)
assert not a1.has(u), a1
apply("LL", a1 * u * K2**2)
# 2. DL
cDL = coeff(I, 0, 1, 1)
a2 = sp.expand(cDL / u)
assert not a2.has(u), a2
apply("DL", -a2 * lt * D3 * K2)
view("LL, DL")
# 3. DD
cDD = coeff(I, 0, 2, 0)
A = primitive_c(cDD)
print("DD primitive", A, "check", check_primitive(A, cDD))
apply("DD", A * D3**2)
view("DD")
pickle.dump((I, Fs), open('red7_state.pkl', 'wb'))
