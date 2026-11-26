import json, subprocess, mpmath as mp
mp.mp.dps=60
BL='/home/nathan/Source/negative-mass-i184/notes/warp/conical_global/target/release/loglog'
def run(args):
    r=subprocess.run([BL,'run']+args,capture_output=True,text=True,env={'RAYON_NUM_THREADS':'2'}); return [json.loads(l) for l in r.stdout.splitlines() if l.startswith('{')]
def val(pp): return sum(mp.mpf(v) for v in pp[::-1])
def parts(x,n):
    out=[];r=mp.mpf(x)
    for _ in range(n): f=float(r); out.append(f); r-=mp.mpf(f)
    return ','.join(repr(v) for v in out)
for f,f1 in ((2,1),(5,10),(5,100)):
    base=None
    for eps in (0, mp.mpf(10)**-30):
        F=mp.mpf(f); F1=mp.mpf(f1)*(1+eps); F2=-F1*F1/F
        s0=';'.join(parts(v,4) for v in (F,F1,F2))
        for mode in ('project',):
            o=run(['--poly','conical','--prec','qd','--mode',mode,'--x0','0','--s0',s0,'--to','200'])[-1]
            st=[val(o[k]) for k in ('F','F1','F2')]
            if eps==0: base=st
            else: print('(%g,%g) %s: perturb F1(0) by 1e-30 relative -> relative change at 200 of F %.1e F1 %.1e F2 %.1e'%(f,f1,mode,*[float(abs(st[i]-base[i])/abs(base[i])) for i in range(3)]))
# project vs conserve DD against QD
for f,f1 in ((5,100),(2,100)):
    q=run(['--poly','conical','--prec','qd','--mode','project','--fwd',repr(float(f)),repr(float(f1)),'--to','200'])[-1]
    for mode in ('project','conserve'):
        n=run(['--poly','conical','--prec','dd','--mode',mode,'--fwd',repr(float(f)),repr(float(f1)),'--to','200'])[-1]
        print('(%g,%g) DD %s vs QD: F1 rel %.1e'%(f,f1,mode,float(abs(val(n['F1'])-val(q['F1']))/abs(val(q['F1'])))))
