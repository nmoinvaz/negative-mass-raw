import sys, time
sys.argv=[sys.argv[0]]
sys.path.insert(0,"/Users/nathan/Source/negative-mass-i185/notes/warp")
import conical_eta0 as ce, mpmath as mp
t0=time.time()
r = ce.kappa_cross(1.5, 3000, mp.mpf("0.01"))
print("t", time.time()-t0)
x,f,g = r["end"]
print("x-xs", mp.nstr(x-r["xs"],8), "kap", mp.nstr(f**2-x**2-1,5), "y", mp.nstr(g-x/(2*f),8), "F2", mp.nstr(r["F2"],10))
pred,kz = ce.kz_pred(r)
print("pred", pred, "kz", kz)
pass
