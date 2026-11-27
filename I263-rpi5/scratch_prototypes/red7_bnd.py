import sys, time, pickle
from red7_lib import *
I, Fs = pickle.load(open('red7_state5.pkl', 'rb'))
print(len(Fs), "steps:", [n for n, _ in Fs])
t0 = time.time()
Bs = []
for name, F in Fs:
    b = bnd(F)
    Bs.append((name, b))
    print(f"{name:14s} B = {sp.simplify(b) if len(str(b)) < 160 else str(b)[:160]}  ({time.time()-t0:.0f} s)", flush=True)
pickle.dump(Bs, open('red7_bnd.pkl', 'wb'))
