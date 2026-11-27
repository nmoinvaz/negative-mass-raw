import sys, time
sys.path.insert(0, '/home/nathan/Source/negative-mass-i39/notes/wormhole_evolution')
import numpy as np, dn
SQ2 = dn.SQ2
def run(n, h, A, X, w=0.5, xc=3.0, sym=True, stop=True, store=False):
    N = int(round(X / h))
    d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray='+', A=A, xc=xc, w=w)], symmetric=sym)
    return dn.evolve(d, stop=stop, store=store)
print("== symmetric ghost pulse, D=4, h=0.02, X=12 (t up to 17)")
for A in (0.2, 0.1, 0.05, 0.01, -0.01, -0.05, -0.1, -0.2):
    t0 = time.time()
    res = run(2, 0.02, A, 12.0)
    ev = res.events
    key = next(iter(ev), None)
    print(f"A={A:+.3f}: events {ev}" + (f" t_event {dn.event_time(res, key)[2]:.3f}" if key else "") + f"  rows {res.rows_done}  {time.time()-t0:.2f}s  tau_end {res.diag['tau'][-1]:.2f} r_end {res.diag['r'][-1]:.3f}")
