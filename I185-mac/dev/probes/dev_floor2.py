exec(open("dev_floor.py").read().split("pts = [")[0])
import numpy as np
def run2(fi, c, tend=-6000.0, tag=""):
    j = json.loads(subprocess.run([BIN,"walk",str(fi),str(c)],capture_output=True,text=True).stdout)
    f = j["floor"][-1]
    F,F1,F2v = [v[0] for v in f]; x = j["x_last"]
    P = x*F1; Q = x*x*F2v + P
    st = {"Q": Q}; t0 = np.log(x)
    ts = np.concatenate([np.linspace(t0, t0-100, 11), np.linspace(t0-100, t0-400, 7)[1:]])
    sol = solve_ivp(rhs, [t0, t0-400], [F,P], args=(st,), method="DOP853", rtol=1e-13, atol=1e-40, t_eval=ts, max_step=0.5)
    print(tag, "status", sol.status, sol.message[:50])
    for t,(FF,PP) in zip(sol.t, sol.y.T):
        e = np.exp(t)
        A = FF*(PP - st["Q"]) - PP*PP
        print(f"  t={t:9.3f} F={FF:.6g} P={PP:.6g}")
run2(0.25,3000,tag="(0.25,3000)")
run2(0.5,100,tag="(0.5,100)")
