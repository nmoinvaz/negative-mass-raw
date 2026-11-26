import json, subprocess, sys, mpmath as mp, time
exec(open('dev_pl2.py').read().split("T=mp.mpf(13)/10")[0])
def stats(o):
    F,F1,F2=(val(o[k]) for k in ('F','F1','F2')); x=mp.mpf(o.get('cp',o.get('x')))
    p=x*F1; q=x*x*F2+p; w=(q+p*p)/(p*p); t=mp.log(x)
    return dict(G=F,p=p,q=q,w=w,T=1/p-t,g=F+mp.log(abs(p)))
cases=[(2,1),(5,100),(-2,-10),(1.5,1)]
cps=[200,1e3,1e4,1e6,1e9,1e12]
for f,f1 in cases:
  for prec,mode in (('dd','project'),('qd','project'),('dd','conserve')):
    t0=time.time()
    out=run(['--poly','conical','--prec',prec,'--mode',mode,'--fwd',str(f),str(f1),'--to','1e12','--cp',','.join(repr(c) for c in cps)])
    e=out[-1]
    print('(%g,%g) %s %s %s steps %d nrel %.1e pre %.1e  %.1fs'%(f,f1,prec,mode,e['stop'],e['steps'],e['n_rel_max'],e['n_rel_pre_max'],time.time()-t0))
    if prec=='qd' or mode=='conserve' or True:
      for o in out:
        if 'cp' in o or o.get('end'):
            s=stats(o)
            print('   eta %.0e G %.12f p %.6e w %.4e T %.12f g %.12f'%(float(o.get('cp',o.get('x'))),s['G'],s['p'],s['w'],s['T'],s['g']))
