import sys, json, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i226/notes/wormhole_evolution")
import constraint_plateau as cp
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs/"
D, hname, fam, side = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4])
amps = [float(x) for x in sys.argv[5].split(",")]
X = {5: 18.0, 6: 15.0}[D]; n = D - 2
sm = json.load(open(RAW + f"D{D}_{fam}_h{hname}/summary.json"))
h = sm["h"]; pst = 0.5 * (sm["lo"] + sm["hi"]); A = pst + side * 1e-8
for a in amps:
    t0 = time.time()
    d = cp.make_data(n, h, X, fam, A)
    st, info = cp.stream(d, stop=True, noise=a * 2.0 ** -52, seed=1)
    ev = {k: list(v) for k, v in info["events"].items()}
    # region: [0, 10]^2
    k = int(round(10.0 / cp.XSTEP)) - 1
    pp = st.region("pp", k=k); mm = st.region("mm", k=k)
    prof = [(round((b + .5) * cp.TW, 2), max(st.tv["pp"][b], st.tv["mm"][b])) for b in range(0, 40, 4)]
    print(f"D={D} {fam} h={h:.6f} side {side:+d} noise {a:g}x2^-52: event {ev}  X10: |C++| {pp[0]:.3e} at (i {pp[1]}, j {pp[2]}, t {(pp[1]+pp[2])*h/cp.SQ2:.2f}) |C--| {mm[0]:.3e} at (i {mm[1]}, j {mm[2]}, t {(mm[1]+mm[2])*h/cp.SQ2:.2f})  {time.time()-t0:.0f}s", flush=True)
    print("    profile t:max|C| " + " ".join(f"{t}:{v:.2e}" for t, v in prof), flush=True)
