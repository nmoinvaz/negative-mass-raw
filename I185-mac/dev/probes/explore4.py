import sys, json, subprocess
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i185/notes/warp")
sys.argv=[sys.argv[0]]
import sympy as sp, mpmath as mp
import det_classify as dc
F0,F1,F2,eta = dc.F0_,dc.F1_,dc.F2_,dc.ETA
N = sp.expand(dc.conical_N())
P = sp.Poly(N, F2)
co = [sp.lambdify((F0,F1,eta), c, "mpmath") for c in P.all_coeffs()]
mp.mp.dps = 50
BIN="/Users/nathan/Source/negative-mass-i185/notes/warp/conical_global/target/release/conical_global"
def walk_state(fi, c, x):
    out = subprocess.run([BIN,"walk",str(fi),str(c),repr(x),"30","1e-32","0.5"],capture_output=True,text=True).stdout
    j = json.loads(out.strip().splitlines()[-1])
    s = [mp.mpf(v[0])+mp.mpf(v[1]) for v in j["state"]]
    return j, s
def coefs(f,g,x): return [c(f,g,x) for c in co]
def wroot(a, w0):
    a3,a2,a1,a0 = a
    G  = lambda w: w**3 + a2*w**2 + a1*a3*w + a0*a3**2
    dG = lambda w: 3*w**2 + 2*a2*w + a1*a3
    w = w0
    for _ in range(60):
        d = dG(w)
        step = G(w)/d
        w -= step
        if abs(step) <= mp.mpf(10)**(-45)*(abs(w)+mp.mpf(10)**(-60)): break
    return w
def make_rhs(st):
    def rhs(y):
        x,f,g = y
        a = coefs(f,g,x)
        w = wroot(a, st["w"])
        return [a[0], g*a[0], w], w, a
    return rhs
def flow(fi, c, delta, tau_max, h):
    j = json.loads(subprocess.run([BIN,"walk",str(fi),str(c)],capture_output=True,text=True).stdout)
    xs = mp.mpf(j["xstar"])
    x0 = float(xs + mp.mpf(delta))
    jj, s = walk_state(fi, c, x0)
    print("walk end flag", jj["end"], "x", jj["x"], "steps", jj["steps"])
    x = mp.mpf(jj["x"]); f,g,f2 = s
    a = coefs(f,g,x)
    st = {"w": a[0]*f2}
    y = [x,f,g]
    rhs = make_rhs(st)
    tau = mp.mpf(0)
    out=[]
    n = int(tau_max/h)
    for i in range(n+1):
        k1,w,a = rhs(y)
        if i % int(1/h) == 0 or i==n:
            x_,f_,g_ = y
            kap = f_**2 - x_**2 - 1
            ge = x_/(2*f_)
            yy = g_ - ge
            beta = 2*f_*x_**3
            Y = yy/mp.sqrt(abs(kap)) if kap!=0 else mp.inf
            out.append((float(tau), x_, f_, g_, kap, yy, Y, w/a[0] if a[0]!=0 else mp.inf))
            print(f"tau={float(tau):7.3f} Delta={mp.nstr(x_-xs,6):>12} kappa={mp.nstr(kap,5):>12} y={mp.nstr(yy,6):>12} Y={mp.nstr(Y,5):>10} F''={mp.nstr(w/a[0],8):>14} a2={mp.nstr(a[1],5)}")
        st["w"] = w
        k2,w2,_ = rhs([y[m]+h/2*k1[m] for m in range(3)])
        st["w"] = w2
        k3,w3,_ = rhs([y[m]+h/2*k2[m] for m in range(3)])
        st["w"] = w3
        k4,w4,_ = rhs([y[m]+h*k3[m] for m in range(3)])
        y = [y[m] + h/6*(k1[m]+2*k2[m]+2*k3[m]+k4[m]) for m in range(3)]
        st["w"] = w4
        tau += h
    return out, xs
import sys
fi, c = float(sys.argv[1]) if len(sys.argv)>1 else 1.5, float(sys.argv[2]) if len(sys.argv)>2 else 3000
