import sys, time
sys.path.insert(0,'.')
import lib1 as L
import sympy as sp
L.setdom(False); L.KAPVAL=sp.Rational(1,1); L.TRUNC=10
t0=time.time()
bg=L.build_background(1,6,False)
print({k:[str(x) for x in v[:4]] for k,v in bg.items()})
print(time.time()-t0)
