import sys, time, pickle
exec(open('red7_run.py').read().split("view(\"start\")")[0])
I, Fs = pickle.load(open('red7_state.pkl', 'rb'))

def solve_ft(g):
    """f with f - f' = g (polynomial in lt)"""
    g = sp.expand(g)
    pg = sp.Poly(g, lt) if g != 0 else None
    f, d = 0, g
    while d != 0:
        f += d
        d = sp.diff(d, lt)
    return sp.expand(f)

# 4. CD: u g(lt) C D3 -> F = -G C D3
cCD = coeff(I, 1, 1, 0)
g = sp.expand(cCD / u)
assert not g.has(u)
G = sp.integrate(g, lt)
apply("CD", -G * C * D3)
# 5. CL: u^2 g C K2 -> F = u gt C K2 with gt - gt' = g
cCL = coeff(I, 1, 0, 1)
cu = sp.collect(cCL, u, evaluate=False)
print("CL parts", list(cu))
g = sp.expand(cu.get(u**2, 0))
gt = solve_ft(g)
apply("CL", u * gt * C * K2)
# 6. CC
cCC = coeff(I, 2, 0, 0)
cu = sp.collect(cCC, u, evaluate=False)
print("CC parts", list(cu))
p = sp.expand(cu.get(u**2, 0))
f = solve_ft(p)
apply("CC", u * f * C**2)
view("CD, CL, CC")
# 7. D: the u theta D3 part and the rest
cD = coeff(I, 0, 1, 0)
cu = sp.collect(cD, u, evaluate=False)
print("D parts", list(cu))
au = sp.expand(cu.get(u, 0))                  # u * theta * (const)
print("u part:", au)
apply("D_u", -lt * au * D3)
cD = coeff(I, 0, 1, 0)
cu = sp.collect(cD, u, evaluate=False)
print("D parts after", list(cu))
A = primitive_c(cD)
print("D primitive", A, "check", check_primitive(A, cD))
apply("D", A * D3)
view("D")
pickle.dump((I, Fs), open('red7_state2.pkl', 'wb'))
