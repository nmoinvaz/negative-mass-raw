import sys, time
sys.path.insert(0,'.')
import lib1 as L, lib2 as M, lib3 as S
import sympy as sp
def go(b,kap,N,fields,kind,log,sym=False,watch=(('dth',1,0,1),)):
    t0=time.time()
    P=S.prep(b,kap,N,symbolic=sym)
    tgt=S.target_series(P,kind,N)
    res=S.solve_affine(P,fields,log,tgt)
    print(f'b={b} kappa={kap} N={N} fields={len(fields)} Y={kind} log={log}: consistent={res["consistent"]}, time {time.time()-t0:.1f}s')
    if res['consistent']:
        Nb=res['Nb']
        for w in watch:
            c=res['cidx'].get(w)
            if c is None: continue
            val=res['xp'][c]
            nbvals=[Nb.to_Matrix()[r,c] for r in range(Nb.shape[0])]
            print('   ',w,'particular value',val,' nullspace spread nonzero:',any(v!=0 for v in nbvals))
        # list all nonzero log (k=1) coefficients of the particular solution at low degree
        lg=[(res['cols'][n],res['xp'][n]) for n in range(len(res['cols'])) if res['cols'][n][3]==1 and res['xp'][n]!=0 and res['cols'][n][1]+res['cols'][n][2]<=2]
        print('    log terms (deg<=2) of particular solution:',lg)
    return res
F3=['dr','dOm','dth']
if __name__=='__main__':
    go(1,1,6,F3,'VR',False)
    go(1,1,6,F3,'VR',True)
    go(1,1,6,F3,'R',False)
    go(1,1,6,F3,'R',True)
