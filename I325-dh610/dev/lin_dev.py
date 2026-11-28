import sys, os, time, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i325/notes/wormhole_evolution")
import numpy as np
import ellis_spectrum as es
gauss = lambda c, w: (lambda l: np.exp(-((l - c) / w) ** 2 / 2))
out = {}
for n, guess in ((4, 4.6866), (3, 2.985)):
    t0 = time.time()
    f = gauss(3, 0.5)
    ra, rb = es.evolve(n, 0.01, 20.0, f, guess), es.evolve(n, 0.005, 20.0, f, guess)
    t = ra[0]; Y = (4 * rb[1] - ra[1]) / 3; P = rb[2]
    v = np.gradient(Y, t)
    print("n", n, "W2", rb[3], "P", P, "time", time.time() - t0, flush=True)
    for tt in range(2, 17):
        i = int(round(tt / 0.1))
        print(f"  t={tt:2d}  Y/P {Y[i]/P:.5f}  v/P {v[i]/P:.5f}  rate {-(np.log(abs(v[i+5]))-np.log(abs(v[i-5]))):.4f}", flush=True)
    out[n] = dict(t=t.tolist(), Y=Y.tolist(), P=P, w2=rb[3])
json.dump(out, open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i325/46cd26b5-b0e6-44ac-88bf-d82659467bc6/scratchpad/lin_dev.json", "w"))
