import sys, time
sys.path.insert(0,'.')
import lib1 as L, lib2 as M
import sympy as sp
L.setdom(False); L.KAPVAL=sp.Rational(1,1); L.TRUNC=10
t0=time.time()
bg=L.build_background(1,7,False)
env=M.make_env(bg)
E0j,ops=M.load_ops()
print('ops sizes',{k:len(v) for k,v in ops.items()})
for k,e in E0j.items():
    s=M.evaluate(e,env)
    print(k,'E0 residual: lowest nonzero degree',s.mindeg_nonzero(), 'nterms',len(s.d))
print(time.time()-t0)
