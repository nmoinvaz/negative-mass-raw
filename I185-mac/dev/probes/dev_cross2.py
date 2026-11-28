exec(open("explore4.py").read().split("import sys\nfi, c")[0])
import numpy as np
from scipy.integrate import solve_ivp
# 1) desingularized flow to kappa ~ 1e-22 (as before), get end state; 2) physical ODE in eta, left
def crossing(fi, c, delta=1e-4, tau_max=9, h=mp.mpf("0.01")):
    j = json.loads(subprocess.run([BIN,"walk",str(fi),str(c)],capture_output=True,text=True).stdout)
    xs = mp.mpf(j["xstar"])
    x0 = float(xs + mp.mpf(delta))
    jj, s = walk_state(fi, c, x0)
    x = mp.mpf(jj["x"]); f,g,f2 = s
    a = coefs(f,g,x)
    st = {"w": a[0]*f2}
    y = [x,f,g]
    rhs = make_rhs(st)
    for i in range(int(tau_max/h)):
        k1,w,a = rhs(y)
        st["w"] = w
        k2,w2,_ = rhs([y[m]+h/2*k1[m] for m in range(3)]); st["w"] = w2
        k3,w3,_ = rhs([y[m]+h/2*k2[m] for m in range(3)]); st["w"] = w3
        k4,w4,_ = rhs([y[m]+h*k3[m] for m in range(3)])
        y = [y[m] + h/6*(k1[m]+2*k2[m]+2*k3[m]+k4[m]) for m in range(3)]
        st["w"] = w4
    k1,w,a = rhs(y)
    return y, w/a[0], xs
y, f2, xs = crossing(1.5, 3000)
x,f,g = y
print("end: x-xs=", mp.nstr(x-xs,8), "kappa=", mp.nstr(f**2-x**2-1,5), "F=",mp.nstr(f,12),"g=",mp.nstr(g,12),"F''=",mp.nstr(f2,10))
# physical ODE in eta going down from x (>eta*) through kappa=0
xf, ff, gf, f2f = [float(v) for v in (x,f,g,f2)]
def rhs_phys(eta, Y, st):
    F,g = Y
    a = [c(F,g,eta) for c in [sp.lambdify((F0,F1,eta_s),cc,"numpy") for cc in []]] if False else None
cof = [sp.lambdify((F0,F1,eta), cc, "numpy") for cc in P.all_coeffs()]
def rp(eta, Y, st):
    F,g = Y
    a = [c_(F,g,eta) for c_ in cof]
    r = np.roots(a)
    r = r[np.abs(r.imag) < 1e-9*(1+np.abs(r.real))].real
    x2 = r[np.argmin(np.abs(r - st["x"]))]
    st["x"] = x2
    return [g, x2]
st = {"x": f2f}
sol = solve_ivp(rp, [xf, xf-0.05], [ff,gf], args=(st,), method="DOP853", rtol=1e-13, atol=1e-16, dense_output=True, max_step=1e-4)
print(sol.status, sol.message, sol.t[-1])
ke = float(x - xs)
for d in (0, -1e-9, -1e-8, -1e-7, -1e-6, -1e-5, -1e-4, -1e-3, -1e-2, -0.04):
    eta_ = float(x) + d
    if eta_ < sol.t[-1]: break
    F_,g_ = sol.sol(eta_)
    kap = F_**2 - eta_**2 - 1
    ge = eta_/(2*F_)
    print(f"d={d:9.1e} eta={eta_:.12f} F={F_:.10f} F'={g_:.10f} kappa={kap:+.3e} y={g_-ge:+.4e}")
