exec(open("dev_floor.py").read().split("class Blow")[0])
import numpy as np
from math import sqrt
cfun = [f for f in cq]
def Qauto(F,P):
    D = P**3*(F*F*P + 2*(1-F*F)*(F+P))
    return (F*P*P - sqrt(D))/(1-F*F)
def Qfull(F,P,t,Q0):
    e = np.exp(t)
    c = [f(F,P,e) for f in cfun]
    Q = Q0
    for _ in range(50):
        g = ((c[0]*Q + c[1])*Q + c[2])*Q + c[3]
        dg = (3*c[0]*Q + 2*c[1])*Q + c[2]
        if dg == 0: break
        dq = g/dg
        Q -= dq
        if abs(dq) <= 1e-15*abs(Q): break
    return Q
def rhs2(t,y):
    F,P = y
    Q0 = Qauto(F,P)
    return [P, Qfull(F,P,t,Q0)]
def ev(t,y): return 1e8 - abs(y[1])
ev.terminal = True
def ev0(t,y): return y[0]
def run(fi,c,tend=-8000.0):
    j = json.loads(subprocess.run([BIN,"walk",str(fi),str(c)],capture_output=True,text=True).stdout)
    f = j["floor"][-1]
    F,F1,F2v = [v[0] for v in f]; x = j["x_last"]
    P = x*F1; Q = x*x*F2v + P
    t0 = np.log(x)
    q0 = Qauto(F,P)
    sol = solve_ivp(rhs2,[t0,tend],[F,P],method="DOP853",rtol=1e-12,atol=1e-30,events=(ev,ev0))
    tc = sol.t_events[1][0] if len(sol.t_events[1]) else None
    tb = sol.t_events[0][0] if len(sol.t_events[0]) else None
    return dict(F=F,P=P,Q=Q,qauto=q0,t0=t0,tc=tc,tb=tb,Pc=(sol.y_events[1][0][1] if tc else None),end=(sol.t[-1],sol.y[:,-1]))
if __name__=="__main__":
    pts = [(0.25,30),(0.25,100),(0.25,300),(0.25,1000),(0.25,3000),(0.5,100),(0.5,300),(0.5,1000),(0.5,3000),(0.75,1000),(0.75,3000)]
    for fi,c in pts:
        r = run(fi,c)
        print(f"({fi},{c}) F={r['F']:.4g} P={r['P']:.4g} Q={r['Q']:.4g} Qauto={r['qauto']:.4g} t_c={r['tc']} P_c={r['Pc']} t_b={r['tb']} end={r['end'][0]:.2f},{r['end'][1]}")
