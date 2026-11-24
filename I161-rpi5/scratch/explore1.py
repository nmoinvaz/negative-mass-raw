# scratch exploration (not a run of record): normal geodesics from a straight slice in g = -2 exp(2 H(p) J(q)) dp dq
import numpy as np
def S(x):
    x = np.clip(x, 0, 1); return x**3*(10 - 15*x + 6*x*x)
def dS(x):
    m = (x > 0) & (x < 1); y = np.clip(x, 0, 1); return np.where(m, 30*y*y*(1 - y)**2, 0.0)
h = j = 1.5
H = lambda p: h*S(p); Hp = lambda p: h*dS(p)
J = lambda q: j*S(q); Jp = lambda q: j*dS(q)
def rhs(y):
    p, q, pd, qd, A, At = y
    s_p = Hp(p)*J(q); s_q = H(p)*Jp(q)
    K = 2*Hp(p)*Jp(q)*np.exp(-2*H(p)*J(q))
    return np.array([pd, qd, -2*s_p*pd**2, -2*s_q*qd**2, At, K*A])
def run(S0=6.0, ns=601, T=10.0, dt=0.002):
    s = np.linspace(-S0, S0, ns)
    # slice p+q = -2 c, c=1 : t_M = -sqrt(2)... label: x_M=(q-p)/sqrt2 = s
    p0 = -1.0 - s/np.sqrt(2)*1.0; q0 = -1.0 + s/np.sqrt(2)*1.0
    y = np.array([p0, q0, np.full(ns, 1/np.sqrt(2)), np.full(ns, 1/np.sqrt(2)), np.ones(ns), np.zeros(ns)])
    out = [y.copy()]; n = int(T/dt)
    for i in range(n):
        k1 = rhs(y); k2 = rhs(y + dt/2*k1); k3 = rhs(y + dt/2*k2); k4 = rhs(y + dt*k3)
        y = y + dt/6*(k1 + 2*k2 + 2*k3 + k4)
        if (i + 1) % 500 == 0: out.append(y.copy())
    return s, np.array(out)
s, out = run()
print("slices", out.shape)
ds = s[1]-s[0]
for k, y in enumerate(out):
    A, At = y[4], y[5]
    L = np.sum(A)*ds; bplus = -np.sum(At)*ds
    # normalization check: 2 e^{2 sigma} pd qd = 1
    nrm = 2*np.exp(2*H(y[0])*J(y[1]))*y[2]*y[3]
    th = At/A
    nz = np.where(np.abs(th) > 1e-9)[0]
    print(f"t={k*1.0:5.1f} L={L:9.4f} b_+={bplus:9.5f} minA={A.min():.4f} norm_err={np.abs(nrm-1).max():.1e} theta!=0 for s in [{s[nz].min() if len(nz) else 0:.2f},{s[nz].max() if len(nz) else 0:.2f}]")
