import sys, time
sys.path.insert(0,'.')
import lib1 as L, lib2 as M, lib3 as S
import sympy as sp
t0=time.time()
N=int(sys.argv[1]) if len(sys.argv)>1 else 6
fields=sys.argv[2].split(',') if len(sys.argv)>2 else ['dr','dOm','dth']
P=S.prep(1,1,N)
print('prep',time.time()-t0)
cols,cidx,rows=S.build(P,fields,False)
print('cols',len(cols),'rows',len(rows),time.time()-t0)
Mm,_=S.to_dm(rows,len(cols))
Nb=Mm.nullspace()
print('nullity',Nb.shape,time.time()-t0)
ymax=N-2
yr=S.ycols(P,cols,cidx,False,ymax)
Pm,ykeys=S.to_dm(yr,len(cols))
PN=Pm*Nb.transpose()
rel=PN.transpose().nullspace()
print('relations among Y coeffs of smooth solutions (deg<=%d):'%ymax, rel.shape)
rel=rel.rref()[0] if hasattr(rel,'rref') else rel
relL=rel.to_Matrix()
for row in range(relL.rows):
    terms=[(ykeys[c][:2],relL[row,c]) for c in range(relL.cols) if relL[row,c]!=0]
    print(terms)
