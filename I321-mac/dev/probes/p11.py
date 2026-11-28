import sys
sys.path.insert(0,'.')
import lib1 as L, lib3 as S
import sympy as sp
F3=['dr','dOm','dth']
def run(b,kap,N,ymax,t,log,sym=False,fields=F3):
    P=S.prep(b,kap,N,symbolic=sym)
    tgt=S.target_series(P,'VR',N)
    tgt={k:v for k,v in tgt.items() if sum(k)<=ymax}
    tgt[(2,1)]=tgt.get((2,1),L.DOM.zero)+L.cv(t) if not sym else tgt.get((2,1),L.DOM.zero)+L.DOM.from_sympy(t)
    res=S.solve_affine(P,fields,log,tgt,ymax=ymax)
    out=(res['consistent'],)
    if res['consistent']:
        c=res['cidx'].get(('dth',1,0,1))
        if c is not None:
            Nb=res['Nb'].to_Matrix()
            out+=(res['xp'][c], any(Nb[r,c]!=0 for r in range(Nb.rows)))
    return out
for t in (0,sp.Rational(1,4),sp.Rational(1,2),1):
    print('t',t,'smooth:',run(1,1,6,3,t,False)[0],' log:',run(1,1,6,3,t,True))
tt=sp.Symbol('t')
print('kappa=2/3, F_Pi/2 = 3/4')
for t in (0,sp.Rational(3,4)):
    print('t',t,'smooth:',run(1,sp.Rational(2,3),6,3,t,False)[0],' log:',run(1,sp.Rational(2,3),6,3,t,True))
