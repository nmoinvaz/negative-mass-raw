import sys, time
sys.path.insert(0,'.')
import lib1 as L, lib2 as M, lib3 as S
import sympy as sp
def run(b,kap,N,fields,sym=False,ymax=None):
    t0=time.time()
    P=S.prep(b,kap,N,symbolic=sym)
    cols,cidx,rows=S.build(P,fields,False)
    Mm,_=S.to_dm(rows,len(cols))
    Nb=Mm.nullspace()
    ymax=ymax or N-2
    yr=S.ycols(P,cols,cidx,False,ymax)
    Pm,ykeys=S.to_dm(yr,len(cols))
    PN=Pm*Nb.transpose()
    rel=PN.transpose().nullspace().rref()[0].to_Matrix()
    out=[]
    for row in range(rel.rows):
        out.append({ykeys[c][:2]:rel[row,c] for c in range(rel.cols) if rel[row,c]!=0})
    print(f'b={b} kappa={kap} N={N} fields={fields} nullity={Nb.shape[0]} time={time.time()-t0:.1f}s')
    for o in out: print('  ',o)
    return out
if __name__=='__main__':
    run(1,sp.Rational(2,3),6,['dr','dOm','dth'])
    run(2,sp.Rational(1,3),6,['dr','dOm','dth'])
    run(1,1,7,['dr','dOm','dth'])
    run(1,1,5,['dr','dOm','dth','hv','hu'])
