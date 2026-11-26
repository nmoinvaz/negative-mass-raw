import json, subprocess, mpmath as mp
mp.mp.dps=60
BL='/home/nathan/Source/negative-mass-i184/notes/warp/conical_global/target/release/loglog'
BO='/home/nathan/Source/negative-mass-i184/notes/warp/conical_global/target/release/conical_global'
def run(b,args):
    r=subprocess.run([b]+args,capture_output=True,text=True,env={'RAYON_NUM_THREADS':'2'}); return [json.loads(l) for l in r.stdout.splitlines() if l.startswith('{')]
def val(pp): return sum(mp.mpf(v) for v in pp[::-1])
mem=[(1.5,1),(1.5,10),(1.5,100),(2,1),(2,10),(2,100),(3,1),(3,10),(3,100),(5,1),(5,10),(5,100),(-2,-100),(-2,-10),(-2,-1)]
print('member   old-vs-QD  newDD-vs-QD   (max relative over F,F1,F2)')
for f,f1 in mem:
    q=run(BL,['run','--poly','conical','--prec','qd','--mode','project','--fwd',repr(float(f)),repr(float(f1)),'--to','200'])[-1]
    n=run(BL,['run','--poly','conical','--prec','dd','--mode','conserve','--fwd',repr(float(f)),repr(float(f1)),'--to','200'])[-1]
    o=run(BO,['fwdstate',repr(float(f)),repr(float(f1)),'200'])[0]
    ref=[val(q[k]) for k in ('F','F1','F2')]
    new=[val(n[k]) for k in ('F','F1','F2')]
    old=[mp.mpf(o['state'][i][0])+mp.mpf(o['state'][i][1]) for i in range(3)]
    eo=[float(abs(old[i]-ref[i])/abs(ref[i])) for i in range(3)]
    en=[float(abs(new[i]-ref[i])/abs(ref[i])) for i in range(3)]
    print('(%g,%g)  old %s   new %s'%(f,f1,' '.join('%.1e'%v for v in eo),' '.join('%.1e'%v for v in en)))
