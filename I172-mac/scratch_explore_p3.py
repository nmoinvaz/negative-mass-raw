import sys, time, pickle
sys.path.insert(0,'/Users/nathan/Source/negative-mass-i172/notes/warp')
argv=sys.argv; sys.argv=[argv[0]]
import conical_limit as cl
sys.argv=argv
K=int(argv[1])
t0=time.time()
g,log=cl.formal_series(cl.N_theta(), cl.Fi, 2, -2*cl.Fi, K, cl.jlog)
print("time",time.time()-t0, [r['status'] for r in log])
d={k:str(v) for k,v in g.d.items()}
pickle.dump(d,open(f"series_K{K}.pkl","wb"))
for k,v in sorted(g.d.items()): print(k, sp_f if False else v)
