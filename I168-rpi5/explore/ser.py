from fractions import Fraction as Fr
import time
NM=17
class Ser:
    __slots__=("d",)
    def __init__(s,d=None): s.d={k:v for k,v in (d or {}).items() if v!=0}
    @staticmethod
    def const(c): return Ser({(0,0):c})
    def __add__(a,b):
        if not isinstance(b,Ser): b=Ser.const(b)
        d=dict(a.d)
        for k,v in b.d.items(): d[k]=d.get(k,0)+v
        return Ser(d)
    __radd__=__add__
    def __neg__(a): return Ser({k:-v for k,v in a.d.items()})
    def __sub__(a,b):
        if not isinstance(b,Ser): b=Ser.const(b)
        return a+(-b)
    def __mul__(a,b):
        if not isinstance(b,Ser): return Ser({k:v*b for k,v in a.d.items()})
        d={}
        for (n1,j1),v1 in a.d.items():
            for (n2,j2),v2 in b.d.items():
                n=n1+n2
                if n>NM: continue
                k=(n,j1+j2); d[k]=d.get(k,0)+v1*v2
        return Ser(d)
    __rmul__=__mul__
    def theta(a):
        d={}
        for (n,j),v in a.d.items():
            d[(n,j)]=d.get((n,j),0)-n*v
            if j>0: d[(n,j-1)]=d.get((n,j-1),0)+j*v
        return Ser(d)
    def shift(a,m): return Ser({(n+m,j):v for (n,j),v in a.d.items() if n+m<=NM})
def Nser(G):
    p=G.theta(); q=p.theta(); p2=p*p
    A0=p2*(p2-q)*(p2+q)
    A1=G*G*p2*q*q+4*G*p2*p2*q-2*G*q*q*q+4*p2*p2*p2-3*p2*q*q
    A2=2*(G*(q-p)+p2)*(G*G*q*q+2*G*p2*p+2*G*p2*q+2*p2*p2-q*q)
    return A0+A1.shift(2)+A2.shift(4)
def rank_and_solve(Amat,bvec,ncols):
    """exact Gaussian elimination over Fractions: returns (rank, particular solution or None, nullspace basis)"""
    rows=[list(r)+[b] for r,b in zip(Amat,bvec)]
    piv=[]; r=0
    for c in range(ncols):
        pr=None
        for i in range(r,len(rows)):
            if rows[i][c]!=0: pr=i;break
        if pr is None: continue
        rows[r],rows[pr]=rows[pr],rows[r]
        pv=rows[r][c]; rows[r]=[x/pv for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][c]!=0:
                f=rows[i][c]; rows[i]=[x-f*y for x,y in zip(rows[i],rows[r])]
        piv.append(c); r+=1
    incons=any(all(x==0 for x in row[:ncols]) and row[ncols]!=0 for row in rows)
    if incons: return len(piv),None,None
    sol=[Fr(0)]*ncols
    for i,c in enumerate(piv): sol[c]=rows[i][ncols]
    free=[c for c in range(ncols) if c not in piv]
    null=[]
    for fcol in free:
        v=[Fr(0)]*ncols; v[fcol]=Fr(1)
        for i,c in enumerate(piv): v[c]=-rows[i][fcol]
        null.append(v)
    return len(piv),sol,null
def solve_series(Fi,Cval,KMAX=9,a2=None):
    """stage-by-stage formal solution g = F - Fi = sum a_{n,j} nu^n T^j, exact; free parameter at k=4 set to Cval.
    returns g (Ser), stage log [(k, rank, ncols, nullspace dim, obstruction?)]"""
    Fi=Fr(Fi); g=Ser({(2,0):(-2*Fi if a2 is None else Fr(a2))}); log=[]
    for k in range(3,KMAX+1):
        J=k//2+2; ncols=J+1
        def resid(vec):
            gk=g+Ser({(k,j):vec[j] for j in range(ncols) if vec[j]!=0})
            N=Nser(Ser.const(Fi)+gk)
            low=[(n,j) for (n,j),v in N.d.items() if n<k+6 and v!=0]
            return [N.d.get((k+6,i),Fr(0)) for i in range(ncols+6)],low
        r0,low=resid([Fr(0)]*ncols)
        cols=[]
        for j in range(ncols):
            e=[Fr(0)]*ncols; e[j]=Fr(1); rj,_=resid(e); cols.append([x-y for x,y in zip(rj,r0)])
        Amat=[[cols[j][i] for j in range(ncols)] for i in range(ncols+6)]
        bvec=[-x for x in r0]
        rk,sol,null=rank_and_solve(Amat,bvec,ncols)
        if sol is None: log.append((k,rk,ncols,None,"obstruction",low)); break
        # free parameter: only a_{4,0} expected to be null direction
        if null:
            sol=[s for s in sol]
            if k==4 and len(null)==1 and null[0][0]!=0:
                # set free coordinate: a_{4,0} = Cval
                shift=(Cval-sol[0])/null[0][0]; sol=[s+shift*n for s,n in zip(sol,null[0])]
        g=g+Ser({(k,j):sol[j] for j in range(ncols) if sol[j]!=0})
        log.append((k,rk,ncols,len(null),"ok",low))
    return g,log
if __name__=="__main__":
    t0=time.time()
    g,log=solve_series(1,0)
    for l in log: print(l)
    print({k:str(v) for k,v in sorted(g.d.items())}, time.time()-t0)
    N=Nser(Ser.const(Fr(1))+g)
    print("lowest nonzero residual order:",min(n for (n,j),v in N.d.items() if v!=0))
