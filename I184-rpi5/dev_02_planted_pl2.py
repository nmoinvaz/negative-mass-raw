import json, subprocess, sys, mpmath as mp
mp.mp.dps = 90
CRATE='/home/nathan/Source/negative-mass-i184/notes/warp/conical_global/target/release/loglog'
def parts(x, n):
    out=[]; r=mp.mpf(x)
    for _ in range(n):
        f=float(r); out.append(f); r=r-mp.mpf(f)
    return out
def pstr(x,n): return ','.join(repr(v) for v in parts(x,n))
def run(args):
    r=subprocess.run([CRATE,'run']+args,capture_output=True,text=True,env={'RAYON_NUM_THREADS':'2'})
    if r.returncode: print(r.stderr[-800:]); sys.exit(1)
    return [json.loads(l) for l in r.stdout.splitlines() if l.startswith('{')]
def val(pp): return sum(mp.mpf(v) for v in pp[::-1])
T=mp.mpf(13)/10; g=mp.mpf(7)/10
def exact(eta):
    eta=mp.mpf(eta); t=mp.log(eta); tau=t+T; p=1/tau; q=-p*p
    return g+mp.log(tau), p/eta, (q-p)/eta**2
for prec,n in (('dd',2),('qd',4)):
  for mode in ('project','conserve'):
    x0=2
    F,F1,F2=exact(x0)
    s0=';'.join(pstr(v,n) for v in (F,F1,F2))
    cps=[200,1e3,1e4,1e6,1e9,1e12]
    out=run(['--poly','pl2','--prec',prec,'--mode',mode,'--x0',str(x0),'--s0',s0,'--to','1e12','--cp',','.join(str(c) for c in cps)])
    print(prec,mode,'steps',out[-1]['steps'],out[-1]['stop'],'nrel',out[-1]['n_rel_max'])
    for o in out:
        if 'cp' in o or o.get('end'):
            x=o.get('cp',o.get('x')); 
            ex=exact(x); 
            e=[abs((val(o[k])-ex[i])/ex[i]) for i,k in enumerate(('F','F1','F2'))]
            print('  eta %.0e'%x, ['%.2e'%mp.mpf(v) for v in e])
