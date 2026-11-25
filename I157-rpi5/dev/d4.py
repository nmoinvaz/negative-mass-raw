import sys, time, pickle
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import three_scalars_ideal as I
t0 = time.time()
Q, Dt = I.wall_numerators()
print("numerators", time.time()-t0, {k: len(v) for k, v in Q.items()}, "det", len(Dt), flush=True)
pickle.dump(({k: {m: (int(co.numerator), int(co.denominator)) for m, co in v.terms()} for k, v in Q.items()},
             {m: (int(co.numerator), int(co.denominator)) for m, co in Dt.terms()}), open(sys.argv[1]+"/Qdump.pkl", "wb"))
for k, v in sorted(Q.items()):
    cs = sorted(set(m[0] for m in v.monoms())); ss = sorted(set(m[1] for m in v.monoms()))
    print(k, "c-degrees", cs, "S", ss)
for R in ("R1", "R2", "R3"):
    g = I.rung_gens(Q, R)
    print(R, len(g), [(l, len(p), max(sum(m) for m in p.monoms())) for l, p in g][:60])
