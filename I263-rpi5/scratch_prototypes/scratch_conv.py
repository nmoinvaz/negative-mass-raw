import sys, time, pickle
sys.path.insert(0, '/home/nathan/Source/negative-mass-i263/notes/wormhole_largeD')
sys.argv = sys.argv[:1]
import sympy as sp
import order7 as o7
t0 = time.time()
parts, tot = o7.r7_parts()
lg, u, th, C, D3, Lc2, q, J2 = o7.X_LG, o7.X_U, o7.X_TH, o7.X_C, o7.X_D3, o7.X_LC, o7.X_Q, o7.X_J2
v = sp.symbols("v0:6")
lt, K2 = sp.symbols("lt K2")
pi, z3, z5 = sp.pi, sp.zeta(3), sp.zeta(5)
om = {v[1]: 2*pi**2/3 + 8*q**2, v[2]: 80*z3 - sp.Rational(8,3)*pi**2*q - sp.Rational(32,3)*q**3,
      v[3]: 22*pi**4/45 + sp.Rational(16,3)*pi**2*q**2 + sp.Rational(32,3)*q**4 - 320*z3*q - 384*z3,
      v[4]: -10432*z5 - 160*pi**2*z3 + 640*q**2*z3 - sp.Rational(64,9)*pi**2*q**3 - sp.Rational(88,45)*pi**4*q - sp.Rational(128,15)*q**5 - sp.Rational(2432,45)*pi**4 + 1536*q*z3 + 3072*z3}
expr = tot.subs(om).subs(J2, pi**3/24 + q**2*pi/2)
expr = expr.subs(Lc2, K2 - q*C + q**2*th).subs(lg, lt - q)
expr = sp.expand(expr)
print("expanded", time.time()-t0, len(expr.args))
Pl = sp.Poly(expr, C, D3, K2)
parts_t = {m: sp.expand(cf) for m, cf in Pl.terms()}
print(sorted(parts_t))
pickle.dump(parts_t, open('parts7_t.pkl', 'wb'))
for m in sorted(parts_t, key=lambda m: (-sum(m), m)):
    cf = parts_t[m]
    by_u = sp.collect(cf, u, evaluate=False)
    out = []
    for k, vv in sorted(by_u.items(), key=lambda kv: str(kv[0])):
        vv = sp.expand(vv)
        dl = sp.Poly(vv, lt).degree() if vv.has(lt) else 0
        dt = sp.Poly(vv, th).degree() if vv.has(th) else 0
        out.append(f"{k}: lt^{dl} th^{dt}")
    print(m, "; ".join(out))
print(time.time()-t0)
