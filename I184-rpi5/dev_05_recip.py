import json, subprocess, sys, mpmath as mp, time
exec(open('dev_pl2.py').read().split("T=mp.mpf(13)/10")[0])
def final(extra, prec='qd'):
    out=run(['--poly','conical','--prec',prec,'--mode','project','--fwd','2','1','--to','1e6','--cp','1e3']+extra)
    e=out[-1]; return e
def G_p(e):
    F,F1=val(e['F']),val(e['F1']); x=mp.mpf(e['x']); return F, x*F1
for label,extra in (('exact',[]),('recip-dd',['--mutate=recip-dd'])):
    a=final(extra); b=final(extra+['--hscale','0.5'])
    Ga,pa=G_p(a); Gb,pb=G_p(b)
    print(label,'steps',a['steps'],b['steps'],'dG %.2e dp %.2e (rel p %.2e)'%(abs(Ga-Gb),abs(pa-pb),abs(pa-pb)/abs(pa)))
# also DD for reference
for label,extra in (('exact dd',[]),):
    a=final(extra,'dd'); b=final(extra+['--hscale','0.5'],'dd')
    Ga,pa=G_p(a); Gb,pb=G_p(b)
    print(label,'dG %.2e dp %.2e'%(abs(Ga-Gb),abs(pa-pb)))
