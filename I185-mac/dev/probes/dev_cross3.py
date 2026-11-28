exec(open("dev_cross2.py").read().split("# physical ODE in eta going down")[0])
import time
mp.mp.dps = 50
def xroot(a, x0):
    a3,a2,a1,a0 = a
    G  = lambda x: ((a3*x + a2)*x + a1)*x + a0
    dG = lambda x: (3*a3*x + 2*a2)*x + a1
    x = x0
    for _ in range(80):
        d = dG(x)
        step = G(x)/d
        x -= step
        if abs(step) <= mp.mpf(10)**(-40)*abs(x): break
    return x
def rhs_p(eta_, Y, st):
    F_, g_ = Y
    a = coefs(F_, g_, eta_)
    x = xroot(a, st["x"])
    st["x"] = x
    return [g_, x]
x_, f_, g_ = y
st = {"x": f2}
Y = [f_, g_]
eta_ = x_
t0 = time.time()
dist = mp.mpf(0)
nxt = [mp.mpf(10)**(-k) for k in (10,9,8,7,6,5,4,3)]
h0 = mp.mpf("1e-12")
n=0
print("start eta-xs", mp.nstr(eta_-xs,8), "kappa", mp.nstr(f_**2-eta_**2-1,5), "F''", mp.nstr(f2,8))
while dist < mp.mpf("1e-3"):
    h = -max(h0, mp.mpf("0.01")*dist)
    k1,_ = rhs_p(eta_, Y, st), None
    s0 = st["x"]
    k2 = rhs_p(eta_+h/2, [Y[0]+h/2*k1[0], Y[1]+h/2*k1[1]], st)
    k3 = rhs_p(eta_+h/2, [Y[0]+h/2*k2[0], Y[1]+h/2*k2[1]], st)
    k4 = rhs_p(eta_+h, [Y[0]+h*k3[0], Y[1]+h*k3[1]], st)
    Y = [Y[0]+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]), Y[1]+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])]
    eta_ += h; dist = x_ - eta_; n+=1
    st["x"] = rhs_p(eta_, Y, st)[1]
    if nxt and dist >= nxt[0]:
        kap = Y[0]**2 - eta_**2 - 1; ge = eta_/(2*Y[0]); yy = Y[1]-ge
        print(f"dist={mp.nstr(dist,3)} eta-xs={mp.nstr(eta_-xs,8):>14} kappa={mp.nstr(kap,4):>10} F'={mp.nstr(Y[1],12)} y={mp.nstr(yy,6)} F''={mp.nstr(st['x'],8)}  ({n} steps, {time.time()-t0:.1f}s)")
        nxt.pop(0)
