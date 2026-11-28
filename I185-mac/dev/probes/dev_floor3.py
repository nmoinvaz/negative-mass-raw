exec(open("dev_floor.py").read().split("pts = [")[0])
import numpy as np
fi,c = 0.25,3000
j = json.loads(subprocess.run([BIN,"walk",str(fi),str(c)],capture_output=True,text=True).stdout)
f = j["floor"][-1]
F,F1,F2v = [v[0] for v in f]; x = j["x_last"]
P = x*F1; Q = x*x*F2v + P
st = {"Q": Q}; t0 = np.log(x)
sol = solve_ivp(rhs, [t0, t0-300], [F,P], args=(st,), method="DOP853", rtol=1e-13, atol=1e-40, dense_output=True, max_step=0.05)
print(sol.status, sol.t[-1], len(sol.t))
for t in np.linspace(-264,-292,29):
    if t < sol.t[-1]: break
    FF,PP = sol.sol(t)
    print(f"t={t:8.2f} F={FF:.6g} P={PP:.6g}")
# print last few accepted steps
for tt,(FF,PP) in list(zip(sol.t, sol.y.T))[-8:]:
    print("last", tt, FF, PP)
