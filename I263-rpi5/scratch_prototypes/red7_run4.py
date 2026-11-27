import sys, time, pickle
src = open('red7_run.py').read().split("view(\"start\")")[0]
exec(src)
I, Fs = pickle.load(open('red7_state3.pkl', 'rb'))
I = sp.expand(I)

def part_C(I):
    return coeff(I, 1, 0, 0)

def eliminate_uC(I):
    cu = sp.collect(part_C(I), u, evaluate=False)
    c1 = sp.expand(cu.get(u, 0))
    if c1 != 0:
        pc = sp.Poly(c1, lt)
        for b in range(pc.degree() + 1):
            cb = pc.coeff_monomial(lt**b)
            if cb != 0:
                apply(f"C_u_lt{b}", -cb * lt**(b + 1) / (b + 1) * C)
eliminate_uC(I)
# 10. K2 coefficient
def part_K(I):
    return coeff(I, 0, 0, 1)
cu = sp.collect(part_K(I), u, evaluate=False)
print("K2 parts", list(cu))
c1 = sp.expand(cu.get(u, 0))
pc = sp.Poly(c1, lt)
for b in range(pc.degree() + 1):
    cb = pc.coeff_monomial(lt**b)
    if cb != 0:
        apply(f"K_u_lt{b}", -cb * lt**(b + 1) / (b + 1) * K2)
cu = sp.collect(part_K(I), u, evaluate=False)
c2 = sp.expand(cu.get(u**2, 0))
print("u^2 part of K2 coefficient:", c2)
assert not c2.has(lt) or True
# c2 = c * theta : F = c u theta K2
cth = sp.Poly(c2, th).coeff_monomial(th)
assert sp.expand(c2 - cth * th) == 0
apply("K_u2th", cth * u * th * K2)
# new u K2 and u theta lt^2 terms
cu = sp.collect(part_K(I), u, evaluate=False)
print("K2 parts after", list(cu))
c1 = sp.expand(cu.get(u, 0))
pc = sp.Poly(c1, lt)
for b in range(pc.degree() + 1):
    cb = pc.coeff_monomial(lt**b)
    if cb != 0:
        apply(f"K_u_lt{b}", -cb * lt**(b + 1) / (b + 1) * K2)
view("K2 steps")
# 11. pure terms
def pure(I):
    return sp.expand(coeff(I, 0, 0, 0))
cp = pure(I)
cu = sp.collect(cp, u, evaluate=False)
print("pure parts", {str(k): (sp.Poly(sp.expand(v), lt).degree() if sp.expand(v).has(lt) else 0) for k, v in cu.items()})
# u^2 theta^2: F = u theta^2
c2 = sp.expand(cu.get(u**2, 0))
print("u^2 part", c2)
if c2 != 0:
    assert sp.expand(c2 - sp.Poly(c2, th).coeff_monomial(th**2) * th**2) == 0
    apply("P_u2", sp.Poly(c2, th).coeff_monomial(th**2) * u * th**2)
# u^-2: write as (1 + ui^2) - 1: F = -lt^b ui
cp = pure(I)
cu = sp.collect(cp, u, evaluate=False)
cm2 = sp.expand(cu.get(u**-2, 0))
print("u^-2 part degree", sp.Poly(cm2, lt).degree())
pcm = sp.Poly(cm2, lt)
for b in range(pcm.degree() + 1):
    cb = pcm.coeff_monomial(lt**b)
    if cb != 0:
        # cb * lt^b * ui^2 = cb lt^b (1 + ui^2) - cb lt^b ; d(-lt^b ui) = lt^b (1 + ui^2) + b lt^(b-1)
        # The expression has u**-2 which dth treats via u: use ui form: convert I's u^-2 to ui^2 first
        pass
# convert u**-2 to ui**2 in I and eliminate lt^b (1+ui^2): subtract cb*d(-lt^b*ui)
I = sp.expand(I.replace(lambda e: e.is_Pow and e.base == u and e.exp < 0, lambda e: ui ** (-e.exp)))
for b in range(pcm.degree(), -1, -1):
    cbl = sp.expand(sp.Poly(sp.expand(sp.collect(sp.expand(pure(I)), ui, evaluate=False).get(ui**2, 0)), lt).coeff_monomial(lt**b)) if sp.expand(pure(I)).has(ui) else 0
    if cbl != 0:
        F = -cbl * lt**b * ui
        dF = sp.expand(dth(F))
        # dth(F) = cbl*(lt^b*u*ui?)... ui' = -(1+ui^2); lt' = -u: d(-lt^b ui) = b lt^(b-1) u ui + lt^b (1 + ui^2); u*ui must be simplified to 1
        dF = sp.expand(dF.subs(u * ui, 1)) if False else sp.expand(dF.replace(lambda e: e.is_Mul and e.has(u) and e.has(ui), lambda e: sp.simplify(e.subs(ui, 1/u))))
        I = sp.expand(I - dF)
        Fs.append((f"P_ui_lt{b}", F))
view("pure u^-2")
pickle.dump((I, Fs), open('red7_state4.pkl', 'wb'))
cp = pure(I)
print(sp.collect(cp, u, evaluate=False).keys())
