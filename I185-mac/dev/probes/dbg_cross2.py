import sys, time
sys.argv=[sys.argv[0]]
sys.path.insert(0,"/Users/nathan/Source/negative-mass-i185/notes/warp")
import conical_eta0 as ce, mpmath as mp
for fi,c in ((1.5,3000),(2.0,3000)):
    t0=time.time()
    r = ce.kappa_cross(fi, c, mp.mpf("0.02"), tau_max=30)
    x,f,g = r["end"]
    print(fi,c,"steps",len(r["hist"]),"t",round(time.time()-t0,1),"x-xs", mp.nstr(x-r["xs"],8), "kap", mp.nstr(f**2-x**2-1,5), "y", mp.nstr(g-x/(2*f),8), "F2", mp.nstr(r["F2"],10), "tau_end", r["hist"][-1][0])
t0=time.time(); j = ce.crate_json(["scan", 1.5, 3000]); print("scan time", time.time()-t0)
