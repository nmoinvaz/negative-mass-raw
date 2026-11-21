import sys, time
from exp2 import *
T = (40+20*l)/0.01 + 50
for s in (0.0001+0.12j, -0.0005+0.12j, -0.001+0.12j, -0.001+0.23j, -0.001+0.01j):
    t0 = time.time()
    yr, pr, nr = integ_ray(s, T)
    t1 = time.time()-t0
    yr2, pr2, nr2 = integ_ray(s, T, rtol=1e-13)
    yr3, pr3, nr3 = integ_ray(s, 2*T)
    print(s, 'ray y1', yr, 'q', pr/yr, 'steps', nr, 'time', round(t1, 2), '| rtol13/11-1', abs(yr2/yr-1), '| 2T/T-1', abs(yr3/yr-1), flush=True)
