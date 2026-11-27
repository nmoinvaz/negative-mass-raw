import sys, time, pickle
src = open('red7_run.py').read().split("view(\"start\")")[0]
exec(src)
I, Fs = pickle.load(open('red7_state2.pkl', 'rb'))
I = sp.expand(I)

def solve_ft(g):
    g = sp.expand(g)
    f, d = 0, g
    while d != 0:
        f += d
        d = sp.diff(d, lt)
    return sp.expand(f)

def full_coeff(I, *gens_pows):
    pass

# 8. K3 C
cK3 = sp.expand(I).coeff(K3, 1)
cK3C = sp.expand(cK3).coeff(C, 1)
print("C K3 coefficient:", cK3C, "; K3 otherwise:", sp.expand(cK3 - cK3C*C))
apply("K3C", sp.Rational(1, 2) * cK3C * D3 * K3)
assert not I.has(K3), "K3 left"
# 9. C coefficient
def part_C(I):
    return coeff(I, 1, 0, 0)
cC = part_C(I)
cu = sp.collect(cC, u, evaluate=False)
print("C parts", list(cu))
# u lt^b C: F = -lt^{b+1}/(b+1) C
cu1 = sp.expand(cu.get(u, 0))
pc = sp.Poly(cu1, lt)
for b in range(pc.degree() + 1):
    cb = pc.coeff_monomial(lt**b)
    if cb != 0:
        apply(f"C_u_lt{b}", -cb * lt**(b + 1) / (b + 1) * C)
# u^2 theta lt^b C: iterate from top b
cC = part_C(I)
cu = sp.collect(cC, u, evaluate=False)
c2 = sp.expand(cu.get(u**2, 0))
print("u^2 part of C coefficient:", c2)
pc = sp.Poly(c2, lt, th)
for b in range(pc.degree(lt), -1, -1):
    cb = sp.expand(sp.Poly(sp.expand(sp.collect(part_C(I), u, evaluate=False).get(u**2, 0)), lt).coeff_monomial(lt**b))
    if cb != 0:
        # cb = c * theta
        assert sp.Poly(cb, th).degree() <= 1, cb
        c_ = sp.Poly(cb, th).coeff_monomial(th)
        assert sp.expand(cb - c_ * th) == 0, cb
        apply(f"C_u2th_lt{b}", c_ * u * th * lt**b * C)
cu = sp.collect(part_C(I), u, evaluate=False)
print("C parts after", list(cu))
# the u^2 theta C^... in the last step: c * u^2 theta C (b = 0)
cu = sp.collect(part_C(I), u, evaluate=False)
view("C steps")
pickle.dump((I, Fs), open('red7_state3.pkl', 'wb'))
