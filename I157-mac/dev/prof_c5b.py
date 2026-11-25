import time, sympy as sp
src=open('/Users/nathan/Source/negative-mass-raw/I157-mac/ind157.py').read()
head=src[:src.index('# ---- P1:')]
head=head.replace('for arg in sys.argv[1:]','for arg in []')
ns={}; exec(compile(head,'ind157_head','exec'),ns)
c5=src[src.index('# ---- C5:'):src.index('failed = [n for n')]
c5=c5.replace('for trial in range(3):','for trial in range(1):')
c5=c5.replace("    toR = lambda F: RG.from_expr(pt(F, 1, c, S, W))\n","    toR = lambda F: RG.from_expr(pt(F, 1, c, S, W))\n    T=time.time()\n")
c5=c5.replace("    A, dd_ = adj3(h0)\n","    print('pt+toR', round(time.time()-T,1), flush=True); T=time.time()\n    A, dd_ = adj3(h0)\n")
c5=c5.replace("    n22 = (","    print('ricci_core', round(time.time()-T,1), [len(Nc[i][j]) for i in range(3) for j in range(i,3)], flush=True); T=time.time()\n    n22 = (")
c5=c5.replace("    gens = [sp.expand(v) for v in coef.values()]\n","    gens = [sp.expand(v) for v in coef.values()]\n    print('reduce+div', round(time.time()-T,1), len(gens), flush=True); T=time.time()\n")
c5=c5.replace("    gb = sp.groebner(gens, U0, U2, order=\"lex\")\n","    import pickle; pickle.dump((gens, a1), open('gens.pkl','wb')); print('saved', flush=True); raise SystemExit\n")
import random
ns['rnd']=random.Random(1); ns['time']=time; ns['report']=lambda *a: print(*a)
exec(compile(c5,'c5','exec'),ns)
