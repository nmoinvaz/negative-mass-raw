import sys, json, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i226/notes/wormhole_evolution")
import constraint_plateau as cp, dn
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs/"
D, hname, fam = int(sys.argv[1]), sys.argv[2], sys.argv[3]
X = {5: 18.0, 6: 15.0}[D]
n = D - 2
sm = json.load(open(RAW + f"D{D}_{fam}_h{hname}/summary.json"))
ck = json.load(open(RAW + f"D{D}_{fam}_h{hname}/constraints.json"))
h = sm["h"]
for side in ("lo", "hi"):
    A = ck[side]["A"]
    t0 = time.time()
    d = cp.make_data(n, h, X, fam, A)
    st, info = cp.stream(d, stop=True)
    (key, (j0, i0)), = info["events"].items()
    st2, info2 = cp.stream(d, stop=True, extra=[i0 + 1])
    k = st2.nx
    pp = st2.region("pp", k=k, Jf=j0)
    mm = st2.region("mm", k=k, Jf=j0)
    print(f"D={D} {fam} h={h:.8f} {side}: event {key} {(j0,i0)} (#40 {ck[side]['event']})  |C++| {pp[0]:.6e} (#40 {ck[side]['pp']:.6e}) at i {pp[1]} j {pp[2]} t {(pp[1]+pp[2])*h/cp.SQ2:.3f}; "
          f"|C--| {mm[0]:.6e} (#40 {ck[side]['mm']:.6e}) at i {mm[1]} j {mm[2]} t {(mm[1]+mm[2])*h/cp.SQ2:.3f}; event t {(i0+j0+1)*h/cp.SQ2:.3f}; sum_terms {pp[3]:.6f} {mm[3]:.6f}; {time.time()-t0:.0f}s", flush=True)
