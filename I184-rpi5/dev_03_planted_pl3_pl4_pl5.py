import json, subprocess, sys, mpmath as mp
exec(open('dev_pl2.py').read().split("T=mp.mpf(13)/10")[0])
R=mp.mpf
def ex3(eta):
    eta=R(eta); t=mp.log(eta); T=R(13)/10; tau=t+T; c=R(1)/3; sg=1/eta**2
    p=1/tau+c*sg; q=-1/tau**2-2*c*sg
    return R(7)/10+mp.log(tau)-c*sg/2, p/eta, (q-p)/eta**2
def ex4(eta):
    e=R(eta); al=R(7)/10; a=R(13)/10; b=R(2)/5
    v=1+e*e; u=a+b*e
    f=al+u/v; f1=b/v-2*e*u/v**2; f2=-4*e*b/v**2-2*u/v**2+8*e*e*u/v**3
    return f,f1,f2
def ex5(eta):
    e=R(eta); return R(7)/10-1/(3*e**3), 1/e**4, -4/e**5
def go(name,exf,x0,to,cps,mutate=None,precs=(('dd',2),('qd',4)),modes=('project','conserve')):
  for prec,n in precs:
    for mode in modes:
      s0=';'.join(pstr(v,n) for v in exf(x0))
      args=['--poly',name,'--prec',prec,'--mode',mode,'--x0',str(x0),'--s0',s0,'--to',str(to),'--cp',','.join(repr(c) for c in cps)]
      if mutate: args.append('--mutate='+mutate)
      out=run(args)
      row=[]
      for o in out:
        if 'cp' in o or o.get('end'):
          x=o.get('cp',o.get('x')); ex=exf(x)
          e=[abs((val(o[k])-ex[i])/ex[i]) for i,k in enumerate(('F','F1','F2'))]
          row.append('%.0e:%s'%(x,'/'.join('%.0e'%v for v in e)))
      print(name,prec,mode,out[-1]['stop'],'steps',out[-1]['steps'],' '.join(row))
if __name__=='__main__':
    which=sys.argv[1]
    if which=='pl3': go('pl3',ex3,2,1e12,[200,1e3,1e6,1e9,1e12])
    if which=='pl4': go('pl4',ex4,10,1e12,[200,1e3,1e6,1e9,1e12])
    if which=='pl5': go('pl5',ex5,10,3000,[30,100,300,1000])
