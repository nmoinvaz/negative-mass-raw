import json, subprocess, sys, time, mpmath as mp
mp.mp.dps = 160
BL='/home/nathan/Source/negative-mass-i184/notes/warp/conical_global/target/release/loglog'
def parts(x,n):
    out=[];r=mp.mpf(x)
    for _ in range(n): f=float(r); out.append(f); r-=mp.mpf(f)
    return ','.join(repr(v) for v in out)
def val(pp): return sum(mp.mpf(v) for v in pp[::-1])
T=mp.mpf(13)/10; g=mp.mpf(7)/10
def ex(eta):
    eta=mp.mpf(eta); tau=mp.log(eta)+T; p=1/tau; q=-p*p
    return g+mp.log(tau), p/eta, (q-p)/eta**2
for mode in ('project','conserve'):
    s0=';'.join(parts(v,8) for v in ex(2))
    t0=time.time()
    r=subprocess.run([BL,'run','--poly','pl2','--prec','od','--mode',mode,'--x0','2','--s0',s0,'--to','1e12','--cp','200,1e3,1e6,1e9'],capture_output=True,text=True,env={'RAYON_NUM_THREADS':'2'})
    out=[json.loads(l) for l in r.stdout.splitlines() if l.startswith('{')]
    print(mode,'time %.1f s'%(time.time()-t0),out[-1]['stop'],out[-1]['steps'],'kt',out[-1]['kt'])
    for o in out:
        if 'cp' in o or o.get('end'):
            x=o.get('cp',o.get('x')); e=ex(x)
            print('  eta %.0e'%x, ' '.join('%.1e'%float(abs((val(o[k])-e[i])/e[i])) for i,k in enumerate(('F','F1','F2'))))
